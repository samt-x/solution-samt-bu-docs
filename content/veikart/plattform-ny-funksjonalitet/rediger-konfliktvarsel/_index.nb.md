---
id: 6600fd23-52ac-42cd-8a38-0eaa8ef08e51
title: "Advarsel ved samtidig redigering av samme side"
linkTitle: "Konfliktvarsel ved redigering"
weight: 150
status: "Ny"
lastmod: 2026-03-18T20:34:20+01:00
last_editor: Erik Hagen

---

Hvis to brukere åpner redigeringsdialogen for samme side samtidig, vil den siste som lagrer overskrive den andres endringer uten advarsel. En enkel «noen redigerer allerede denne siden»-melding ville redusert risikoen for tapte endringer.

## Utfordring

Konfliktvarselet krever en form for delt tilstand: at én nettleser kan se at en annen nettleser har åpnet redigeringsdialogen for en bestemt side. `localStorage` er bruker-lokalt og fungerer ikke på tvers av brukere.

## Mulige løsninger

### A – Cloudflare Workers KV (lettvekt presence-register)

Når redigeringsdialogen åpnes: skriv `{ user, page, openedAt }` til KV med TTL på f.eks. 10 minutter.
Når en annen bruker åpner samme side: les KV og vis advarsel hvis oppføringen finnes og ikke er utløpt.
Når dialogen lukkes eller lagres: slett oppføringen.

**Fordeler:** Lav latens, ingen ekstern avhengighet utover eksisterende CF-infrastruktur. KV er gratis på CF Workers free tier.
**Ulemper:** Krever endring i Cloudflare Worker + ny KV-binding. TTL-basert – stale locks hvis nettleseren krasjer uten å slette.

### B – GitHub-fil som lock-register

Skriv en liten JSON-fil (f.eks. `.editing-locks.json`) til en branch i repoet via GitHub API. Leses av andre brukere ved åpning av dialog.

**Fordeler:** Ingen ny infrastruktur.
**Ulemper:** GitHub API-kall er treige for dette formålet. Risiko for konflikt på lock-filen selv.

### C – Kun advare basert på aktive bygg

En enklere tilnærming: vis advarsel hvis det finnes et aktivt bygg nylig trigget fra samme side (utledet fra commit-meldingen). Ikke en ekte lock, men dekker det vanligste tilfellet.

**Fordeler:** Bruker eksisterende GitHub Actions API – ingen ny infrastruktur.
**Ulemper:** Dekker ikke tilfellet der en bruker har åpnet dialogen men ikke lagret ennå.

## Anbefalt tilnærming

**Alternativ A** (CF Workers KV) er den reneste løsningen og passer godt med eksisterende arkitektur. Alternativ C kan vurderes som et raskt første steg.

## Relatert

- `cloudflare-worker/oauth-worker.js` – eksisterende CF Worker som kan utvides
- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html` – `openQuillEditDialog()`
- Veikart: [Bygg-status og Lukk-knapp](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/veikart/bygg-status-sperre/) – beslektet problem
