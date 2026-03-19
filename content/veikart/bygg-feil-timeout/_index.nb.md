---
id: 525385db-0ade-4ad8-82ab-235951af786e
title: "Falsk «Build job failed» ved lange byggejobber"
linkTitle: "Falsk byggefeil ved timeout"
weight: 85
status: "Ny"
lastmod: 2026-03-18T20:37:02+01:00
last_editor: Erik Hagen

---

Pending-indikatoren rapporterer «Build job failed» etter at ETag-pollingen har nådd maksimumsantall forsøk – selv om bygget faktisk fortsatt kjører eller har fullført vellykket. Tidsgrensen (180 forsøk × ~1 sek = 3 min) er ikke en pålitelig proxy for byggefeil.

## Rotårsak

`startGhPoll()` / ETag-pollingen i `custom-footer.html` teller forsøk og gir opp etter en fast grense:

```javascript
if (++attempts > 180) {
    // viser "Build job failed"
}
```

Dette er en timeout-heuristikk, ikke en faktisk statussjekk. Bygg som tar over 3 minutter (f.eks. ved mange modulrepoer, treg runner eller kø) vil alltid utløse falsk feil.

## Riktig løsning

Erstatt timeout-logikken med en direkte sjekk mot GitHub Actions API. Rapporter feil kun hvis GitHub selv sier `conclusion: failure` (eller `cancelled` uten etterfølgende suksess).

### Foreslått flyt

1. ETag-poll oppdager at siden er endret (bygg ferdig) → fortsett som i dag
2. ETag-poll når maksimumsgrense → **ikke** rapporter feil direkte
3. I stedet: gjør ett kall mot `/repos/SAMT-X/samt-bu-docs/actions/workflows/hugo.yml/runs?per_page=1`
4. Sjekk `conclusion` på siste run:
   - `success` → vis «Endringer publisert», last inn siden
   - `failure` → vis feilmelding
   - `null` (kjører fortsatt) → nullstill teller og fortsett å polle
   - `cancelled` → håndter som i dag (vent på nytt bygg)

### Alternativ forenkling

Fjern maksimumsgrensen helt og stol utelukkende på GitHub API-polling (`checkCompletions()` / `startGhPoll()`). ETag-poll er kun for å oppdage at siden faktisk er oppdatert – ikke for å detektere feil.

## Relatert

- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html` – `startGhPoll()`, ETag-pollingen, `checkCompletions()`
- Veikart: [Statusrapportering og bygg-køer](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/veikart/statusrapportering-gui/) – bakgrunn for nåværende polling-arkitektur
