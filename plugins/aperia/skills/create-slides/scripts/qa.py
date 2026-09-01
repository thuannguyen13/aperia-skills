#!/usr/bin/env python3
"""QA an Aperia HTML slide deck.

    python3 scripts/qa.py <slug>.html

Checks the rules that are objectively checkable: tone, notes, density,
palette, graphic-element handling, chart discipline, undrawn sequences,
and placeholders.
Exits non-zero if any ERROR is found. WARN items are judgement calls:
read them, then decide.

It cannot check what the slide *looks* like. Still open the file.
"""
import re
import sys
from collections import Counter

try:
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("pip install beautifulsoup4 --break-system-packages")

ALWAYS_DARK = ["s-cover", "s-agenda", "s-section", "s-statement", "s-quote", "s-end"]
NO_FOOTER = ["s-cover", "s-section", "s-end"]
CHARTS = ["colchart", "bchart", "stack", "donut", "lchart", "gantt", "tline-bars"]
DIAGRAMS = ["flow", "gantt", "tline-bars"]
# Ordering words: the slide is walking through something in sequence.
ORDER = re.compile(r"\b(first|firstly|then|next|afterwards?|subsequently|finally|lastly|"
                   r"step \d|steps?|stages?|phases?|followed by|begins? with|ends? with)\b", re.I)
# Sequence nouns: only meaningful in a heading. In body copy "analyst workflow"
# is a noun, not a process, so these alone must never fire the check.
SEQ_NOUN = re.compile(r"\b(journey|pipeline|workflow|process|lifecycle|end.to.end|hand.?off)\b", re.I)
DATA_LABELS = {"col-val", "bval", "dlbl", "axlbl", "seg", "stack-legend", "gantt-bar",
               "gantt-axis", "col-lbl", "tline-bar", "s-num", "chart-note", "donut-val",
               "donut-lbl", "stat-val", "s-meta", "flow-node"}

PALETTE = {
    # brand
    "002f67", "004785", "0072bc", "7ed3f7", "c8eaf5", "004583",
    "000000", "ffffff", "fff", "58595b", "a7a9ac", "f1f2f2",
    # theme-internal neutrals and blue tints defined in slides.css
    "1c1f24", "e3e6ea", "cfe0f0", "9fbedb", "a8c4dd", "3a8fd1", "6cb0e0",
    "eaf3fb", "bfdcf0", "eafaff", "f4f8fc", "f6fafe", "0a1e38",
    # sentiment (callouts and badges only)
    "16a34a", "d97706", "dc2626", "15803d", "bbf7d0", "b45309",
    "fde68a", "fffbeb", "fef2f2", "fecaca", "f0fdf4",
}

BANNED = [
    (r"lorem|ipsum", "lorem placeholder"),
    (r"\[insert|\bTBD\b|\bTODO\b|XXX", "unfilled placeholder"),
    (r"Click to edit", "PowerPoint placeholder text"),
    (r"•", "literal bullet character, use ul.s-list, the marker is CSS"),
]

STOP = {"a", "an", "and", "as", "at", "but", "by", "for", "from", "in", "into", "nor",
        "of", "on", "onto", "or", "over", "per", "the", "to", "up", "via", "with",
        "vs", "is", "it", "we", "our", "not", "than", "that", "if", "so", "yet"}

errs, warns = [], []


def err(slide, msg):
    errs.append(f"  [{slide}] {msg}")


def warn(slide, msg):
    warns.append(f"  [{slide}] {msg}")


def slide_words(slide):
    """Visible narrative words: excludes notes, footer, and chart data labels."""
    clone = BeautifulSoup(str(slide), "html.parser")
    for tag in clone.select("aside.notes, .s-foot, svg"):
        tag.decompose()
    for tag in list(clone.find_all(True)):
        if tag.decomposed or tag.parent is None:
            continue
        if DATA_LABELS & set(tag.get("class") or []):
            tag.decompose()
    return len(clone.get_text(" ", strip=True).split())


