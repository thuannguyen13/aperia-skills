# Known deviations from Aperia Brand Guidelines v1.0

Audit of every hex value in this plugin against the palette in `BRAND.md`.
Re-run `python3 scripts/validate.py` from the repo root after any theme edit.

This file doubles as the allowlist for that check, but **only through the
`approved` blocks**. The script reads the fenced ```approved blocks below and
nothing else, so a hex that appears in prose, in a table of what a value used to
be, or in a paragraph explaining why something was removed does **not** pass.
Approving a value means adding it to an `approved` block, deliberately.

Keep those blocks accurate: a value in use and not listed fails the build, and a
value listed but no longer used should be deleted along with its narrative.

Status as of plugin v3.0.0.

---

## 1. Asset / guideline mismatch, needs a decision from the brand owner

The supplied graphic-element SVGs use a gradient stop that is **not** the Dark Blue in
the guideline table:

| Where | Value in file | Value in `BRAND.md` | Delta |
|---|---|---|---|
| `assets/pattern-single.svg`, `assets/pattern-double.svg` | `#004583`, rgb(0,69,131) | Dark Blue `#004785`, rgb(0,71,133) | 2 points on G and B |

They are visually indistinguishable, so this is almost certainly a transcription
difference between the artwork and the written spec rather than an intentional third
blue. **Not auto-corrected**, because the artwork is the artwork, and changing brand
assets is the brand owner's call, not a build step.

Resolve it one way or the other, then delete this section:

- If the guideline table is authoritative → update the two SVGs to `#004785`.
- If the artwork is authoritative → correct the Dark Blue row in `BRAND.md`.

`snippets.html` reproduces the same stops, so whichever way it goes, update it too.

**Approved provisionally.** The value is in the shipped artwork, so failing the
build on it would block every release without moving the decision forward. It
stays approved until the brand owner rules, and this section stays open.

```approved
#004583   graphic-element gradient stop, in the supplied SVGs
```

---

## 2. Resolved: series 4 and 5 remapped to palette

`../ui-components/styles.css` and `../ui-components/snippets.html` were inherited from the earlier
standalone report skill and carried two off-palette blues in the 4th and 5th chart
series positions.

| Was | Now | Notes |
|---|---|---|
| `#3A8FD1` (`.tline-bar.b4`, `.gantt-bar.b4`, 4th `.flow-node`, gantt dot) | Sky Blue `#7ED3F7` | Text flipped from `#FFF` to Aperia Blue. White on Sky Blue is 1.67:1 and fails; Aperia Blue on Sky Blue is 7.83:1 and is a listed approved pair |
| `#5FA9D8` (5th stacked segment) | Light Blue `#C8EAF5` | Same text flip, 10.32:1 |

This now matches the `--series-1` to `--series-7` order in `tokens.css`.

**No `approved` block, deliberately.** Both values above are history. `#5FA9D8` is
used nowhere and must stay that way. `#3A8FD1` is still in the deck theme and is
approved there, in section 5, on its own merits. Naming a value in a "was" column
no longer approves it, which is the hole this structure closes.

---

## 3. Accepted: semantic status colors

`BRAND.md` permits red / amber / green "for genuine semantic status, kept minimal."
These appear only in `.callout` and badge variants signalling problem / caution /
positive, never as decoration or chart series:

```approved
#DC2626   critical type      #FEF2F2   critical fill      #FECACA   critical border
#D97706   warning bar        #B45309   warning type       #FFFBEB   warning fill
#FDE68A   warning border
#16A34A   positive bar       #15803D   positive type      #F0FDF4   positive fill
#BBF7D0   positive border
```

No action needed. Do not add new values to this set, and do not use these as
chart series colors.

**Extending the role, rather than the set.** A component may need one of these
values somewhere other than a callout or a badge. That is allowed, but it is not
silent: reuse the existing hex, do not invent a variant, and record the wider use
as a new numbered section explaining what the component needed and why the core
palette could not supply it. Section 7 is the worked example, and the mapping it
records is the one to reuse rather than deriving a second answer.

---

## 4. Open: light blue-grey tints in the report theme

The report theme uses a family of light blue-grey tints for card fills, table
highlights, badge backgrounds, and borders that are **not** in the guideline palette:

```approved
#EAF3FB   surface fill       #EAFAFF   surface fill       #F4F8FC   surface fill
#F6FAFE   surface fill       #EEF5FC   surface fill       #E6EEF6   surface fill
#BFDCF0   border             #C3D8EC   border             #E3E6EA   border
#B9CDE2   muted type on dark #DCE8F3   muted type on dark
#CFE0F0   muted type on dark #9FBEDB   muted type on dark
#1C1F24   near-black body type
```

The guideline offers Light Blue `#C8EAF5` and Light Gray `#F1F2F2` for this job, but
collapsing eleven values into two would flatten the component hierarchy the theme
depends on: surfaces, borders, and muted-on-dark type would all become the same color.

**This is a design decision, not a find-and-replace**, so it has been left as-is and
recorded here rather than silently changed.

Two ways to close it, both requiring the brand owner:

1. **Extend the guideline** with a sanctioned tint ramp derived from Aperia Blue.
   This is the honest fix, since the theme demonstrably needs the steps.
2. **Reduce to palette.** Map surfaces to `#F1F2F2`, borders to `#A7A9AC` at low
   opacity, muted-on-dark to `#C8EAF5`, body type to `#000000`. Re-check contrast on
   every dark panel afterward.

Until then: the report theme and the deck theme both draw on this set. The deck
has a related and separate gap of its own, recorded in section 5.

