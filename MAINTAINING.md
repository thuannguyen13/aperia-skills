# Maintaining

For people editing this repo. To install and use the plugin, see [README.md](README.md).

## Change the brand

1. Edit `plugins/aperia/skills/apply-branding/brand/`: `tokens.css` holds every value, `BRAND.md` holds the rules and names the tokens, `assets/` must match. A value changes in `tokens.css` only; a rule changes in `BRAND.md` only.
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
python3 plugins/aperia/skills/apply-branding/ui-components/assemble.py <file.html>
```

Fills a document's style marker, `<style>/* @aperia report [charts] [icons] */</style>` or `<style>/* @aperia slides */</style>`, with the stylesheets in the order the recipe names. The model never reads or types the CSS; the script copies the files in. Re-running replaces the injected block from the same words, so it is safe after every content edit. `--print report charts` writes the CSS to stdout for inspection.

Values are controlled in two places and no third. A change for every future output is an edit to the repo file. A change for one document is a second `<style>` block the model writes after the marker; later rules win, and the next assemble run leaves that block alone. Nothing is ever edited inside the injected block.

The script resolves the layers from its own location.

A layer file must never contain a closing style tag, even inside a comment, because the browser ends the style element there. The script refuses to inject one.

`examples/` holds one assembled output per skill, built from a bare marker with the script. Rebuild them after a theme change so they keep showing what the skills produce.

## gallery.py

```bash
python3 scripts/gallery.py [out.html]      # default: gallery.html
```

Renders the three snippet libraries as one page so the components can be reviewed by eye, then runs `assemble.py` on it, so the gallery is styled by the same layers a real document gets. Each component carries its name, an anchor and the class names its markup uses; a sticky index lists all of them, grouped by source file; the raw markup sits behind a disclosure on each one.

The page is generated, never hand-edited, so it cannot drift from what the skills actually copy. Nothing under `plugins/` is written, and the snippet libraries are read exactly as the skills read them.

It reads the nine grouped snippet files, `base/structure.html`, `emphasis.html`, `tables.html`, `charts.html`, `timelines.html` and `charts/trend.html`, `compare.html`, `proportion.html`, `intensity.html`, plus `icons/index.html`, and parses the `<!-- ===== NAME ===== -->` comments they already use. A comment whose name line is followed by prose and a plain `-->` is a group heading and renders as one; each file's banner header, a bare run of `=`, is not a component and does not appear. Add a component to a library and it appears here with no change to this script.

The script stays outside `plugins/` on purpose: a Desktop install mounts the skills, and the gallery is for whoever is working on them, not for the model. The generated file is gitignored.

## Where the shared layers live

`brand/` and `ui-components/` sit inside `plugins/aperia/skills/apply-branding/`, and the other two skills read them as `../apply-branding/brand/` and `../apply-branding/ui-components/`. One copy, no build step.

The reason for that spot is Claude Desktop. It mounts each folder under `skills/` that contains a `SKILL.md`, side by side at `/mnt/skills/plugins/<plugin>:<skill>/`, and nothing else: not the plugin root, not a folder without a `SKILL.md`. Layers at the plugin root never arrived, and both skills were broken there from 0.3.0 to 0.8.0. A folder that is a skill arrives, so the layers live in one. `apply-branding` is a real skill, the freeform branding entry point, and the carrier of the layers at the same time.

The folder name differs by client: `apply-branding` in Claude Code, `aperia:apply-branding` on Desktop. Prose paths are written with the plain name and each consumer skill says so in Step 0; the three scripts that cross into the layer look for both names. This relies on both clients mounting a plugin's skills beside each other, which is observed on Claude Code and Desktop and promised by neither. If a client ever isolated skills from one another, the fallback is a committed copy of the layers inside each skill, which commit `9b51f83` on the 0.9.0 branch implemented before this layout replaced it.

A skill folder on its own is not complete, so the Claude Desktop skill uploader, which takes one folder, is not an install path. Install through the marketplace, or upload the whole plugin as a zip with `.claude-plugin/plugin.json` at the archive root.

## Icons

Nothing is bundled. `skills/apply-branding/ui-components/icons/icon.py` fetches each icon from the Lucide CDN (`cdn.jsdelivr.net/npm/lucide-static`) on first use, pinned to the release named at the top of the script, and caches it under `~/.cache/aperia-icons/`. Bump the version there on purpose. A sandbox that blocks that host cannot produce icons; the script says so and the skill leaves the icon out.

## Ad-hoc branding

`apply-branding` covers a freeform request that fits neither `create-report` nor `create-slides`: a landing page, an email, a one-off graphic. Its `SKILL.md` loads the layers it holds and lets the model build the requested format on top, with the `page` recipe in `assemble.py` for HTML. Do not add a fourth skill for a new format; extend `apply-branding` or one of the two existing skills.
