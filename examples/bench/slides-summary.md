# create-slides benchmark: 0.8.0 (old) against 0.9.0 (new)

Prompt: `prompt-slides.md`, identical `source.md` in both run folders. Model opus, effort medium, same allowed tools. Runs were sequential, old first.

## Side by side

| Measure | old (0.8.0) | new (0.9.0) |
| --- | --- | --- |
| Wall seconds (date stamps) | 270 | 229 |
| duration_ms | 266965 | 226405 |
| duration_api_ms | 247936 | 207490 |
| num_turns | 19 | 16 |
| total_cost_usd | 1.9685 | 1.5965 |
| is_error | false | false |
| permission_denials | [] | [] |
| stderr.log | empty (0 bytes) | empty (0 bytes) |
| usage.input_tokens | 28 | 24 |
| usage.cache_creation_input_tokens | 93740 | 78720 |
| usage.cache_read_input_tokens | 992768 | 699559 |
| usage.output_tokens | 21382 | 18377 |
| readout.html size | 59.6 KB | 59.8 KB |
| `<style` literal occurrences | 3 | 3 |
| actual `<style>` elements | 1 | 1 |
| marker block filled with CSS | yes, 37114 chars inside `<style data-aperia="slides">` | yes, 37431 chars inside `<style data-aperia="slides">` |
| assemble.py path named in injected header | `ui-components/assemble.py` | `apply-branding/components/assemble.py` |
| slide count | 16 (`article.slide` inside 16 `section.stage`) | 16 |
| dark / light | 9 / 7 | 9 / 7 |
| comparison table | 1 `.cmp-table` | 1 `.cmp-table` |
| stat row | 1 `.s-numbers` slide with 3 `.stat-card` | 1 `.s-numbers` slide with 3 `.stat-card` |
| prompt sections present | all four, each behind a divider | all four, each behind a divider |
| speaker notes | 16 `aside.notes` | 16 `aside.notes` |
| inline SVG total | 24 | 24 |
| Lucide content icons | 3 (`syringe`, `palette`, `shield-check`, bundled `lucide-icons.json`) | 3 (`file-code`, `palette`, `shield-check`, fetched by `scripts/icon.py`) |
| `lucide` string in html class or data attributes | 0 | 0 |
| hex colors outside the injected block | `002F67`, `004583`, `0072BC` | `002F67`, `004583`, `0072BC` |
| off-palette values | none | none |
| QA script result | `16 slides, 9 dark, 7 light. Clean.` exit 0 | `16 slides, 9 dark, 7 light. Clean.` exit 0 |
| body word count | 906 | 926 |
| SKILL.md size read by the run | 483 lines, 23916 bytes | 181 lines, 12499 bytes |

Palette read from `new/plugins/aperia/skills/apply-branding/brand/palette.py`: 42 values (tokens.css plus the approved DEVIATIONS.md blocks).

## Slide titles in order

| # | old | new |
| --- | --- | --- |
| 1 | Toolkit 0.8.0 One Source For Every Value | Toolkit 0.8.0 One Source For Style, One Source For The Palette |
| 2 | What We Will Cover | What We Will Cover |
| 3 | Summary (divider 01/04) | Summary (divider 01/04) |
| 4 | Every Value Has One Home | What 0.8.0 Removed (stat row) |
| 5 | The Release In Three Numbers (stat row) | Three Things Changed At Once |
| 6 | What Changed (divider 02/04) | What Changed (divider 02/04) |
| 7 | Three Moves | How A Document Gets Its Styles Now |
| 8 | The Text Caught Up With The Code | Where Each Value Lives (comparison table) |
| 9 | Mark, Assemble, Verify | Shipped Styles Now Follow The Rules |
| 10 | 0.7.0 Against 0.8.0 (comparison table) | A Rule We Do Not Enforce On Ourselves Is A Suggestion. |
| 11 | A Value Lives In One File, Or It Drifts. | Verification (divider 03/04) |
| 12 | Verification (divider 03/04) | What The Validator Now Catches |
| 13 | What The Checker Now Fails | The Release Documented Itself |
| 14 | Next Steps (divider 04/04) | Next Steps (divider 04/04) |
| 15 | What This Asks Of Maintainers | What This Asks Of Us |
| 16 | Questions | Questions |

## Layout classes used

| class | old | new |
| --- | --- | --- |
| s-light s-text | 6 | 5 |
| s-dark s-section | 4 | 4 |
| s-light s-icons | 1 | 1 |
| s-light s-two-col | 0 | 1 |
| s-dark s-statement | 1 | 0 |
| s-dark flat s-text | 0 | 1 |
| s-dark flat s-numbers | 1 | 1 |
| s-dark s-cover / s-agenda / s-end | 1 each | 1 each |

Components in both: one `.cmp-table`, one `.flow` with 4 steps, one `.callout`, one `.g3` icon block. New also used `.g2` / `.g2-a`.

## Comparison table content

