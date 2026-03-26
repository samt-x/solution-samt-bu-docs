---
id: f2ecebba-c800-416c-94fb-6e32d36576b2
title: "Pending-indikator fanger ikke opp bygg trigget utenfor nettstedets editor"
linkTitle: "Pending-indikator: eksterne bygg"
weight: 87
status: "Godkjent"
lastmod: 2026-03-21T01:11:16+01:00
last_editor: erikhag1git (Erik Hagen)

---

Pending-indikatoren nederst til venstre («1 endring bygges») oppdateres kun når brukeren lagrer via nettstedets innebygde editor – fordi den er drevet av `localStorage`-tilstand satt av `samtuIncrementPending()`. Bygg trigget utenfra – direkte commit i GitHub web-UI, lokal push, eller API-kall – vises ikke i indikatoren.

Byggehistorikk-dialogen viser derimot disse jobbene korrekt (med live sekundtelling), fordi den henter direkte fra GitHub Actions API.

## Konsekvens

En bruker som sitter på nettstedet ser «Byggehistorikk» i idle-tilstand selv om et bygg faktisk pågår. Indikatoren gir et feilaktig inntrykk av at alt er stille – og siden lastes ikke automatisk inn når bygget er ferdig.

## Foreslått løsning

Utvid bakgrunnspollingen (som allerede kjøres hvert 45. sek for ETag-endringer) til å også sjekke GitHub Actions API for aktive bygg:

1. Hent `/repos/SAMT-X/samt-bu-docs/actions/workflows/hugo.yml/runs?per_page=3&status=in_progress` (krever token)
2. Hvis det finnes aktive runs som **ikke** er i `localStorage`-pending-state (dvs. ikke trigget av denne nettleseren):
   - Oppdater indikatoren til å vise «Bygg pågår» (uten pending-teller – ikke vår endring)
   - Start URL-poll / ETag-poll for å oppdage når siden er oppdatert
   - Vis auto-reload og lydsignal som vanlig når bygget er ferdig

### Skille mellom egne og andres bygg

| Kilde | Håndtering |
|-------|-----------|
| Eget bygg (via editor) | Som i dag – `localStorage`-pending-state, teller, fanfare |
| Andres bygg (ekstern) | Ny flyt – indikator uten teller, diskret lydsignal ved ferdig |
| Eget bygg direkte i GitHub | Samme som andres bygg (ingen `localStorage`-oppføring) |

### Forutsetning

Brukeren må være innlogget (token tilgjengelig) for at bakgrunnspollingen skal kunne kalle GitHub API. For ikke-innloggede brukere: ingen endring fra dagens oppførsel.

## Implementert (2026-03-21) – tema-commit `b600033`

> **OBS – ikke testet i praksis.** Funksjonaliteten er implementert og deployet, men ikke verifisert med et faktisk eksternt bygg. Test ved å pushe en endring direkte til GitHub mens en annen nettleserfane er åpen og innlogget på nettstedet.

**Ny funksjon: `checkExternalBuilds()`** kalles fra bakgrunnspollingen hvert 45. sek (når eget bygg ikke pågår og bruker er innlogget):

1. Henter `/actions/workflows/hugo.yml/runs?per_page=3` fra GitHub API
2. Hvis aktivt bygg (`in_progress`/`queued`) finnes: viser diskret `samtuShowExternalBuildIndicator()` og starter `startBgFastPoll()` (ETag-poll hvert 5. sek)
3. `bgFastTimer` oppdager ETag-endring → auto-last inn siden (ingen banner)
4. Hvis bygg er ferdig ved neste bgTimer-tick og `bgExternalRun` er satt: auto-last inn i stedet for banner

**Visuelle detaljer:**
- Ekstern indikator: spinner + «Nettstedet oppdateres…» med `opacity: .7` (vs. full opasitet for egne bygg)
- Ekstern indikator bruker `data-external`-attributt, ikke `data-building` → hindrer ikke bakgrunnspolling
- Ingen fanfare eller lydsignal (stille auto-reload)

**Begrensning (som planlagt):** Krever innlogget bruker (token) for å kalle GitHub API. Ikke-innloggede brukere: uendret oppførsel.

## Relatert

- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html` – `checkExternalBuilds()`, `startBgFastPoll()`, `stopBgFastPoll()`, `samtuShowExternalBuildIndicator()`
- Veikart: [Falsk byggefeil ved timeout](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/veikart/bygg-feil-timeout/) – beslektet GitHub API-polling
- Veikart: [Statusrapportering og bygg-køer](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/veikart/statusrapportering-gui/) – bakgrunn
