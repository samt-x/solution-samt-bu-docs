---
id: f9cbe239-500e-4760-882e-e3a5dd7c3b71
title: "Bygg-status-sperre og riktig Lukk-knapp"
linkTitle: "Bygg-status og Lukk-knapp"
weight: 70
status: "Godkjent"
last_editor: erikhag1git (Erik Hagen)
lastmod: 2026-03-15T23:49:44+01:00

---

**Implementert 2026-03-12.** Begge delene er gjennomført i temaet (`custom-footer.html` og `edit-switcher.html`).

Når brukeren trykker Lagre i redigeringsdialogen, sendes en commit til GitHub og et bygg starter automatisk. Knappen som i dag heter **«Avbryt»** er misvisende fordi commiten ikke kan angres – byggejobben fortsetter uavhengig av om dialogen lukkes.

## Problem 1: «Avbryt» lover noe det ikke kan holde

Etter at brukeren har trykket Lagre bør knappen ikke lenger hete «Avbryt». Riktigere tekst: **«Lukk dette vinduet»**, supplert med en liten informasjonstekst om at jobben fortsetter i bakgrunnen selv om dialogen lukkes.

## Problem 2: Ingen advarsel når bygg pågår

Hvis en bruker (samme eller en annen) prøver å redigere en side mens en byggejobb allerede kjører på grunn av en nylig lagring på den siden, vil en ny commit enten:
- skape en **race condition** mot ensure-uuids-botten, eller
- gi en «Update is not a fast forward»-konflikt

(Vi har lagt inn automatisk retry, men det er et plaster, ikke en løsning.)

## Foreslått løsning

### Del 1 – Rename Avbryt → Lukk-knapp med forklaring

Etter at Lagre er klikket og commit er sendt:
- Knapp-tekst endres fra «Avbryt» til «Lukk dette vinduet»
- Liten grå informasjonstekst dukker opp under statusfeltet: «Jobben fortsetter i bakgrunnen. Du kan lukke dette vinduet trygt.»

### Del 2 – Bygg-status-sjekk ved åpning av redigeringsdialog

Når `openQuillEditDialog()` kalles, sjekkes GitHub Actions API for pågående bygg:

```javascript
GET /repos/SAMT-X/samt-bu-docs/actions/workflows/hugo.yml/runs?per_page=1
```

Hvis nyeste kjøring har `status: "in_progress"` eller `status: "queued"` og ble opprettet de siste ~10 minuttene:
- Vis en advarsel øverst i dialogen: «⚠ Et bygg pågår akkurat nå. Lagring kan føre til konflikt – vent til bygget er ferdig.»
- Knappen kan fremdeles brukes (ikke blokkere), men advarselen er tydelig.

### Teknisk gjennomførbarhet

| Sjekk | Metode | CORS | Token |
|-------|--------|------|-------|
| GitHub Actions runs | `GET /repos/.../actions/workflows/hugo.yml/runs` | ✅ tillatt | Brukes allerede |
| Cloudflare Pages deployments | `GET api.cloudflare.com/...` | ❌ blokkert | Ikke aktuelt |

GitHub Actions API er altså det eneste alternativet – men det holder, og brukerne er allerede innlogget med GitHub-token.

Sjekken er **kryssbruker**: hvis bruker A lagrer og bruker B åpner redigeringsdialogen sekunder senere, vil B se advarselen.

## Prioritet

Lav – automatisk retry håndterer de fleste tilfeller i praksis. Men bør gjøres for å:
- gi brukere riktig forventning om hva «Avbryt» gjør
- gjøre flerbruker-scenariet tryggere

## Relatert

- `custom-footer.html`: `openQuillEditDialog`, `pollQeBuild`, `startGhPoll`
- MEMORY.md: «Slett side med undermapper» (lignende pattern – blokkering ved ugunstig tilstand)