old, columns Concern / 0.7.0 / 0.8.0:
- Stylesheet delivery: Pasted by the model, Injected by the script
- Palette source: Restated in slides.css, Read from tokens.css
- Font loading: An import and a link, One link in head
- Off-token values: Documented only, Failed by validate.py

new, columns Concern / Through 0.7.0 / In 0.8.0:
- Theme CSS: Pasted into each document, Injected into the marker
- Palette hexes: Restated in slides.css, Read from tokens.css
- Palette for scripts: Hardcoded in qa.py, Shared brand/palette.py
- Inter font: Imported by tokens.css, One link in the head

## QA script output

Both scripts were run read-only against the matching deck.

old, `old/.../create-slides/scripts/qa.py readout.html`:

    Aperia slide QA, readout.html
    16 slides · 9 dark · 7 light

    Clean. Now open it in a browser and look at every slide.

exit 0.

new, `new/.../create-slides/scripts/qa.py readout.html`: identical text, exit 0.

## result field, first 600 chars

old:

    Done. `readout.html` is in this folder, assembled and passing QA clean.

    **Deck**: 16 slides, 9 dark / 7 light.
    - Cover, agenda, four section dividers (01–04), a statement pivot, closing.
    - Summary: light bullets + a dark `s-numbers` stat row (90 KB, 4 new checks, 26 literals) with its insight line.
    - What changed: `.g3` icon blocks (Inject / Consolidate / Enforce), docs-cleanup bullets, a `.flow` for the new build sequence (Mark, Assemble, Verify, Repeat), and a `.cmp-table` of 0.7.0 against 0.8.0 with the 0.8.0 column highlighted.
    - Verification: what `validate.py` now fails, plus a callout

new:

    `readout.html` written and assembled; `qa.py` reports clean (16 slides, 9 dark / 7 light, no errors or warnings).

    Path: /private/tmp/claude-501/-Users-thuannguyen-Documents-code-aperia-skills/e6298f6f-521d-47fa-bed1-2d6baa60e4df/scratchpad/bench/runs/slides-new/readout.html
    Keys: arrows or space to move, `O` overview, `N` notes, `F` full screen, Ctrl/Cmd+P for a 16:9 PDF.

    Structure: cover, agenda, then the four sections you asked for, each behind a divider. Summary carries the stat row (90 KB of hand-copied CSS per output, 26 white literals, 4 new validator checks) plus a bullet slide. Wha

## Observations

- Both runs completed with no error, no permission denial and an empty stderr.log. Neither asked a question or waited for approval, as the prompt required.
- The new run cost 19 percent less (1.60 against 1.97 USD), took 41 fewer wall seconds, used 3 fewer turns, and read 293k fewer cached input tokens. The new SKILL.md is 12499 bytes against 23916, roughly half, which is the most likely cause of the token and turn drop.
- Output quality is close to equal on every checkable dimension: 16 slides both, same dark/light split, all four requested sections present behind dividers, one comparison table and one stat row in each, 16 speaker-note blocks in each, no off-palette color, both QA scripts clean.
- Both decks got the theme injected into the `<style data-aperia="slides">` marker rather than pasted by hand, and neither added a second `<style>` element. The injected header names the moved path in the new run, `apply-branding/components/assemble.py` against `ui-components/assemble.py`, which confirms the 0.9.0 relocation of the components layer took effect.
- Icon sourcing changed: 0.8.0 read a bundled `ui-components/icons/lucide-icons.json` with 2,025 icons, 0.9.0 has no bundled JSON and `scripts/icon.py` fetches from the Lucide CDN on demand. The fetch worked here; both decks ended with 3 icons in identical markup shape, so the change is invisible in the output but adds a network dependency. Neither deck tags its icons with a `lucide` class or data attribute, so they are only identifiable as Lucide by path data.
- Defect in the new deck: all 10 footer logos and the `.s-numbers` logo are emitted as `<svg class="logo" viewBox="0 0 135 40">` with no `aria-label="Aperia"`. The old deck has the label on all 11. Both snippet files carry two logo variants, one labeled and one bare, so this is a pick from the ambiguous source rather than a change in 0.9.0, but the new run picked the unlabeled one everywhere. Neither QA script flags it.
- Component coverage differs slightly. The old deck used `s-statement` for its pivot slide; the new deck wrote the same kind of pivot line as a `s-dark flat s-text` slide, so `s-statement` went unused. The new deck used `s-two-col` and a `.g2` grid, which the old deck did not.
- Both decks left `<span class="s-num"></span>` empty in markup, filled by the single inline script at runtime. Same in both, not a regression.
- Content differences are editorial rather than structural. The new deck leads with the palette consolidation and gives verification two slides; the old deck leads with the single-source framing and gives verification one. The new comparison table includes the `qa.py` palette hardcoding row, which the old table does not.
- Both final messages flagged the same open item honestly: the deck was QA'd by script but not viewed in a browser. The new message also flagged that the source has no next-steps content, so those four cards are derived.
