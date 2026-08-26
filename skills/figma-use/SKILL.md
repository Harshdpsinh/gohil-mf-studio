---
name: figma-use
description: MANDATORY prerequisite before every use_figma call. Trigger on Figma write or Plugin API inspect including nodes, variables, components, auto-layout, fills.
---

# use_figma — Figma Plugin API Skill

Canonical source (do not fork the rules):
https://raw.githubusercontent.com/figma/mcp-server-guide/main/skills/figma-use/SKILL.md

Always pass `skillNames: figma-use` on `use_figma`.

Site wiring for Gohil MF Studio (engine HTML is not modified):
- [WEBSITE.md](WEBSITE.md)
- [tokens.json](tokens.json)
- [FIGMA.md](../../FIGMA.md)

## Before any use_figma call

1. Load the canonical SKILL.md from the URL above.
2. Use `return` for output. Never `figma.notify()` or `figma.closePlugin()`.
3. Colors are 0–1, not 0–255.
4. Load fonts before editing text.
5. Switch pages with `await figma.setCurrentPageAsync(page)` only.
6. Work in small steps. Return created and mutated node IDs.
7. Match existing Studio tokens in tokens.json. Do not invent new CSS names.
