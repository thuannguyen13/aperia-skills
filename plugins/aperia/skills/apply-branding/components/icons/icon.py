#!/usr/bin/env python3
"""Emit inline Lucide SVG markup for Aperia HTML output.

The icon inherits its color from CSS (`stroke="currentColor"`), so it takes
whatever color the surrounding text or element already has. Never hard-code
a stroke color; recolor the way you'd recolor text.

    python3 icons/icon.py shield-check
    python3 icons/icon.py --search alert

As a module:

    from icon import svg, search
    html = svg("shield-check")

Nothing is bundled. Each icon is fetched from a Lucide CDN on first use,
pinned to one release so a slug always gives the same paths, and cached
locally so the next use is free. Two hosts are tried in order. Where neither
is reachable, set APERIA_ICONS_DIR to a folder of Lucide SVG files (the
icons/ folder of a lucide-static package) and icons are read from there.
Otherwise the script says so and exits non-zero; leave the icon out, it is
never the only signal.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

# Pinned so a slug resolves to the same artwork on every machine. Bump on
# purpose, in one place.
LUCIDE_VERSION = "1.41.0"
CDNS = [f"https://cdn.jsdelivr.net/npm/lucide-static@{LUCIDE_VERSION}",
        f"https://unpkg.com/lucide-static@{LUCIDE_VERSION}"]
CDN = CDNS[0]
LOCAL_DIR = os.environ.get("APERIA_ICONS_DIR")
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".cache", "aperia-icons", LUCIDE_VERSION)
TIMEOUT = 8

TPL = ('<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
       'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" '
       'aria-hidden="true">{paths}</svg>')

_names = None  # the full Lucide name list, fetched once per run


def _fetch(path):
    """Body text for a path under the package, from the first host that answers,
    or None when no host is reachable or the file is missing."""
    for host in CDNS:
        try:
            with urllib.request.urlopen(f"{host}/{path}", timeout=TIMEOUT) as resp:
                return resp.read().decode("utf-8")
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError):
            continue
    return None


def _local(slug):
    """The SVG text from APERIA_ICONS_DIR, or None when unset or the file is missing."""
    if not LOCAL_DIR:
        return None
    try:
        with open(os.path.join(LOCAL_DIR, f"{slug}.svg"), encoding="utf-8") as fh:
            return fh.read()
    except OSError:
        return None


def _inner(svg_text):
    """The child elements of a lucide-static SVG, without the wrapper."""
    m = re.search(r"<svg\b[^>]*>(.*)</svg>", svg_text, re.S)
    if not m:
        return None
    return " ".join(line.strip() for line in m.group(1).strip().splitlines() if line.strip())


def paths(slug):
    """Path markup for a slug, from the local cache or the CDN."""
    cached = os.path.join(CACHE_DIR, f"{slug}.txt")
    if os.path.exists(cached):
        with open(cached, encoding="utf-8") as fh:
            return fh.read()
    body = _local(slug) or _fetch(f"icons/{slug}.svg")
    inner = _inner(body) if body else None
    if inner:
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(cached, "w", encoding="utf-8") as fh:
            fh.write(inner)
    return inner


def svg(slug: str, stroke_width: float = 1.75) -> str:
    """Return inline SVG markup for a Lucide slug (e.g. 'shield-check')."""
    inner = paths(slug)
    if inner is None:
        raise KeyError(f"Could not fetch Lucide icon '{slug}' from {' or '.join(CDNS)}. Either "
                       f"the slug is wrong (check lucide.dev/icons) or no host is reachable; "
                       f"set APERIA_ICONS_DIR to a folder of Lucide SVGs, or leave the icon "
                       f"out rather than drawing one.")
    return TPL.format(w=stroke_width, paths=inner)


def names():
    """Every Lucide icon name, from the CDN's tag index; None when offline."""
    global _names
    if _names is None:
        body = _fetch("tags.json")
        _names = sorted(json.loads(body)) if body else None
    return _names


def search(term: str):
    full = names()
    if full is None:
        sys.exit("Could not fetch the Lucide name index; the network is unavailable.")
    term = term.lower()
    return sorted(k for k in full if term in k)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        print(f"Icons come from Lucide {LUCIDE_VERSION}, fetched on demand.")
    elif args[0] == "--search":
        hits = search(args[1])
        print("\n".join(hits) if hits else "no match")
    else:
        try:
            for slug in args:
                print(svg(slug))
        except KeyError as e:
            sys.exit(str(e.args[0]))
