---
id: b8bf5c67-7a5f-4de5-a3f4-232e7e60e725
title: Dokumentasjonspraksis
linkTitle: Dokumentasjonspraksis
weight: 30
lastmod: 2026-03-27T23:29:13+01:00
last_editor: Erik Hagen

---
Vi utvikler beste praksis for dokumentasjon gjennom gode eksempler – ikke ved å låse oss til en rigid mal fra start. Denne siden samler erfaringer og mønstre etter hvert som de trer frem.

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
