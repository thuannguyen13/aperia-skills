# Aperia Claude Toolkit

## Overview

A Claude plugin with two skills that produce on-brand Aperia output, built on
two shared reference layers. Built from Aperia Brand Guidelines v1.0.

| Skill | Invoke as | Output |
|---|---|---|
| Create report | `/aperia:create-report` | Self-contained HTML report, briefing, or proposal |
| Create slides | `/aperia:create-slides` | Self-contained HTML deck that runs in the browser |

Each skill reads two shared layers before producing anything:
`brand/` (palette, typography, logo rules, the parallelogram element) and
`ui-components/` (cards, badges, callouts, tables, a full chart toolkit, an
icon set, and milestone/status timelines), so the same piece looks and
behaves the same way whether it lands in a report or a deck. Neither layer
is a skill on its own — they're reference folders every skill reads, the
same way `brand/` always has been.

## How to install

### Claude Code

Start a Claude Code session and type in following commands:
```
/plugin marketplace add thuannguyen13/aperia-skills
/plugin install aperia@aperia-skills
```

### Desktop / Cowork

Open Claude Desktop and following instruction:

1. Navigate `Settings` → `Plugins` → `Add` → `Add marketplace` → `Add from a repository`
2. Then pick `thuannguyen13/aperia-skills` from the list or paste the repo URL.
3. Install `Aperia Claude Toolkit` from it.

## How to use

Invoke a skill by name, then describe what you want:
- `/aperia:create-slides` build a readout from the Q3 findings
- `/aperia:create-report` write this up as a strategic briefing


## Maintaining

Changing the brand, the validation rules, and the repo conventions are covered
in [MAINTAINING.md](MAINTAINING.md).
