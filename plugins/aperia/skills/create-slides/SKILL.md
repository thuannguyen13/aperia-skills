---
name: create-slides
description: Build an on-brand Aperia slide deck as one self-contained HTML file that runs in the browser and prints to a 16:9 PDF. Use for presentations, readouts, and pitch decks. It does not produce PowerPoint.
metadata:
  version: "0.9.1"
---

# Aperia Deck

A presentation as one self-contained HTML file. Arrow keys, space and swipe move between slides; `O` opens a thumbnail overview, `N` the presenter notes, `F` full screen; Ctrl/Cmd+P prints one slide per landscape page, a 16:9 PDF. No dependency beyond Google Fonts.

## What to read

**Where the shared layer is.** `brand/` and `components/` live in the sibling skill `apply-branding`. Every path below writes that folder as `../apply-branding/`, its name in Claude Code; on Claude Desktop the same folder is `../aperia:apply-branding/`. Run `ls ..` from this skill folder once and use the name you find. The scripts resolve it on their own.

**Always.** `../apply-branding/brand/BRAND.md` in full. `references/snippets.html`: the skeleton, the brand sprite, every layout and the deck script. Copy the layout markup and replace the copy, not the structure.

**Only if needed.** `references/charts.html` when a slide carries a stat row or a chart. `../apply-branding/components/COMPONENTS.md` when a component's meaning or a chart choice is in question. `../apply-branding/components/icons/index.html` only if a slide carries an icon.

**Never.** `references/slides.css`, beyond a skim for class names and the type tokens. `../apply-branding/brand/tokens.css`, not even to orient: `BRAND.md` names every token it defines. The deck carries one marker, `<style>/* @aperia slides */</style>`, and `../apply-branding/components/assemble.py` fills it with `tokens.css` and `slides.css`, in that order.

A value not in `BRAND.md` or `tokens.css` is not an Aperia value. `slides.css` implements the `COMPONENTS.md` design language in canvas units: the same badge and callout sentiments, status on text and chip color, the same series order. Where it is stricter (a donut capped at 3 segments), the stricter rule holds.

## Workflow

1. **Read the source**: a file the user points at, or pasted content. `markitdown` handles `.docx`/`.pdf`/`.pptx` if installed.
2. **Outline first**: slide sequence, layout and tone per slide. Show it and get a nod before generating, unless the user asked for the finished deck straight away.
3. **If the source contains a table, ask what to do with it**, once, listing every table found: keep the contents as a table, or convert to a chart or diagram. Never convert silently.
4. **Build** the single HTML file from the skeleton in `references/snippets.html`.
5. **Assemble**: `python3 ../apply-branding/components/assemble.py <file>` from this skill folder. Re-run after any later edit.
6. **QA**: `python3 <this skill dir>/scripts/qa.py <file>`, then open the file and look at every slide. No browser in the session: do not search for one; tell the user the visual pass and the print preview are still open.
7. **Save** as `<slug>.html` in the working directory unless the user names a location. Tell the user the path and the keys: arrows, `O`, `N`, `F`, Ctrl/Cmd+P.

Anything beyond the theme goes in a second `<style>` after the marker, never inside the injected one. This is rare.

---

## The canvas

Every slide is a fixed 1920 × 1080 box, scaled to fit the viewport on screen and a 16:9 page in print.

- Fixed canvas units only inside a slide. Every font size from the type tokens in `slides.css`. Never `vw`, `vh`, `clamp()` or `%` font sizes.
- No mobile breakpoint for slide content. Only the deck chrome adapts.
- Content that does not fit is two slides. Never shrink the type.

```html
<section class="stage">
  <article class="slide s-light s-text"> … </article>
</section>
```

## Light and dark

- Light slides carry text: a paragraph, four or more points, a table, a chart the reader studies.
- Dark slides carry emphasis: covers, agendas, section dividers, statements, quotes, one big number, closings. **These are always dark**; `qa.py` fails a light one.
- Rhythm: dark cover, dark agenda, dark divider, light content through the section, a dark statement at the turning point, dark close. Roughly a third dark.
- One dark tone class, `s-dark` (brand gradient). Add `flat` for solid Aperia Blue on in-body emphasis, big-number and donut slides. `flat` changes only the background.

## Layouts

