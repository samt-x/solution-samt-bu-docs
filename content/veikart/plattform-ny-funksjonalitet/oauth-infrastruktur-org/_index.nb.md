---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: aebdf240-bc40-43a5-a547-50139b0a6400
title: "Flytt OAuth-infrastruktur til organisasjonskonto"
linkTitle: "OAuth-infrastruktur – org"
weight: 125
status: "Ny"
# Gyldige verdier: Ny | Tidlig utkast | Pågår | Til QA | Godkjent | Avbrutt
lastmod: 2026-04-19T14:04:31+02:00
last_editor: Erik Hagen

---

I dag kjører Cloudflare Worker-en (`samt-bu-cms-auth.erik-hag1.workers.dev`) og GitHub OAuth App-en («Decap CMS – SAMT-X») på personlige kontoer tilknyttet én enkelt utvikler. Hvis denne personen forlater prosjektet eller bytter konto, slutter innlogging og redigering å fungere for alle brukere.

## Hva bør gjøres

1. **Cloudflare Worker** – flytt `samt-bu-cms-auth`-workeren til en delt Cloudflare-konto eller organisasjonskonto eid av SAMT-X-prosjektet
2. **GitHub OAuth App** – eksisterende «SAMT-X Docs»-app eies allerede av `samt-x`-organisasjonen ✅ – men callback URL peker på den personlige Worker-en (punkt 1 løser dette)
3. **Cloudflare API-nøkler** – oppdater GitHub Actions-secrets (`CF_ACCOUNT_ID`, `CF_API_TOKEN`) til ny konto

## Risiko ved å ikke gjøre det

- Tap av tilgang til én personlig konto → alle redaktører mister innloggingsmuligheten
- Ingen varslingsmekanisme – problemet oppdages først når brukere rapporterer at redigering ikke fungerer

## Prioritet

Lav på kort sikt (én person har kontroll), men bør gjøres før prosjektet åpnes for bredere bruk.
