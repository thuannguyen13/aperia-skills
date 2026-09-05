## 0.8.0

- **Styles are injected, not typed.** New `ui-components/assemble.py` fills a document's style marker (`<style>/* @aperia report charts icons */</style>` or `/* @aperia slides */`) with the layer files in order, byte for byte, and replaces its own block on re-run. Both skills stop telling the model to read and paste stylesheets; document-specific rules go in a second `<style>` after the marker. Cuts about 90 KB of hand-copied CSS per output and the drift that came with it.
- **The palette has one source again.** `slides.css` reads `tokens.css` instead of restating the ten hexes and the type ramp; its canvas radii are recorded overrides. `qa.py` reads the palette through the new `brand/palette.py`, which `validate.py` shares, instead of a hardcoded set. Check 6 now covers `skills/` too.
- **Shipped CSS follows its own rules.** Six chart label sizes at 10px and 11px moved onto the `--text-*` ramp. New `--radius-sm` (4px, 7.5 canvas units in decks) replaces every small literal radius. `tokens.css` sets body in Regular, matching what every theme already did; recorded as `DEVIATIONS.md` section 9.
- `validate.py`: the palette check now sees three-digit hex and `rgb()`/`rgba()`; new checks fail raw px `font-size`, off-token `border-radius`, skill descriptions under 80 characters, and any em dash. The 26 `#fff` literals became `var(--white)`.
- `tokens.css` no longer `@import`s Inter; the `<link>` in `<head>` is the one place the font loads.
- Stale text fixed: version stamps and `chartSeries` in `DEVIATIONS.md`, `deck`/`report` skill names in `BRAND.md`, "three skills" and "720px" in the slides skill, and `MAINTAINING.md`'s edit order, which 0.7.0 had inverted.
- Skill descriptions rewritten to two or three sentences that name the output and, for slides, that PowerPoint is not one.
- Every em dash in the docs, comments and snippets replaced. `.prettierrc` committed alongside the existing `.prettierignore`.
- `examples/toolkit-0-8-0-release.html`: this release written up with `create-report`, assembled by the script from a bare marker. The assemble script refuses a layer file containing a closing style tag, which the browser would treat as the end of the block even inside a comment.

