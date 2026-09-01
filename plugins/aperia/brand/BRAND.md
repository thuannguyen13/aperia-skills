# Aperia Brand Guidelines: Reference

> **This is a reference document, not a skill.** It is the single source of truth for
> Aperia's visual identity. Every skill in the `aperia` plugin reads this file in full
> before producing anything. Do not duplicate these values into a skill, read them here.
>
> **Source**: Aperia Brand Guidelines v1.0 (Logo, Color, Typography, Photography,
> Graphic Elements, Applications).
>
> **Companion files** (same directory):
> - `tokens.css`: the token file. Palette, type scale and weights as CSS custom
>   properties. Anything that needs the values programmatically parses these.
> - `assets/aperia-logo.svg`, `assets/pattern-single.svg`, `assets/pattern-double.svg`
> - `DEVIATIONS.md`: audited gaps between this guideline and what ships here

Apply Aperia's visual identity to any artifact: presentations, documents, spreadsheets,
HTML pages, charts, and social/banner assets. This document is the **brand layer**. It
defines what things look like. The skill that invoked it defines how the artifact is built.


---

## Color

Pantone and CMYK are for print and promotional items. **RGB/HEX are for web and digital**, so use HEX in any artifact this environment produces.

### Core palette

| Name | HEX | RGB | Pantone | CMYK | Role |
|---|---|---|---|---|---|
| Aperia Blue | `#002F67` | 0/47/103 | P108-16C | 100/70/0/50 | Primary brand color: hero fills, dark panels, headings on light |
| Dark Blue | `#004785` | 0/71/133 | P105-8C | 100/65/0/30 | Secondary blue, gradient partner |
| Sapphire Blue | `#0072BC` | 0/114/188 | P106-8C | 100/50/0/0 | Accent: labels, links, highlights, chart series |
| Sky Blue | `#7ED3F7` | 126/211/247 | P115-5C | 45/0/0/0 | Light accent, eyebrow text on dark |
| Light Blue | `#C8EAF5` | 200/234/245 | P115-10C | 20/0/2/0 | Tints, soft fills |

### Neutral palette

Neutrals add texture and depth. In text-heavy compositions, de-emphasize secondary information by setting it in grey.

| Name | HEX | RGB | Pantone | Role |
|---|---|---|---|---|
| Black | `#000000` | 0/0/0 | n/a | Type, logo alternate |
| Dark Gray | `#58595B` | 88/89/91 | P179-13C | Muted body copy, captions |
| Medium Gray | `#A7A9AC` | 167/169/172 | P179-6C | Subtle UI, rules, disabled |
| Light Gray | `#F1F2F2` | 241/242/242 | P179-2C | Muted backgrounds, cards |
| White | `#FFFFFF` | 255/255/255 | n/a | Backgrounds, type on dark |

### Accessible combinations

All pairings below pass WCAG AAA and are the approved defaults:

- Aperia Blue on White · Aperia Blue on Light Gray · White on Aperia Blue
- White on Dark Blue · White on Sapphire Blue · Aperia Blue on Sky Blue
- White on Dark Gray · White on Black

Ensure high contrast between type and its background in every composition. Do not introduce colors outside this palette, including for charts, accents, or gradients.

### Color application

- Gradients use **only** palette colors (e.g. Aperia Blue → Dark Blue, White → Light Blue).
- Charts: build series from Aperia Blue → Dark Blue → Sapphire Blue → Sky Blue → Light Blue, then neutrals. Never introduce red/green/amber except for genuine semantic status, and keep those minimal.
- **No colored border accents on cards or panels.** A card keeps its neutral
  hairline edge. Status and identity ride markers, chips and type: a status dot,
  a labelled chip, a colored heading. A tinted or colored border edge reads as
  templated decoration rather than as information, and it duplicates a signal
  the content already carries.
- In `python-pptx` / `openpyxl`, convert HEX to `RGBColor(0x00, 0x2F, 0x67)` form.

