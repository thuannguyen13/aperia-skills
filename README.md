# Aperia Claude Toolkit

## Overview

A Claude plugin with three skills that produce on-brand Aperia output.
Built from Aperia Brand Guidelines v1.0.

| Skill | Invoke as | Output |
|---|---|---|
| Create report | `/aperia:create-report` | Self-contained HTML report, briefing, or proposal |
| Create slides | `/aperia:create-slides` | Self-contained HTML deck that runs in the browser |
| Apply branding | `/aperia:apply-branding` | Any other artifact in the Aperia brand |
| Apply UI components | `/aperia:apply-ui-components` | One or a few Aperia-styled pieces — a card, a table, a chart, a timeline, an icon — dropped into a page, dashboard, or artifact |

Each skill reads one shared brand layer before producing anything, so the
palette, typography, logo rules, and parallelogram element come out right
without you specifying them.

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
- `/aperia:apply-branding` make this dashboard on-brand
- `/aperia:apply-ui-components` add an Aperia-styled comparison table here


## Maintaining

Changing the brand, the validation rules, and the repo conventions are covered
in [MAINTAINING.md](MAINTAINING.md).
