---
id: 1cfce35d-fbef-467a-8853-fff18ae46d28
title: "Statusrapportering og GUI for bygg-køer"
linkTitle: "Statusrapportering og bygg-køer"
weight: 130
status: "Godkjent"
last_editor: erikhag1git (Erik Hagen)
lastmod: 2026-03-18T19:58:23+01:00

---

Målbildet er å gi brukerne enkel oversikt over egne og andres jobber i kø – med en kompakt statusindikator (nederst til venstre) og en hendelsesfeed (nederst til høyre) med lyd og historikk.

## Observert oppførsel (utgangspunkt 2026-03-17, etter sesjon 5)

1. **Dialog åpen, bygg startet:** «Nettsted oppdateres (N sek)...» i dialogheaderen + lydsignal ved start. Fungerer bra.
2. **Dialog lukket / navigert:** `#qe-job-indicator` viser **alltid** en synlig knapp – «Byggehistorikk» i idle-tilstand, byggestatus under aktive bygg.
3. **Klikk på indikatoren:** Åpner jobbhistorikk-dialog med siste 15 bygg for innlogget bruker (GitHub Actions API).
4. **Ferdig bygg:** Lydsignal + automatisk navigering, uavhengig av om dialogen er åpen eller lukket.

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

## Steg 2 – Jobbhistorikk og forbedringer ✅ FULLFØRT (2026-03-17, sesjon 5)

### 2a – Jobbhistorikk-knapp alltid synlig ✅

`#qe-job-indicator` vises nå permanent (ikke bare under aktive bygg). Idle-tilstand: klokkikon + «Byggehistorikk». Klikk åpner `#job-history-dialog` med siste 15 bygg for innlogget bruker hentet fra GitHub Actions API.

**Implementasjonsdetaljer:**
- `data-building="1"` settes på indikatoren ved `samtuShowPendingIndicatorWithTotal()`, fjernes ved `samtuShowDoneIndicator()`
- Bakgrunnspollen (`setInterval` hvert 45. sek) sjekker `qeInd.dataset.building` i stedet for `display !== 'none'` – forhindrer at alltid-synlig indikator blokkerer andres-endringer-banner
- `samtuIncrementPending()` kaller nå `samtuShowPendingIndicator(newCount)` umiddelbart – indikatoren oppdateres i det du klikker Lagre, ikke først etter dialog-lukking/refresh

### 2b – Minimering fjernet ✅

Minimize-funksjonaliteten (`qe-minimize-pill`, `minimizeQeDialog()`, `⊟`-knappen) er fjernet. Begrunnelse: pillen forsvant ved navigering og ga bare støy med dobbel status. Cancel-knappen heter igjen «Lukk dette vinduet» etter lagring.

### 2c – ETag-timeout økt ✅

`if (++attempts > 90)` → `if (++attempts > 180)` (3 min maks). Fikser falsk «Build job failed»-signal ved bygg som tar > 90 sek.

**Filer endret (sesjon 5):**
- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html`
- `themes/hugo-theme-samt-bu/layouts/partials/edit-switcher.html`

---

## Steg 3 – Sekundtelling, køstatus og avløst-håndtering ✅ FULLFØRT (2026-03-17, sesjon 6)

### 3a – Sekundtelling for kjørende jobber ✅

Kjørende jobb (`status: in_progress`) viser nå antall sekunder siden start (f.eks. «47 sek»). Oppdateres live hvert sekund via en re-render-timer i historikk-dialogen (ingen ny API-fetch – beregnes fra `run.created_at`).

### 3b – «I kø»-status for ventende jobber ✅

Jobber i kø (`status: queued`, `waiting`, `pending`, `requested`) viser nå:
- Klokkeikon (grå `fa-clock-o`) i stedet for spinner
- Teksten «I kø» i stedet for «kjører…» eller et tidsstempel

GitHub Pages-miljøet bruker `waiting` i tillegg til `queued` for jobber som venter på concurrency-gruppen. Begge (og `pending`/`requested`) behandles nå likt.

### 3c – Avløst-håndtering ✅

**Bakgrunn:** GitHub Pages kansellerer automatisk eldre jobber i kø når en nyere jobb med høyere prioritet venter («Canceling since a higher priority waiting request for pages exists»). Skjer ved 3+ raske lagringer.

**Implementert:**
- `conclusion: cancelled` → grå `fa-check-circle` (ikke rød `fa-exclamation-circle`) + teksten «Avløst»
- `checkCompletions()`: teller kansellerte som resolved, rydder hele pending-state når minst én suksess finnes og ingen aktive gjenstår – pending-teller henger aldri lenger
- `startGhPoll()`: kansellert run trigger ikke wah-wah + feilmelding, men holder polling og venter på nytt bygg
- Brukerveiledningen (om/hvordan-bidra/) oppdatert med forklaring på avløste jobber og køoppførsel

### 3d – Live-oppdatering av jobbhistorikk-dialog ✅

`loadHistory()` splittet i `fetchHistory()` + `renderHistory(runs)`:
- `renderHistory` re-rendres hvert sekund fra cache (live elapsed-teller uten API-kall)
- `fetchHistory` re-hentes automatisk hvert 15. sek mens dialogen er åpen
- `openHistory()` / `closeHistory()` rydder timere korrekt ved åpne/lukke, ESC og klikk utenfor

**Filer endret (sesjon 6):**
- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html`

---

## Steg 2 (opprinnelig) – Rikere statusinformasjon ⚠ RULLET TILBAKE (2026-03-17, sesjon 4)

*(Historisk referanse – konsepter kan gjenbrukes)*

### 2a – Elapsed + actor ⚠ RULLET TILBAKE

