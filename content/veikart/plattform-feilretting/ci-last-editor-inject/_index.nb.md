---
id: 7ee1e5cc-73be-463b-99bd-913dbfc73076
title: "CI-injeksjon av last_editor for ikke-CMS-redigeringer"
linkTitle: "CI: last_editor for alle redigeringsveier"
weight: 75
status: "Ny"
last_editor: erikhag1git (Erik Hagen)
lastmod: 2026-03-15T23:49:44+01:00

---

## Bakgrunn

`last_editor`-feltet i frontmatter settes i dag kun av den innebygde CMS-editoren. Sider redigert via GitHub web-UI, GitHub API eller lokal klon → push får feltet satt via `fix-last-editor.py` (batch, kjørt én gang), men nye redigeringer via disse kanalene vil mangle `last_editor` frem til de redigeres via CMS.

## Mål

Sikre at `last_editor` settes korrekt uansett hvilken redigeringskanal som brukes – uten at redaktøren trenger å gjøre noe ekstra.

## Foreslått løsning

Nytt steg i `hugo.yml` (og `trigger-docs-rebuild.yml`):

Når en menneskelig push utløser workflow (`github.actor` ≠ `github-actions[bot]`):

1. Hent pusherens display-navn via GitHub API: `GET /users/{github.actor}`
2. Bygg `last_editor`-verdi: `login (navn)` eller `login (ukjent navn)`
3. For hver `.md`-fil endret i pushen (fra `git diff --name-only HEAD~1 HEAD`):
   - Sett `last_editor` hvis feltet mangler eller har bot-verdi
   - Behold eksisterende menneskelige verdier
4. Commit med `[skip ci]`-tag (samme mønster som ensure-uuids)

## Dekker alle redigeringsveier

| Redigeringskanal | Dekkes av |
|-----------------|-----------|
| Innebygd CMS-editor | Allerede implementert (skriver `last_editor` ved lagring) |
| GitHub web-UI | Dette tiltaket |
| GitHub API | Dette tiltaket |
| Lokal klon → push | Dette tiltaket |
| Bot-commits | Filtreres ut (injiseres ikke, vises ikke) |

## Relatert

- `.github/scripts/fix-last-editor.py` – batch-versjon av samme logikk (kjørt én gang)
- `.github/scripts/inject-lastmod.py` – tilsvarende mønster for `lastmod`-feltet
- `themes/hugo-theme-samt-bu/layouts/partials/header.html` – visningslogikk
