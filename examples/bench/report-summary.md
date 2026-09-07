# create-report benchmark: 0.8.0 (old) against 0.9.0 (new)

Both runs used the same prompt (`prompt-report.md`), the same `source.md`, `--model opus --effort medium`, and the tool allowlist `Read Write Edit Bash Glob Grep Skill`. Each ran once, sequentially, from its own run folder. Both finished with `is_error: false`, `subtype: success`, an empty `permission_denials` list, an empty `stderr.log`, and a `readout.html` on disk. Neither run was retried.

## Side by side

| Measure | old (0.8.0) | new (0.9.0) |
| --- | --- | --- |
| Wall seconds (date stamps) | 274 | 243 |
| duration_ms | 272081 | 240027 |
| duration_api_ms | 251513 | 220530 |
| num_turns | 17 | 16 |
| total_cost_usd | 2.152123 | 1.561487 |
| usage.input_tokens | 34 | 26 |
| usage.cache_creation_input_tokens | 101423 | 73672 |
| usage.cache_read_input_tokens | 1225396 | 722324 |
| usage.output_tokens | 21001 | 18539 |
| readout.html size | 104604 bytes, 102.2 KB | 104824 bytes, 102.4 KB |
| `<style` tags (real elements) | 2 | 2 |
| `<style` occurrences in raw text | 4 (2 elements, 2 mentions inside CSS comments) | 4 (2 elements, 2 mentions inside CSS comments) |
| `@aperia` marker block | `<style data-aperia="report">`, CSS follows the marker comment inside the same tag | `<style data-aperia="report">`, CSS follows the marker comment inside the same tag |
| Injected CSS in the marker block | 77274 chars, about 566 rule blocks | 78396 chars, about 572 rule blocks |
| Files named in the injected block | tokens.css (brand), styles.css (base), styles.css (references) | tokens.css (brand), styles.css (base), styles.css (references) |
| Assemble attribution | `data-aperia="report"` plus the comment "Assembled by ui-components/assemble.py" | `data-aperia="report"` plus the comment "Assembled by apply-branding/components/assemble.py" |
| Second document-specific style block | 412 chars, 2 rules (`code` styling) | 46 chars, 1 rule (`.sec-intro + .stat-row` spacing) |
| Distinct classes used in the body | 66 | 78 |
| Classes used but not defined in any style block | 0 | 0 |
| Tables | 3 (`cmp-table` once, `stack-table` twice) | 2 (`cmp-table` once, `stack-table` once) |
| Comparison table present | yes, `cmp-table` with `.hl` on the 0.8.0 column | yes, `cmp-table` across 8 mechanisms with `.hl` on the current column |
| Stat row present | yes, one `stat-row` with 4 `stat-card` | yes, one `stat-row` with 4 `stat-card` |
| Broken in-page anchors | 0 of 10 | 0 of 10 |
| Tag imbalance (non-void elements) | none | none |
| `<script>` blocks / inline `<svg>` | 1 / 5 | 1 / 5 |
| External dependencies | Google Fonts stylesheet plus 2 preconnect hints | Google Fonts stylesheet, no preconnect hints |
| Body word count | 1359 | 1417 |
| Em or en dashes in rendered text | 0 | 0 |
| Off-palette hex outside the injected style block | none | none |

Colors used outside the injected style block, both runs: `002F67`, `004583`, `0072BC`, `FFFFFF`. All four are in the palette loaded from `apply-branding/brand/palette.py` (42 values: `tokens.css` plus the approved deviations in `DEVIATIONS.md`). The old run's second style block adds one `rgba(255,255,255,...)` tint, which is `FFFFFF` and also in palette.

## Component families

Searched for the class-name families `stat`, `kpi`, `table`, `timeline`, `gantt`, `chart`, `callout`, `card`.

| Family | old | new |
| --- | --- | --- |
| stat | stat-row, stat-card, stat-val, stat-lbl | stat-row, stat-card, stat-val, stat-lbl |
| kpi | none | none |
| table | cmp-table, stack-table | cmp-table, stack-table |
| timeline | none | none |
| gantt | none | none |
| chart | none | none |
| callout | callout, callout-tag | callout, callout-tag |
| card | card, stat-card, outcome-card | card, stat-card |

Top 25 classes by frequency.

Old: badge 28, b-gray 16, layer-name 15, layer-tool 15, b-blue 10, hl 7, wrap 6, ic-ok 6, text-2xl 5, sec-label 4, sec-intro 4, stat-card 4, stat-val 4, stat-lbl 4, card 4, mb-3 4, callout 4, principle 4, num 4, ptext 4, pdesc 4, dp-col 3, dp-label 3, ic-mid 3, ic-no 3.

New: badge 20, b-gray 11, hl 9, ic-ok 8, layer-name 8, layer-tool 8, wrap 6, b-blue 6, text-2xl 5, ic-no 5, dlv 5, sec-label 4, sec-intro 4, stat-card 4, stat-val 4, stat-lbl 4, card 4, mb-3 4, flow-step 4, flow-rail 4, flow-node 4, flow-line 4, flow-body 4, flow-title 4, flow-desc 4.

