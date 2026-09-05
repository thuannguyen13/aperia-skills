# Changelog

## 0.3.0

- **Removed the `apply-branding` and `apply-ui-components` skills.** The
  plugin now ships two skills, `create-report` and `create-slides`.
- **`apply-ui-components`'s component library moved out of `skills/` into a
  new top-level reference folder, `plugins/aperia/ui-components/`** —
  `styles.css`, `snippets.html`, `charts.css`/`charts.html`,
  `icons.css`/`icons.html`, and a new `COMPONENTS.md` documenting all of it
  (the same role `brand/BRAND.md` plays for the brand layer). It is a
  sibling of `brand/`, not a skill: no frontmatter, nothing auto-invokes it.
  `create-report` reads it the same way it already read `brand/`
  (`../../ui-components/...`); `create-slides` keeps its own canvas-unit
  implementation but follows the same design language, documented in its
  own `SKILL.md`.
- **New build step, `scripts/bundle-skills.py`.** Builds one standalone bundle per skill in `dist/`, inlining the layers that skill reads and rewriting its references, so a skill uploaded on its own to Claude Desktop carries the same files a plugin install would have given it. Without it `create-report` cannot render outside a plugin install, since its base components now live in `ui-components/`. CI builds the bundles on every push and pull request, so a broken layer reference fails there instead of at upload time.
- Fixed two stale reference paths the bundle check surfaced: `brand/tokens.css` pointed at `../BRAND.md` for a file in its own directory, and `brand/DEVIATIONS.md` still named the component theme by its pre-refactor path.
- There is currently no skill for a freeform branding request that fits
  neither `create-report` nor `create-slides` — that was `apply-branding`'s
  job. See `MAINTAINING.md`, "Ad-hoc branding", if that need comes back.

## 0.2.0

- New skill: `apply-ui-components`. A paste-in library of the presentational
  components from the report theme — cards, badges, callouts, tables,
  milestone/status timelines (including a new `htimeline`, the horizontal
  form), a chart toolkit (bar/stacked/scenario/PERT plus the extended family:
  line, area, combo, scatter, bubble, grouped/stacked category bars, a
  constrained pie/donut, radial gauge, treemap, radar, funnel, sparkline,
  heatmap), and a 37-icon set extracted from a licensed Streamline Icon Set —
  for dropping into anything that isn't a full report or deck.
- `create-report` and `create-slides` now consume `apply-ui-components` as
  the shared base component layer instead of maintaining their own parallel
  copies, so a badge, a callout, or a chart series reads the same way across
  every Aperia surface. `create-report`'s own files are trimmed to what's
  actually unique to a full report: nav/hero/footer chrome, the phased-roadmap
  `phases` timeline, and the data-driven `sgantt` delivery-plan subsystem.
  `create-slides` keeps its own canvas-unit implementation (screen tokens
  don't translate to the deck's fixed 1920×1080 coordinate system) but now
  states and follows the same design language explicitly.

## 0.1.0

Initial beta release. Versions below 1.0.0 are beta.

- Three skills: `create-report`, `create-slides`, `apply-branding`.
- Shared brand layer in `plugins/aperia/brand/`: `BRAND.md`, `tokens.css`, `assets/`, `DEVIATIONS.md`. All skills read it at runtime.
- Validation via `scripts/validate.py` and CI: manifests, skill frontmatter, palette conformance, version bump on plugin changes.