---

## Typography

**Inter** is the primary typeface and a foundational pillar of the identity (free, SIL OFL, at rsms.me/inter or Google Fonts).

- Weights in use: **Light, Regular, Medium, SemiBold, Bold**. Light is the default for body text; in MS Office applications (Word, PowerPoint) use **Regular** for body.
- **SemiBold (600) is sanctioned for UI emphasis in the HTML themes**: headings, table headers, card titles, labels and buttons, where Bold is too heavy against Light body copy and Medium is too weak. It is not a body weight. Body copy stays Regular or Light, and the never-set-body-in-Bold rule is unchanged. Weights outside this list remain exceptional.
- **Alternative typeface: Arial** wherever Inter can't be embedded (Outlook emails and signatures, system-font contexts). Arial is the system font on Mac and Windows.
- **Body text: Regular or Light only.** Never set body copy in Bold. Bold is for brief highlights.
- **Never underline** text or headlines.
- Build hierarchy with different **sizes/scales and weights**: big, strong headlines against smaller type. Inter Medium suits pull quotes and large paragraphs.
- Print minimum type size: **5pt**.
- **Minimum on-screen type size: 12px.** Nothing renders below it, including
  micro-labels, badges, tag pills, chart legends, axis ticks, captions and footnotes.
  Where a label needs to read as subordinate at 12px, build that from weight,
  letter-spacing, case and color, never by going smaller.

### Type scale

The ramp below is the Aperia Figma design system scale and is the sanctioned set of
sizes. Adding a step is a change to this document, not a local decision.

Token names are **size-semantic, never role names**, and no size is tied to an
`h1`..`h6` tag. A heading gets its size from a token applied at the use site, so the
same step can serve a heading in one place and a number in another.

| Token | Size / line-height | Ratio |
|---|---|---|
| `xs` | 12 / 16 | |
| `sm` | 14 / 20 | 1.17 |
| `base` | 16 / 24 | 1.14 |
| `md` | 18 / 28 | 1.13 |
| `lg` | 20 / 32 | 1.11 |
| `xl` | 24 / 36 | 1.20 |
| `2xl` | 28 / 40 | 1.17 |
| `3xl` | 32 / 48 | 1.14 |
| `4xl` | 36 / 52 | 1.13 |
| `5xl` | 40 / 56 | 1.11 |

Each step carries the paired line-height shown; use them together.

**Two Figma steps are not in the web ramp.** The design system also holds 10/12 and
11/16. Both fall below the 12px on-screen minimum above, so they stay print and
Figma only and the web ramp starts at `xs`.

**The 36 and 40 leadings are derived**, not taken from Figma, which stops at 32/48.
They continue the ramp's +4 leading progression. Confirm them with the designer
before treating them as final.

The ramp is deliberately fine-grained rather than merged: it is the shared
reference for every skill, so it has to cover editorial, data and display type
without a component being pushed onto a step that does not fit it.

**Responsive headings** are clamped between two ramp steps, never off-scale values.
The two display utilities clamp between ramp steps and are named for their
ceiling: `2xl` runs 20/32 to 28/40, and `5xl` runs 28/40 to 40/56.

The `deck` skill is the exception: its slide faces are measured in canvas units on
a 1920x1080 box that is scaled to fit the viewport, so it maps this ramp onto that
canvas with 19.5px as its own floor, which holds the 12px minimum down to a 1180px
viewport.

### Case

- **Title Case** for field labels, actions, menu items, page titles. (Capitalize major words; skip articles and short prepositions.)
- **Sentence case** for longer copy: page/field descriptions, tooltips, body paragraphs.
- **ALL-CAPS cautiously**: brand names, core navigation points, short calls to action, standard abbreviations. Never an all-caps sentence or paragraph, and never all-lowercase.
- Use correct punctuation and capitalize proper nouns.

