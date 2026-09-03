# Changelog

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
