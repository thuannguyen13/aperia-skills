---
name: create-report
description: Generate professional, on-brand HTML strategic reports, briefings, reviews, and proposals in the Aperia brand identity. Use whenever the user wants an Aperia report, branded report, executive briefing, strategic review, client proposal, or any structured long-form document that should follow the Aperia brand guidelines, including phrasings like "Aperia report", "write this up as a briefing", "turn this into a proposal", or any request for a polished, shareable long-form document in the Aperia look and feel. For Aperia branding on anything that is not a report or a deck, use the apply-branding skill instead. Built on the shared apply-ui-components library, so every card, table, chart, badge, callout and timeline in a report matches what any other Aperia surface uses for the same job. Output is a single self-contained HTML file with sticky navigation, a gradient hero, sections, cards, data visualizations, comparison tables, phased roadmaps, accordions, and, for delivery and release plans, a searchable grouped Gantt with milestone cards, an environment chain and an Assumptions / Risks / Dependencies block.
---

# Aperia Report

Produces a single self-contained HTML strategic report in the Aperia brand
identity. A report is built in two layers: the **base component library**
(cards, badges, callouts, tables, charts, timelines — everything a report
shares with any other Aperia UI surface) lives once, in the sibling
**apply-ui-components** skill, and is not duplicated here. This skill adds
only what a full report needs on top of it: the page chrome (nav, hero,
footer), the phased-roadmap timeline, and the data-driven delivery-plan
subsystem (sgantt). If you find yourself about to invent markup or CSS for a
card, a chart, or a timeline that isn't documented in this file, it almost
certainly belongs in apply-ui-components already — check there before
improvising.

## Step 0: Read the brand layer first (required)

Before writing a single line of HTML:

