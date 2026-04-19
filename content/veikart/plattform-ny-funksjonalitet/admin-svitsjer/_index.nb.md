---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: 32d0f020-7521-4c07-8fba-c84100a5f7cb
title: "Admin-svitsjer i headeren"
linkTitle: "Admin-svitsjer"
weight: 97
status: "Ny"
# Gyldige verdier: Ny | Tidlig utkast | Pågår | Til QA | Godkjent | Avbrutt
lastmod: 2026-04-19T00:00:00+02:00
last_editor: Erik Hagen

---

En egen «Admin»-dropdown i headeren for brukere med skrivetilgang, med funksjonalitet som ikke passer i den vanlige «Endre»-menyen.

## Foreslått innhold

- **PR-oversikt** – liste over åpne pull requests på tvers av alle modulrepoer (`samt-bu-docs`, `samt-bu-drafts`, `team-architecture` osv.), med merge-knapper direkte i grensesnittet
- **Build-status** – oversikt over aktive og nylige bygg i GitHub Actions
- **Moduloppdatering** – manuell trigger av `hugo mod get` + rebuild for alle moduler

## Teknisk tilnærming

- Vises kun for brukere med `write`/`admin`-rettigheter (gjenbruk `checkCollaboratorPermission`)
- GitHub API: `GET /repos/SAMT-X/{repo}/pulls` for alle aktuelle repos
- Merge via `PUT /repos/SAMT-X/{repo}/pulls/{number}/merge`
- Samme dropdown-mønster som eksisterende «Endre»- og «Innhold»-svitsjere

## Avhengighet

Forutsetter at PR-flyten («Pull request-støtte i Endre-menyen») er ferdig og i bruk.

## Prioritet

Lav – eksperimentell idé. Vurder etter at PR-flyten er grundig testet.
