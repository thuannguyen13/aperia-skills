# Maintaining

For people editing this repo. To install and use the plugin, see [README.md](README.md).

## Change the brand

1. Edit `plugins/aperia/brand/`: `BRAND.md` first, then `tokens.css`, and `assets/` to match. They must never drift from `BRAND.md`.
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
- Every hex in the plugin is either in `tokens.css` or listed in a fenced ```approved block in `brand/DEVIATIONS.md`. The palette is read from `tokens.css` rather than hardcoded, so the check cannot drift from the tokens.

Off-palette values are a decision, not an accident. Anything the check flags gets fixed or written into `plugins/aperia/brand/DEVIATIONS.md` with a reason. That file is both the audit trail and the allowlist. It currently covers the semantic status colors, the report theme's light tint ramp, the deck theme's dark chart ramp, the PowerPoint template accent alternates, and the `#004583` vs `#004785` mismatch between the supplied SVG assets and the guideline table.

Approval is structural: only hexes inside a fenced ```approved block count. Mentioning a value in prose, in a "was" column, or in a paragraph explaining why it was dropped does not approve it. Approval is plugin-wide rather than per file, so a value approved for one theme will pass in the other; scope it by narrative if that matters.

## Conventions

- `brand/` holds reference files only, with no frontmatter, so nothing there loads as a skill alongside the three real ones.
- Skills reach it by relative path: `../../brand/BRAND.md`, and brand assets by `../../brand/assets/`. A skill never keeps its own copy of either.
- Each `SKILL.md` opens with a gate requiring that read and closes with a checklist that includes the guideline's Application Checklist.
- If a color or type value isn't in `BRAND.md` or `tokens.*`, it isn't an Aperia value.

## Ad-hoc branding

A reference file doesn't auto-trigger the way a skill does, so the brand layer loads only through a skill. Requests that fit neither `create-report` nor `create-slides` are covered by `apply-branding`, whose only job is to load the brand layer and let the model build the requested format on top of it.
