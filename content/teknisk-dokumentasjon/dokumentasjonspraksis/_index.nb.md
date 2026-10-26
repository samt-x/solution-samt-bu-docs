---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: b8bf5c67-7a5f-4de5-a3f4-232e7e60e725
title: Dokumentasjonspraksis
linkTitle: Dokumentasjonspraksis
weight: 30
lastmod: 2026-10-25T22:01:18+01:00
last_editor: Erik Hagen

---
Vi utvikler beste praksis for dokumentasjon gjennom gode eksempler – ikke ved å låse oss til en rigid mal fra start. Denne siden samler erfaringer og mønstre etter hvert som de trer frem.

## Dokumentasjon følger endringen

Fast regel fra 2026-10-25: **Hver endring i funksjonalitet skal vurderes mot dokumentasjonen**, enten den løser et issue eller ikke. Det gjelder også endringer i tema, bygg (CI), skript, oppgavestyring og oppsett i GitHub-organisasjonen.

Vurder og oppdater i samme arbeidsøkt som endringen:

| Hva | Hvor |
| --- | --- |
| **Løsningsdokumentasjonen** – hvordan det virker | Teknisk dokumentasjon for løsningen, for eksempel denne seksjonen eller [Oppgavestyring](/prosjektleveranser/loesninger/samhandlingsplattform/oppgavestyring/) |
| **Brukerveiledningen** – hva brukeren ser og gjør | [Brukerveiledning](../../brukerveiledning/) |
| **Annet som berøres** | Veikart, README, instruksjoner for Claude (`CLAUDE.md`) |

Sidene på nettstedet oppdateres **på norsk og engelsk**.

**Fortløpende, ikke samlet opp.** Dokumentasjonen skrives når endringen er **i bruk**, ikke etter hvert mellomsteg og ikke samlet til slutten av arbeidsøkta. En endring er live med en gang, og detaljene er lettest å få riktig mens de er ferske. Mens en utforming fortsatt diskuteres, venter dokumentasjonen.

**Når noe får nytt navn** (en type, et felt, en side, et repo …), søk etter det gamle navnet i innholdet i **alle** innholdsrepoene, ikke bare der det er kjent at det står.

**Kontrollen skrives ned.** Når et issue lukkes, har sluttkommentaren en linje som begynner med **«Dokumentasjon:»**. Den lenker til det som er oppdatert, eller sier hvorfor ingenting måtte endres. Uten den linjen er issuet ikke ferdig.

## Tilnærming

Strukturen på en dokumentasjonsside bør gjenspeile innholdstypen. For beslutningsdokumentasjon (som veikart-elementer) har vi latt oss inspirere av [ADR-formatet (Architecture Decision Records)](https://adr.github.io/), tilpasset vårt behov.

Første eksempel på dette mønsteret: [Legg til underkapittel – valg i Endre-menyen](../../veikart/legg-til-underkapittel/).

## Fremvoksende mønster: beslutningsdokumentasjon

Brukes for veikart-elementer og andre valg der det er nyttig å dokumentere *hvorfor*, ikke bare *hva*.

| Kapittel | Innhold |
| --- | --- |
| **Bakgrunn** | Behovet som skal løses – kort og konkret |
| **Valgt løsning** | Hva vi har bestemt oss for, inkl. gjenstående arbeid |
| **Alternativer vurdert** | Andre løsninger som ble vurdert, uten vurdering |
| **Begrunnelse** | Hvorfor valgt løsning ble foretrukket fremfor alternativene |

> Dette er ikke en bindende mal – det er et startpunkt. Juster strukturen der innholdet krever det, og oppdater denne siden når mønsteret utvikler seg.