Utviklet og testet, men rullet tilbake pga. bugs i kombinasjon med 2b/2c. Kode tilgjengelig på commit `9593675` i `hugo-theme-samt-bu`. Kan rulles frem med `git reset --hard 9593675 && git push --force` i temaet, etterfulgt av submodule-oppdatering i `samt-bu-docs`.

**Kjente bugs som må løses før re-deploy:**

1. **Race-condition:** `pollQeBuild` (ETag-poll i dialogen) og `checkCompletions` (GitHub API-poll ved sideinnlasting) kjører parallelt på siste lagrede side. Begge dekrementerer pending-teller, `seenCompleted` blir feil.
2. **ETag-banner etter eget bygg:** Etter at pending-state ryddes og siden lastes inn på nytt, oppdager ETag-poll at siden er endret (av *vårt eget* bygg) og viser «Siden er oppdatert» som om det er andres endring. Delvis fikset med `sessionStorage._samtuOwnBuildDone`, men ikke tilstrekkelig testet.
3. **Stuck count ved flere samtidige bygg:** Pending-teller nådde aldri 0 ved 4 raske lagringer i sekvens.

**Anbefalt tilnærming ved re-implementering:**
- Fjern `seenCompleted`-logikken helt fra `checkCompletions`
- Bruk «kø-tom»-strategi: når `inProgress=0 && queued=0 && myCompleted > 0` → alt ferdig, rydd opp og last inn
- Sørg for at `checkCompletions` IKKE starter hvis `_samtuDialogPollActive` er satt

`samtuShowPendingIndicatorWithTotal` viser nå:

| Scenario | Tekst |
|---|---|
| 1 endring, kjører | `⟳ Din endring bygges · 45 sek` |
| 1 endring, i kø | `⟳ Din endring i kø · 12 sek` |
| N endringer, alle kjører | `⟳ N endringer bygges · 1 min` |
| N kjører, M i kø | `⟳ N bygges · M i kø · 55 sek` |

Elapsed beregnes fra `pending.lastSaveAt` og oppdateres automatisk hvert 3. sek (samme som poll-syklusen).

### 2b – Split inProgress/queued ⚠ RULLET TILBAKE (se 2a)

`checkCompletions()` teller nå `inProgress` og `queued` separat (i stedet for `totalActive`). Fungerer uavhengig av om Cloudflare er på free-tier (1 parallell) eller Pro (5 parallelle) – GitHub Actions API reflekterer sannheten i begge tilfeller.

**Ny signatur:** `samtuShowPendingIndicatorWithTotal(count, inProgress, queued)`

### 2c – Hendelsesfeed + pling (bottom-right)

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

## Steg 4 – «Mine»/«Alle»-faner i byggehistorikk-dialog ✅ FULLFØRT (2026-03-17, sesjon 7)

Undertabs i dialog-headeren lar brukeren veksle mellom egne og alle bygg:

- **«Mine»** (standard): filtrerer på innlogget bruker via `&actor=` – samme som før
- **«Alle»**: henter alle 15 siste bygg i repoet, viser actor som sublinje per rad
- **Navnecache:** `/users/{login}` hentes én gang per unik login per sidebesøk, caches i JS-dict. Viser `login (Full Name)` når navn er tilgjengelig – krever at GitHub-profilen har Name-feltet satt
- **Tab-bytte** nullstiller cache og re-fetcher umiddelbart
- **Filer endret:** `edit-switcher.html` (HTML), `custom-footer.html` (JS)

> **Merk:** `data.name` fra GitHub API er `null` hvis brukeren ikke har satt navn i sin GitHub-profil (`github.com/settings/profile`). Visningsnavn i Hugo-innhold (`last_editor`-feltet) er manuelt satt og ikke koblet til GitHub-profilen.

---

## Steg 5 – Overordnet statusoversikt for alle brukere

**Status:** Vurderes – settes evt. på roadmap

Sanntidsoversikt over alle aktive bygg på tvers av brukere. Polling av GitHub Actions API + presentasjon av `triggering_actor.login` per run. Mulig implementasjon: klikk på indikatoren åpner dropdown med alle aktive runs.

**Avhengighet:** Krever GitHub-token (allerede tilgjengelig for innloggede brukere).

---

## Teknisk kontekst

Nøkkelfunksjoner i `custom-footer.html`:

| Funksjon | Signatur | Rolle |
|----------|----------|-------|
| `samtuIncrementPending()` | – | Øker pending-teller i localStorage **og oppdaterer indikatoren umiddelbart** |
| `samtuDecrementPending()` | – | Kalles ved ferdig bygg – reduserer teller |
| `samtuShowPendingIndicator(count)` | – | Shorthand, kaller under med `null` |
| `samtuShowPendingIndicatorWithTotal` | `(count, totalActive)` | Oppdaterer `#qe-job-indicator` med tekst + setter `data-building="1"` |
| `samtuShowDoneIndicator()` | – | Viser «Endringer publisert – klikk for å laste inn» + fjerner `data-building` |
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

**`#qe-job-indicator`** (bottom-left, alltid synlig): Idle → klokkikon + «Byggehistorikk». Under bygg → spinner + «N endringer bygges». Ferdig → lenke «Endringer publisert – klikk for å laste inn». Klikk åpner `#job-history-dialog`. Bakgrunnspoll bruker `data-building`-attributtet for å unngå konflikt med andres-endringer-deteksjon.

**`#page-update-banner`** (bottom-right, grønn): ETag-basert bakgrunnspolling hvert 45. sek. Vises kun ved andres endringer (når ingen egne pending). Kandidat for erstatning av hendelsespill i fremtidig steg (se Steg 3).
