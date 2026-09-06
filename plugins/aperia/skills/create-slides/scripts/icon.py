#!/usr/bin/env python3
"""Emit inline Lucide SVG markup for Aperia HTML slides.

A thin wrapper over the shared ../apply-branding/components/icons/icon.py, which fetches
each icon from the Lucide CDN on demand. This adds the slide-specific
stroke width and the .iblock helper, nothing else.

    python3 scripts/icon.py shield-check users refresh-cw
    python3 scripts/icon.py --search shield
    python3 scripts/icon.py --block database Consolidate "One evidence store."

The icon inherits its color from CSS (`stroke="currentColor"`), so the theme
handles the tone rule automatically: dark blue on light slides, sky blue on
dark ones. Never hard-code a stroke color.
"""
import glob
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
# Clients name a mounted skill folder differently, apply-branding in Claude
# Code and aperia:apply-branding on Claude Desktop, so look for both.
_SKILLS = os.path.join(HERE, "..", "..")
_LAYER = next((d for d in [os.path.join(_SKILLS, "apply-branding")] + sorted(glob.glob(os.path.join(_SKILLS, "*:apply-branding")))
               if os.path.isdir(d)), None)
if _LAYER is None:
    sys.exit("icon.py: the apply-branding skill, which holds the shared icon script, is not "
             f"installed beside create-slides under {os.path.normpath(_SKILLS)}.")
SHARED = os.path.join(_LAYER, "components", "icons", "icon.py")
_spec = importlib.util.spec_from_file_location("shared_icon", SHARED)
shared = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(shared)

STROKE = 1.6  # slide faces are read from further away than a page


def svg(slug: str) -> str:
    return shared.svg(slug, STROKE)


def block(slug: str, heading: str, body: str) -> str:
    """Return a complete .iblock (icon + heading + one line of copy)."""
    return (f'<div class="iblock">\n  {svg(slug)}\n'
            f'  <h3>{heading}</h3><p>{body}</p>\n</div>')


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
    elif args[0] == "--search":
        hits = shared.search(args[1])
        print("\n".join(hits) if hits else "no match")
    elif args[0] == "--block":
        print(block(args[1], args[2], args[3]))
    else:
        try:
            for slug in args:
                print(svg(slug))
        except KeyError as e:
            sys.exit(str(e.args[0]))
