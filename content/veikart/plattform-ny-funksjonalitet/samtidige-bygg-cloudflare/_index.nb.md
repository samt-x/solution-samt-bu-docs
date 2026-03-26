---
id: 7a4bb610-b4ef-416a-855a-ab251a5eff45
title: "Realisering av samtidige bygg gjennom Cloudflare Pages"
linkTitle: "Samtidige bygg via Cloudflare"
weight: 92
status: "Pågår"
lastmod: 2026-03-19T00:11:03+01:00
last_editor: Erik Hagen
---

GitHub Pages avløser automatisk eldre bygg i kø når et nyere bygg med høyere prioritet venter («Canceling since a higher priority waiting request for pages exists»). Dette betyr at ved tre eller flere raske lagringer i sekvens vil kun det siste bygget fullføres – de mellomliggende avløses.

Cloudflare Pages native build med Git-integrasjon støtter opptil 6 samtidige bygg (Workers Paid-plan).

## Hva som er gjort (sesjon 13, 2026-03-19)

### Alternativ B implementert ✅

`lastmod`-injeksjon er flyttet inn i modulrepoene:

- `inject-lastmod.py` opprettet i alle 4 modulrepoer (team-architecture, samt-bu-drafts, solution-samt-bu-docs, team-pilot-1) under `.github/scripts/`
- `trigger-docs-rebuild.yml` i alle 4 modulrepoer oppdatert: `fetch-depth: 0` + nytt inject-lastmod-steg som committer med `[skip ci]`
- Bot-commits hoppes over ved bestemmelse av lastmod-timestamp (ny `get_lastmod`-logikk)
- `hugo.yml` i samt-bu-docs forenklet: fjernet multi-repo-checkout, inject-lastmod og `HUGO_MODULE_REPLACEMENTS`
- Erstattet med `hugo mod get @latest` + `hugo mod tidy` for alle moduler – henter siste versjon inkl. injisert lastmod direkte fra Go-modulproxy
- `build.sh` opprettet i samt-bu-docs-rot – klar til bruk av CF Pages native build

### Delvis løst: cancel-in-progress ✅

`concurrency: cancel-in-progress: false` → `true` i `hugo.yml`. Løser køproblemet i praksis:
- 4 raske redigeringer → 3 avlyses, 1 bygger (alle endringer er med i det ene bygget)
- Testet og bekreftet: ~1 minutt byggetid (vesentlig raskere enn før)
- Gjelder alle brukere – bygg fra ulike GitHub-brukere kombineres på samme måte

### Blokkert: CF Pages Git-integrasjon ❌

CF Pages støtter ikke å legge til Git-integrasjon på et eksisterende Direct Upload-prosjekt:
- Dashboard-siden `settings/builds-deployments` krasjer med «Refresh the page to try again» for Direct Upload-prosjekter
- CF API har ikke GitHub OAuth-kobling eksponert (`/pages/git/github/installations` → 404)
- Build-config og env vars ble satt via API (✅), men Git-kobling krever nytt prosjekt

### CF Pages-konfigurasjon satt via API ✅

Følgende er allerede konfigurert på det eksisterende `samt-bu-docs`-prosjektet:
- Build command: `bash build.sh`
- Output directory: `public`
- Env vars (production + preview): `HUGO_VERSION=0.155.3`, `HUGO_ENVIRONMENT=production`, `TZ=Europe/Oslo`, `GONOSUMDB=*`, `GOPROXY=direct`

## Gjenstående steg for fullt gjennomslag

### Steg 1 – Opprett nytt CF Pages-prosjekt med Git-integrasjon

Kan gjøres parallelt med at eksisterende site fortsetter å virke på `samt-bu-docs.pages.dev`.

1. Gå til [CF Pages → Create application → Pages → Connect to Git](https://dash.cloudflare.com/11cfadda66cca20b7736f23e40a070ef/workers-and-pages/create/pages/setup)
2. Velg **SAMT-X/samt-bu-docs**, branch **main**
3. Build command: `bash build.sh`, output: `public`
4. Env vars: `HUGO_VERSION=0.155.3`, `HUGO_ENVIRONMENT=production`, `TZ=Europe/Oslo`, `GONOSUMDB=*`, `GOPROXY=direct`
5. Aktiver **«Include Git submodules»**
6. Gi midlertidig navn, f.eks. `samt-bu-docs-git`

### Steg 2 – Opprett deploy hook og legg til som GitHub secret

- CF Pages → samt-bu-docs-git → Settings → Deploy hooks → Create hook (`github-actions`, branch `main`)
- Legg til URL som secret `CF_PAGES_DEPLOY_HOOK` i SAMT-X/samt-bu-docs

### Steg 3 – Oppdater hugo.yml

Endre `trigger-cf-pages`-jobben (repository_dispatch) til å bruke deploy hook i stedet for wrangler-deploy. Hele wrangler-deploy-steget kan fjernes fra `build`-jobben når CF native build er verifisert.

### Steg 4 – Byt prosjektnavn

- Rename `samt-bu-docs` → `samt-bu-docs-old` (eller slett)
- Rename `samt-bu-docs-git` → `samt-bu-docs`
- Subdomainen `samt-bu-docs.pages.dev` følger prosjektnavnet automatisk

## Viktig avklaring: Workers Paid ≠ Direct Upload

Workers Paid-planens «6 concurrent build slots» gjelder **kun CF-side native builds** (Git-integrasjon). Direct Upload (`wrangler pages deploy`) bruker ikke disse slotene – builds skjer i GitHub Actions. Kjøp av Workers Paid har dermed ingen effekt på Direct Upload-flyten.

## Relatert

- `samt-bu-docs/.github/workflows/hugo.yml` – nåværende bygg- og deploy-flyt
- `samt-bu-docs/build.sh` – klar for CF native build
- Veikart: [Statusrapportering og bygg-køer](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/veikart/statusrapportering-gui/)
- Veikart: [Falsk byggefeil ved timeout](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/veikart/bygg-feil-timeout/)
