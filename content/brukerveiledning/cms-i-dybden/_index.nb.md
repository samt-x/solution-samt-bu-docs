---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: 9080238f-b1aa-4a19-bc88-f27718fb6222
title: "Innebygd editor – i dybden"
linkTitle: "Innebygd editor"
weight: 10
lastmod: 2026-04-24T16:59:36+02:00
last_editor: Erik Hagen

---

Denne siden utdyper det innebygde redigeringsverktøyet i SAMT-BU Docs. Den forutsetter at du kjenner grunnprinsippene fra [Innebygd redigering](/samt-bu-docs/om/hvordan-bidra/innebygd-redigering/) og dekker emner du møter etter hvert som du bruker verktøyet mer.

## Forslagsflyt for brukere uten skrivetilgang

Brukere med GitHub-konto men uten direkte skrivetilgang til repoet kan bidra gjennom nøyaktig samme grensesnitt. Systemet oppdager rettighetsnivået automatisk når Endre-menyen åpnes, og tilpasser menynavnene:

| Med skrivetilgang | Uten skrivetilgang |
|-------------------|--------------------|
| Rediger denne siden | Foreslå endring av dette kapitlet |
| Nytt kapittel etter dette | Foreslå nytt kapittel etter dette |
| Nytt underkapittel | Foreslå nytt underkapittel |
| Slett denne siden | Foreslå sletting av denne siden |

### Hva skjer teknisk

I stedet for å committe direkte til `main` oppretter systemet automatisk:

1. En **fork** av repoet under brukerens eget GitHub-brukernavn (kun første gang – tar inntil 20–30 sek)
2. En **branch** med navn `<brukernavn>/suggest-<dato>`
3. En **pull request** fra den branchen mot `main`

Brukeren ser statusmeldingen «✓ Pull request sendt» og en klikkbar lenke til PR-en etter lagring. En redaktør med skrivetilgang ser over forslaget og godkjenner eller avviser det på GitHub.

### Begrensning: Flytt-funksjonen

«Flytt dette kapitlet» støtter ikke forslagsflyt og er kun tilgjengelig for brukere med skrivetilgang.

### Håndtere innkomne forslag (for redaktører)

Forslag vises som åpne pull requests i det aktuelle repoet på GitHub. Når du godkjenner og merger en PR, trigges nettstedets byggepipeline automatisk og endringen publiseres innen ca. 1 minutt.

## Tospråklig redigering

Nettstedet er tospråklig (norsk og engelsk). Hver side finnes i to versjoner – én norsk og én engelsk – og de to versjonene er koblet via et felles UUID-felt.

**Praktisk konsekvens:** Når du oppretter eller redigerer en side, endrer du kun én språkversjon om gangen. Den andre forblir uendret.

**Anbefalt arbeidsflyt for ny side:**

1. Opprett siden på norsk (via «Nytt kapittel» eller «Nytt underkapittel»)
2. Legg til norsk innhold og lagre
3. Naviger til den nye norske siden, klikk **«Endre»** og velg **«Rediger denne siden»**
4. Bruk språkvelgeren i headeren til å bytte til engelsk
5. Åpne den tilsvarende engelske siden og rediger den på samme måte

Hvis du bare oppretter én språkversjon, vil den andre vise en tom side (eller standardtekst) for besøkende som bruker det andre språket.

## Tospråklig redigering – flytte og slette

**Flytte:** Flytt-funksjonen opererer på begge språkversjoner samtidig – du trenger bare utføre flyttingen én gang.

**Slette:** Sletting fjerner alltid begge språkversjoner i ett og samme steg. Det er ikke mulig å slette kun én språkversjon via grensesnittet.

## Statusfeltet – kun for use cases

Use case-sider (under «Behov») har et statusfelt som styrer symbolet som vises i menyen. Øvrige sider skal ha tomt statusfelt.

| Symbol | Norsk verdi | Engelsk verdi |
|--------|-------------|---------------|
| ◍ | Ny | New |
| ◔ | Tidlig utkast | Early draft |
| ◐ | Pågår | In progress |
| ◕ | Til QA | For QA |
| ⏺ | Godkjent | Approved |
| ⨂ | Avbrutt | Cancelled |

Statusfeltet redigeres i skjemaet som åpnes av «Rediger denne siden». Symbolet genereres automatisk – du trenger kun velge riktig tekstverdi.

## UUID-feltet – ikke rør det

Alle sider har et skjult `id`-felt (UUID). Det er usynlig i redigeringsdialogen og settes automatisk av en GitHub Actions-workflow. UUID-en er permanent – den kobler norsk og engelsk versjon av samme side og brukes for kryssreferanser.

Du vil aldri se dette feltet i editoren, og du trenger ikke tenke på det.

## Sorteringsrekkefølge (`weight`)

`weight`-feltet bestemmer rekkefølgen i sidebarmenyen. Lavere tall = høyere opp. Feltet er synlig og redigerbart i skjemaet.

**Praktisk tommelfingerregel:**

- Legg nye sider med `weight` i tioer-trinn (10, 20, 30 …) for å gi rom til seinere innskudd
- Hvis du vil flytte en side i menyen uten å bruke flytt-funksjonen, kan du justere `weight`-feltet direkte

## Bilder

Bilder kan limes direkte inn i tekstfeltet (Ctrl+V eller høyreklikk → Lim inn). De lastes automatisk opp til et dedikert bilderepo og kobles inn i siden.

For best kvalitet: bruk PNG for skjermbilder og diagrammer, JPEG for fotografier.

## Markdown i tekstfeltet

Det innebygde tekstverktøyet (TipTap) viser innholdet visuelt, men lagrer det som Markdown. Du kan bruke verktøylinjens knapper, eller skrive Markdown-syntaks direkte:

| Markdown | Resultat |
|----------|----------|
| `**tekst**` | **fet tekst** |
| `*tekst*` | *kursiv tekst* |
| `# Overskrift` | Overskrift nivå 1 |
| `## Overskrift` | Overskrift nivå 2 |
| `` `kode` `` | `kode` |
| `[lenketekst](url)` | Klikkbar lenke |

## Fallgruver

### Endring publiseres ikke

Hvis du lukker redigeringsdialogen uten å klikke «Lagre», forkastes endringene. Det finnes ingen autosave.

### Bygget feiler

Hvis statusindikatoren viser advarselikon etter lagring, er endringen registrert i Git men ikke publisert. Kontakt en administrator. Endringen er ikke tapt – den ligger i commit-historikken og kan publiseres på nytt.

### Siden ble slettet ved en feil

Sletting via grensesnittet er ikke umiddelbart reverserbart. Ta kontakt med en administrator – siden finnes i Git-historikken og kan gjenopprettes.

### Sortering ser ikke ut til å endre seg

Nettleseren kan cache sidemenyen. Hard-reload (Ctrl+Shift+R) løser det som regel.
