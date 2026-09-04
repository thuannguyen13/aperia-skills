# Aperia UI Components: Reference

> **This is a reference document, not a skill.** It documents the shared
> component library in this folder — cards, badges, callouts, tables, charts,
> timelines, icons — used by every skill in the `aperia` plugin that builds
> HTML (`create-report` directly; `create-slides` in translated canvas
> units). Do not duplicate a component's CSS into a skill, reference it here.
>
> **Companion files** (same directory):
> - `styles.css`: the base component theme. Paste after `../brand/tokens.css`'s `:root` block.
> - `snippets.html`: ready-to-paste markup for every component below.
> - `charts.css` / `charts.html`: the extended chart family (line, area, combo, scatter, bubble, grouped/stacked bars, pie, donut, radial gauge, treemap, radar, funnel, sparkline, heatmap) — load only if used.
> - `icons.css` / `icons.html` / `scripts/icon.py` / `assets/lucide-icons.json`: Lucide icons (MIT), 2000+ available, generated on demand — see "Icon toolkit" below.

Everything here is static, hand-authored markup plus CSS, with one
exception: icons are generated on demand by a small script
(`scripts/icon.py`) rather than pasted from a fixed list — see "Icon
toolkit" below. Nothing here is a DATA object or has anything to keep in
sync. It carries no page chrome (nav, hero, footer) and no data-driven
grouped-Gantt subsystem (sgantt) — those are `create-report`-specific and
documented in that skill's own files.

## How a skill consumes this layer

1. Read **`../brand/BRAND.md`** in full, and paste **`../brand/tokens.css`**'s `:root` block into the output's `<style>`.
2. Paste **`styles.css`** from this folder **after** it, verbatim. Order matters: the two blocks name a few things differently (`--sapphire-blue` in the brand layer vs `--sapphire` here) and redefine `--radius` and the `--text-*` steps identically; pasting the component theme second means it wins on any shared name, which is what the components are written against, while the brand block still supplies `--min-size`, `--font-sans`, the `--fw-*` weights and `--grad-hero`.
3. Load Inter with weight 600 included (`https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap`); Arial fallback via the `--sans` token. Body text is Light/Regular, never Bold.
4. Wrap components in `<div class="wrap">...</div>` unless they already sit inside a container with its own width constraint — `.wrap` caps content at 920px, which every component here is designed against.
5. Copy the matching block(s) from **`snippets.html`**, fill in real content. Never ship an empty card or lorem ipsum.
6. If you use the `concerns` accordion, ship its toggle script (in `snippets.html`, right after the accordion markup) once per page.
7. If the chart you need is a line, area, combo, scatter, bubble, grouped/stacked bars, pie, donut, radial gauge, treemap, radar, funnel, sparkline, or heatmap (see the Chart toolkit below), also paste **`charts.css`** after `styles.css`, and copy markup from **`charts.html`**.
8. If the content needs an inline icon, also paste **`icons.css`** and copy markup from **`icons.html`** — see the Icon toolkit below, including the licensing note, before using them.
9. Run the checklist at the bottom of this file and the Application Checklist in `../brand/BRAND.md`.

**Do not work from memory of the palette or the type rules.** If a value is not in `BRAND.md` or `tokens.css`, it is not an Aperia value. Do not invent it.

## Component toolkit