| Slide layout | Classes |
|---|---|
| Always dark | `s-cover` `s-agenda` `s-section` `s-statement` `s-quote` `s-end` |
| Light, text | `s-text` `s-two-col` `s-icons` |
| Either tone | `s-numbers` `s-image-full` |

Full markup for each is in `references/snippets.html`; `s-numbers` and the charts are in `references/charts.html`. `s-text`, `s-two-col`, `s-icons`, `s-agenda` and `s-numbers` style nothing; `qa.py` keys on them, so keep applying them.

- **The closing slide carries the graphic element and a heading, nothing else.** The ask, the date and the contact are spoken from the notes. `qa.py` fails anything more.
- Components drop into any layout and are not slide classes: `.card`, `.iblock`, `.callout`, `.badge`, `.cmp-table`, `.flow`, `.stat-row`, the `.g2` `.g3` `.g4` grids, the charts. A comparison-table slide is `s-light s-text` holding a `.cmp-table`.
- Height helpers: `.fill` takes the leftover height and keeps the element's own display (on a `.g2`/`.g3`/`.g4` the rows center); `.fill-c` is the flex-column version for a bullet list or loose block.

### Sequences are diagrams, not bullets

Anything step-by-step, a flow, a journey, a process, a pipeline, is drawn:

- Ordered stages, no timeline: `.flow`, numbered nodes left to right, one short line each, three to five steps. More is two slides or a coarser grouping.
- Stages that occupy time: `.gantt`.
- Relative effort, not a schedule: `.tline-bars`.
- A cycle: `.flow`, with the heading saying so and the last step closing the loop.

Every stage title is a verb ("Ingest", "Score", "Triage"). A step that needs more than two words is drawn at the wrong altitude; group it.

---

## Brand on a slide

| Token | Role on a slide |
|---|---|
| Aperia Blue | Dark slide backgrounds, headings on light, chart series 1 |
| Dark Blue | Gradient partner, chart series 2 |
| Sapphire Blue | Kickers on light, bullet markers, the insight line, chart series 3 |
| Sky Blue | Kickers and stat values on dark, chart series 4 |
| Light Blue | Tints, the "rest of the total" band in charts |

Neutrals as usual, Dark Gray for muted copy. Green, amber and red only in callouts and badges, never a chart series. `qa.py` flags any hex outside the theme.

If, and only if, this deck will be shown beside one built on the official Aperia PowerPoint template, redefine `--sapphire-blue` as `#1570E0` and `--sky-blue` as `#25B4F1` in the deck's own `<style>` after the marker (both approved in `DEVIATIONS.md` section 6). Ask before doing this.

- Inter from Google Fonts, Arial fallback. Regular for body; Medium, SemiBold and Bold build hierarchy. Never underline.
- Left-align. Center only on cover and statement slides. Never justify.
- Title Case for every heading. ALL-CAPS only for kickers, chart notes and badges.
- Every size is a token from the Type scale block in `slides.css`: `--slide-text-*` for body on a slide face, `--slide-display-*` for headlines; `--slide-text-xs` is the slide-face floor. Deck chrome (`.ui-*`) uses the brand `--text-*` steps. Never a raw px size on a slide, never a screen-px `--text-*` on a slide face.
- Voice: fact-based, steady. Slide copy is shorter and flatter than report copy; a slide asserts, the presenter explains. No exclamation marks.

### Brand assets

The three SVGs are defined once in a sprite at the top of `<body>` (in `references/snippets.html`, paste as-is) and referenced with `<use>`:

| Symbol | Source | Where |
|---|---|---|
| `#ap-shape-double` | `pattern-double.svg` | Cover and closing slides |
| `#ap-shape-single` | `pattern-single-portrait.svg` | Sections, statements, dark in-body slides |
| `#ap-logo` | `aperia-logo.svg` | Cover (white) and every content slide footer |

The logo uses `fill="currentColor"`: Aperia Blue on light, white on dark, set by CSS. Never recolor it another way.

Graphic element on a slide, on top of the `BRAND.md` rules: `.shape-cover` (double) and `.shape-panel` (portrait single) run the full 1080px at `height:100%; width:auto`, top-right, no width cap. The double covers roughly the right two thirds, the single roughly the right 45%; never resize either to balance a slide, move the text. Keep headings and body within roughly the left two thirds.

