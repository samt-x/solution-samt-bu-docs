---
id: 92dc0a2e-1c31-4f62-b1da-0c55b80f89e0
title: "TipTap som WYSIWYG-editor"
linkTitle: "TipTap som editor"
weight: 110
status: "Godkjent"
lastmod: 2026-03-27T23:29:13+01:00
last_editor: Erik Hagen

---

**Implementert 2026-03-11 (kveld).** TipTap v2 erstatter Quill v1 i begge editordialoger (qe-dialog og np-dialog).

## Implementasjon

- **CDN:** Dynamic `import()` fra `esm.sh` – lastes lazy første gang dialog åpnes
- **Extensions:** StarterKit, Table + TableRow/Cell/Header, Link, Image, `tiptap-markdown`
- **Markdown roundtrip:** `editor.commands.setContent(md)` inn, `editor.storage.markdown.getMarkdown()` ut
- **Toolbar:** Custom HTML-knapper (`data-qe` / `data-np`), active-state via `is-active`-klasse
- **Tabellredigering:** Innsetting, legg til/slett rad og kolonne fra toolbar
- **Bildepaste:** base64 → data-URL i editor, erstattes med filnavn ved lagring, committes som blob
- **Delt last:** `loadTiptap()` i global scope – `_Tiptap` gjenbrukes av begge IIFE-er

## Nøkkelforskjell fra Quill

| | Quill | TipTap |
|---|---|---|
| Tabeller | GFM-mal som tekst | Visuell ProseMirror-tabell |
| Markdown ut | Turndown (HTML→MD) | `tiptap-markdown` native |
| Markdown inn | `marked.parse()` (MD→HTML) | Direkte `setContent(md)` |
| CDN | UMD fra jsDelivr | ESM fra esm.sh |
| Toolbar | Quill Snow (innebygd) | Custom HTML |

## Relatert

- `edit-switcher.html`: CSS og HTML for toolbar + editor-container
- `custom-footer.html`: `loadTiptap`, `initNpEditor`, `setupQeToolbar`, `openQuillEditDialog` (navn beholdt for bakoverkompatibilitet)
- Endringslogg 2026-03-11 kveld i `claude-kontekst/`
