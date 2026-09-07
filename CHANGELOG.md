# Changelog

## 0.9.1

Fixes from a Claude Desktop run of both skills.

- The deck line chart takes five series. `slides.css` defined `ln1` and `ln2` only; a run with three channels wrote its own CSS once and dropped a channel once. A series is now `<g class="ln lnN">` holding its polyline, dots, labels and name, colored through `currentColor` in the ramp order the bars use, with dark-slide remaps. A bare `polyline.ln1` from an older deck still renders.
- The line chart snippet is drawn in its own box. It declared a 1350 by 390 viewBox and plotted every point in 900 by 260 coordinates, so the example filled the top-left two thirds. Rewritten at canvas scale with two series.
- `qa.py` counts table body cells at half weight. Cells counted as prose, so any real comparison table tripped the 55-word warning and a run shortened "24 months" to "24m" to pass.
- `icon.py` tries a second host, unpkg after jsdelivr, and reads from `APERIA_ICONS_DIR` when set to a folder of Lucide SVGs. jsdelivr is blocked in some sandboxes, which left `.iblock` unusable there.
- New `create-report/scripts/qa.py`, following the slides script: assembled marker naming only the toolkits in use, sprite, skip link, nav links resolving, drawer after nav, footer, section labels, palette, duplicate ids, placeholders, dashes, classes no stylesheet defines, one of `gantt` or `sgantt`, no hand-added `full` or `max-height` on the plan block, `DATA` present when a plan is mounted, no `transform:scale`. Both bench runs and the Desktop run improvised these checks.
- `swatch-grid` removed from the base layer. It laid out named colors with hex values, which no report or deck in this toolkit needs; no skill named it and no run used it.
- The report wordmark is one `#ap-logo` sprite referenced by `<use>`, as the deck already did, instead of the path data pasted in the nav and again in the footer. The stylesheet sets its color per surface.

## 0.9.0

