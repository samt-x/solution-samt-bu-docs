---
id: c5e5948f-2ac0-46f7-b27e-43a14f614046
title: "AI writing assistance in the editor"
linkTitle: "AI writing assistance"
weight: 160
status: "New"
lastmod: 2026-03-21T01:30:22+01:00
last_editor: erikhag1git (Erik Hagen)

---

Users of the built-in editing interface can save time on writing, translation, and proofreading with AI directly in the editor — without SAMT-BU project incurring any API costs.

## Concept

The user provides their own API key from an AI provider they already have an account with. The key is stored locally in the browser (`localStorage`) and used to call the provider's API **directly** — no CF Worker or server-side component required.

```
Browser  →  [chosen AI provider's API]
             (key in localStorage, never sent to SAMT-BU infrastructure)
```

## Supported providers (planned)

| Provider | API | CORS from browser | Notes |
|----------|-----|--------------------|-------|
| Anthropic Claude | `api.anthropic.com/v1/messages` | ✅ with `anthropic-dangerous-direct-browser-calls: true` | claude-haiku is cheapest |
| OpenAI / ChatGPT | `api.openai.com/v1/chat/completions` | ✅ | gpt-4o-mini = low cost |
| Google Gemini | `generativelanguage.googleapis.com` | ✅ via `?key=` | free tier available |
| Ollama (local) | `localhost:11434` | ✅ (local) | free, requires local install |

## UX in the TipTap editor

Three buttons in the editor toolbar plus a settings button:

```
[ Improve ]  [ Translate to EN ]  [ Shorten ]  [⚙ AI settings]
```

If no key is configured → clicking opens the settings dialog directly.

## Technical implementation

All changes in `custom-footer.html` (theme):

1. **`aiComplete(instruction, text)`** – shared function that delegates to the correct adapter
2. **One adapter per provider** – wraps the call in the provider's format, returns text (~20 lines per adapter)
3. **AI settings dialog** – choose provider, enter key, choose model, test button; saved to `localStorage`
4. **AI toolbar in TipTap** – three action buttons + settings button

### localStorage keys

| Key | Content |
|-----|---------|
| `samtu-ai-provider` | `anthropic` / `openai` / `gemini` / `ollama` |
| `samtu-ai-key` | API key |
| `samtu-ai-model` | Selected model (e.g. `claude-haiku-4-5-20251001`) |

## Benefits

- **No cost to the project** – user uses their own account
- **No new infrastructure** – no CF Worker changes required
- **Extensible** – new providers added as a single adapter with no structural changes
- **Works offline** for Ollama users

## Priority

Low — useful additional feature, but not critical to the core workflow.

## Related

- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html` – TipTap editor and `openQuillEditDialog()`
- Roadmap: [Conflict warning during editing](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/veikart/rediger-konfliktvarsel/)
