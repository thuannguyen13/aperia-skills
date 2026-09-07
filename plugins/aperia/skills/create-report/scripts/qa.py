#!/usr/bin/env python3
"""QA an Aperia HTML report.

    python3 scripts/qa.py <slug>.html

Checks the rules that are objectively checkable: the assembled marker and
the toolkits it names, the brand sprite, skip link, nav and drawer, footer,
section labels, palette, duplicate ids, placeholders, dashes, classes no
stylesheet defines, and the delivery-plan rules.
Exits non-zero if any ERROR is found. WARN items are judgement calls:
read them, then decide.

It cannot check what the page *looks* like, at a narrow viewport or in
print. Still open the file when a browser is available.
"""
import glob
import importlib.util
import os
import re
import sys
from collections import Counter

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("pip install beautifulsoup4 --break-system-packages")

HERE = os.path.dirname(os.path.abspath(__file__))
# The palette is read from the brand layer, not copied here: tokens.css plus
# the approved blocks in DEVIATIONS.md, through brand/palette.py in the
# apply-branding skill beside this one.
# Clients name a mounted skill folder differently, apply-branding in Claude
# Code and aperia:apply-branding on Claude Desktop, so look for both.
_SKILLS = os.path.join(HERE, "..", "..")
_LAYER = next((d for d in [os.path.join(_SKILLS, "apply-branding")] + sorted(glob.glob(os.path.join(_SKILLS, "*:apply-branding")))
               if os.path.isdir(d)), None)
if _LAYER is None:
    sys.exit("qa.py: the apply-branding skill, which holds the brand layer, is not "
             f"installed beside create-report under {os.path.normpath(_SKILLS)}.")
BRAND_DIR = os.path.join(_LAYER, "brand")
_PALETTE = os.path.join(BRAND_DIR, "palette.py")
_spec = importlib.util.spec_from_file_location("palette", _PALETTE)
palette = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(palette)

PALETTE = palette.load(BRAND_DIR)

# Classes that mean the charts toolkit is in use; the marker must name it.
CHART_CLASSES = {"colchart", "bchart", "stack", "donut", "lchart", "heatmap", "cf", "spark",
                 "cf-line", "cf-bar", "cf-area", "hm-grid", "bullet", "slope", "dumbbell"}
ICON_CLASSES = {"icon", "iblock"}

BANNED = [
    (r"lorem|ipsum", "lorem placeholder"),
    (r"\[insert|\bTBD\b|\bTODO\b|XXX", "unfilled placeholder"),
]

errs, warns = [], []


def err(where, msg):
    errs.append(f"  [{where}] {msg}")


def warn(where, msg):
    warns.append(f"  [{where}] {msg}")


def defined_classes(soup):
    """Every class name any <style> block in the document selects."""
    names = set()
    for style in soup.find_all("style"):
        names.update(re.findall(r"\.([A-Za-z_][\w-]*)", style.get_text()))
    return names


def visible_text(soup):
    clone = BeautifulSoup(str(soup), "html.parser")
    for tag in clone.select("style, script, svg, template"):
        tag.decompose()
    return clone.get_text(" ", strip=True)


