#!/usr/bin/env python3
"""Copy the shared layers into every skill, so each skill folder is complete.

`plugins/aperia/brand/` and `plugins/aperia/ui-components/` are the single
source. Every client that installs the plugin mounts a skill folder on its
own: Claude Desktop puts it at /mnt/skills/plugins/<skill>/ with nothing above
it, and the Agent Skills specification says a skill may not reach outside its
own directory. So each skill carries a committed copy of both layers, written
by this script and never edited by hand. Skill files reference the layers
from the skill root, `brand/tokens.css`, on every client.

    python3 scripts/sync-layers.py           # refresh the copies
    python3 scripts/sync-layers.py --check   # fail if any copy is out of date
    python3 scripts/sync-layers.py --zip     # also write dist/<skill>.zip for the
                                             # Claude Desktop skill uploader

validate.py runs the check, so a brand edit committed without a sync fails
CI with this script's name in the message.

After copying, every relative reference in a skill is verified to resolve to
a file inside that skill: `brand/...` and `ui-components/...` from the skill
root, `../` from the file that holds it, and os.path.join(HERE, ...) in
scripts. A reference that escapes the skill is the Desktop break this exists
to prevent.
"""
import filecmp
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "aperia"
SKILLS = PLUGIN / "skills"
DIST = ROOT / "dist"

LAYERS = ("brand", "ui-components")

# Suffixes whose contents can hold a path. Binary assets carry none.
TEXT = {".md", ".css", ".html", ".py", ".json", ".svg", ".txt", ".js"}

# Anything that looks like a relative path: a ../ climb, or a layer name
# followed by a path, which is read from the skill root.
CHECK_REF = re.compile(
    r"(?<![\w./-])((?:\.\./)+[\w./-]+|(?:" + "|".join(LAYERS) + r")/[\w./-]+)"
)
# A path built from os.path.join parts, which the pattern above cannot see.
CHECK_JOIN = re.compile(r'os\.path\.join\(HERE,\s*((?:"[^"]+",?\s*)+)\)')

FAILURES = []


def fail(msg):
    FAILURES.append(msg)


def skills():
    return sorted(d for d in SKILLS.iterdir() if (d / "SKILL.md").exists())


def stale(source, copy):
    """Paths that differ between a layer and a skill's copy of it."""
    if not copy.exists():
        return ["(missing)"]
    out = []

    def walk(cmp, prefix=""):
        out.extend(prefix + n for n in cmp.left_only + cmp.right_only + cmp.diff_files)
        for name, sub in cmp.subdirs.items():
            walk(sub, prefix + name + "/")

    walk(filecmp.dircmp(source, copy, ignore=[".DS_Store"]))
    return out


def check():
    for skill in skills():
        for layer in LAYERS:
            for path in stale(PLUGIN / layer, skill / layer):
                fail(f"{skill.relative_to(ROOT)}/{layer}/{path} is out of date. "
                     f"Run: python3 scripts/sync-layers.py")


def sync():
    for skill in skills():
        for layer in LAYERS:
            target = skill / layer
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(PLUGIN / layer, target, ignore=shutil.ignore_patterns(".DS_Store"))


def verify(skill):
    """Every relative reference in the skill resolves to a file inside it."""
    for path in sorted(skill.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT:
            continue
        text = path.read_text(errors="ignore")
        rel = path.relative_to(ROOT)

        refs = [(m.group(1).rstrip(".,;:)"), False) for m in CHECK_REF.finditer(text)]
        refs += [("/".join(re.findall(r'"([^"]+)"', m.group(1))), True)
                 for m in CHECK_JOIN.finditer(text)]

        for ref, from_file in refs:
            base = path.parent if from_file or ref.startswith("../") else skill
            target = (base / ref).resolve()
            if not target.is_relative_to(skill.resolve()):
                fail(f"{rel}: '{ref}' points outside the skill")
            elif not target.exists():
                fail(f"{rel}: '{ref}' does not exist in the skill")


def zip_skills():
    DIST.mkdir(exist_ok=True)
    for skill in skills():
        shutil.make_archive(str(DIST / skill.name), "zip", root_dir=SKILLS, base_dir=skill.name)
        print(f"ok: {DIST.relative_to(ROOT)}/{skill.name}.zip")


def main(argv):
    if not SKILLS.is_dir():
        print(f"FAIL: no skills directory at {SKILLS.relative_to(ROOT)}")
        return 1

    if "--check" in argv:
        check()
    else:
        sync()
    for skill in skills():
        verify(skill)

    if FAILURES:
        print()
        for msg in FAILURES:
            print(f"FAIL: {msg}")
        print(f"\n{len(FAILURES)} problem(s) found.")
        return 1

    if "--zip" in argv:
        zip_skills()
    for skill in skills():
        size = sum(f.stat().st_size for f in skill.rglob("*") if f.is_file())
        print(f"ok: {skill.name} carries {', '.join(LAYERS)}, {size // 1024}KB")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
