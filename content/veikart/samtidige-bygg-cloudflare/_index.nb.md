---
id: 9d68d1e1-27b6-4adb-a587-642523da4c3f
title: "Realisering av samtidige bygg gjennom Cloudflare Pages"
linkTitle: "Samtidige bygg via Cloudflare"
weight: 92
status: "Ny"
lastmod: 2026-03-18T22:07:46+01:00
last_editor: Erik Hagen

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

## Blokkerende problem: lastmod-injeksjon for modulinnhold

CF Pages native build støtter kun én enkelt repo. `hugo.yml` gjør i dag tre ting CF Pages ikke kan gjøre på egenhånd:

| Steg | Hva | Konsekvens hvis mangler |
|------|-----|------------------------|
| Multi-repo checkout | Henter team-architecture, samt-bu-drafts, solution-samt-bu-docs, team-pilot-1 med full git-historikk | Modulinnhold bygges fra Go-modul-cache (zip, ingen git-historikk) |
| `inject-lastmod.py` | Leser `git log` per `.md`-fil og skriver `lastmod:` inn i frontmatter | «Sist endret»-datoer vises ikke på modul-sider |
| `HUGO_MODULE_REPLACEMENTS` | Peker Hugo til lokale kloner med injisert lastmod | Hugo bruker uendret modul-cache |

**Kort sagt: CF Pages native build fungerer, men modul-sider mister «Sist endret»-datoer.**

## Hva som må løses for å bytte uten funksjonstap

To mulige tilnærminger:

### A – Pre-bygg i GitHub Actions, push til CF Pages via Direct Upload (dagens flyt, men robust)
Behold GitHub Actions-bygget. Løs wrangler-timeouts med retry-logikk (allerede gjort – se `hugo.yml`). CF Pages brukes kun som hosting.

### B – Flytt lastmod-logikken inn i modulrepoene
Endre `trigger-docs-rebuild.yml` i hvert modulrepo til å injisere `lastmod:` direkte i filene og committe det. Da finnes lastmod-feltene i selve repo-filene – CF Pages trenger ikke git-historikk. Krever:
1. Oppdatere `trigger-docs-rebuild.yml` i team-architecture, samt-bu-drafts, solution-samt-bu-docs, team-pilot-1 til å kjøre `inject-lastmod.py` og committe endringer
2. Fjerne inject-lastmod-steget fra `hugo.yml`
3. Fjerne multi-repo-checkout og `HUGO_MODULE_REPLACEMENTS` fra `hugo.yml`
4. Konfigurere CF Pages til å bygge med `hugo --gc --minify` og riktig Hugo-versjon

**Alternativ B er den anbefalte veien** – gir CF Pages native build uten funksjonstap, og lastmod-datoene blir versjonskontrollerte i modulrepoene (en bonus).

## Relatert

- `.github/workflows/hugo.yml` – nåværende bygg- og deploy-flyt
- Veikart: [Statusrapportering og bygg-køer](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/veikart/statusrapportering-gui/) – avløst-håndtering (steg 3c)
- Veikart: [Falsk byggefeil ved timeout](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/veikart/bygg-feil-timeout/)
