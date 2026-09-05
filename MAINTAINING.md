# Maintaining

For people editing this repo. To install and use the plugin, see [README.md](README.md).

## Change the brand

1. Edit `plugins/aperia/brand/`: `tokens.css` holds every value, `BRAND.md` holds the rules and names the tokens, `assets/` must match. A value changes in `tokens.css` only; a rule changes in `BRAND.md` only.
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

## bundle-skills.py

```bash
python3 scripts/bundle-skills.py
```

Builds `dist/<skill>/` and `dist/<skill>.zip`, one standalone bundle per skill, for the Claude Desktop skill uploader. Neither is committed.

The plugin install and the uploader lay files out differently. An install copies the whole of `plugins/aperia/`, so `brand/` and `ui-components/` sit beside `skills/` and `../../brand/BRAND.md` resolves. The uploader takes one folder per skill with nothing above it, so the same reference resolves to nothing. `create-slides` survives that because its theme is self-contained; `create-report` does not, because its base components live in `ui-components/` and its own `references/styles.css` defines one variable and reads 36 from elsewhere.

So the script copies each layer a skill reads into a copy of that skill and rewrites the references to match. The repo still keeps one copy of each layer; the duplication happens at build time. It fails if a reference escapes a bundle or points at a file the bundle does not contain, which is the packaging break it exists to catch, and CI runs it on every push and pull request for that reason.

Run it before uploading, and after moving anything between the layers and the skills.

## Conventions

- `brand/` and `ui-components/` hold reference files only, with no frontmatter, so neither loads as a skill alongside the two real ones. `brand/` is the visual identity (palette, type, logo, the graphic element); `ui-components/` is the component library built on top of it (cards, badges, callouts, tables, the chart toolkit, the icon set, milestone/status timelines), see `ui-components/COMPONENTS.md`.
- Skills reach both by relative path: `../../brand/BRAND.md` and `../../brand/assets/`, `../../ui-components/base/styles.css` and friends. A skill never keeps its own copy of either layer, if you're about to paste component CSS into a skill's own `references/`, it almost certainly belongs in `ui-components/` instead.
- `create-slides` is the one exception: its canvas-unit coordinate system can't literally share `ui-components/base/styles.css` (screen px vs. a fixed 1920×1080 canvas), so it keeps its own `slides.css` implementation, translated to match the same design language (`ui-components/COMPONENTS.md`'s color/sentiment/chart rules) rather than sharing the file.
- Each `SKILL.md` opens with a gate requiring the brand-layer read (and the component-layer read, for skills that build HTML) and closes with a checklist that includes the guideline's Application Checklist.
- Reference paths are written two ways, and `bundle-skills.py` depends on the difference. Prose and comments name a layer from the **skill root**, `../../brand/tokens.css`, whatever file they sit in, because the skill root is where a reader starts. Code under `scripts/` resolves against its own file instead, so it climbs the real number of levels. Keep new references in whichever form matches, or the bundles fail to build.
- If a color or type value isn't in `BRAND.md` or `tokens.*`, it isn't an Aperia value.

## Ad-hoc branding

There is currently no skill for a freeform request that fits neither
`create-report` nor `create-slides` (a landing page, an email, a one-off
graphic). If that need comes back, either add a thin skill whose only job is
to load `brand/` (and `ui-components/`, if the output needs any of its
pieces) and let the model build the requested format on top, or extend one
of the two existing skills, don't duplicate the reference layers into a new
copy either way.
