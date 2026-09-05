#!/usr/bin/env python3
"""Build one standalone upload bundle per skill.

A plugin install keeps `brand/` and `ui-components/` as siblings of `skills/`,
so `../../brand/BRAND.md` resolves and both skills render. The Claude Desktop
skill uploader takes one folder per skill instead, with nothing above it, so
`../../` resolves to nothing: `create-slides` still renders because its theme
is self-contained, `create-report` cannot, because the refactor moved its base
components out into `ui-components/`.

This inlines the layers each skill actually reads into a copy of that skill and
rewrites every reference to match, so an uploaded skill carries the same files
a plugin install would have given it. The repo keeps one copy of each layer;
the duplication happens at build time, in dist/, which is not committed.

Layout of a bundle, and the rewrite that produces it:

    dist/create-report/
      SKILL.md            ../../brand/BRAND.md      -> brand/BRAND.md
      references/         ../../ui-components/...   -> ui-components/...
      scripts/            os.path.join "..","..",".." -> ".."
      brand/              (copied whole)
      ui-components/      (copied whole)

Two kinds of reference, because the repo writes them two ways:

- Prose and comments name a layer from the **skill root**, `../../brand/...`,
  whatever file they sit in. That is how every SKILL.md and every reference
  file already reads. In a bundle the skill root is the bundle root, so the
  climb drops entirely: `brand/...`.
- Code in `scripts/` resolves paths against its own file, so those climb
  `depth + 2` levels in the source and `depth` in a bundle.

References between the two layers are already relative to each other and come
across unchanged.

Fails if a reference escapes the bundle or points at a file that isn't in it,
which is the packaging break this exists to catch.

Usage: python3 scripts/bundle-skills.py
"""

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "aperia"
SKILLS = PLUGIN / "skills"
OUT = ROOT / "dist"

# The reference layers, by directory name. A skill gets a copy of each one it
# mentions; nothing is copied speculatively.
LAYERS = ("brand", "ui-components")

# Suffixes worth rewriting and checking. Binary assets carry no paths.
TEXT = {".md", ".css", ".html", ".py", ".json", ".svg", ".txt", ".js"}

FAILURES = []


def fail(msg):
    FAILURES.append(msg)


# `../../ui-components/styles.css` and friends, in prose, CSS comments and
# markdown alike.
SLASH_REF = re.compile(r"((?:\.\./)+)(" + "|".join(LAYERS) + r")\b")

# The same reference written as os.path.join parts, which is how
# create-slides/scripts/icon.py finds the shared icon set.
JOIN_REF = re.compile(r'((?:"\.\.",\s*)+)(?="(?:' + "|".join(LAYERS) + r')")')

# Anything that looks like a relative path, for the verification pass.
CHECK_REF = re.compile(
    r"(?<![\w./-])((?:\.\./)+[\w./-]+|(?:" + "|".join(LAYERS) + r")/[\w./-]+)"
)


def layers_used(skill_dir):
    """Which layers this skill's own files reference."""
    used = set()
    for path in skill_dir.rglob("*"):
        if path.is_file() and path.suffix.lower() in TEXT:
            text = path.read_text(errors="ignore")
            used.update(name for name in LAYERS if f"{name}/" in text or f'"{name}"' in text)
    return sorted(used)


def rewrite(path, depth):
    """Point a skill file's layer references at the bundled copies.

    `depth` is how many directories the file sits below the skill root, which
    only `scripts/` code needs: it resolves against its own location, climbing
    `depth + 2` in the source and `depth` here. Prose names a layer from the
    skill root, two levels up wherever it is written, and loses the climb.
    """
    text = path.read_text()
    code = path.suffix.lower() == ".py"
    rel = path.relative_to(OUT)

    def slash(match):
        ups = match.group(1).count("../")
        expected = depth + 2 if code else 2
        if ups != expected:
            fail(f"{rel}: '{match.group(0)}' climbs {ups} levels, expected {expected}")
            return match.group(0)
        return "../" * (depth if code else 0) + match.group(2)

    def join(match):
        ups = match.group(1).count('".."')
        if ups != depth + 2:
            fail(f"{rel}: os.path.join climbs {ups} levels, expected {depth + 2}")
            return match.group(0)
        return '"..", ' * depth

    text = SLASH_REF.sub(slash, text)
    text = JOIN_REF.sub(join, text)
    path.write_text(text)


def verify(bundle):
    """Every relative reference in the bundle resolves to a file inside it.

    A `../` reference is file-relative; one that opens with a layer name is
    read from the skill root, the same two ways the rewrite treats them.
    """
    for path in sorted(bundle.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT:
            continue
        for match in CHECK_REF.finditer(path.read_text(errors="ignore")):
            ref = match.group(1).rstrip(".,;:)")
            base = path.parent if ref.startswith("../") else bundle
            target = (base / ref).resolve()
            rel = path.relative_to(OUT)
            if not target.is_relative_to(bundle.resolve()):
                fail(f"{rel}: '{ref}' points outside the bundle")
            elif not target.exists():
                fail(f"{rel}: '{ref}' does not exist in the bundle")


def build(skill_dir):
    bundle = OUT / skill_dir.name
    shutil.copytree(skill_dir, bundle)

    used = layers_used(skill_dir)
    for name in used:
        shutil.copytree(PLUGIN / name, bundle / name)

    for path in sorted(bundle.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT:
            continue
        # Layer files already sit in the same arrangement they had in the
        # plugin root, so their references to each other still resolve.
        if path.relative_to(bundle).parts[0] in used:
            continue
        rewrite(path, len(path.relative_to(bundle).parts) - 1)

    verify(bundle)
    shutil.make_archive(str(bundle), "zip", root_dir=OUT, base_dir=skill_dir.name)

    size = sum(f.stat().st_size for f in bundle.rglob("*") if f.is_file())
    return f"{skill_dir.name}: {', '.join(used) or 'no layers'}, {size // 1024}KB"


def main():
    if not SKILLS.is_dir():
        print(f"FAIL: no skills directory at {SKILLS.relative_to(ROOT)}")
        return 1

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()

    built = [build(d) for d in sorted(SKILLS.iterdir()) if (d / "SKILL.md").exists()]

    if FAILURES:
        print()
        for msg in FAILURES:
            print(f"FAIL: {msg}")
        print(f"\n{len(FAILURES)} problem(s) found. dist/ left in place to inspect.")
        return 1

    for line in built:
        print(f"ok: {line}")
    print(f"\n{len(built)} bundle(s) in {OUT.relative_to(ROOT)}/, zipped beside each folder.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
