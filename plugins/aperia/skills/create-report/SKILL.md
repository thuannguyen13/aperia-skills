---
name: create-report
description: Generate professional, on-brand HTML strategic reports, briefings, reviews, and proposals in the Aperia brand identity. Use whenever the user wants an Aperia report, branded report, executive briefing, strategic review, client proposal, or any structured long-form document that should follow the Aperia brand guidelines, including phrasings like "Aperia report", "write this up as a briefing", "turn this into a proposal", or any request for a polished, shareable long-form document in the Aperia look and feel. For Aperia branding on anything that is not a report or a deck, use the apply-branding skill instead. Output is a single self-contained HTML file with sticky navigation, a gradient hero, sections, cards, data visualizations, comparison tables, phased roadmaps, accordions, and, for delivery and release plans, a searchable grouped Gantt with milestone cards, an environment chain and an Assumptions / Risks / Dependencies block.
---

# Aperia Report

Produces a single self-contained HTML strategic report in the Aperia brand identity.

## Step 0: Read the brand layer first (required)

Before writing a single line of HTML:

1. Read **`../../brand/BRAND.md`** in full.
2. Read **`../../brand/tokens.css`** and paste its `:root` block into your `<style>`.
3. Read **`references/styles.css`** (the full Aperia report theme) and **`references/snippets.html`** (ready-to-paste markup).
4. If the report is a delivery, release or roadmap plan, read **`references/interactive.html`** (the script-driven delivery-plan components and the DATA-object contract).

**Do not work from memory of the palette, the type rules, or the graphic-element rules.** They live in `BRAND.md` and only there. If a value you want is not in `BRAND.md` or `tokens.css`, it is not an Aperia value. Do not invent it.

Brand assets are at `../../brand/assets/`. Inline the SVGs, never link them.

---

## Workflow

1. **Read the user's content.** Identify the title, subtitle, audience, core sections, and the one message the reader should walk away with.
2. **Choose visualizations strategically.** See "Strategic visualization thinking" below. Numbers become range bars or bar charts, not stat cards alone; proportions become stacked bars; timelines get proportional widths.
3. **Map each section to a component** from the toolkit.
4. **Build one self-contained HTML file**: Google Fonts link, the pasted theme, skip link, nav, hero, sections, dark panel / CTA, footer, scripts.
5. **Apply brand assets** per `BRAND.md`: logo in nav (Aperia Blue) and footer (recolored `#FFFFFF`); `pattern-double` in the hero; `pattern-single` in dark panels and CTA boxes.
6. **Run the checklist** at the bottom of this file *and* the Application Checklist in `BRAND.md`.
7. **Save and deliver** the file, then tell the user it opens in any browser, prints to PDF, and is shareable as-is.

If the user gives minimal content, scaffold intelligently and flag what to replace. Never leave a section empty or filled with lorem.

---

## Strategic visualization thinking

**Default to visuals that encode meaning, not just display numbers.** Ask: what is the insight? Then choose the form that makes it undeniable at a glance.

| Insight type | Best visual form | Avoid |
|---|---|---|
| A number has real uncertainty | `pert-cols` (3-column range) + `pert-bar-track` gradient | Lone stat card |
| A few items dominate the total | `bchart` horizontal bars, sorted descending | Unsorted table |
| Item count vs effort are asymmetric | `bchart` with `beff` hr/item column | Just a total |
| How scope decisions shift a total | `scn-wrap` scenario bar chart (base + hatched add) | Bullet list |
| Proportions of a whole | `stack` proportional stacked bar + % in legend | Pie chart |
| Complexity tiers with item counts | `tier-wrap` 3-column cards with top border color | Plain list |
| A sequential process, each stage feeding the next | `flow` step pipeline (numbered nodes + rail) | `principles` grid (implies parallel) |
| A schedule of a few phases, one bar each, on a continuous axis | `gantt` staggered rows on a shared time axis | Flush proportional bars |
| A schedule of many work items over named sprints or stages, grouped and searchable | `sgantt` grouped Gantt, rendered from DATA | `gantt`, which assumes one bar per row on a continuous axis |
| Effort distributed across phases (size only, not a schedule) | `tline-bars` with `flex:N` widths | Equal-width boxes |
| Qualitative, unordered principles | `principles` 2-col grid | Numbered prose |
| Up to 4 dated checkpoints | `mstone-row` milestone cards, status on the top border | A table of dates |
| More than 4 dated checkpoints | `vtimeline` vertical rail, three-state marker | `mstone-row` wrapped onto a second row |
| A promotion path of up to 4 environments | `envchain` DEV to PROD cards | `flow` (loses the per-environment identity) |
| A promotion path of 5 or more environments | `vtimeline` with `envc e-*` entries | A vertical variant of `envchain` |
| What the plan assumes, risks and waits on | `ard` three-column block | Three bullet lists |

