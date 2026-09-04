---
name: create-slides
description: Build an on-brand Aperia slide deck as a single self-contained HTML file.
---

# Aperia Deck

Builds a presentation as **one self-contained HTML file**.

## Step 0: Read the brand layer first (required)

Before writing a line of HTML:

1. Read **`../../brand/BRAND.md`** in full, especially Color, Typography, Logo,
   Graphic Element, and Format Notes.
2. Read **`../../brand/tokens.css`** for the values, but **never paste it into
   a deck**. `references/slides.css` is the only style block a deck carries: it
   already mirrors the brand values in canvas space, so a second `:root` would
   override them with screen-px ones. `--radius` is the clearest case, 15 canvas
   units here against 8px there, and a paste flattens every card in the deck.
3. Read **`references/slides.css`** (the slide theme) and
   **`references/snippets.html`** (the layouts and the deck script).

**Do not work from memory of the palette or the type rules.** If a value is not
in `BRAND.md` or `tokens.css`, it is not an Aperia value. Do not invent it.

Brand assets are at `../../brand/assets/`. The rules below cover what is
specific to slides; everything about the identity itself lives in `BRAND.md`.

**Design language follows `../../ui-components/COMPONENTS.md`.** That shared
reference layer is the canonical source for how a component *means*
something, independent of the canvas-unit vs. screen-px difference: which
color a badge or callout carries for which sentiment, that status rides
text/chip color rather than a colored card edge, the fixed `s1→s5`
chart-series order (aperia-blue, dark-blue, sapphire, sky-blue, light-blue),
and the chart-selection logic (a bar chart needs a real quantitative axis, a
part-to-whole story stays within a slice budget, never invent a percentage
to force a chart). `slides.css` already implements all of this in canvas
units — the badge and callout palettes below are the same hex values
`../../ui-components/styles.css` uses on screen, not a reinterpretation.
When the two diverge (this deck caps a donut at 3 segments where
`../../ui-components/COMPONENTS.md` allows 5, since a slide is read from
across a room in a few seconds), that is a deliberate, more conservative
choice for the presentation context, not a gap to close.

No PowerPoint template, no build step, no dependency beyond Google Fonts.

What the output does:

- Arrow keys / space / swipe move between slides; `O` opens a thumbnail
  overview, `N` toggles presenter notes, `F` goes full screen.
- Ctrl/Cmd+P prints one slide per landscape page, a clean 16:9 PDF.
- Opens on any machine, hosts anywhere, sends as a link.

## Workflow

1. **Read the source.** A file the user points at, or content pasted into the
   conversation. `markitdown` handles `.docx`/`.pdf`/`.pptx` if it is installed.
2. **Outline first.** Decide the slide sequence and the layout and tone for each
   slide. Show the outline and get a nod before generating, unless the user
   asked for the finished deck straight away.
3. **If the source contains a table, ask what to do with it**, before building,
   not after. A table that made sense in a document is often the wrong shape on
   a slide. Offer the choice plainly: keep the exact contents as a table, or
   convert it into a chart or a diagram. Ask once, listing each table you found,
   and never convert silently, the numbers may be the point.
4. **Read `references/slides.css` and `references/snippets.html`** before writing
   a line of HTML. Paste the theme verbatim; copy the layout markup and replace
   the copy, not the structure.
5. **Build** the single HTML file.
6. **QA**: run `python3 <this skill dir>/scripts/qa.py <file>`, required, then
   look at it.
7. **Save** as `<slug>.html` in the working directory, unless the user names a
   different location, and tell them the path.

Tell the user how to drive it: arrow keys, `O`, `N`, `F`, and Ctrl/Cmd+P for the
PDF.

---

## The canvas: read this before anything else

**Every slide is a fixed 1920 × 1080 box.** The script scales the whole canvas to
fit the viewport; the print stylesheet scales it onto a 13.333in × 7.5in page.
Because the canvas never changes size, slide design is predictable, what you
see is what prints.

This means:

- Use **fixed canvas units only** inside a slide, and take every font size from
  the type tokens in `slides.css`. Never `vw`, `vh`, `clamp()`, or `%` font
  sizes. Responsive-web habits are wrong here: a slide is a fixed canvas, not a
  flowing page, and viewport units break the print output.
- There is **no mobile breakpoint** for slide content and none is needed, the
  whole canvas shrinks together. Only the deck chrome adapts.
