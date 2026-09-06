# Aperia UI Components: Reference

> **This is a reference document, not a skill.** It documents the shared
> component library in this folder, cards, badges, callouts, tables, charts,
> timelines, icons, used by every skill in the `aperia` plugin that builds
> HTML (`create-report` directly; `create-slides` in translated canvas
> units). Do not duplicate a component's CSS into a skill, reference it here.
>
> **Companion files** (one folder per toolkit, beside this file):
> - `assemble.py`: fills a document's style marker with the stylesheets below, in order. The one way styles reach an output; nothing is pasted by hand.
> - `base/styles.css`: the base component theme. Injected after `../brand/tokens.css`, which it reads for every palette, type and radius value.
> - `base/`: ready-to-paste markup, one file per group. `structure.html` (card grid, stat row, principle cards, part header), `emphasis.html` (badge, callout, accordion, dark panel, CTA box), `tables.html` (comparison, stack, outcome, tier cards, swatch grid), `charts.html` (ranked bars, proportion bar, scenario bars, estimate range), `timelines.html` (gantt, effort bars, step flow, risk block, and the four dated-checkpoint components).
> - `charts/styles.css` plus `charts/trend.html` (line, area, combo, sparkline), `compare.html` (grouped bars, stacked bars, scatter, bubble, radar), `proportion.html` (pie, donut, treemap, funnel) and `intensity.html` (heatmap, radial gauge), load only if used.
> - `icons/styles.css` / `icons/index.html` / `icons/icon.py`: Lucide icons (MIT), 2,000+ available, fetched from the Lucide CDN on demand, see "Icon toolkit" below.

Everything here is static, hand-authored markup plus CSS, with one
exception: icons are generated on demand by a small script
(`icons/icon.py`) rather than pasted from a fixed list, see "Icon
toolkit" below. Nothing here is a DATA object or has anything to keep in
sync. It carries no page chrome (nav, hero, footer) and no data-driven
grouped-Gantt subsystem (sgantt), those are `create-report`-specific and
documented in that skill's own files.

## How a skill consumes this layer

1. Read **`../brand/BRAND.md`** in full. The values it names live in **`../brand/tokens.css`**, the only place a foundation value is defined, guideline and system alike.
2. Put one marker where the styles go, `<style>/* @aperia report */</style>` (a deck uses `slides`), and run **`assemble.py <file>`** from this folder once the document is written. It injects `tokens.css`, then **`base/styles.css`**, then any optional toolkit, then the skill's own theme, byte for byte, and replaces its own block on every re-run. Nothing is pasted by hand and nothing is edited inside the injected block; document-specific rules go in a second `<style>` after it. `base/styles.css` reads the tokens rather than repeating them and adds the surface roles, the status ramp, the environment colors, and two aliases for names the brand layer spells differently (`--sapphire` for `--sapphire-blue`, `--med-gray` for `--medium-gray`). One token, `--fg`, deliberately overrides the brand value; it says so in place and is recorded in `../brand/DEVIATIONS.md` section 4.
3. Load Inter with weight 600 included (`https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap`) with a `<link>` in `<head>`; Arial fallback via the `--sans` token. Body text is Regular, never Bold.
4. Wrap components in `<div class="wrap">...</div>` unless they already sit inside a container with its own width constraint, `.wrap` caps content at 920px, which every component here is designed against.
5. Copy the matching block(s) from the **`base/`** file for that group, fill in real content. Never ship an empty card or lorem ipsum.
6. If you use the `concerns` accordion, ship its toggle script (in `base/emphasis.html`, right after the accordion markup) once per page.
7. If the chart you need is a line, area, combo, scatter, bubble, grouped/stacked bars, pie, donut, radial gauge, treemap, radar, funnel, sparkline, or heatmap (see the Chart toolkit below), add the word `charts` to the marker so **`charts/styles.css`** is injected, and copy markup from the matching **`charts/`** file.
8. If the content needs an inline icon, add the word `icons` to the marker so **`icons/styles.css`** is injected, and copy markup from **`icons/index.html`**, see the Icon toolkit below, including the licensing note, before using them.
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
| A short (≤~6 entry) sequence read left-to-right | `htimeline`, same entries as `vtimeline`, sideways |
| DEV to PROD promotion path, up to 4 | `envchain` |
| DEV to PROD promotion path, 5 or more | `vtimeline` or `htimeline` with `envc e-*` entries |
| Assumptions, risks and dependencies | `ard`, three columns |

