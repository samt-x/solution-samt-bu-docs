---
id: 6424458e-9066-47e6-9412-47278d236735
title: "Statusrapportering og GUI for bygg-køer"
linkTitle: "Statusrapportering og bygg-køer"
weight: 130
status: "Pågår"
last_editor: erikhag1git (Erik Hagen)

---

Målbildet er å gi brukerne enkel oversikt over egne og andres jobber i kø – med en kompakt statusindikator (nederst til venstre) og en hendelsesfeed (nederst til høyre) med lyd og historikk.

## Observert oppførsel (utgangspunkt 2026-03-17)

1. **Dialog åpen, bygg startet:** «Nettsted oppdateres (N sek)...» i dialogheaderen + lydsignal ved start. Fungerer bra.
2. **Dialog lukket, samme side:** `#qe-job-indicator` viser generisk tekst – ingen info om hvem, tid eller antall.
3. **Navigert til ny side mens bygg pågår:** Indikatoren viser enkel teller uten skille mellom kjørende og ventende, og uten elapsed-tid.
4. **Bug – lyd uteblir etter navigering:** Lydsignalet for «ferdig bygg» spilles ikke når brukeren har navigert til en ny side.

---

## Steg 1 – Lydsignal ved ferdig bygg etter navigering ✅ FULLFØRT (2026-03-17)

**Rotårsak (løst):**

1. `samtuPlaySuccess()` ble aldri kalt i `checkCompletions()` completion-branchen.
2. `_samtuAudioCtx` var `null` på ny side (opprettes kun under brukergestus på forrige side).

**Implementert fix:**

- `checkCompletions()` completion-branch kaller nå `samtuPlaySuccess()` + 1800ms forsinkelse før reload.
- `_samtuPlayNotes()` forsøker å opprette ny `AudioContext` hvis den er `null` (Chrome tillater dette for origins med høy brukerengasjement).
- `samtuShowDoneIndicator()` vises alltid som visuell fallback.

**Filer endret:**
- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html`

---

## Steg 2 – Rikere statusinformasjon (bottom-left) ← PÅGÅR

### 2a – Elapsed + actor ✅ FULLFØRT (2026-03-17)

`samtuShowPendingIndicatorWithTotal` viser nå:

| Scenario | Tekst |
|---|---|
| 1 endring, kjører | `⟳ Din endring bygges · 45 sek` |
| 1 endring, i kø | `⟳ Din endring i kø · 12 sek` |
| N endringer, alle kjører | `⟳ N endringer bygges · 1 min` |
| N kjører, M i kø | `⟳ N bygges · M i kø · 55 sek` |

Elapsed beregnes fra `pending.lastSaveAt` og oppdateres automatisk hvert 3. sek (samme som poll-syklusen).

### 2b – Split inProgress/queued ✅ FULLFØRT (2026-03-17)

`checkCompletions()` teller nå `inProgress` og `queued` separat (i stedet for `totalActive`). Fungerer uavhengig av om Cloudflare er på free-tier (1 parallell) eller Pro (5 parallelle) – GitHub Actions API reflekterer sannheten i begge tilfeller.

**Ny signatur:** `samtuShowPendingIndicatorWithTotal(count, inProgress, queued)`

### 2c – Hendelsesfeed + pling (bottom-right) ← NESTE

**Konsept:** Skille mellom *status* (bottom-left, pågående tilstand) og *hendelser* (bottom-right, ting som har skjedd).

**Bottom-right – hendelsespill:**
- Viser siste hendelse som kompakt pill: `🔔 Erik Hagen endret /om-samt-bu (2 min siden)`
- Klikk → dropdown med siste 5–10 hendelser (lagret i localStorage)
- Pling-lyd (én note) ved andres hendelse; fanfare ved egen (eksisterende)
- Erstatter dagens grønne `#page-update-banner` (som bare viser "Siden er oppdatert" uten kontekst)

**Datakilder:**
- Egne hendelser: allerede kjent (actor, url, tidspunkt fra pending-state)
- Andres hendelser: ETag-polling oppdager endring → API-kall mot `/actions/runs?status=completed&per_page=3` for `triggering_actor.login`

**Filer som endres:**
- `custom-footer.html`: ETag-poll → event-log + pling
- `edit-switcher.html`: nytt HTML-element for pill + dropdown

---

## Steg 3 – Overordnet statusoversikt for alle brukere

**Status:** Vurderes – settes evt. på roadmap

Sanntidsoversikt over alle aktive bygg på tvers av brukere. Polling av GitHub Actions API + presentasjon av `triggering_actor.login` per run. Mulig implementasjon: klikk på indikatoren åpner dropdown med alle aktive runs.

**Avhengighet:** Krever GitHub-token (allerede tilgjengelig for innloggede brukere).

---

## Teknisk kontekst

Nøkkelfunksjoner i `custom-footer.html`:

| Funksjon | Signatur | Rolle |
|----------|----------|-------|
| `samtuIncrementPending()` | – | Kalles ved Lagre – øker pending-teller i localStorage |
| `samtuDecrementPending()` | – | Kalles ved ferdig bygg – reduserer teller |
| `samtuShowPendingIndicator(count)` | – | Shorthand, kaller under med `null, null` |
| `samtuShowPendingIndicatorWithTotal` | `(count, inProgress, queued)` | Oppdaterer `#qe-job-indicator` med rik tekst |
| `samtuShowDoneIndicator()` | – | Viser «Endringer publisert – klikk for å laste inn» |
| `samtuPlaySuccess()` | – | Spiller seiersfanfare + tale |
| `samtuUnlockAudio()` | – | Låser opp AudioContext under brukergestus |
| `startGhPoll()` | – | GitHub Actions-polling (kjøres på siden der Lagre ble klikket) |
| `checkCompletions()` | – | Resume-polling ved sideinnlasting (kjøres på ny side) |

**`localStorage`-pending-state:**
```json
{
  "count": 1,
  "firstSaveAt": 1710638400000,
  "lastSaveAt": 1710638400000,
  "seenCompleted": 0,
  "actor": "erikhag1git"
}
```

**`#page-update-banner`** (bottom-right, grønn): ETag-basert bakgrunnspolling hvert 45. sek. Vises kun ved andres endringer (når ingen egne pending). Skal erstattes av hendelsespill i steg 2c.
