# create-slides: friction in the nested runs

Sources: the nested session transcripts.

- old: `~/.claude/projects/...-bench-runs-slides-old/1ba8ed69-8754-435d-abde-03f20aa174b9.jsonl`, 90 lines, 18 tool calls
- new: `~/.claude/projects/...-bench-runs-slides-new/5f68dc98-d7a7-4d6a-9af8-5efd628cf263.jsonl`, 78 lines, 15 tool calls

Turn numbers below are the jsonl line index, written as `[n]`, with the tool call ordinal as `#n`. Neither run used the Write tool; both wrote the deck with a Bash heredoc, so "first Write" means the heredoc that created readout.html.

## 1. Tool errors, failed commands, retries, files not found

| | old | new |
| --- | --- | --- |
| is_error tool results | 1 | 0 |
| failed or empty commands | 1 | 0 |
| retries of a failed step | 0 | 0 |
| file not found | 0 | 0 |
| icon.py failures | 0 | 0 |
| assemble.py failures | 0 | 0 |

Detail:

- old `[85]` `#18`, the only error in either run: `ls /Applications | head -30; which chromium` returned exit 1 because `which chromium` found nothing. This came after `#17` `[82]`, `ls "/Applications/Google Chrome.app/..."; python3 -c "import playwright"`, which returned a bare `Traceback (most recent call last):`, playwright not installed. Both calls were the model hunting for a way to render the deck for a visual check. Neither is skill friction; both are environment probes after the deck was already finished. The model then gave up on the visual pass and said so in its final message.
- new made no browser probe at all.
- icon.py: old `#12` `[58]` ran `python3 scripts/icon.py syringe palette shield-check` against the bundled `ui-components/icons/lucide-icons.json` and got 3 SVGs first try. new `#11` `[54]` ran `python3 scripts/icon.py file-code palette shield-check`, which in 0.9.0 fetches each icon from the Lucide CDN, and also got 3 SVGs first try. No fetch error, no fallback, no missing-slug retry in either run. The network dependency added in 0.9.0 was exercised and it held.
- assemble.py: one clean call in old (`#15` `[73]`, invoked as `old/plugins/aperia/ui-components/assemble.py` from the bench root), two clean calls in new (`#13` `[65]` and `#15` `[72]`, invoked as `../apply-branding/components/assemble.py` from the skill folder). Both printed `assemble: readout.html <- slides (36KB of CSS)`. Neither run had to search for the script or correct its path.

## 2. Reads the SKILL.md read rule forbids, and repeat reads

The read rules differ between versions, so the same action is a violation in one and not the other.

- old SKILL.md Step 0 says read `BRAND.md` in full, read `references/snippets.html`, and skim `references/slides.css`. It has no "never read" list. It does say "Do not paste either stylesheet."
- new SKILL.md has an explicit **Never** line: "`references/slides.css` and `../apply-branding/brand/tokens.css`, beyond a skim of `slides.css` for class names and the type tokens."

| behavior | old | new |
| --- | --- | --- |
| read tokens.css | yes, `#4` `[21]`, `cat brand/tokens.css` in full, 5624 chars. Not forbidden by the old text. | yes, `#10` `[47]`, `sed -n '1,60p' brand/tokens.css`. This is on the new **Never** list. |
| read slides.css | 4 separate passes: `#7` `sed 1,140p`, `#8` `grep '^\.'`, `#9` `grep h1/h2/h3/s-list/chart-frame`, `#13` `sed 316,486p`. Together roughly the whole 486-line file, past "skim". | 2 passes: `#7` `sed -n '1,90p'`, `#9` `grep` for class names. Stays inside the skim allowance. |
| read qa.py source | yes, twice: `#10` `sed 1,80p` plus a grep, `#11` `sed 85,260p`. Not mentioned in the read rules either way. | yes, once: `#8` `cat scripts/qa.py` in full. |
| same file read twice | snippets.html, forced: `#5` `cat references/snippets.html` overflowed the Bash output cap at 31.7 KB and was persisted to a tool-results file, then `#6` Read of that persisted file, 34641 chars. | same pattern: `#5` `cat references/snippets.html` overflowed at 31.6 KB, then `#6` Read of the original file, 34558 chars. |