| Content type | Component |
|---|---|
| 4 top-line points / exec summary | 2×2 `card` grid (`.g2`/`.g3`/`.g4`) with badges |
| Inline status/category tag | `badge` (b-blue/b-sky/b-green/b-amber/b-gray/b-red) |
| 2 to 4 standalone key numbers | `stat-row`, never `bchart` |
| Inline note | `callout` (blue=neutral, green=positive, amber=warning, red=critical) |
| A labelled warning or provenance note | `callout tagged` (add `.soft` for neutral) |
| A small set of named colors | `swatch-grid` |
| Comparison of options | `cmp-table` with ✓/✗/~ (recommended column gets `.hl`) |
| Categorical list with role/type/focus tags | `stack-table` with badge columns, never `bchart` |
| Role-based before/after outcomes | `outcome-grid` with ↓/↑ |
| Concerns / FAQs | `concerns` accordion (interactive, ships a tiny script) |
| Parallel / unordered principles | `principles` grid, never for a sequence |
| Summary / recommendation | `dark-panel` (Aperia Blue + single graphic element) |
| The ask | `cta-box` (Aperia Blue + single graphic element) |
| Effort distributed across phases (size only, not a schedule) | `tline-bars` (flex:N widths) |
| A schedule of a few phases on a continuous time axis | `gantt`, staggered rows |
| A sequential process / method pipeline | `flow`, numbered nodes + rail, never `principles` |
| Up to 4 dated milestones | `mstone-row` |
| More than 4 dated milestones, or entries with more body text than a card can hold | `vtimeline` |
| A short (≤~6 entry) sequence read left-to-right | `htimeline` — same entries as `vtimeline`, sideways |
| DEV to PROD promotion path, up to 4 | `envchain` |
| DEV to PROD promotion path, 5 or more | `vtimeline` or `htimeline` with `envc e-*` entries |
| Assumptions, risks and dependencies | `ard`, three columns |

## Icon toolkit (`icons.css` / `icons.html` / `scripts/icon.py`)

**[Lucide](https://lucide.dev)** (MIT license — free to use and redistribute,
no restriction to work around), the same icon set `create-slides` uses. Not
a fixed catalog: `assets/lucide-icons.json` bundles 2000+ icons, and
`scripts/icon.py` emits inline SVG for any of them by name —
`python3 scripts/icon.py shield-check`, or `--search alert` to find a slug.
`create-slides/scripts/icon.py` points at this same JSON file rather than
keeping its own copy, so both skills draw from one icon set.

Every icon is stroke-based (`fill="none" stroke="currentColor"`) and sizes
at `1em`, so it inherits color and size from wherever it sits (see the usage
examples at the top of `icons.html`); recolor it the way you'd recolor text,
never by editing the path data or adding a fill.

`icons.html` lists a short set of commonly useful slugs as a starting point
(status/feedback, navigation, objects, people, data/trend) — it is not the
full set. Run the script's `--search` for anything not listed there before
concluding Lucide doesn't have it; with 2000+ icons it almost always does.

