#!/usr/bin/env python3
"""Validate the aperia marketplace before it ships.

A broken manifest fails silently for everyone downstream, so this runs in CI on
every push and is worth running locally before you commit.

Checks:
  1. Both manifests parse and carry their required keys.
  2. Every plugin `source` in marketplace.json resolves to a real plugin.
  3. Every skill has a SKILL.md with name + description frontmatter, and the
     name matches its directory (the directory is what /aperia:<name> uses).
  4. Every hex in the plugin is either in tokens.css or listed in an ```approved
     block in DEVIATIONS.md. Off-palette values must be a decision, not an
     accident, and mentioning one in prose is not a decision.
  5. tokens.css defines the core and neutral palette and the chart series ramp.

Usage: python3 scripts/validate.py
"""

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
    """Check 3."""
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

        if not description:
            fail(f"{rel}/SKILL.md: frontmatter has no 'description'")
        elif len(description) < 80:
            note(f"{rel}/SKILL.md: description is {len(description)} chars. "
                 f"It is the only thing Claude sees when deciding to load the skill.")


HEX = re.compile(r"#([0-9a-fA-F]{6})\b")

# Only hexes inside a fenced ```approved block in DEVIATIONS.md are allowlisted.
APPROVED_BLOCK = re.compile(r"^```approved[ \t]*\n(.*?)^```", re.M | re.S)


def check_palette(plugin_name, plugin_dir):
    """Checks 4 and 5."""
    tokens_path = plugin_dir / "brand" / "tokens.css"
    if not tokens_path.exists():
        fail(f"{plugin_name}: brand/tokens.css is missing, so there is no palette to "
             f"check against")
        return
    tokens = tokens_path.read_text()

    # tokens.css is the single source of brand values. Every hex it defines is,
    # by definition, the palette.
    palette = {m.group(1).upper() for m in HEX.finditer(tokens)}
    if not palette:
        fail(f"{plugin_name}/tokens.css: no hex values found, so the palette is empty")
        return

    # Check 5: the named tokens every skill relies on are actually defined.
    required = [
        "--aperia-blue", "--dark-blue", "--sapphire-blue", "--sky-blue", "--light-blue",
        "--black", "--dark-gray", "--medium-gray", "--light-gray", "--white",
    ]
    for name in required:
        if not re.search(rf"{re.escape(name)}\s*:", tokens):
            fail(f"{plugin_name}/tokens.css: missing required token '{name}'")
    for n in range(1, 8):
        if not re.search(rf"--series-{n}\s*:", tokens):
            fail(f"{plugin_name}/tokens.css: missing chart series step '--series-{n}'")

    deviations_path = plugin_dir / "brand" / "DEVIATIONS.md"
    if not deviations_path.exists():
        fail(f"{plugin_name}: brand/DEVIATIONS.md is missing, so off-palette "
             f"values have nowhere to be recorded")
        return
    # Approval is structural, not textual. Only the fenced ```approved blocks
    # count, so a hex named in prose, in a "was" column, or in a paragraph about a
    # value that was removed does not silently pass.
    blocks = APPROVED_BLOCK.findall(deviations_path.read_text())
    recorded = {m.group(1).upper() for block in blocks for m in HEX.finditer(block)}
    if not blocks:
        fail(f"{plugin_name}/DEVIATIONS.md: no ```approved blocks found. Off-palette "
             f"values are approved by listing them in one, not by mentioning them.")

    offenders = {}
    for path in sorted(plugin_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".css", ".html", ".svg", ".json", ".md"}:
            continue
        if path == deviations_path:
            continue
        for match in HEX.finditer(path.read_text(errors="ignore")):
            value = match.group(1).upper()
            if value not in palette and value not in recorded:
                offenders.setdefault(value, set()).add(str(path.relative_to(ROOT)))

    for value, files in sorted(offenders.items()):
        fail(f"off-palette #{value} in {', '.join(sorted(files))}. "
             f"Fix it, or add it to an ```approved block in brand/DEVIATIONS.md "
             f"with a reason")


def main():
    plugins = check_manifests()
    for plugin_name, plugin_dir in plugins:
        check_skills(plugin_name, plugin_dir)
        check_palette(plugin_name, plugin_dir)

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
