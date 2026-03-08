---
title: "CMS i dybden"
linkTitle: "CMS i dybden"
weight: 10
---

Decap CMS er det nettleserbaserte redigeringsverktøyet for SAMT-BU Docs. Denne siden dekker funksjonalitet og fallgruver som ikke er åpenbare ved første øyekast.

## De seks CMS-portalene

Innholdet er fordelt på seks portaler – én per repo og språk. Det finnes ingen «superportal» som dekker alt; du må bruke riktig portal for riktig innhold.

| Portal | Språk | Dekker | Åpnes via |
|--------|-------|--------|-----------|
| Docs (nb) | Norsk | Hoveddelen av samt-bu-docs-repoet | «Endre» → «Andre valg» |
| Docs (en) | Engelsk | Hoveddelen av samt-bu-docs-repoet | «Edit» → «Other options» |
| Arkitektur (nb) | Norsk | team-architecture-repoet | «Endre» → «Andre valg» |
| Arkitektur (en) | Engelsk | team-architecture-repoet | «Edit» → «Other options» |
| Utkast (nb) | Norsk | samt-bu-drafts-repoet | «Endre» → «Andre valg» |
| Utkast (en) | Engelsk | samt-bu-drafts-repoet | «Edit» → «Other options» |

**Snarveien «Denne siden»** i Endre-menyen tar deg direkte til gjeldende side i riktig portal, uansett hvilken portal og seksjon det gjelder. Dette er den raskeste måten å redigere en eksisterende side.

## Tospråklig redigering

Nettstedet er tospråklig (norsk og engelsk). CMS-portalene er adskilt per språk – det finnes ingen automatisk oversettelse.

**Hva dette betyr i praksis:**

- Opprett siden i norsk portal (f.eks. Docs nb) og lagre
- Bytt til engelsk portal (Docs en) og opprett samme side med engelsk innhold
- UUID-feltet (`id`) kobler de to språkversjonene – det settes automatisk og skal ikke endres

Hvis du kun oppretter én språkversjon, vil siden mangle innhold på det andre språket (brukere som bytter språk vil se en tom side eller feilmelding).

## Statusfeltet og statussymboler

Kun use case-sider (under «Behov») bruker statusfeltet. Gyldige verdier:

| Symbol | Norsk verdi | Engelsk verdi |
|--------|-------------|---------------|
| ◍ | Ny | New |
| ◔ | Tidlig utkast | Early draft |
| ◐ | Pågår | In progress |
| ◕ | Til QA | For QA |
| ⏺ | Godkjent | Approved |
| ⨂ | Avbrutt | Cancelled |

Symbolet genereres automatisk fra verdien – du trenger kun velge riktig tekst i CMS-en. Øvrige sider skal ha tomt statusfelt.

## Lagring og publisering – tidslinjen

```
Du klikker «Lagre» i CMS
    ↓  (noen sekunder)
Decap CMS oppretter en commit på GitHub
    ↓  (1–3 minutter)
GitHub Actions bygger nettstedet
    ↓
Ny versjon er live på samt-x.github.io/samt-bu-docs/
```

Du kan følge med på byggingen under **Actions**-fanen i GitHub-repoet. Hvis bygget feiler (rød X), er ikke endringen publisert – ta kontakt med en administrator.

## UUID-feltet – ikke rør det

Alle sider har et skjult `id`-felt (UUID). Det er usynlig i CMS-editoren (`widget: hidden`) og settes automatisk av en GitHub Actions-workflow. UUID-en er permanent – den kobler norsk og engelsk versjon av samme side og brukes eventuelt for kryssreferanser.

Du vil aldri se dette feltet i CMS-en, og du trenger ikke tenke på det.

## Fallgruver og kjente begrensninger

### Testinnhold etter CMS-sesjon

Decap CMS lagrer direkte til `main`-branchen. Hvis du har testet funksjoner eller skrevet uferdige utkast uten å slette dem, kan disse havne i nettstedet. **Sjekk alltid `git diff` (eller GitHub commit-historikken) etter en CMS-sesjon** hvis du er usikker på hva som ble lagret.

### Sorteringsrekkefølge (`weight`)

Sidene i CMS-listen kan sorteres på `weight`-feltet (som samsvarer med rekkefølgen i sidebarmenyen). Lavere tall = høyere opp. Hvis du ikke setter `weight`, havner siden bakerst.

### Ny side vs. ny mappe

I Hugo er hver side en **mappe** med en `_index.nb.md`-fil inni. CMS-en håndterer dette automatisk – du trenger ikke opprette mapper selv. Men husk at en side uten underkapitler og uten synlig innhold vil vises som tom i nettstedet.

### Lokalt testmiljø

CMS-en støtter lokal testing: kjør `hugo server` og åpne portalen i nettleseren, klikk «Work with Local Repository». Endringer lagres da direkte til filsystemet ditt (ikke GitHub) og du kan se dem live i forhåndsvisningen uten å committe.
