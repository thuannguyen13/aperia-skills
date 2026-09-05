# Bench

One run of `create-report` per plugin version on the same prompt and source, in Claude Code, non-interactively. `old/` is 0.7.0, `new/` is 0.8.0. Each folder holds the report the run produced and the JSON meter Claude Code returned. `comparison.json` is the two meters side by side.

### Run it again

1. Extract the old plugin: `git archive <commit> plugins/aperia | tar -x -C <dir>`.
2. In an empty folder with `source.md` beside it, run `claude -p "$(cat prompt.md)" --output-format json --plugin-dir <plugin> --allowedTools Read Write Edit Bash Glob Grep Skill`.
3. Repeat for the new plugin, then compare `duration_ms`, `usage` and `total_cost_usd`.
