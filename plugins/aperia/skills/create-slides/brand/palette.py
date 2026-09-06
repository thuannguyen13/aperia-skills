#!/usr/bin/env python3
"""Read the Aperia palette from the files that own it.

The plugin has one source for brand colors, `tokens.css`, and one allowlist
for values outside it, the fenced ```approved blocks in `DEVIATIONS.md`.
Every check that asks "is this color allowed" reads both from here, so the
repo validator and the deck QA script cannot hold a second copy of the
palette that drifts from the first.

    from palette import load, colors_in
    allowed = load(brand_dir)         # set of "RRGGBB", upper case
    found = colors_in(css_text)       # every color literal in a text, same form

`colors_in` sees all three ways a color is written in this plugin: six-digit
hex, three-digit hex (`#fff`), and `rgb()` / `rgba()`. Alpha is ignored, since
an opacity of a palette color is that color (DEVIATIONS.md section 7).
"""
import re
from pathlib import Path

HEX6 = re.compile(r"#([0-9a-fA-F]{6})\b")
HEX3 = re.compile(r"#([0-9a-fA-F]{3})\b(?![0-9a-fA-F])")
RGB = re.compile(r"rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})")

# Only hexes inside a fenced ```approved block count. A value named in prose,
# in a "was" column, or in a paragraph about a removed value is not approved.
APPROVED_BLOCK = re.compile(r"^```approved[ \t]*\n(.*?)^```", re.M | re.S)


def colors_in(text):
    """Every color literal in `text`, normalized to 'RRGGBB' upper case."""
    found = {m.group(1).upper() for m in HEX6.finditer(text)}
    found |= {"".join(c * 2 for c in m.group(1)).upper() for m in HEX3.finditer(text)}
    found |= {"%02X%02X%02X" % tuple(int(c) for c in m.groups()) for m in RGB.finditer(text)}
    return found


def tokens(brand_dir):
    """The palette tokens.css defines. Empty if the file is missing."""
    path = Path(brand_dir) / "tokens.css"
    return colors_in(path.read_text()) if path.exists() else set()


def approved(brand_dir):
    """Off-palette values DEVIATIONS.md approves, and whether any block exists."""
    path = Path(brand_dir) / "DEVIATIONS.md"
    if not path.exists():
        return set(), False
    blocks = APPROVED_BLOCK.findall(path.read_text())
    return {c for block in blocks for c in colors_in(block)}, bool(blocks)


def load(brand_dir):
    """Every color the plugin may use: the tokens plus the approved deviations."""
    return tokens(brand_dir) | approved(brand_dir)[0]
