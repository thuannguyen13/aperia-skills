# Friction while using create-report: 0.8.0 (old) against 0.9.0 (new)

Source: the nested session transcripts.

- old: `~/.claude/projects/-private-tmp-...-bench-runs-report-old/ae93bb7b-f549-4b34-a08a-1b1f2b9cc3b3.jsonl`, 16 tool calls
- new: `~/.claude/projects/-private-tmp-...-bench-runs-report-new/6663c30c-b80a-459f-8186-8b27a09fd597.jsonl`, 15 tool calls

Both sessions ran in auto mode with `bashFirst: strict`, so every read, write and check went through Bash. Neither session called `Read`, `Write` or `Edit`; `readout.html` was created with a `cat > readout.html <<'HTMLEOF'` heredoc in both. Turn numbers below are tool-call indexes within the nested session. The stored `thinking` blocks are empty in both transcripts, so re-planning is visible only through the commands and the short text lines between them.

## 1. Tool errors, failed commands, retries, file not found

| | old | new |
| --- | --- | --- |
| Tool calls with `is_error: true` | 1 (turn 13) | 0 |
| Commands that returned nothing useful | 1 (turn 11) | 0 |
| Retries | 1 (turn 14 repeats turn 13's assemble step) | 0 |

Old, turn 13. The command combined a python heredoc that inserted a hand-written `<style>` block with a call to the assembler:

```
python3 ../../../old/plugins/aperia/ui-components/assemble.py readout.html
```

Result, exit code 2:

```
/Library/Developer/CommandLineTools/usr/bin/python3: can't open file
'/private/tmp/.../scratchpad/bench/runs/report-old/../../../old/plugins/aperia/ui-components/assemble.py':
[Errno 2] No such file or directory
```

The path is one level short: the working directory was the run folder, not the skill folder, and the skill writes its assemble path as `../../ui-components/assemble.py`, relative to the skill folder. The python heredoc in the same command had already run, so the hand-written style block landed in the file and only the assemble step failed. Turn 14 retried with a full absolute path and succeeded: `assemble: readout.html <- report (75KB of CSS)`.

Old, turn 11. `grep -n "code\b" ui-components/base/styles.css skills/create-report/references/styles.css brand/tokens.css | head` returned no matches at all. This is what led to the hand-written CSS in turn 13.

New had no failed command. Turn 13 ran the assembler the way the skill documents it, from the skill folder with the relative script path and an absolute target: `cd .../skills/create-report && python3 ../apply-branding/components/assemble.py /.../report-new/readout.html`, output `assemble: readout.html <- report (76KB of CSS)`.

## 2. Reads the skill's read rule discourages, and repeat reads

Both versions carry the same rule: never read a stylesheet, skim one only when a class's behaviour is unclear. Old states it as "Do not read or paste any stylesheet"; new states it as a "**Never.** Any stylesheet" heading.

Old, stylesheet touches across 4 separate turns:

- turn 8: `grep "^\.|^ *\.mb-|^\.text-" ui-components/base/styles.css`, class inventory
- turn 9: `grep "@page|@media print"` on `references/styles.css` and `base/styles.css`
- turn 11: `grep "code\b"` on `base/styles.css`, `references/styles.css` and `brand/tokens.css`
- turn 12: `grep "--sans|--fw-|--light-gray|--aperia-blue|..."` on `brand/tokens.css` and `base/styles.css`

`base/styles.css` was touched at turns 8, 9, 11 and 12, four times. `references/styles.css` at turns 9 and 11. `tokens.css` at turns 7 and 12. Old's turn 7 also read the first 60 lines of `assemble.py`, which the skill does not ask for.

New, stylesheet touches in 1 turn:

- turn 10: `grep "^\.\(text-\|mb-\|mt-\|sec-\|sub-\|caption\|wrap\|lead\)"` on `components/base/styles.css` plus `grep "^\."` on `create-report/references/styles.css`

New also read the first 50 lines of `tokens.css` and the first 60 of `assemble.py` in turn 9. No file was read twice in the new run.

Prescribed reads were followed in both. Old read `BRAND.md` (3), `COMPONENTS.md` (4), `base/index.html` (5) and `references/snippets.html` (6). New read `BRAND.md` (3), `COMPONENTS.md` (4), `references/snippets.html` (5), then the four snippet files its chosen components live in: `structure.html` (6), `emphasis.html` (7), `tables.html` (8) and the Step Flow section of `timelines.html` (11). New also followed the new instruction "Run `ls ..` from this skill folder once" literally, at turn 2.

Neither run opened `references/interactive.html`, which both skills say to read "if the report is a delivery, release or roadmap plan". The document is a release readout, so the condition is arguably met and was skipped silently in both. Neither run explained the skip.

## 3. Hand-written CSS, and edits to the assembled block

Neither run edited inside the injected `<style data-aperia>` block. Both put their extra rules in a second `<style>` after the marker, which both skills allow.

Old, turn 13, wrote 412 characters of CSS by hand after the empty grep at turn 11:

```
code { font-family:var(--sans); font-size:inherit; font-weight:var(--fw-medium); color:inherit;
       background:var(--muted); border-radius:var(--radius-sm); padding:0 4px }
.hero code, .dark-panel code, .cta-box code { background:rgba(255,255,255,.14) }
```

Its final message names this as the one new thing introduced, with the reason: no layer styles `code`, and the browser default is monospace, which `BRAND.md` does not sanction. The rule uses only tokens, so it stays in palette.

New wrote 46 characters, one spacing rule, `.sec-intro + .stat-row { margin-top: 4px }`. It used `<code>` markup nowhere, so it never hit the gap old found.

## 4. Pauses, re-planning, stated uncertainty

Neither run paused, asked a question or said it was unsure what the skill wanted. The transcripts hold no such statement, and the thinking blocks are empty.

The closest thing to re-planning is old's turn 11 to 13 sequence: it went looking for a `code` rule, found none, and then decided to write one and to justify it in the final message. New's only visible course correction is turn 11, going back for the Step Flow snippet in `timelines.html` after the other component files were read, before writing.

Text lines between the tool calls, in order. Old: "I'll start by reading the source notes and the required brand/component layers", then "Now the report skill's own snippets". New: "I'll start by reading the source notes and the skill's reference material", then "Sibling layer is `apply-branding`. Reading the required docs", then "Writing the report now".

## 5. Tool calls before the first write of readout.html

Old: 9 calls before turn 10 wrote the file.

1. `ls -la` plus `cat source.md`
2. `ls -R` on the plugin root plus `wc -l` on the five files it planned to read
3. `cat brand/BRAND.md`
4. `cat ui-components/COMPONENTS.md`
5. `cat ui-components/base/index.html`
6. `cat skills/create-report/references/snippets.html`
7. head of `ui-components/assemble.py` plus a grep of type and radius tokens in `tokens.css`
8. class inventory grep on `base/styles.css`
9. print-rule grep on `references/styles.css` and `base/styles.css`

New: 11 calls before turn 12 wrote the file.

1. `ls -la` plus `cat source.md`
2. `ls ..` from the skill folder plus `ls -R` of the skill folder
3. `ls -R` of `apply-branding` plus `cat brand/BRAND.md`
4. `cat components/COMPONENTS.md`
5. `cat references/snippets.html`
6. `cat components/base/structure.html`
7. `cat components/base/emphasis.html`
8. `cat components/base/tables.html`
9. head of `components/assemble.py` plus head of `brand/tokens.css`
10. class inventory grep on `base/styles.css` and `references/styles.css`
11. Step Flow section of `components/base/timelines.html`

New spent two more calls before writing because the component library is split into four snippet files instead of one `index.html`, and because it ran the prescribed `ls ..` discovery step.

## 6. Validation and QA steps, and their output

Neither plugin ships a QA script for reports. `qa.py` exists only under `create-slides`, in both versions. Both checklists therefore had to be checked by hand, and both runs improvised greps.

Old, 3 checks after assembling.

- turn 14, assemble plus a marker check: `assemble: readout.html <- report (75KB of CSS)`, `data-aperia="report"`, `104604 readout.html`
- turn 15, dashes, sections, links, component counts: `dashes-ok`; `sections: ['summary','changed','verification','next-steps']`; `links: ['changed','main','next-steps','summary','verification']`; `styles blocks: 4`; counts for stat-row 3, cmp-table 8, stack-table 6, outcome-grid 3, principles 5, dark-panel 9, cta-box 9, skip-link 4, nav-drawer 7
- turn 16, `grep -n "<style"`: four hits, of which two are mentions inside CSS comments. This turn exists because turn 15's raw count of 4 was ambiguous.

New, 2 checks after assembling.

- turn 14, a python check of class resolution, dashes, the marker and ids: `missing: []`, `em dash present: False`, `style blocks: 4`, `ids: [...]`. The `marker:` line of that check is wrong: the regex `@aperia[^*]*` matched the `@aperia` mention inside the injected `references/styles.css` header comment, not the marker, so it printed 15 lines of assembler documentation instead of the marker text. The model did not act on the bad output.
- turn 15, `grep -n "<style\|</style>"`: opens at 8 and 1051, closes at 1050 and 1053, plus the two comment mentions, which resolves the same count ambiguity old needed a separate turn for.

New's class-resolution check (every class used exists in the injected CSS) is stronger than anything old ran. Old's check counted components by name only.

Checklist items neither run could perform and neither flagged as skipped: the printed-PDF pass and, in new, the narrow-viewport pass. New's final message states the file "opens in any browser, prints to PDF, and shares as a single file" without having rendered it.

## 7. Skill text quoted back as confusing, contradictory, stale, or pointing at a missing file

Nothing in either SKILL.md was quoted back as wrong. The two related remarks are:

- Old's final message reports a gap rather than an error: `code` is styled by nothing in `tokens.css`, `base/styles.css` or the report theme, so it wrote the rule itself. Turn 11's empty grep is the evidence.
- New's final message reports a stale path in the input, not in the skill: "the source lists `ui-components/assemble.py` while the skill folder ships it at `apply-branding/components/assemble.py`, so I quoted the source's path as written rather than silently correcting it".

The one path problem that did bite is old's turn 13, and it comes from the skill's habit of writing script paths relative to the skill folder (`../../ui-components/assemble.py`) while the model worked from the output folder. New's workflow line says explicitly "run `python3 ../apply-branding/components/assemble.py <file>` from this skill folder", and new did exactly that, first try.

## My own difficulties running the bench

- None on the two runs. Both exited 0, wrote `readout.html`, produced empty `stderr.log` files and needed no retry.
- The `bench/runs` folder holds `slides-old` and `slides-new` alongside the report folders, so the project directory listing under `~/.claude/projects` has five bench entries. The two report transcripts were identified by the `session_id` in each `result.json`, not by folder name alone.
- `thinking` blocks are stored empty in both transcripts, so item 4 above is answered from commands and interstitial text only. There is no record of internal deliberation to quote.
- Old's turn 10 and new's turn 12 are single Bash calls carrying the whole HTML document as a heredoc, so any naive scan for file paths in commands picks up paths that are report content rather than files the model read. The read inventory in items 2 and 5 counts only the pre-write turns.