def main(path):
    raw = open(path, encoding="utf-8").read()
    soup = BeautifulSoup(raw, "html.parser")
    body = soup.body
    if body is None or not soup.find_all("section"):
        sys.exit("No <section> inside <body>, is this an Aperia report?")

    # ---- head and marker ----
    if "fonts.googleapis.com" not in raw or "Inter" not in raw:
        err("doc", "Inter is not loaded from Google Fonts")
    for tag in soup.find_all(["link", "script"]):
        src = tag.get("href") or tag.get("src") or ""
        if src.startswith("http") and "fonts.g" not in src:
            err("doc", f"external dependency beyond Google Fonts: {src}")

    marker = soup.find("style", attrs={"data-aperia": True})
    bare = re.search(r"<style>\s*/\*\s*@aperia\s+([\w \t-]+?)\s*\*/\s*</style>", raw)
    if marker is None:
        if bare:
            err("doc", "the style marker is empty, run assemble.py")
        else:
            err("doc", 'no style marker, add <style>/* @aperia report */</style> in <head> and run assemble.py')
        words = set()
    else:
        words = set(marker["data-aperia"].split())
        if "report" not in words:
            err("doc", f'the marker was assembled as "{marker["data-aperia"]}", not report')
        if len(soup.find_all("style", attrs={"data-aperia": True})) > 1:
            err("doc", "more than one assembled style block")

    used = Counter(c for t in soup.find_all(class_=True) for c in t.get("class", []))
    if marker is not None:
        has_charts = bool(CHART_CLASSES & set(used))
        has_icons = bool(ICON_CLASSES & set(used))
        if has_charts and "charts" not in words:
            err("doc", "chart classes used but the marker does not name charts, add it and re-run assemble.py")
        if has_icons and "icons" not in words:
            err("doc", "icon classes used but the marker does not name icons, add it and re-run assemble.py")
        if "charts" in words and not has_charts:
            warn("doc", "the marker names charts but no chart is used, drop the word and re-run assemble.py")
        if "icons" in words and not has_icons:
            warn("doc", "the marker names icons but no icon is used, drop the word and re-run assemble.py")

    # ---- chrome ----
    first = body.find(True)
    skip = soup.select_one("a.skip-link")
    if skip is None:
        err("doc", "no skip link")
    elif first is not skip:
        err("doc", "the skip link is not the first element in <body>")
    if skip is not None and soup.find(id=(skip.get("href") or "#")[1:]) is None:
        err("doc", "the skip link target does not exist")
    if not soup.select_one("#ap-logo"):
        err("doc", "brand sprite missing, #ap-logo symbol not defined; the nav and footer reference it with <use>")
    for logo in soup.select("svg.logo"):
        if not logo.get("aria-label"):
            err("doc", 'a logo without aria-label="Aperia"')

    nav = soup.find("nav")
    if nav is None:
        err("doc", "no <nav>")
    else:
        if not nav.select_one(".nav-brand"):
            err("nav", "no .nav-brand logo link")
        if not nav.select_one(".nav-burger"):
            err("nav", "no hamburger button")
        drawer = nav.find_next_sibling(True)
        if drawer is None or "nav-drawer" not in drawer.get("class", []):
            err("nav", "the .nav-drawer is not the element right after </nav>")
        links = [a.get("href", "") for a in nav.select(".nav-links a")]
        if not links:
            err("nav", "no links in .nav-links")
        section_ids = {s.get("id") for s in soup.find_all("section") if s.get("id")}
        for href in links:
            if not href.startswith("#") or soup.find(id=href[1:]) is None:
                err("nav", f"link {href} resolves to nothing")
        missing = section_ids - {h[1:] for h in links}
        if missing:
            warn("nav", f"sections with an id but no nav link: {', '.join(sorted(missing))}")
        if drawer is not None and "nav-drawer" in drawer.get("class", []):
            dl = {a.get("href", "") for a in drawer.select("a")}
            if dl != set(links):
                err("nav", "drawer links do not mirror the nav links")
    if not soup.find(id="burger") or not soup.find(id="drawer"):
        err("nav", "burger and drawer ids missing, the drawer script keys on them")

    hero = soup.select_one("header.hero")
    if hero is None:
        err("doc", "no header.hero")
    else:
        em = hero.select_one("h1 em")
        if em is not None:
            if re.search("[\u2013\u2014-]", em.get_text()):
                err("hero", "dash in the <em> subtitle")
            if em.get("style"):
                err("hero", "inline style on the <em> subtitle")

    footer = soup.find("footer")
    if footer is None:
        err("doc", "no <footer>")
    else:
        ftext = footer.get_text(" ", strip=True)
        if "·" not in ftext:
            warn("footer", "footer line should read Title · Subtitle · Month Year")

    for s in soup.find_all("section"):
        sid = s.get("id") or "section"
        if not s.select_one(".sec-label"):
            warn(sid, "section without a sec-label eyebrow")
        lbl = s.select_one(".sec-label")
        if lbl is not None and re.match(r"^\s*(\d+|[ivx]+)[.)]?\s", lbl.get_text(), re.I):
            err(sid, "numbered sec-label, sections are not numbered")
        if s.select_one("hr"):
            err(sid, "divider line, whitespace only between sections")
    if not soup.find(id="main"):
        err("doc", 'no element with id="main"')

    # ---- document level ----
    ids = Counter(t["id"] for t in soup.find_all(id=True))
    for i, n in ids.items():
        if n > 1:
            err("doc", f"duplicate id '{i}' used {n} times")

    for hexv in sorted(palette.colors_in(raw) - PALETTE):
        err("doc", f"off-palette color #{hexv}")

    text = visible_text(body)
    for pat, label in BANNED:
        if re.search(pat, text, re.I):
            err("doc", label)
    if re.search("[\u2013\u2014]", text):
        err("doc", "em or en dash in the copy, use a colon, a comma or two sentences")

    defined = defined_classes(soup)
    unknown = sorted(c for c in used if c not in defined)
    if unknown:
        warn("doc", f"classes no stylesheet defines: {', '.join(unknown)}")

    for t in soup.find_all(style=True):
        if "transform" in t["style"] and "scale" in t["style"]:
            err("doc", "transform:scale in an inline style, never scale a grid to fit")
    for img in soup.select("img"):
        if img.get("alt") is None:
            warn("doc", "image without an alt attribute")
    if "piechart" in used or "pie" in used:
        err("doc", "pie chart, the library has no pie: use stack, treemap or a donut")

    # ---- delivery plan ----
    scripts = " ".join(s.get_text() for s in soup.find_all("script"))
    has_gantt = "gantt" in used
    has_sgantt = "sgantt" in used
    if has_gantt and has_sgantt:
        err("plan", "both gantt and sgantt, one report carries one")
    mounts = [t for t in soup.find_all(id=re.compile(r"^(m|g|f|fc|ct|env)-"))]
    if (has_sgantt or mounts) and not re.search(r"\bDATA\s*=", scripts):
        err("plan", "plan mount points present but no DATA object in a script")
    for sg in soup.select(".sgantt"):
        wrap = sg.find_parent(class_="wrap")
        if wrap is not None and "full" in wrap.get("class", []):
            err("plan", "hand-added full on the plan wrap, the script adds it when the grid needs it")
        if wrap is not None:
            others = [c for c in wrap.find_all(True, recursive=False)
                      if not (set(c.get("class", [])) & {"sg-bar", "sg-legend", "sg-counts", "sgantt", "sg-cap", "sub-h", "sub-note"})]
            if others:
                warn("plan", "the plan wrap holds more than the plan block")
        style = sg.get("style", "")
        if "max-height" in style or "overflow" in style:
            err("plan", "max-height or overflow on .sgantt, either one stops the header sticking")
    if has_sgantt and "syncScrollbox" not in scripts:
        err("plan", "sgantt without the render script from references/interactive.html")
    if "concerns" not in used and "concern" in scripts.lower():
        warn("doc", "accordion script shipped but no concerns block uses it")

    # ---- report ----
    n = len(soup.find_all("section"))
    print(f"Aperia report QA, {path}")
    print(f"{n} sections\n")
    if errs:
        print(f"ERRORS ({len(errs)})")
        print("\n".join(errs), "\n")
    if warns:
        print(f"WARNINGS ({len(warns)})")
        print("\n".join(warns), "\n")
    if not errs and not warns:
        print("Clean. Now open it in a browser, narrow it, and print it.")
    elif not errs:
        print("No errors. Review the warnings, then open it in a browser, narrow it, and print it.")
    return 1 if errs else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1]))