### Chart type selection

Before reaching for a bar chart, ask: **does this data have a real quantitative axis?** If not, a bar chart implies false precision.

| Data character | Right form | Wrong form |
|---|---|---|
| Categorical list with role/type/focus tags, no numeric axis | `stack-table` with badge columns | `bchart` with invented % bars |
| 2 to 4 key numbers where the number is the message | `stat-row` stat cards | `bchart` (bars encode the number redundantly) |
| Ranked quantities on a real common scale | `bchart`, sorted descending | `stat-row` (loses rank) |
| How scope/scenario choices shift a total | `scn-wrap` (base + hatched add) | `bchart` (hides the baseline) |
| Proportions summing to 100% | `stack` bar, % in legend | Pie chart, or `bchart` |
| A sequential process / method pipeline | `flow` | `principles` grid |
| A schedule over time, few phases, one bar each | `gantt` | `tline` flush bars |
| A schedule over time, many grouped rows | `sgantt` | `gantt` with hand-written rows |
| Effort distribution across phases | `tline-bars` with `flex:N` | Equal-width boxes |
| Uncertainty around a central estimate | `pert-cols` + gradient bar | Lone stat card |

**The test:** if you had to invent the numbers to make the bar chart work (e.g. "Coverage Weight: 100%, 80%, 75%"), use `stack-table` instead.

**On pie charts, avoid them.** A pie is only legible with 2 or 3 near-equal slices. Use a `stack` proportional bar with percentages in the legend.

**Sequence vs distribution.** If phases happen *in order over time*, use a Gantt, where each phase is its own row on a time axis. Flush `tline` bars sitting together read as one segmented bar, which misleads when the intent is sequence. Which Gantt is decided in one place only: "Choosing between `gantt` and `sgantt`" under Delivery-plan components. Do not decide it from the tables above.

**Process vs principles.** If steps feed each other in order, use `flow` with numbered nodes and a rail. Reserve `principles` for genuinely parallel, unordered items.

### Bar chart consistency rules

Inconsistent column widths in a `bchart` always come from one of these:

1. **No inline `style=` overrides** on `.bval`, `.bname`, or `.beff`, which change rendered column width relative to the header row.
2. **No non-row content** (labels, `<p>`, headings) inside `.bchart`, which inherits flex layout and distorts the grid.
3. **Header row (`.brow-head`) uses the same column divs as data rows**: same classes, count, and order.
4. **Never mix rows with different column counts.** If one row omits `.beff`, all rows including the header omit it.
5. **`.bval` contains only the numeric value**, never a badge or multi-word label. Use `stack-table` for that.

### Visualization anti-patterns, never do these

- **No absolute-positioned floating labels** over a bar track. They overlap on narrow viewports.
- **No fixed-pixel column grids** in data rows (`180px 60px 1fr`). Use flex with `flex: 0 0 Npx` for fixed cols and `flex:1` for the elastic col.
- **No z-index stacking inside bar tracks.** Use `display:flex; overflow:hidden` so segments sit side by side.
- **No equal-width timeline bars.** Use `flex:N` proportional to duration.
- **No `width:%` on bar fills inside flex tracks.** Reserve `width:%` for fills inside a `position:relative` track with `overflow:hidden`.
- **No manufactured ordinal bars.** Invented percentages make the chart lie. Use `stack-table`.
- **No text labels in `.bval`.** It is a number column.
- **No flush proportional bars for a schedule.** Use a Gantt, chosen per "Choosing between `gantt` and `sgantt`".
- **No `principles` grid for a sequential process.** Use `flow`.
- **No pie charts.**
- **No hand-written `sgantt` rows.** It is rendered from the DATA object. Writing the grid by hand desynchronises the search index, the counts and the tooltip.
- **No `gantt` and `sgantt` in the same report.** They are two answers to one question. Pick one.
- **No status colour as the only signal.** Every milestone card and environment card carries its name and step number too.
- **No wrapped `mstone-row`.** More than 4 milestones is `vtimeline`, not a card grid on two rows.
- **No wrapped `envchain`, and no vertical `envchain`.** More than 4 environments is a `vtimeline` with `envc` entries.
- **No unreset Gantt bars on mobile.** At ≤700px reset bars to `position:static` left-anchored fills with per-bar width overrides scaled to the longest phase (`!important`), or they collapse to slivers.
- **No spaced or centered Gantt axis labels at the edges.** Write ticks with no space (`60d`), keep `white-space:nowrap`, and align first/last ticks to the axis edges (`transform:none` and `translateX(-100%)`).

---

## Section component toolkit

