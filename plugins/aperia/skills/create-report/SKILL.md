---
name: create-report
description: Build an on-brand Aperia report, briefing, review, or proposal as one self-contained HTML file with navigation, charts, tables, and roadmap timelines. Use for any long-form document the reader scrolls through.
metadata:
  version: "0.9.1"
---

# Aperia Report

One self-contained HTML report in the Aperia identity. Cards, badges, callouts, tables, charts and timelines come from the shared `../apply-branding/components/` layer. This skill adds only the page chrome (nav, hero, footer), the phased roadmap and the data-driven delivery-plan subsystem (sgantt). Before inventing markup for anything else, check `COMPONENTS.md`; it is almost certainly there.

## What to read

**Where the shared layer is.** `brand/` and `components/` live in the sibling skill `apply-branding`. Every path below writes that folder as `../apply-branding/`, its name in Claude Code; on Claude Desktop the same folder is `../aperia:apply-branding/`. Run `ls ..` from this skill folder once and use the name you find. The scripts resolve it on their own.

**Always.** `../apply-branding/brand/BRAND.md` in full. `../apply-branding/components/COMPONENTS.md` in full: the toolkits, the chart rules, the timeline entry contract; this file does not repeat them. `references/snippets.html`: this skill's own markup (the style marker, nav, hero, footer, phases, delivery-plan mount points).

**Only if picked.** The one snippet file the **File** column in `COMPONENTS.md` names for each component you chose, under `../apply-branding/components/base/` or `../apply-branding/components/charts/`. `../apply-branding/components/icons/index.html` only if the report needs an inline icon; generate icons with `../apply-branding/components/icons/icon.py`. `references/interactive.html` only if the report carries a plan rendered from `DATA` (`gantt`, `sgantt`, milestones, environments); it holds the script-driven components and the DATA-object contract. A readout or summary with no plan does not need it.

**Never.** Any stylesheet. The report carries one marker, `<style>/* @aperia report */</style>`, with the word `charts` and/or `icons` added when those toolkits are used, and `../apply-branding/components/assemble.py` fills it with `../apply-branding/brand/tokens.css`, `../apply-branding/components/base/styles.css`, the optional toolkits and this skill's `references/styles.css`, in that order. Skim a stylesheet only when a class's behaviour is unclear.

A value not in `BRAND.md` or `tokens.css` is not an Aperia value. Brand assets are at `../apply-branding/brand/assets/`; inline the SVGs.

---

## Workflow

1. **Read the user's content.** Title, subtitle, audience, sections, and the one message the reader should walk away with.
2. **Map each section to a component** from `COMPONENTS.md`'s tables, or to `phases` / sgantt below when the content is phased work or a grouped schedule.
3. **Build one self-contained HTML file**: Google Fonts link, the style marker, skip link, nav, hero, sections, dark panel or CTA, footer, scripts. Then run `python3 ../apply-branding/components/assemble.py <file>` from this skill folder. Re-run it after any later edit. Report-specific rules go in a second `<style>` after the marker.
4. **Brand assets**: one `#ap-logo` sprite, referenced by `<use>` in nav (Aperia Blue) and footer (white, both set by the stylesheet); `pattern-double` in the hero; `pattern-single` in dark panels and CTA boxes.
5. **QA**: `python3 <this skill dir>/scripts/qa.py <file>`, then the checklist at the end of this file.
6. **Save and deliver.** Tell the user the path and which checklist items were run. No browser in the session: do not search for one; say the narrow-viewport and print passes are still open rather than claiming the file prints.

Minimal content from the user: scaffold and flag what to replace. Never leave a section empty or with lorem.

## Report-only decisions

- **No pie charts in a report.** The library ships none. Proportions use `stack` or, for more categories, `treemap`; `donutchart` only when a circle is the form the reader expects, at most 5 slices.
- **`gantt` or `sgantt`**: see the table under Delivery-plan components. A phased roadmap with four workstreams is `gantt`; a sprint plan with thirty features grouped by capability is `sgantt`. Never both in one report.
- **`phases`**: sequential phases of work, each with a duration pill and a deliverables list. For the work itself, not dated checkpoints (`vtimeline` / `mstone-row`) and not a short conceptual pipeline (`flow`). Markup in `references/snippets.html`; node color cycles `pd-blue`, `pd-sapphire`, `pd-dark`, repeating.

