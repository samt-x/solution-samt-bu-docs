---
title: "Statusrapportering og GUI for bygg-køer"
linkTitle: "Statusrapportering og bygg-køer"
weight: 130
status: "Pågår"
last_editor: erikhag1git (Erik Hagen)

---

Målbildet er å gi brukerne enkel oversikt over egne og andres jobber i kø – både de som venter på push og de som er åpnet for redigering – med en kompakt statusindikator (nederst til venstre) og mulighet til å klikke seg til ytterligere detaljer.

## Observert oppførsel (utgangspunkt 2026-03-17)

Tre tilstander og én bug:

1. **Dialog åpen, bygg startet:** «Nettsted oppdateres (N sek)...» i dialogheaderen + lydsignal ved start. Fungerer bra.
2. **Dialog lukket, samme side:** `#qe-job-indicator` viser «Oppdateringsjobb pågår» – generisk, ingen info om hvem, tid eller antall.
3. **Navigert til ny side mens bygg pågår:** Indikatoren viser «1 endring bygges...» (fra `samtuShowPendingIndicatorWithTotal`). Antall fra min pending-state, totalt aktive på GitHub i parentes – men ingen klar skille mellom «mine» og «andres» bygg.
4. **Bug – lyd uteblir etter navigering:** Lydsignalet for «ferdig bygg» spilles ikke når brukeren har navigert til en ny side.

---

## Steg 1 – Lydsignal ved ferdig bygg etter navigering ← NESTE

**Status:** Ikke startet

**Rotårsak:** To separate problemer:

1. `samtuPlaySuccess()` kalles **aldri** i resume-sporet. Koden i `checkCompletions()` (linje ~345–348 i `custom-footer.html`) gjør kun `samtuDecrementPending()` + `window.location.href = ...` – ingen lyd.
2. `_samtuAudioCtx` er `null` på den nye siden (opprettes kun i `samtuUnlockAudio()` ved Lagre-klikk på *forrige* side). `_samtuPlayNotes()` returnerer tidlig hvis `_samtuAudioCtx` er null.

**Planlagt fix:**

- I `checkCompletions()` completion-branchen: kall `samtuPlaySuccess()` + legg inn ~1800ms forsinkelse før `window.location.href`-reload
- I `_samtuPlayNotes()`: forsøk å opprette ny AudioContext hvis den er null (Chrome tillater dette for origins med høy brukerengasjement)
- Fallback: visuell «Endringer publisert – klikk for å laste inn»-indikator (allerede implementert i `samtuShowDoneIndicator()`) vises alltid uavhengig av om lyden spilles

**Filer som endres:**
- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html`

---

## Steg 2 – Rikere statusinformasjon

**Status:** Ikke startet

Gjeldende statustekst er for generisk. Ønsket:

- **Hvem:** Brukernavn på den som har endringen i kø (allerede lagret i `actor`-feltet i pending-state)
- **Tid:** Elapsed siden jobben ble startet (`lastSaveAt` er tilgjengelig i pending-state)
- **Mine vs. andres:** Tydelig visuell skille – f.eks. «Din endring bygges (45 sek)» vs. «2 andres endringer i kø»
- **Klikk for detaljer:** Indikatoren kan klikkes og vise en liten popup med full liste

**Tilgjengelige data i `localStorage`-pending-state:**
```json
{
  "count": 1,
  "firstSaveAt": 1710638400000,
  "lastSaveAt": 1710638400000,
  "seenCompleted": 0,
  "actor": "erikhag1git"
}
```

**Filer som endres:**
- `custom-footer.html`: `samtuShowPendingIndicatorWithTotal()`, `checkCompletions()`
- `edit-switcher.html`: evt. ny HTML for detaljpopup

---

## Steg 3 – Overordnet statusoversikt for alle brukere

**Status:** Vurderes – settes evt. på roadmap

Separat liten statusvisning som viser alle aktive bygg på tvers av brukere, ikke bare din. Krever polling av GitHub Actions API og presentasjon av `triggering_actor.login` per run.

Mulig implementasjon: Klikk på indikatoren åpner en liten dropdown med liste over alle aktive runs, hvem som trigget dem, og status.

**Avhengighet:** Krever GitHub-token (allerede tilgjengelig for innloggede brukere).

---

## Teknisk kontekst

Nøkkelfunksjoner i `custom-footer.html`:

| Funksjon | Rolle |
|----------|-------|
| `samtuIncrementPending()` | Kalles ved Lagre – øker pending-teller i localStorage |
| `samtuDecrementPending()` | Kalles ved ferdig bygg – reduserer teller |
| `samtuShowPendingIndicatorWithTotal(count, total)` | Oppdaterer `#qe-job-indicator` |
| `samtuShowDoneIndicator()` | Viser «Endringer publisert – klikk for å laste inn» |
| `samtuPlaySuccess()` | Spiller seiersfanfare + tale |
| `samtuUnlockAudio()` | Låser opp AudioContext under brukergestus |
| `startGhPoll()` | GitHub Actions-polling (kjøres på siden der Lagre ble klikket) |
| `checkCompletions()` | Resume-polling ved sideinnlasting (kjøres på ny side) |