| Content type | Component |
|---|---|
| 4 top-line points / exec summary | 2×2 `card` grid with badges |
| Estimate with uncertainty range | `pert-cols` + `pert-bar-track` |
| Effort / hours distribution | `bchart` (sorted, with hr/item column) |
| Item proportions | `stack` proportional bar |
| Scenario / "what-if" comparison | `scn-wrap` |
| Complexity tiers | `tier-wrap` 3-column tier cards |
| Sequential process / method pipeline | `flow`, never `principles` |
| Phased plan, a few phases on a continuous axis | `gantt`, never flush `tline` bars |
| Grouped, searchable schedule of many work items | `sgantt` + toolbar, rendered from DATA |
| Effort distribution across phases | `tline-bars` (flex:N) + `tline-detail` grid |
| Categorical list with role/type/focus | `stack-table` with badge columns, never `bchart` |
| 2 to 4 standalone key numbers | `stat-row`, never `bchart` |
| Problem statement | `callout` (red/amber) |
| Comparison of options | `cmp-table` with ✓ / ✗ / ~ (recommended column gets `.hl`) |
| Chosen stack / layered approach | `stack-table` |
| Role-based outcomes | `outcome-grid` with ↓/↑ |
| Concerns / FAQs | `concerns` accordion (interactive) |
| Key metrics | `stat-row` with large numbers |
| Parallel / unordered principles | `principles` grid |
| Summary / recommendation | `dark-panel` (Aperia Blue + single graphic element) |
| The ask | `cta-box` (Aperia Blue + single graphic element) |
| Inline notes | `callout` (blue=neutral, green=positive, amber=warning, red=critical) |
| A labelled warning or provenance note | `callout tagged` (add `.soft` for neutral) |
| A report with two or more self-contained parts | `part-head` pill number + `sub-h` uppercase sub-headings |
| Up to 4 dated milestones | `mstone-row` (data-driven) |
| More than 4 dated milestones | `vtimeline` (data-driven, same array) |
| DEV to PROD promotion path, up to 4 | `envchain` |
| DEV to PROD promotion path, 5 or more | `vtimeline` (data-driven, same array) |
| Assumptions, risks and dependencies | `ard` (data-driven) |

---

## Delivery-plan components (data-driven)

Use these when the report is a delivery, release or roadmap plan. Markup and the
full render script are in `references/interactive.html`; styles are already in
`references/styles.css`.

### The DATA-object pattern

These are the script conventions for the whole skill. Follow them exactly; a report
that invents its own naming is wrong even if it renders.

**1. The markup is never hand-written.** You write one `DATA` object and the script
renders the milestones, the environment chain, the grouped Gantt, the count line and
the A/R/D block from it. The search index, the status counts and the tooltip all read
that same object, so a hand-written row is invisible to search, missing from the
counts and silent on hover. In the source HTML all five are empty mount points and
nothing else.

**2. `DATA` lives at the top of the last `<script>` in the file**, immediately above
the render script pasted from `references/interactive.html`. One `DATA` object per
report, never one per section, and never inside the render script itself. It is the
only part of that script you edit.

```js
const DATA = { <key>: { unit, sortByCompletion, editable, milestoneForm, milestones,
                        envForm, environments, cols, ends, rows, ard } };
```

**3. One key per plan, and the key is the id suffix.** A report with two parts uses
two keys and one copy of the render script. Every mount point for a plan is its
prefix plus that key, with no other id naming used anywhere:

| Id | Element | Filled by |
|---|---|---|
| `m-<key>` | `div.mstone-row` | `renderMilestones()` |
| `f-<key>` | `input[type=search]` in the toolbar | read by `applyView()` |
| `fc-<key>` | `span.sg-fcount` | `applyView()` |
| `ct-<key>` | `div.sg-counts` | `renderGantt()` |
| `g-<key>` | `div` inside `div.sgantt` | `renderGantt()` |
| `env-<key>` | `div.envchain` or `div.vtimeline` | `renderEnvs()` |
| `ard-<key>` | `div.ard` | `renderARD()` |

Expand and collapse buttons carry the key in `data-expand` / `data-collapse` rather
than an id. Edit-mode controls use `data-edit`, `data-addopen`, `data-addcancel`,
`data-undo`, `data-export` and `data-addform`, each set to the key; the add form's
fields are `nf-<key>-name`, `-group`, `-desc`, `-from`, `-to`, `-status`, `-tags`,
with `groups-<key>` for the datalist and `err-<key>` for the error line.

**4. `milestoneForm` picks the milestone rendering.** `"cards"` (the default) gives
`.mstone-row`, `"timeline"` gives `.vtimeline`. The mount point is `m-<key>` for
both, and the script sets the container class from this key, so the DATA always
wins over whatever class the markup carries. The entries themselves do not change.

