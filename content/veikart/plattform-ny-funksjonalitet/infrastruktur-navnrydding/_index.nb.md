---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: c5145be6-1a5d-42bb-b037-54bfed670ed6
title: "Navnerydding: infrastruktur og tjenester"
linkTitle: "Infrastruktur – navnrydding"
weight: 126
status: "Ny"
# Gyldige verdier: Ny | Tidlig utkast | Pågår | Til QA | Godkjent | Avbrutt
lastmod: 2026-04-19T14:07:55+02:00
last_editor: Erik Hagen

---

Det er i dag en inkonsistens mellom navn på nettstedet, infrastrukturkomponenter og OAuth-app. Dette bør ryddes opp i en samlet gjennomgang.

## Inkonsistenser

| Komponent | Nåværende navn | Ønsket retning |
|-----------|---------------|----------------|
| Nettsted | SAMT-BU Docs (`samt-bu-docs.pages.dev`) | Beholdes – spesifikt for dette prosjektet |
| Cloudflare Worker | `samt-bu-cms-auth.erik-hag1.workers.dev` | Bør flyttes og evt. omdøpes (se også «OAuth-infrastruktur – org») |
| GitHub OAuth App | «SAMT-X Docs» (eies av `samt-x`-org) | Generisk for hele org – greit som det er |

## Hva bør avklares

- Skal Worker-en hete `samt-bu-auth` (prosjektspesifikk) eller `samt-x-auth` (generisk for org)?
- Hvis én Worker skal betjene flere fremtidige nettsted under SAMT-X, bør den ha et generisk navn
- Callback URL i OAuth App må oppdateres om Worker-en får nytt domene

## Avhengighet

Bør koordineres med «Flytt OAuth-infrastruktur til organisasjonskonto».
