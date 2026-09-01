---
name: apply-branding
description: Apply the Aperia brand to anything that is not a report or a slide deck, or create something new in the Aperia brand from scratch. Use whenever the user wants Aperia branding on any output, including phrasings like "make this on-brand", "apply the Aperia brand", "Aperia colors", "Aperia style", "brand this page", or requests to build a landing page, email, dashboard, diagram, form, graphic, or any other artifact in the Aperia look and feel. Loads the shared brand layer (palette, typography, logo rules, graphic element) and lets you build the output freely on top of it. Use create-report instead for a long-form HTML report, and create-slides instead for a presentation; this skill covers everything else.
---

# Apply Aperia Branding

Loads the Aperia brand layer so any output you build carries the brand
correctly. This skill has no output format of its own: read the brand layer,
then build whatever the user asked for on top of it.

## Step 1: Read the brand layer (required)

Before producing anything:

1. Read **`../../brand/BRAND.md`** in full: palette, typography, logo rules,
   the parallelogram graphic element, and the Application Checklist.
2. Read **`../../brand/tokens.css`** for the palette, the type scale and the
   weights. It is the only token file; parse the custom properties if the output
   needs the values programmatically.
3. Brand assets live in **`../../brand/assets/`**: `aperia-logo.svg`,
   `pattern-single.svg` (landscape tile), `pattern-single-portrait.svg`
   (full-bleed portrait), `pattern-double.svg`.

**Do not work from memory of the palette or the type rules.** If a value is not
in `BRAND.md` or the token files, it is not an Aperia value. Do not invent one.
Sanctioned exceptions are recorded in `../../brand/DEVIATIONS.md`; do not add
new ones from this skill.

## Step 2: Build what was asked

There is no template here. Apply the brand rules from `BRAND.md` to the
artifact the user wants, whatever its format. Typography is Inter with an Arial
fallback. Use the token values verbatim, embed assets rather than linking out
when the output must be self-contained, and follow the guideline's rules for
logo clearspace and the graphic element.

## Hand off when a sibling skill fits better

- A long-form, sectioned HTML document (report, briefing, review, proposal):
  use the **create-report** skill. It carries the full report theme and
  component library.
- A presentation (slides, deck, readout): use the **create-slides** skill. It
  builds a self-contained HTML deck that prints to a 16:9 PDF.

Both already load the brand layer themselves; do not combine this skill with
them.

## Before you finish

- [ ] `BRAND.md` was read this session, with no palette or type values from memory
- [ ] Every color and font in the output traces to `BRAND.md`, the token files,
      or a recorded deviation
- [ ] The guideline's Application Checklist in `BRAND.md` passes for the output
