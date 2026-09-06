#!/usr/bin/env python3
"""Render the snippet libraries as one labelled, navigable gallery.

The libraries are copy-paste files: every component is introduced by a

    <!-- ========== NAME ========== -->

comment, which a browser does not render. Open one directly and you get
unstyled markup; concatenate all three and you get thousands of pixels of
unlabelled components with no way to map what you see back to a class name.
This reads those comments back out and builds a page where each component
carries its own name, an anchor and the classes its markup uses, so the
component library can be reviewed by eye.

The page is generated, never hand-edited, so it cannot drift from what the
model actually copies. Nothing under plugins/ is read for anything but its
contents, and nothing there is written, so the snippet libraries stay exactly
as the skills read them.

This is a maintainer tool and deliberately lives outside plugins/: a Desktop
install mounts the skills, and the gallery is for whoever is working on them.

It carries the same @aperia marker a real document does and is filled by the
plugin's own assemble.py, so the components are styled by the layers a report
would get, not by anything this script knows about the brand.

Usage: python3 scripts/gallery.py [out.html]     (default: gallery.html)
"""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "aperia"
LAYERS = Path("skills") / "apply-branding"
UI = PLUGIN / LAYERS / "ui-components"

# Section names are written as they should read, so they are used verbatim.
# A component is introduced by <!-- ===== NAME ===== -->, and a group heading
# by the same opener followed by prose and a plain -->. The name sits on one
# line between two runs of '=' and contains no '=' itself, which is what keeps
# each file's own banner header, a bare run of '=' on its first line, from
# matching: the header addresses whoever writes a document, not whoever
# reviews the components, so it is not in the gallery.
SECTION = re.compile(r"<!--\s*={5,}\s*([^\n=]+?)\s*={5,}\s*(?:-->|\n(.*?)-->)", re.S)
CLASSES = re.compile(r'class="([^"]+)"')

# Source file, the marker word that injects its stylesheet, and when it applies.
SOURCES = [
    ("base/structure.html", None, "Always injected"),
    ("base/emphasis.html", None, "Always injected"),
    ("base/tables.html", None, "Always injected"),
    ("base/charts.html", None, "Always injected"),
    ("base/timelines.html", None, "Always injected"),
    ("charts/trend.html", "charts", "Add `charts` to the marker"),
    ("charts/compare.html", "charts", "Add `charts` to the marker"),
    ("charts/proportion.html", "charts", "Add `charts` to the marker"),
    ("charts/intensity.html", "charts", "Add `charts` to the marker"),
    ("icons/index.html", "icons", "Add `icons` to the marker"),
]

CHROME = """
<style>
:root { --gal-ink:#1c1f24; --gal-mute:#6b7280; --gal-line:#e3e6ea; --gal-bg:#fbfbfc }
body { margin:0; background:var(--gal-bg); color:var(--gal-ink);
       font:14px/1.5 Inter,-apple-system,system-ui,sans-serif }
.gal { display:grid; grid-template-columns:17rem minmax(0,1fr); align-items:start }
.galnav { position:sticky; top:0; max-height:100vh; overflow:auto;
          padding:1.5rem 1rem 3rem; border-right:1px solid var(--gal-line); background:#fff }
.galnav h1 { font-size:.75rem; letter-spacing:.08em; text-transform:uppercase;
             color:var(--gal-mute); margin:0 0 .4rem }
.galnav .built { font-size:.7rem; color:var(--gal-mute); margin:0 0 1rem }
.navgroup { display:flex; justify-content:space-between; font-weight:600;
            font-size:.78rem; margin:1.25rem 0 .4rem; color:#002F67 }
.navgroup span { color:var(--gal-mute); font-weight:400 }
.galnav ul { list-style:none; margin:0; padding:0 }
.galnav li a { display:block; padding:.2rem 0 .2rem .6rem; color:var(--gal-mute);
               text-decoration:none; font-size:.78rem; border-left:2px solid transparent }
.galnav li a:hover { color:#0072BC; border-left-color:#0072BC }
.galmain { padding:1.5rem 2rem 6rem; min-width:0 }
.layer h2 { font-size:1rem; margin:2.5rem 0 .2rem; color:#002F67 }
.layer .note { margin:0 0 .75rem; color:var(--gal-mute); font-size:.78rem }
.group { margin:1.5rem 0 1rem; padding-left:.75rem; border-left:3px solid #0072BC }
.group h4 { margin:0 0 .2rem; font-size:.85rem; color:#002F67 }
.group p { margin:0; font-size:.78rem; color:var(--gal-mute); max-width:62ch }
.galnav li.grouprow a { color:#002F67; font-weight:600; margin-top:.4rem }
.item { background:#fff; border:1px solid var(--gal-line); border-radius:.5rem;
        margin:0 0 1.25rem; overflow:hidden }
.item > header { padding:.7rem 1rem; border-bottom:1px solid var(--gal-line);
                 display:flex; flex-wrap:wrap; gap:.5rem 1rem; align-items:baseline }
.item h3 { margin:0; font-size:.9rem; font-weight:600 }
.chips { display:flex; flex-wrap:wrap; gap:.3rem }
.chips code { font:11px/1.6 ui-monospace,SFMono-Regular,Menlo,monospace;
              color:var(--gal-mute); background:#f4f5f7; border-radius:3px; padding:0 .35rem }
.chips .more { color:var(--gal-mute); font-size:11px; align-self:center }
.preview { padding:1.5rem; overflow-x:auto }
.item details { border-top:1px solid var(--gal-line) }
.item summary { padding:.5rem 1rem; cursor:pointer; font-size:.76rem; color:var(--gal-mute) }
.item pre { margin:0; padding:0 1rem 1rem; overflow-x:auto;
            font:12px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace }
@media (max-width:900px) {
  .gal { grid-template-columns:1fr }
  .galnav { position:static; max-height:none; border-right:0;
            border-bottom:1px solid var(--gal-line) }
}
</style>
"""


