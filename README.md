# Aperia Claude Toolkit

## Overview

A Claude plugin with three skills that produce on-brand Aperia output, built on one shared brand and component layer. Built from Aperia Brand Guidelines v1.0.

| Skill | Invoke as | Output |
|---|---|---|
| Create report | `/aperia:create-report` | Self-contained HTML report, briefing, or proposal |
| Create slides | `/aperia:create-slides` | Self-contained HTML deck that runs in the browser |
| Apply branding | Automatic, just describe the artifact | Anything else in the Aperia look: a page, an email, a dashboard, a graphic |

The brand layer (palette, typography, logo rules, the parallelogram element) and the component layer (cards, badges, callouts, tables, a chart toolkit, icons, milestone and status timelines) live inside the `apply-branding` skill, and the other two read them from there, so the same piece looks the same in a report, a deck or a page.

## How to install

### Claude Code

Start a Claude Code session and run:
```
/plugin marketplace add thuannguyen13/aperia-skills
/plugin install aperia@aperia-skills
```

### Desktop / Cowork

In Claude Desktop:

1. Navigate `Settings` → `Plugins` → `Add` → `Add marketplace` → `Add from a repository`
2. Then pick `thuannguyen13/aperia-skills` from the list or paste the repo URL.
3. Install `Aperia Claude Toolkit` from it.

## How to use

Invoke a skill by name, then describe what you want:
- `/aperia:create-slides` build a readout from the Q3 findings
- `/aperia:create-report` write this up as a strategic briefing

Anything else in the Aperia look needs no command. Describe it, for example "build an Aperia landing page for the Q3 launch", and Claude loads the branding skill on its own.


## Maintaining

Changing the brand, the validation rules, and the repo conventions are covered in [MAINTAINING.md](MAINTAINING.md).
