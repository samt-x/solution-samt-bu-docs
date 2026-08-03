---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: "c95d738e-1fe5-43ac-94a8-80202e0a2faa"
title: Innebygd redigering i nettleseren
linkTitle: Innebygd redigering
weight: 5
aliases:
  - /om/hvordan-bidra/innebygd-redigering/
  - /hvordan-bidra/innebygd-redigering/
lastmod: 2026-08-04T01:11:46+02:00
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
2. Gå til  **Innstillinger** (klikk på profilbildet øverst til høyre → *Settings*)
3. Velg  **Applications** i venstremenyen
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

**Skrivetilgang:** Endringen publiseres direkte. **Uten skrivetilgang:** Det opprettes automatisk et endringsforslag (pull request). Du ser «Foreslå endring av dette kapitlet» i stedet for «Rediger denne siden» i menyen, og etter lagring vises en lenke til forslaget. En redaktør ser over og godkjenner.

Nettstedet oppdateres automatisk etter lagring. En statusindikator nede til venstre i skjermen holder deg oppdatert underveis.

## Bilder

Bilder limes direkte inn i tekstfeltet (Ctrl+V). De lastes automatisk opp og kobles inn i siden.

PNG anbefales for skjermbilder og diagrammer, JPEG for fotografier.

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

## Gi tilbakemelding

Bruk **«Gi kommentar»** i Endre-menyen for å sende et innspill uten å redigere direkte. Kommentaren registreres som en GitHub Issue knyttet til siden.

## Statusindikator og jobbhistorikk

Indikatoren nede til venstre viser byggstatus. Normalt tar et bygg **ca. 1 minutt**.

| Tilstand | Tekst |
| --- | --- |
| Ingen pågående jobb | «Byggehistorikk» |
| Venter på bygg | «N endringer bygges…» |
| Ferdig | «Endringer publisert – klikk for å laste inn» |

> Ser du «Avløst» i jobbhistorikken, er ikke endringen tapt – den ble publisert av en nyere jobb.

## Forslagsflyt for brukere uten skrivetilgang

Brukere med GitHub-konto men uten direkte skrivetilgang til repoet kan bidra gjennom nøyaktig samme grensesnitt. Systemet oppdager rettighetsnivået automatisk når Endre-menyen åpnes, og tilpasser menynavnene:

| Med skrivetilgang | Uten skrivetilgang |
| --- | --- |
| Rediger denne siden | Foreslå endring av denne siden |
| Nytt kapittel etter dette | Foreslå nytt kapittel etter dette |
| Nytt underkapittel | Foreslå nytt underkapittel |
| Slett denne siden | Foreslå sletting av denne siden |

I stedet for å committe direkte til `main` oppretter systemet automatisk en branch og et forslag. Etter lagring vises en bekreftelse med lenke til forslaget.

> **Merk:** «Flytt dette kapitlet» støtter ikke forslagsflyt og er kun tilgjengelig for brukere med skrivetilgang.

**Du blir ikke varslet når du sender inn.** Det kommer én e-post, og den kommer først når forslaget er behandlet – enten godkjent eller lagt bort. Du trenger ikke gjøre noe med den; alt er allerede gjort.

## For redaktører – behandle innkomne forslag

Velg **«Behandle forslag»** under Prosjekt i Endre-menyen. Punktet vises kun for brukere med skrivetilgang.

Dialogen viser alle åpne forslag på tvers av alle innholdsrepoene, med hvem som har sendt inn og når. For hvert forslag kan du godkjenne eller avslå, begge deler med en bekreftelse i to trinn.

Du trenger altså ikke gå til GitHub for å behandle forslag.

Når du har valgt, skjer tre ting automatisk:

1. Forslaget får en forklarende tittel, slik at e-posten til bidragsyteren har et emnefelt som gir mening
2. Endringen tas inn, og nettstedet bygges på nytt
3. En vennlig melding legges igjen til bidragsyteren – **et par minutter senere**, ikke med det samme

Forsinkelsen er med vilje: legges meldingen ut umiddelbart, får bidragsyteren to e-poster i stedet for én. Du trenger ikke vente eller holde fanen åpen – meldingen ligger i kø og sendes selv om du lukker nettleseren.

**Er forslaget i konflikt** med innhold som er endret i mellomtiden, kan det ikke slås sammen automatisk. Da må det foreløpig løses i GitHub.

## Tospråklig redigering

Nettstedet er tospråklig (norsk og engelsk). Hver side finnes i to versjoner – én norsk og én engelsk – koblet via et felles UUID-felt. Når du oppretter eller redigerer en side, endrer du kun én språkversjon om gangen.

**Anbefalt arbeidsflyt for ny side:**

1. Opprett siden på norsk (via «Nytt kapittel» eller «Nytt underkapittel»)
2. Legg til norsk innhold og lagre
3. Bytt til engelsk via språkvelgeren i headeren
4. Åpne den tilsvarende engelske siden og rediger på samme måte

Flytt-funksjonen og sletting opererer på begge språkversjoner samtidig – én handling dekker begge.

## Statusfeltet – kun for use cases

Use case-sider (under «Behov») har et statusfelt som styrer symbolet i menyen. Øvrige sider skal ha tomt statusfelt.

| Symbol | Norsk verdi | Engelsk verdi |
| --- | --- | --- |
| ◍ | Ny | New |
| ◔ | Tidlig utkast | Early draft |
| ◐ | Pågår | In progress |
| ◕ | Til QA | For QA |
| ⏺ | Godkjent | Approved |
| ⨂ | Avbrutt | Cancelled |

## UUID-feltet – ikke rør det

Alle sider har et skjult `id`-felt (UUID). Det er usynlig i redigeringsdialogen og settes automatisk. UUID-en er permanent og kobler norsk og engelsk versjon av samme side. Du trenger aldri tenke på det.

## Sorteringsrekkefølge (`weight`)

`weight`-feltet bestemmer rekkefølgen i sidebarmenyen. Lavere tall = høyere opp. Bruk tioer-trinn (10, 20, 30 …) for å gi rom til seinere innskudd.

## Rapporter feil

Opplever du noe som ikke fungerer som det skal? Bruk **«Gi kommentar»** i Endre-menyen og beskriv hva som skjedde. Rapporten registreres som en sak og følges opp av teamet.

> Et dedikert «Rapporter feil»-menyvalg er under planlegging.