- If content does not fit at 1920 × 1080, it is **two slides**. Never shrink the
  type to make it fit.

Every slide sits inside a `.stage` wrapper:

```html
<section class="stage">
  <article class="slide s-light s-text"> … </article>
</section>
```

---

## Light and dark

- **Light slides carry text.** Any slide with a paragraph, four or more points,
  a table, a chart the reader must study, anything they actually read.
- **Dark slides carry emphasis.** Covers, agendas, section dividers, single
  statements, quotes, one big number, closings.

**Covers, agendas, section dividers, statements, quotes and closing slides are
always dark.** Fixed, not a default. `qa.py` fails the deck if one is light.

Expect a rhythm: dark cover, dark agenda, dark section divider, light content
through the section, a dark statement at the turning point, dark close. All-dark
is unreadable; all-light is flat. Roughly a third dark is right.

There is **one dark tone class, `s-dark`** (brand gradient). Add `flat`
alongside it, `class="slide s-dark flat"`, to swap the gradient for solid
Aperia Blue on in-body emphasis slides, big-number slides, and any slide
carrying a donut. `flat` changes only the background; every tone rule still
comes from `s-dark`, so nothing can go half-styled.

## Layouts

Address a slide by its tone class plus its layout class. Full markup for every
one is in `references/snippets.html`.

| Slide layout | Classes |
|---|---|
| **Always dark** | `s-cover` `s-agenda` `s-section` `s-statement` `s-quote` `s-end` |
| **Light, text** | `s-text` `s-two-col` `s-icons` |
| **Either tone** | `s-numbers` `s-image-full` |

**Six of those carry CSS**: `s-cover`, `s-section`, `s-statement`, `s-quote`,
`s-end` and `s-image-full`. `s-text`, `s-two-col`, `s-icons`, `s-agenda` and
`s-numbers` style nothing. They are naming conventions `qa.py` reads, the tone
rule keys on `s-agenda`, so keep applying them even though dropping one changes
no pixel.

**The closing slide carries the graphic element and a heading, nothing else.**
No subtitle, no contact block, no logo footer, no page number. The ask, the date
and who to contact are spoken from the notes. `qa.py` fails an `s-end` slide
that has anything but its heading, and the theme hides stray children anyway.

Components drop into any layout and are not slide classes: `.card`, `.iblock`,
`.callout`, `.badge`, `.cmp-table`, `.flow`, `.stat-row`, the `.g2` `.g3` `.g4`
card grids, and the chart components below. A comparison-table slide is
`s-light s-text` holding a `.cmp-table`, not a `cmp-table` slide.

### Sequences become diagrams, not bullets

**If the content describes a flow, a journey, a process, a pipeline, or anything
step-by-step, draw it.** A numbered list of stages is the single most common way
a deck wastes a slide: the audience has to reconstruct the sequence in their
heads from text that shows no direction.

Reach for the right shape:

- **Ordered stages, no timeline**: `.flow`. Numbered nodes connected left to
  right, one short line of description each. Three to five steps; more than five
  is two slides or a coarser grouping.
- **Stages that occupy time**: `.gantt`. Use it the moment durations or overlap
  matter, because `.flow` implies order but says nothing about how long.
- **Relative effort across stages, explicitly not a schedule**: `.tline-bars`.
- **A cycle rather than a line**: `.flow` still works; say so in the heading and
  make the last step's copy close the loop back to the first.

Give every stage a verb for its title ("Ingest", "Score", "Triage"), not a noun
phrase. If a step cannot be named in one or two words, the sequence is drawn at
the wrong altitude, group it.

Two height helpers, and they are not interchangeable: `.fill` takes the leftover
height and keeps the element's own display (add it to a `.g2`/`.g3`/`.g4` grid
and the rows centre); `.fill-c` is the flex-column version, for centring a
bullet list or a loose block. Putting `.fill` on a grid used to flatten it,
that is why they are separate.

---

## Brand foundations (non-negotiable)

### Palette: how the brand colors are used on a slide

The values live in `../../brand/BRAND.md` and `tokens.css`. Take them from
there. What is specific to slides is the role each one plays:

