---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: c794131f-0639-4f6f-b87e-4031deea5a65
title: "«Gi kommentar» i Endre-menyen via GitHub Issues"
linkTitle: "Gi kommentar (issues)"
weight: 96
status: "Ny"
# Gyldige verdier: Ny | Tidlig utkast | Pågår | Til QA | Godkjent | Avbrutt
lastmod: 2026-04-19T18:06:04+02:00
last_editor: Erik Hagen

---

Et nytt menyvalg «Gi kommentar» i Endre-menyen lar innloggede brukere sende tilbakemelding på en side uten å redigere innholdet direkte. Kommentaren opprettes som en GitHub Issue i riktig repo.

## Brukerflyt

1. Bruker klikker «Gi kommentar» i Endre-menyen
2. En enkel dialog åpnes med et fritekstfelt
3. Tittel forhåndsutfylles med sidetittel og lenke til siden
4. Ved innsending: `POST /repos/SAMT-X/{repo}/issues` oppretter issue
5. Bruker ser bekreftelse med lenke til den opprettede issue-en

## Teknisk

- Samme autentisering og rettighetsmønster som øvrige operasjoner
- Krever kun at brukeren er innlogget – ikke nødvendigvis skrivetilgang til repoet
- GitHub Issues er åpne for alle autentiserte brukere å opprette (om repo har issues aktivert)
- Forhåndsutfylt body: sidetittel + URL + fritekst fra bruker

## Relatert

- Kan kombineres med varsling ved merge-konflikter i PR-flyten
- Grunnlag for fremtidig «Admin»-svitsjer som viser åpne issues per side
