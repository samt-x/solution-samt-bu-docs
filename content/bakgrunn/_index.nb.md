---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: 4fe26ad6-aa99-46b9-b522-b5f8bfa09bf7
title: "Bakgrunn og begrunnelse"
linkTitle: "Bakgrunn"
weight: 5
lastmod: 2026-05-04T18:20:02+02:00
last_editor: Erik Hagen

---

Denne seksjonen forklarer behovet som lå bak utviklingen av SAMT-BU Docs, hvilke alternativer som ble vurdert, og hvorfor vi endte opp med å bygge en egentilpasset løsning.

## Behovet

SAMT-BU er et samarbeidsprosjekt på tvers av etater, forvaltningsnivåer og kommuner. Dokumentasjonsplattformen skal støtte dette samarbeidet konkret:

- **Ikke-tekniske fagpersoner** – jurister, informasjonsarkitekter, tjenestedesignere og kommuneansatte – skal kunne lese, kommentere og bidra med innhold uten å kjenne til Git eller kommandolinjeverktøy
- **Eksternt bidrag** – personer uten direkte tilgang til repoet skal kunne foreslå endringer som deretter godkjennes av prosjektgruppen
- **Tospråklighet** – nettstedet og redaktørgrensesnittet skal fungere på både norsk og engelsk, med tanke på internasjonalt samarbeid

## Vurderte alternativer

Vi evaluerte tre etablerte verktøy i kategorien *git-baserte CMS-løsninger*:

| Alternativ | Ekstern bidragsflyt | Norsk/engelsk UI | Vurdering |
|--|--|--|--|
| **Alternativ A** – forkbasert CMS | ✅ Via brukernes egne GitHub-forks | ❌ Engelsk | Testet i praksis. Ikke-tekniske brukere forvirres av fork-varsler og uventede repoer i sin GitHub-konto. For høy terskel. |
| **Alternativ B** – hostede CMS-tjenester | ✅ Via leverandørens service account | ❌ Engelsk | Løser bidragsproblemet, men er en betalt SaaS-tjeneste med lukket redaktørgrensesnitt kun på engelsk og uten mulighet for innbygging i nettstedet. |
| **Alternativ C** – CMS med påkrevd skrivetilgang | ❌ Ikke støttet | ❌ Engelsk | Støtter ikke ekstern bidragsflyt i det hele tatt. |

Ingen av alternativene dekket alle kravene samtidig.

## Valgt tilnærming

Vi bygde en egentilpasset løsning basert på mønsteret fra de beste delene av alternativene over:

- **Innebygd editor** direkte i nettstedets sider – ingen ekstern portal, ingen omplanting til annet grensesnitt
- **Worker-basert bidragsflyt** – en Cloudflare Worker oppretter branch, commit og pull request på vegne av bidragsyteren, via en dedikert bot-konto. Bidragsyteren trenger ikke skrivetilgang til repoet
- **Tospråklig redaktørgrensesnitt** – alt tekst i editordialogene finnes på norsk og engelsk, styrt av nettstedets aktive språk
- **Åpen kildekode, ingen leverandøravhengighet** – løsningen eier vi selv og kan videreutvikle fritt

## Særlig fortrinn: tospråklighet

Ingen av de etablerte verktøyene vi evaluerte tilbyr flerspråklig redaktørgrensesnitt. For SAMT-BU Docs er dette et vesentlig fortrinn: norske brukere jobber på norsk, mens internasjonale samarbeidspartnere – f.eks. ved deltakelse i initiativ som Skills Dataspace i EU – kan bruke det samme grensesnittet på engelsk.

## Mer informasjon

- [Teknisk arkitektur og nøkkelfiler](/prosjektleveranser/loesninger/cms-loesninger/samt-bu-docs/teknisk-dokumentasjon/) – detaljer om komponenter, CI/CD og oppsett
- [Veikart](/prosjektleveranser/loesninger/cms-loesninger/samt-bu-docs/veikart/) – planlagte forbedringer, inkludert fullstendig bransjebenchmark
