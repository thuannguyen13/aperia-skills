# Aperia Components: Reference

> Reference, not a skill. The shared component library every Aperia HTML skill uses: `create-report` directly, `create-slides` in canvas units through its own theme. Do not copy a component's CSS into a skill.
>
> Beside this file: `assemble.py`, which fills a document's style marker; `base/` (`styles.css` plus `structure.html`, `emphasis.html`, `tables.html`, `charts.html`, `timelines.html`); `charts/` (`styles.css` plus `trend.html`, `compare.html`, `proportion.html`, `intensity.html`); `icons/` (`styles.css`, `index.html`, `icon.py`). The **File** column in the tables below is the one map from a component to the file holding its markup.

This layer carries no page chrome (nav, hero, footer) and no data-driven grouped Gantt; those are `create-report`'s own.

## How to use it

1. One marker where the styles go, `<style>/* @aperia report */</style>` (`page` for a freeform page, `slides` for a deck). Add the word `charts` when a picked component's File is under `charts/`, and `icons` when the page carries an icon. Run `assemble.py <file>` after the document is written and after every later edit. Nothing is typed inside the injected block; document-specific rules go in a second `<style>` after it.
2. Load Inter with a `<link>` in `<head>`: `https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap`. Arial fallback comes from the `--sans` token.
3. Wrap content in `<div class="wrap">`, 920px, unless it already sits in a width-capped container.
4. Pick from the tables below, read the one file the **File** column names, copy the block, fill in real content. No empty cards, no lorem ipsum.
5. The `concerns` accordion ships its toggle script (in `base/emphasis.html`, after the markup) once per page.
6. Sizes come from the `--text-*` tokens with their `--leading-*`, shape from `--radius`, `--radius-sm`, `--radius-pill` or `50%`. No raw px sizes, no other radius.
7. Every component collapses at ≤700px on its own; check the `@media` block at the end of `base/styles.css` for the ones you used.
8. More than one inlined graphic element on a page: a unique `id` on every gradient and clip.

`base/styles.css` reads the brand tokens and adds surface roles, the status ramp (`--st-*`), the environment colors (`--env-*`) and two aliases, `--sapphire` and `--med-gray`. `--fg` overrides the brand value on purpose, recorded in `../brand/DEVIATIONS.md` section 4.

## Component toolkit

| Content type | Component | File |
|---|---|---|
| 4 top-line points / exec summary | 2×2 `card` grid (`.g2`/`.g3`/`.g4`) with badges | `base/structure.html` |
| Inline status/category tag | `badge` (b-blue/b-sky/b-green/b-amber/b-gray/b-red) | `base/emphasis.html` |
| 2 to 4 standalone key numbers | `stat-row`, never `bchart` | `base/structure.html` |
| Inline note | `callout` (blue=neutral, green=positive, amber=warning, red=critical) | `base/emphasis.html` |
| A labelled warning or provenance note | `callout tagged` (add `.soft` for neutral) | `base/emphasis.html` |
| Comparison of options | `cmp-table` with ✓/✗/~ (recommended column gets `.hl`) | `base/tables.html` |
| Categorical list with role/type/focus tags | `stack-table` with badge columns, never `bchart` | `base/tables.html` |
| Role-based before/after outcomes | `outcome-grid` with ↓/↑ | `base/tables.html` |
| Concerns / FAQs | `concerns` accordion (interactive, ships a tiny script) | `base/emphasis.html` |
| Parallel / unordered principles | `principles` grid, never for a sequence | `base/structure.html` |
| Summary / recommendation | `dark-panel` (Aperia Blue + single graphic element) | `base/emphasis.html` |
| The ask | `cta-box` (Aperia Blue + single graphic element) | `base/emphasis.html` |
| Effort distributed across phases (size only, not a schedule) | `tline-bars` (flex:N widths) | `base/timelines.html` |
| A schedule of a few phases on a continuous time axis | `gantt`, staggered rows | `base/timelines.html` |
| A sequential process / method pipeline | `flow`, numbered nodes + rail, never `principles` | `base/timelines.html` |
| Up to 4 dated milestones | `mstone-row` | `base/timelines.html` |
| More than 4 dated milestones, or entries with more body text than a card can hold | `vtimeline` | `base/timelines.html` |
| A short (≤~6 entry) sequence read left-to-right | `htimeline`, same entries as `vtimeline`, sideways | `base/timelines.html` |
| DEV to PROD promotion path, up to 4 | `envchain` | `base/timelines.html` |
| DEV to PROD promotion path, 5 or more | `vtimeline` or `htimeline` with `envc e-*` entries | `base/timelines.html` |
| Assumptions, risks and dependencies | `ard`, three columns | `base/timelines.html` |