---

## Delivery-plan components (data-driven)

For a delivery, release or roadmap plan. Markup and the render script are in `references/interactive.html`; the field-by-field DATA contract is in its header comment. Read it there.

- **The markup is never hand-written.** Write one `DATA` object; the script renders the milestones, the environment chain, the grouped Gantt, the count line and the A/R/D block. In the source HTML all five are empty mount points.
- **`DATA` sits at the top of the last `<script>`**, directly above the render script pasted from `references/interactive.html`. One `DATA` per report, one key per plan, one copy of the render script.
- **The key is the id suffix** of every mount point:

| Id | Element | Filled by |
|---|---|---|
| `m-<key>` | `div.mstone-row` | `renderMilestones()` |
| `f-<key>` | `input[type=search]` in the toolbar | read by `applyView()` |
| `fc-<key>` | `span.sg-fcount` | `applyView()` |
| `ct-<key>` | `div.sg-counts` | `renderGantt()` |
| `g-<key>` | `div` inside `div.sgantt` | `renderGantt()` |
| `env-<key>` | `div.envchain` or `div.vtimeline` | `renderEnvs()` |
| `ard-<key>` | `div.ard` | `renderARD()` |

  Buttons carry the key in `data-expand` / `data-collapse`; edit-mode controls in `data-edit`, `data-addopen`, `data-addcancel`, `data-undo`, `data-export`, `data-addform`; add-form fields are `nf-<key>-name`, `-group`, `-desc`, `-from`, `-to`, `-status`, `-tags`, with `groups-<key>` for the datalist and `err-<key>` for the error line.
- **`milestoneForm` and `envForm`** pick the rendering, `"cards"` (default) or `"timeline"`, on the same mount. 4 or fewer entries: cards (`.mstone-row`, `.envchain`). More than 4: timeline (`.vtimeline`, for environments with `envc e-*` entries). Never let cards wrap to a second row; change the form, not the container.
- **Entries use the shared entry contract** in `COMPONENTS.md` (`lead`/`chip`/`title`/`note`/`cls`). The built-in mappers also accept the friendlier `milestones` (`d`, `flag`) and `environments` (`name`, `badge`) shapes.
- **`cols[].s` and `cols[].e` are ISO dates, required.** `rows[].st` is exactly `Done`, `In progress`, `Planned` or `At risk`.
- **Edit mode** (`editable:true`) changes nothing outside the browser tab. Say so in the edit note and keep Export reachable.

| Question | `gantt` (shared) | `sgantt` (this skill) |
|---|---|---|
| How many rows? | Up to about 8 | More than about 8 |
| Group, collapse or search? | No | Yes |
| Horizontal axis | Continuous time, bars by percentage | Named columns: sprints, then release stages (`phase:true`) |
| One row spans several units? | Rarely | Often; adjacent cells merge into one bar |
| Markup | Hand-written | Rendered from `DATA` |

**sgantt width is decided by the script.** The plan block (`sub-h`, toolbar, legend, counts, grid, caption) sits in its own `.wrap` with nothing else inside, as `references/interactive.html` shows. `syncScrollbox()` adds `.full` to that `.wrap` when the grid's minimum width does not fit, and `.scrolls` to the box when it still does not. Do not add `wrap full` by hand, and never give `.sgantt` a `max-height` or an unconditional `overflow`; either one silently stops the header sticking.

---

## Building the HTML

In order:

