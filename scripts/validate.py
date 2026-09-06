#!/usr/bin/env python3
"""Validate the aperia marketplace before it ships.

A broken manifest fails silently for everyone downstream, so this runs in CI on
every push and is worth running locally before you commit.

Checks:
  1. Both manifests parse and carry their required keys.
  2. Every plugin `source` in marketplace.json resolves to a real plugin.
  3. Every skill has a SKILL.md with name + description frontmatter, and the
     name matches its directory (the directory is what /aperia:<name> uses).
  4. Every color in the plugin, written as six-digit hex, three-digit hex or
     rgb()/rgba(), is either in tokens.css or listed in an ```approved block
     in DEVIATIONS.md. Off-palette values must be a decision, not an
     accident, and mentioning one in prose is not a decision.
  5. tokens.css defines the core and neutral palette and the chart series ramp.
  6. No stylesheet redefines a token the brand layer already defines. One
     source per value; the documented overrides are listed in OVERRIDES
     below, with the reason each is allowed.
  7. BRAND.md states no value that tokens.css owns, and every token it names
     exists. The guideline carries the rules and the print equivalents; the
     digital values have one home, so there is nothing to drift.
  8. No stylesheet sets a raw px font-size or a border-radius outside the
     shape tokens. Sizes come from the --text-* ramp, shape from --radius,
     --radius-sm, --radius-pill, 50% or 0.
  9. No em dash anywhere in the plugin or the repo docs. The model reads
     these files as its writing example.
 10. Every SKILL.md carries metadata.version equal to plugin.json, so a
     mounted copy can say which release it is.

The two shared layers live inside plugins/aperia/skills/apply-branding/,
a real skill, so every client that mounts a plugin's skills side by side
carries them along for the other two.

The palette itself is read by skills/apply-branding/brand/palette.py, which the
deck QA script shares, so neither holds a copy of it.

Usage: python3 scripts/validate.py
"""

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILURES = []
NOTES = []


def fail(msg):
    FAILURES.append(msg)


def note(msg):
    NOTES.append(msg)


def load_json(path, label):
    if not path.exists():
        fail(f"{label}: missing at {path.relative_to(ROOT)}")
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as e:
        fail(f"{label}: invalid JSON at line {e.lineno} col {e.colno} ({e.msg})")
        return None


def check_manifests():
    """Checks 1 and 2. Returns the list of plugin directories to walk."""
    market = load_json(ROOT / ".claude-plugin" / "marketplace.json", "marketplace.json")
    if market is None:
        return []

    for key in ("name", "owner", "plugins"):
        if key not in market:
            fail(f"marketplace.json: missing required key '{key}'")

    plugin_dirs = []
    for entry in market.get("plugins", []):
        name = entry.get("name", "<unnamed>")
        if "source" not in entry:
            fail(f"marketplace.json: plugin '{name}' has no source")
            continue

        plugin_dir = (ROOT / entry["source"]).resolve()
        if not plugin_dir.is_dir():
            fail(f"marketplace.json: plugin '{name}' source does not exist: {entry['source']}")
            continue

        manifest = load_json(plugin_dir / ".claude-plugin" / "plugin.json", f"{name}/plugin.json")
        if manifest is None:
            continue

        for key in ("name", "description", "version"):
            if key not in manifest:
                fail(f"{name}/plugin.json: missing required key '{key}'")

        if manifest.get("name") != entry.get("name"):
            fail(
                f"name mismatch: marketplace.json says '{entry.get('name')}', "
                f"plugin.json says '{manifest.get('name')}'. Install id would be wrong."
            )

        if not re.fullmatch(r"\d+\.\d+\.\d+", str(manifest.get("version", ""))):
            fail(f"{name}/plugin.json: version '{manifest.get('version')}' is not semver")

        plugin_dirs.append((manifest.get("name", name), plugin_dir))

    return plugin_dirs


FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def check_skills(plugin_name, plugin_dir):
    """Checks 3 and 10 (the version half)."""
    plugin_version = str(load_json(plugin_dir / ".claude-plugin" / "plugin.json", "plugin.json").get("version", ""))
    skills_dir = plugin_dir / "skills"
    if not skills_dir.is_dir():
        fail(f"{plugin_name}: no skills/ directory")
        return

    found = sorted(d for d in skills_dir.iterdir() if d.is_dir())
    if not found:
        fail(f"{plugin_name}: skills/ is empty")

    for skill in found:
        rel = skill.relative_to(ROOT)
        md = skill / "SKILL.md"
        if not md.exists():
            fail(f"{rel}: no SKILL.md, so this directory will not load as a skill")
            continue

        match = FRONTMATTER.match(md.read_text())
        if not match:
            fail(f"{rel}/SKILL.md: no YAML frontmatter block at the top of the file")
            continue

        fields = dict(
            re.match(r"^([a-zA-Z-]+):\s*(.*)$", line).groups()
            for line in match.group(1).splitlines()
            if re.match(r"^([a-zA-Z-]+):\s*(.*)$", line)
        )

        name = fields.get("name", "").strip()
        description = fields.get("description", "").strip()

        if not name:
            fail(f"{rel}/SKILL.md: frontmatter has no 'name'")
        elif name != skill.name:
            fail(
                f"{rel}/SKILL.md: name '{name}' does not match directory '{skill.name}'. "
                f"Users invoke the directory name."
            )

        version = re.search(r"^\s+version:\s*\"?([^\"\n]+)\"?\s*$", match.group(1), re.M)
        if not version:
            fail(f"{rel}/SKILL.md: frontmatter has no metadata.version, so a mounted "
                 f"copy cannot say which release it is")
        elif version.group(1).strip() != plugin_version:
            fail(f"{rel}/SKILL.md: metadata.version is {version.group(1).strip()}, "
                 f"plugin.json says {plugin_version}")

        if not description:
            fail(f"{rel}/SKILL.md: frontmatter has no 'description'")
        elif len(description) < 80:
            fail(f"{rel}/SKILL.md: description is {len(description)} chars, under 80. "
                 f"It is the only thing Claude sees when deciding to load the skill.")