Classes present in one run only. Old only: amber, num, outcome-card, outcome-from, outcome-grid, outcome-role, outcome-to, pdesc, principle, principles, ptext. New only: b-amber, delivs, dlv, flow, flow-body, flow-desc, flow-line, flow-node, flow-rail, flow-step, flow-title, p-body, p-desc, p-dot, p-duration, p-ind, p-item, p-line, p-name, pd-blue, pd-dark, pd-sapphire, phases. 55 classes are shared.

## Structure

Old headings in order:

- H1 Toolkit 0.8.0 / One Source For Styles And Palette
- H2 What This Release Is (id `summary`)
- H2 Changes By File (id `changed`)
- H2 How This Was Checked (id `verification`)
- H2 What Follows From 0.8.0 (id `next-steps`)
- H2 Confirm The 0.8.0 Follow-Through (CTA)
- H3 Styles Are Injected, Not Typed; The Palette Has One Source Again; Shipped CSS Follows Its Own Rules; The Docs Match The Code; The Shape Of The Change

New headings in order:

- H1 Toolkit 0.8.0 / Styles Are Injected, Not Typed
- H2 What 0.8.0 Is For (id `summary`)
- H2 0.7.0 Against 0.8.0 (id `changed`)
- H2 How The Release Was Checked (id `verification`)
- H2 What Follows 0.8.0 (id `next`)
- H2 Two Things To Confirm (CTA)
- H3 The Script Owns The CSS; One Palette, One Ramp; Shipped CSS Follows Its Own Rules; Stale Text Corrected; The Rule This Release Establishes

All four requested sections (summary, what changed, verification, next steps) are present in both, as H2 sections carrying the ids the nav links to. No requested section is missing in either run. Both carry a skip link to `#main`, a nav plus mobile drawer, a hero, and a footer.

## result field, first 600 chars

Old:

> `readout.html` written and assembled (104 KB, self-contained; Google Fonts is the only external dependency).
>
> **Structure**: nav + mobile drawer, hero, four sections matching the nav ids (`summary`, `changed`, `verification`, `next-steps`), footer.
>
> **Components used, all from the existing layers**: `stat-row` (4 numbers straight from the notes: ~90 KB, 26, 6, 4), `g2` card grid for the four release themes, `dark-panel` for the takeaway, `stack-table` for changes by file and again for the check list, `cmp-table` with `.hl` on the 0.8.0 column, `outcome-grid` for who feels the change, `principl

New:

> `readout.html` is written and assembled (76 KB of CSS injected by `assemble.py` from a bare marker).
>
> **Structure**: nav + drawer, gradient hero with `pattern-double`, four sections (Summary, What Changed, Verification, Next Steps), footer on Aperia Blue. Skip link present, nav links resolve to all four ids.
>
> **Components, all taken from the shared layer or this skill, nothing new invented**:
> - Summary: `stat-row` (~90 KB, 4 checks, 26 literals, 1 palette source) + 2×2 `card` grid with badges
> - What Changed: `cmp-table` 0.7.0 vs 0.8.0 across 8 mechanisms with the current column as `.hl`, then

## Observations

1. Both runs succeeded on the first attempt, wrote `readout.html`, exited 0, logged nothing to stderr and recorded no permission denials. There is no failure to report on either side.
2. The new run cost 27 percent less (1.56 against 2.15 USD) and finished 32 seconds sooner, with one fewer turn. The saving comes from context read, not output: cache reads fell from 1.23M to 0.72M tokens and cache creation from 101K to 74K, while output tokens fell only 12 percent (21001 to 18539).
3. Both runs assembled the marker block correctly. The `<style data-aperia="report">` tag holds the assembler comment followed by the same three source files in the same order, so injection worked identically. The attribution comment differs only because the script moved: old says `ui-components/assemble.py`, new says `apply-branding/components/assemble.py`, matching the 0.9.0 rename.
4. The injected block is slightly larger in the new run (78396 against 77274 chars, 572 against 566 rule blocks), which reflects the reference stylesheet changes in 0.9.0, not anything the model wrote.
5. The old run added a 412-char document-specific style block defining `code` typography and three context overrides, and its own result text names this as a new thing introduced. The new run's extra block is 46 chars, a single spacing rule. The new skill produced less hand-written CSS on top of the shared layer.
6. The new run reached for more of the shared component layer: 78 distinct classes against 66, including a 4-step `flow` for verification and a `phases` block with duration pills and deliverables for next steps. The old run used `outcome-grid` and `principles` for the same jobs and stated it deliberately skipped `phases` because the notes carry no durations, so the new run filled those fields from inference rather than from the source.
7. Neither run used a chart, KPI, gantt or timeline class. Both used exactly one `stat-row` of four `stat-card` and exactly one `cmp-table` with `.hl` on the current column, so the two prompt requests were met the same way in both.
8. No defects surfaced in either file on the checks run: no undefined classes, no broken in-page anchors (10 anchors each), no unbalanced non-void tags, no em or en dashes in rendered text, and no off-palette hex anywhere outside the injected block.
9. The new run dropped the two `preconnect` hints for Google Fonts that the old run emitted. The stylesheet link itself is present in both, so the font still loads; only the connection hint is gone.
10. Section ids differ by one name: old uses `next-steps`, new uses `next`. Both are internally consistent with their nav links.
11. Both models flagged content they could not source. Old flagged that the notes record no manual render or print pass and that its four next steps are inferred. New flagged that its "Not Covered" callout is an inference, and that it quoted the source's `ui-components/assemble.py` path as written rather than correcting it to the new location.