Badge and callout colors signal sentiment: red problem, amber caution, blue direction, green positive.

Inline `<code>` is styled by every layer: Inter at Medium weight on a `--muted` chip, white-tinted on dark surfaces. No layer defines a monospace face, so do not add one.

## Icon toolkit (`icons/`)

Lucide (MIT), fetched on demand: `python3 icons/icon.py shield-check` emits inline SVG, `--search alert` finds a slug. Nothing is bundled; `icons/index.html` lists common slugs and the usage markup, not the full set. The script tries two hosts; where neither is reachable, set `APERIA_ICONS_DIR` to a folder of Lucide SVGs and it reads from there. Otherwise it says so; leave the icon out.

- An icon supplements a badge, callout or marker color. It is never the only signal.
- Always generate the SVG with the script. Never hand-write or edit path data, never add a fill; icons are `stroke="currentColor"` and recolor like text.
- Size with `.icon-sm`/`.icon-md`/`.icon-lg`/`.icon-xl` standalone, or bare `.icon` to inherit `1em` inline.

## Chart toolkit

| Content type | Component | File |
|---|---|---|
| Estimate with real uncertainty | `pert-cols` + `pert-bar-track` gradient | `base/charts.html` |
| Ranked quantities on a real common scale | `bchart`, sorted descending, never for categorical data | `base/charts.html` |
| Proportions of a whole, ≤6 categories, precise comparison matters | `stack` proportional bar + % in legend | `base/charts.html` |
| Proportions of a whole, ≤5 slices, a circle is the expected form (an exec "here's the mix" moment) | `donutchart` | `charts/proportion.html` |
| Same, plus a meaningful running total to put in the center | `donutchart` | `charts/proportion.html` |
| How scope/scenario choices shift a total | `bchart` with a `bfill add` segment and a `bdelta` line, ordered by scope not size | `base/charts.html` |
| Complexity tiers with item counts | `tier-wrap` 3-column cards | `base/tables.html` |
| One series over time | trend chart, line form (`cf-line`) | `charts/trend.html` |
| Two or three series over time, one comparable to another | trend chart, line form with a `.compare` dashed line, or `gbar` if the x-axis is categorical rather than continuous | `charts/trend.html` |
| Volume under a trend, single series | trend chart, area form (`cf-area`) | `charts/trend.html` |
| Composition of a total changing over time | trend chart, area form stacked as cumulative polygons, never independently-filled series | `charts/trend.html` |
| Two metrics on different scales over the same timeline | trend chart, combo form (`cf-bar` plus `cf-line`), dual axis | `charts/trend.html` |
| Two to three series compared across a handful of categories | `gbar`, grouped bars | `charts/compare.html` |
| Many categories, each with an internal composition, over time or sequence | `sbar`, stacked category bars, not `stack` above, which is one bar for one whole | `charts/compare.html` |
| Correlation between two numeric variables | `scatterchart` | `charts/compare.html` |
| Correlation between two variables plus a third magnitude, or a 4-quadrant classification | `bubblechart` | `charts/compare.html` |
| One metric against its own min-max range | `gauge-card`, never a pie or donut for this | `charts/intensity.html` |
| Hierarchical or categorical proportions of a whole, more than ~6 categories | `treemap`, area-correct via `flex-grow`, not percentages | `charts/proportion.html` |
| A profile across 5-7 named dimensions, 1-2 subjects | `radar-card` | `charts/compare.html` |
| A sequential process with drop-off at each stage | `funnel` | `charts/proportion.html` |
| A single number plus its recent trend | `spark-card` | `charts/trend.html` |
| Intensity across two categorical axes (e.g., time × day) | `heatmap` | `charts/intensity.html` |

### Chart rules

