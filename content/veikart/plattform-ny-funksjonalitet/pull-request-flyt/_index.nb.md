---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: 88a7cc4a-b428-488f-b159-1696bbc68594
title: "Pull request-støtte i Endre-menyen"
linkTitle: "Pull request-flyt"
weight: 95
status: "Til QA"
lastmod: 2026-04-24T16:38:14+02:00
last_editor: Erik Hagen

---

Brukere uten direkte push-tilgang til repoet kan bidra via det innebygde grensesnittet ved å sende forslag som pull requests i stedet for direktecommit til `main`.

## Implementert

### Rettighetssjekk og branch-oppretting

| Funksjon | Plassering | Beskrivelse |
|----------|------------|-------------|
| `checkCollaboratorPermission(repo, callback)` | `custom-footer.html` | GitHub API `GET /repos/SAMT-X/<repo>/collaborators/<login>` – 204 = write-tilgang, annet = bare-leser. Resultat caches 1 time i localStorage (`samtu-perm-<repo>`). |
| `makePrBranch()` | `custom-footer.html` | Genererer branch-navn: `<login>/suggest-<åååå><mm><dd>-<hh><mm><ss>`. |
| `createPr(token, repo, branchName, title, body)` | `custom-footer.html` | `POST /repos/SAMT-X/<repo>/pulls`, returnerer PR-objekt med `html_url`. |
| `ensureForkReady(token, repo)` | `custom-footer.html` | Sjekker om fork finnes → oppretter om ikke → synkroniserer `main` med upstream. Venter maks 20 × 2 sek = 40 sek på ny fork. |

### Meny-tilpasning

Når Endre-menyen åpnes og brukeren mangler write-tilgang, omdøpes alle menyitems i sanntid (via `checkCollaboratorPermission`):

| Original tekst | Foreslå-tekst |
|----------------|---------------|
| Rediger dette kapitlet | Foreslå endring av dette kapitlet |
| Edit this chapter | Suggest change to this chapter |
| Nytt kapittel etter dette | Foreslå nytt kapittel etter dette |
| New chapter after this | Suggest new chapter after this |
| Nytt underkapittel | Foreslå nytt underkapittel |
| New sub-chapter | Suggest new sub-chapter |
| Slett denne siden | Foreslå sletting av denne siden |
| Delete this page | Suggest deletion of this page |

### Flyt per dialog

**Rediger-dialog (QE):** `canWrite=false` → `ensureForkReady` → commit til fork-branch → `createPr` → viser «✓ Pull request: #N» med klikkbar lenke i statusfeltet. «Lagre»-knapp blir «Sendt» (deaktivert, grønn).

**Ny side/underkapittel-dialog (NP):** `canWrite=false` → `ensureForkReady` → commit til fork-branch → `createPr` → lenke til PR vises i statusfeltet. «Opprett»-knapp blir «Sendt».

**Slett-dialog:** `canWrite=false` → `ensureForkReady` → slett-commit til fork-branch → `createPr` → heading endres til «Forslag sendt!» med PR-lenke. Bygg-polling startes ikke.

### PR-titler og -beskrivelser

| Dialog | PR-tittel (nb) | PR-tittel (en) |
|--------|---------------|---------------|
| Rediger | «Foreslår endring: \<sidetittel\>» | «Suggest change: \<title\>» |
| Ny side | «Foreslår ny side: \<tittel\>» | «Suggest new page: \<title\>» |
| Slett | «Foreslår sletting: \<sidetittel\>» | «Suggest deletion: \<title\>» |

PR-beskrivelse inkluderer brukerens GitHub-brukernavn og kilden («via SAMT-BU Docs redigeringsgrensesnitt»).

## Ikke implementert

- **Flytt-dialog** – `_mvCommit` brukes direkte uten rettighetssjekk. Lite kritisk da flytt primært er en admin-operasjon.

## Hva gjenstår / mulig videre arbeid

- **Mer testing** av fork-flyt for brukere som aldri har forket repoet – verifisere ventetid og feilhåndtering
- **Duplikat-PR** – hva skjer hvis brukeren sender to forslag etter hverandre uten at første PR er merget? GitHub avviser per i dag med feil.
- **PR-flyt i flytt-dialog** – om flytt skal bli tilgjengelig for ikke-redaktører
- **Notification til repo-eier** – i dag krever merge manuell oppfølging. Slack-varsling eller e-post er mulig fremtidig utvidelse.

## Relatert

- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html` – `checkCollaboratorPermission()`, `makePrBranch()`, `createPr()`, `ensureForkReady()`
- `themes/hugo-theme-samt-bu/layouts/partials/edit-switcher.html` – Endre-menyen og meny-tilpasnings-JS