1. Read **`../../brand/BRAND.md`** in full.
2. Read **`../../brand/tokens.css`** and paste its `:root` block into your `<style>`.
3. Read **apply-ui-components' `references/styles.css` and `references/snippets.html`** — the base component library every report is built from — and its `SKILL.md` for the full component toolkit, chart toolkit and the rules governing them (bar chart consistency, no invented percentages, pie/donut constraints, the timeline entry contract, etc.). This file does not repeat that guidance; apply-ui-components is the source of it.
4. If the report needs the extended chart family (line, area, combo, scatter, bubble, grouped/stacked bars, pie, donut, radial gauge, treemap, radar, funnel, sparkline, heatmap), also read apply-ui-components' **`references/charts.css`** and **`references/charts.html`**.
5. If the report needs an inline icon, also read apply-ui-components' **`references/icons.css`** and **`references/icons.html`**, including its licensing note.
6. Read **`references/styles.css`** (this skill — chrome, sgantt, the phased-roadmap timeline) and **`references/snippets.html`** (this skill's own markup: nav, hero, footer, phases, delivery-plan mount points).
7. If the report is a delivery, release or roadmap plan, also read **`references/interactive.html`** (the script-driven delivery-plan components and the DATA-object contract).

**Do not work from memory of the palette, the type rules, or the graphic-element rules.** They live in `BRAND.md` and only there. If a value you want is not in `BRAND.md` or `tokens.css`, it is not an Aperia value. Do not invent it.

Brand assets are at `../../brand/assets/`. Inline the SVGs, never link them.

---

## Workflow

1. **Read the user's content.** Identify the title, subtitle, audience, core sections, and the one message the reader should walk away with.
2. **Choose visualizations strategically.** See apply-ui-components' `SKILL.md` — "Chart toolkit" and "Chart rules" — for the canonical decision guide (numbers become range bars or bar charts, not stat cards alone; proportions become stacked bars or a capped pie/donut; a schedule becomes `gantt` or, for many grouped rows, `sgantt`, decided under "Choosing between `gantt` and `sgantt`" below).
3. **Map each section to a component** from apply-ui-components' component/chart/icon toolkits, or from this file's phases/sgantt additions when the content calls for those specifically.
4. **Build one self-contained HTML file**: Google Fonts link, the pasted theme (both layers), skip link, nav, hero, sections, dark panel / CTA, footer, scripts.
5. **Apply brand assets** per `BRAND.md`: logo in nav (Aperia Blue) and footer (recolored `#FFFFFF`); `pattern-double` in the hero; `pattern-single` in dark panels and CTA boxes.
6. **Run the checklist** at the bottom of this file, apply-ui-components' own checklist, *and* the Application Checklist in `BRAND.md`.
7. **Save and deliver** the file, then tell the user it opens in any browser, prints to PDF, and is shareable as-is.

If the user gives minimal content, scaffold intelligently and flag what to replace. Never leave a section empty or filled with lorem.

---

## Visualization thinking specific to reports

Component selection, chart-type selection, bar-chart consistency, and the
full anti-pattern list live in apply-ui-components' `SKILL.md` — read that
first. Two decisions exist only in the context of a full report, because
they involve components that only this skill has:

- **A schedule of a few phases on a continuous axis** is apply-ui-components' `gantt`. **A schedule of many work items over named sprints or stages, grouped and searchable** is `sgantt`, which exists only here — decided under "Choosing between `gantt` and `sgantt`" below, never from a generic chart-selection table.
- **A sequential, multi-week phase of work with a duration and a deliverables list** (not a dated checkpoint, not a chart) is the `phases` component below — distinct from apply-ui-components' `flow` (a short conceptual pipeline) and from its milestone timelines (dated checkpoints, not durations).

**No pie charts, full stop, in this skill** — a stricter rule than apply-ui-components' constrained ≤5-slice allowance. A report's proportions use `stack` or, for more categories, `treemap`. This is a deliberate report-specific choice, not an oversight; do not loosen it to match apply-ui-components without the user asking for that here specifically.

### The phased roadmap (`phases`)

A dot-and-line rail narrating **sequential phases of work**, each with a
duration pill and a bulleted deliverables list — see
`references/snippets.html` for the markup and `references/styles.css` for
`.phases`/`.p-item`/`.p-dot`/`.pd-*`/`.p-line`/`.p-duration`/`.delivs`/`.dlv`.
Use it when the content is the *work itself* (what happens in each phase and
what it produces), not dated checkpoints (that's `vtimeline`/`mstone-row`
from apply-ui-components) and not a short conceptual pipeline (that's
`flow`). Node color cycles `pd-blue` → `pd-sapphire` → `pd-dark`, repeating
for a 4th-plus phase.

---

## Delivery-plan components (data-driven)

Use these when the report is a delivery, release or roadmap plan. Markup and the
full render script are in `references/interactive.html`; styles are in this
skill's `references/styles.css` (sgantt) — the milestone cards, vertical
timeline, environment chain and A/R/D block it renders use the CSS classes
defined in apply-ui-components' `references/styles.css`, since a rendered
plan is a DATA-driven instance of those same components, not a different
visual design.

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
The cards-or-timeline threshold is the same one apply-ui-components documents under
"Choosing a timeline form" (4 or fewer → cards, more → timeline) — this is that same
decision, just DATA-driven instead of hand-authored.

**5. `envForm` picks the environment rendering**, exactly as `milestoneForm` does:
`"cards"` gives `.envchain`, `"timeline"` gives a `.vtimeline` of `envc` entries.
The mount is `env-<key>` for both. Same threshold, same source rule.

**6. Every `vtimeline` entry uses apply-ui-components' four-field entry contract**
(`lead`/`chip`/`title`/`note`/`cls` — see that skill's `SKILL.md`), whatever it
describes. The renderer places them identically, so a new content type adapts by
filling the same fields and needs no new CSS.

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
| `sgantt` | A grouped schedule over named columns | Sprint columns plus shaded release-stage columns (`phase:true`). Adjacent lit cells merge into one bar. The full grid shows; the column header sticks under the nav as the page scrolls. This component exists only in create-report — apply-ui-components' `gantt` covers the continuous-axis case only |
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

**This is the only place that decision is made.** Both are schedules over time, so
"it is a timeline" does not settle it. `gantt` is defined in apply-ui-components;
`sgantt` exists only here. Answer these instead:

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

### Milestones and environment chains: cards or timeline

**This is the only place that decision is made for a delivery plan.** It is the
same rule apply-ui-components documents under "Choosing a timeline form" for
hand-authored content — here it is DATA-driven via `milestoneForm`/`envForm`
instead of picked by which markup you paste.

| Content | Entries | `milestoneForm` / `envForm` |
|---|---|---|
| Milestones | 4 or fewer | `"cards"` (default) → `.mstone-row` |
| Milestones | More than 4 | `"timeline"` → `.vtimeline` |
| Environments | 4 or fewer | `"cards"` (default) → `.envchain` |
| Environments | More than 4 | `"timeline"` → `.vtimeline` with `envc e-*` entries |

The cut is at 4 for the same reason in both cases: `.mstone-row` is an auto-fit
grid with a 190px minimum and `.envcard` a 150px minimum, both inside the 920px
`.wrap`, so a 5th entry wraps to a ragged second row or a lone banner card.
**Never let either wrap.** If a set grows past 4, change the `Form` value, do not
widen the container — and there is no vertical variant of `.envchain` specifically;
past 4 it renders as the same `.vtimeline` the milestones use, environment colour
riding the chip only.

Both stay in the 920px `.wrap` in every form. Only the timeline block breaks out
to `.wrap.full`, per "Container width" below.

### Edit mode honesty

Edit mode changes nothing outside the browser tab. Say that in the edit note, and
keep Export reachable whenever editing is on. Do not imply changes are saved.

---

## Building the HTML

Produce a single self-contained file with, in order:

1. Google Fonts link (Inter only). Labels use the `--label` token, which maps to Inter: no mono typeface is sanctioned by the brand
2. The full `<style>` block, in this order: the `:root` block from
   `../../brand/tokens.css`, then **apply-ui-components' `references/styles.css`
   pasted verbatim**, then, only if used, its `references/charts.css` and/or
   `references/icons.css`, then **this skill's own `references/styles.css`
   pasted verbatim, last**. Order matters throughout: each later block wins on
   any name it shares with an earlier one, which is what every component is
   written against. This skill's file supplies only chrome, sgantt and
   `phases` — it does not redefine anything the base layer already owns
3. Sticky `nav`, exactly `56px` tall: inlined logo (left, Aperia Blue), desktop scroll-link strip (right), hamburger button (mobile)
4. Mobile `nav-drawer` immediately after `</nav>`, set `position:fixed; top:56px`, hidden by default
5. Gradient `hero`: eyebrow, title, subtitle, optional meta row, and the inlined `pattern-double` top-right. The hero `<em>` subtitle inside `<h1>` must **omit the em dash** and be in Title Case. Its size comes from the theme's `.hero h1 em` rule, not an inline style
6. Content sections, each opening with a `sec-label` eyebrow naming the section, never numbered, then the `h2`
7. A `dark-panel` and/or `cta-box` (both from apply-ui-components) for the recommendation and the ask, each with `pattern-single` top-right
8. Footer on Aperia Blue with the white logo + `Report Title · Subtitle · Month Year`
9. At the end of `<body>`, only the scripts the report actually needs: the
   accordion script from apply-ui-components' `snippets.html` **if** it carries
   a `concerns` accordion, the mobile nav drawer script from this skill's
   `snippets.html` **if** it carries the drawer (it always should — paste only
   one of these two, never both, since apply-ui-components' script does not
   include the drawer toggle and this skill's does not include the accordion
   toggle), and for a delivery plan one final `<script>` holding your `DATA`
   object followed by the render script pasted from `references/interactive.html`.
   Do not ship a script for a component the report does not use

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
- All `h2` and `h3` headings in Title Case.
- Give every inlined `<linearGradient>` and `clipPath` a **unique `id`**.

Component-level rules (badge/callout sentiment colors, comparison-table `.hl`,
accordion body background, and every other component convention) live in
apply-ui-components' `SKILL.md` and are not repeated here.

### Fixed design decisions specific to this skill

apply-ui-components' `SKILL.md` covers the shared fixed decisions (no colored
border accents, `--radius`/`--radius-pill` only, eyebrow-vs-heading hierarchy).
Two more apply only to the sgantt subsystem, which exists only here:

- The `.sgantt` box has **no padding**: the header row and group bands sit flush
  with the box edges, and the edge inset lives on the first and last cells.
- Timeline bars (`.sg-blk`) are **14px** tall.

### Responsive breakpoint (≤700px)

Every component apply-ui-components owns collapses per its own responsive
block (see that skill's `SKILL.md` and `references/styles.css`/`charts.css`).
This skill adds three of its own, plus the one documented exception:

| Component | Mobile behaviour |
|---|---|
| `.nav-links` | `display:none` |
| `.nav-burger` | `display:flex` |
| `.nav-drawer` | visible when `.open` |
| `.phases` | Stacks naturally, no override needed |
| `.sgantt` | **Exception.** A grouped Gantt is a fixed set of named columns; collapsing them destroys the thing it exists to show, so it keeps every column and scrolls horizontally inside its own box instead. The page itself still never scrolls horizontally — the overflow is on `.sgantt`, not `body`. Only `--sg-labelw` (256px → 180px) and `--sg-endw` narrow. Do not add a one-column override for it, and do not reset its bars the way `.gantt` requires |
| `.sg-tip` | `display:none` (no hover on touch) |

### Printing

apply-ui-components' print rules already cover every component it owns (dark
surfaces repaint solid, cards/callouts/rows avoid breaking inside). This skill
adds the page setup and its own chrome/sgantt specifics:

- **`@page` sizing**: A4 portrait by default, with a named `wide` landscape
  page for `.wrap.full` blocks (an `sgantt` at 5+ columns). Browsers that
  ignore named pages fall back to portrait, where the print stylesheet's
  tightened `--sg-*` geometry still fits. Do not reach for `transform:scale`:
  it shrinks the painted box but not the page it paginates into, so a scaled
  grid still breaks and clips.
- **Hero and footer print as solid Aperia Blue**, the same `print-color-adjust:exact`
  treatment apply-ui-components uses for `dark-panel`/`cta-box`, since gradients
  are the fragile part, not flat fills.
- **Every sgantt row prints.** A `beforeprint` handler (in `references/interactive.html`)
  clears each plan's search box and expands its collapsed groups; `afterprint`
  restores both, so a printed plan never silently omits filtered or collapsed
  rows while the reader's on-screen state survives.

### Reference files

- **apply-ui-components' `references/styles.css`, `snippets.html`, `charts.css`, `charts.html`, `icons.css`, `icons.html`**: the base component library. Read that skill's own reference-file notes for what each covers.
- **`references/styles.css`** (this skill): chrome, the `phases` timeline, and the sgantt subsystem. Paste inside `<style>`, after the base layer.
- **`references/snippets.html`** (this skill): skip link, nav, drawer, hero, `phases`, delivery-plan mount points, footer, and the nav-drawer script.
- **`references/interactive.html`**: the delivery-plan components. Mount-point markup for milestones, the environment chain, the Gantt and the A/R/D block, the toolbar and edit form, and the documented render script with the DATA-object contract.
- **`../../brand/assets/*.svg`**: raw path data for the logo and both patterns.

---

## Checklist before delivering

Run **all three**: this list, apply-ui-components' own checklist for every
component you used from it, and the Application Checklist in `../../brand/BRAND.md`.

### Chrome and page-level, always applies

- [ ] `BRAND.md` and `tokens.css` were read before writing, with no palette values from memory
- [ ] The `<style>` block order is `tokens.css` `:root`, then apply-ui-components' `styles.css` (and `charts.css`/`icons.css` if used), then this skill's own `styles.css`, last, all verbatim
- [ ] Inter loaded with weight 600 included; Arial fallback declared; body Light/Regular, never Bold
- [ ] Logo inlined in nav (Aperia Blue) and footer (`#FFFFFF`), undistorted, ≥24px
- [ ] Nav strip scrolls horizontally (`flex-wrap:nowrap; overflow-x:auto; min-width:0`); hamburger wired
- [ ] Mobile drawer present, closes on link tap, burger animates to ×
- [ ] Graphic element top-right, full container height, no `max-width` cap, no distortion/flip/rotation, behind content
- [ ] Hero `<em>` subtitle: no em dash, Title Case, no inline `font-size`
- [ ] Every section opens with an unnumbered `sec-label` eyebrow; no divider line anywhere; all nav links resolve
- [ ] Section order follows the default flow, or the delivery-plan flow when the content is a schedule
- [ ] Footer reads `Title · Subtitle · Month Year`
- [ ] Skip link present
- [ ] Only the scripts the report uses are shipped — the nav-drawer script and the accordion script are never both pasted from two different files
- [ ] Printed to PDF and checked: dark surfaces (hero, footer, and everything apply-ui-components owns) keep their fill and white type, any `sgantt` fits the page width whole, no heading stranded at a page foot, no card or row split across pages, footer prints cleanly
- [ ] File is self-contained, with Google Fonts as the only external dependency
- [ ] **No pie charts anywhere in the report** — stricter than apply-ui-components' constrained allowance; use `stack` or `treemap` instead

### Per component, only if the report carries it

- [ ] `phases`: durations and deliverables are real, not placeholder; node color cycles blue → sapphire → dark
- [ ] Every other component present collapses gracefully at ≤700px per apply-ui-components' own responsive rules

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
