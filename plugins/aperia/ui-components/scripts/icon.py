#!/usr/bin/env python3
"""Emit inline Lucide SVG markup for Aperia HTML output.

The icon inherits its color from CSS (`stroke="currentColor"`), so it takes
whatever color the surrounding text or element already has. Never hard-code
a stroke color — recolor the way you'd recolor text.

    python3 scripts/icon.py shield-check
    python3 scripts/icon.py search alert-triangle
    python3 scripts/icon.py --search alert

As a module:

    from icon import svg, search
    html = svg("shield-check")

Same asset and the same `svg()`/`search()` behavior as
create-slides/scripts/icon.py, which points at this same JSON file rather
than keeping its own copy — see ../COMPONENTS.md, "Icon toolkit".
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ICONS_PATH = os.path.join(HERE, "..", "assets", "lucide-icons.json")

with open(ICONS_PATH, encoding="utf-8") as fh:
    ICONS = json.load(fh)

TPL = ('<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
       'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" '
       'aria-hidden="true">{paths}</svg>')


def svg(slug: str, stroke_width: float = 1.75) -> str:
    """Return inline SVG markup for a Lucide slug (e.g. 'shield-check')."""
    if slug not in ICONS:
        near = [k for k in ICONS if slug in k][:8]
        hint = f" Did you mean: {', '.join(near)}?" if near else ""
        raise KeyError(f"No Lucide icon '{slug}'.{hint}")
    return TPL.format(w=stroke_width, paths=ICONS[slug])


def search(term: str):
    return sorted(k for k in ICONS if term.lower() in k)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        print(f"{len(ICONS)} icons bundled.")
    elif args[0] == "--search":
        hits = search(args[1])
        print("\n".join(hits) if hits else "no match")
    else:
        for slug in args:
            print(svg(slug))