## Icon toolkit (`icons/`)

**[Lucide](https://lucide.dev)** (MIT license, free to use and redistribute,
no restriction to work around), the same icon set `create-slides` uses. Not
a fixed catalog: nothing is bundled. `icons/icon.py` fetches any of the
2,000+ icons from the Lucide CDN on first use, pinned to one release and
cached locally, and emits inline SVG by name,
`python3 icons/icon.py shield-check`, or `--search alert` to find a slug.
`create-slides/scripts/icon.py` is a thin wrapper over this script, so both
skills draw from one icon set. Without network the script says so and exits;
leave the icon out, it is never the only signal.

Every icon is stroke-based (`fill="none" stroke="currentColor"`) and sizes
at `1em`, so it inherits color and size from wherever it sits (see the usage
examples at the top of `icons/index.html`); recolor it the way you'd recolor text,
never by editing the path data or adding a fill.

`icons/index.html` lists a short set of commonly useful slugs as a starting point
(status/feedback, navigation, objects, people, data/trend), it is not the
full set. Run the script's `--search` for anything not listed there before
concluding Lucide doesn't have it; with 2,000+ icons it almost always does.

- **An icon is a supplement to a color/label, never a replacement for one.** Status still rides the badge/callout/marker color system already documented elsewhere in this file; an icon just adds a recognizable shape next to it (see the `callout amber` example in `icons/index.html`, which keeps `.amber`'s color and adds `triangle-alert` beside it, rather than the icon carrying the meaning alone).
- **Don't hand-write or guess at path data.** Always generate the SVG from the script. A hand-drawn "close enough" icon won't match Lucide's grid or stroke weight.
- Size with `.icon-sm`/`.icon-md`/`.icon-lg`/`.icon-xl` for a standalone icon, or leave the bare `.icon` class to inherit `1em` inline with text.

## Chart toolkit

One category, whatever the underlying geometry, a bar, a curve, an arc and a
grid square are all still just a chart. Everything through `bchart`/`stack`/
`tier-wrap` lives in `base/styles.css` (already loaded in step 2 above).
Everything from `linechart` down needs `charts/styles.css` and the matching `charts/` file too,
load them per step 7 before using any row marked **(charts/)**. That
split is a file-loading convenience only (no report needs a radar chart, so
it isn't force-loaded into every one); it is not a second category, and
nothing below treats it as one.

| Content type | Component |
|---|---|
| Estimate with real uncertainty | `pert-cols` + `pert-bar-track` gradient |
| Ranked quantities on a real common scale | `bchart`, sorted descending, never for categorical data |
| Proportions of a whole, ≤6 categories, precise comparison matters | `stack` proportional bar + % in legend |
| Proportions of a whole, ≤5 slices, a circle is the expected form (an exec "here's the mix" moment) | `piechart` **(charts/)** |
| Same, plus a meaningful running total to put in the center | `donutchart` **(charts/)** |
| How scope/scenario choices shift a total | `scn-wrap` (base + hatched addition) |
| Complexity tiers with item counts | `tier-wrap` 3-column cards |
| One series over time | `linechart` **(charts/)** |
| Two or three series over time, one comparable to another | `linechart` with a `.compare` dashed line **(charts/)**, or `gbar` if the x-axis is categorical rather than continuous |
| Volume under a trend, single series | `areachart` **(charts/)** |
| Composition of a total changing over time | `areachart`, stacked, two cumulative polygons, never independently-filled series **(charts/)** |
| Two metrics on different scales over the same timeline | `combochart`, bars + line, dual axis **(charts/)** |
| Two to three series compared across a handful of categories | `gbar`, grouped bars **(charts/)** |
| Many categories, each with an internal composition, over time or sequence | `sbar`, stacked category bars, not `stack` above, which is one bar for one whole **(charts/)** |
| Correlation between two numeric variables | `scatterchart` **(charts/)** |
| Correlation between two variables plus a third magnitude, or a 4-quadrant classification | `bubblechart` **(charts/)** |
| One metric against its own min-max range | `gauge-card`, never a pie or donut for this **(charts/)** |
| Hierarchical or categorical proportions of a whole, more than ~6 categories | `treemap`, area-correct via `flex-grow`, not percentages **(charts/)** |
| A profile across 5-7 named dimensions, 1-2 subjects | `radar-card` **(charts/)** |
| A sequential process with drop-off at each stage | `funnel` **(charts/)** |
| A single number plus its recent trend | `spark-card` **(charts/)** |
| Intensity across two categorical axes (e.g., time × day) | `heatmap` **(charts/)** |

**Pie and donut are sanctioned, but for a narrow job**: a part-to-whole story
with at most 5 slices, where a circle is what the audience expects (an
exec-summary "here's the mix" moment), not a place precise comparison
matters. Past 5 categories, or whenever two slices are close enough in size
that the reader needs to compare them precisely, angles stop being legible,
group the long tail into one "Other" slice (see the donut example in
`charts/proportion.html`) or reach for `stack`/`bchart` instead, both of which compare
more precisely than a pie ever will. `gauge-card` is a different job
entirely and is not a pie/donut substitute: it shows one value against its
own min-max range, never a categorical breakdown.

**Skills may narrow this further.** `create-report` bans pie charts outright
(see that skill's own rules), this toolkit's ≤5-slice allowance is the
permissive default, not a floor every consumer must offer.

### Chart rules

- **Bar chart consistency (`bchart`)**: no inline `style=` on `.bval`/`.bname`/`.beff`; no non-row content inside `.bchart`; header row uses the same column divs, count and order as data rows; never mix rows with different column counts; `.bval` holds only a number, never a badge or label.
- **No manufactured percentages.** If you'd have to invent a number to make a `bchart` or `stack` work, the data is categorical, use `stack-table` instead.
- **No absolute-positioned floating labels** over a bar track, they overlap on narrow viewports. **No z-index stacking inside bar tracks**, use `display:flex; overflow:hidden` so segments sit side by side.
- **One shared coordinate frame for the SVG family.** `linechart`, `areachart`, `combochart`, `scatterchart`, and `bubblechart` all use the same 640×300 `viewBox` and plot geometry (documented in `charts/styles.css`'s header comment) so they read consistently if more than one appears on a page. Recompute point positions with that comment's formulas for your own data, never eyeball pixel values, and never change the viewBox for one chart without changing the formulas to match.
- **Series color order is fixed**: `s1` aperia-blue, `s2` dark-blue, `s3` sapphire, `s4` sky-blue (light, pair with dark text where it fills an area), `s5` light-blue, `s6` dark-gray, `s7` a neutral (med-gray/`--muted`) for a long tail or "other" bucket. Assign series to `s1` outward in the order they matter most; never skip ahead to a later token for a series that isn't literally last in importance.
- **Comparison, not a second focal series, is dashed.** A prior period, a baseline, or a benchmark uses `.compare` (line/combo) or `.radar-poly.compare` (radar), solid stroke stays reserved for the thing the chart is actually about.
- **A dual-axis combo chart labels both axes, visibly, every time.** Never let the reader assume the bars and the line share a scale.
- **Bubble radius scales by √value, not value.** Otherwise a bubble twice the value reads as four times the area.
- **`piechart`/`donutchart` cap at 5 slices**, sorted descending starting at 12 o'clock going clockwise, and every slice gets a `.pie-legend` entry stating its %, never rely on color or angle alone. Group anything past the 5th slice into one "Other" entry rather than adding a 6th sliver.
- **`piechart`/`donutchart` stops are cumulative conic-gradient percentages** (`color START% END%`), not degrees and not a hand-drawn SVG arc, each slice's END% must equal the next slice's START%, and the last slice ends at exactly 100%.
- **Treemap and stacked-bar/area proportions come from `flex-grow` ratios or true cumulative sums, never hand-typed percentages that might not add to 100.**
- **A heatmap always ships a legend bar and a `title` per cell.** A single-hue opacity ramp is not decodable from color alone in print or for a color-blind reader without the value in the tooltip.
- **A heatmap's row-label gutter is `--hm-labelw`, set on the `.heatmap`** (default 56px, 40px at ≤700px). Word labels need a wider value; never hand-write a `grid-template-columns` override.
- **`gauge-card`'s fill color is a status token** (`.ahead`/`.risk`/`.done`, the same three states the milestone timelines use), chosen for what the number means, not decoration.

## The entry contract (mstone-row / vtimeline / htimeline / envchain)

`mstone-row`, `vtimeline` and `htimeline` all render the same conceptual
entry, whatever it describes, a milestone, an environment, a step:

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
An environment's identity rides its chip only, never the marker, never a
colored card edge. Every skill that renders one of these, including
`create-report`'s DATA-driven delivery plans, which render the same classes
from a `DATA` object instead of hand-authored markup, uses this exact same
contract, so content written for one drops into the other without reshaping.

## Choosing a timeline form

This is the only place this decision is made, every row above defers here.

| Question | Answer |
|---|---|
| ≤4 dated milestones, no need to fill more than a small card each? | `mstone-row` |
| More than 4 entries, OR any entry needs more than a title + one line of note? | `vtimeline` |
| A short (up to ~6) sequence that reads naturally left-to-right, a compact roadmap, a short process, and fits the container width? | `htimeline` |
| DEV→PROD promotion path, ≤4 environments? | `envchain` |
| DEV→PROD promotion path, 5+ environments? | `vtimeline` or `htimeline` with `envc e-*` entries, never a wrapped or vertical `envchain` |

`mstone-row` wraps to a ragged second row past 4 entries (it's an auto-fit
grid with a 190px minimum inside a 920px `.wrap`), that wrap is the defect
these rules exist to prevent. If a set grows past its form's limit, change
the component, never widen the container.

`htimeline` is the sideways form: each `.ht-item` takes an equal flex share
of the row, so more than about 6 entries or entries carrying real body text
crowd each other under `.wrap`'s 920px cap. When in doubt, prefer
`vtimeline`, it degrades gracefully at any length, `htimeline` does not.
`htimeline` needs no separate mobile markup: at ≤700px it collapses onto the
same vertical rail `vtimeline` uses, handled entirely by `base/styles.css`.

## Timeline / process rules (not charts, but the same "never fake it" spirit)

- **No equal-width timeline bars for a sequence.** `tline-bars` is for effort *distribution* only (`flex:N`, bars sit flush and share one row); a real schedule is `gantt` or a milestone timeline. Flush bars read as one segmented bar, not phases progressing over time.
- **No `principles` grid for a sequential process.** Use `flow`.
- **`gantt` positioning**: `left% = (start/T)*100`, `width% = (duration/T)*100` where T is total days; verify each row's `left + width` equals the next row's `left`. Axis ticks carry no space (`60d`), `white-space:nowrap`, first/last ticks aligned to the axis edges (already handled by the shipped CSS).
- **`tline-bars` and `gantt` bars use `b1` to `b7`**, the same fixed series order as the chart `s1` to `s7` classes: assign from `b1` outward in phase order and stop where the phases stop. `b4`, `b5` and `b7` already pair dark text with their light fills, so never override a bar's `color`.
- **`gantt` mobile reset is mandatory**: at ≤700px the CSS resets bars to left-anchored fills, but the per-bar width overrides in the `@media` block are per-report and must be recomputed for your phase durations (scaled to the longest phase), or bars render as slivers.

## Checklist before delivering

- [ ] `BRAND.md` read this session, no palette or size values from memory
- [ ] `assemble.py` run after the last edit; nothing typed or edited inside the injected `<style data-aperia>` block
- [ ] Inter loaded with weight 600; Arial fallback declared; body text Regular, never Bold
- [ ] Every size is a `--text-*` token; no raw px, no new step, nothing below `--text-xs`, no bare `h1`..`h6` rule setting `font-size`
- [ ] Shape from `--radius` / `--radius-sm` / `--radius-pill`; no literal `border-radius` other than `50%` for a circle
- [ ] Only palette colors: core blues and neutrals, nothing else
- [ ] No colored border accents on cards or panels (status rides the marker/chip, identity rides the chip, per BRAND.md)
- [ ] Recommended option in any comparison table carries `.hl`
- [ ] Badge/callout colors signal sentiment (red=problem, amber=caution, blue=direction, green=positive)
- [ ] No empty cards, no lorem ipsum
- [ ] Content wrapped in `.wrap` (or an equivalent width-capped container)
- [ ] Every component present collapses correctly at ≤700px (check the table in `base/styles.css`'s responsive block for the ones you used)
- [ ] `concerns` accordion, if used, ships its toggle script once
- [ ] Milestone sets of more than 4 use `vtimeline`, not a wrapped `mstone-row`; environment chains of 5+ use `vtimeline`/`htimeline`, not a wrapped or vertical `envchain`
- [ ] `htimeline` used only for ≤~6 short entries; longer or text-heavy sets use `vtimeline` instead
- [ ] Unique gradient/clip `id`s if more than one `dark-panel`/`cta-box` graphic element appears on the page

### Icons, only if used

- [ ] The marker carries the word `icons`, so `icons/styles.css` was injected
- [ ] Every icon was generated by `icons/icon.py`, not hand-written, `fill="none" stroke="currentColor"`, unedited, not recolored by touching the path
- [ ] An icon sits beside a badge/callout/color that already carries the status meaning, never as the only signal

### Charts, only if used (either file)

- [ ] `piechart`/`donutchart` used only for the part-to-whole job (never as a substitute for `gauge-card`'s single-value job), capped at 5 slices, long tail grouped into "Other"
- [ ] Every pie/donut slice has a `.pie-legend` entry with its %; conic-gradient stops are cumulative and the last one ends at 100%
- [ ] `bchart` rows use the flex model, not fixed-px grids; `.bval` holds a number only
- [ ] `scn-wrap` bars use `display:flex; overflow:hidden`, no z-index stacking
- [ ] If any row uses `charts/styles.css`: the marker carries the word `charts`, so it was injected
- [ ] `linechart`/`areachart`/`combochart`/`scatterchart`/`bubblechart` all share the one 640×300 frame and its formulas, point positions computed, not eyeballed
- [ ] Series colored `s1` outward in order of importance, `s6`/neutral reserved for "other"/long tail
- [ ] A comparison series (prior period, baseline, benchmark) is dashed (`.compare`), never a second solid focal line
- [ ] A `combochart`'s two axes are both labeled on the chart itself
- [ ] Bubble radius in `bubblechart` scales by √value, not value directly
- [ ] `treemap`/`sbar` proportions come from `flex-grow` values or true cumulative sums, not hand-typed percentages
- [ ] `heatmap` ships its legend bar and a `title` on every cell
- [ ] `gauge-card`'s fill color is one of the `.ahead`/`.risk`/`.done` status tokens, chosen for what the value means
- [ ] Every chart present collapses correctly at ≤700px