- `brand/` and `components/` moved into a third skill, `apply-branding`. Desktop mounts only folders under `skills/` that have a `SKILL.md`, so layers at the plugin root never arrived. Broken since 0.3.0. The other skills read them as `../apply-branding/`. `bundle-skills.py` and `dist/` are gone.
- `apply-branding` is a skill again, for anything that is not a report or a deck. New `page` recipe in `assemble.py`: tokens and base components, optional charts and icons, no theme.
- Icons are fetched, not bundled. `icons/icon.py` pulls from the Lucide CDN on first use, pinned to 1.41.0, and caches. The 430 KB JSON is gone. The slides copy is now a thin wrapper.
- Every `SKILL.md` carries `metadata.version`, checked against `plugin.json`.
- `qa.py` and the slides icon wrapper name the missing skill instead of failing on an import.
- Snippet libraries split by group: `base/` becomes `structure`, `emphasis`, `tables`, `charts`, `timelines`; `charts/` becomes `trend`, `compare`, `proportion`, `intensity`. Both `index.html` files are gone.
- Every component section renamed to a short, distinct name (`Ranked Bars`, `Effort Bars`, `Estimate Range`). Caveats moved from the name to a note under it. No CSS class renamed.
- Both toolkit tables in `COMPONENTS.md` gain a **File** column naming where each component's markup lives, replacing the `**(charts/)**` suffix.
- `.gantt-bar` and `.tline-bar` gain `b5` to `b7`, completing the seven-step series ramp. Dark text on the light fills.
- `.hm-grid` reads `var(--hm-labelw, 56px)` instead of a hardcoded gutter, so a heatmap with word labels needs no override.
- Column-chart bars sit on their baseline. `.col-lbl` carried a `margin-top` that pushed the axis rule 21px below the bars.
- New `scripts/gallery.py` renders the snippet libraries as one labelled page, assembled with the real layers. Maintainer tool, outside `plugins/`.
- `dist/` removed, and `examples/` now holds only `bench/`: one run of each skill per plugin version, 0.8.0 against 0.9.0, with the Claude Code meters and the transcript write-ups. The sample report was built against the old component names; `gallery.py` replaces it.
- De-duplicated: the nine snippet files carried an identical header restating `COMPONENTS.md` and `charts/styles.css`, now a pointer; the per-file component lists in `COMPONENTS.md` and the chart-family list in `create-report/SKILL.md` duplicated the File column and are gone; `gallery.py` globs the snippet files instead of listing them. New validate check 11 fails if the File column and the files on disk drift apart.
- `ui-components/` renamed to `components/`. The folder and its doc now share a name, matching `brand/BRAND.md`.
- `apply-branding` carries `user-invocable: false`. It stays available to the model for freeform branding but no longer appears in the user's skill picker, where it read as a third document type rather than the layer holder.
- Every `SKILL.md` opens with the same "What to read" rule in three parts: Always, Only if picked, Never. Stylesheets sit under Never, since `assemble.py` injects them. New validate check 12 fails a read rule that names a file that does not exist, puts a stylesheet under Always or Only if, or a snippet under Never.
- `apply-branding` gains `references/page.html`, the document skeleton for the `page` recipe, following the skeleton the deck ships. `SKILL.md` is a read rule, a routing rule, a four-step workflow and the non-HTML case; rules that `BRAND.md` and `COMPONENTS.md` already carry are not restated.
- The grouped Gantt decides its own width. `--sg-colw` was defined but never applied, so the "5 or more columns needs `wrap full`" rule in `create-report` was arithmetic the CSS did not enforce. Columns now carry it as a minimum, the plan block sits in its own `.wrap`, and `syncScrollbox()` adds `.full` to that `.wrap` when the grid does not fit, then `.scrolls` when it still does not. The skill no longer states the threshold.
- The skills no longer restate values a stylesheet or script owns (nav height, bar height, wrap width, the sgantt tokens, the slide floor, the print page, the `qa.py` word limits). They name the token or the script instead. New validate check 13 fails any backticked path in any markdown file under the plugin that does not resolve.
- Fixes from the 0.9.0 bench transcripts. Every footer logo in the slides snippets carries `aria-label="Aperia"`; the worked examples had dropped it while the fragment kept it, and a run copying the examples shipped ten unlabeled logos. `qa.py` now fails an unlabeled logo. The numbers and chart slides moved from `create-slides/references/snippets.html` into `references/charts.html`, read only when a slide needs one; the single file was 32 KB, over the Bash output cap, so every run read it twice. `code` is styled in `base/styles.css`, `slides.css` and the report theme, Inter Medium on a muted chip; no layer had a rule, and a run wrote its own. The `interactive.html` read condition names the components that need it instead of "a delivery, release or roadmap plan", which a release readout met without needing the file. `tokens.css` is under Never in `create-slides` with the reason. Both skills say what to report when no browser is available instead of claiming the file prints; a run spent two calls hunting for Chrome.
- Stale references removed: the `<plugin dir>` assemble path and the pre-0.9.0 file names in `create-report`, the `next`/`goal` milestone classes that no CSS defines, the `python-pptx` conversion lines in `BRAND.md`, the two-skill wording in `create-slides`, the `/aperia:apply-branding` command in the README, and the old `plugins/aperia/brand/` paths in `MAINTAINING.md`. `BRAND.md` now lists `pattern-single-portrait.svg` and `palette.py`.

## 0.8.0