**5. `envForm` picks the environment rendering**, exactly as `milestoneForm` does:
`"cards"` gives `.envchain`, `"timeline"` gives a `.vtimeline` of `envc` entries.
The mount is `env-<key>` for both.

**6. Every `vtimeline` entry is four fields, whatever it describes.** The renderer
places them identically, so a new content type adapts by filling the same fields
and needs no new CSS. This is the only place the entry shape is defined.

| Field | Required | Holds |
|---|---|---|
| `lead` | yes | The prominent top slot: a date for milestones, an environment name for the chain. Never a bare ordinal, since the rail already shows order |
| `chip` | no | A small chip inline beside the lead: the milestone flag, the environment badge |
| `title` | no | A second line. Milestones use it; environments omit it |
| `note` | no | The body line |
| `cls` | no | Marker state and variant: `done` `next` `goal` `risk`, plus `est`, or `envc e-qa` |

An entry may declare those names directly. The built-in mappers translate the
friendlier `milestones` and `environments` shapes onto them, so existing DATA keeps
working: a milestone's `d` fills `lead`, its `flag` fills `chip`; an environment's
`name` fills `lead`, its `badge` fills `chip`.

**7. Two rules the shape does not enforce:**

- `cols[].s` and `cols[].e` are ISO dates and are **required**. The tooltip computes
  start, end and elapsed weeks from them.
- `rows[].st` must be exactly `Done`, `In progress`, `Planned` or `At risk`. The
  count line and the tooltip chip match on the string.

The field-by-field contract for every key is documented in the header comment of
`references/interactive.html`. Read it there rather than guessing.

### What each component is for

| Component | Use it for | Notes |
|---|---|---|
| `mstone-row` | Up to 4 dated checkpoints | Status on the top border: `done` `next` `goal` `risk`, plus `est` for a dashed (estimated) date, or `envc e-qa` for an environment-coloured card |
| `vtimeline` | More than 4 dated checkpoints | Same array, same `cls` vocabulary, rendered as a rail. Only the marker carries colour, in three decodable states that need no legend: blue ahead, amber for risk or an estimated date, green for done and for the final live milestone. `est` also hollows the marker and dashes the connector. The date stays neutral heading ink throughout |
| `sgantt` | A grouped schedule over named columns | Sprint columns plus shaded release-stage columns (`phase:true`). Adjacent lit cells merge into one bar. The full grid shows; the column header sticks under the nav as the page scrolls |
| `sg-bar` toolbar | Search, expand/collapse all, match count | Search covers name, description, group and tags. Zero matches shows an empty state, not a blank grid |
| `sg-tip` tooltip | Start, end, elapsed weeks, span, tags | Flips at the viewport edge; hidden below 700px |
| Edit mode | Add a row, delete with one-level undo, tag, export JSON | Opt in per plan with `editable:true`. State is in-memory for the tab; say so in the UI |
| `envchain` | Promotion path, up to 4 environments | Rendered from `environments`, one card per entry with arrows between |
| `vtimeline` (envc) | Promotion path, 5 or more | The same rail as the milestones, with `envc e-*` entries. The environment name leads, the Synthetic or Production badge is the inline chip. No second vertical chain exists |
| `ard` | Assumptions / Risks / Dependencies | Three columns, owner and severity as metadata |

### The `sgantt` header sticks to the page

`.sgantt` has **no height cap and no scrollport of its own by default**. The full
grid always shows and the page is the vertical scroller. `.sg-head` is
`position:sticky; top:56px`, so the column header pins just under the sticky nav
as the reader scrolls the page.

That only holds while no overflow ancestor sits between the header and the page,
because `position:sticky` resolves against the nearest scrollport. So the
horizontal scrollbox is **conditional**: after each render, and on resize,
`syncScrollbox()` measures the grid against its container and adds `.scrolls`
(which applies `overflow-x:auto`) only when it genuinely overflows. On a wide
`.wrap.full` desktop the grid fits, the class stays off, and the header sticks. On
a narrow viewport the class goes on, the box scrolls sideways so the page never
does, and the header stops sticking: `.sgantt.scrolls .sg-head` resets to
`position:static`, because inside that scrollport `top:56px` would otherwise
read as a dead band above the header. That is the accepted tradeoff, and it is the
same one mobile already made.

Three details, all handled in `references/styles.css`:

- Default overflow is `clip`, not `hidden` or `auto`. It still rounds the flush
  header and band backgrounds at the corners, but does **not** create a scrollport,
  which the other two would.
- The header carries an opaque `background` and a `z-index` above the bars, which
  sit in `position:relative` cells. It stays below the nav's z-index, so it slides
  under the nav rather than over it.
