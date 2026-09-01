#!/usr/bin/env python3
"""Emit inline Lucide SVG markup for Aperia HTML slides.

The icon inherits its color from CSS (`stroke="currentColor"`), so the theme
handles the tone rule automatically: dark blue on light slides, sky blue on
dark ones. Never hard-code a stroke color.

    python3 scripts/icon.py shield-check users refresh-cw
    python3 scripts/icon.py --search shield
    python3 scripts/icon.py --block database Consolidate "One evidence store."

As a module:

    from icon import svg, block
    html = svg("shield-check")
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


def svg(slug: str, stroke_width: float = 1.6) -> str:
    """Return inline SVG markup for a Lucide slug (e.g. 'shield-check')."""
    if slug not in ICONS:
        near = [k for k in ICONS if slug in k][:8]
        hint = f" Did you mean: {', '.join(near)}?" if near else ""
        raise KeyError(f"No Lucide icon '{slug}'.{hint}")
    return TPL.format(w=stroke_width, paths=ICONS[slug])


def block(slug: str, heading: str, body: str) -> str:
    """Return a complete .iblock (icon + heading + one line of copy)."""
    return (f'<div class="iblock">\n  {svg(slug)}\n'
            f'  <h3>{heading}</h3><p>{body}</p>\n</div>')


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
    elif args[0] == "--block":
        print(block(args[1], args[2], args[3]))
    else:
        for slug in args:
            print(svg(slug))