def main(path):
    raw = open(path, encoding="utf-8").read()
    soup = BeautifulSoup(raw, "html.parser")
    slides = soup.select(".slide")

    if not slides:
        sys.exit("No .slide elements found, is this an Aperia slide deck?")

    # ---- document level ----
    if "fonts.googleapis.com" not in raw or "Inter" not in raw:
        errs.append("  [doc] Inter is not loaded from Google Fonts")
    if "--slide-w:1920px" not in raw.replace(" ", ""):
        errs.append("  [doc] slides.css canvas variables missing, theme not pasted in full")
    if not soup.select("#ap-logo"):
        errs.append("  [doc] brand sprite missing, #ap-logo symbol not defined")
    if not soup.select_one(".deck"):
        errs.append("  [doc] no .deck container")
    for s in slides:
        if not (s.parent and "stage" in s.parent.get("class", [])):
            errs.append("  [doc] a .slide is not wrapped in a .stage")
            break

    ids = Counter(t["id"] for t in soup.find_all(id=True))
    for i, n in ids.items():
        if n > 1:
            errs.append(f"  [doc] duplicate id '{i}' used {n} times")

    for hexv in set(m.lower() for m in re.findall(r"#([0-9a-fA-F]{3,6})\b", raw)):
        if hexv not in PALETTE and not re.fullmatch(r"[a-f0-9]{6}", hexv) is None:
            if hexv not in PALETTE:
                errs.append(f"  [doc] off-palette color #{hexv}")

    deck_text = soup.select_one(".deck").get_text(" ", strip=True) if soup.select_one(".deck") else ""
    for pat, label in BANNED:
        if re.search(pat, deck_text, re.I):
            errs.append(f"  [doc] {label}")

    n = len(slides)
    if n < 4:
        warns.append(f"  [doc] only {n} slides, thin for a deck")
    if n > 24:
        warns.append(f"  [doc] {n} slides, over the 24-slide guide, condense or split")

    dark = sum(1 for s in slides if "s-dark" in s.get("class", []))
    if dark == n:
        errs.append("  [doc] every slide is dark, unreadable, text slides must be light")
    if dark == 0:
        errs.append("  [doc] no dark slides, cover, sections and closer are always dark")
    elif dark / n > 0.65:
        warns.append(f"  [doc] {dark} of {n} slides are dark, light layouts should carry the text")

    # ---- slide level ----
    for i, s in enumerate(slides, 1):
        cls = set(s.get("class", []))
        tag = f"{i:02d}"
        is_dark = "s-dark" in cls
        layout = next((c for c in ALWAYS_DARK if c in cls), None)

        if layout and not is_dark:
            err(tag, f"{layout} must be dark (add s-dark), this is fixed, not a default")

        notes = s.select_one("aside.notes")
        if not notes:
            err(tag, "no presenter notes, every slide needs them")
        elif len(notes.get_text(strip=True).split()) < 8:
            warn(tag, "presenter notes are a fragment, write what the presenter says")

        if "s-end" in cls:
            body = s.select_one(".s-body")
            extra = [c.name for c in body.find_all(recursive=False) if c.name != "h1"] if body else []
            if extra:
                err(tag, f"closing slide carries {', '.join(extra)}, heading only, the rest is spoken")

        needs_foot = not (set(NO_FOOTER) & cls)
        foot = s.select_one(".s-foot")
        if needs_foot and not foot:
            err(tag, "missing .s-foot (logo + slide number)")
        if foot:
            if not foot.select_one('use[href="#ap-logo"]'):
                err(tag, ".s-foot has no logo")
            if not foot.select_one(".s-num"):
                err(tag, ".s-foot has no slide number")

        # graphic element
        for shp in s.select("svg.shape"):
            if shp.get("preserveaspectratio", "").lower() != "xmaxymin meet":
                err(tag, 'graphic element needs preserveAspectRatio="xMaxYMin meet"')
            st = (shp.get("style") or "").lower()
            if "rotate" in st or "scalex(-" in st or "scale(-" in st:
                err(tag, "graphic element is rotated or flipped, never allowed")
            if "max-width" in st:
                err(tag, "graphic element must not be width-capped, height drives it")

        # density
        words = slide_words(s)
        bullets = s.select("ul.s-list > li")
        if len(bullets) > 6:
            err(tag, f"{len(bullets)} bullets, over six means this is two slides")
        if words > 85:
            err(tag, f"{words} words of body copy, split this slide")
        elif words > 55 and not is_dark:
            warn(tag, f"{words} words of body copy, trim toward 40")

        # a sequence described in bullets should have been drawn
        bullet_text = " ".join(b.get_text(" ", strip=True) for b in bullets)
        head_text = " ".join(h.get_text(" ", strip=True) for h in s.select("h1, h2"))
        distinct_order = {m.group(0).lower() for m in ORDER.finditer(bullet_text + " " + head_text)}
        looks_sequential = len(distinct_order) >= 2 or SEQ_NOUN.search(head_text)
        if len(bullets) >= 3 and looks_sequential:
            if not any(s.select_one("." + d) for d in DIAGRAMS):
                warn(tag, "reads like a sequence but is bulleted, draw it with .flow or .gantt")

        # charts
        chart_here = [c for c in CHARTS if s.select_one("." + c)]
        insights = s.select(".insight")
        if chart_here and not insights:
            err(tag, f"chart ({chart_here[0]}) with no .insight, call out the one takeaway")
        if len(insights) > 1:
            warn(tag, f"{len(insights)} insight lines, one chart, one insight")
        for d in s.select(".donut"):
            stops = len(re.findall(r"var\(--", d.get("style", "")))
            if stops > 3:
                err(tag, f"donut with {stops} segments, 4+ parts belong in a .stack bar")

        # canvas rule
        for t in s.find_all(style=True):
            if re.search(r"font-size:\s*[\d.]+(vw|vh|%)|clamp\(", t["style"]):
                err(tag, "viewport-relative font size inside a slide, the canvas is fixed 1920x1080")

        for img in s.select("img"):
            if img.get("alt") is None:
                warn(tag, "image without an alt attribute")

        # Title Case on headings
        for h in s.select("h1, h2, h3"):
            txt = h.get_text(" ", strip=True)
            if len(txt.split()) < 3 or txt.isupper():
                continue
            bad = [w for w in txt.split()[1:]
                   if w[:1].islower() and w.lower() not in STOP and len(w) > 3 and w.isalpha()]
            if len(bad) >= 2:
                warn(tag, f'heading may not be Title Case: "{txt[:58]}"')

    # ---- report ----
    print(f"Aperia slide QA, {path}")
    print(f"{n} slides · {dark} dark · {n - dark} light\n")
    if errs:
        print(f"ERRORS ({len(errs)})")
        print("\n".join(errs), "\n")
    if warns:
        print(f"WARNINGS ({len(warns)})")
        print("\n".join(warns), "\n")
    if not errs and not warns:
        print("Clean. Now open it in a browser and look at every slide.")
    elif not errs:
        print("No errors. Review the warnings, then open it and look at every slide.")
    return 1 if errs else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: qa.py <deck.html>")
    sys.exit(main(sys.argv[1]))