| Token | Role on a slide |
|---|---|
| Aperia Blue | Primary. Dark slide backgrounds, headings on light, chart series 1 |
| Dark Blue | Secondary blue, gradient partner, chart series 2 |
| Sapphire Blue | Accent. Kickers on light, bullet markers, the insight line, chart series 3 |
| Sky Blue | Light accent. Kickers and stat values on dark, chart series 4 |
| Light Blue | Tints, the "rest of the total" band in charts |

Neutrals carry their usual roles, with Dark Gray for muted copy.

Sentiment colors (green/amber/red) exist **only** for callouts and badges. Never
use them for a chart series. `qa.py` flags any hex outside the theme.

> The values above are the brand-guideline palette and are the default. The
> official Aperia PowerPoint template ships two slightly different accents. If
> this HTML deck will be shown next to a deck built on that template, and only
> then, swap Sapphire `#0072BC` → `#1570E0` and Sky `#7ED3F7` → `#25B4F1`, and
> add both to the palette list in `qa.py`. Ask before doing this; otherwise
> keep the values above.

### Typography: Inter

- **Inter**, loaded from Google Fonts, fallback Arial. Regular (400) for body;
  Medium/SemiBold/Bold build hierarchy. Never underline a headline.
- **Left-align by default.** Centering is for the cover and statement slides
  only. Never justify.
- **Title Case for every heading.** ALL-CAPS only for short uppercase labels
  (kickers, chart notes, badges), never for running text.
- **Every size comes from the Type scale token block in `slides.css`.** That
  block is the single authority: it maps the `BRAND.md` ramp onto the canvas
  and names each token for the brand step it mirrors, `--slide-text-*` for body
  type on a slide face and `--slide-display-*` for headlines. Sizes there are
  canvas units multiplied by the fit-to-viewport scale, so the slide-face floor
  is 19.5px rather than 12px. Deck chrome (`.ui-*`) sits outside the canvas and
  uses the brand `--text-*` steps in real screen px. Never write a raw px
  font-size on a slide, never override the scale slide by slide, and never put
  a screen-px `--text-*` value on a slide face.

### Voice

Fact-based, steady, trustworthy. Slide copy should be shorter and flatter than
report copy, a slide asserts, the presenter explains. No hyperbole, no
exclamation marks.

---

## Brand assets

Three real SVGs live in `../../brand/assets/`. They are **defined once in a sprite** at the
top of `<body>` and referenced with `<use>` on each slide, so the path data
appears once, and there is no gradient-id collision anywhere in the file. The
sprite is in `references/snippets.html`; paste it as-is.

| Symbol | Source | Where |
|---|---|---|
| `#ap-shape-double` | `../../brand/assets/pattern-double.svg` | Cover and closing slides |
| `#ap-shape-single` | `../../brand/assets/pattern-single-portrait.svg` | Sections, statements, dark in-body slides |
| `#ap-logo` | `../../brand/assets/aperia-logo.svg` | Cover (white) and every content slide footer |

`pattern-single-portrait.svg` is the full-bleed portrait rendition of the single
parallelogram. It is not the same file as `pattern-single.svg`, which is the
landscape tile the `create-report` skill uses. Slides want the portrait one.

The logo symbol uses `fill="currentColor"`, so CSS enforces the color rule
automatically: Aperia Blue on light slides, white on dark. Never recolor it any
other way, never distort, rotate, or add effects.

## Graphic element rules (strict)

1. **Top-right, always.** Never another corner.
2. **`preserveAspectRatio="xMaxYMin meet"`** so the whole shape shows and the
   curved edge is never clipped awkwardly.
3. **No distortion.** `height:100%; width:auto`, never two fixed mismatched
   dimensions.
4. **No rotation, no flip.**
5. **Palette gradients only**, exactly as supplied. On a blue slide it reads as
   a subtle "element behind", that is intended.
6. **Fill the full slide height, never capped.** Both elements, the double
   pattern on covers (`.shape-cover`) and the single pattern on sections,
   statements and dark in-body slides (`.shape-panel`), run the full 720px at
   `height:100%; width:auto`, anchored top-right. A width cap forces a shorter
   shape and breaks the treatment, so neither class carries one.
7. **Proportion follows the artwork, not a cap.** The double pattern is
   landscape and covers roughly the right two thirds at full height; the single
   pattern is portrait and covers roughly the right 45%. Both are correct as
   drawn, the gradient is navy to dark blue, so on a blue slide the element
   reads as depth behind the content rather than a graphic competing with it.
   Never resize either one to "balance" a slide; move the text instead.
