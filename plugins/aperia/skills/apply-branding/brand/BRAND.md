# Aperia Brand: Rules

> Reference, not a skill. Every skill reads it in full. Rules live here, values live in `tokens.css`. A value not in `tokens.css` is not an Aperia value; do not take one from memory.
>
> Source: Aperia Brand Guidelines v1.0. Companion files: `tokens.css`; `assets/aperia-logo.svg`, `assets/pattern-single.svg`, `assets/pattern-single-portrait.svg`, `assets/pattern-double.svg`; `DEVIATIONS.md`, the recorded gaps between the guideline and what ships; `palette.py`, the palette reader the scripts use.

---

## Color

HEX for digital, Pantone or CMYK for print. This table adds what a stylesheet cannot carry: the print equivalents and the role of each color.

| Name | Token | Pantone | CMYK | Role |
|---|---|---|---|---|
| Aperia Blue | `--aperia-blue` | P108-16C | 100/70/0/50 | Primary: hero fills, dark panels, headings on light |
| Dark Blue | `--dark-blue` | P105-8C | 100/65/0/30 | Secondary blue, gradient partner |
| Sapphire Blue | `--sapphire-blue` | P106-8C | 100/50/0/0 | Accent: labels, links, highlights |
| Sky Blue | `--sky-blue` | P115-5C | 45/0/0/0 | Light accent, eyebrow text on dark |
| Light Blue | `--light-blue` | P115-10C | 20/0/2/0 | Tints, soft fills |
| Black | `--black` | n/a | | Type, logo alternate |
| Dark Gray | `--dark-gray` | P179-13C | | Muted body copy, captions |
| Medium Gray | `--medium-gray` | P179-6C | | Rules, subtle UI, disabled |
| Light Gray | `--light-gray` | P179-2C | | Muted backgrounds, cards |
| White | `--white` | n/a | | Backgrounds, type on dark |

Approved contrast pairs (WCAG AAA): Aperia Blue on White · Aperia Blue on Light Gray · White on Aperia Blue · White on Dark Blue · White on Sapphire Blue · Aperia Blue on Sky Blue · White on Dark Gray · White on Black.

- Palette colors only, everywhere: charts, accents, gradients, secondary text.
- Gradients pair two palette colors (Aperia Blue to Dark Blue, White to Light Blue).
- Chart series in this order: Aperia Blue, Dark Blue, Sapphire Blue, Sky Blue, Light Blue, then neutrals.
- Red, amber and green only for genuine status, kept minimal.
- No colored border accents on cards or panels. Status rides a dot, a chip or a heading color.
- Secondary information in grey.

---

## Typography

- Inter. Arial where Inter cannot be embedded (Outlook, system-font contexts).
- Weights: Light, Regular, Medium, SemiBold, Bold. Body is Regular on screen and in Office, Light or Regular in print, never Bold. SemiBold (`--fw-semibold`) for UI emphasis: headings, table headers, card titles, labels, buttons. Medium for pull quotes and large paragraphs.
- Never underline.
- Hierarchy from size and weight contrast, not decoration.
- Nothing on screen below `--min-size`: labels, badges, legends, ticks, captions and footnotes included. A subordinate label gets weight, letter-spacing, case or color, not a smaller size. Print minimum 5pt.

### Type scale

- Ten steps, `--text-xs` to `--text-5xl`, in `tokens.css`, each used with its paired `--leading-*`.
- Token names are sizes, not roles. No size is tied to an `h1`..`h6` tag; the token is applied at the use site.
- No new step. Between two steps, take the nearer and build the difference from weight, spacing, case or color.
- Responsive display sizes clamp between two ramp steps and are named for the ceiling: `2xl` and `5xl`.
- Slides map this ramp onto a 1920x1080 canvas with 19.5px as the floor; `create-slides` holds those tokens.

### Case, alignment, spacing

- Title Case for headings, labels, actions, menu items, page titles. Sentence case for descriptions, tooltips, body. ALL-CAPS only for brand names, short navigation, short calls to action and abbreviations. Never all-caps or all-lowercase running text.
- Left-align. Center only on landing pages, heroes and columns. Never right-align, never justify.
- Body leading about 1.5. One paragraph spacing and one indent, used consistently. Numbered paragraphs left-aligned, the number not indented.
- Phone numbers `(NPA) XXX-XXXX`. URLs without `https://`. Email addresses carry first and last name.

---

## Logo

`assets/aperia-logo.svg`, 135x40, Aperia Blue. Inline it, never link it.

- Aperia Blue, black or white only. On dark or blue backgrounds recolor every `fill` to `--white`.
- Clear space on all sides: the cap height of "Aperia".
- Minimum 24px on screen, 10mm in print.
- Stands alone. It never reads as attached to the graphic element.
- Never: shadow, transparency, stretch, outline, gradient, rotation, another typeface, weight or treatment.
- Beside a partner logo: center-aligned, optically equal, two letter-A gap, horizontal or vertical. Beside a product logo: horizontal only, one letter-A gap with a vertical rule, the product never taller than Aperia.

---

## Graphic element

The curved-edge parallelogram. Three SVGs ship in `assets/`:

| File | Shape | Use |
|---|---|---|
| `pattern-double.svg` | Two elements, gradient, viewBox 406.1x283.3 | Hero banners, landscape covers |
| `pattern-single.svg` | One element, gradient, viewBox 127.6x85.1 | Dark panels, CTA boxes |
| `pattern-single-portrait.svg` | The single element, full-bleed portrait, viewBox 226.8x283.5 | Portrait formats; slide sections and statements |

1. Top-right, always.
2. Whole element visible, curve included: `preserveAspectRatio="xMaxYMin meet"`.
3. `height:100%; width:auto`. No width cap, no stretch. Surplus width bleeds off the right edge under `overflow:hidden`.
4. No rotation, no flip.
5. Palette gradients only, as supplied.
6. Behind content: element `z-index:0`, content `z-index:1`. Never over text or a photo subject.
7. Text sits left.
8. Landscape surface: the double pattern, uncut. Portrait surface: the portrait single, never a solid single.
9. More than one inlined SVG on a page: a unique `id` on every `linearGradient` and `clipPath`.

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

Alternative treatments, sparingly: two opposite gradient elements on the right for vertical formats; a larger element behind for horizontal formats; two solid palette elements for internal-only items. Over a photo, the overlay gradient is Dark Blue at 100% opacity, 100% location, to Aperia Blue at 0% opacity, 10% location, angle 70°.

---

## Photography

Real people in real settings: natural expressions, working clothes, clean simple environments, high contrast, a clear focal point and a free zone for any copy. Only typography or a CTA button goes over an image. Prefer open space at the top or right so the element and the text have room.

Never: posed or negative expressions, blur or reflection effects, artificial lighting, hard shadows, flare or over-exposure, cluttered or busily patterned scenes.

Royalty-free sources: unsplash.com, rawpixel.com, pexels.com, freepik.com.

---

## Voice

Fact-based, steady, clear. No hyperbole, no exclamation marks.

---

## Format notes

- **PowerPoint / Word**: Inter Regular body, Bold or Medium headings. Backgrounds Aperia Blue with the element top-right, or white with Aperia Blue type.
- **Excel**: header rows Aperia Blue with white type, banding Light Gray, Sapphire Blue for emphasis. The element on cover and summary sheets only, never on data sheets.
- **HTML**: Inter from Google Fonts, palette as custom properties, SVGs inlined. A full report is `create-report`.
- **Diagrams and charts**: palette series in order, left-aligned labels, Inter, approved contrast pairs, no pie where a stacked bar reads better.