---

## 5. Open: dark-slide chart ramp in the deck theme

Added with the HTML `deck` skill in v2.0.0.

On a light slide the chart series map cleanly onto `chartSeries` in
`tokens.css`. On a dark navy slide, Aperia Blue and Dark Blue are invisible
against the background, so `slides.css` shifts the whole ramp lighter. The
palette offers only three light-enough blues (Sapphire, Sky, Light Blue) and the
ramp needs five distinguishable steps, so two intermediates were invented:

| Value | Where | Role |
|---|---|---|
| `#3A8FD1` | `.s-dark .c2`, 4th `.flow-node` | Second step of the dark ramp |
| `#6CB0E0` | `.s-dark .c5`, 5th `.flow-node` | Fifth step of the dark ramp |

Two more values sit outside the palette for reasons unrelated to charts:

| Value | Where | Role |
|---|---|---|
| `#A8C4DD` | `.s-dark` muted copy, agenda counters, donut and gantt labels | Muted type on dark. Light Blue is too bright to read as secondary |
| `#0A1E38` | `.ui-notes` | Presenter-notes panel. Deck chrome, never printed and never part of a slide face |

```approved
#3A8FD1   dark ramp, second step   #6CB0E0   dark ramp, fifth step
#A8C4DD   muted type on dark       #0A1E38   presenter-notes panel
```

This is the same shape of problem as section 4: the guideline palette does not
carry enough steps for the component hierarchy, and collapsing the five dark
series into the three available blues would make adjacent series
indistinguishable. **Left as-is and recorded rather than silently remapped.**

Closing it needs the same brand-owner decision as section 4, and ideally the
same answer, since a sanctioned tint ramp derived from Aperia Blue would serve
both the report tints and this dark chart ramp.

## 6. Accepted: PowerPoint template accent alternates

`skills/create-slides/SKILL.md` documents a conditional swap for the case where an HTML
deck is shown alongside one built on the official Aperia PowerPoint template,
which ships two slightly different accents:

| Guideline | Template alternate |
|---|---|
| Sapphire Blue `#0072BC` | `#1570E0` |
| Sky Blue `#7ED3F7` | `#25B4F1` |

The skill instructs the model to ask before applying it and to keep the
guideline values otherwise, so these are documented alternates rather than
values in a theme.

**Approved.** They are not used in any stylesheet, but they are written into a
shipped `SKILL.md`, so the scan sees them and they need an entry. Approving them
here records that the appearance is deliberate.

```approved
#1570E0   PowerPoint template accent, Sapphire Blue alternate
#25B4F1   PowerPoint template accent, Sky Blue alternate
```

---

## 7. Accepted: delivery-plan status ramp and environment chain

Added with the `create-report` skill's delivery-plan components in v3.0.0: the grouped
Gantt, milestone cards and the environment chain need a four-state status ramp
and five environment colors. The guideline palette has neither.

**No new hex values were introduced.** Every value below is either a core
palette color or one of the semantic status colors already accepted in section 3.

### Status ramp

| State | Bar / border | Type | Background | Border | Source |
|---|---|---|---|---|---|
| Done | `#16A34A` | `#15803D` | `#F0FDF4` | `#BBF7D0` | Section 3 green |
| In progress | Sapphire Blue `#0072BC` | Sapphire Blue | `#EAF3FB` | `#BFDCF0` | Core palette + section 4 tints |
| Planned | Medium Gray `#A7A9AC` | Dark Gray `#58595B` | Light Gray `#F1F2F2` | `#E3E6EA` | Neutral palette + section 4 |
| At risk | `#D97706` | `#B45309` | `#FFFBEB` | `#FDE68A` | Section 3 amber |

Blue is the working state and gray is the inert one, so the two states that
carry most of the rows stay on-palette. Green and amber are reserved for the
two states that are genuinely a status signal: finished, and at risk.

### Environment chain

| Environment | Value | Source |
|---|---|---|
| DEV | Sapphire Blue `#0072BC` | Core palette |
| QA | Dark Blue `#004785` | Core palette |
| UAT | Aperia Blue `#002F67` | Core palette |
| STAG | `#B45309` | Section 3 amber |
| PROD | `#15803D` | Section 3 green |

The promotion path darkens through the three core blues, then switches to the
semantic pair at the point where the environment starts carrying production
data: amber for the staging window, green for live. Color is never the only
signal on these cards; each one also carries a step number and the environment
name.

### Why this is still recorded as a deviation

Section 3 holds the set itself closed: no new values, and none of them as a
chart series color. Neither line is broken here. What is wider is the role. The
values appear on Gantt bars, milestone card borders and environment cards, not
only in callouts and badges. Section 3 asks for exactly that to be written down
as its own section, which is what this is.

The alternative is a status ramp built only from the five core blues. It was
rejected because "done" and "at risk" would then be two blues, which is the one
distinction a reader of a delivery plan has to make at a glance. Sky Blue and
Light Blue also fail contrast as type or as small bars on white.

Closing this properly needs the same brand-owner decision as sections 4 and 5:
a sanctioned status ramp in the guideline. Until then the mapping above is the
one to reuse, so a second report does not invent a third answer.

**No `approved` block.** This section introduces no value of its own: every hex it
maps is either core palette or already approved in section 3.

**Opacities, not new hexes.** Shaded release-stage columns use
`rgba(0,47,103,.035)` and focus rings use `rgba(0,114,188,.16)`: opacities of
Aperia Blue and Sapphire Blue over white, the same technique the theme already
uses for shadows. They composite to a value not in the palette but introduce no
new hex literal.