- Print unpins the header and drops `.scrolls`, so the full grid prints.
- **The group bands do not stick.** Pinning them needs a second sticky layer offset
  by the header's height, which is not fixed once a column label wraps to two
  lines. Collapse-all and search handle long lists instead.

**Coupling warning:** `top:56px` on `.sg-head` must match the nav height, and the
conditional `.scrolls` class must keep its measurement. Give `.sgantt` an
unconditional `overflow` or a `max-height` and the header silently stops sticking,
because the box becomes the scrollport again.

### Choosing between `gantt` and `sgantt`

**This is the only place that decision is made.** Every table and rule elsewhere in
this file defers here. Both are schedules over time, so "it is a timeline" does not
settle it. Answer these instead:

| Question | `gantt` | `sgantt` |
|---|---|---|
| How many rows? | Up to about 8 | More than about 8 |
| Does the reader need to group, collapse or search them? | No | Yes |
| What is the horizontal axis? | Continuous time, bars positioned by percentage | A fixed set of named columns: sprints, then release stages |
| Does one row span several units? | Rarely, one bar per row | Often, and adjacent cells merge into one bar |
| Where does the markup come from? | Hand-written | Rendered from the DATA object |

A phased delivery roadmap with four workstreams is `gantt`. A sprint plan with
thirty features grouped by capability is `sgantt`.

Do not put both in one report. Pick the one the content is.

### Milestones: cards or timeline

**This is the only place that decision is made.** Both forms render the same
`milestones` array with the same `cls` vocabulary, so the choice is about how many
entries there are and nothing else.

| Entries | Form | `milestoneForm` |
|---|---|---|
| 4 or fewer | `mstone-row`, one horizontal row of cards | `"cards"` (the default) |
| More than 4 | `vtimeline`, a vertical rail | `"timeline"` |

The cut is at 4 because `.mstone-row` is an auto-fit grid with a 190px minimum
inside the 920px `.wrap`, so a fifth card wraps. A wrapped card grid is the defect
this rule exists to prevent: the second row is ragged, and a 7 or 9 entry set leaves
one orphan card sitting alone under six. **Never let `mstone-row` wrap to a second
row.** If the set grows past 4, change `milestoneForm`, do not widen the container.

Milestones stay in the 920px `.wrap` in both forms. Only the timeline block breaks
out to `.wrap.full`, per "Container width".

### Environment chain: cards or timeline

Same shape of rule as the milestones, and the same two forms.

| Environments | Form | `envForm` |
|---|---|---|
| 4 or fewer | `.envchain`, one row of cards with arrows | `"cards"` (the default) |
| More than 4 | `.vtimeline` with `envc e-*` entries | `"timeline"` |

`.envcard` has a 150px minimum, so five cards wrap in `.wrap` and the last one
stretches across a row by itself, reading as a banner rather than the end of a
chain. **There is no vertical variant of `.envchain`.** Past 4, the chain renders
as the same `vtimeline` the milestones use: step number in the neutral date slot,
the environment name in the prominent lead slot, the Synthetic or Production badge
as the inline chip, and the note plus client line as the body. There is no step
number: the rail already shows order. The environment colour shows on that
flag chip only. Markers stay on the three-state scale, so the whole chain reads
blue until the final live environment, which is green. One vertical component,
not two.

Both forms render from `DATA[key].environments` into the `env-<key>` mount.

### Edit mode honesty

Edit mode changes nothing outside the browser tab. Say that in the edit note, and
keep Export reachable whenever editing is on. Do not imply changes are saved.

---

## Building the HTML

Produce a single self-contained file with, in order:

1. Google Fonts link (Inter only). Labels use the `--label` token, which maps to Inter: no mono typeface is sanctioned by the brand
2. The full `<style>` block, in this order: **the `:root` block from
   `../../brand/tokens.css` first, then `references/styles.css` pasted verbatim**.
   Order matters. The two blocks name some values differently (`--sapphire-blue`
   in the brand layer, `--sapphire` in the theme) and redefine a few identically
   (`--radius`, the `--text-*` steps). Putting the theme second means it wins on
   any shared name, which is what the components are written against, while the
   brand block still supplies what the theme does not define: `--min-size`,
   `--font-sans`, the `--fw-*` weights, `--grad-hero` and `--series-1` to
   `--series-7`. Paste only the `:root` block, not the base element rules that
   follow it in `tokens.css`