### Icons

Lucide, fetched on demand. `python3 <this skill dir>/scripts/icon.py shield-check users` emits inline SVG; `--search shield` finds a slug. The script tries two hosts; where neither is reachable, set `APERIA_ICONS_DIR` to a folder of Lucide SVGs (the `icons/` folder of a `lucide-static` package) and it reads from there. Otherwise leave the icon out. `stroke="currentColor"`, colored by the theme; never hard-code a stroke. One icon per heading, one stroke weight throughout, never mixed with emoji or filled glyphs.

---

## Charts

CSS and SVG only, no chart library.

| The data | Component | Not this |
|---|---|---|
| A few categories compared on one scale, time-ordered | `.colchart` vertical columns | A table |
| Ranked quantities, one scale | `.bchart` horizontal bars, **sorted descending** | Unsorted list |
| Part-to-whole, **2 to 3 parts** | `.donut` | none |
| Part-to-whole, **4+ parts** | `.stack` proportional bar, % in the legend | A pie or a donut |
| A trend over time, up to 5 series | `.lchart` inline SVG line, one `<g class="ln lnN">` per series | Columns per period |
| A schedule progressing over time | `.gantt` rows on a shared axis | Flush proportional bars |
| Relative effort size, explicitly not a schedule | `.tline-bars` with `flex:N` | Equal-width boxes |
| 2 to 4 standalone numbers where the number is the message | `.stat-row` on `s-numbers` | Bars encoding the same number twice |
| Categorical list with role/type tags, no numeric axis | `.cmp-table` or `.card` grid | A bar chart with invented percentages |

- Series colors only: `.c1` navy, `.c2` dark blue, `.c3` sapphire, `.c4` sky, `.c5` light blue. Never restyle a series by hand; each `.cN` carries its own label color in `--on` and remaps on dark slides.
- A legend matches its own fills. The donut sets colors inline via `conic-gradient`; write its legend swatches inline from the same values.
- Data labels on, gridlines off. No 3D, no shadows, no legend where a direct label does.
- One insight per chart: every chart slide ends with one `.insight` line stating the conclusion, not describing the chart. `qa.py` fails a chart slide without one. An `s-numbers` slide gets one too, saying which number is the argument; `qa.py` does not check that one.
- No pie charts. 2 to 3 parts is the donut, everything else the stacked bar.
- Never invent numbers to make a chart work. Categorical data is a table or cards.
- A table kept from the source is `.cmp-table` with the contents intact, read across not down: a handful of rows, at most four columns, or it goes to the notes or an appendix.
- One chart per slide.

## Length

- Short input (memo, notes, under ~800 words): one slide per point, roughly 5 to 10 slides.
- Long input (report, full document): the executive narrative, roughly 12 to 24 slides. Detail that does not survive goes into the notes.
- Aim at 40 words of body copy per slide. `qa.py` counts table body cells at half weight, so a real comparison table fits without shortening its cells. It warns and then errors past its word and bullet limits; an error means the slide was always two slides.

## Presenter notes

Every slide gets an `<aside class="notes">`: what the presenter says, the context behind the point, the handoff to the next slide. Two or three sentences, not a restatement of the bullets.

## QA

```bash
python3 <this skill dir>/scripts/qa.py <slug>.html
```

Needs `beautifulsoup4`; if missing, the script prints the install command. Checks tone rules, notes on every slide, bullet and word density, palette, graphic-element handling, insight lines, duplicate ids, placeholder text, Title Case headings, the logo label. Errors must be fixed; warnings are judgement calls.

Then look at every slide, which the script cannot. Without a browser, report these as not done rather than claiming the deck prints:

- [ ] Nothing overflows the slide box, especially the longest bullet slide
- [ ] Footer logo and slide number clear the content on every slide
- [ ] Graphic element sits behind the text, never across it
- [ ] Every `font-size` is a `slides.css` token; nothing below `--slide-text-xs` on a slide face
- [ ] Contrast pairs from `BRAND.md` on every dark slide
- [ ] Print preview gives one slide per page, no blank pages, no clipped edges

## When this is the wrong skill

- **The deliverable must be a `.pptx` file.** No skill in this plugin writes PowerPoint. Say so and let the user decide.
- **The content is read, not presented**: a long-form report or briefing is `create-report`.