def sections(path):
    """[(kind, name, body)] for one snippet library, in file order.

    kind is "group" for a heading, whose body is its prose, or "item" for a
    component, whose body is the markup up to the next block.
    """
    text = path.read_text()
    blocks = list(SECTION.finditer(text))
    found = []
    for n, m in enumerate(blocks):
        name, prose = m.group(1).strip(), m.group(2)
        if prose:
            found.append(("group", name, " ".join(prose.split())))
            continue
        end = blocks[n + 1].start() if n + 1 < len(blocks) else len(text)
        found.append(("item", name, text[m.end():end]))
    return found


def classes_in(markup):
    """The distinct class names a block uses, in first-seen order."""
    seen = []
    for group in CLASSES.findall(markup):
        for name in group.split():
            if name not in seen:
                seen.append(name)
    return seen


def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def build():
    """(nav html, body html, marker words, per-file counts)."""
    nav, body, words, counts = [], [], ["page"], []
    for rel, flag, note in SOURCES:
        path = UI / rel
        if not path.exists():
            sys.exit(f"gallery: missing {path.relative_to(ROOT)}")
        if flag and flag not in words:
            words.append(flag)
        found = sections(path)
        items = [b for b in found if b[0] == "item"]
        counts.append((rel, len(items)))
        key = slug(rel.rsplit("/", 1)[-1].removesuffix(".html"))
        nav.append(f'<div class="navgroup">{html.escape(rel)}'
                   f'<span>{len(items)}</span></div><ul>')
        body.append(f'<section class="layer"><h2 id="{key}">{html.escape(rel)}</h2>'
                    f'<p class="note">{html.escape(note)}</p></section>')
        for kind, name, payload in found:
            anchor = f"{key}-{slug(name)}"
            if kind == "group":
                nav.append(f'<li class="grouprow"><a href="#{anchor}">'
                           f'{html.escape(name)}</a></li>')
                body.append(f'<div class="group" id="{anchor}">'
                            f'<h4>{html.escape(name)}</h4>'
                            f'<p>{html.escape(payload)}</p></div>')
                continue
            used = classes_in(payload)
            chips = "".join(f"<code>.{html.escape(c)}</code>" for c in used[:12])
            if len(used) > 12:
                chips += f'<span class="more">+{len(used) - 12}</span>'
            nav.append(f'<li><a href="#{anchor}">{html.escape(name)}</a></li>')
            body.append(
                f'<article class="item" id="{anchor}">'
                f'<header><h3>{html.escape(name)}</h3>'
                f'<div class="chips">{chips}</div></header>'
                f'<div class="preview">{payload}</div>'
                f'<details><summary>Markup</summary>'
                f'<pre>{html.escape(payload.strip())}</pre></details>'
                f'</article>')
        nav.append("</ul>")
    return "\n".join(nav), "\n".join(body), words, counts


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "gallery.html").resolve()
    nav, body, words, counts = build()
    total = sum(n for _, n in counts)
    out.write_text(
        '<meta charset="utf-8"><title>Aperia UI components</title>\n'
        '<link href="https://fonts.googleapis.com/css2?family=Inter'
        ':wght@300;400;500;600;700&display=swap" rel="stylesheet">\n'
        f'<style>/* @aperia {" ".join(words)} */</style>\n'
        + CHROME +
        '<div class="gal"><nav class="galnav">'
        '<h1>Aperia UI components</h1>'
        f'<p class="built">{total} components, generated by scripts/gallery.py</p>'
        + nav + '</nav><main class="galmain">' + body + '</main></div>\n')

    assemble = UI / "assemble.py"
    result = subprocess.run([sys.executable, str(assemble), str(out)],
                            capture_output=True, text=True)
    if result.returncode != 0:
        sys.stderr.write(result.stdout + result.stderr)
        return result.returncode

    for rel, n in counts:
        print(f"  {rel:<24} {n:>3} components")
    print(f"ok: {out.name} <- {total} components, styled by "
          f"{' '.join(words)}. Open it in a browser.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