8. **Never over text.** The element is `z-index:0`, `.s-body` is `z-index:1`.
   Because the element sits right, text sits left, keep headings and body copy
   within roughly the left two thirds and nothing will collide.

---

## Icons

Lucide line icons, the full set bundled offline in
`../../ui-components/assets/lucide-icons.json` — shared with
`../../ui-components/`, not a local copy. Browse at https://lucide.dev/icons/
and use the exact slug.

```bash
python3 <this skill dir>/scripts/icon.py shield-check users   # inline SVG
python3 <this skill dir>/scripts/icon.py --search shield      # find a slug
```

The markup uses `stroke="currentColor"`, so the theme colors it: dark blue on
light slides, sky blue on dark. Never hard-code a stroke color.

One icon per heading, same stroke weight throughout, never mixed with emoji or
filled glyphs.

---

## Charts

Slides get a **CSS/SVG chart set**, no chart library, so the file stays one
file. Pick the form that matches the data.

| The data | Component | Not this |
|---|---|---|
| A few categories compared on one scale, time-ordered | `.colchart` vertical columns | A table |
| Ranked quantities, one scale | `.bchart` horizontal bars, **sorted descending** | Unsorted list |
| Part-to-whole, **2 to 3 parts** | `.donut` | none |
| Part-to-whole, **4+ parts** | `.stack` proportional bar, % in the legend | A pie or a donut |
| A trend over time | `.lchart` inline SVG line | Columns per period |
| A schedule progressing over time | `.gantt` rows on a shared axis | Flush proportional bars |
| Relative effort size, explicitly not a schedule | `.tline-bars` with `flex:N` | Equal-width boxes |
| 2 to 4 standalone numbers where the number is the message | `.stat-row` on `s-numbers` | Bars encoding the same number twice |
| Categorical list with role/type tags, no numeric axis | `.cmp-table` or `.card` grid | A bar chart with invented percentages |

### Chart rules

- **Series colors only:** `.c1` navy, `.c2` dark blue, `.c3` sapphire, `.c4`
  sky, `.c5` light blue. Never a rainbow, never sentiment colors.
- **Never restyle a series by hand.** Each `.cN` carries its own label color in
  a `--on` custom property, so text sitting on a fill stays legible in both
  tones automatically. The ramp remaps on dark slides (navy would vanish on
  navy) while staying five distinct values, writing your own hex breaks that.
- **A legend must match its own fills.** Where a chart sets colors inline rather
  than by class, since the donut's `conic-gradient` is the one case, write the
  legend swatches inline from the same values. Mixing inline fills with `.cN`
  legend swatches silently disagrees on dark slides.
- **Data labels on. Gridlines off.** No 3D, no drop shadows, no legends where a
  direct label would do.
- **One insight per chart, called out.** Every chart slide ends with a single
  `.insight` line stating the takeaway in words. `qa.py` fails a chart slide
  without one. Not a description of the chart, the conclusion from it.
- **A numbers slide carries one too.** An `s-numbers` slide with a `.stat-row`
  gets the same single `.insight` line, saying which of the numbers is the
  argument. `qa.py` does not check this one, so it is on you.
- **No pie charts.** A pie is only legible with 2 to 3 near-equal slices; use the
  donut for that case and the stacked bar for everything else. (`../../ui-components/COMPONENTS.md`
  allows a plain pie too, capped at 5 slices, for freeform pages read up close;
  a slide is read from across a room, so this deck stays with the donut-only,
  3-segment ceiling `qa.py` enforces — narrower, not a different rule.)
- **Never invent numbers to make a chart work.** If you had to manufacture the
  percentages, the data is categorical, use a table or cards.
- **A table from the source is a decision, not a default.** Ask first (step 3),
  then follow the answer. Keeping it means `.cmp-table` with the contents
  intact; converting means picking the form from the table above and dropping
  the columns that were only there for completeness. A table that survives onto
  a slide should be one the audience reads across, not down: a handful of rows
  and no more than four columns, or it belongs in the notes or an appendix.
- **One chart per slide.** Two charts is two slides.

---

## Length

Match the source. Don't pad, don't dump.

- **Short input** (memo, notes, under ~800 words): mirror its structure, one
  slide per point. Roughly 5 to 10 slides.
- **Long input** (report, full document): condense to the executive narrative.
  Take the argument, not every paragraph. Roughly 12 to 24 slides. Detail that
  doesn't survive the cut goes into the presenter notes, not onto the slide.