The snippets.html double read is the single clearest piece of friction and it is identical in both versions. The file is 579 lines and about 31.6 KB, just over the Bash output cap, so `cat` always spills and always costs a second call. Both SKILL.md files tell the model to read that file, and neither warns that `cat` will truncate or suggests the Read tool for it. new lost slightly less by re-reading the source file directly; old re-read the persisted output file, which also carried the `wc -l` header lines from the earlier call.

The tokens.css read is the one place where new violated its own stated rule. It came bundled into a directory-orientation call (`ls` of apply-branding, `ls components`, then the sed), so it reads as the model confirming the layer layout rather than mining values, and no off-palette color reached the output.

## 3. Hand-written CSS, or edits inside the assembled block

Neither run wrote CSS by hand and neither edited inside the marker.

- Both wrote the document with the bare marker `<style>/* @aperia slides */</style>` in `<head>` and let assemble.py fill it. The heredoc content at old `#14` `[67]` and new `#12` `[59]` is byte-identical in that region.
- Neither deck has a second `<style>` element, so no document-specific rules were added.
- Post-QA edits in both runs were text-only replacements in slide body copy, applied by a python heredoc with `assert` guards, outside the marker.
- One process deviation, old only: after its post-QA edit (`#16` `[77]`) old ran `qa.py` but did not re-run `assemble.py`. The old checklist says "assemble.py was run after the last edit". The edit did not touch the marker so the output is correct, but the stated order was not followed. new did re-run assemble.py after its edit (`#15` `[72]`), matching the rule.

## 4. Pauses, re-planning, stated uncertainty

Thinking blocks in both transcripts are redacted, present as `{"type":"thinking","signature":...}` with empty content, so internal reasoning is not readable. What is visible is the narration text and the shape of the tool sequence.

- old narration: `[12]` "I'll start by reading the brand layer and skill references as required.", `[27]` "Now the snippets file and slides.css.", `[66]` "All references read. Writing the deck.", `[72]` "Now assemble and QA."
- new narration: `[12]` "I'll start by reading the source and the skill's references.", `[58]` "Building the deck now.", `[64]` "Now assemble the theme and run QA."

Neither run said it was unsure what the skill wanted, asked a question, or restarted a step. Both moved read, write, assemble, QA, fix, QA, report with no backtracking. The only visible pause is old's two-call browser hunt at the end, which is a stated limitation rather than confusion: its final message says "no browser on this machine to render it, so the by-eye pass for overflow and print preview is still open" and quantifies the densest slide instead. new's final message states the same gap in one line without probing for a browser.

new's SKILL.md workflow step 2 says "Outline first ... Show it and get a nod before generating, unless the user asked for" a direct build. The prompt said not to ask, and new skipped the outline step without comment. old's equivalent step was not visible in the narration either. No friction, but the rule did require the model to notice an exception.

## 5. Tool calls before the first write of readout.html

old: 13 calls, then the heredoc at `#14`.

1. `ls` bench root and `cat runs/slides-old/source.md`
2. `ls -R brand ui-components`
3. `cat brand/BRAND.md` (16106 chars)
4. `cat brand/tokens.css` (5624 chars)
5. `wc -l` snippets and slides.css, `cat references/snippets.html` (truncated, persisted)
6. Read of the persisted tool-result file (34641 chars)
7. `sed -n '1,140p' references/slides.css`
8. `grep -n '^\.' references/slides.css | head -120`
9. `grep -n 'h1\|h2\|h3\|s-list\|chart-frame\|chart-note' references/slides.css`
10. `sed -n '1,80p' scripts/qa.py` plus a `grep` for defs
11. `sed -n '85,260p' scripts/qa.py`
12. `python3 scripts/icon.py syringe palette shield-check`
13. `sed -n '316,486p' references/slides.css`

new: 11 calls, then the heredoc at `#12`.

1. `ls -la` and `cat source.md`
2. `ls` skill dir, `ls ..`, `ls references scripts`
3. `cat apply-branding/brand/BRAND.md` (8029 chars)
4. `wc -l` snippets, slides.css, qa.py
5. `cat references/snippets.html` (truncated, persisted)
6. Read of `references/snippets.html` directly (34558 chars)
7. `sed -n '1,90p' references/slides.css`
8. `cat scripts/qa.py`
9. `grep` class names in `references/slides.css`
10. `ls` apply-branding, `ls components`, `sed -n '1,60p' brand/tokens.css`
11. `python3 scripts/icon.py file-code palette shield-check`

Call `#2` in new is the `ls ..` the new SKILL.md explicitly asks for, to learn whether the sibling folder is `apply-branding` or `aperia:apply-branding`. It found `apply-branding` and every later path used that name. The instruction did its job in one call.

