---
title: "Realisering av samtidige bygg gjennom Cloudflare Pages"
linkTitle: "Samtidige bygg via Cloudflare"
weight: 92
status: "Ny"
---

GitHub Pages avløser automatisk eldre bygg i kø når et nyere bygg med høyere prioritet venter («Canceling since a higher priority waiting request for pages exists»). Dette betyr at ved tre eller flere raske lagringer i sekvens vil kun det siste bygget fullføres – de mellomliggende avløses.

Cloudflare Pages har en annen kømodell og kan potensielt bygge og deploye flere versjoner i sekvens uten å avløse hverandre.

## Spørsmål å avklare

- Støtter Cloudflare Pages (free tier / Pro) parallelle eller sekvensielle bygg uten avløsning?
- Er det mulig å konfigurere bygg-køen slik at alle commits deployes, ikke bare den siste?
- Hva er maks byggetid og køgrenser på de ulike CF Pages-planene?

## Mulig gevinst

Dersom CF Pages lar alle bygg fullføres i rekkefølge, kan «avløst»-scenariet elimineres helt – i stedet for at brukere opplever at endringer tilsynelatende «forsvinner» fra byggehistorikken og må vente på et nytt bygg.

## Nåværende status

Nettstedet deployes allerede til Cloudflare Pages (`samt-bu-docs.pages.dev`) via `wrangler pages deploy` i `hugo.yml`. Bygget kjøres i GitHub Actions – CF Pages brukes kun som deploy-target, ikke som byggemiljø.

Et alternativ er å la CF Pages også **bygge** (ikke bare motta deploy) – da styrer CF Pages sin egen byggekø og GitHub Actions-køen er irrelevant.

## Relatert

- `.github/workflows/hugo.yml` – nåværende bygg- og deploy-flyt
- Veikart: [Statusrapportering og bygg-køer](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/veikart/statusrapportering-gui/) – avløst-håndtering (steg 3c)
- Veikart: [Falsk byggefeil ved timeout](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/veikart/bygg-feil-timeout/)