**Aim at forty words of body copy per slide.** `qa.py` counts the visible words
on the slide face, notes, footer and chart data labels excluded, and **table
cells counted**, then warns over 55 on a light slide and errors over 85. More
than six bullets is an error too. Aim at 40, treat 55 as the line to argue with,
and read 85 as "this was always two slides".

## Presenter notes

**Every slide gets notes**, in an `<aside class="notes">` inside the slide. They
never render on the slide face, they appear in the presenter bar when the
presenter presses `N`.

Not a restatement of the bullets: what the presenter should say, the context
behind the point, and the handoff into the next slide. Two or three sentences.
This is a requirement, not a nicety.

---

## QA (required)

```bash
python3 <this skill dir>/scripts/qa.py <slug>.html
```

Paths in this file are relative to this skill directory, while the deck is
written in the working directory, so give both scripts their full path from
wherever you are. Each one resolves its own assets, so neither cares about the
current directory.

`qa.py` needs `beautifulsoup4`. If it is missing the script says so and prints
the install command. This is the one dependency in the plugin; the other three
skills need none.

It checks tone rules, notes on every slide, bullet and word density, palette
compliance, graphic-element handling, chart insight lines, duplicate ids,
placeholder text, and Title Case headings. Errors must be fixed. Warnings are
judgement calls, read them and decide.

Then **open the file and look at every slide**. The script cannot see overflow,
a collision with the footer, or an icon crowding a heading. Check in particular:

- Nothing overflows the 1920 × 1080 box, especially the longest bullet slide.
- The footer logo and slide number clear the content on every slide.
- The graphic element sits behind the text, never across it.
- Print preview (Ctrl/Cmd+P) gives one slide per page with no blank pages and
  no clipped edges.

---

## Files

- `references/slides.css`: the complete slide theme. Paste inside `<style>`.
  Read this first.
- `references/snippets.html`: document skeleton, brand sprite, every layout,
  every chart, and the deck script. Read this second, copy from it.
- `../../brand/assets/`: `aperia-logo.svg`, `pattern-single-portrait.svg`,
  `pattern-double.svg` if you need raw path data.
- `../../ui-components/assets/lucide-icons.json`: all 2,025 Lucide icons as path data, shared with `../../ui-components/`.
- `scripts/icon.py`: emit inline icon markup.
- `scripts/qa.py`: the required checker.

## Checklist before delivering

`qa.py` covers density, notes, palette, duplicate ids, and Title Case. This
covers what it cannot see.

- [ ] `BRAND.md` and `tokens.css` were read before writing
- [ ] Every color traces to `tokens.css`, or to a recorded entry in
      `brand/DEVIATIONS.md`
- [ ] Inter with Arial fallback; nothing underlined; no justified text
- [ ] Every `font-size` comes from a token in the `slides.css` Type scale
      block, no raw px anywhere
- [ ] No `font-size` below 12px: `--slide-text-xs` (19.5px in canvas units) is
      the floor on a slide face, `--text-xs` (12px) for `.ui-*` deck chrome
- [ ] Contrast pairs from the approved combinations in `../../brand/BRAND.md`
      on every dark slide
- [ ] Logo Aperia Blue on light, white on dark, nothing else; undistorted;
      clear space respected
- [ ] Graphic element top-right only, full slide height, behind the text
- [ ] Nothing overflows the 1920 x 1080 box on any slide, checked by eye
- [ ] Footer logo and slide number clear the content on every slide
- [ ] Ctrl/Cmd+P gives one slide per page, no blanks, no clipped edges
- [ ] Presenter notes on every slide, not a restatement of the bullets
- [ ] Every chart carries its insight line
- [ ] The Application Checklist in `../../brand/BRAND.md` passes

## When this is the wrong skill

Two cases, and in both the answer is to stop and say so rather than to improvise:

- **The deliverable must be a PowerPoint `.pptx` file.** This skill produces
  HTML, and an HTML file renamed is not a `.pptx`. No skill in this plugin
  writes PowerPoint. Say so and let the user decide, rather than improvising a
  conversion.
- **The content is read, not presented**, a long-form report or briefing the
  reader scrolls through. Slides are the wrong container for it.

Everything else about producing the deck is covered here, on top of the brand
layer this skill reads in Step 0.