### Alignment, leading, spacing

- **Left-align by default** for headlines, paragraphs, and quotes. Center alignment only for landing pages, hero sections, and columns. **Never right-align or justify.**
- Align to the grid; when aligning with other copy, align to the containers.
- **Leading**: comfortable, never too tight or too loose. ~1.5× for body copy is a safe default.
- **Paragraph spacing**: one or two default line breaks, applied consistently throughout the document.
- **Element spacing**: group related elements tightly; separate unrelated ones. White space guides the reader and sets the focus area.
- **Indents**: pick one standard indent and apply it to every paragraph. Numbered paragraphs are left-aligned, and never indent the number itself.

### Type setting rules

- Phone numbers in US format, separated by dashes: `(NPA) XXX-XXXX`
- URLs written without `https://` → `www.aperia.com`
- Email addresses contain first and last names

---

## Logo

The Aperia wordmark ships with this skill: `assets/aperia-logo.svg` (135×40, Aperia Blue). Inline it into HTML/SVG artifacts rather than linking externally.

- **Color**: Aperia Blue, black, or white **only**. On dark or blue backgrounds, recolor every `fill` to `#FFFFFF`.
- **Clear space / exclusion zone**: equal to the cap height of "Aperia" on all sides. Nothing intrudes into it.
- **Minimum size**: 24px height on screen, 10mm in print.
- **Pairing with partners**: center-aligned, optically equal size, **two letter-'A' spacing** between marks. Horizontal or vertical alignment allowed.
- **Pairing with products/sub-brands**: horizontal only, **one letter-'A' spacing** with a vertical rule between them. The product logo may never be taller than the Aperia logo.

### Logo misuse, never do these

Drop shadow · changed transparency · stretch or distort · off-palette colors · outlined · changed typeface, weight, or treatment · gradient fill · rotation.

---

## Graphic element (the parallelogram)

The curved-edge parallelogram is how Aperia's graphic style stays consistent. Two ready-made SVGs ship here:

| File | What it is | Where to use |
|---|---|---|
| `assets/pattern-double.svg` | Two-element gradient shape (viewBox 406.1×283.3) | Hero banners, landscape covers |
| `assets/pattern-single.svg` | Single-element gradient shape (viewBox 127.6×85.1) | Dark panels, CTA boxes, portrait formats |

### Rules (strict)

1. **Position: top-right** of the surface, always. Never any other corner.
2. **Show the full element** with its curved edge clearly visible, using `preserveAspectRatio="xMaxYMin meet"`. Showing too little of the curve is a misuse.
3. **No distortion.** Lock the aspect ratio (`height:100%; width:auto`), never stretch.
4. **No rotation, no flip.**
5. **Palette colors only** for the shape and its gradient.
6. **Fill the container height.** Don't cap width; surplus width bleeds off the right edge under `overflow:hidden`.
7. **Background only**: element at `z-index:0`, content at `z-index:1`. Never cover subjects or text.
8. **Don't cut the element** on a landscape background, and don't use a single solid element on a portrait background.

### With logo, text, and photography

- **Logo**: the logo stands alone and must not appear to relate to the element. Element top-right, logo positioned so the two read separately.
- **Text**: because the element sits right, **text sits left**.
- **Photography**: prefer images with open space at the top or right; avoid busy top/left backgrounds. Use the element as background, never over the subject. Recommended gradient overlay: upper point Dark Blue at 100% opacity / 100% location, lower point Aperia Blue at 0% opacity / 10% location, angle 70°.
- The element may be used as an image container to emphasize part of a photo. Use sparingly so it stays impressive.

### Alternative styles

1. **Two opposite gradient elements**, both on the right, excess of the second removed. Best for vertical formats (posters, standees, mobile screens, wallpapers).
2. **Bigger element behind.** Remove the excess of the larger element. Best for horizontal formats (desktop/TV wallpaper, slide covers).
3. **Two opposite solid elements**, using solid palette colors instead of gradients, for internal-use items of limited quantity (team decks, team-building materials, internal decor).

