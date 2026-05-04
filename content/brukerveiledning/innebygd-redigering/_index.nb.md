---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: "c95d738e-1fe5-43ac-94a8-80202e0a2faa"
title: "Innebygd redigering i nettleseren"
linkTitle: "Innebygd redigering"
weight: 5
aliases:
  - /om/hvordan-bidra/innebygd-redigering/
  - /hvordan-bidra/innebygd-redigering/
lastmod: 2026-05-04T22:59:22+02:00
last_editor: Erik Hagen

---

Du redigerer innhold direkte i nettleseren i et visuelt tekstverktøy – ingen Markdown- eller Git-kunnskap nødvendig. Alle vanlige redaktøroppgaver er tilgjengelige fra **«Endre»**-menyen øverst til høyre i headeren.

## Hva du trenger

- En **GitHub-konto** (opprett gratis på [github.com](https://github.com)) – det er alt som trengs

**Skrivetilgang er ikke nødvendig.** Uten skrivetilgang sendes endringene dine som et *endringsforslag* (pull request) som en redaktør ser over og godkjenner. Med skrivetilgang publiseres endringen direkte. I begge tilfeller brukes nøyaktig samme grensesnitt – menynavnene tilpasses automatisk.

### Om GitHub-autorisasjonen

Første gang du bruker redigeringsfunksjonene, ber SAMT-BU Docs om tilgang til GitHub-kontoen din via en innloggingspopup. SAMT-BU Docs bruker en **GitHub App** som kun har tilgang til de spesifikke repoene appen er installert på – ikke andre repositorier på kontoen din.

#### Trekke tilbake autorisasjonen

Du kan når som helst trekke tilbake tilgangen:

1. Logg inn på [github.com](https://github.com)
2. Gå til **Innstillinger** (klikk på profilbildet øverst til høyre → *Settings*)
3. Velg **Applications** i venstremenyen
4. Klikk på fanen **Authorized GitHub Apps**
5. Finn **SAMT-BU Docs** i listen og klikk **Revoke**

Etter at du har tilbakekalt tilgangen, vil du bli bedt om å logge inn på nytt neste gang du bruker redigeringsfunksjonene.

## Redigere en eksisterende side

1. Gå til siden du vil redigere
2. Klikk **«Endre»**-menyen øverst til høyre i headeren
3. Velg **«Rediger denne siden»**
4. Logg inn med GitHub-kontoen din hvis du ikke allerede er innlogget (popup-vindu)
5. Gjør endringene dine i det visuelle tekstverktøyet
6. Klikk **«Lagre»**

**Tips:** Bilder kan limes direkte inn i tekstfeltet (Ctrl+V eller høyreklikk → Lim inn).

**Skrivetilgang:** Endringen publiseres direkte. **Uten skrivetilgang:** Det opprettes automatisk et endringsforslag (pull request). Du ser «Foreslå endring av dette kapitlet» i stedet for «Rediger denne siden» i menyen, og etter lagring vises en lenke til forslaget. En redaktør ser over og godkjenner.

Nettstedet oppdateres automatisk etter lagring. En statusindikator nede til venstre i skjermen holder deg oppdatert underveis.

## Opprette en ny side

1. Gå til siden du vil plassere den nye siden ved siden av (søsken) eller under (underkapittel)
2. Klikk **«Endre»** og velg:
   - **«Nytt kapittel etter dette»** – ny side på samme nivå som den du er på
   - **«Nytt underkapittel»** – ny side ett nivå ned under den du er på
3. Fyll inn tittel og eventuelt innhold i dialogen
4. Klikk **«Lagre»**

Uten skrivetilgang vises «Foreslå nytt kapittel etter dette» / «Foreslå nytt underkapittel» i stedet. Forslaget sendes som en pull request og en lenke vises etter at du har klikket «Lagre».

## Flytte et kapittel

1. Gå til siden du vil flytte
2. Klikk **«Endre»**-menyen øverst til høyre
3. Velg **«Flytt dette kapitlet»** – en dialog åpnes og Endre-menyen grås ut
4. Naviger i menyen til stedet du ønsker
5. Klikk **«Flytt hit (før)»** for å plassere det før valgt side, eller **«Flytt hit (etter)»** for å plassere det etter

> **Merk:** Flytt-funksjonen krever skrivetilgang og støtter ikke forslagsflyt (pull request).

## Slette en side

1. Gå til siden du vil slette
2. Klikk **«Endre»**-menyen øverst til høyre
3. Velg **«Slett denne siden»**
4. Bekreft i dialogen

Siden og begge språkversjoner (norsk og engelsk) slettes i ett og samme trinn.

Uten skrivetilgang vises «Foreslå sletting av denne siden» i stedet.

> **Merk:** Sletting er ikke umiddelbart reverserbart via grensesnittet. Kontakt en administrator ved feilsletting.

## Videre lesing

For mer avanserte emner – forslagsflyt, tospråklig redigering, bilder og fallgruver – se [Avansert bruk](avansert/).

## Gi tilbakemelding

Bruk **«Gi kommentar»** i Endre-menyen for å sende et innspill uten å redigere direkte. Kommentaren registreres som en GitHub Issue knyttet til siden.

## Statusindikator og jobbhistorikk

Indikatoren nede til venstre viser byggstatus. Normalt tar et bygg **ca. 1 minutt**.

| Tilstand | Tekst |
|----------|-------|
| Ingen pågående jobb | «Byggehistorikk» |
| Venter på bygg | «N endringer bygges…» |
| Ferdig | «Endringer publisert – klikk for å laste inn» |

> Ser du «Avløst» i jobbhistorikken, er ikke endringen tapt – den ble publisert av en nyere jobb.