The two calls new saved over old are both slides.css passes: old made 4 reads of that file across the run, new made 2.

## 6. qa.py runs

Two runs each, same shape: one that warned, one that came back clean.

| | old | new |
| --- | --- | --- |
| run 1 | `#15` `[73]`, bundled with assemble. `WARNINGS (1)  [15] 64 words of body copy, trim toward 40`. No errors. | `#13` `[65]`, bundled with assemble. `WARNINGS (2)  [05] 56 words of body copy, trim toward 40  [15] 58 words of body copy, trim toward 40`. No errors. |
| fix | `#16` `[77]`, python heredoc shortening the four bullets on slide 15, then qa only | `#14` `[69]`, python heredoc with three replacements across slides 05 and 15, then a separate assemble plus qa |
| run 2 | `#16`, `Clean.` | `#15` `[72]`, `Clean.` |

Both models acted on the warnings rather than dismissing them, and both got to clean in one fix. Neither ever saw an ERROR. Neither QA script flagged the missing logo `aria-label` in the new deck, so that defect passed both checkers.

## 7. Skill text quoted back as confusing, contradictory, stale, or pointing at a missing file

Nothing. Neither run quoted a line of SKILL.md as unclear, and neither hit a broken path.

Verified independently: every relative path either SKILL.md names resolves in its own tree. old's `../../brand/BRAND.md`, `../../ui-components/COMPONENTS.md`, `../../ui-components/assemble.py`, `../../ui-components/icons/lucide-icons.json`, `../../ui-components/base/styles.css` all exist. new's `../apply-branding/brand/BRAND.md`, `../apply-branding/components/COMPONENTS.md`, `../apply-branding/components/assemble.py`, `../apply-branding/components/icons/index.html`, `../apply-branding/brand/tokens.css`, `scripts/icon.py`, `scripts/qa.py` all exist. No stale reference survived the 0.9.0 move of the components layer, at least on the paths these runs touched.

The nearest thing to a documentation gap is the one named in section 2: both SKILL.md files instruct a read of `references/snippets.html`, which is 31.6 KB, and neither says how to read it without hitting the Bash output cap. Both runs paid a wasted call for that.

## 8. How each run chose between the labeled and unlabeled logo variants

The transcripts do not show the reasoning, since thinking is redacted, but the source makes the mechanism clear and both snippet files are identical here.

`references/snippets.html` carries the logo two ways, the same in 0.8.0 and 0.9.0:

- line 111 to 112, a standalone documentation block headed "slide footer, put this in every content slide, omit on cover/section/end", which uses `<svg class="logo" viewBox="0 0 135 40" aria-label="Aperia">`
- lines 161, 187, 202, 238, 263, 289 and onward, inside every full slide example, which use the bare `<svg class="logo" viewBox="0 0 135 40">` with no label
- line 134, the cover logo, which has `aria-label="Aperia"`

So the file contradicts itself: the block that says "put this in every content slide" is labeled, and every worked example of a content slide is not. old resolved it toward the documentation block and emitted `aria-label="Aperia"` on all 11 logos. new resolved it toward the worked examples and emitted the label only on the cover, leaving 10 footer logos unlabeled. new's SKILL.md pushes harder in that direction: "Copy the layout markup and replace the copy, not the structure", and its read list sends the model to snippets.html for "every layout" rather than to a prose rule. Following the new instruction more literally produced the worse markup.

This is a defect in the shared snippet file, not a 0.9.0 regression in itself, but 0.9.0's stronger copy-verbatim framing makes the unlabeled variant the likely outcome. Fixing line 161 onward to carry `aria-label="Aperia"` would remove the ambiguity for both versions.

## My own difficulties running this bench

- Thinking blocks are stored with empty content in both transcripts, so section 4 rests on narration text and tool sequence rather than on stated reasoning. If internal reasoning matters for a future comparison, the runs would need to be captured with thinking retained.
- Both nested runs hit the Bash output cap on `cat references/snippets.html`, which pushed the content into a persisted tool-results file. It did not block anything, but it means a raw transcript read undercounts what the model saw unless the persisted files are followed.
- Nothing else. Both commands ran first try inside the 600000 ms timeout, exit 0, empty stderr, no permission denial, no retry needed. The outer shell resets its working directory between Bash calls, so every command in this analysis used absolute paths.