3. Sticky `nav`, exactly `56px` tall: inlined logo (left, Aperia Blue), desktop scroll-link strip (right), hamburger button (mobile)
4. Mobile `nav-drawer` immediately after `</nav>`, set `position:fixed; top:56px`, hidden by default
5. Gradient `hero`: eyebrow, title, subtitle, optional meta row, and the inlined `pattern-double` top-right. The hero `<em>` subtitle inside `<h1>` must **omit the em dash** and be in Title Case. Its size comes from the theme's `.hero h1 em` rule, not an inline style
6. Content sections, each opening with a `sec-label` eyebrow naming the section, never numbered, then the `h2`
7. A `dark-panel` and/or `cta-box` for the recommendation and the ask, each with `pattern-single` top-right
8. Footer on Aperia Blue with the white logo + `Report Title · Subtitle · Month Year`
9. At the end of `<body>`, only the scripts the report actually needs: the
   accordion script **if** it carries a `concerns` accordion, the mobile nav
   drawer script **if** it carries the drawer (it always should), and for a
   delivery plan one final `<script>` holding your `DATA` object followed by the
   render script pasted from `references/interactive.html`. Do not ship a script
   for a component the report does not use

A skip link (`<a href="#main" class="skip-link">`) is the first element inside
`<body>`, and the content wrapper carries `id="main"`.

### Container width

Every section sits in `.wrap`, which caps content at 920px. That is the default,
and it is right for prose, cards, stat rows, charts and ordinary tables. This is
the only place the width decision is made.

The breakout is per component, never per section. A section keeps its heading,
eyebrow, intro, milestones and every other block inside `.wrap`; only the wide
component moves into a sibling `<div class="wrap full">` (full viewport width,
same side padding) inside the same section, together with the chrome that
belongs to it (its `sub-h`, toolbar, legend, counts and caption for an
`sgantt`). Close the default `.wrap`, open `.wrap full` for the wide block,
then reopen `.wrap` for what follows.

A component earns the breakout only when its intrinsic minimum width does not
fit the 848px of usable space inside `.wrap`, and that width comes from named
columns that cannot be dropped. Decide by arithmetic, not by feel:

- `sgantt`: minimum width is `--sg-labelw` (256) + `--sg-endw` (92) + `--sg-colw`
  (104) per data column. That is `348 + 104n`, and `.wrap` leaves 848px usable, so
  **5 or more columns needs `wrap full`**; 4 or fewer fits the default.
- A comparison table wide enough to overflow 848px, or any component that would
  otherwise scroll horizontally inside its own box on a desktop screen.

Never widen anything because it merely looks like it could use the room, and
never put prose or a section heading in `wrap full`. At any width the wide
component owns its own horizontal overflow; the page body never scrolls
horizontally.

### Mobile nav rules

- Desktop (>700px): horizontal scroll-link strip, hamburger hidden.
- Mobile (≤700px): link strip `display:none`, hamburger `display:flex`.
- The drawer is a full-width dropdown below the nav bar with tap-friendly padding.
- The burger animates to × via a `.open` class; tapping any drawer link closes it.

### Type sizes come from the scale

Sizes are the `--text-*` tokens in the pasted `:root`, taken from the Aperia Figma
design system, ten steps: `xs` 12/16, `sm` 14/20, `base` 16/24, `md` 18/28,
`lg` 20/32, `xl` 24/36, `2xl` 28/40, `3xl` 32/48, `4xl` 36/52, `5xl` 40/56.
Use each with its paired `--leading-*`.

Three rules, all of them hard:

- **Only tokens.** Never a raw px `font-size`, and never a new step. The ramp is
  sanctioned in `../../brand/BRAND.md`, so a new size is a change to that document.
- **No tag-tied sizes.** A bare `h1`..`h6` rule sets weight, tracking and spacing,
  never `font-size`. Size comes from the use site: a `.text-*` utility on the
  element, or a component rule that references a token. Write
  `<h2 class="text-2xl">`, not a global `h2 { font-size: ... }`.
- **Nothing below `xs`.** Figma also holds 10/12 and 11/16; both are below the
  12px floor and are print and Figma only.

If a role feels between two steps, take the nearer one and build the difference
from weight, letter-spacing, case or color. The two display steps are responsive
by `clamp()` built from step pairs, with the Figma mobile variants as the floors:
`2xl` runs `clamp(lg, 3vw, 2xl)` and `5xl` runs `clamp(2xl, 4.4vw, 5xl)`, each named
for its ceiling. Both ends are ramp steps, so a clamp never lands off-scale.

### Required structure rules

- Every section opens with a `sec-label` eyebrow, plain text with no numbering;
  nav links match every section `id`.
- **No divider lines anywhere.** No `::after` hairline on the eyebrow, no rule
  above a `part-head`, and no border between sections. Sections separate by
  whitespace alone, on screen and in print.
- Logical flow, default: Summary → Problem/Context → Options/Evidence → Decision
  → Plan → Ask. The middle two stages exist to weigh options, so include them only
  when there are options to weigh. A report that documents a decision already made
  has nothing to put there.
- Logical flow, delivery plan: Summary → the plans, one section each → Recommendation
  → Ask. Use this whenever the content is a schedule rather than a proposal.