### Correct hero pattern

```css
.hero       { position:relative; overflow:hidden }
.hero-shape { position:absolute; top:0; right:0; height:100%; width:auto; z-index:0 }
.hero-inner { position:relative; z-index:1 }   /* text sits left */
```

```html
<svg class="hero-shape" viewBox="0 0 406.1 283.3" preserveAspectRatio="xMaxYMin meet"
     aria-hidden="true" xmlns="http://www.w3.org/2000/svg">
  <!-- paste defs + paths from assets/pattern-double.svg; give each gradient a unique id -->
</svg>
```

When inlining more than one SVG in a page, give every `<linearGradient>` and `clipPath` a **unique `id`** to avoid collisions.

---

## Photography

Aperia is fact-based and steady; photography must read as **trustworthy and authentic**: real situations in real settings.

**Principles**: high quality and contrast · expressive and natural · clean and simple · similar hues and complementing colors · professional and confident · diverse and unclichéd.

- **Lighting**: dark or light to suit the content; avoid hard or long shadows on subjects.
- **Environment**: simple and neat; avoid cluttered, distracting compositions.
- **Expressions**: professional, natural, friendly; proper working clothes. No unnatural poses or exaggerated/negative expressions.
- **Composition**: every image needs a clear focal point and a safe zone (free area) for any message placed on it. Do not put any graphic element other than typography or CTA buttons on top of an image.

**Four photo types**: People (portraits front-and-center, in focus, clean background; workplace shots candid and interactive, in full body, half body, and aerial views) · Places (architecture and environments evoking stability, trust, innovation, ambition; people present but never the protagonist) · Abstracts (simple, expressing strength, unity, or movement) · Objects (focus on the main object).

**Don'ts**: exaggerated posing · negative expression · reflection or blurry effect · people lit with artificial light · complicated environment · dark or threatening light · flare or over-exposure · casual, informal, or busily patterned attire.

Royalty-free sources: unsplash.com, rawpixel.com, pexels.com, freepik.com.

---

## Voice

Fact-based, steady, trustworthy, authentic. Copy is dependable and clear, not hyperbolic.

---

## Application checklist

Run this before delivering any branded artifact:

- [ ] Every color is from the core or neutral palette, with no off-palette values
- [ ] Type is Inter (or Arial fallback); body in Regular/Light, never Bold
- [ ] No on-screen type below 12px anywhere, labels and legends included
- [ ] Nothing underlined; no all-caps or all-lowercase running text
- [ ] Text left-aligned (center only for hero/landing); nothing justified or right-aligned
- [ ] Contrast pairs come from the approved accessible combinations
- [ ] Logo in Aperia Blue, black, or white; clear space respected; ≥24px / 10mm
- [ ] Graphic element top-right, undistorted, unrotated, full curve visible, behind content
- [ ] Text sits left where the element sits right; logo stands alone
- [ ] Photography follows type, lighting, expression, and safe-zone rules
- [ ] Hierarchy built from size and weight contrast, not decoration

---

## Format notes

- **PowerPoint / Word**: Inter Regular for body (not Light, because of Office rendering). Headings in Bold or Medium. Slide backgrounds in Aperia Blue with the graphic element top-right, or white with Aperia Blue type. Convert HEX via `RGBColor`.
- **Excel**: header rows in Aperia Blue with white type; banding in Light Gray; Sapphire Blue for emphasis. Keep the graphic element out of data sheets and use it on cover/summary sheets only.
- **HTML / web**: load Inter from Google Fonts; define the palette as CSS custom properties; inline the SVG assets. For full report layouts use the `report` skill.
- **Diagrams / charts**: palette-only series, left-aligned labels, Inter, high-contrast pairs, no pie charts where a proportional stacked bar reads better.