HEX = re.compile(r"#([0-9a-fA-F]{6})\b")

# tokens.css is the single source of brand values, guideline and system alike.
TOKENS = "tokens.css"

# Where the shared layers live, relative to the plugin. They sit inside a
# skill, so one walk of skills/ covers every stylesheet.
LAYERS = Path("skills") / "apply-branding"


def brand_css(plugin_dir):
    """The token file as one string, or None if it is missing."""
    path = plugin_dir / LAYERS / "brand" / TOKENS
    if not path.exists():
        return None, [TOKENS]
    return path.read_text(), []


def palette_module(plugin_dir):
    """brand/palette.py, the plugin's own palette reader, loaded from its path."""
    path = plugin_dir / LAYERS / "brand" / "palette.py"
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location("palette", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def check_palette(plugin_name, plugin_dir):
    """Checks 4 and 5."""
    tokens, missing = brand_css(plugin_dir)
    if tokens is None:
        fail(f"{plugin_name}: brand/{TOKENS} is missing, so there is no palette "
             f"to check against")
        return
    palette_mod = palette_module(plugin_dir)
    if palette_mod is None:
        fail(f"{plugin_name}: brand/palette.py is missing, so nothing can read the palette")
        return

    # tokens.css is the single source of brand values. Every color it defines
    # is, by definition, the palette.
    palette = palette_mod.tokens(plugin_dir / LAYERS / "brand")
    if not palette:
        fail(f"{plugin_name}/{TOKENS}: no color values found, so the palette is empty")
        return

    # Check 5: the named tokens every skill relies on are actually defined.
    required = [
        "--aperia-blue", "--dark-blue", "--sapphire-blue", "--sky-blue", "--light-blue",
        "--black", "--dark-gray", "--medium-gray", "--light-gray", "--white",
    ]
    for name in required:
        if not re.search(rf"{re.escape(name)}\s*:", tokens):
            fail(f"{plugin_name}/{TOKENS}: missing required token '{name}'")
    for n in range(1, 8):
        if not re.search(rf"--series-{n}\s*:", tokens):
            fail(f"{plugin_name}/{TOKENS}: missing chart series step '--series-{n}'")

    deviations_path = plugin_dir / LAYERS / "brand" / "DEVIATIONS.md"
    if not deviations_path.exists():
        fail(f"{plugin_name}: brand/DEVIATIONS.md is missing, so off-palette "
             f"values have nowhere to be recorded")
        return
    # Approval is structural, not textual. Only the fenced ```approved blocks
    # count, so a hex named in prose, in a "was" column, or in a paragraph about a
    # value that was removed does not silently pass.
    recorded, has_blocks = palette_mod.approved(plugin_dir / LAYERS / "brand")
    if not has_blocks:
        fail(f"{plugin_name}/DEVIATIONS.md: no ```approved blocks found. Off-palette "
             f"values are approved by listing them in one, not by mentioning them.")

    offenders = {}
    for path in sorted(plugin_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".css", ".html", ".svg", ".json", ".md", ".py"}:
            continue
        if path == deviations_path or path.name == "palette.py":
            continue
        for value in palette_mod.colors_in(path.read_text(errors="ignore")):
            if value not in palette and value not in recorded:
                offenders.setdefault(value, set()).add(str(path.relative_to(ROOT)))

    for value, files in sorted(offenders.items()):
        fail(f"off-palette #{value} in {', '.join(sorted(files))}. "
             f"Fix it, or add it to an ```approved block in brand/DEVIATIONS.md "
             f"with a reason")


# Every stylesheet reads brand/tokens.css rather than repeating it, so a
# token defined in both is a second source for one value. These are
# deliberate and recorded; anything else is drift.
OVERRIDES = {
    "--fg": "near-black body ink over the brand's Aperia Blue, DEVIATIONS.md section 4",
    "--radius": "create-slides maps the radius onto its 1920 canvas, slides.css :root",
    "--radius-sm": "create-slides maps the radius onto its 1920 canvas, slides.css :root",
}

DECL = re.compile(r"(--[\w-]+)\s*:")


def root_tokens(path):
    """Token names defined in any :root block of a stylesheet."""
    if not path.exists():
        return set()
    text = re.sub(r"/\*.*?\*/", "", path.read_text(), flags=re.S)
    return {m.group(1) for block in re.findall(r":root\s*\{(.*?)\n\}", text, re.S)
            for m in DECL.finditer(block)}


def stylesheets(plugin_dir):
    """Every stylesheet other than tokens.css itself."""
    for sheet in sorted((plugin_dir / "skills").rglob("*.css")):
        if sheet.name != TOKENS:
            yield sheet


def check_single_source(plugin_name, plugin_dir):
    """Check 6."""
    brand = root_tokens(plugin_dir / LAYERS / "brand" / TOKENS)
    if not brand:
        return
    for sheet in stylesheets(plugin_dir):
        for name in sorted(root_tokens(sheet) & brand):
            if name in OVERRIDES:
                continue
            fail(f"{sheet.relative_to(ROOT)}: redefines '{name}', which brand/{TOKENS} "
                 f"already defines. Read it with var() instead, or record the override.")


# BRAND.md sets a 12px floor and a ten-step ramp; COMPONENTS.md says shape
# comes from the radius tokens. Both are rules about literals, so both are
# checked as literals. Circles (50%) and squared corners (0) are not shapes
# the tokens name.
RAW_FONT_SIZE = re.compile(r"font-size\s*:\s*[\d.]+px")
RADIUS = re.compile(r"border-radius\s*:\s*([^;}]+)")
LENGTH = re.compile(r"\d*\.?\d+(?:px|em|rem|%)")


def check_literals(plugin_name, plugin_dir):
    """Check 8."""
    for sheet in stylesheets(plugin_dir):
        text = re.sub(r"/\*.*?\*/", "", sheet.read_text(), flags=re.S)
        rel = sheet.relative_to(ROOT)
        for m in RAW_FONT_SIZE.finditer(text):
            fail(f"{rel}: '{m.group(0)}' is a raw px size. Use a --text-* token.")
        for m in RADIUS.finditer(text):
            if any(length != "50%" for length in LENGTH.findall(m.group(1))):
                fail(f"{rel}: 'border-radius:{m.group(1)}' is off the shape tokens. "
                     f"Use --radius, --radius-sm or --radius-pill.")


def check_no_em_dash():
    """Check 9. Repo docs and everything in plugins/."""
    paths = [p for p in ROOT.glob("*.md")]
    paths += [p for p in (ROOT / "plugins").rglob("*") if p.is_file()
              and p.suffix.lower() in {".md", ".css", ".html", ".py", ".svg", ".json"}]
    for path in sorted(paths):
        for n, line in enumerate(path.read_text(errors="ignore").splitlines(), 1):
            if "\u2014" in line:
                fail(f"{path.relative_to(ROOT)}:{n}: em dash. Use a colon, a comma or two sentences.")


# BRAND.md names tokens rather than repeating their values: | Aperia Blue |
# `--aperia-blue` | ... Two things can go wrong, and both are checked.
NAMED_TOKEN = re.compile(r"`(--[\w-]+)`")


def check_guideline_states_no_values(plugin_name, plugin_dir):
    """Check 7."""
    brand_md = plugin_dir / LAYERS / "brand" / "BRAND.md"
    tokens, _ = brand_css(plugin_dir)
    if tokens is None or not brand_md.exists():
        return
    text = brand_md.read_text()

    # A hex in the guideline is a second copy of a value tokens.css owns.
    for m in HEX.finditer(text):
        fail(f"{plugin_name}/BRAND.md: states #{m.group(1)}. Colors live in "
             f"{TOKENS}; name the token instead, so there is one copy of the value.")

    # A token the guideline names must exist, or the pointer dangles.
    defined = root_tokens(plugin_dir / LAYERS / "brand" / TOKENS)
    for m in NAMED_TOKEN.finditer(text):
        if m.group(1) not in defined:
            fail(f"{plugin_name}/BRAND.md: names '{m.group(1)}', which {TOKENS} "
                 f"does not define.")


def main():
    plugins = check_manifests()
    for plugin_name, plugin_dir in plugins:
        check_skills(plugin_name, plugin_dir)
        check_palette(plugin_name, plugin_dir)
        check_single_source(plugin_name, plugin_dir)
        check_guideline_states_no_values(plugin_name, plugin_dir)
        check_literals(plugin_name, plugin_dir)
    check_no_em_dash()

    for msg in NOTES:
        print(f"note: {msg}")

    if FAILURES:
        print()
        for msg in FAILURES:
            print(f"FAIL: {msg}")
        print(f"\n{len(FAILURES)} problem(s) found.")
        return 1

    names = ", ".join(name for name, _ in plugins)
    print(f"ok: {names} validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