- **An icon is a supplement to a color/label, never a replacement for one.** Status still rides the badge/callout/marker color system already documented elsewhere in this file; an icon just adds a recognizable shape next to it (see the `callout amber` example in `icons.html`, which keeps `.amber`'s color and adds `triangle-alert` beside it, rather than the icon carrying the meaning alone).
- **Don't hand-write or guess at path data.** Always generate the SVG from the script. A hand-drawn "close enough" icon won't match Lucide's grid or stroke weight.
- Size with `.icon-sm`/`.icon-md`/`.icon-lg`/`.icon-xl` for a standalone icon, or leave the bare `.icon` class to inherit `1em` inline with text.

## Chart toolkit

One category, whatever the underlying geometry — a bar, a curve, an arc and a
grid square are all still just a chart. Everything through `bchart`/`stack`/
`tier-wrap` lives in `styles.css` (already loaded in step 2 above).
Everything from `linechart` down needs `charts.css` and `charts.html` too —
load them per step 7 before using any row marked **(charts.css)**. That
split is a file-loading convenience only (no report needs a radar chart, so
it isn't force-loaded into every one); it is not a second category, and
nothing below treats it as one.

| Content type | Component |
|---|---|
| Estimate with real uncertainty | `pert-cols` + `pert-bar-track` gradient |
| Ranked quantities on a real common scale | `bchart`, sorted descending, never for categorical data |
| Proportions of a whole, ≤6 categories, precise comparison matters | `stack` proportional bar + % in legend |
| Proportions of a whole, ≤5 slices, a circle is the expected form (an exec "here's the mix" moment) | `piechart` **(charts.css)** |
| Same, plus a meaningful running total to put in the center | `donutchart` **(charts.css)** |
| How scope/scenario choices shift a total | `scn-wrap` (base + hatched addition) |
| Complexity tiers with item counts | `tier-wrap` 3-column cards |
| One series over time | `linechart` **(charts.css)** |
| Two or three series over time, one comparable to another | `linechart` with a `.compare` dashed line **(charts.css)**, or `gbar` if the x-axis is categorical rather than continuous |
| Volume under a trend, single series | `areachart` **(charts.css)** |
| Composition of a total changing over time | `areachart`, stacked — two cumulative polygons, never independently-filled series **(charts.css)** |
| Two metrics on different scales over the same timeline | `combochart`, bars + line, dual axis **(charts.css)** |
| Two to three series compared across a handful of categories | `gbar`, grouped bars **(charts.css)** |
| Many categories, each with an internal composition, over time or sequence | `sbar`, stacked category bars — not `stack` above, which is one bar for one whole **(charts.css)** |
| Correlation between two numeric variables | `scatterchart` **(charts.css)** |
| Correlation between two variables plus a third magnitude, or a 4-quadrant classification | `bubblechart` **(charts.css)** |
| One metric against its own min-max range | `gauge-card` — never a pie or donut for this **(charts.css)** |
| Hierarchical or categorical proportions of a whole, more than ~6 categories | `treemap`, area-correct via `flex-grow`, not percentages **(charts.css)** |
| A profile across 5-7 named dimensions, 1-2 subjects | `radar-card` **(charts.css)** |
| A sequential process with drop-off at each stage | `funnel` **(charts.css)** |
| A single number plus its recent trend | `spark-card` **(charts.css)** |
| Intensity across two categorical axes (e.g., time × day) | `heatmap` **(charts.css)** |

**Pie and donut are sanctioned, but for a narrow job**: a part-to-whole story
with at most 5 slices, where a circle is what the audience expects (an
exec-summary "here's the mix" moment), not a place precise comparison
matters. Past 5 categories, or whenever two slices are close enough in size
that the reader needs to compare them precisely, angles stop being legible —
group the long tail into one "Other" slice (see the donut example in
`charts.html`) or reach for `stack`/`bchart` instead, both of which compare
more precisely than a pie ever will. `gauge-card` is a different job
entirely and is not a pie/donut substitute: it shows one value against its
own min-max range, never a categorical breakdown.

**Skills may narrow this further.** `create-report` bans pie charts outright
(see that skill's own rules) — this toolkit's ≤5-slice allowance is the
permissive default, not a floor every consumer must offer.

### Chart rules

- **Bar chart consistency (`bchart`)**: no inline `style=` on `.bval`/`.bname`/`.beff`; no non-row content inside `.bchart`; header row uses the same column divs, count and order as data rows; never mix rows with different column counts; `.bval` holds only a number, never a badge or label.
- **No manufactured percentages.** If you'd have to invent a number to make a `bchart` or `stack` work, the data is categorical — use `stack-table` instead.
- **No absolute-positioned floating labels** over a bar track — they overlap on narrow viewports. **No z-index stacking inside bar tracks** — use `display:flex; overflow:hidden` so segments sit side by side.
- **One shared coordinate frame for the SVG family.** `linechart`, `areachart`, `combochart`, `scatterchart`, and `bubblechart` all use the same 640×300 `viewBox` and plot geometry (documented in `charts.css`'s header comment) so they read consistently if more than one appears on a page. Recompute point positions with that comment's formulas for your own data — never eyeball pixel values, and never change the viewBox for one chart without changing the formulas to match.
- **Series color order is fixed**: `s1` aperia-blue, `s2` dark-blue, `s3` sapphire, `s4` sky-blue (light — pair with dark text where it fills an area), `s5` light-blue, `s6` dark-gray, `s7` a neutral (med-gray/`--muted`) for a long tail or "other" bucket. Assign series to `s1` outward in the order they matter most; never skip ahead to a later token for a series that isn't literally last in importance.
- **Comparison, not a second focal series, is dashed.** A prior period, a baseline, or a benchmark uses `.compare` (line/combo) or `.radar-poly.compare` (radar) — solid stroke stays reserved for the thing the chart is actually about.
- **A dual-axis combo chart labels both axes, visibly, every time.** Never let the reader assume the bars and the line share a scale.
- **Bubble radius scales by √value, not value.** Otherwise a bubble twice the value reads as four times the area.
- **`piechart`/`donutchart` cap at 5 slices**, sorted descending starting at 12 o'clock going clockwise, and every slice gets a `.pie-legend` entry stating its % — never rely on color or angle alone. Group anything past the 5th slice into one "Other" entry rather than adding a 6th sliver.
- **`piechart`/`donutchart` stops are cumulative conic-gradient percentages** (`color START% END%`), not degrees and not a hand-drawn SVG arc — each slice's END% must equal the next slice's START%, and the last slice ends at exactly 100%.
- **Treemap and stacked-bar/area proportions come from `flex-grow` ratios or true cumulative sums — never hand-typed percentages that might not add to 100.**
- **A heatmap always ships a legend bar and a `title` per cell.** A single-hue opacity ramp is not decodable from color alone in print or for a color-blind reader without the value in the tooltip.
- **`gauge-card`'s fill color is a status token** (`.ahead`/`.risk`/`.done`, the same three states the milestone timelines use), chosen for what the number means — not decoration.

## The entry contract (mstone-row / vtimeline / htimeline / envchain)

`mstone-row`, `vtimeline` and `htimeline` all render the same conceptual
entry, whatever it describes — a milestone, an environment, a step:

| Field | Holds |
|---|---|
| lead / m-date / vt-lead / ht-lead | The prominent slot: a date for milestones, an environment name for a chain |
| chip / m-flag / vt-chip / ht-chip | A small pill beside the lead: a flag, a badge |
| title / m-title / vt-title / ht-title | A second line (milestones use it; environments usually omit it) |
| note / m-note / vt-note / ht-note | The body line |
| cls | Status: `done` `risk` `est` (nothing = "ahead", the default blue), plus `envc e-dev`/`e-qa`/`e-uat`/`e-stag`/`e-prod` for an environment entry |

Status rides a three-state marker so no legend is needed: blue for anything
ahead, amber for risk or an estimated date (`est` also hollows the marker and
dashes the connecting line), green for done or the final live environment.
An environment's identity rides its chip only — never the marker, never a
colored card edge. Every skill that renders one of these — including
`create-report`'s DATA-driven delivery plans, which render the same classes
from a `DATA` object instead of hand-authored markup — uses this exact same
contract, so content written for one drops into the other without reshaping.

## Choosing a timeline form

This is the only place this decision is made — every row above defers here.

| Question | Answer |
|---|---|
| ≤4 dated milestones, no need to fill more than a small card each? | `mstone-row` |
| More than 4 entries, OR any entry needs more than a title + one line of note? | `vtimeline` |
| A short (up to ~6) sequence that reads naturally left-to-right — a compact roadmap, a short process — and fits the container width? | `htimeline` |
| DEV→PROD promotion path, ≤4 environments? | `envchain` |
| DEV→PROD promotion path, 5+ environments? | `vtimeline` or `htimeline` with `envc e-*` entries — never a wrapped or vertical `envchain` |

`mstone-row` wraps to a ragged second row past 4 entries (it's an auto-fit
grid with a 190px minimum inside a 920px `.wrap`) — that wrap is the defect
these rules exist to prevent. If a set grows past its form's limit, change
the component, never widen the container.

`htimeline` is the sideways form: each `.ht-item` takes an equal flex share
of the row, so more than about 6 entries or entries carrying real body text
crowd each other under `.wrap`'s 920px cap. When in doubt, prefer
`vtimeline` — it degrades gracefully at any length, `htimeline` does not.
`htimeline` needs no separate mobile markup: at ≤700px it collapses onto the
same vertical rail `vtimeline` uses, handled entirely by `styles.css`.

## Timeline / process rules (not charts, but the same "never fake it" spirit)

- **No equal-width timeline bars for a sequence.** `tline-bars` is for effort *distribution* only (`flex:N`, bars sit flush and share one row); a real schedule is `gantt` or a milestone timeline. Flush bars read as one segmented bar, not phases progressing over time.
- **No `principles` grid for a sequential process.** Use `flow`.
- **`gantt` positioning**: `left% = (start/T)*100`, `width% = (duration/T)*100` where T is total days; verify each row's `left + width` equals the next row's `left`. Axis ticks carry no space (`60d`), `white-space:nowrap`, first/last ticks aligned to the axis edges (already handled by the shipped CSS).
- **`gantt` mobile reset is mandatory**: at ≤700px the CSS resets bars to left-anchored fills, but the per-bar width overrides in the `@media` block are per-report and must be recomputed for your phase durations (scaled to the longest phase), or bars render as slivers.

## Checklist before delivering

- [ ] `BRAND.md` and `tokens.css` read this session, no palette or size values from memory
- [ ] `<style>` block is the `tokens.css` `:root` first, then `styles.css` verbatim
- [ ] Inter loaded with weight 600; Arial fallback declared; body text Light/Regular, never Bold
- [ ] Every size is a `--text-*` token; no raw px, no new step, nothing below `--text-xs`, no bare `h1`..`h6` rule setting `font-size`
- [ ] Shape from `--radius` / `--radius-pill`; no literal `border-radius:100px`
- [ ] Only palette colors: core blues and neutrals, nothing else
- [ ] No colored border accents on cards or panels (status rides the marker/chip, identity rides the chip, per BRAND.md)
- [ ] Recommended option in any comparison table carries `.hl`
- [ ] Badge/callout colors signal sentiment (red=problem, amber=caution, blue=direction, green=positive)
- [ ] No empty cards, no lorem ipsum
- [ ] Content wrapped in `.wrap` (or an equivalent width-capped container)
- [ ] Every component present collapses correctly at ≤700px (check the table in `styles.css`'s responsive block for the ones you used)
- [ ] `concerns` accordion, if used, ships its toggle script once
- [ ] Milestone sets of more than 4 use `vtimeline`, not a wrapped `mstone-row`; environment chains of 5+ use `vtimeline`/`htimeline`, not a wrapped or vertical `envchain`
- [ ] `htimeline` used only for ≤~6 short entries; longer or text-heavy sets use `vtimeline` instead
- [ ] Unique gradient/clip `id`s if more than one `dark-panel`/`cta-box` graphic element appears on the page

### Icons, only if used

- [ ] `icons.css` pasted after `styles.css`, in the same `<style>` block
- [ ] Every icon was generated by `scripts/icon.py`, not hand-written — `fill="none" stroke="currentColor"`, unedited, not recolored by touching the path
- [ ] An icon sits beside a badge/callout/color that already carries the status meaning, never as the only signal

### Charts, only if used (either file)

- [ ] `piechart`/`donutchart` used only for the part-to-whole job (never as a substitute for `gauge-card`'s single-value job), capped at 5 slices, long tail grouped into "Other"
- [ ] Every pie/donut slice has a `.pie-legend` entry with its %; conic-gradient stops are cumulative and the last one ends at 100%
- [ ] `bchart` rows use the flex model, not fixed-px grids; `.bval` holds a number only
- [ ] `scn-wrap` bars use `display:flex; overflow:hidden`, no z-index stacking
- [ ] If any row uses `charts.css`: it's pasted after `styles.css`, in the same `<style>` block
- [ ] `linechart`/`areachart`/`combochart`/`scatterchart`/`bubblechart` all share the one 640×300 frame and its formulas — point positions computed, not eyeballed
- [ ] Series colored `s1` outward in order of importance, `s6`/neutral reserved for "other"/long tail
- [ ] A comparison series (prior period, baseline, benchmark) is dashed (`.compare`), never a second solid focal line
- [ ] A `combochart`'s two axes are both labeled on the chart itself
- [ ] Bubble radius in `bubblechart` scales by √value, not value directly
- [ ] `treemap`/`sbar` proportions come from `flex-grow` values or true cumulative sums, not hand-typed percentages
- [ ] `heatmap` ships its legend bar and a `title` on every cell
- [ ] `gauge-card`'s fill color is one of the `.ahead`/`.risk`/`.done` status tokens, chosen for what the value means
- [ ] Every chart present collapses correctly at ≤700px
