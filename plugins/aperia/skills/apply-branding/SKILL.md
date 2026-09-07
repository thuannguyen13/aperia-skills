---
name: apply-branding
description: Apply the Aperia brand to anything that is not a report or a slide deck, such as a landing page, an email, a dashboard, a diagram, a form, or a one-off graphic, or build one from scratch in the Aperia look. Holds the brand and component layers the other Aperia skills read.
user-invocable: false
metadata:
  version: "0.9.0"
---

# Apply Aperia Branding

## What to read

**Always.** `brand/BRAND.md` in full, then `components/COMPONENTS.md` in full.

**Only if picked.** The one snippet file the **File** column in `COMPONENTS.md` names for each component you chose. `components/icons/index.html` only if the artifact carries an icon. For an HTML artifact, `references/page.html`, the skeleton to start from.

**Never.** `components/base/styles.css`, `components/charts/styles.css`, `components/icons/styles.css`. `assemble.py` injects them; skim one only when a class's behaviour is unclear.

## When this is the wrong skill

- A long-form document the reader scrolls through is `create-report`.
- A presentation is `create-slides`.
- No PowerPoint, Word or Excel file is produced here. Say so.

Name the skill that fits and stop.

## Workflow

1. Read the user's content and pick each component from the tables in `COMPONENTS.md`.
2. Start from `references/page.html`. Its marker, `<style>/* @aperia page */</style>`, gets the word `charts` or `icons` added when those toolkits are used.
3. Run `python3 <this skill dir>/components/assemble.py <file.html>`, and again after any later edit.
4. Save as `<slug>.html` in the working directory unless the user names a location, and tell the user the path.

## Other outputs

For anything that is not HTML, `BRAND.md` is the brief and `brand/tokens.css` holds every value: HEX for digital, Pantone or CMYK for print. Read `tokens.css` only in this case; nothing injects the values there.