- No empty cards or lorem. Write real content from what the user gave you.
- The recommended option in a comparison table gets `.hl`.
- Badge/callout colors signal sentiment (red=problem, amber=caution, blue=direction, green=positive).
- All `h2` and `h3` headings in Title Case.
- Accordion body (`.c-body`) background is `#FFFFFF`, not `var(--light-gray)`.
- Give every inlined `<linearGradient>` and `clipPath` a **unique `id`**.

### Fixed design decisions, do not override

These were set deliberately by the brand owner. The theme already encodes them;
never re-introduce the old value with an inline style or a local rule.

- The `.sgantt` box has **no padding**: the header row and group bands sit flush
  with the box edges, and the edge inset lives on the first and last cells.
- Timeline bars (`.sg-blk`) are **14px** tall.
- **No colored border accents on cards or panels**, per `BRAND.md`. Cards keep
  the neutral hairline. Status rides the three-state marker (blue ahead, amber
  for risk or an estimate, green for done or live), identity rides the chip and
  the heading colour. Never re-introduce a colored top or left edge on
  `mstone`, `ard-col`, `envcard` or `tier-card`.
- Shape comes from tokens too: `--radius` for cards and panels,
  `--radius-pill` for badges, tags, chips and round buttons. Never a literal
  `border-radius:100px`.
- An eyebrow or label above a heading stays visually subordinate to it: the
  heading takes the larger step (`.ard-col h3` sits at `base` over an `xs` tag
  with .05em tracking). If a label reads as big as its heading, fix the
  hierarchy, not the label copy.

### Responsive breakpoint (≤700px), mandatory per component

Every component in the table below collapses to a single column at ≤700px, **with one
exception**: `.sgantt`. A grouped Gantt is a fixed set of named columns, and collapsing
them destroys the thing the component exists to show, so it keeps every column and
scrolls horizontally inside its own box. The page itself still never scrolls
horizontally, because the overflow is on `.sgantt`, not on `body`. Only
`--sg-labelw` narrows (256px to 180px), and `--sg-endw` with it. Do not add a
one-column override for it, and do not reset its bars the way `.gantt` requires.

| Component | Mobile behaviour |
|---|---|
| `.g2`, `.principles`, `.dp-cols`, `.tier-wrap`, `.tline-detail`, `.gantt-detail` | `grid-template-columns:1fr` |
| `.pert-cols` | `1fr`; center column loses `transform:scale` |
| `.bchart` rows | name col `flex:0 0 120px`; `beff` col hidden |
| `.scn-wrap` rows | `scn-bar-wrap` hidden; name takes remaining space |
| `.tline-bars` | `flex-direction:column`; each bar `width:100%` |
| `.gantt` | axis hidden; label stacks above track; bars reset to static left-anchored fills with per-bar width overrides (`!important`) |
| `.flow` | stacks naturally, no override |
| `.nav-links` | `display:none` |
| `.nav-burger` | `display:flex` |
| `.nav-drawer` | visible when `.open` |
| `.cta-box` | padding `28px 20px` |
| `.ard` | `grid-template-columns:1fr` |
| `.mstone-row` | two columns |
| `.envchain` | stacks; `.env-arrow` hidden |
| `.vtimeline` | no override: it is single-column by construction |
| `.callout.tagged` | `flex-direction:column` |
| `.sgantt` | **Exception, see above.** Keeps every column; only `--sg-labelw` and `--sg-endw` narrow. The measured `.scrolls` class turns on here, so the box scrolls sideways and the header stops sticking |
| `.sg-tip` | `display:none` (no hover on touch) |

### Printing

The theme prints without help, but three of its choices are worth knowing.

- **Dark surfaces print.** The hero, dark panel, CTA box and footer set
  `print-color-adjust:exact` and repaint as a solid Aperia Blue rather than a
  gradient, since engines drop gradients far more readily than flat fills. Fill
  and white type are set together, so neither can be lost without the other.
- **Wide blocks get a landscape page.** `@page wide` plus `.wrap.full { page:wide }`
  turns only the full-width blocks landscape and leaves the rest portrait. Browsers
  that ignore named pages fall back to portrait, where the print stylesheet's
  tightened `--sg-*` geometry still fits the grid. Do not reach for
  `transform:scale`: it shrinks the painted box but not the page it paginates into,
  so a scaled grid still breaks and clips.
- **Every row prints.** A `beforeprint` handler clears each plan's search box and
  expands its collapsed groups, and `afterprint` restores both, so a printed plan
  never silently omits filtered or collapsed rows while the reader's on-screen state
  survives.

Pagination is granular rather than per section: cards, milestones, timeline entries,
A/R/D columns, callouts, table rows and Gantt rows avoid breaking inside, and
headings avoid breaking after so none is stranded at a page foot.