1. Google Fonts link, Inter only. Labels use the `--label` token; no mono typeface.
2. The style marker, `<style>/* @aperia report charts icons */</style>`, with `charts` and `icons` present only when used.
3. The brand sprite from `references/snippets.html`, which defines `#ap-logo` once, then the sticky `nav`: logo by `<use>` left, scroll-link strip right, hamburger for mobile, with the `nav-drawer` right after `</nav>`.
4. Gradient `hero`: eyebrow, title, subtitle, optional meta row, inlined `pattern-double` top-right. The `<em>` subtitle inside `<h1>` is Title Case, no dash, no inline size.
5. Sections, each opening with a `sec-label` eyebrow naming the section, never numbered, then the `h2`.
6. A `dark-panel` and/or `cta-box` for the recommendation and the ask, each with `pattern-single` top-right.
7. Footer on Aperia Blue: white logo + `Report Title · Subtitle · Month Year`.
8. At the end of `<body>`, only the scripts the report uses: the nav-drawer script from `references/snippets.html` (always), the accordion script from `../apply-branding/components/base/emphasis.html` only with a `concerns` accordion, and for a delivery plan one final `<script>` holding `DATA` then the render script.

A skip link (`<a href="#main" class="skip-link">`) is the first element in `<body>`; the content wrapper carries `id="main"`.

### Structure

- Nav links match every section `id`.
- No divider lines anywhere: no hairline on the eyebrow, no rule above a `part-head`, no border between sections. Whitespace only.
- Section order, default: Summary, Problem/Context, Options/Evidence, Decision, Plan, Ask. The middle two only when there are options to weigh.
- Section order, delivery plan: Summary, one section per plan, Recommendation, Ask.
- `h2` and `h3` in Title Case.
- Sizes: a `.text-*` utility at the use site or a component rule that names a token. A bare `h1`..`h6` rule sets weight, tracking and spacing, never `font-size`.
- Unique `id` on every inlined `<linearGradient>` and `clipPath`.

### Container width

Every section sits in `.wrap`. Only a component that would overflow `.wrap` on a desktop screen moves into a sibling `<div class="wrap full">` inside the same section, with its own chrome and nothing else; close `.wrap`, open `.wrap full`, reopen `.wrap` after. The sgantt does this on its own. Never prose or a heading in `wrap full`; never widen because it looks like it could use the room. The page body never scrolls horizontally.

### Printing

The stylesheet handles the page setup, the solid dark surfaces and the sgantt expand-before-print. Never `transform:scale` a grid to fit a page.

---

## QA

```bash
python3 <this skill dir>/scripts/qa.py <slug>.html
```

Needs `beautifulsoup4`; if missing, the script prints the install command. Checks that the marker was assembled and names only the toolkits in use, the sprite, skip link, nav links and drawer, footer, section labels, palette, duplicate ids, placeholder text, dashes, classes no stylesheet defines, and the delivery-plan rules below. Errors must be fixed; warnings are judgement calls.

## Checklist before delivering

`COMPONENTS.md` rules apply to every component taken from it. This covers what only a report has and the script cannot see.

- [ ] `assemble.py` run after the last edit; the marker names `charts` and `icons` only if used; nothing edited inside the injected block
- [ ] Nav strip scrolls horizontally; hamburger and drawer wired; every nav link resolves
- [ ] Hero `<em>` subtitle: Title Case, no dash, no inline size
- [ ] Every section opens with an unnumbered `sec-label`; no divider line anywhere; section order follows the flow for the content type
- [ ] Footer reads `Title · Subtitle · Month Year`; skip link present
- [ ] Only the scripts the report uses are shipped
- [ ] No pie chart anywhere
- [ ] Delivery plan: every row rendered from `DATA`; ISO `s`/`e` on every column; every `st` one of the four strings; mount ids match the key; search finds a row by tag; edit mode, if on, says changes live in the tab
- [ ] Only one of `gantt` and `sgantt`; the sgantt block sits alone in its own `.wrap` with no hand-added `full`, no `max-height` and no unconditional `overflow`
- [ ] In a browser, when one is available: checked at a narrow viewport, the drawer works and only the sgantt box scrolls sideways
- [ ] In a browser, when one is available: printed to PDF and checked, dark surfaces keep their fill and white type, any `sgantt` fits the page whole, no heading stranded at a page foot, no card or row split across pages
- [ ] Self-contained, Google Fonts the only external dependency
