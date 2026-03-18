---
title: "Pull request-støtte i Endre-menyen"
linkTitle: "Pull request-flyt"
weight: 95
status: "Ny"
---

I dag krever redigering via Endre-menyen at brukeren har direkte push-tilgang til repoet. Eksterne bidragsytere – fagpersoner, pilotdeltakere og andre uten repo-tilgang – kan ikke bidra via det innebygde grensesnittet.

Pull request-støtte ville gjort det mulig for alle GitHub-brukere å foreslå endringer med samme enkle brukeropplevelse som dagens direkteflyt.

## Foreslått flyt

1. Bruker åpner redigeringsdialogen og gjør endringer som normalt
2. Ved lagring: GitHub API oppretter en ny branch (`<login>/patch-<dato>`) og committer dit i stedet for direkte til `main`
3. GitHub API oppretter deretter en pull request fra denne branchen mot `main`
4. Bruker ser bekreftelse med lenke til PR-en i stedet for bygg-indikatoren

### Deteksjon av rettigheter

GitHub API-endepunktet `GET /repos/SAMT-X/samt-bu-docs/collaborators/<login>/permission` returnerer brukerens rettighetsnivå (`admin`, `write`, `read`, `none`). Dette kan brukes til å velge flyt automatisk:

| Rettighetsnivå | Flyt |
|----------------|------|
| `write` / `admin` | Direktecommit til `main` (dagens flyt) |
| `read` / `none` | Branch + pull request |

Alternativt: alltid tilby PR-flyt som valg i dialogen, uavhengig av rettigheter.

## Teknisk gjennomførbarhet

All nødvendig funksjonalitet finnes i GitHub REST API:

| Operasjon | Endepunkt |
|-----------|-----------|
| Hent gjeldende SHA for `main` | `GET /repos/.../git/ref/heads/main` |
| Opprett branch | `POST /repos/.../git/refs` |
| Commit til branch | `PUT /repos/.../contents/<path>` med `branch`-parameter |
| Opprett PR | `POST /repos/.../pulls` |

Eksisterende `createFilesInOneCommit()` i `custom-footer.html` bruker allerede de fleste av disse – branch-støtte er i stor grad en utvidelse av det som finnes.

## Utfordringer

- **Fork-flyt:** Brukere uten lesetilgang til et privat repo må forke først. Håndteres av `POST /repos/.../forks` + commit mot fork + PR fra fork. Mer kompleks flyt.
- **Konflikthåndtering:** PR kan ha merge-konflikter som brukeren selv ikke kan løse via grensesnittet.
- **Byggestatus:** PR-bygg trigges ikke av `hugo.yml` (kun push til `main`) – pending-indikatoren gir ikke mening for PR-flyt. Bygg forekommer først etter merge.

## Prioritet

Medium – øker tilgjengelighet for bidragsytere betydelig uten å endre opplevelsen for eksisterende brukere med push-tilgang.

## Relatert

- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html` – `createFilesInOneCommit()`, `doGitHubLogin()`
- `themes/hugo-theme-samt-bu/layouts/partials/edit-switcher.html` – Endre-menyen og dialogene
