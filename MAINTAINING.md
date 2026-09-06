# Maintaining

For people editing this repo. To install and use the plugin, see [README.md](README.md).

## Change the brand

1. Edit `plugins/aperia/brand/`: `tokens.css` holds every value, `BRAND.md` holds the rules and names the tokens, `assets/` must match. A value changes in `tokens.css` only; a rule changes in `BRAND.md` only. Then run `python3 scripts/sync-layers.py` to refresh the copy each skill carries; never edit those copies.
2. Bump `version` in `plugins/aperia/.claude-plugin/plugin.json`.
3. Add a `CHANGELOG.md` entry.
4. Run `python3 scripts/validate.py`, then `claude plugin validate .`.
5. Commit and push.
6. Tag the release with `claude plugin tag plugins/aperia`. It writes an `aperia--v<version>` tag and re-checks that `plugin.json` and the marketplace entry still agree.

Step 2 is not optional. The version is the install cache directory name, so edits shipped without a bump leave teammates on stale files. CI fails a pull request that changes `plugins/` without it. `CHANGELOG.md` versions track this same field. Teammates pick up a release with `/plugin marketplace update aperia-skills`, which lands on their next session start.

Because every skill reads `BRAND.md` at runtime, step 1 is usually the whole job and the skills themselves rarely need touching.

Never edit the installed copy under `~/.claude/plugins/cache/`. The next update overwrites it. Work here and push.

## validate.py

```bash
python3 scripts/validate.py
```

No dependencies beyond Python 3. CI runs the same script on every push and pull request, so a broken manifest fails here rather than silently for everyone downstream. It checks:

- Both manifests parse and carry their required keys.
- Every plugin `source` in `marketplace.json` resolves, the two `name` values agree, and `version` is semver. A name mismatch would make the documented install id wrong.
- Every skill has a `SKILL.md` with `name` and `description` frontmatter, and the name matches its directory, since the directory is what `/aperia:<name>` uses.
- `tokens.css` defines the core and neutral palette and the seven chart series steps.
- Every color in the plugin, as six-digit hex, three-digit hex or `rgb()`/`rgba()`, is either in `tokens.css` or listed in a fenced ```approved block in `brand/DEVIATIONS.md`. The palette is read through `plugins/aperia/brand/palette.py`, which the deck's `qa.py` also uses, so no script holds a copy of it.
- No stylesheet redefines a token `tokens.css` defines, except the overrides listed in `OVERRIDES` inside the script with a reason.
- No stylesheet sets a raw px `font-size` or a `border-radius` outside `--radius`, `--radius-sm`, `--radius-pill` and `50%`.
- Skill descriptions are at least 80 characters. The description is the only text Claude reads when deciding to load a skill on its own.
- No em dash in any file. The model reads these files as its writing example.

Off-palette values are a decision, not an accident. Anything the check flags gets fixed or written into `plugins/aperia/brand/DEVIATIONS.md` with a reason. That file is both the audit trail and the allowlist. It currently covers the semantic status colors, the report theme's light tint ramp, the deck theme's dark chart ramp, the PowerPoint template accent alternates, and the `#004583` vs `#004785` mismatch between the supplied SVG assets and the guideline table.

Approval is structural: only hexes inside a fenced ```approved block count. Mentioning a value in prose, in a "was" column, or in a paragraph explaining why it was dropped does not approve it. Approval is plugin-wide rather than per file, so a value approved for one theme will pass in the other; scope it by narrative if that matters.

## assemble.py

```bash
python3 plugins/aperia/ui-components/assemble.py <file.html>
```

Fills a document's style marker, `<style>/* @aperia report [charts] [icons] */</style>` or `<style>/* @aperia slides */</style>`, with the stylesheets in the order the recipe names. The model never reads or types the CSS; the script copies the files in. Re-running replaces the injected block from the same words, so it is safe after every content edit. `--print report charts` writes the CSS to stdout for inspection.

Values are controlled in two places and no third. A change for every future output is an edit to the repo file. A change for one document is a second `<style>` block the model writes after the marker; later rules win, and the next assemble run leaves that block alone. Nothing is ever edited inside the injected block.

The script resolves the layers from its own location, so it works from a plugin install and from a standalone bundle without a rewrite.

A layer file must never contain a closing style tag, even inside a comment, because the browser ends the style element there. The script refuses to inject one.

`examples/` holds one assembled output per skill, built from a bare marker with the script. Rebuild them after a theme change so they keep showing what the skills produce.

## sync-layers.py

```bash
python3 scripts/sync-layers.py           # refresh the copies
python3 scripts/sync-layers.py --check   # what CI runs
python3 scripts/sync-layers.py --zip     # dist/<skill>.zip for the Desktop uploader
```

Every client mounts a skill folder on its own. Claude Desktop puts it at `/mnt/skills/plugins/<skill>/` with nothing above it, and the Agent Skills specification says a skill may not reach outside its own directory. So `brand/` and `ui-components/` at the plugin root are the single source, and each skill carries a committed copy of both, written by this script. Skill files reference the layers from the skill root, `brand/tokens.css` and `ui-components/assemble.py`, on every client. A Claude Code install carries the layers three times, root plus two copies; only the copies are read.

The copies are never edited by hand. `validate.py` fails when a copy is behind the source, so a brand change committed without a sync fails CI with this script's name in the message. The repo grows by about 1.4 MB for the two copies, most of it the icon set.

After copying, the script verifies that every relative reference in a skill resolves to a file inside that skill. A reference that escapes the skill is the Desktop break this exists to prevent. This was broken from 0.3.0, when the layers moved out of the skills, until 0.9.0.

## Ad-hoc branding

There is currently no skill for a freeform request that fits neither
`create-report` nor `create-slides` (a landing page, an email, a one-off
graphic). If that need comes back, either add a thin skill whose only job is
to load `brand/` (and `ui-components/`, if the output needs any of its
pieces) and let the model build the requested format on top, or extend one
of the two existing skills, don't duplicate the reference layers into a new
copy either way.