- **Styles are injected, not typed.** New `ui-components/assemble.py` fills a document's style marker (`<style>/* @aperia report charts icons */</style>` or `/* @aperia slides */`) with the layer files in order, byte for byte, and replaces its own block on re-run. Both skills stop telling the model to read and paste stylesheets; document-specific rules go in a second `<style>` after the marker. Makes the copy guaranteed instead of left to the model. One measured run in Claude Code showed no cost or time gain, because the model was already concatenating the files with the shell; see examples/bench.
- **The palette has one source again.** `slides.css` reads `tokens.css` instead of restating the ten hexes and the type ramp; its canvas radii are recorded overrides. `qa.py` reads the palette through the new `brand/palette.py`, which `validate.py` shares, instead of a hardcoded set. Check 6 now covers `skills/` too.
- **Shipped CSS follows its own rules.** Six chart label sizes at 10px and 11px moved onto the `--text-*` ramp. New `--radius-sm` (4px, 7.5 canvas units in decks) replaces every small literal radius. `tokens.css` sets body in Regular, matching what every theme already did; recorded as `DEVIATIONS.md` section 9.
- `validate.py`: the palette check now sees three-digit hex and `rgb()`/`rgba()`; new checks fail raw px `font-size`, off-token `border-radius`, skill descriptions under 80 characters, and any em dash. The 26 `#fff` literals became `var(--white)`.
- `tokens.css` no longer `@import`s Inter; the `<link>` in `<head>` is the one place the font loads.
- Stale text fixed: version stamps and `chartSeries` in `DEVIATIONS.md`, `deck`/`report` skill names in `BRAND.md`, "three skills" and "720px" in the slides skill, and `MAINTAINING.md`'s edit order, which 0.7.0 had inverted.
- Skill descriptions rewritten to two or three sentences that name the output and, for slides, that PowerPoint is not one.
- Every em dash in the docs, comments and snippets replaced. `.prettierrc` committed alongside the existing `.prettierignore`.
- `examples/toolkit-0-8-0-release.html`: this release written up with `create-report`, assembled by the script from a bare marker. The assemble script refuses a layer file containing a closing style tag, which the browser would treat as the end of the block even inside a comment.

## 0.7.0

- **`BRAND.md` no longer states any value `tokens.css` owns.** Its palette tables listed the HEX and RGB for all 10 colors and its type scale listed all 20 size and leading numbers, every one of them a second copy. The tables now name the token instead and keep what a stylesheet cannot carry: Pantone, CMYK and the role each color plays. The type scale keeps its rules and drops its numbers. `#FFFFFF` in the logo rule, `600` in the weight rule and the four `12px` mentions of the on-screen floor all became token names too.
- `validate.py` check 7 is inverted to match: it used to compare the guideline's copy against the tokens, and now fails on any hex in `BRAND.md` at all, plus on any token the guideline names that `tokens.css` does not define. Comparing copies was treating the symptom.

## 0.6.0

- **`tokens.css` is one file again, with provenance marked inside it.** The 0.5.0 split into `colors.css` / `typography.css` / `shape.css` is reversed: 98 lines across three files was structure without payoff, and a consumer that pasted two of three got undefined radii with nothing to catch it. The file now opens with the rule that governs it: a GUIDELINE section for values Aperia Brand Guidelines v1.0 states, and a SYSTEM section, kept separate, for scales the guideline is silent on. All 57 tokens carry over unchanged.
- **`DEVIATIONS.md` gains section 8**, the policy for those system scales: spacing, elevation and motion are derived from what the components already do, not signed off by the brand owner, and each lands with a record of what it changed. No scale is defined yet.
- `validate.py` gains check 7: every color `BRAND.md` names in a palette table must be defined under the matching token name with the same value, so the guideline and the tokens cannot drift apart.

## 0.5.0

- **The brand layer is one file per primitive.** `tokens.css` is split into `colors.css` (palette, semantic aliases, gradients, the seven chart series steps), `typography.css` (font stack, weights, the ten size/leading steps, the guideline element defaults, the Inter `@import`) and `shape.css` (the two radii). A consumer pastes all three, in that order. All 57 tokens carry over with no value changed and nothing defined twice.
- **The component layer stopped repeating brand values.** `base/styles.css` had redefined 32 of them, the palette, both type ramps and the radii, and `COMPONENTS.md` told you to paste it second so it would win. Those definitions are gone; it now reads the brand files. `--fg` is the one deliberate override left, near-black body ink over Aperia Blue, already recorded in `DEVIATIONS.md` section 4.
- `validate.py` gains check 6: a token defined in both layers fails unless it is listed in `OVERRIDES` with a reason. Scoped to `ui-components`, since `create-slides` still keeps its own palette copy.
- Added `.prettierignore` for `brand/`, `ui-components/` and the skills' `references/`. Those files are pasted verbatim into every output, so reformatting them quadruples what ships.