- **No manufactured percentages.** If a number has to be invented to make a `bchart` or `stack` work, the data is categorical: use `stack-table`.
- **`bchart`**: no inline `style=` on `.bval`/`.bname`/`.beff`; only row content inside `.bchart`; header row uses the same column divs, count and order as data rows; `.bval` holds a number and at most a `.bdelta` line. Rows use the flex model, not fixed-px grids.
- **No absolute-positioned labels over a bar track and no z-index stacking inside one.** Segments sit side by side under `display:flex; overflow:hidden`.
- **Series color order is fixed**: `s1` aperia-blue, `s2` dark-blue, `s3` sapphire, `s4` sky-blue (dark text on an area fill), `s5` light-blue, `s6` dark-gray, `s7` neutral for a long tail or "other". Assign from `s1` outward in order of importance; never skip ahead.
- **A comparison series is dashed**: a prior period, baseline or benchmark uses `.compare` (line/combo) or `.radar-poly.compare`. Solid stroke is the focal series only.
- **The trend chart in all three forms, the scatter plot and the bubble chart share one 640×300 `viewBox` and the plot geometry in `charts/styles.css`'s header comment.** Compute point positions with those formulas; never eyeball, never change the viewBox for one chart.
- **The combo form labels both axes on the chart.**
- **`bubblechart` radius scales by √value.**
- **`donutchart`: at most 5 slices**, sorted descending from 12 o'clock clockwise, the long tail grouped into one "Other", every slice with a `.pie-legend` entry stating its %. Stops are cumulative conic-gradient percentages (`color START% END%`), each END equal to the next START, the last at exactly 100%. Only for a part-to-whole story where a circle is expected; where precise comparison matters, `stack` or `bchart`. Never as a substitute for `gauge-card`.
- **`treemap`, `sbar` and stacked area proportions come from `flex-grow` ratios or true cumulative sums**, never hand-typed percentages.
- **`heatmap` ships a legend bar and a `title` on every cell.** Its row-label gutter is `--hm-labelw` on `.heatmap` (56px, 40px at ≤700px); widen it for word labels, never override `grid-template-columns`.
- **`gauge-card` fill is a status token**, `.ahead`/`.risk`/`.done`, chosen for what the number means.

## The entry contract (mstone-row / vtimeline / htimeline / envchain)

One entry shape, whatever it describes: a milestone, an environment, a step.

| Field | Holds |
|---|---|
| lead / m-date / vt-lead / ht-lead | The prominent slot: a date for milestones, an environment name for a chain |
| chip / m-flag / vt-chip / ht-chip | A small pill beside the lead: a flag, a badge |
| title / m-title / vt-title / ht-title | A second line (milestones use it; environments usually omit it) |
| note / m-note / vt-note / ht-note | The body line |
| cls | Status: `done` `risk` `est` (nothing = "ahead", the default blue), plus `envc e-dev`/`e-qa`/`e-uat`/`e-stag`/`e-prod` for an environment entry |

Status rides the marker in three states, no legend: blue ahead, amber for risk or an estimated date (`est` also hollows the marker and dashes the connector), green for done or the final live environment. An environment's identity rides its chip only, never the marker, never a card edge. `create-report`'s DATA-driven plans render the same classes from a `DATA` object.

## Choosing a timeline form

The one place this decision is made.

| Question | Answer |
|---|---|
| ≤4 dated milestones, no need to fill more than a small card each? | `mstone-row` |
| More than 4 entries, OR any entry needs more than a title + one line of note? | `vtimeline` |
| A short (up to ~6) sequence that reads naturally left-to-right, a compact roadmap, a short process, and fits the container width? | `htimeline` |
| DEV→PROD promotion path, ≤4 environments? | `envchain` |
| DEV→PROD promotion path, 5+ environments? | `vtimeline` or `htimeline` with `envc e-*` entries, never a wrapped or vertical `envchain` |

`mstone-row` and `envchain` wrap to a ragged second row past 4 entries; that wrap is the defect. Past a form's limit, change the component, never widen the container. `htimeline` crowds past about 6 entries or with body text; when in doubt, `vtimeline`. At ≤700px `htimeline` collapses onto the vertical rail on its own.

## Timeline and process rules

- **`tline-bars` is effort distribution only** (`flex:N`, flush bars in one row). A real schedule is `gantt` or a milestone timeline.
- **A sequential process is `flow`, never a `principles` grid.**
- **`gantt` positioning**: `left% = (start/T)*100`, `width% = (duration/T)*100`, T the total days; each row's `left + width` equals the next row's `left`. Axis ticks carry no space (`60d`).
- **`tline-bars` and `gantt` bars use `b1` to `b7`** in phase order, the same ramp as `s1` to `s7`. `b4`, `b5` and `b7` carry dark text on light fills; never override a bar's `color`.
- **`gantt` mobile reset**: at ≤700px the CSS resets bars to left-anchored fills, but the per-bar width overrides in the `@media` block are per document and must be recomputed for your phase durations, scaled to the longest phase.