### Reference files

- **`references/styles.css`**: the complete Aperia report theme. Paste inside `<style>`.
- **`references/snippets.html`**: ready-to-paste markup for skip link, nav, drawer, hero, every static component, part headers, tagged callout, dark-panel, cta-box, footer, and both scripts.
- **`references/interactive.html`**: the delivery-plan components. Mount-point markup for milestones, the environment chain, the Gantt and the A/R/D block, the toolbar and edit form, and the documented render script with the DATA-object contract.
- **`../../brand/assets/*.svg`**: raw path data for the logo and both patterns.

---

## Checklist before delivering

Run **both** this list and the Application Checklist in `../../brand/BRAND.md`.

### Always applies

- [ ] `BRAND.md` and `tokens.css` were read before writing, with no palette values from memory
- [ ] The `<style>` block is the `tokens.css` `:root` first, then `styles.css` verbatim
- [ ] Inter loaded with weight 600 included; Arial fallback declared; body Light/Regular, never Bold
- [ ] Every size is a `--text-*` token; no raw px, no new step, nothing below `--text-xs`, and no bare `h1`..`h6` rule setting `font-size`
- [ ] Shape from `--radius` and `--radius-pill`; no literal `border-radius:100px`
- [ ] Only palette colors: core blues and neutrals, nothing else
- [ ] Logo inlined in nav (Aperia Blue) and footer (`#FFFFFF`), undistorted, ≥24px
- [ ] Nav strip scrolls horizontally (`flex-wrap:nowrap; overflow-x:auto; min-width:0`); hamburger wired
- [ ] Mobile drawer present, closes on link tap, burger animates to ×
- [ ] Graphic element top-right, full container height, no `max-width` cap, no distortion/flip/rotation, behind content
- [ ] Text sits left wherever the element sits right
- [ ] Hero `<em>` subtitle: no em dash, Title Case, no inline `font-size`
- [ ] All `h2`/`h3` in Title Case; nothing underlined; nothing justified
- [ ] Unique gradient/clip ids across all inlined SVGs
- [ ] Every section opens with an unnumbered `sec-label` eyebrow; no divider line anywhere; all nav links resolve
- [ ] Section order follows the default flow, or the delivery-plan flow when the content is a schedule
- [ ] Footer reads `Title · Subtitle · Month Year`
- [ ] Skip link present, `focus-visible` outline intact, reduced-motion block kept
- [ ] Only the scripts the report uses are shipped
- [ ] Printed to PDF and checked: dark surfaces keep their fill and white type,
      any `sgantt` fits the page width whole, no heading stranded at a page
      foot, no card or row split across pages, footer prints cleanly
- [ ] File is self-contained, with Google Fonts as the only external dependency

### Per component, only if the report carries it

- [ ] `concerns` accordion: `.c-body` background `#FFFFFF`, accordion script shipped
- [ ] `bchart`: rows use the flex model, not fixed-px grids; `.bval` holds a number only
- [ ] `tline-bars`: proportional `flex:N` widths, never equal-width boxes
- [ ] `scn-wrap`: bars use `display:flex; overflow:hidden`, no z-index stacking
- [ ] `gantt`: no absolute-positioned labels in the track; bars reset at ≤700px
- [ ] Every visualization present collapses gracefully at ≤700px per the table above

### Per component, delivery plans

- [ ] Every plan is rendered from `DATA`, with no hand-written `sgantt` rows
- [ ] Every `cols` entry has ISO `s` and `e`; every row `st` is one of the four exact strings
- [ ] Mount-point ids match their DATA key (`m-`, `f-`, `fc-`, `ct-`, `g-`, `env-`, `ard-`)
- [ ] Status ramp and environment colors come from the `--st-*` / `--env-*` tokens, never new hexes
- [ ] Search finds a row by its tag, and zero matches shows the empty state
- [ ] Edit mode, if on, says changes live in the tab only and keeps Export reachable
- [ ] Only one of `gantt` and `sgantt` appears in the report
- [ ] `sgantt` has no `max-height` and no unconditional `overflow`; `.scrolls` is applied by measurement only, and `.sg-head` `top` matches the nav height
- [ ] Milestone sets of more than 4 use `vtimeline`; no `mstone-row` wraps to a second row
- [ ] Environment chains of more than 4 render as a `vtimeline`, not a wrapped or vertical `envchain`
- [ ] The `wrap full` threshold was recomputed against the current `--sg-colw`,
      not assumed: an `sgantt` needs `wrap full` when
      `--sg-labelw + --sg-endw + (--sg-colw × columns) > 848`. At today's
      256 + 92 + 104 that is `348 + 104n > 848`, so 5 or more columns. Change the
      token and redo the sum.
