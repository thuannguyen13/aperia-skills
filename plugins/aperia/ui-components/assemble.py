#!/usr/bin/env python3
"""Inject the Aperia stylesheets into an HTML file, in the right order.

The model writes the document with an empty style marker and never types the
CSS itself. This script copies the layer files into that marker byte for
byte, so the output carries exactly what the repo ships.

    python3 assemble.py report.html            # fill the marker in place
    python3 assemble.py --print report charts  # write the CSS to stdout

The marker names a recipe and any optional layers:

    <style>/* @aperia report */</style>
    <style>/* @aperia report charts icons */</style>
    <style>/* @aperia slides */</style>

Running again is safe: the injected block carries the same words in a
data-aperia attribute, and the script replaces that block from the same
recipe. Anything the document needs on top of the layers goes in its own
separate <style> block after the marker, never inside the injected one.

Recipes, in paste order:

    report   brand/tokens.css, ui-components/base/styles.css,
             [charts/styles.css], [icons/styles.css], the create-report theme
    slides   brand/tokens.css, the create-slides theme

Works from a plugin install (brand/ and ui-components/ beside skills/) and
from a standalone skill bundle (brand/ and ui-components/ beside references/).
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent  # the plugin, or a standalone skill bundle

RECIPES = {
    "report": {
        "layers": ["brand/tokens.css", "ui-components/base/styles.css"],
        "optional": {"charts": "ui-components/charts/styles.css",
                     "icons": "ui-components/icons/styles.css"},
        "theme": ("create-report", "styles.css"),
    },
    "slides": {
        "layers": ["brand/tokens.css"],
        "optional": {},
        "theme": ("create-slides", "slides.css"),
    },
}

MARKER = re.compile(
    r"<style>\s*/\*\s*@aperia\s+([\w \t-]+?)\s*\*/\s*</style>"
    r"|<style data-aperia=\"([\w -]+)\">.*?</style>",
    re.S,
)


def theme_path(skill, name):
    """The skill theme, wherever this layout keeps it."""
    for candidate in (ROOT / "skills" / skill / "references" / name,
                      ROOT / "references" / name):
        if candidate.exists():
            return candidate
    sys.exit(f"assemble: cannot find {name} for {skill} under {ROOT}")


def css_for(words):
    """The concatenated CSS for a marker's words, e.g. ['report', 'charts']."""
    recipe_name, flags = words[0], words[1:]
    recipe = RECIPES.get(recipe_name)
    if recipe is None:
        sys.exit(f"assemble: unknown recipe '{recipe_name}', expected one of {', '.join(RECIPES)}")
    unknown = [f for f in flags if f not in recipe["optional"]]
    if unknown:
        allowed = ", ".join(recipe["optional"]) or "none"
        sys.exit(f"assemble: '{recipe_name}' takes no flag '{unknown[0]}' (allowed: {allowed})")

    files = [ROOT / p for p in recipe["layers"]]
    files += [ROOT / recipe["optional"][f] for f in recipe["optional"] if f in flags]
    files.append(theme_path(*recipe["theme"]))

    parts = []
    for path in files:
        if not path.exists():
            sys.exit(f"assemble: missing layer file {path}")
        parts.append(f"/* ---- {path.name} ({path.parent.name}) ---- */\n{path.read_text().strip()}")
    head = ("/* Assembled by ui-components/assemble.py from the words in data-aperia.\n"
            "   Do not edit inside this block: it is replaced on every run. Put\n"
            "   document-specific rules in a separate <style> after it. */")
    return head + "\n\n" + "\n\n".join(parts) + "\n"


def assemble(path):
    text = path.read_text()
    matches = list(MARKER.finditer(text))
    if not matches:
        sys.exit("assemble: no marker found. Add <style>/* @aperia report */</style> "
                 "(or slides) where the styles go.")
    if len(matches) > 1:
        sys.exit(f"assemble: {len(matches)} markers found, expected one")

    m = matches[0]
    words = (m.group(1) or m.group(2)).split()
    block = f'<style data-aperia="{" ".join(words)}">\n{css_for(words)}</style>'
    path.write_text(text[:m.start()] + block + text[m.end():])

    if "fonts.googleapis.com" not in text:
        print("assemble: warning, no Google Fonts <link> found; Inter will not load")
    print(f"assemble: {path.name} <- {' '.join(words)} ({len(block) // 1024}KB of CSS)")


def main(argv):
    if len(argv) >= 2 and argv[0] == "--print":
        sys.stdout.write(css_for(argv[1:]))
        return 0
    if len(argv) != 1:
        sys.exit(__doc__)
    assemble(Path(argv[0]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
