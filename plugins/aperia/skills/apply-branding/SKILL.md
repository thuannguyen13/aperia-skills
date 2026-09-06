---
name: apply-branding
description: Apply the Aperia brand to anything that is not a report or a slide deck, such as a landing page, an email, a dashboard, a diagram, a form, or a one-off graphic, or build one from scratch in the Aperia look. Holds the brand and component layers the other Aperia skills read.
user-invocable: false
metadata:
  version: "0.9.0"
---

# Apply Aperia Branding

Builds any artifact that is not a scrolling report or a slide deck in the Aperia identity, or re-skins one the user brings. This folder also holds the two layers every Aperia skill reads: `brand/` and `components/`. Nothing here is duplicated elsewhere.

## Step 0: Read the brand layer first (required)

1. Read **`brand/BRAND.md`** in full. It carries the rules: palette roles, type, logo, the graphic element, photography, voice, and the format notes for Office, Excel, HTML and diagrams.
2. Read **`components/COMPONENTS.md`** for the component and chart toolkits and the rules that govern them, then then only the snippet files the components you picked actually need. `COMPONENTS.md`'s toolkit tables carry a **File** column naming the one file each component's markup is in: `components/base/` holds `structure.html`, `emphasis.html`, `tables.html`, `charts.html` and `timelines.html`, and `components/charts/` holds `trend.html`, `compare.html`, `proportion.html` and `intensity.html`. Icons are in `components/icons/index.html`. Do not read all nine.

**Do not work from memory of the palette or the type rules.** The values live in `brand/tokens.css`. If a value is not there, it is not an Aperia value.

## When this is the wrong skill

- A long-form document the reader scrolls through is `create-report`.
- A presentation is `create-slides`.
- A PowerPoint, Word or Excel file cannot be produced here; say so. The format notes in `BRAND.md` still tell you how to brand one the user builds themselves.

Say which skill fits and stop, rather than building a report or a deck here.

## HTML output

Write the page around one style marker, `<style>/* @aperia page */</style>`, adding the word `charts` or `icons` when those toolkits are used, then run:

```bash
python3 <this skill dir>/components/assemble.py <file.html>
```

It fills the marker with `brand/tokens.css`, `components/base/styles.css` and the optional toolkits, byte for byte, and replaces its own block on every re-run. Page-specific rules go in a second `<style>` after the marker, never inside the injected one. Load Inter with a `<link>` in `<head>` as `COMPONENTS.md` shows, and inline the SVG assets from `brand/assets/` rather than linking them.

Use the components as documented: wrap content in `.wrap`, take sizes from the `--text-*` tokens, keep the graphic element top-right and behind the content, and run the checklist in `COMPONENTS.md` before delivering.

## Other outputs

For anything that is not HTML, `BRAND.md` is the whole brief: palette in HEX for digital and Pantone or CMYK for print, Inter with Arial as the fallback, the logo rules, the graphic element rules, and the format notes. Take every value from `brand/tokens.css` and every rule from `BRAND.md`, and run the Application Checklist at the end of `BRAND.md` before delivering.

## Icons

`python3 <this skill dir>/components/icons/icon.py <slug>` emits an inline Lucide icon, fetched on demand. If the fetch fails, leave the icon out; it is never the only signal.

## Files

- `brand/`: `BRAND.md`, `tokens.css`, `DEVIATIONS.md`, `palette.py`, `assets/`.
- `components/`: `COMPONENTS.md`, `assemble.py`, `base/`, `charts/`, `icons/`.
