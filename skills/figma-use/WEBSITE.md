# Figma skill → Gohil MF Studio (no engine changes)

This folder is the official [figma-use](https://github.com/figma/mcp-server-guide/blob/main/skills/figma-use/SKILL.md) skill, wired to this site **without editing** `MF-Ratings-Engine.html`.

## Why the HTML is unchanged

The live app is a single-file browser tool. Ratings, TRI, portfolio, SWP, and SIP logic stay in that file. Figma is used only as a design source. Tokens below already match the CSS variables in the engine.

## What you need

1. Figma desktop or browser with the file open.
2. Figma MCP / `use_figma` enabled in the agent that will write to Figma.
3. This skill loaded **before** every `use_figma` call (`skillNames: figma-use`).

This Grok session does **not** have `use_figma` connected (GitHub / Voice / Automations only). Connecting Figma MCP in the client is required before any canvas write.

## Screen map (existing app)

| Figma frame | App view | Do not change |
|---|---|---|
| Home | `#view-home` | Cards + Load TRI |
| Rate | `#view-rate` | Scoring table |
| Portfolio | `#view-pf` | Staging + verdicts |
| SWP | `#view-swp` | 3-bucket plan |
| SIP | `#view-sip` | FPA bands |
| Setup | `#view-setup` | TRI + brand |

## Token map (already in the HTML)

See `tokens.json`. Light and dark modes use the same names.

When building Figma variables, use these names so a later paint pass can copy values without renaming CSS in the engine.

## Safe workflow

1. Load `SKILL.md`.
2. Create or open a Figma file named `Gohil MF Studio`.
3. Create variable collection `Studio` with modes `Light` and `Dark`.
4. Create variables matching `tokens.json`.
5. Build frames that **mirror** the existing screens. Do not invent new product flows.
6. Export screenshots for review. Apply pixels to CSS only when the user asks to restyle.

## `use_figma` starter (when MCP is connected)

```js
const page = figma.currentPage;
const existing = page.findOne(n => n.name === "Gohil MF Studio / Home");
return { page: page.name, hasHome: !!existing, childCount: page.children.length };
```

Create frames only if that returns `hasHome: false`. Never overwrite the HTML from Figma automatically.
