---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: 88a7cc4a-b428-488f-b159-1696bbc68594
title: "Pull request-støtte i Endre-menyen"
linkTitle: "Pull request-flyt"
weight: 95
status: "Godkjent"
# Gyldige verdier: Ny | Tidlig utkast | Pågår | Til QA | Godkjent | Avbrutt
lastmod: 2026-05-02T17:51:52+02:00
last_editor: Erik Hagen

---

Brukere uten direkte skrivetilgang til repoet kan bidra via det innebygde grensesnittet ved å sende forslag som pull requests – uten å eie en fork eller ha skrivetilgang.

## Arkitektur – Worker-basert PR-flyt

I stedet for den fork-baserte tilnærmingen bruker løsningen en **Cloudflare Worker** (`auth.samt-bu.no/suggest`) som oppretter branch, commit og PR på vegne av bidragsyteren. Selve GitHub-operasjonene utføres av en dedikert bot-konto (`samt-x-bot`) med skrivetilgang til alle innholdsrepoer.

### Nøkkelkomponenter

| Komponent | Rolle |
|-----------|-------|
| `samt-x-bot` | GitHub-konto med `push`-tilgang til alle 9 SAMT-X-innholdsrepoer via team `content-bots` |
| `WORKER_PAT` | Klassisk GitHub PAT (`repo`-scope) fra `samt-x-bot`, lagret som Cloudflare Worker secret |
| `POST /suggest` | Worker-endepunkt som mottar filinnhold + brukertoken, og oppretter branch+commit+PR |
| `suggestViaWorker()` | Frontend-funksjon som kaller Worker-endepunktet |

### Flyt – steg for steg

1. Bruker åpner Endre-menyen → `checkCollaboratorPermission()` sjekker skrivetilgang (bruker-spesifikk cache, 1 t TTL)
2. Menyvalg omdøpes til «Foreslå…» hvis `canWrite=false`
3. Bruker gjør endring og klikker Lagre/Send
4. Frontend kaller `suggestViaWorker(repo, branch, treeItems, …)` med brukerens GitHub App-token
5. Worker verifiserer token-format (`ghu_`/`ghp_`-prefiks) og bruker `WORKER_PAT` til alle GitHub API-kall
6. Worker oppretter branch → commit → PR i det aktuelle SAMT-X-repoet
7. Statusfeltet i dialogen viser «✓ Pull request: #N» med klikkbar lenke

### Meny-tilpasning

| Original tekst | Foreslå-tekst |
|----------------|---------------|
| Rediger dette kapitlet | Foreslå endring av dette kapitlet |
| Nytt kapittel etter dette | Foreslå nytt kapittel etter dette |
| Nytt underkapittel | Foreslå nytt underkapittel |
| Slett denne siden | Foreslå sletting av denne siden |

### PR-titler

| Dialog | PR-tittel (nb) |
|--------|----------------|
| Rediger | «Foreslår endring: \<sidetittel\>» |
| Ny side | «Foreslår ny side: \<tittel\>» |
| Slett | «Foreslår sletting: \<sidetittel\>» |

PR-beskrivelsen inkluderer brukerens GitHub-brukernavn og kilden.

## Admin-arbeidsflyt ved mottatt PR

1. GitHub sender varsel om ny PR
2. Admin ser over endringen i PR-visningen
3. Klikk **Merge pull request** – branchen slettes automatisk (`delete_branch_on_merge: true`)
4. Skriv en kommentar i PR-tråden som bekrefter at forslaget er tatt inn og at nettstedet oppdateres

## Tekniske detaljer og kjente begrensninger

- **Flytt-dialog** støtter ikke forslagsflyt – krever skrivetilgang (admin-operasjon)
- **Duplikat-PR** – hvis bruker sender to forslag uten at første er merget, feiler andre forsøk med GitHub-feil. Håndteres ikke i dag
- **`samt-x-bot`-konto** bør på sikt migreres til en organisasjonskonto utenfor personlig eierskap (se ROS-dokumentasjon)

## Nøkkelfiler

- `cloudflare-worker/oauth-worker.js` – `handleSuggest()`, Worker-endepunkt
- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html` – `checkCollaboratorPermission()`, `makePrBranch()`, `suggestViaWorker()`
- `themes/hugo-theme-samt-bu/layouts/partials/edit-switcher.html` – meny-tilpasnings-JS
