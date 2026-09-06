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
    <style>/* @aperia page charts */</style>

Running again is safe: the injected block carries the same words in a
data-aperia attribute, and the script replaces that block from the same
recipe. Anything the document needs on top of the layers goes in its own
separate <style> block after the marker, never inside the injected one.

Recipes, in paste order:

    report   brand/tokens.css, ui-components/base/styles.css,
             [charts/styles.css], [icons/styles.css], the create-report theme
    slides   brand/tokens.css, the create-slides theme
    page     brand/tokens.css, ui-components/base/styles.css,
             [charts/styles.css], [icons/styles.css], no skill theme

The layers live inside the apply-branding skill, beside the other skill
folders, so a client that mounts a plugin's skills side by side sees them
at ../apply-branding/.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent     # skills/apply-branding/ui-components
LAYERS = HERE.parent                         # skills/apply-branding
SKILLS = LAYERS.parent                       # skills

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
    "page": {
        "layers": ["brand/tokens.css", "ui-components/base/styles.css"],
        "optional": {"charts": "ui-components/charts/styles.css",
                     "icons": "ui-components/icons/styles.css"},
        "theme": None,
    },
}

MARKER = re.compile(
    r"<style>\s*/\*\s*@aperia\s+([\w \t-]+?)\s*\*/\s*</style>"
    r"|<style data-aperia=\"([\w -]+)\">.*?</style>",
    re.S,
)


def theme_path(skill, name):
    """The skill's own theme, in its references/ folder."""
    candidate = SKILLS / skill / "references" / name
    if candidate.exists():
        return candidate
    sys.exit(f"assemble: cannot find {name} for {skill} under {SKILLS}")


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

    files = [LAYERS / p for p in recipe["layers"]]
    files += [LAYERS / recipe["optional"][f] for f in recipe["optional"] if f in flags]
    if recipe["theme"]:
        files.append(theme_path(*recipe["theme"]))

    parts = []
    for path in files:
        if not path.exists():
            sys.exit(f"assemble: missing layer file {path}")
        if "</style" in path.read_text():
            # The browser ends the style element at that text, comment or not.
            sys.exit(f"assemble: {path.name} contains '</style', which would cut the block short")
        parts.append(f"/* ---- {path.name} ({path.parent.name}) ---- */\n{path.read_text().strip()}")
    head = ("/* Assembled by apply-branding/ui-components/assemble.py from the words in data-aperia.\n"
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