## 0.4.0

- **`ui-components/` is grouped into one folder per toolkit.** `base/`, `charts/` and `icons/`, each holding a `styles.css` and an `index.html`, so a file no longer repeats the name of the folder it sits in. `icons/` is self-contained: `icon.py` and `lucide-icons.json` moved in beside the CSS, and the layer's top-level `scripts/` and `assets/` folders are gone. Every reference in both skills, `COMPONENTS.md` and `MAINTAINING.md` moved with them.
- `bundle-skills.py` now resolves `os.path.join` paths too, not just slash-style ones. The icon script's path to the shared JSON is built that way, so moving the asset had broken it silently.

## 0.3.0

- **Removed the `apply-branding` and `apply-ui-components` skills.** The plugin now ships two skills, `create-report` and `create-slides`.
- **`apply-ui-components`'s component library moved out of `skills/` into a new top-level reference folder, `plugins/aperia/ui-components/`**, `styles.css`, `snippets.html`, `charts.css`/`charts.html`, `icons.css`/`icons.html`, and a new `COMPONENTS.md` documenting all of it (the same role `brand/BRAND.md` plays for the brand layer). It is a sibling of `brand/`, not a skill: no frontmatter, nothing auto-invokes it. `create-report` reads it the same way it already read `brand/` (`../../ui-components/...`); `create-slides` keeps its own canvas-unit implementation but follows the same design language, documented in its own `SKILL.md`.
- **New build step, `scripts/bundle-skills.py`.** Builds one standalone bundle per skill in `dist/`, inlining the layers that skill reads and rewriting its references, so a skill uploaded on its own to Claude Desktop carries the same files a plugin install would have given it. Without it `create-report` cannot render outside a plugin install, since its base components now live in `ui-components/`. CI builds the bundles on every push and pull request, so a broken layer reference fails there instead of at upload time.
- Fixed two stale reference paths the bundle check surfaced: `brand/tokens.css` pointed at `../BRAND.md` for a file in its own directory, and `brand/DEVIATIONS.md` still named the component theme by its pre-refactor path.
- There is currently no skill for a freeform branding request that fits neither `create-report` nor `create-slides`, that was `apply-branding`'s job. See `MAINTAINING.md`, "Ad-hoc branding", if that need comes back.

## 0.2.0

- New skill: `apply-ui-components`. A paste-in library of the presentational components from the report theme, cards, badges, callouts, tables, milestone/status timelines (including a new `htimeline`, the horizontal form), a chart toolkit (bar/stacked/scenario/PERT plus the extended family: line, area, combo, scatter, bubble, grouped/stacked category bars, a constrained pie/donut, radial gauge, treemap, radar, funnel, sparkline, heatmap), and a 37-icon set extracted from a licensed Streamline Icon Set, for dropping into anything that isn't a full report or deck.
- `create-report` and `create-slides` now consume `apply-ui-components` as the shared base component layer instead of maintaining their own parallel copies, so a badge, a callout, or a chart series reads the same way across every Aperia surface. `create-report`'s own files are trimmed to what's actually unique to a full report: nav/hero/footer chrome, the phased-roadmap `phases` timeline, and the data-driven `sgantt` delivery-plan subsystem. `create-slides` keeps its own canvas-unit implementation (screen tokens don't translate to the deck's fixed 1920×1080 coordinate system) but now states and follows the same design language explicitly.

## 0.1.0

Initial beta release. Versions below 1.0.0 are beta.

- Three skills: `create-report`, `create-slides`, `apply-branding`.
- Shared brand layer in `plugins/aperia/brand/`: `BRAND.md`, `tokens.css`, `assets/`, `DEVIATIONS.md`. All skills read it at runtime.
- Validation via `scripts/validate.py` and CI: manifests, skill frontmatter, palette conformance, version bump on plugin changes.
