---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: a1dec965-c693-4bbd-a231-1162fb4306ef
title: "Utviklernotater og Claude-kontekst"
linkTitle: "Utviklernotater"
weight: 50
lastmod: 2026-04-27T09:40:51+02:00
last_editor: Erik Hagen

---

Denne siden er skrevet for både menneskelige utviklere og for AI-assistenten Claude Code, som brukes aktivt i utvikling og vedlikehold av SAMT-BU Docs. Den samler kontekst, konvensjoner og arkitekturbeslutninger som ellers lett går tapt mellom arbeidsøkter.

> **For Claude:** Denne filen leses eksplisitt ved behov. `MEMORY.md` (auto-lastet) er en kompakt indeks – denne filen er kilden til dypere kontekst.
>
> **OBS – historisk kontekst:** Denne dokumentasjonen ble påbegynt ~2026-03-02. Mye tidligere lærdom og beslutningshistorikk finnes kun i commit-loggene. Ved ukjente problemer: kjør `git log --oneline` i `hugo-theme-samt-bu` og `samt-bu-docs`, deretter `git show <hash>` for detaljer.

---

## Minnehåndtering (Claude Code)

Claude Code bruker to nivåer for persistent kontekst:

| Nivå | Fil | Rolle | Grense |
|------|-----|-------|--------|
| 1 | `MEMORY.md` (se stier under) | Auto-lastet ved sesjonstart – kompakt indeks og kritiske «aldri glem»-punkter | 200 linjer |
| 2 | `claude-kontekst/_index.nb.md` (denne filen) | Canonical kilde – leses eksplisitt ved behov, ingen linjegrense, versjonskontrollert i git | Ingen |

**Konvensjon:** Detaljer hører hjemme her (i repo). `MEMORY.md` peker hit. Ingenting viktig trimmes bort – det flyttes hit i stedet.

### Memory-mapper og topic-filer

Claude Code oppretter én memory-mappe per prosjektnøkkel (avledet av arbeidskatalog). Prosjektet har to aktive mapper fordi arbeidskatalogen ble endret ved repo-migrering:

| Arbeidskatalog | Memory-mappe |
|----------------|--------------|
| `S:\app-data\github\samt-bu-repos\samt-bu-docs\` *(gammel)* | `C:\Users\Win11_local\.claude\projects\S--app-data-github-samt-bu-repos-samt-bu-docs\memory\` |
| `S:\app-data\github\samt-x-repos\samt-bu-docs\` *(aktiv)* | `C:\Users\Win11_local\.claude\projects\S--app-data-github-samt-x-repos-samt-bu-docs\memory\` |

**Bruk alltid den aktive mappen** (`samt-x-repos`). Den gamle beholdes som historisk referanse.

Filer i aktiv memory-mappe:

| Fil | Innhold |
|-----|---------|
| `MEMORY.md` | Auto-lastet indeks – pekere, git-status, kritiske punkter |
| `cms-routing.md` | Detaljert rutinglogikk for edit-switcher (fire grener, slug-beregning, sjekkliste for ny modul) |

### Sesjonsavslutning – alltid gjør dette

Når brukeren ber om oppdatering av memory/kontekst, eller signaliserer at sesjonen nærmer seg slutten:

1. Kjør `git status` i alle berørte repoer
2. Commit ucommittede endringer – spør aldri om dette skal gjøres, bare gjør det
3. Push
4. Oppdater `MEMORY.md` og/eller denne filen med ny innsikt fra sesjonen
5. Bekreft at alt er rent

**Aldri avslutt sesjon med uncommittede endringer uten å ha spurt eksplisitt.**

---

## Arkitektur og nøkkelfiler

### Repostruktur

| Repo | Formål | Lokal sti |
|------|--------|-----------|
| `samt-bu-docs` | Hoved-repo – konfigurasjon, innhold, CI/CD | `S:/app-data/github/samt-x-repos/samt-bu-docs/` |
| `hugo-theme-samt-bu` | Tema – all presentasjonslogikk (submodule) | `themes/hugo-theme-samt-bu/` |
| `team-architecture` | Hugo-modul, innhold for arkitektur-teamet | `S:/app-data/github/samt-x-repos/team-architecture/` |
| `team-semantics` | Hugo-modul, innhold for semantikk-teamet | `S:/app-data/github/samt-x-repos/team-semantics/` |
| `samt-bu-drafts` | Hugo-modul, utkast og innspill | `S:/app-data/github/samt-x-repos/samt-bu-drafts/` |
| `solution-samt-bu-docs` | Hugo-modul, teknisk dok. for SAMT-BU Docs | `S:/app-data/github/samt-x-repos/solution-samt-bu-docs/` |

### Viktigste filer å kjenne

| Fil | Hva |
|-----|-----|
| `themes/hugo-theme-samt-bu/layouts/partials/custom-head.html` | All tilpasset CSS – redigeres oftest |
| `themes/hugo-theme-samt-bu/layouts/partials/header.html` | HTML-skjelett, jQuery-lasting, restore-tabs |
| `themes/hugo-theme-samt-bu/layouts/partials/topbar.html` | Header-innhold, inline flex-CSS |
| `themes/hugo-theme-samt-bu/layouts/partials/search.html` | Søkefelt + script-lasting (lunr, horsey, search.js) |
| `themes/hugo-theme-samt-bu/layouts/partials/edit-switcher.html` | Endre/Edit-dropdown (WYSIWYG, Ny side, Slett) – ingen Decap-avhengighet |
| `themes/hugo-theme-samt-bu/layouts/partials/footer.html` | Scroll-spy, scroll-fade, sidebar-JS |
| `themes/hugo-theme-samt-bu/static/js/altinndocs-learn.js` | Sidebar-akkordeon, clipboard, keyboard-nav |
| `themes/hugo-theme-samt-bu/layouts/index.json` | JSON-output-template for søkeindeks |
| `hugo.toml` | Konfigurasjon – baseURL, moduler, navSwitcher, språk |
| `.github/workflows/hugo.yml` | CI/CD – bygg, deploy, inject-lastmod |
| `.github/scripts/inject-lastmod.py` | Injiserer lastmod i modulinnhold (kun CI) |

### CSS-lagmodell (tre lag, siste vinner)

```
designsystem.css  →  theme.css  →  custom-head.html
```

Tilpasninger gjøres alltid i `custom-head.html`.

### 3-kolonne layout

- `html, body { height: 100%; overflow: hidden }` – ingen sidescroll
- **Venstre (#sidebar):** 20% / maks 260px – nav
- **Midten (#body):** flex 1 – innhold
- **Høyre (#page-toc):** 18% / maks 240px – TOC
- Scrollbarer skjult (`scrollbar-width: none !important` + `#sidebar *::-webkit-scrollbar { display: none !important }`)
- Collapsible: toggle-knapper i heading-rad, restore-tabs i `<body>`, tilstand i localStorage

### Scroll-fade (venstre og høyre panel)

Begge paneler bruker samme teknikk: et ekte DOM-element med `position: sticky; bottom: 0` plassert *inne i* innholdsstrømmen (ikke `::after` på containeren).

- **TOC:** `<div class="toc-scroll-fade">` som siste element i `#page-toc`
- **Sidebar:** `<div class="sidebar-scroll-fade hidden">` som siste element i `.highlightable` (i `menu.html`)
- JS (footer.html) toggles `.hidden`-klassen basert på scroll-posisjon og overflow

**OBS:** `::after` på en scroll-container fungerer IKKE riktig med `position: sticky` – gir solid blokk, ikke gradient-overlay.

### Sidebar-akkordeon (altinndocs-learn.js)

Klikk på pil-ikonet (`<i class="category-icon">`) styres av `jQuery('#sidebar .category-icon').on('click', ...)` i `altinndocs-learn.js`.

- **Klikk på pilen:** `e.stopPropagation()` forhindrer bobling til `<a>` → ingen navigasjon. Ikonklasse toggles, `<ul>` toggles.
- **Klikk på teksten (`<span>`):** ingen handler → bobler til `<a>` → navigerer til seksjonsindeks-siden normalt.

```javascript
jQuery('#sidebar .category-icon').on('click', function(e) {
    e.stopPropagation();
    $(this).toggleClass('fa-sort-down fa-caret-right');
    $(this).closest('li').children('ul').toggle();
});
```

**Kritisk:** Bruk `e.stopPropagation()` på ikonet – ikke `return false` på `<a>`. Å sette `return false` på `<a>` for alle elementer med barn blokkerer navigasjon til seksjonsindeks-sider. Se kjente-problemer for full historikk.

### theme.css-feller å kjenne

Noen regler i `theme.css` er designet for det opprinnelige ikke-scrollende layoutet og må overstyres:

| Regel | Problem | Override i custom-head.html |
|-------|---------|------------------------------|
| `#top-github-link { top: 50%; transform: translateY(-50%) }` | Dytter GitHub-lenken halvveis ned i #body | `position: static !important; top: auto !important; transform: none !important` |
| `.adocs-content { padding-bottom: 36px; margin-bottom: 12px }` | Unødvendig stor avstand under innhold | `padding-bottom: 12px !important; margin-bottom: 4px !important` |
| `.highlightable { overflow: auto; height: 100% }` | .highlightable vil scroll separat | `overflow: visible !important; height: auto !important` |

---

## Hugo Modules

Innhold fra externe repoer monteres via `[module.imports]` i `hugo.toml`.

| Modul | Montert under |
|-------|---------------|
| `github.com/SAMT-X/team-architecture` | `content/teams/team-architecture/` |
| `github.com/SAMT-X/team-semantics` | `content/teams/team-semantics/` |
| `github.com/SAMT-X/samt-bu-drafts` | `content/utkast/` |
| `github.com/SAMT-X/solution-samt-bu-docs` | `content/loesninger/cms-loesninger/samt-bu-docs/` |

**Oppdatere en modul:**
```bash
hugo mod get github.com/SAMT-X/<navn>@latest
```

**Legge til ny modul:** Se CLAUDE.md – "Legge til ny modul".

**Tidsstempler (lastmod):** Modulinnhold leveres som zip → ingen git-historikk → `Sist endret` vises ikke lokalt. CI løser dette via `inject-lastmod.py` + `HUGO_MODULE_REPLACEMENTS`. Kun `team-architecture` og `samt-bu-drafts` er med i CI-replacement per nå.

**Kryssrepo-triggering (aktivert 2026-03-05):** Push til `samt-bu-drafts` eller `team-architecture` trigger automatisk nybygg av `samt-bu-docs` via `repository_dispatch`. Mekanismen er dokumentert i detalj i `teknisk-dokumentasjon/ci-cd-pipeline/`. Krever secret `DOCS_REBUILD_TOKEN` (PAT med `workflow`-scope) i hvert modulrepo. For å legge til et nytt modulrepo: se oppskriften i CI/CD-dokumentasjonen.

**Etter manuell push til team-architecture (lokalt):** Kjør alltid `GONOSUMDB=* GOPROXY=direct hugo mod get github.com/SAMT-X/team-architecture@latest` i samt-bu-docs, bygg, og commit + push `go.mod`/`go.sum`. (Ikke nødvendig for CMS-redigering – da skjer alt automatisk.)

**UUID-workflow rebase-konflikt (kjent mønster):** Ny fil pushes → UUID-workflow committer `id:`-felt raskt → neste push til samme fil avvises. `git pull --rebase` kan gi merge-konflikt mellom `---`-avslutning og påfølgende innhold. Løsning: skriv filen ferdig (behold `id:` fra HEAD + legg inn eget innhold), `git add`, `GIT_EDITOR=true git rebase --continue`.

**Org-migrering (2026-03-03):** Alle repos flyttet fra `SAMT-BU` → `SAMT-X`. Ved `hugo mod get @latest` etter org-bytte: fjern `require`-blokken i go.mod manuelt og kjør `GONOSUMDB=* GOPROXY=direct hugo mod tidy` – ikke `hugo mod get`, da dette feiler mot gammel pinnet versjon med feil modul-sti.

---

## GitHub OAuth-flyt (innebygd, uten Decap)

Decap CMS og alle tilknyttede portaler er fjernet (2026-03-11). Innlogging skjer nå direkte via nettstedets egen OAuth-popup.

### Token-håndtering (`custom-footer.html`, global `<script>`)

| Funksjon | Rolle |
|----------|-------|
| `getStoredToken()` | Leser token fra `samt-bu-gh-token` (localStorage). Fallback til Decap-nøkler for migrering. |
| `storeToken(token)` | Lagrer token i `samt-bu-gh-token`. |
| `doGitHubLogin(onSuccess)` | Åpner OAuth-popup mot Cloudflare Worker, implementerer Netlify/Decap `postMessage`-protokollen på åpner-siden, kaller `onSuccess(token)` etter vellykket innlogging. |

**Protokollen (Cloudflare Worker callback):**
1. Popup sender `"authorizing:github"` til opener (wildcard)
2. Opener svarer `"authorizing:github"` til `e.source` – popup lærer openers origin
3. Popup sender `"authorization:github:success:{token, provider}"` tilbake
4. Opener parser JSON, kaller `storeToken()`, lukker popup, kaller `onSuccess`

**Popup-blokkering:** Dersom popup er blokkert av nettleseren, vises en `alert()` om å tillate popup-vinduer.

**Logg ut:** Slett `samt-bu-gh-token` fra localStorage manuelt (DevTools → Application → Local Storage).

### Edit-switcher – nåværende menyvalg

| Valg | Implementasjon |
|------|----------------|
| «Rediger dette kapitlet» | WYSIWYG TipTap-editor (qe-dialog), henter og lagrer fil via GitHub API |
| «Nytt kapittel etter dette» | «Ny side»-dialog (np-dialog, mode=sibling) |
| «Nytt underkapittel» | «Ny side»-dialog (np-dialog, mode=child), ikon `fa-folder-o` |
| «Slett denne siden» | Bekreftelsesdialog → atomisk slett nb+en → polling → auto-navigering |

**Synlighet:** Alle fire vises kun når `.File` finnes og `$entrySlug != ""`. «Slett» og «Nytt underkapittel» skjules i tillegg på rot-nivå (`$dirPath == "content"`).

### Repo-ruting i edit-switcher (tre grener + default)

Basert på `path.Dir .File.Path` (normalisert):

- `hasPrefix "teams/"` → `githubRepo = "team-architecture"`
- `eq/hasPrefix "utkast"` → `githubRepo = "samt-bu-drafts"`
- `eq/hasPrefix "loesninger/cms-loesninger/samt-bu-docs"` → `githubRepo = "solution-samt-bu-docs"`
- Alt annet → `githubRepo = "samt-bu-docs"` (default)

**Når en ny modul legges til:** Legg til nytt grein i `edit-switcher.html` *før* `{{ else }}`-blokken.

### UUID (id-felt i frontmatter)

- UUID v4, samme verdi i nb og en for samme side – **aldri endres manuelt**
- Håndteres av `.github/workflows/ensure-uuids.yml` (finnes i alle fire repoer)
- `$entrySlug` brukes ikke lenger til Decap-routing – kun som betingelse for å vise edit-knapper

---

## Søkesystem

- **Stack:** Lunr.js + Horsey.js autocomplete, indeks generert som Hugo JSON-output
- **Konfigurasjon:** `[outputs] home = ["HTML", "RSS", "JSON"]` i `hugo.toml`
- **Template:** `themes/hugo-theme-samt-bu/layouts/index.json`
- **JS:** `themes/hugo-theme-samt-bu/static/js/search.js`
- **`baseurl`-variabel:** Settes som inline script i `search.html` fra `{{.Site.BaseURL}}`

**Lazy-loading (implementert og deployet 2026-03-03):**

`initLunr()` kalles ikke ved sidelasting. Søkeindeksen hentes (via `$.getJSON()`) kun første gang brukeren fokuserer søkefeltet (`$.one("focus", initLunr)`). Flaggene `searchIndexLoading`/`searchIndexLoaded` forhindrer dobbelthenting. Alle search-scripts har `defer` → rekkefølgegaranti mot jQuery (som også har `defer`) er ivaretatt.

---

## Lokale hjelpeverktøy

### Synkroniseringsskript – oppdater alle repoer på én gang

Tre skript under `S:\app-data\github\samt-x-repos\`:

| Skript | Funksjon |
|--------|----------|
| `pull-all.bat` / `.sh` | `git pull` for alle repoer (henter fra remote) |
| `push-all.bat` / `.sh` | `git push` for alle repoer med upushede commits |
| `sync-all.bat` / `.sh` | Bidireksjonell synk: fetch → rebase → push per repo |

**`sync-all` anbefalt arbeidsflyt:**
```
Før du begynner:  sync-all
Underveis:        commit + push-all
Når du er ferdig: sync-all
```

`sync-all` bruker `git pull --rebase` (ikke merge) for å unngå unødvendige merge-commits. Stopper og rapporterer ved ekte konflikter – løser aldri konflikter automatisk på vegne av deg. Spesialtilfelle `go.mod`/`go.sum`: `git checkout --theirs go.mod go.sum && hugo mod tidy`.

---

## GitHub CLI (gh)

- **Plassering:** `C:\Program Files\GitHub CLI\gh.exe` – ikke i PATH i bash fra Claude Code
- **Bruk alltid full sti:** `"/c/Program Files/GitHub CLI/gh.exe"`
- **Slette repos:** krever ekstra scope – kjør `gh auth refresh -h github.com -s delete_repo` og fullfør nettleserflyt

---

## samt-bu-drafts – innholdsstruktur

Én mappe per aktør/bidragsyter, med tynt foreldresidehode og én undermappe per innspill:

```
content/
  kommuneforlaget/          (weight 10, alwaysopen: true)
    _index.nb.md            ← kort beskrivelse av aktøren
    brukstilfelle-analyse/
      _index.nb.md          ← selve innspillet
  samt-bu-pilot-1/          (weight 20)
    _index.nb.md
    erfaringer-fra-pilot/
      _index.nb.md
  novari-hk-dir/            (weight 30)
    _index.nb.md
    felles-prosjekt-vilbli-utdanning/
      _index.nb.md
```

**Legge til nytt innspill fra eksisterende aktør:** Opprett ny undermappe under aktørmappen.
**Legge til ny aktør:** Opprett ny aktørmappe med `_index.nb.md` + `_index.en.md` (tynt hode, `alwaysopen: true`, neste ledige weight) + undermappe for første innspill.

---

## samt-bu-files – filstruktur

Brukes til å lagre binærfiler (Word, PDF, bilder) som lenkes til fra `samt-bu-drafts` eller andre moduler.

### Mappestruktur

```
library/        ← Ferdige/offisielle dokumenter, organisert per aktør/tema
  Novari/       ← Vedlegg og rapporter fra Novari
drafts/         ← Innspill under arbeid, flatt med dato-prefix
  yyyy-mm-dd Tittel.docx
```

**Konvensjon for `drafts/`:** Filnavn format `yyyy-mm-dd Tittel.docx` – sikrer kronologisk sortering og sporbarhet. Mellomrom i filnavn enkodes som `%20` i URL-er.

**Planlagt neste steg:** Vurdere én mappe per innspill i `drafts/` (for å romme vedlegg og oppfølgingsdokumenter). Se `veikart/innspill-mappestruktur/`.

---

## Kildehenvisningsmønster (Word-dokumenter)

Bekreftet fungerende mønster for å lenke til Word-filer i `samt-bu-files`:

```markdown
> **Kilde:** <Avsender>, <dato>.
> [Åpne i Word Online](<officeapps-url>) – [last ned Word-fil](<github-raw-url>)
```

- **Office viewer URL:** `https://view.officeapps.live.com/op/view.aspx?src=https%3A%2F%2Fraw.githubusercontent.com%2F<ORG>%2F<repo>%2Fmain%2F<sti>%2F<fil%20navn>.docx&ui=nb-NO&rs=nb-NO`
- **Nedlastings-URL:** `https://github.com/<ORG>/<repo>/raw/main/<sti>/<fil%20navn>.docx`
- Mellomrom i filnavn → `%20` i begge URLer
- Eksempel i bruk: `content/teams/team-architecture/Arkitekturstyring/_index.nb.md` og `samt-bu-drafts/kommuneforlaget/brukstilfelle-analyse/_index.nb.md`

---

## Oversettelse NB→EN – siste fullstendige gjennomgang

**Dato:** 2026-03-21 (sesjon 20)

Alle repoer har 100 % EN-dekning fra og med denne datoen. Ved fremtidige sesjoner er det tilstrekkelig å sjekke kun filer endret *etter* 2026-03-21:

```bash
git log --since="2026-03-21" --name-only --pretty=format: -- "*.nb.md" | sort -u | grep -v '^$'
```

Kjøres i hvert repo (`samt-bu-docs`, `solution-samt-bu-docs`, `team-architecture`, `team-semantics`, `samt-bu-drafts`). Tilsvarende EN-fil for hvert treff sjekkes og oppdateres.

**Hva ble gjort i gjennomgangen:**
- 12 nye EN-filer: `solution-samt-bu-docs/veikart/` (alle manglende)
- 3 nye EN-filer: `team-architecture/` (KS-Pål, Pilot-arkitektur, Pilot-arkitektur/Pilot 1)
- 6 utdaterte EN-filer oppdatert: `om-dette-nettstedet`, `hvordan-bidra`, `teknisk-dokumentasjon/_index`, `kjente-problemer`, `github-auth-uavhengig-av-cms`, `arkitektur/_index`
- Feil i NB fikset: «vis»→«via», «GitHub Pages»→«Cloudflare Pages» i `om-dette-nettstedet`

---

## Konvensjoner

- **Commit-meldinger:** Skrives på norsk (se git-historikken for stil)
- **Frontmatter:** YAML (`---`), ikke TOML
- **Mappestruktur:** Hver side i egen mappe med `_index.nb.md` og `_index.en.md`
- **Presentasjonsendringer:** Commit i `hugo-theme-samt-bu`, deretter oppdater submodule-peker i `samt-bu-docs`
- **Temasubmodule:** `themes/hugo-theme-samt-bu/` – etter branch-rename: `git remote set-head origin main`

---

## Innholdsstruktur (10 seksjoner)

| Seksjon | Weight | Kilde |
|---------|--------|-------|
| `om/` | 1 | lokal |
| `behov/` | 10 | lokal |
| `pilotering/` | 20 | lokal |
| `arkitektur/` | 30 | lokal |
| `loesninger/` | 40 | lokal |
| `rammeverk/` | 50 | lokal |
| `arkitektur/informasjonsarkitektur/` | 30 (sub) | lokal |
| `innsikt/` | 70 | lokal placeholder |
| `teams/` | 80 | lokal + moduler |
| `utkast/` | 90 | modul samt-bu-drafts |

**Repo-navnekonvensjon:** `samt-bu-`-prefiks = publisert innhold/produkt. `team-`-prefiks = internt arbeidsrepo.

### Use cases (behov/use-cases/) – status 2026-03-10

22 nummererte use cases (01–22). Nylig lagt til/endret:
- **20** – Tilgjengeliggjøring av resultater fra grunnskolen (stub, weight 20)
- **21** – Valg av utdanningsløp (full innhold inkl. «Innspill til løsningsvalg», weight 21)
- **22** – Analysedata fra barnehage til voksenopplæring (full innhold + KS Digital/Azure Databricks-merknad, weight 22; mappe het tidligere `20-analyse-vestland-fk`)

Seksjonstittel endret: «Case» → «Case-beskrivelser» / «Case descriptions».

Seksjon «Innspill til løsningsvalg» lagt til i case 21 og 22. Øvrige 20 caser mangler denne seksjonen – se `veikart/oppdater-use-case-mal/`.

---

## Endringslogg – 2026-03-10 (kveld)

### ensure-uuids løkke-fiks
`ensure-uuids.yml` fikk `if: github.actor != 'github-actions[bot]'` på jobbnivå. Tidligere kjørte workflowen på seg selv: bruker pusher → auto-UUID-commit → trigger ny ensure-uuids → ny UUID-commit forsøker push → avvist pga. race. Nå stopper løkken ved kilden.

### «Ny side – samme nivå»-dialog: fullstendig implementert

Alle endringer i `hugo-theme-samt-bu/layouts/partials/` (`edit-switcher.html` + `custom-footer.html`).

**Dialogfunksjonalitet:**
- Åpnes fra «Side – samme nivå» i Endre-menyen
- Draggbar via tittelbaren (grab/grabbing cursor)
- Resizable via CSS `resize: both` (håndtak nede til høyre)
- Lukkes med ✕-knapp eller «Avbryt» – **ikke** ved klikk utenfor
- Tilbakestiller posisjon til midten ved ny åpning
- Fontstørrelse 16px eksplisitt på alle inputfelter (nettlesere arver ikke font-size inn i form-elementer)

**Feltene:**
- Tittel (norsk) – påkrevd
- Korttittel / linkTitle – valgfri, brukes som slug-kilde
- Vekt – forhåndsutfylt med gjeldende sides vekt + 1
- Status – dropdown med gyldige verdier + blank (utelater `status:` fra frontmatter)
- Innhold (markdown) – valgfri brødtekst

**GitHub API – atomisk commit (Git Data API):**
Alle filendringer (nye filer + vektjusteringer for søsken) skjer i **én enkelt commit** via Git Data API (trees-APIet). Flyt:
1. `GET /git/ref/heads/main` → hent current commit SHA
2. `GET /git/commits/{sha}` → hent current tree SHA
3. Parallel fetch: sibling-filer som trenger vektjustering (`fetchSiblingWeightUpdates`)
4. `POST /git/trees` med alle filer (NB + EN + oppdaterte søsken) → ny tree SHA
5. `POST /git/commits` → ny commit SHA
6. `PATCH /git/refs/heads/main` → oppdater ref

Dette gir **nøyaktig 1 push per ny side** uansett antall søsken, og eliminerer race condition mot `ensure-uuids.yml`.

**Commit-meldingsformat:** `Ny side: <tittel>`

**UUID:** Legges til av `ensure-uuids.yml` etter push (kjører én gang, alltid grønn).

### Sidebar-menyendringer (2026-03-10 kveld)

**alwaysopen fjernet fra samt-bu-drafts:**
`alwaysopen: true` var satt på aktørmapper (kommuneforlaget, samt-bu-pilot-1, novari-hk-dir) i `samt-bu-drafts`. Dette ga klassen `parent` i `menu.html`, som trigget `font-family: 'DIN-bold'` fra theme.css og forstyrret den bold-baserte brødsmuleindikasjonen. Løst i to steg:
1. `menu.html`: `alwaysopen`-noder bruker nå klassen `alwaysopen` (ikke `parent`)
2. `custom-head.html`: `#sidebar ul.topics li.alwaysopen > ul { display: block; }` beholder åpen-effekten uten bold
3. Deretter fjernet `alwaysopen: true` helt fra alle 6 filene i samt-bu-drafts – standard menyoppførsel er ønsket

**Pilikon-klikk uten navigasjon:**
Tidligere: `<i class="category-icon">` lå inne i `<a>`. `stopPropagation()` på ikonet virket ikke pålitelig fordi klikk i `<a>`-padding ble registrert som klikk på `<a>`, ikke `<i>`.

Løsning: Flytte hendelsen til `<a>`-handler som sjekker `e.target`:
```javascript
jQuery('#sidebar a').on('click', function(e) {
    var icon = $(e.target).hasClass('category-icon') ? $(e.target) : null;
    if (icon) {
        e.preventDefault();
        icon.toggleClass('fa-sort-down fa-caret-right');
        icon.closest('li').children('ul').toggle();
    }
});
```
- Klikk på ikonet: `preventDefault()` stopper navigasjon, toggle submenyen
- Klikk på tekst: navigerer normalt
- Flere submenyer kan være åpne samtidig (JS lukker ikke andre ved toggle)
- Merk: ved navigasjon (tekst-klikk) re-rendrer Hugo sidebar og viser kun gjeldende sti

**Tekst-trunkering i sidebar:**
`<a>` er nå `display: flex` med `<span flex:1; min-width:0; padding-right:6px>`. `text-overflow: ellipsis` (som allerede var i theme.css) virker nå korrekt: lang menytekst kuttes med `...` med litt luft før ikonet/kanten.

---

## Endringslogg – 2026-03-11

### «Slett denne siden» – implementert

Nytt menyvalg i Endre-dropdown. Endringer i `hugo-theme-samt-bu/layouts/partials/edit-switcher.html` og `custom-footer.html`.

**Synlighet:** Vises kun når `.File` finnes (ikke på autogenererte listesider) og `$entrySlug != ""` og `$dirPath != "content"`. Rødt med søppelkasse-ikon (`fa-trash-o`).

**Bekreftelsesdialog:** Sentrert overlay-modal (ikke float), som «Ny side»-dialogen. To seksjoner i samme `#del-overlay`:
- `#del-confirm-section` – viser tittel, «Er du sikker?», Slett- og Avbryt-knapper
- `#del-build-section` – vises etter vellykket sletting, med bygg-status og Lukk/OK-knapper

**Atomisk sletting (Git Data API):**
`deleteFilesInOneCommit(token, repo, paths, commitMsg)` sletter begge språkfiler i én commit:
1. `GET /git/ref/heads/main` → current commit SHA
2. `GET /git/commits/{sha}` → tree SHA
3. `POST /git/trees` med `{ path, mode, type, sha: null }` per fil som skal slettes
4. `POST /git/commits` → ny commit
5. `PATCH /git/refs/heads/main` → oppdater ref

**Navigering etter sletting:** `.Parent.Pages`-loop i Hugo-template beregner `$afterDeleteUrl`:
- Forrige søsken (url for siden rett over gjeldende i seksjonsrekkefølge) – foretrekkes
- Neste søsken – om gjeldende er første
- Foreldresiden (`$parentUrl`) – fallback
**Viktig:** `.PrevInSection`/`.NextInSection` virker IKKE for seksjonsider (`_index.md` branch bundles) – disse er alltid nil. Manuell loop er eneste løsning.

**Bygg-polling (GitHub Actions API):**
`pollBuild(startTime)` kaller `GET /repos/SAMT-X/samt-bu-docs/actions/workflows/hugo.yml/runs?per_page=5` hvert 5. sekund. Filtrerer på `run.created_at >= startTime - 30000` (30s klokke-buffer). Status-tekst:
- `queued` eller `in_progress` → «Bygging av nettstedet pågår – forventet ~1 min – X sek så langt»
- `completed/success` → 3 sekunders nedtelling («Navigerer om 3 sek… / 2 sek… / 1 sek…») → `navAfterDelete()`
- `completed/failure` → feilmelding

**Bakgrunnspolling (dialog kan lukkes):**
`activePollTimer` er modul-variabel. `closeDialog()` fjerner IKKE timeren – polling fortsetter i bakgrunnen. `navAfterDelete()` kaller `window.location.href = afterDeleteUrl + '?_=Date.now()'` (cache-bust) selv om dialog er lukket.

**Jobbindikator i footer (`#del-job-indicator`):**
Vises (`display:flex`) i det svarte footerfeltet (nede til venstre) så lenge polling kjører. Viser `fa-spinner fa-spin` + tekst «Oppdateringsjobb pågår». Skjules (`display:none`) i `navAfterDelete()`.

**Fontarv – mønster:**
Nettlesere arver IKKE `font-size` inn i `<button>`-elementer. Eksplisitt `font-size:16px; font-family:inherit` nødvendig på alle knapper i dialogen.

**Token-funksjoner – global scope:**
`getStoredToken()`, `storeToken()` og `doGitHubLogin()` ligger i global `<script>`-blokk øverst i `custom-footer.html`, delt av alle redigeringsfunksjoner. (Erstattet `getDecapToken()` i 2026-03-11-sesjonen.)

### Hugo-template-variabel scope (lært mønster)

`:=` deklarerer i **gjeldende scope** – ikke tilgjengelig i ytre blokker.
`=` tilordner til en allerede deklarert variabel (ytre scope).

**Mønster for å løfte en variabel ut av en `{{ if }}`-blokk:**
```hugo
{{ $dirPath := "" }}         ← deklarér i ytre scope
{{ if .File }}
  {{ $dirPath = ... }}       ← tilordne (ikke :=)
{{ end }}
{{ $dirPath }}               ← tilgjengelig her
```

Galt: `{{ $dirPath := ... }}` inne i `{{ if .File }}` → variabelen eksisterer ikke utenfor blokken.

### Bash-kommandokjeder – aldri bruk `cd ..`

Bash-verktøyet resetter arbeidskatalog mellom kall. `cd ..` i en kjede av kommandoer (med `&&`) fungerer IKKE forutsigbart og kan føre til at `git add` leter i feil mappe. Bruk alltid absolutte stier.

### Ny veikart-oppføring: GitHub-auth uavhengig av CMS

Opprettet `solution-samt-bu-docs/content/veikart/github-auth-uavhengig-av-cms/`. Dokumenterer at `getDecapToken()` leser Decap-spesifikke localStorage-nøkler (`netlify-cms-user`, `decap-cms-user`) og at dette er en risiko ved CMS-bytte. Tre alternativer: A (PAT-input), B (selvstendig OAuth-flyt), C (utvid getDecapToken med nøytral nøkkel som overgangsløsning).

---

## Endringslogg – 2026-03-11 (natt)

### «Ny side» – UUID vises ikke på siden (rotårsak funnet og fikset)

**Symptom:** Nye sider manglet `ID:`-feltet i metadata-linjen på nettstedet, selv om UUID lå i frontmatter på GitHub.

**Rotårsak 1 – Race condition i bygg-polling (`custom-footer.html`):**
«Ny side»-commit trigger to `hugo.yml`-kjøringer:
1. Bygg A – fra «Ny side»-commit (uten UUID)
2. Bygg B – fra `ensure-uuids`-commit (med UUID)

`ID:`-feltet rendres av `header.html` linje 106–108 via `{{ with .Params.id }}` – vises kun når UUID er i frontmatter. Siden `ensure-uuids` alltid committer UUID etter en ny side, gir bygg A et midlertidig deployet nettsted uten UUID.

Polling erklærte «ferdig» for tidlig (etter kun bygg A) → navigering til side deployet av bygg A → ingen UUID synlig.

**Fix:** `lastAllCompleteAt`-variabel (grace-periode). Etter at alle kjente bygg er ferdige, venter polling 15 sekunder før navigering. Hvis bygg B starter i mellomtiden → `anyPending = true` → grace nullstilles → polling venter på bygg B. `per_page` økt fra 5 til 20 for å fange flere bygg.

```javascript
if (anyPending) {
    lastAllCompleteAt = 0; // reset grace
    ...
}
if (!lastAllCompleteAt) { lastAllCompleteAt = Date.now(); }
if (Date.now() - lastAllCompleteAt < 15000) { return; } // vent 15 sek
// Ferdig
```

**Rotårsak 2 – `ensure-uuids.yml` push-konflikt (alle 4 repoer):**
Raske påfølgende sideopprettinger → to `ensure-uuids`-kjøringer overlapper → siste `git push` avvises stille → UUID mistes permanent (ingen retry, ingen feilmelding).

**Fix:** Retry-løkke i alle 4 `ensure-uuids.yml` (samt-bu-docs, team-architecture, samt-bu-drafts, solution-samt-bu-docs):
```yaml
for i in 1 2 3; do
  git pull --rebase origin main && git push && break
  echo "Push-forsøk $i feilet, prøver igjen..."
  sleep 3
done
```

**Forventet totalvente-tid:** ~50s bygg + 15s grace = ~65 sekunder.
**Fallback:** Hvis grace-perioden utløper før bygg B starter (ensure-uuids meget sen), navigeres til side uten UUID. En manuell reload etter ~1 min viser UUID (bygg B ferdig). Med retry-fiksen vil ensure-uuids alltid committe UUID, så reload fungerer som forventet.

---

## Endringslogg – 2026-03-11 (sen natt)

### «Underkapittel»-dialog – implementert

Erstatter alert-popup med ekte dialog (gjenbruker `#np-overlay`).

**Ny global funksjon:** `openNewChildDialog(repo, dirPath, lang, currentPermalink)` i `custom-footer.html` IIFE.

**Ny variabel `npMode = 'sibling' | 'child'`** styrer:
- URL-beregning i submit-callback:
  - `child`: `currentPermalink.replace(/\/?$/, '/') + slug + '/'`
  - `sibling`: `currentPermalink.replace(/\/[^\/]+\/?$/, '/') + slug + '/'`
- Dialogtittel og knapp-tekst i `showNpBuildPanel()`

**`openNewSiblingDialog`** fikk `npMode = 'sibling'` + eksplisitt reset av dialogtittel.

**`edit-switcher.html`:** Underkapittel-valget vises ved `ne $dirPath "content"` (ikke på rot). `onclick` kaller `openNewChildDialog(...)`.

### UUID vises ikke etter ny side – rotårsak #3 funnet og fikset

**Rotårsak (ny):** `ensure-uuids.yml` pusher med `GITHUB_TOKEN`. GitHub blokkerer per design at `GITHUB_TOKEN`-pusher trigger andre workflows. UUID-commiten trigget derfor aldri `hugo.yml` → bygg B eksisterte ikke → reload hjalp ikke (UUID ble aldri deployet).

**Fix i `ensure-uuids.yml`:**
1. `actions: write`-permission lagt til
2. Commit-steget fikk `id: uuid-commit` + `echo "changed=true/false" >> $GITHUB_OUTPUT`
3. Nytt steg: kaller `workflow_dispatch` på `hugo.yml` hvis `changed == 'true'`

```yaml
- name: Trigger Hugo-bygg for UUID-commit
  if: steps.uuid-commit.outputs.changed == 'true'
  run: |
    curl -s -X POST \
      -H "Authorization: Bearer ${{ secrets.GITHUB_TOKEN }}" \
      -H "Accept: application/vnd.github+json" \
      https://api.github.com/repos/SAMT-X/samt-bu-docs/actions/workflows/hugo.yml/dispatches \
      -d '{"ref":"main"}'
```

`workflow_dispatch` via GITHUB_TOKEN fungerer (direkte API-kall, ikke push) og trigget `hugo.yml` korrekt.

**OBS:** 15s grace-periode i `npPollBuild` er nå mer avgjørende enn noensinne – `workflow_dispatch`-bygget starter noe etter UUID-commiten.

### Ny veikart-oppføring: Slett side med undermapper

`solution-samt-bu-docs/content/veikart/slett-side-med-undermapper/` – dokumenterer at «Slett denne siden» kun sletter `_index.nb.md` + `_index.en.md`, ikke undermapper. To alternativer: A) blokker sletting hvis siden har barn (anbefalt, enkelt), B) rekursiv sletting via Trees API.

---

## Endringslogg – 2026-03-11 (ettermiddag)

### «Rediger innhold» (qe-dialog) – WYSIWYG med frontmatter-redigering

#### Hva er implementert

**Frontmatter-feltredigering** (`#qe-meta-panel` i `edit-switcher.html`):
- Fire felt vises mellom headerbar og editor: Tittel (`title`), Meny (`linkTitle`), Vekt (`weight`), Status (dropdown)
- Populeres automatisk fra filens YAML-frontmatter ved åpning
- Lagres tilbake til frontmatter ved «Lagre»-klikk (atomisk commit via Git Data API)
- `linkTitle`/`weight`/`status` utelates fra frontmatter om feltet er tomt (fjernes med `removeFmField`)

**YAML-helpere** i qe-dialog IIFE (`custom-footer.html`):
- `parseFmField(fm, key)` – henter én YAML-linje fra frontmatter-streng
- `setFmField(fm, key, line)` – erstatter/legger til YAML-linje
- `removeFmField(fm, key)` – fjerner YAML-linje
- `qeYamlStr(s)` – siterer verdi hvis nødvendig (inneholder `:` eller `"`)

**Quill WYSIWYG-editor** (Quill v1.3.7 fra jsDelivr CDN):
- `#qe-editor-area` som flex-kolonne-wrapper → toolbar som sibling + container med `flex:1`
- Turndown (markdown→HTML) + Turndown GFM-plugin for tabellkonvertering ved lagring
- `marked.parse()` for HTML→Quill på åpning
- Paste-handler for bilder (base64 → legges til `qeImages`/`qeImageMap`, committes som separate filer)

**Tabellknapp (⊞):**
- Setter inn GFM-tabellmal som ren tekst via `qeEditor.insertText(idx, tbl, 'user')`
- Hugo + Turndown håndterer GFM-tabeller i Markdown – ingen Quill-plugin nødvendig

#### Hva feilet – quill-better-table

Forsøkte å integrere `quill-better-table@1.2.10` for visuell tabellredigering. Tre runder med feilsøking:

| Problem | Rotårsak |
|---------|---------|
| `TypeError: e is not a constructor` | CDN-global heter `window.quillBetterTable` (lowercase), ikke `QuillBetterTable` |
| `quill: Cannot import modules/better-table` | Feil global-referanse, registrering feilet stille |
| `TypeError: Failed to execute 'insertBefore' on 'Node'` | QBT-modulens konstruktør gjør DOM-manipulasjon som feiler i `position:fixed`-containere |

**Konklusjon:** quill-better-table er fundamentalt inkompatibel med fixed-position overlays. Fjernet helt.

#### Kjent begrensning – Quill generelt

Quill v1 rendrer tabeller som rå Markdown-tekst (` | col | col | `), ikke som visuell tabell. Brukere ser og redigerer tabellsyntaks direkte, ikke en visuell tabellcelle-editor. Dette er akseptabelt som mellomløsning, men ikke ideelt.

**Neste steg:** Vurdere **TipTap** som erstatning for Quill. Se veikart-oppføring `veikart/tiptap-som-editor/`.

#### Viktig note for eventuell tilbakevending til Quill

Paste av bilder er implementert i qe-dialog (paste-handler på `qeEditor.root`), men **er ikke testet i produksjon** i denne sesjonen. Mønsteret ble først validert for np-dialog («Ny side»). Verifiser at bildelasting, base64-lagring og commit fungerer likt for qe-dialog.

#### Layout-fix: dobbelt toolbar

**Problem:** `#qe-body-quill` hadde `display:flex; flex-direction:column` inline. Quill v1 inserter toolbar som DOM-sibling *før* container-elementet, i *foreldreelementet*. Dette ga to toolbars (en i `#qe-editor-area`, en i foreldren).

**Fix:** Fjerne flex-stilene fra `#qe-body-quill` direkte. Gi i stedet `#qe-editor-area` flex-column-rollen. `#qe-body-quill` er da et vanlig blokk-element – Quill inserter toolbar som forventet sibling i `#qe-editor-area`.

---

## Endringslogg – 2026-03-11 (kveld)

### TipTap erstatter Quill – begge editordialoger

Quill v1 (+ Turndown + marked) er fjernet. TipTap v2 er ny editor i både `qe-dialog` («Rediger innhold») og `np-dialog` («Ny side»/«Underkapittel»).

#### Arkitektur

**Lasting:** Dynamic `import()` fra `esm.sh` – ingen bundler nødvendig. Delt `loadTiptap()` funksjon i global `<script>`-blokk (etter token-funksjonene). Pakker som lastes:
- `@tiptap/core@2` – Editor-klassen
- `@tiptap/starter-kit@2` – bold, italic, headings, lists, code, blockquote
- `@tiptap/extension-table@2` + TableRow, TableCell, TableHeader – visuell ProseMirror-tabell
- `@tiptap/extension-link@2` – lenker
- `@tiptap/extension-image@2` – bildeinnsetting (bildelim)
- `tiptap-markdown` – Markdown roundtrip via `editor.storage.markdown`

**Tilstand:** `window._Tiptap` caches alle extensions etter første lasting. `window._tiptapLoading` forhindrer dobbelt-import. `'tiptap-ready'`-event synkroniserer ventende callbacks.

**Markdown roundtrip:**
- Inn: `editor.commands.setContent(markdownString)` – `tiptap-markdown` parser direkte
- Ut: `editor.storage.markdown.getMarkdown()` – serialiserer til Markdown
- Erstatter Turndown + marked (som begge krevde HTML-mellomsteg)

#### Editor-containere

| | Quill (gammel) | TipTap (ny) |
|---|---|---|
| qe-dialog editor | `#qe-body-quill` | `#qe-body-pm` |
| np-dialog editor | `#np-body-quill` | `#np-body-pm` |
| Toolbar | Quill Snow (innebygd) | Custom HTML `#qe-toolbar` / `#np-toolbar` |
| CSS-klasser | `.ql-*` | `.ProseMirror`, `.tiptap-toolbar` |

**Toolbar-mønster:** HTML-knapper med `data-qe`/`data-np`-attributter. Klikk-handler på toolbar-containeren. `is-active`-klasse oppdateres via `editor.on('selectionUpdate')` og `editor.on('transaction')`.

**qe-toolbar** inkluderer i tillegg: addRowBefore, addRowAfter, deleteRow, addColBefore, addColAfter, deleteCol – tabelloperasjoner fra toolbar.

#### Bildepaste

Paste-handler på `editor.view.dom` (ProseMirror-roten). Lagrer base64 i `qeImages`/`npImages`, viser data-URL i editor. Ved lagring: string-replace i markdown-output → commit som blob via Git Data API.

#### Hva ble IKKE endret

- `openQuillEditDialog`-funksjonsnavnet beholdes for bakoverkompatibilitet med `edit-switcher.html`-kall
- All GitHub API-flyt (commit, poll, navigation) er uendret
- Frontmatter-feltene (title, linkTitle, weight, status) er uendret
- `parseFmField`, `setFmField`, `removeFmField`, `qeYamlStr` er uendret

#### Mulig fremtidig problem: tiptap-markdown eksport

`tiptap-markdown` er importert som `mods[8].Markdown || (mods[8].default && mods[8].default.Markdown) || mods[8].default` – defensiv fallback i tilfelle esm.sh wrapper gir default-eksport i stedet for named export. Verifiser i DevTools at `window._Tiptap.Markdown` er en funksjon (TipTap extension) etter første lasting.

---

## Endringslogg – 2026-03-11 (sen kveld)

### Div. bugfikser og layout-forbedringer etter TipTap-migrering

#### 404-feil for Altinn CSS fjernet

`custom-head.html` linje 2–3 refererte `altinndigitalisering.css` og `altinn.css` – begge manglende filer (arv fra Docdock-malen, aldri lagt til). Ga 404-støy i konsollen. Linjene er fjernet.

`DINWeb*.woff`-fontene referert fra `designsystem.css` (via `../fonts/`) finnes heller ikke, men disse er i en fil vi ikke eier. Harmløse da `custom-head.html` uansett overstyrer til Helvetica/Arial.

#### Nummerert liste i TipTap-editor viste ikke tall

Global CSS (theme/designsystem) nullstilte `list-style` på alle lister. Fiks: eksplisitte CSS-regler i `edit-switcher.html`:
```css
#qe-body-pm .ProseMirror ul, #np-body-pm .ProseMirror ul { list-style-type: disc; }
#qe-body-pm .ProseMirror ol, #np-body-pm .ProseMirror ol { list-style-type: decimal; }
```

#### `hide_toc`-frontmatter – skjul innholdsfortegnelse

Ny parameter `hide_toc: true` i frontmatter skjuler `<aside id="page-toc">` og lar `#body` (flex:1) ta full bredde automatisk.

- **`footer.html`:** `{{ if not .Params.hide_toc }}<aside ...>...</aside>{{ end }}`
- **`edit-switcher.html`:** Checkbox «Skjul innholdsfortegnelse» / «Hide TOC» i qe-meta-panel
- **`custom-footer.html`:** `parseFmField(qeFrontmatter, 'hide_toc') === 'true'` ved åpning; `setFmField`/`removeFmField` ved lagring

#### qe-dialog header og meta-panel – layout-fiks

Flere iterasjoner. Endelig tilstand:

**Blå header-bar:**
- Tre-kolonnestruktur: `<div flex:1>` (spacer) | `#qe-title` (sentrert) | `<div flex:1 justify:flex-end>` (knapper)
- Tittel: `font-size:1.35rem; font-weight:700`
- Tittel-tekst: `Rediger side: <tittel>` / `Edit page: <title>` – uten hermeteikn
- `jsonify`-wrapping ga synlige `"..."` rundt tittelen – stripes i JS med `.replace(/^"(.*)"$/, '$1')`

**Grått meta-panel:**
- Innhold wrappes i `max-width:960px; margin:0 auto` – flush med editor-kolumnen
- CSS-regel normaliserer alle form-kontroller til uniform høyde:
  ```css
  #qe-meta-panel input[type="text"],
  #qe-meta-panel input[type="number"],
  #qe-meta-panel select {
    height: 2rem; box-sizing: border-box; padding: .3rem .5rem;
    border: 1px solid #bbb; border-radius: 3px; font-size: 14px;
    font-family: inherit; line-height: 1.2; vertical-align: middle;
  }
  ```
- `<select>` ignorerer padding-basert høyde på tvers av nettlesere – `height: 2rem` i CSS-regel er eneste pålitelige fix
- Tittel-felt: 280px (fra 200px); Meny-felt: 150px
- Inline `style`-attributter på hvert felt ryddet – CSS-regelen tar over

**Fortsatt gjenstår:** Avklart og fikset i påfølgende sesjon (se endringslogg 2026-03-11 sen kveld / ny sesjon nedenfor).

---

## Endringslogg – 2026-03-11 (ny sesjon, kveld)

### qe-dialog meta-panel: input/select høyde og vertikal linjering

Flere runder med feilsøking. Endelig løsning:

- Fjernet eksplisitt `height`-attributt på alle felter – Chrome ignorerer `height` på `<select>` inkonsistent
- Bruker `padding:.25rem .4rem` (inputs) og `padding:.25rem .3rem` (select) – lar begge elementtyper size naturlig fra innhold + padding → konsistent høyde på tvers av nettlesere
- CSS-regelen `#qe-meta-panel input, select { height: 2rem; }` i `edit-switcher.html` `<style>`-blokk beholdes og tar over fra inline `style`-attributter

### Decap CMS fjernet fullstendig

**Steg 1 – Uavhengig OAuth-flyt (`custom-footer.html`):**
- `getDecapToken()` erstattet med `getStoredToken()` + `storeToken()` + `doGitHubLogin(onSuccess)`
- Token lagres i `samt-bu-gh-token` (eget localStorage-nøkkel)
- Fallback til Decap-nøkler (`netlify-cms-user`, `decap-cms-user`) for migrering av eksisterende sesjoner
- Alle fire dialog-åpnere (Ny side, Rediger, Slett) kaller nå `doGitHubLogin(callback)` i stedet for `alert("Du må logge inn via Decap CMS...")` når token mangler
- Workeren (`samt-bu-cms-auth.erik-hag1.workers.dev`) er uendret – støttet protokollen fra før

**Steg 2 – Rydding av Decap-portaler og edit-switcher:**
- 18 filer slettet fra `static/edit/` (alle CMS-portaler: docs/arkitektur/utkast/loesninger × nb/en + to oversiktssider)
- Edit-switcher: «Denne siden (Decap)» og «Andre valg»-menypunkter fjernet
- Variabler fjernet: `$collection`, `$portalPath`, `$overviewPath`, `$portalURL`, `$overviewURL`, `$pageEditURL`, `$addChildURL`

### Menytekster i Endre-dropdown

| Gammelt | Nytt |
|---------|------|
| «Rediger innhold» | «Rediger dette kapitlet» |
| «Side – samme nivå» | «Nytt kapittel etter dette» |
| «Underkapittel» | «Nytt underkapittel» |

**OBS:** i18n-filer (`i18n/nb.toml` og `en.toml` i `samt-bu-docs`) overstyrer template-default. Endringer i template-default alene har ingen effekt hvis i18n-nøkkelen finnes. Oppdatering måtte gjøres i begge steder.

Ikon for «Nytt underkapittel» endret fra `fa-plus` til `fa-folder-o`.

---

## Endringslogg – 2026-03-12

### «Ny side»-dialog og «Nytt underkapittel»-dialog: full-skjerm layout

Begge dialogene (menyvalg 2 og 3) bruker nå samme full-skjerm layout som qe-dialog (menyvalg 1).

**Endringer i `hugo-theme-samt-bu`:**

- `edit-switcher.html`: Erstattet lite flytende modal (680px, draggbar, `resize:both`) med full-skjerm overlay:
  - Blå header-bar med `#np-dialog-title`, `#np-status-text`, Avbryt og Opprett-knapp
  - Grått meta-panel med feltene Tittel, Meny, Vekt, Status (horisontalt, som qe)
  - TipTap-editor (`#np-body-pm`) fyller resten av skjermen
  - Feilmelding (`#np-msg`) vises som rød stripe under meta-panel
  - `Opprett side`-knappen er `type="submit" form="np-form"` (HTML5 form-assosiasjon – knapp utenfor `<form>`)
  - CSS: `#np-form input/select` får `height:2rem`-normalisering (likt qe-meta-panel); `#np-body-pm` er nå flex:1 full-høyde

- `custom-footer.html`:
  - Fjernet drag-logikk (~30 linjer)
  - `openNewSiblingDialog` / `openNewChildDialog`: fjernet posisjon-reset, `overlay.style.display = 'flex'`
  - Ny `setNpStatus(text)` – oppdaterer `#np-status-text` i header (som `setStatus` i qe)
  - `showNpBuildPanel`: kun `setNpStatus(...)` – ikke lenger form-hide/build-section-show
  - `npPollBuild`: bruker `setNpStatus` konsekvent, fjernet `#np-panel-done`-referanser
  - Fjernet `#np-close-x`- og `#np-panel-close`-lyttere

### Vurdering: Cloudflare Pages som erstatning for GitHub Pages

**Problem:** GitHub Pages CDN-propagering tar 1–3 minutter *etter* at `hugo.yml` viser grønt bygg. Dette er ikke noe vi kan fikse fra nettleser-polling – det er GitHub Pages' interne pull-baserte CDN-arkitektur.

**Cloudflare Pages:** Push-basert CDN. Siden er tilgjengelig 5–15 sekunder etter at bygget er ferdig og filene er lastet opp. Gratis (500 bygg/mnd – reelt tak er ~16 push/dag).

**Anbefalt migrasjonsstrategi (Alternativ B):**
- GitHub Actions beholder all eksisterende logikk (inject-lastmod, HUGO_MODULE_REPLACEMENTS, etc.)
- Siste deploy-steg byttes ut: `Deploy to GitHub Pages` → `wrangler pages deploy ./public`
- Ny URL: `https://samt-bu-docs.pages.dev/` (ingen substi `/samt-bu-docs/`)
- `baseURL` og `editURL` i `hugo.toml` oppdateres
- Cloudflare-konto finnes allerede (OAuth-worker)
- Custom domene (f.eks. `samt-x.no`) er ikke nødvendig, men mulig (~100–200 kr/år)
- Secrets som trengs i GitHub: `CF_API_TOKEN` + `CF_ACCOUNT_ID`

**Status:** Ikke implementert – notert for neste sesjon.

---

## Endringslogg – 2026-03-12 (sesjon 2)

### ✅ Cloudflare Pages – FERDIG

Migrasjonen fra GitHub Pages til Cloudflare Pages ble gjennomført:

- **`hugo.toml`:** `baseURL` endret til `https://samt-bu-docs.pages.dev/`
- **`.github/workflows/hugo.yml`:** GitHub Pages-steg (`configure-pages`, `upload-pages-artifact`, separat `deploy`-jobb) erstattet med ett steg: `npx wrangler pages deploy ./public --project-name samt-bu-docs --branch main`
- Secrets lagt til i GitHub: `CF_API_TOKEN`, `CF_ACCOUNT_ID`
- Cloudflare Pages-prosjekt opprettet via wrangler CLI
- **Ny nettstedsadresse:** `https://samt-bu-docs.pages.dev/`
- **Gammel adresse** (`https://samt-x.github.io/samt-bu-docs/`) er ikke lenger aktiv

**Effekt:** CDN-propagering til norske noder ned fra 1–3 min → 5–20 sek etter grønt bygg.

### ✅ GUI-tilbakemelding for byggestatus – FERDIG

Tre separate polling-mekanismer implementert i `custom-footer.html`:

| Case | Utløser | Metode | Hastighet |
|------|---------|--------|-----------|
| 1 – Rediger side | Lagre i qe-dialog | ETag-sammenligning (same-origin HEAD-poll, 1 sek intervall) | ~15–20 sek etter grønt bygg |
| 2 – Ny side | Opprett i np-dialog (sibling) | URL-poll 404→200 (1 sek intervall) | ~0 sek etter grønt bygg |
| 3 – Nytt underkapittel | Opprett i np-dialog (child) | URL-poll 404→200 (1 sek intervall) | ~0 sek etter grønt bygg |

**ETag-polling (case 1):** `HEAD`-request med `cache: no-store` + cachebust-param (`?_cf=<timestamp>`) mot samme URL. Sammenligner `etag` / `last-modified`-headere. Endring → side ble deployet. Fallback til GitHub Actions API-polling hvis ETag ikke er tilgjengelig.
Maks 180 forsøk (1 sek intervall = 3 min). **Ved timeout:** Kaller GitHub Actions API for å sjekke faktisk status – rapporter feil kun hvis API bekrefter det (se `bygg-feil-timeout`-fiks, sesjon 21).

**URL-polling (cases 2+3):** `HEAD` mot ny side-URL. HTTP 200 → siden finnes. Krever ingen token.
Maks 90 forsøk (90 sek). **Ved timeout:** Samme GitHub API-sjekk som ETag-poll. `startUrlPoll(url, onDone, onError, onStatus, startTime)` – `startTime` er valgfri, `npPollBuild()` sender den alltid.

**CORS-begrensning:** `api.cloudflare.com` blokkerer cross-origin kall fra nettleser (CF Pages `pages.dev`-domene). Cloudflare API er derfor ikke aktuelt fra browser – GitHub Actions API og same-origin polling brukes i stedet.

**UUID generert client-side:** `crypto.randomUUID()` (med fallback) genererer UUID i nettleseren for nye sider. Eliminerer behovet for at `ensure-uuids`-botten lager en ekstra commit → reduserer ventetid for cases 2+3 med ~40 sek.

**Auto-navigasjon (case 1):** Etter ETag-endring vises «✓ Ferdig! Laster inn om 2 sek…» + «Last inn nå ↗»-knapp. Siden lastes automatisk etter 2 sekunder.

### ✅ Statustekst – «Nettsted oppdateres (x sek)»

«Venter på deploy…» / «Waiting for deploy…» erstattet med «Nettsted oppdateres (x sek)…» / «Updating site (xs)…» med live sekund-teller. Fjerner teknisk jargon («deploy») fra brukergrensesnittet.

### ✅ Knapper og feilhåndtering

- **«Lagre»-knapp etter feil:** Vises nå som «Prøv igjen» (ikke «Lagre») etter lagrefeil
- **Feilmelding oversatt:** «Update is not a fast forward» → «Konflikt: siden ble endret av andre. Prøv igjen.»
- **Knapp-stil ved feil:** `background` og `cursor` nullstilles riktig (gråstil fra vellykket lagring henger ikke igjen)
- **np-dialog Opprett-knapp:** Disabled umiddelbart ved klikk (før token-sjekk og validering). Re-enables med riktig tekst (norsk/engelsk, sibling/child) ved feil
- **Automatisk retry:** `tryCommit()` wrapper kaller `createQeCommit` opptil 2 ganger ved «Update is not a fast forward». Viser «Prøver på nytt…» mellom forsøkene (1,5 sek pause). Håndterer GitHub API-caching og ensure-uuids race condition usynlig for brukeren

### ✅ Slett-dialog – polling og UX-fiks

- **Tittel med doble quotes:** `{{ .Title | jsonify }}` i `edit-switcher.html` sender `"tittel"` med omsluttende quotes. Strippes nå i `openDeleteDialog` (samme fix som qe-dialog tittel): `title.replace(/^"(.*)"$/, '$1')`
- **Statustekst:** «Bygger…» / «Bygging av nettstedet starter om litt…» erstattet med «Nettsted oppdateres (x sek)…» med elapsed-sekunder
- **Polling – GH Actions API erstattet med URL 404-poll:** `pollBuild` brukte `startGhPoll` (2 sek intervall, treig GH API). Erstattet med same-origin HEAD-poll mot nåværende side-URL (`window.location.href`) som venter på HTTP 404 – siden forsvinner fra CF CDN når bygget er ferdig. Mønster: 200→404 (omvendt av ny-side: 404→200). Ventetid: tilnærmet null etter grønt bygg, typisk 1–5 sek (pollintervall 1 sek).

### ✅ np-dialog – Opprett-knapp grå ved innsending

`submitBtn.style.background = '#888'; submitBtn.style.cursor = 'default'` lagt til når knappen settes til «Oppretter…». Nullstilles i catch-blokken ved feil. Konsistent med «Lagret»-knappen i qe-dialog.

### ✅ Statustekst – fontstørrelse økt

`font-size:.85rem` → `font-size:1rem` på `#np-status-text` og `#qe-status-text` i `edit-switcher.html`. Opacity justert `.8` → `.85`.

### Veikart: Bygg-status-sperre og Lukk-knapp

Ny veikart-oppføring: `veikart/bygg-status-sperre/`. Noterer:
- «Avbryt»-knappen er misvisende etter at commit er sendt – commit kan ikke angres
- Forslag: rename til «Lukk dette vinduet» + informasjonstekst om at bygget fortsetter
- Forslag: sjekk GitHub Actions API ved åpning av redigeringsdialog – vis advarsel hvis bygg allerede kjører (kryssbruker-synlig via GH Actions API, token finnes allerede)

---

## Endringslogg – 2026-03-13

### ✅ UUID-workflow slått sammen (SLÅTT SAMMEN)

`ensure-uuids.yml` slettet i alle 4 repoer. UUID-steget kjører nå som del av:
- `hugo.yml` (samt-bu-docs) – steget kjøres rett etter checkout, FØR modul-checkout og bygg
- `trigger-docs-rebuild.yml` (team-architecture, samt-bu-drafts, solution-samt-bu-docs) – steget kjøres FØR `repository_dispatch`-kallet

Viktige detaljer:
- `[skip ci]`-tag i commit-melding forhindrer at UUID-commiten trigger ny workflow-kjøring
- `if: github.actor != 'github-actions[bot]'` på jobbnivå i `trigger-docs-rebuild.yml` forhindrer løkke
- `permissions: contents: write` nødvendig for at workflow-bot kan pushe
- Retry-løkke (for i in 1 2 3) med `git pull --rebase origin main && git push` håndterer push-konflikter fra parallelle kjøringer
- `hugo.yml`-bygget kjøres i samme workflow-run etter UUID-steget – arbeidstre har allerede UUIDs → ingen ekstra `workflow_dispatch` nødvendig

### ✅ GUI-forbedringer – conflict-håndtering og dialog-UX

Alle endringer i `hugo-theme-samt-bu/layouts/partials/custom-footer.html`.

**Økt retry-antall:** `tryCommit(blobItems, 5)` (var 2). Re-fetcher HEAD SHA mellom hvert forsøk.

**Bot vs. menneske-distinguering ved konflikt (etter 5 mislykkede forsøk):**
```javascript
fetch('/repos/<repo>/commits?path=<fil>&per_page=1', ...)
  → login === 'github-actions[bot]' → «Lagring feilet. Prøv igjen.»
  → isHuman → «Konflikt: siden ble endret av @<login>. Prøv igjen.»
```
Fjernet uriktig «repo opptatt»-melding (Cloudflare setter push-jobber i kø uansett).

**Bygg-advarsel scopet til gjeldende fil:**
`checkBuildInProgress(filePath, callback)` tar nå `filePath`-parameter. Sjekker GitHub-commit-filer via `GET /repos/.../commits/<run.head_sha>` → `commit.files[].filename`. Advarselen vises kun hvis pågående bygg inkluderer akkurat den filen brukeren redigerer.

**«Lukk dette vinduet»-knapp i np-dialog:**
`showNpBuildPanel()` setter `#np-cancel`-knappens tekst til «Lukk dette vinduet» / «Close this window» etter commit. `openNewSiblingDialog` og `openNewChildDialog` resetter til «Avbryt»/«Cancel» ved åpning.

**Auto-reload ved ferdig bygg:**
- `qe-dialog`: byggjobb ferdig → `doNav()` kaller `window.location.href = <url>?_=<timestamp>` (reload nåværende side). Ingen «klikk for å laste inn»-melding.
- `np-dialog onDone`: `window.location.href = window.location.href.split('?')[0] + '?_=' + Date.now()` (reload nåværende side, ikke navigasjon til ny side).
- Ingen navigasjon til ny side – brukeren auto-reloades og kan eventuelt navigere selv.

### ✅ Sidebar – bug-fikser

**Kategori-ikon-posisjonering (1.1-collapse-bug):**
`category-icon` hadde `position: absolute; top: 8px; right: 6px` uten noen `position: relative` på overordnet `<li>`. Alle ikoner stakk seg opp i forhold til `#sidebar` root → ikon-klikk-områder overlappet feil `<li>`. Fiks: `#sidebar ul li { position: relative; }` i `custom-head.html`. Bekreftet fikset av bruker.

**Inkonsistent bold i sidebar (Chrome):**
`font-family: 'DIN-bold'` fra `theme.css` på `li.parent > a` / `li.active > a` rendret inkonsistent i Chrome (font-loading race eller Chrome-spesifikk rendering). To-lags løsning:

1. **CSS** (`custom-head.html`): `#sidebar ul li.parent > a, #sidebar ul li.active > a { font-weight: bold; }` – virker uavhengig av webfont-status
2. **JS** (`footer.html`): `applyActiveParent()` – setter klasser OG `a.style.fontWeight = 'bold'` (inline style) basert på `window.location.pathname` vs `data-nav-id`. Kjøres to ganger: umiddelbart + `setTimeout(fn, 0)` etter at deferred scripts er ferdige.

```javascript
function applyActiveParent() {
  var path = window.location.pathname;
  if (path.slice(-1) !== '/') path += '/';
  document.querySelectorAll('#sidebar [data-nav-id]').forEach(function(li) {
    var id = li.getAttribute('data-nav-id');
    if (!id) return;
    var isActive = id === path;
    var isParent = !isActive && id.length > 1 && path.slice(0, id.length) === id;
    li.classList.toggle('active', isActive);
    li.classList.toggle('parent', isParent);
    var a = li.querySelector(':scope > a');
    if (a) a.style.fontWeight = (isActive || isParent) ? 'bold' : '';
    var icon = li.querySelector(':scope > a .category-icon');
    if (icon) {
      icon.classList.toggle('fa-sort-down', isActive || isParent);
      icon.classList.toggle('fa-caret-right', !isActive && !isParent);
    }
  });
}
applyActiveParent();
setTimeout(applyActiveParent, 0);
```

**Viktig arkitekturnotat – scriptkjøringsrekkefølge:**
- `altinndocs-learn.js` er lastet med `defer` → kjører ETTER inline scripts i footer.html
- Inline script (footer.html) kjøres under HTML-parsing → `applyActiveParent()` kjøres FØR deferred scripts
- `setTimeout(fn, 0)` sikrer at re-apply også kjøres ETTER deferred scripts og jQuery ready-handlers
- Ingen av de deferred scripts (`altinndocs-learn.js`, `altinndocs.js`) modifiserer `parent`/`active`-klasser

**✅ Sidebar-kollaps for første child i seksjon (2026-03-13):**
Symptom: Navigering til `01-resultater-vgo` (første use case, weight:1) kollapset hele sidebaren opp til toppnivå – `Behov` og `Case-beskrivelser` ble ikke vist som ekspanderte. Alle andre sider fungerte korrekt.

Rotårsak: Ikke funnet gjennom statisk kode-analyse. CSS-klassene `parent`/`active` ble satt korrekt av `applyActiveParent()`, men `ul`-elementenes `display` ble ikke oppdatert – trolig en CSS-spesifisitets- eller timing-konflikt spesifikk for denne siden.

Fix (`footer.html`): `applyActiveParent()` setter nå `ul.style.display` **direkte** i tillegg til CSS-klasser:
```javascript
var ul = li.querySelector(':scope > ul');
if (ul) ul.style.display = (isActive || isParent) ? 'block' : '';
```
Inline `style.display` overstyrer alle CSS-regler og er robust mot spesifisitetsproblemer. Når verken aktiv eller forelder, fjernes inline-stilen og CSS tar over normalt.

---

## Endringslogg – 2026-03-13

### GitHub Pages → Cloudflare Pages redirect

Ny workflow `.github/workflows/gh-pages-redirect.yml` deployer en statisk redirect-side til GitHub Pages. Sender alle besøkende fra `samt-x.github.io/samt-bu-docs/*` til `samt-bu-docs.pages.dev/*` med stipreservering via JS.

**Nøkkelvalg:** Workflowen kjøres kun manuelt (`workflow_dispatch`) – ikke ved push. GitHub Pages beholder siste deploy permanent, så redirect-siden trenger aldri rebuildes. Eliminerer overhead på alle fremtidige push.

**Teknikk:** `index.html` + `404.html` (identiske) – GitHub Pages serverer `404.html` for alle ukjente stier → JS stripper `/samt-bu-docs`-prefix → redirect til ny URL. Meta refresh som no-JS-fallback (sender til rot, uten stipreservering).

### Windows-mappenavn og git tracking

`git` sporer aldri nye filer/mapper automatisk. Ved omdøping i Windows Utforsker: gammel mappe committes som slettet, ny mappe forblir «untracked» og må `git add`-es eksplisitt. Alltid sjekk `git status` etter mappeoperasjoner på Windows.

### CI: core.quotepath=false for UTF-8 i stier

Hugo bruker `git log -- <filsti>` for å hente `lastmod` via `enableGitInfo`. Git på Ubuntu/Linux har `core.quotepath=true` som standard → non-ASCII-tegn i stier (f.eks. `ø` i `22-analysedata-for-hele-løpet`) escapes → Hugo klarer ikke matche filen → `.Lastmod` forblir null → «Sist endret» vises ikke.

Fix i `hugo.yml` (ett steg før Hugo-bygg):
```yaml
- name: Konfigurer git for UTF-8-stier
  run: git config --global core.quotepath false
```
Gjelder alle fremtidige filer med `æ`, `ø`, `å` eller andre non-ASCII-tegn i mappenavn.

### DIN-font 404-feil (kosmetisk, ikke fikset)

`designsystem.css` inneholder `@font-face`-deklarasjoner for `DINWeb` og `DINWeb-Bold` som peker på `/fonts/DINWeb.woff...`. Filene finnes ikke → 404 i konsollen på alle sider. Ingen visuell effekt (fallback til Helvetica/Arial). Se veikart: `din-font-404`.

---

## Endringslogg – 2026-03-13 (sesjon 2)

### ✅ TipTap-versjonspinning – tiptap-markdown@0.8.10

**Problem:** Editoren sluttet å fungere for alle brukere midt i dagen. Feilmelding: «Kunne ikke laste editoren. Prøv å oppdatere siden.» (alert fra catch-blokken i `loadTiptap()`).

**Rotårsak:** `tiptap-markdown` var importert uten versjonsnummer (`https://esm.sh/tiptap-markdown`). esm.sh hadde cachet en eldre, TipTap v2-kompatibel build i måneder. Da cachen ble invalidert (sannsynligvis en CDN-vedlikeholdsoperasjon), ble `latest` resolvet på nytt fra npm → `tiptap-markdown@0.9.0`, som krever `@tiptap/core@^3.0.1`. Inkompatibelt med våre TipTap v2-importer → `Promise.all` feilet → editor utilgjengelig for alle.

**Fix:** Pinnet til `https://esm.sh/tiptap-markdown@0.8.10` (siste versjon kompatibel med TipTap v2) i `custom-footer.html`.

**Beslutning – versjonsstrategi for TipTap-importer:**

| Import | Pin-strategi | Begrunnelse |
|--------|-------------|-------------|
| `@tiptap/core`, `@tiptap/starter-kit`, `@tiptap/extension-*` | `@2` (major-pin) | Sikker mot breaking changes; v2 er stabilt og vedlikeholdt |
| `tiptap-markdown` | `@0.8.10` (eksakt pin) | v0.9.0 krever TipTap v3 – kan ikke følge major-pin |

**Oppdatering ved fremtidig behov:** Gjøres manuelt og samlet. Sjekk at alle TipTap-pakker er gjensidig kompatible (spesielt `tiptap-markdown` mot `@tiptap/core`). Test tabeller og Markdown-roundtrip i DevTools etter endring. Ingen automatisk oppfanging – eksakte pins gjør at ingenting brekker uten aktiv handling.

### ✅ Auto-reload etter sidenavigering – fikset

**Problem:** Når et bygg ble oppdaget ferdig via resume-koden (etter navigering til ny side), ble siden ikke lastet inn automatisk – «klikk for å laste inn»-meldingen ble vist i stedet.

**Rotårsak:** Resume-koden kalte `samtuShowDoneIndicator()` (som viser en klikkbar lenke), ikke direkte navigasjon.

**Fix:** Endret til `window.location.href = window.location.href.split('?')[0] + '?_=' + Date.now()` i resume-koden og i bakgrunnspollingens «egne ventende endringer»-gren.

---

## Endringslogg – 2026-03-14

### «not a fast forward» – analyse og fix

**Symptom:** Konsekvent `422 Update is not a fast forward` ved lagring mens et annet bygg var i gang, selv 30+ sekunder etter forrige lagring (ingen reell race condition mot andre brukere).

**Rotårsak:** GitHub REST API cacher `GET /git/ref/heads/main` med `Cache-Control: private, max-age=60`. `tryCommit` re-fetcher ref mellom forsøk, men får 60 sekunder gammel HEAD SHA fra nettleserens HTTP-cache. Dermed ender `PATCH /git/refs/heads/main` med å sende en foreldet SHA som parent – avvist med `not a fast forward`.

**Fix:** `cache: 'no-store'` på begge GET-kall i `createQeCommit()`:
```javascript
fetch(apiBase + '/git/ref/heads/main', { headers: h, cache: 'no-store' })
fetch(apiBase + '/git/commits/' + headSha, { headers: h, cache: 'no-store' })
```

**Viktig:** `cache: 'no-store'` er nødvendig på *begge* kall. Kun første holder ikke – commit-SHA trenger også fersk data.

### `tryCommit` – 120 sekunders deadline

`tryCommit(blobItems, deadline)` er en retry-wrapper rundt `createQeCommit()`:
- Fanger `Error('Update is not a fast forward')` og venter 2 sekunder mellom forsøk
- Deadline: `Date.now() + 120000` (2 min) – gir rom for at mange bygg kan stå i kø
- Forsøk fortsetter selv om dialogen lukkes (`overlay.style.display !== 'none'`-sjekk endret til å IKKE avbryte)
- Feiler etter deadline → brukervennlig feilmelding, «Prøv igjen»-knapp

```javascript
function tryCommit(blobItems, deadline) {
  return createQeCommit(...)
    .catch(function(err) {
      if (err.message === 'Update is not a fast forward' && Date.now() < deadline) {
        if (overlay.style.display !== 'none') setStatus('Prøver på nytt…');
        return new Promise(function(res) { setTimeout(res, 2000); })
          .then(function() { return tryCommit(blobItems, deadline); });
      }
      throw err;
    });
}
```

### Pending build-indikator – arkitektur og implementering

**Formål:** Vise brukeren at commits er i bygg-køen mens de navigerer rundt i nettstedet, og gi en live nedtelling som er koblet til faktiske GitHub Actions-kjøringer.

#### localStorage-state

Nøkkel: `samtu-build-pending`. Format:
```json
{
  "count": 2,
  "firstSaveAt": 1741900000000,
  "lastSaveAt": 1741900060000,
  "seenCompleted": 0,
  "actor": "erikhag1"
}
```

| Felt | Beskrivelse |
|------|-------------|
| `count` | Antall ventende bygg (egne) |
| `firstSaveAt` | Tidsstempel for første save i denne økt-serien – brukes som startpunkt for GitHub API-spørring |
| `lastSaveAt` | Tidsstempel for siste save |
| `seenCompleted` | Antall ferdige bygg allerede prosessert på tvers av sidelastinger |
| `actor` | GitHub-brukernavn (fra `localStorage.getItem('samt-bu-gh-user')`) |

#### Funksjoner (`custom-footer.html`)

| Funksjon | Rolle |
|----------|-------|
| `samtuIncrementPending()` | Øker count, setter `firstSaveAt` (behold eksisterende), oppdaterer `lastSaveAt` og `actor` |
| `samtuDecrementPending()` | Decrementerer count, øker `seenCompleted`, kaller `samtuClearPending()` om count = 0 |
| `samtuClearPending()` | Fjerner localStorage-nøkkel |
| `samtuShowPendingIndicator(count)` | Viser spinner + «N endringer bygges…» i `#qe-job-indicator` |
| `samtuShowPendingIndicatorWithTotal(count, totalActive)` | Som over, men legger til «(M totalt)» i parentes hvis andre brukeres bygg pågår |
| `samtuShowDoneIndicator()` | (beholdes for edge cases) Viser klikk-for-reload-lenke |

#### Flyt ved lagring

1. `onSaveSuccess()` kalles etter vellykket commit
2. `samtuIncrementPending()` – lagrer state med actor
3. `pollQeBuild(startTime, qeOldEtag)` starter ETag-polling (1 sek intervall) for aktiv dialog
4. Bruker kan navigere bort – spinneren vises via resume-koden på neste side

#### Resume-kode (kjøres ved sidelasting via `setTimeout(200ms)`)

1. Leser `samtuGetPending()`
2. Sjekker at `firstSaveAt` finnes og er < 10 min gammel
3. Viser spinner med gjeldende count
4. Starter `setInterval(checkCompletions, 3000)`

`checkCompletions()` gjør:
1. `GET /repos/SAMT-X/samt-bu-docs/actions/workflows/hugo.yml/runs?per_page=20` med `cache: 'no-store'`
2. Filtrerer på `run.created_at >= firstSaveAt - 30000`
3. Teller `myCompleted` (runs der `triggering_actor.login === p.actor` og `status=completed/success`)
4. Teller `totalActive` (alle runs med `status=queued/in_progress` i vinduet)
5. Kaller `samtuShowPendingIndicatorWithTotal(count, totalActive)` for live UI-oppdatering
6. Hvis `myCompleted > seenCompleted`: `samtuDecrementPending()` → reload side

#### `pollQeBuild.onBuildDone()` – ETag-deteksjon

Brukes når dialogen er åpen. Kaller `samtuDecrementPending()` istedenfor `samtuClearPending()`. Navigerer via `doNav()` (reload nåværende side).

#### Bakgrunnspolling (andre brukeres endringer)

Kjøres i eget `<script>`-blokk. Oppdaget ETag-endring mens `qe-job-indicator` er skjult:
- Hvis `p.count > 0` (egne bygg ventende): `samtuDecrementPending()` + auto-reload
- Ellers: vis «Andre endringer publisert»-banner

Bakgrunnspolling er **suspendert** mens `#qe-job-indicator` vises (for å unngå dobbelt-firing).

#### Actor-basert filtrering (skalerbarhet)

GitHub API returnerer `triggering_actor.login` for hvert workflow-run. Filtrering på dette sikrer at kun den innloggede brukerens egne bygg decrementerer telleren. Andre brukeres bygg telles i `totalActive` og vises i parentes.

**Forutsetning:** Alle commit/push-operasjoner krever gyldig GitHub-token (OAuth) – anonym commit er umulig via GitHub API. `actor`-feltet er alltid tilgjengelig når `samtuIncrementPending()` kalles.

**Design for skalering:** Løsningen er designet for store samarbeidsprosjekter med mange samtidige brukere (norske og internasjonale). Hver bruker ser sin egen teller; totaltelleren gir kontekst om global aktivitet.

#### Potensielle feilscenarioer

| Scenario | Håndtering |
|----------|-----------|
| Bruker er ikke innlogget | `actor` er tom streng → `isMine`-sjekk fallback til `!p.actor` (teller alt) |
| GitHub API rate limit | `checkCompletions()` feiler stille i `.catch()` – spinner forblir, ingen krasj |
| Build feilet (`conclusion != 'success'`) | Telles ikke som `myCompleted` → counter decrementeres ikke → bruker må manuelt rydde |
| > 10 min uten bygg | `firstSaveAt`-sjekken rydder state automatisk |

---

## Automatisert testing – verktøy og pipeline

### Installert og klar (2026-03-14)

| Verktøy | Versjon | Plassering |
|---------|---------|------------|
| Python | 3.12.10 | `C:\Users\Win11_local\AppData\Local\Programs\Python\Python312\python.exe` |
| Playwright | 1.58.0 | Installert via pip |
| Chromium | 145 (playwright) | `C:\Users\Win11_local\AppData\Local\ms-playwright\chromium-1208` |
| python-dotenv | 1.2.2 | Installert via pip |

**Kjørekommando (fra `tools/playwright/`):**
```powershell
C:\Users\Win11_local\AppData\Local\Programs\Python\Python312\python.exe test_pending_indicator.py
```

### E2E-test A: Pending-indikator (`test_pending_indicator.py`)

**Fil:** `samt-bu-docs/tools/playwright/test_pending_indicator.py`
**Konfigurasjon:** `tools/playwright/.env` (i .gitignore – aldri commit)

```ini
GITHUB_TOKEN=<hent fra localStorage 'samt-bu-gh-token' i nettleseren>
GITHUB_USER=erikhag1
SAMTU_BASE_URL=https://samt-bu-docs.pages.dev
TEST_PAGE=/om/om-samt-bu/
HEADLESS=false
SLOW_MO=400
```

**Slik henter du token:** Åpne `samt-bu-docs.pages.dev` i nettleseren → F12 → Application → Local Storage → `samt-bu-gh-token`.

**Hva testes (9 steg):**
1. Last nettstedet
2. Injiser token i localStorage (ingen OAuth-popup)
3. Åpne Endre-meny (`#edit-toggle` → `#edit-menu`)
4. Åpne redigeringsdialog (`#qe-overlay`)
5. Gjør endring (zero-width space – usynlig for lesere)
6. Lagre og observer pending-indikator (`#qe-job-indicator`)
7. Naviger til annen side – verifiser at indikator gjenopprettes
8. Poll hvert 15 sek og observer nedtelling per ferdig bygg
9. Verifiser at indikator forsvinner og localStorage er ryddet

**Output:** Screenshots i `tools/playwright/screenshots/<tidsstempel>/` med rød highlight-ramme rundt relevante elementer.

**Neste steg for testen:**
- Kjør og se at alle 9 steg fungerer
- Juster selektorer om noe feiler (skriptet printer tydelig hvilket steg)
- Legg til test for count=2 (to raske saves)

### Planlagte testtyper (ikke implementert ennå)

**B) Smoke-test** – rask verifisering av at nettstedet laster, meny vises, dialog åpner seg.

**C) GitHub API-enhetstest (Python Requests)** – tester `triggering_actor`-filtrering og pending-logikk direkte mot GitHub API uten nettleser.

### Demo-video pipeline (planlagt)

Målet er å produsere dokumentasjonsvideoer og brukerveiledninger automatisk.

**Steg 1 – Skjermopptak:** Playwright recorder (`record_video_dir`) produserer `.webm` av hele testforløpet.

**Steg 2 – Lyd:** ElevenLabs (gratis tier: 10 000 tegn/mnd ≈ 10–15 min tale). Stemmekloning fra ~1 min opptak av din stemme. Output: MP3/WAV.

**Steg 3 – Komposisjon:** FFmpeg legger lyden over skjermvideoen:
```bash
ffmpeg -i screen.webm -i narration.mp3 -c:v copy -c:a aac -shortest demo_final.mp4
```

**Steg 4 (fremtidig) – Talking head overlay:** D-ID eller HeyGen animerer et bilde til å snakke (lipsync mot ElevenLabs-lyden) og FFmpeg legger det inn som picture-in-picture.

**Rekkefølge:** Playwright → ElevenLabs lyd → FFmpeg → (D-ID avatar). Steg 1–3 er klar til implementering etter at E2E-testen fungerer.

---

## Endringslogg – 2026-03-14 (sesjon 2)

### ✅ TipTap selvhostet bundle – esm.sh eliminert

**Problem:** «Kunne ikke laste editoren» dukket opp igjen. Konsoll-feil: `SyntaxError: Unexpected token '}'`. Alle 9 esm.sh-importer feilet, inkludert `tiptap-markdown@0.8.10` som hadde fungert dagen før.

**Rotårsak:** esm.sh endret internt hvordan modul-filer genereres. Nye filer inneholder relative sub-importer med `^` i URL-path, f.eks.:
```
import "/@tiptap/pm@^2.7.0/commands?target=es2022"
import "prosemirror-state@^1.4.3?target=es2022"
```
Nettleseren URL-encoder `^` til `%5E` når den følger disse importene. esm.sh router ikke `%5E` riktig → returnerer JSON-feilmelding → nettleseren forsøker å parse JSON som JS → `SyntaxError: Unexpected token '}'` (siste tegn i `{"error":"..."}`).

**Viktig:** Dette rammer ALLE TipTap-versjoner (2.26.0 og 2.27.2 verifisert), fordi alle avhenger av ProseMirror med `^`-ranges. Det er en esm.sh platform-bug, ikke et TipTap-versjonsproblem.

**Fix: selvhostet prebygd bundle**

Byggesett opprettet i `samt-bu-docs/tools/tiptap-build/`:

| Fil | Innhold |
|-----|---------|
| `package.json` | TipTap 2.26.0 + tiptap-markdown 0.8.10 + esbuild |
| `entry.js` | Eksporterer Editor, StarterKit, Table*, Link, Image, Markdown |
| `.gitignore` | Ekskluderer `node_modules/` |

Bundle bygges med:
```bash
cd tools/tiptap-build
npm install
node_modules/.bin/esbuild entry.js --bundle --format=esm --minify --outfile=../../static/js/tiptap-bundle.js
```

Output: `static/js/tiptap-bundle.js` (524 KB minifisert, committet til repo, serveres av Cloudflare Pages CDN).

`loadTiptap()` i `custom-footer.html` endret fra 9 parallelle esm.sh-importer til én lokal import:
```javascript
import('/js/tiptap-bundle.js').then(function(mod) {
  window._Tiptap = {
    Editor: mod.Editor, StarterKit: mod.StarterKit,
    Table: mod.Table, TableRow: mod.TableRow, ...
  };
  ...
})
```

**Fordeler:**
- Ingen ekstern CDN-avhengighet
- Raskere lasting (én request, Cloudflare CDN-cached, same-origin)
- Ingen versjonsdrift – bundle oppdateres kun ved eksplisitt byggsteg
- Eliminerer hele klassen av esm.sh-problemer permanent

**Oppdatere TipTap i fremtiden:**
1. Endre versjoner i `tools/tiptap-build/package.json`
2. `npm install` i den mappen
3. Kjør esbuild-kommandoen over
4. Commit `static/js/tiptap-bundle.js` + `package.json` + `package-lock.json`
5. Push → Cloudflare Pages deployer automatisk

**Versjoner i bundle:** `@tiptap/*@2.26.0`, `tiptap-markdown@0.8.10`

---

### ✅ Playwright E2E-test – første kjøring

Første vellykkede kjøring av `tools/playwright/test_pending_indicator.py`:
- Alle 9 steg fullførte
- TipTap-timeout økt fra 8000ms til 25000ms (CDN-lasting tar lengre tid)
- `.env` konfigurert med `GITHUB_TOKEN` (gho_*), `GITHUB_USER=erikhag1git`

Test-konfigurasjon oppdatert for neste kjøring:
- `TEST_PAGE=/test-samt-bu-docs/test-1/` (dedikert testside)
- Steg 5 endret: endrer tittelfeltet (`#qe-field-title`) med tidsstempel-suffix i stedet for usynlig zero-width space
- Steg 3: screenshot med gul highlight på «Rediger dette kapitlet» i menyen
- Steg 4: venter på `#qe-field-title` populert i stedet for fast `wait_for_timeout`

---

### ✅ Endringslogg 2026-03-14 – Playwright-opprydding og HTML-videoviewer

#### Bakgrunn
Lang sesjon med iterativ utvikling av Playwright-demo og -testskript. Sesjonen krasjet i VS Code; ny sesjon startet i terminal. Alt var committet ved krasj.

#### Endringer i `tools/playwright/test_pending_indicator.py`

**Fjernet FFmpeg-avhengighet:**
- `find_ffmpeg()`, `convert_to_mp4()` og `import subprocess` slettet
- `VIDEO_PAD_TOP = 100` og `VIDEO_PAD_BOT = 200` fjernet – padding var kun for Windows Media Player
- Videofilen er nå ren 1920×1080 WebM uten svarte soner

**Viewport-fix:**
- `--start-maximized` fjernet fra Chromium-args
- På 1920×1200-skjerm utvidet `--start-maximized` viewporten ut over 1080px etter auto-reload → `record_video_size=1920×1080` klippet innhold. Uten flagget holder Playwright viewporten stabilt på 1920×1080 gjennom hele opptaket.

**WebM-håndtering:**
- `.webm` flyttes fra `SCREENSHOTS/video/<hash>.webm` → `SCREENSHOTS/demo.webm` etter recording
- `video/`-mappen slettes etter flytting

**Steg 8 – krasj-fix:**
- `inject_indicator_pulse()` og tilhørende `page.evaluate()`-kall pakket i `try/except`
- Årsak: siden auto-reloader (triggered av JS når `count=0`) midt i polling-løkken → «Execution context was destroyed» exception
- Fix: `continue` til neste 15-sekunders intervall etter navigation-feil

**Forklaringsboble deaktivert:**
- `show_bubble()`-kallet i steg 7 kommentert ut – boblen var for lavt plassert (`bottom: 70px`) og falt delvis utenfor viewport i noen scenarier
- Skal aktiveres igjen på kontrollert måte med korrekt posisjonering

#### Ny `tools/playwright/viewer.html`

Egenutviklet HTML-videospiller for å vise demo uten spilleroverlay-problemer:
- `<video>`-element uten native browser-kontroller
- Kontrollpanel (play/pause, seek, ±10s, tid, fullskjerm) plassert **under** videoen – aldri overlaid
- Lastes automatisk som `demo.webm` fra samme mappe (drag-and-drop/fil-velger som fallback)
- Kopieres automatisk inn i screenshot-mappen etter hver kjøring
- Tastatur: mellomrom = pause/play, piltaster = ±5s

**Fordeler vs. Windows Media Player:**
- Ingen overlay-kontroller som dekker innholdet ved pause
- Fungerer for alle brukere med moderne nettleser
- Mye mindre filstørrelse (WebM vs. H.264 MP4)

#### `.gitignore`-oppdatering

Lagt til:
```
tools/playwright/screenshots/**/*.webm
tools/playwright/screenshots/**/*.mp4
```
13 tidligere trackede videofiler fjernet fra git-indeksen. Fremtidige videofiler genereres lokalt ved kjøring av skriptet.

#### Nåværende tilstand

Ren baseline for videre demo- og testutvikling:
- Kun `screenshots/20260314_210250/` i git (11 PNG-screenshots + viewer.html)
- Videofil (`demo.webm`) genereres lokalt og ignoreres av git
- Skriptet kjøres med: `python test_pending_indicator.py` fra `tools/playwright/`

#### Neste steg for Playwright-demo

1. Legg til forklaringstekster (bobler) på kontrollert måte – posisjon og timing defineres eksplisitt
2. Tale/voiceover – vurderes når visuell demo er ferdigstilt
3. Vurder om skriptet skal splittes i «test» (automatisert verifisering) og «demo» (visuell presentasjon)

---

## Endringslogg – 2026-03-15

### ✅ Playwright E2E-test B: To ventende byggejobber (`test_two_pending_jobs.py`)

**Fil:** `samt-bu-docs/tools/playwright/test_two_pending_jobs.py`

**Scenariet (9 steg):**

| Steg | Handling | Forventet tilstand |
|------|----------|--------------------|
| 1 | Last nettsted + injiser credentials | — |
| 2 | Rediger og lagre **Test 1** | count=1 synlig |
| 3 | Naviger til **Test 2** (`page.goto`) | count=1 gjenopprettes |
| 4 | Rediger og lagre **Test 2** | count=2 ← kjernen |
| 5 | Naviger tilbake til **Test 1** (`page.goto`) | count=2 gjenopprettes |
| 6 | Vent på første bygg | count: 2→1 |
| 7 | Vent på andre bygg | count: 1→0 |
| 8 | Verifiser titler i sidebaren | Begge oppdatert |
| 9 | Slutt-tilstand | Ingen pending state |

**Ny env-var:** `TEST_PAGE_2` (default `/test-samt-bu-docs/test-2/`) – ingen endring i eksisterende `.env` nødvendig.

**`do_edit_and_save(page, step_prefix, page_label)`:** Ny hjelpefunksjon – wrapper for åpne meny → åpne dialog → endre tittel → lagre. Brukes for begge testsider uten kodeduplisering.

**Viktig lærdom – sidebar-navigering i Playwright:** Bruk alltid `page.goto(URL)` for å navigere mellom testpagene. Sidebar-lenkesøk (`#sidebar a` filter tekst) feiler fordi seksjonen kan kollapse etter auto-reload triggered av pending-state resume-koden. Første kjøring krasjet i steg 3 av denne årsaken.

**Resultat av første vellykkede kjøring (2026-03-15):**
count=1 etter Test 1 ✅ · count=2 etter Test 2 ✅ · 2→1 etter ~60s ✅ · 1→0 etter ~105s ✅ · PASS slutt-tilstand ✅

### ✅ viewer.html – klikk på video toggler play/pause

`cursor: pointer` på `<video>` + `v.addEventListener('click', togglePlay)` + oppdatert hint-tekst. Tre linjer totalt.

---

## Endringslogg – 2026-03-14 (sesjon 3 – memory og automatisering)

### Memory-system etablert og dokumentert

**Bakgrunn:** MEMORY.md hadde vokst til 224 linjer (grense: 200). Sesjonen ryddet opp og etablerte et robust, trelags memory-system.

#### Ny filstruktur under `C:\Users\Win11_local\.claude\projects\...\memory\`

| Fil | Innhold |
|-----|---------|
| `MEMORY.md` | Kompakt indeks – 135 linjer, god buffer. Inneholder 6 kritiske enkeltlinjer som alltid leses. |
| `critical-notes.md` | Alt fra «Kritiske aldri glem» + «Sidebar-mønstre» – tematisk organisert i 6 seksjoner |
| `session-start-prompts.md` | To varianter av oppstartsprompt (A: kort / B: eksplisitt) |
| `cms-routing.md` | Uendret – rutinglogikk for edit-switcher |

**Trelags sikkerhetsmodell:**
1. 6 kritiske enkeltlinjer i MEMORY.md (auto-lastet, alltid synlig)
2. `critical-notes.md` i sesjonsstart-lista (eksplisitt ved oppstart)
3. Full detalj i `claude-kontekst/` (ved behov)

### `erikhag1git/claude-memory` – privat GitHub-repo

Opprettet `https://github.com/erikhag1git/claude-memory` (privat) for versjonskontroll av memory-filene.

**Begrunnelse for valg:** Memory-filene er personlige (maskinstier, instruksjoner til Claude) og tilhører `erikhag1git`, ikke `SAMT-X`-org-en. Prosjektkunnskap (claude-kontekst, veikart) forblir i `solution-samt-bu-docs`.

**Lokal plassering:** `S:\app-data\github\erikhag1git-repos\claude-memory\`

```
claude-memory/
├── README.md          ← full dokumentasjon av systemet
└── samt-bu-docs/      ← kopi av de 4 memory-filene
```

### Automatisk synkronisering – to lag

**A – Claude Code PostToolUse-hook:**
- Konfigurert i `C:\Users\Win11_local\.claude\settings.json`
- Matcher `Write|Edit` → leser `tool_input.file_path` fra stdin JSON
- Kjører `sync-memory.ps1` – sjekker om endret fil er i memory-mappen, kopierer + committer + pusher kun hvis ja
- Avslutter stille uten å gjøre noe for alle andre filer

**B – Windows Task Scheduler:**
- Oppgavenavn: «Claude Memory Sync - samt-bu-docs»
- Kjøres hvert 30. minutt, uavhengig av Claude Code
- Plukker opp manuelle endringer og edge cases

**Sync-script:** `C:\Users\Win11_local\.claude\hooks\sync-memory.ps1`
Krever `-ExecutionPolicy Bypass` pga. Windows standard policy.

### Veikart-oppføringer som bør oppdateres

To veikart-oppføringer i `solution-samt-bu-docs` er utdaterte og bør revideres:
- `ny-side-samme-nivaa/` – beskriver GitHub-lenke-tilnærming som ble erstattet av den implementerte dialogen
- `ny-cms-portal/` – refererer til Decap CMS (fjernet 2026-03-11)

### Ryddet opp

## Endringslogg – 2026-03-15 (sesjon 4)

### Fullført i denne sesjonen

**«Sist endret av»-visning på alle sider:**
- `header.html` (tema): Nytt Hugo-template som henter `last_editor` fra frontmatter, med fallback til `.GitInfo.AuthorName`. Vises som «av <navn>» inline i lastmod-span med `color:#aaa; font-size:0.85em`.
- `inject-lastmod.py` (CI-skript): Utvidet med `get_author()` funksjon (git log `%aN`) og `last_editor:` injeksjon i modulinnhold-frontmatter.
- Disse to endringene dekker alle sider: lokale sider via GitInfo, modulinnhold via CI-injeksjon.

**Playwright test B (to ventende jobber):**
- Ny testfil: `tools/playwright/test_two_pending_jobs.py`
- Demonstrerer 2 redigeringer i kø (count 1→2), deretter begge bygg fullfører (2→1→0)
- `do_edit_and_save()` hjelpefunksjon – gjenbrukbar på tvers av sider
- Navigasjon via `page.goto()` (ikke sidebar-klikk) – sidebar kollapser etter auto-reload

**Vekt-refaktorering (10-inkrement):**
- Python-skript `reweight_content.py` kjørt: 155 filer endret på tvers av 5 repoer
- Manuell korreksjon av singleton-grupper: `samt-bu-drafts` root→90, `team-semantics` root→20
- `custom-footer.html`: vekt-inkrement endret fra +1 til +10 i `fetchSiblingWeightUpdates`
- Alle commits pushet: samt-bu-docs (118 filer), team-architecture (1 fil), team-semantics (2 filer), solution-samt-bu-docs (34 filer)

**viewer.html (Playwright HTML-viewer):**
- Klikk på videoelement toggler spill/pause (`cursor: pointer` + click-handler)
- Hint-tekst oppdatert

### Viktig lærdom: Vekt-singleton-fallgruve

Modulrepo-rot `_index.nb.md`-filer er singletons i sin egen repo, men vektene styrer rekkefølgen i modernettsstedet. Reweight-skript som behandler singletons som «gruppe» og tildeler dem vekt 10, bryter navigasjonsrekkefølgen. **Løsning:** Ikke kjør automatisk reweight på modulrot-filer – sett dem manuelt.


- 4 untrackede screenshot-mapper slettet (`20260314_184838/`, `_191326/`, `_193537/`, `_210104/`)

## Endringslogg – 2026-03-15 (sesjon 5)

### Fullført i denne sesjonen

**Seksjonssider – preamble og seksjonsinnhold-label:**
- `list.html` (tema): Sider med barn renderes nå slik: eventuell body-tekst pakkes i `<div class="section-preamble">` (bold), deretter `<div class="section-children-label">` med «Seksjonsinnhold:» / «Section contents:», deretter barnelenkelisten. Sider uten barn renderes uendret.
- `custom-head.html`: CSS for `.section-preamble { font-weight: bold }` og `.section-children-label` (liten bold uppercase, color #555).
- `i18n/nb.toml` + `en.toml`: nøkkel `sectionChildrenLabel`.
- **Merk:** «Seksjonsinnhold:»-labelen bruker `<div>`, ikke `<h*>` → dukker ikke opp i Hugo's TOC eller scroll-spy.

**page-meta – uniform font og bunn-justering:**
- `.page-meta` i `custom-head.html`: `color: #666 → #aaa`, `align-items: flex-end` lagt til.
- `header.html`: fjernet inline `color`/`font-size`-stiler fra `page-meta-id` og den nestede «av»-span i `page-meta-lastmod`. Alle felter arver nå uniform stil (13px, #aaa) fra containeren.
- Resultat: «Sist endret: dato», «av bruker», «ID: guid» og «Status» vises med lik skriftstørrelse, lik farge og er bunn-justert.

**TOC – ingen endringer nødvendig:**
- Ingen sider har `hide_toc: true` i dag – allerede i ønsket tilstand.

**Claude Code-plugins installert (brukernivå, persistent):**
- `frontend-design@claude-plugins-official` – produksjonsklar CSS/HTML-generering
- `github@claude-plugins-official` – GitHub MCP-server (issues, PRs, CI)
- `playwright@claude-plugins-official` – E2E-teststøtte
- `commit-commands@claude-plugins-official` – `/commit`, `/commit-push-pr`, `clean_gone`

### Nyttig lærdom: `<div>` vs `<h*>` i Hugo-templates

Heading-elementer (`<h2>`, `<h3>` osv.) lagt til i Hugo-templates vil ikke dukke opp i `{{ .TableOfContents }}` (som bygges fra markdown-kilde, ikke template-HTML), men kan plukkes opp av scroll-spy JS som skanner DOM. Bruk `<div>` med styling for visuell heading uten TOC-oppføring.

---

## Endringslogg – 2026-03-16

### ✅ Frontmatter-panelredesign – stablet layout

**Filer:** `themes/hugo-theme-samt-bu/layouts/partials/edit-switcher.html`

**Problem:** Alle felt (Tittel, Menytittel, Vekt, Status, Innholdsfortegnelse) lå i én rad med cramped layout. STATUS lå for lavt.

**Fix:** Hvert felt pakket i `<div style="display:flex; flex-direction:column; gap:.2rem;">` med label over felt. Container: `align-items:flex-start; gap:1.4rem; padding:.55rem 1.5rem`. STATUS sank til bunn fordi `align-items` manglet `flex-start` – kortere divs sank til bunn av flex-container.

**Avkrysningsboks-justering:** Usynlig spacer `<span style="color:transparent; user-select:none; pointer-events:none;">–</span>` over checkboxen kompenserer for manglende label-høyde.

### ✅ Select-tekstsentrering

**Problem:** Native `<select>` med `height:2rem` plasserte teksten nederst i Chrome (ikke midtstilt). Selve boksen var også høyere enn inputs pga. default padding.

**Løsning:** CSS-override:
```css
#qe-meta-panel select, #np-form select {
  height: 2rem;
  line-height: 2rem;
  padding-top: 0;
  padding-bottom: 0;
}
```
`line-height = height` med null vertikal padding er Chrome-idiom for sentrert tekst i `<select>`. Ingen `height:auto` – det gjeninnfører default browser-padding.

### ✅ «Innholdsfortegnelse» – positiv logikk

**Problem:** Feltet het «Skjul innholdsfortegnelse» (negativ logikk, ukrysset som default) – forvirrende for redaktører.

**Fix (tre steder):**
1. `edit-switcher.html`: Etikett endret til «Innholdsfortegnelse», `checked`-attributt lagt til
2. `custom-footer.html` lese-side: `parseFmField(qeFrontmatter, 'hide_toc') !== 'true'` (invertert)
3. `custom-footer.html` skrive-side: `if (!checked) setFmField(hide_toc: true)` / `else removeFmField(hide_toc)`

Semantikk: «avkrysset = vis TOC» (positiv). `hide_toc: true` skrives kun til frontmatter når boksen er ukrysset.

### ✅ Lydsignaler for GUI-brukere (nettleseren)

**Filer:** `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html`

**Problem:** Browser autoplay policy blokkerer `AudioContext` og `speechSynthesis` fra `setInterval`-callbacks. Lyd må initialiseres under brukergestur.

**Løsning:**
```javascript
var _samtuAudioCtx = null;

function samtuUnlockAudio() {
  // Oppretter/gjenopptar AudioContext + sender stille SpeechSynthesisUtterance
  // Kalles på lagreknapp-klikk og np-form submit (brukergestur)
}

function samtuPlaySuccess() {
  // Web Audio API: 880 Hz oscillator med exponential gain falloff (0.4s)
  // Web Speech API: SpeechSynthesisUtterance('Build job complete', 'en-US')
}
```

`samtuUnlockAudio()` kalles i:
- `#qe-save-btn` click handler
- `#np-form` submit handler

`samtuPlaySuccess()` kalles i:
- `startGhPoll` → `if (run.conclusion === 'success')`
- `startUrlPoll` → `if (r.ok)`

### ✅ Default statusverdi blank ved ny side

**Problem:** Ny side hadde «Ny» som default status, både i HTML og JS.

**HTML-fix:** `<option value="" selected>–</option>` plassert øverst i `<select id="np-status">`.

**JS-fix (to steder):** `document.getElementById('np-status').value = ''` (var `'Ny'` begge steder – ble satt etter `form.reset()`).

### ✅ Trelydssystem for Claude Code CLI

**Dokumentert i:** `C:\Users\Win11_local\.claude\projects\...\memory\feedback_use_skills_proactively.md`

PowerShell `[Console]::Beep()` + `System.Speech.Synthesis.SpeechSynthesizer` pakket rundt `gh run watch --exit-status`. Tre lyder:
- **Start:** 600Hz+900Hz pip + «Build job started»
- **Suksess:** C-E-G-C stigende fanfare + «Build job complete»
- **Feil:** 400Hz→300Hz→220Hz fallende wah-wah + «Build job failed»

### ✅ Memory-fil: feedback_use_skills_proactively.md

Ny fil i `C:\Users\Win11_local\.claude\projects\...\memory\`. Inneholder:
1. Regel om å alltid vurdere skills proaktivt (frontend-design for CSS/HTML, simplify, commit)
2. CI-lyd-kommandoen (bash + PowerShell) med de tre lydsignalene

**Why:** Brukeren måtte eksplisitt be om `frontend-design`-skill ved et CSS-layoutproblem – noe den er spesiallaget for.

---

## Endringslogg – 2026-03-16 (sesjon 2)

### ✅ GUI-lydsignaler – fullstendig implementert og testet

**Filer:** `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html`

#### Arkitektur

Tre lydfunksjoner i global `<script>`-blokk (over poll-funksjonene):

| Funksjon | Lyd | Tale | Kalt fra |
|----------|-----|------|----------|
| `samtuPlayStart()` | 600+900 Hz opptakt | «Build job started» | `startGhPoll`, `startUrlPoll`, ETag-polling |
| `samtuPlaySuccess()` | C5–E5–G5–C6 fanfare | «Build job complete» | Inline i ETag-deteksjon, `startGhPoll`, `startUrlPoll` |
| `samtuPlayFailure()` | 400→300→220 Hz wah-wah | «Build job failed» | ETag-timeout, `startGhPoll` feil, `startUrlPoll` timeout |

Felles hjelpefunksjoner:
- `_samtuPlayNotes(notes)` – Web Audio API, ADSR-envelope (attack 20ms, sustain, release 30–80ms), returnerer total ms-varighet
- `_samtuSpeak(text, delayMs)` – `SpeechSynthesisUtterance` med forsinkelse slik at tale alltid kommer **etter** lydsignalet

#### Tre rotnårsaker som ble funnet og fikset

**1. ETag-polling-stien manglet lyder helt:**
`pollQeBuild` bruker ETag-basert `setInterval` som primærvei (ikke `startGhPoll`). `startGhPoll` er kun fallback uten ETag. Lyder måtte legges til direkte i ETag-stien.

**2. `doNav()` ble kalt synkront → AudioContext stoppet:**
`samtuPlaySuccess()` kaller `_samtuAudioCtx.resume().then(...)` – en microtask. Umiddelbart etter ble `doNav()` kalt synkront → `window.location.href` trigget navigasjon → AudioContext destruert før microtask-køen rakk å starte notene.

Fix:
- Dialog **lukket**: `setTimeout(doNav, 1600)` – gir fanfaren (1.35s) tid til å spille
- Dialog **åpen**: nedtelling økt fra 2s til 3s – dekker fanfare + tale

**3. Enkeltnoter hørtes som «blipp»:**
Opprinnelig envelope: `setValueAtTime(0.28) → exponentialRamp(0.001)` med 0.12s varighet → brå decay, ingen sustain.

Fix: ADSR-envelope med `linearRamp` attack + `setValueAtTime` sustain + `exponentialRamp` release. Notevarigheter økt: 0.22s × 3 + 0.60s for fanfare.

**4. Tale avbrøt lydsignalet (parallell avspilling):**
Tale ble startet parallelt med lydsignal via `speechSynthesis.speak()`. Fix: `_samtuSpeak(text, delayMs)` med `setTimeout` basert på returnert ms-varighet + 150ms buffer.

#### Lydparametre (endelige)

| Lyd | Toner (Hz) | Tidsoffsets (s) | Varighet per note (s) | Tale starter etter |
|-----|-----------|----------------|----------------------|-------------------|
| Start | 600, 900 | 0, 0.15 | 0.12, 0.20 | ~500ms |
| Suksess | 523, 659, 784, 1047 | 0, 0.25, 0.50, 0.75 | 0.22, 0.22, 0.22, 0.60 | ~1500ms |
| Feil | 400, 300, 220 | 0, 0.28, 0.56 | 0.25, 0.25, 0.55 | ~1260ms |

#### `samtuUnlockAudio()` – forutsetning

Kalles under brukergestus (lagre-klikk / form submit) for å opprette og aktivere `AudioContext` og låse opp `speechSynthesis`. Uten dette vil alle lydfunksjoner feile stille (autoplay policy). Kalles i `#qe-save-btn` click-handler og `#np-form` submit-handler.

---

## Endringslogg – 2026-03-17 (sesjon 5)

### ✅ «Hvordan bidra»-siden oppdatert

`content/om/hvordan-bidra/_index.nb.md` og `_index.en.md` er omskrevet med presis veiledning for innebygd TipTap-editor – erstatter utdatert Decap CMS-instruksjon. Nytt:
- Seksjon «Anbefalt: Innebygd redigering» erstatter «Alternativ 1 – CMS»
- Ny seksjon «Hva du trenger» (GitHub-konto + skrivetilgang)
- Ny seksjon «Opprette en ny side» med korrekte menynavn («Nytt kapittel etter dette», «Nytt underkapittel»)
- Tip om bildepaste (Ctrl+V) – ingen dedikert bildeknapp finnes ennå
- Merknad om pågående arbeid med oversikt over andres redigeringer

### ✅ Jobbhistorikk-knapp – alltid synlig

`#qe-job-indicator` er nå alltid synlig (endret fra `display:none` til `display:flex` i `edit-switcher.html`).

**Idle-tilstand:** `fa-history`-ikon + «Byggehistorikk» / «Build history» med `opacity:.7`.

**Under bygg:** `samtuShowPendingIndicatorWithTotal()` skriver over med spinner + «N endringer bygges…» + setter `data-building="1"`.

**Ferdig:** `samtuShowDoneIndicator()` viser «Endringer publisert – klikk for å laste inn» + fjerner `data-building`.

**Bakgrunnspoll-fix:** Sjekker nå `qeInd.dataset.building` i stedet for `qeInd.style.display !== 'none'` for å avgjøre om egne bygg pågår. Forhindrer at alltid-synlig indikator blokkerer andres-endringer-banneret.

**Umiddelbar oppdatering:** `samtuIncrementPending()` kaller nå `samtuShowPendingIndicator(newCount)` etter å ha oppdatert localStorage. Indikatoren viser byggestatus i det brukeren klikker «Lagre», ikke først ved navigering.

### ✅ Minimering fjernet

Hele minimize-funksjonaliteten er slettet:
- HTML: `#qe-minimize-pill` og `⊟`-knappen i qe-header fjernet fra `edit-switcher.html`
- JS: `minimizeQeDialog()`, `qeMinimizeTimer`, `qeMinimizeSaveTime` slettet fra `custom-footer.html`
- Cancel-knapp i qe-dialog: heter «Lukk dette vinduet» / «Close this window» etter lagring (var «Minimer»), og lukker direkte via `closeQeDialog`
- `onBuildDone()`: pill-visible-grenen fjernet – kun to grener igjen (dialog åpen / dialog lukket)

**Begrunnelse:** Pillen forsvant ved navigering til en ny side og ga bare dobbel statusinformasjon.

### ✅ ETag-poll-timeout økt

`if (++attempts > 90)` → `if (++attempts > 180)` (1 sek intervall → maks 3 minutter).

**Rotårsak for falsk «Build job failed»:** Et bygg tok ~1m56s. Timeouten på 90 sek utløste `samtuPlayFailure()` mens bygget fortsatt kjørte og faktisk fullførte korrekt.

### Nøkkelpunkter for fremtidige sesjoner

- `data-building`-attributtet er den kanoniske måten å sjekke om qe-bygg pågår (ikke `display`)
- `samtuIncrementPending()` oppdaterer nå indikatoren umiddelbart – ingen treg respons
- Jobbhistorikk-dialog (`#job-history-dialog`) åpnes ved klikk på indikatoren, henter siste 15 bygg fra GitHub Actions API filtrert på `actor=<login>`

---

## Endringslogg – 2026-03-17 (sesjon 6)

### ✅ Jobbhistorikk: sekundtelling, køstatus og avløst-håndtering

**Bakgrunn:** Ved 3+ raske lagringer kansellerer GitHub Pages automatisk eldre jobber i kø («Canceling since a higher priority waiting request for pages exists»). Kansellerte jobber vistes som rød `!` og pending-teller hengte. GitHub Actions bruker dessuten statuser `waiting`/`pending`/`requested` i tillegg til `queued` – alle falt tidligere gjennom til rødt feil-ikon.

**Implementert i `custom-footer.html`:**

| Endring | Detalj |
|---------|--------|
| `statusIcon()` | `in_progress` → spinner, `queued`/`waiting`/`pending`/`requested` → grå klokke, `cancelled` → grå `fa-check-circle`, `failure` → rød `!` |
| Tidskolonne | `queued`/`waiting` → «I kø», `in_progress` → «X sek» (elapsed), `cancelled` → «Avløst», ferdig → `timeAgo` |
| `checkCompletions()` | Teller `myCancelled` separat. Trigger ferdig-sekvens når `myCompleted > 0 && totalActive === 0` – rydder hele pending-state, ingen heng |
| `startGhPoll()` | `conclusion === 'cancelled'` → kall `onStatus('Avløst – venter på nytt bygg…')`, ikke `onError` |
| Live elapsed | `loadHistory` splittet i `fetchHistory()` + `renderHistory(runs)`. Re-render hvert sek fra cache, re-fetch hvert 15. sek mens dialog er åpen |
| `openHistory()` / `closeHistory()` | Rydder alle timere ved lukking (✕-knapp, klikk utenfor, ESC) |

**Brukerveiledning oppdatert** (`content/om/hvordan-bidra/_index.nb.md`):
- Ny seksjon «Statusindikator og jobbhistorikk» med tabell over indikator-tilstander
- Forklaring av GitHub-køoppførsel og avløste jobber for ikke-tekniske redaktører

**Veikart oppdatert** (`veikart/statusrapportering-gui/`): Steg 3 lagt til og markert fullført.

### Lært: GitHub Actions-køstatuser

GitHub Actions returnerer disse statusene for workflow runs (ikke bare `queued` og `in_progress`):

| Status | Når |
|--------|-----|
| `queued` | Jobb er i kø, venter på runner |
| `waiting` | Jobb venter på concurrency-gruppen (Pages-miljøet) |
| `pending` | Jobb venter på manuell godkjenning eller ressurs |
| `requested` | Jobb er forespurt men ikke startet |
| `in_progress` | Jobb kjører |
| `completed` | Jobb er ferdig (se `conclusion` for utfall) |

**Conclusions:** `success`, `failure`, `cancelled`, `timed_out`, `skipped`, `action_required`

`cancelled` med meldingen «Canceling since a higher priority waiting request for pages exists» betyr at GitHub Pages-miljøet kansellerte en eldre jobb til fordel for nyere. Alle git-commits er bevart – den nyeste jobben deployer alle endringer.

---

## Endringslogg – 2026-03-17 (sesjon 7)

### «Mine»/«Alle»-faner i byggehistorikk-dialog

Undertabs i `#job-history-dialog` lar brukeren veksle mellom egne og alle bygg:

- **«Mine»** (standard): filtrerer på innlogget bruker via `&actor=<login>` i GitHub Actions API
- **«Alle»**: henter siste 15 bygg i repoet uten actor-filter, viser actor som sublinje per rad
- **Navnecache:** `GET /users/{login}` hentes én gang per unik login per sidebesøk, caches i JS-dict. Viser `login (Full Name)` – krever at GitHub-profilen har Name-feltet satt (`data.name !== null`)
- **Tab-bytte:** nullstiller runs-cache og re-fetcher umiddelbart

**Filer endret:** `edit-switcher.html` (HTML for tabs), `custom-footer.html` (JS)

### GitHub-redigeringslenke – riktig repo for modulinnhold

`footer.html`s «Rediger denne siden i GitHub»-lenke hadde ikke fått oppdatert rutinglogikk etter at `edit-switcher.html` fikk fire grener. Lenken brukte alltid `samt-bu-docs`-repoet, selv for modulinnhold (team-architecture, samt-bu-drafts, solution-samt-bu-docs).

**Fix:** Lagt til tilsvarende `hasPrefix`-sjekker i `footer.html` (linje ~51) som i `edit-switcher.html`. Kritisk: **ved ny modul må begge filer oppdateres**.

---

## Endringslogg – 2026-03-17 (sesjon 9)

### Felles pending-indikator for ny side og sletting

**Problem:** `#np-job-indicator` og `#del-job-indicator` var egne statiske `position:fixed; bottom:0; left:0`-elementer som viste «Oppdateringsjobb pågår». De overlappet med `#qe-job-indicator`, brukte ikke `samtuIncrementPending()`, og statusen forsvant ved navigering (ikke i localStorage).

**Fix:**
- `np-dialog` etter vellykket commit: erstatter `showNpJobIndicator()` med `samtuIncrementPending()`
- `npPollBuild onDone/onError`: erstatter `hideNpJobIndicator()` + `samtuClearPending()` med `samtuDecrementPending()`
- `del-dialog` etter vellykket commit: erstatter `showJobIndicator()` med `samtuIncrementPending()`, legger til `samtuUnlockAudio()` i confirm-handler
- `pollBuild onDone`: erstatter `hideJobIndicator()` med `samtuDecrementPending()` + `samtuPlaySuccess()`
- bgTimer-vakt forenklet: sjekker kun `qeInd.dataset.building` (ikke lenger npInd/delInd)
- `#np-job-indicator` og `#del-job-indicator` fjernet fra `edit-switcher.html`

Alle tre flows (redigering, ny side, sletting) bruker nå konsekvent `samtuIncrementPending()` / `samtuDecrementPending()` → delt `#qe-job-indicator` viser «1 endring bygges…» / «N endringer bygges…» for alle operasjoner.

### «Not a fast forward» ved ny side/sletting

**Rotårsak:** `createFilesInOneCommit()` og `deleteFilesInOneCommit()` hentet `GET /git/ref/heads/main` uten `cache: 'no-store'`. GitHub cacher dette kallet i nettleseren i ~60 sekunder → foreldet SHA → «Update is not a fast forward» ved commit like etter en annen commit.

**Fix:** `cache: 'no-store'` lagt til på ref-fetchet i begge funksjoner (linje ~842 og ~1048 i `custom-footer.html`). `createQeCommit` hadde dette riktig fra sesjon 4.

**Lært mønster:** Alle `GET /git/ref/heads/main`-kall i `custom-footer.html` MÅ ha `cache: 'no-store'`. Retry-logikk løser ikke dette problemet siden selve ref-fetchet i retry-loopen også caches.

---

## Endringslogg – 2026-03-18 (sesjon 10)

### ✅ Byggehistorikk: «Oppdatert» → «Endre side»

Commit-meldingsformat i begge koderetninger endret for konsistens med «Ny side» og «Slett side»:

- `createQeCommit()` (~linje 1416): `(qeLang === 'en' ? 'Edit page: ' : 'Endre side: ') + qePageTitle`
- `renderHistory()`: `msg.replace(/^Oppdatert: /, 'Endre side: ').replace(/^Updated: /, 'Edit page: ')` – fikser også eldre historikkoppføringer i dialogen

**Filer endret:** `custom-footer.html`

---

### ✅ «Slett denne siden»: rekursiv sletting med advarsel

**Problem:** «Slett denne siden» slettet kun `_index.nb.md` + `_index.en.md`. Sider med undermapper ble ikke fullt slettet, og brukeren fikk ingen advarsel.

#### Ny `deleteDirectoryRecursive(token, repo, dirPath, commitMsg)`

Bruker GitHub Trees API for å slette hele mapper i én commit:
1. `GET /git/ref/heads/main` → head SHA
2. `GET /git/commits/{sha}` → tree SHA
3. `GET /git/trees/{treeSha}?recursive=1` → alle filer
4. Filtrer: `items.filter(i => i.type === 'blob' && i.path.startsWith(dirPath + '/'))`
5. `POST /git/trees` med `sha: null` per fil → ny tree SHA
6. `POST /git/commits` → ny commit SHA
7. `PATCH /git/refs/heads/main` → oppdater ref

Alle GitHub Trees API-kall har `cache: 'no-store'`.

#### To-stegs bekreftelsesdialog

`openDeleteDialog(repo, dirPath, lang, title, afterDeleteUrl, childCount)` – ny parameter `childCount`:

- **`childCount === 0`:** Enkel bekreftelse i `#del-confirm-section`. Rød knapp «Slett denne siden». `doCommit()` kaller `deleteFilesInOneCommit` (kun de to språkfilene).
- **`childCount > 0`:** Gul advarselsboks vises med antall underkapitler. Knapp: «Vis bekreftelse». Klikk → `showStep2()` → viser `#del-confirm-section-2` med rød boks:
  - Tittel: «Er du helt sikker?»
  - Tekst: «Du er i ferd med å slette «{tittel}» og alle {N} underkapitler. Dette kan ikke angres via nettstedet (men kan gjenopprettes fra GitHub-commit-historikken av en administrator). Det er ikke sjekket om andre sider lenker til noen av sidene som slettes — slike lenker kan bli brutte.»
  - Knapper: «Tilbake» (tilbake til steg 1) og «Ja, slett alt permanent» (kaller `doCommit()`)
  - `doCommit()` bruker `deleteDirectoryRecursive` for sider med barn

#### `showBuildPanel()` – bug-fix

Skjuler nå begge bekreftelseseksjoner:
```javascript
document.getElementById('del-confirm-section').style.display = 'none';
document.getElementById('del-confirm-section-2').style.display = 'none'; // Ny linje
document.getElementById('del-build-section').style.display = 'block';
```
Problemet: Etter steg-2-bekreftelse ble steg-2-innholdet hengende synlig under bygg-panelet.

#### HTML-teknikk: title via data-attributt

`{{ .Title | jsonify }}` og `{{ .Title | js }}` inne i `onclick="..."` HTML-attributt gir begge problemer:
- `jsonify` produserer `"tittel"` med omsluttende quotes → HTML-attributten terminerer for tidlig
- `js` produserer `{0xc000814300...}` (intern Go-peker) i dette konteksten

**Løsning:** `data-del-title="{{ .Title }}"` + `this.dataset.delTitle` i onclick.

#### Fontarv i dialogen (px ikke rem)

Alle `font-size`-verdier i `#del-dialog` endret fra `rem` til `px` fordi `1rem` arver fra HTML-rotelementet (~10px i dette temaet), ikke fra dialogens `font-size:16px`. Alle barn bruker `16px`/`17px` eksplisitt.

**Filer endret:** `edit-switcher.html`, `custom-footer.html`

---

### ✅ `last_editor` – konsistent visning `login (Navn)`

**Problem:** Ulike steder viste `last_editor` ulikt: «erikhag1git (ukjent navn)», «erikhag1git», «Erik Hagen» (bare git-navn). Byggehistorikk «Alle»-fane viste riktig «erikhag1git (Erik Hagen)» – dette er fasiten.

#### Fix 1 – skrivesiden (`custom-footer.html` linje ~1515)

```javascript
// Gammel (skrev «(ukjent navn)» ved manglende navn):
var editorValue = editorLogin ? editorLogin + ' (' + (editorName || 'ukjent navn') + ')' : null;

// Ny:
var editorValue = editorLogin
  ? (editorName ? editorLogin + ' (' + editorName + ')' : editorLogin)
  : null;
```
Skriver nå `erikhag1git (Erik Hagen)` om navn finnes, ellers bare `erikhag1git`.

#### Fix 2 – visningssiden (`header.html`)

**Steg A – strip gammel `(ukjent navn)` fra lagrede verdier:**
```hugo
{{ $editor = $editor | replaceRE ` \(ukjent navn\)` "" }}
```

**Steg B – supplement bare-login med GitInfo-navn:**
```hugo
{{ if and $editor (not (strings.Contains $editor "(")) }}
  {{ with .GitInfo }}
    {{ if not (strings.Contains .AuthorName "[bot]") }}
      {{ $editor = printf "%s (%s)" $editor .AuthorName }}
    {{ end }}
  {{ end }}
{{ end }}
```
Hvis `last_editor` er bare en login (ingen parentes), hentes visningsnavnet fra git-commit-historikken → gir `erikhag1git (Erik Hagen)` uten å re-lagre filene.

**Fallback (ingen `last_editor` i frontmatter):** Viser bare `.GitInfo.AuthorName` = `Erik Hagen`. Eks: sider commitet direkte via git uten nettstedseditor. Loginen er ikke tilgjengelig fra git-historikk alene.

**Filer endret:** `custom-footer.html`, `header.html`

#### ⚠ Korrigert samme sesjon: GitInfo.AuthorName ≠ siste innholdsredaktør

**Bug oppdaget:** `2benmoen` redigerte en side via nettstedseditor → `last_editor: 2benmoen`. Siden ble etterpå berørt av UUID-workflow eller annen commit → `.GitInfo.AuthorName` = `Erik Hagen`. Supplementeringen ga `2benmoen (Erik Hagen)` – feil navn på feil bruker.

**Rotårsak:** `.GitInfo.AuthorName` er forfatteren av **siste git-commit på filen**, ikke nødvendigvis den som redigerte innholdet.

**Fix:** Supplement-steget fjernet fra `header.html`. Endelig korrekt logikk:
1. Hent `last_editor` fra frontmatter → strip `(ukjent navn)` → vis som den er
2. Fallback kun hvis `last_editor` er tom: vis `.GitInfo.AuthorName`

| Scenario | Vises |
|----------|-------|
| `last_editor: 2benmoen` | `2benmoen` |
| `last_editor: erikhag1git (Erik Hagen)` | `erikhag1git (Erik Hagen)` |
| Ingen `last_editor`, siste git-committer = Erik Hagen | `Erik Hagen` |

---

## Endringslogg – 2026-03-18 (sesjon 15, natt)

### CF Pages Git-integrasjon – eksperimentert og revertert

Forsøkte å bytte fra wrangler til CF Pages native Git-integrasjon. Endte med full revert. Se sesjon 16 for opprydding.

**Hva ble gjort:**
- DIN-font-aliaser fikset i `custom-head.html` (`@font-face local('Arial Bold')` + `strong/b` override)
- `ul margin-bottom` fikset (`.a-text ul { margin-bottom: 1rem !important }`)
- GUI-forbedringer i byggehistorikk: tidsstempel til venstre, `1m56s`-format, CF-tilstander (kø/pågår/ferdig)
- SHA-basert CF-deteksjon via GitHub Checks API (`waitForCfCheckRun`)
- CF Pages Git-integrasjon opprettet som nytt prosjekt `samt-bu-docs-git` (siden `samt-bu-docs` var Direct Upload og ikke kunne konverteres)

**Siste stabile tema-commit FØR eksperimenteringen:** `b309330` (kl. 22:28)

**Commits fra eksperimenteringen (kan plukkes opp igjen):** `9e7721c`–`67567db` i `hugo-theme-samt-bu`

**Filer endret:** `custom-head.html`, `custom-footer.html`

---

## Endringslogg – 2026-03-19 (sesjon 16, tidlig morgen)

### ✅ Tilbake til stabil wrangler-tilstand

**Bakgrunn:** Sesjon 15 endte i ustabil tilstand – `hugo.yml` brukte CF Git-integrasjon, og SHA-basert polling (`waitForCfCheckRun`) timeouter med wrangler siden wrangler ikke lager GitHub check-runs.

**Hva ble gjort:**

1. **`hugo.yml` revertert til wrangler** – hentet innhold fra commit `34ed286`. Ett `build`-jobb, `baseURL "https://samt-bu-docs.pages.dev/"`, `npx wrangler pages deploy`.

2. **Tema fullt revertert til `b309330`** – `git checkout b309330 -- .` i `hugo-theme-samt-bu` → ny commit `7abb6a8`. Fjerner alle CF-spesifikke GUI-endringer, SHA-routing og `waitForCfCheckRun`.

3. **`cancel-in-progress: false`** – endret fra `true` for å unngå at raske endringer avbryter aktive bygg. Kjent bieffekt: ved 3+ samtidige jobber vises den tredje ikke i byggehistorikken før de to første er ferdige (ikke farlig, alt blir riktig til slutt).

**CF Pages Git-integrasjonen (`samt-bu-docs-git.pages.dev`):** Fortsatt aktiv, bygger ved push til `main`. Bør slettes i CF-dashbordet (bruker build-kvote unødvendig). Kan ikke interferere med wrangler-deployen – separate prosjekter.

**CF Pages og parallelle bygg:** CF Pages serialiserer deployments (én aktiv per prosjekt), uavhengig av wrangler eller Git-integrasjon. Ekte parallelle bygg krever annen plattform.

**Nøkkel-commits:**
- `hugo-theme-samt-bu`: `7abb6a8` (revert til b309330)
- `samt-bu-docs`: `85a085d` (cancel-in-progress: false)

**Filer endret:** `.github/workflows/hugo.yml`, `themes/hugo-theme-samt-bu` (submodule-peker)

---

## Analyse: Parallelle bygg på Cloudflare Pages – hypotese, test og konklusjon

### Bakgrunn og hypotese

Nettstedsredaktøren lar brukere lagre endringer direkte fra nettleseren. Hvert lagre-klikk trigger en GitHub-commit → GitHub Actions-bygg → wrangler deploy. Ved rask redigering (f.eks. tre sider på 30 sekunder) oppstår spørsmålet: kan CF Pages kjøre disse deploys parallelt, slik at alle tre er synlige på nettstedet raskt?

**Hypotesen** var at CF Pages sin native Git-integrasjon – med annonserte «6 concurrent build slots» på betalte planer – kanskje ville tillate ekte parallelle deployments til samme prosjekt/branch, i motsetning til wrangler (Direct Upload) der hvert deploy er en sekvensiell opplasting.

**Motivasjon for å undersøke dette:** GUI-en viser en pending-indikator og byggehistorikk. Hvis bygg kjøres parallelt, kan alle tre ferdigstilles omtrent samtidig og nettstedet oppdateres raskt. Med sekvensiell behandling må brukeren vente på at bygg 1 → 2 → 3 kjøres i tur.

### Hva vi testet (sesjon 15, 2026-03-18/19)

1. **CF Pages Direct Upload (wrangler)** – eksisterende oppsett. Bygg skjer i GitHub Actions, output lastes opp via `npx wrangler pages deploy`. `cancel-in-progress: true` avbrøt eldre bygg ved ny push.

2. **CF Pages Git-integrasjon** – opprettet nytt CF Pages-prosjekt `samt-bu-docs-git` koblet direkte til `SAMT-X/samt-bu-docs`-repoet på GitHub. CF Pages bygger da selv (Hugo) på sine egne servere ved push til `main`, uten GitHub Actions. Byttet `hugo.yml` til kun å kjøre UUID-sjekk + trigge CF via deploy hook.

3. **Observerte byggetider** med Git-integrasjon ved multiple raske pusher: tidsstemplene i byggehistorikken viste tydelig at hvert bygg ventet på at forrige var ferdig før det startet.

### Hva vi observerte

| Observasjon | Implikasjon |
|-------------|-------------|
| CF Pages Git-integrasjon køer bygg sekvensielt per prosjekt/branch – bekreftet fra tidsmålinger i sesjon 15 | «6 concurrent build slots» gjelder _ulike_ prosjekter eller branches parallelt, ikke multiple pusher til _samme_ branch |
| `samt-bu-docs-git.pages.dev` og `samt-bu-docs.pages.dev` viser alltid identisk innhold etter bygg | Begge peker på `main`-branchen – de er to uavhengige visninger av samme kodebase |
| Wrangler deploy (Direct Upload) serialiserer også på CF sin side | CF Pages tillater uansett kun én aktiv deployment per prosjekt om gangen, uavhengig av deploy-metode |
| SHA-basert polling via GitHub Checks API (`waitForCfCheckRun`) fungerte med Git-integrasjon | Wrangler lager ingen GitHub check-runs → polling timeouter. Krever altså Git-integrasjon for å brukes |

### Konklusjon

**CF Pages støtter ikke ekte parallelle deployments til samme prosjekt/branch**, verken via wrangler eller native Git-integrasjon. «6 concurrent build slots» refererer til kapasitet på tvers av prosjekter, ikke innad i ett prosjekt.

Nåværende løsning (`cancel-in-progress: false`) er det beste vi kan oppnå med CF Pages: alle bygg kjøres i kø og fullføres i rekkefølge. Siste endring vinner til slutt. Eneste kjente bieffekt er at GUI-en ikke viser jobb nr. 3 i byggehistorikken før de to første er ferdige.

**Ekte parallelle deploys** ville krevd en plattform uten denne begrensningen (f.eks. Vercel), eller en arkitektur der hver redaktørsesjon deployer til en unik preview-URL som merges inn. Begge er uforholdsmessig komplekse for dette prosjektets skala.

**`samt-bu-docs-git`-prosjektet er slettet** fra CF-dashbordet (2026-03-19).

---

## Trygg rekonstruksjon – strategi og kandidatliste (oppdatert 2026-03-20)

### Bakgrunn

Original baseline: `ca0a076` = `d3657b1` (17.03 13:08) – stabil tilstand med jobbhistorikk, køstatus og avløst-håndtering, ingen CF-avhengigheter.

**Nåværende tema-baseline etter sesjon 18:** `916251e` (20.03, natt)

Sesjon 18 innførte følgende på toppen av baseline (alle testet og bekreftet ok):

| Ny tema-commit | Beskrivelse |
|----------------|-------------|
| `74ac24b` | Mine/Alle-faner + tidsstempel i byggehistorikk (fra `58f2442` + `2c68a55`) |
| `191fd92` | Byggetid fra API (`updated_at − created_at`), fjernet localStorage-løsning |
| `0a5d052` | Sekundteller også i kø-fasen (ingen «I kø»-tekst) |
| `491770a` | `cache: no-store` på ref-henting i createFilesInOneCommit + deleteFilesInOneCommit |
| `ee813df` | Felles pending-indikator for ny side og sletting (kandidat #4) |
| `916251e` | Startsignal (samtuPlayStart) ved oppstart av slettepolling |

### Ufravikelige premisser

1. **Aldri igjen forsøke parallelle bygg via Cloudflare** – stengt dør.
2. **Innhold (`content/`) påvirkes aldri av GUI-endringer** – kun tema og `.github/`.
3. **Én funksjon om gangen** – test og verifiser før neste.
4. **Alltid manuelt (ikke cherry-pick)** – unngår uønskede kontekstlinjer.

### ✅ Alle kandidater innarbeidet (sesjon 18–19)

| # | Tema-commit (ny) | Beskrivelse | Status |
|---|-----------------|-------------|--------|
| 1 | `74ac24b` | Mine/Alle-faner + tidsstempel i byggehistorikk | ✅ sesjon 18 |
| 2 | `0f48f71`+`733ce00`+`a74773b` | Fix: «Endre i GitHub»-lenke riktig repo + last_editor-bonus | ✅ sesjon 19 |
| 3 | `491770a` | `cache: no-store` i createFilesInOneCommit + deleteFilesInOneCommit | ✅ sesjon 18 |
| 4 | `ee813df` | Felles pending-indikator for ny side og sletting | ✅ sesjon 18 |
| 5+6 | `dac996a` | Slett-dialog UX + rekursiv sletting (to-stegs, deleteDirectoryRecursive) | ✅ sesjon 19 (utest) |
| 7 | `0f48f71`+`733ce00` | `last_editor`: konsistent visning, GitHub API-oppslag | ✅ sesjon 19 |
| 8 | `3d3ae27` | createQeCommit: brukervennlig feilmelding ved konflikter | ✅ sesjon 19 |
| 9 | (se sesjon 18) | Font-fikser: DIN→Arial, bold !important, margin-bottom ul | ✅ sesjon 18 |
| 10 | – (hugo.yml) | CI retry-løkke for wrangler deploy (lå allerede i hugo.yml) | ✅ sesjon 19 |

**Bevisst utelatt (CF-avhengige, ikke aktuelle):**
- `9e7721c`–`67567db`: CF Pages ETag-polling, SHA-basert deteksjon, `waitForCfCheckRun`.

**Adaptivt poll-intervall** – `d58a7c6` – CF-agnostisk, kan vurderes som fremtidig forbedring.

**Nåværende tema-HEAD:** `3d3ae27` (2026-03-20)

### Fremgangsmåte

For hver kandidat:
1. `git show <hash>` – forstå eksakt hva som endres
2. Gjør endringen manuelt i nåværende fil
3. Bygg lokalt med `hugo server` og verifiser
4. Commit i temaet → push → oppdater submodule-peker i `samt-bu-docs` → push
5. Observer bygg og oppførsel på `samt-bu-docs.pages.dev`

---

## Endringslogg – 2026-03-20 (sesjon 19)

### Rekonstruksjon fullført – kandidater #2, #5+#6, #7, #8, #9, #10

Startet fra baseline `916251e` (sesjon 18). Alle gjenstående kandidater innarbeidet manuelt og pushet.

**Kandidat #2 – Fix: «Endre i GitHub»-lenke riktig repo (`footer.html`)**
- `hasPrefix`-routing i `footer.html`: `teams/team-architecture/`, `teams/team-semantics/`, `utkast/`, `loesninger/cms-loesninger/samt-bu-docs/` → korrekt repo-URL
- Alle andre sider: fallback til `$Site.Params.editURL` som før
- Tema-commit: `0f48f71`

**Bonus til #7 – fullt navn fra GitHub API + last_editor ved ny side**
- `header.html`: `data-editor-login`-attributt på redaktør-span; strip av gamle `(ukjent navn)`-verdier
- `footer.html` (JS): `fetch('https://api.github.com/users/' + login)` → oppdaterer span med fullt navn (ingen token nødvendig)
- `custom-footer.html`: `last_editor` skrives til frontmatter ved opprettelse av ny side
- `custom-footer.html`: editorValue-logikk: `login (Fullt navn)` hvis navn finnes, ellers bare `login`
- Tema-commits: `733ce00`, `a74773b`

**Kandidat #5+#6 kombinert – Slett-dialog UX + rekursiv sletting**
- `edit-switcher.html`: tittel via `data-del-title` (unngår HTML-encoding), `{{ len .Pages }}` sendes som `childCount`
- `edit-switcher.html`: ny dialog-HTML (520px, 8px radius) med `del-children-warning`, `del-footnote`, `del-confirm-section-2`; font-størrelse px (ikke rem – unngår 10px-arv)
- `custom-footer.html`: `openDeleteDialog` tar nå `childCount`; to-stegs flyt (`showStep2()`, `doCommit()`); `deleteDirectoryRecursive()` via GitHub Trees API
- `showBuildPanel()` skjuler `del-confirm-section-2`
- Tema-commit: `dac996a`

**Kandidat #8 – createQeCommit: brukervennlig feilmelding**
- «Update is not a fast forward» → «Konflikt: siden ble endret av andre. Prøv igjen.» (nb) / «Conflict: page was changed by others. Try again.» (en)
- Tema-commit: `3d3ae27`

**Kandidat #9** – Innarbeidet sesjon 18 (DIN→Arial @font-face, margin-bottom ul)

**Kandidat #10 – CI retry-løkke for wrangler deploy**
- Lå allerede i `hugo.yml` (retry-løkke med 3 forsøk, 15 sek mellom)
- Ingen endring nødvendig

**Viktig lært mønster – font-size rem i dialogen:**
`1rem` i dette temaet arver ~10px fra HTML-roten (ikke 16px som normalt). Bruk alltid eksplisitte px-verdier i dialoger og overlays.

---

## Endringslogg – 2026-03-20 (sesjon 18)

### Byggehistorikk GUI – rekonstruksjon og forbedringer

Startet fra baseline `ca0a076` (`d3657b1`, 17.03 13:08). Alle endringer er manuelt innarbeidet og testet.

**Innarbeidet fra rekonstruksjonslisten:**
- **Kandidat #1** (`58f2442`): Mine/Alle-faner i byggehistorikk
- **Kandidat #3** (`1082501`): `cache: no-store` på ref-henting i createFilesInOneCommit og deleteFilesInOneCommit
- **Kandidat #4** (`f9efd4a`): Felles pending-indikator for ny side og sletting

**Nye forbedringer (ikke i original kandidatliste):**
- Byggetid fra API (`updated_at − created_at`) erstatter localStorage-løsning (`samtuStoreBuildTime`/`samtuLookupBuildTime` fjernet). Gir korrekt varighet for alle bygg uavhengig av om de ble fulgt i nettleseren.
- Tidsstempel (yy-mm-dd / hh:mm:ss) per rad i byggehistorikk – kombinert med kandidat #1.
- Sekundteller vises også i kø-fasen (`queued`/`waiting`/`pending`/`requested` behandles likt `in_progress`). Ikonet (⏰ vs spinner) skiller visuelt.
- Startsignal (`samtuPlayStart`) manglet i sletteflytens `pollBuild` – lagt til.

**Læring – `cache: no-store`:**
Feilen «Update is not a fast forward» oppstår fordi nettleseren cacher `GET /git/ref/heads/main` i 60 sek. Retry-løkken henter da samme foreldede SHA og feiler på nytt. `createQeCommit` hadde allerede `cache: no-store`; de to andre manglet det. Alltid sjekk alle tre ved fremtidige endringer i commit-flyten.

**Læring – localStorage for byggetid:**
Å lagre byggetid i localStorage er unødvendig – GitHub API gir `created_at` og `updated_at` på hvert run. `updated_at − created_at` ≈ byggetid, alltid tilgjengelig, null lokalt state.

---

## Endringslogg – 2026-03-21 (sesjon 21)

### Fiks: falsk «Build job failed» ved lange byggejobber (bygg-feil-timeout)

**Tema-commit:** `414fa54`

**Problem:** ETag-pollingen (redigering) og URL-pollingen (ny side) hadde harde maksimumsgrenser (180s / 90s). Etter grensen ble det umiddelbart spilt feilsignal og vist feilmelding – selv om bygget fortsatt pågikk eller hadde fullført.

**Løsning:** Ved timeout kaller polleren GitHub Actions API og sjekker faktisk byggestatus:

| API-svar | Handling |
|----------|----------|
| `in_progress` / `queued` | Nullstill teller, fortsett polling |
| `completed/success` | Vis ferdig, naviger |
| `completed/cancelled` | Nullstill, vis «Avbrutt – venter på nytt bygg…» |
| `completed/failure` | Vis faktisk feil |
| Ingen run funnet | Vis tidsavbrudd (fallback) |

**`_checkingApi`-flagg** forhindrer parallelle API-kall mellom intervalltikk mens det async-fetches.

**To pollere fikset:**

- **ETag-poll** (`pollQeBuild` i `custom-footer.html`, 180s): Sjekker GH API ved timeout, filterer på `startTime - 30000` (30s klokke-buffer som `startGhPoll`).
- **URL-poll** (`startUrlPoll`, 90s): Identisk logikk. Funksjonen tar nå valgfri `startTime`-parameter; `npPollBuild()` sender `startTime` ved kall. Fallback: `Date.now() - 120000` (2 min bakover) for kall uten `startTime`.

**Veikart-status:** `bygg-feil-timeout` → Godkjent.

---

## Endringslogg – 2026-03-21 (sesjon 21, del 2)

### Ny funksjon: pending-indikator fanger opp eksternt-trigget bygg

**Tema-commit:** `b600033`

**Problem:** Pending-indikatoren var usynlig for bygg trigget utenfra (lokal push, GitHub web-UI, API). Brukere så idle-tilstand selv om et bygg pågikk, og siden ble ikke automatisk lastet inn ved ferdig bygg.

**Nye globale funksjoner:**
- `samtuShowExternalBuildIndicator()` – spinner + «Nettstedet oppdateres…» med `opacity:.7`. Bruker `data-external`-attributt (ikke `data-building`) → hindrer ikke bakgrunnspolling og overstyres av eget bygg.
- `samtuHideExternalBuildIndicator()` – fjerner ekstern-indikatoren.

**Utvidet bakgrunnspolling (bakgrunnspolling-scriptet):**
- `bgExternalRun` og `bgFastTimer` – nye modulvariabler.
- `checkExternalBuilds()` – kaller GH Actions API hvert 45. sek (fra bgTimer) når ingen egne bygg pågår og bruker er innlogget. Starter `bgFastTimer` (5s ETag-poll) når aktivt eksternt bygg oppdages.
- `startBgFastPoll()` / `stopBgFastPoll()` – starter/stopper rask ETag-poll. bgFastTimer auto-laster inn siden ved ETag-endring.
- bgTimer skiller nå mellom tre tilfeller ved ETag-endring:
  1. Eget bygg ventende → `samtuDecrementPending()` + reload (som før)
  2. Eksternt bygg sporet (`bgExternalRun` satt) → `stopBgFastPoll()` + reload (ny)
  3. Ukjent endring → banner (som før)

**Ingen endring for ikke-innloggede brukere.**

**Veikart-status:** `pending-indikator-externe-bygg` → Godkjent.

---

## Endringslogg – 2026-03-27 (sesjon 22)

### Veikart-oppsplitting

`solution-samt-bu-docs/content/veikart/` er nå delt i fire underseksjoner:

| Mappe | Weight | Innhold |
|-------|--------|---------|
| `plattform-ny-funksjonalitet/` | 10 | 10 oppføringer – nye funksjoner (implementert og planlagt) |
| `plattform-dokumentasjon/` | 15 | 4 oppføringer – utredninger, strategidok., utdaterte guider |
| `plattform-feilretting/` | 20 | 5 oppføringer – feilrettinger (implementert og planlagt) |
| `innholdsoppgaver/` | 30 | 3 oppføringer – innhold, struktur, administrasjon |

`plattform-dokumentasjon/` inneholder: `ny-side-samme-nivaa` (utdatert), `ny-cms-portal` (utdatert, refererer Decap), `samtidige-bygg-cloudflare` (utredning), `branch-strategi-gui-utvikling` (strategidok.).

### nytt-modulrepo flyttet til teknisk-dokumentasjon

`veikart/nytt-modulrepo/` → `teknisk-dokumentasjon/nytt-modulrepo/` (weight 25, mellom github-struktur:20 og dokumentasjonspraksis:30). `status`-felt fjernet.

### Tema-klon reconciliering

`S:/app-data/github/samt-x-repos/hugo-theme-samt-bu/` (separat klon) var bak remote – fast-forwardet til `b600033` med `git pull --rebase`.

### Git-tilstand ved sesjonsavslutning

| Repo | Tilstand |
|------|----------|
| `hugo-theme-samt-bu` (submodule) | ✅ `b600033` |
| `hugo-theme-samt-bu` (separat klon) | ✅ `b600033` |
| `samt-bu-docs` | ✅ `43281a1` |
| `solution-samt-bu-docs` | ✅ `e9bb2cd` |

---

## Endringslogg – 2026-04-25 (sesjon 34)

### Domeneflytting: samt-bu.no inn i Cloudflare

Nettstedet har fått eget domene. Full oversikt over hva som ble gjort:

**Infrastruktur:**
- `samt-bu.no` lagt til i Cloudflare (nameservere byttet fra Gigahost til `john.ns.cloudflare.com` / `tina.ns.cloudflare.com`)
- `docs.samt-bu.no` – custom domain på Cloudflare Pages-prosjektet `samt-bu-docs`
- `auth.samt-bu.no` – custom domain på Cloudflare Worker `samt-bu-cms-auth`
- `samt-bu.no` → 301 redirect til `docs.samt-bu.no` (Cloudflare Redirect Rule)
- `samt-bu-docs.pages.dev` → 301 redirect til `docs.samt-bu.no` (Pages Function `functions/_middleware.js`)
- GitHub Pages deaktivert for `SAMT-X/samt-bu-docs`

**Kodeendringer:**
- `hugo.toml` + `hugo.yml`: `baseURL` → `https://docs.samt-bu.no/`
- `cloudflare-worker/oauth-worker.js`: CORS-origin og build-status proxy URL → `docs.samt-bu.no`
- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html`: `workerBase` → `https://auth.samt-bu.no`
- GitHub OAuth App: callback-URL → `https://auth.samt-bu.no/callback`, navn → «SAMT-X Docs»
- `CLAUDE.md`: alle URL-referanser oppdatert
- Cloudflare API-token rotert, GitHub Actions secret `CF_API_TOKEN` oppdatert

**Verifisert fungerende:**
- OAuth-innlogging via `auth.samt-bu.no`
- CI-deploy med nytt token
- PR-forslagsflyt for bruker uten skrivetilgang
- Redirect-kjeden fra gamle URL-er

### Ny dokumentasjon denne sesjonen

- `veikart/plattform-ny-funksjonalitet/pull-request-flyt/` – status oppdatert til «Til QA», full implementeringsbeskrivelse
- `om/hvordan-bidra/innebygd-redigering/` – skrivetilgang ikke nødvendig, forslagsflyt forklart
- `brukerveiledning/cms-i-dybden/` – ny seksjon «Forslagsflyt for brukere uten skrivetilgang»

### Gjeldende URL-er

| Formål | URL |
|--------|-----|
| Nettsted | `https://docs.samt-bu.no/` |
| OAuth-worker | `https://auth.samt-bu.no` |
| Rotdomene (redirect) | `https://samt-bu.no/` → `docs.samt-bu.no` |
| Gammel URL (redirect) | `https://samt-bu-docs.pages.dev/` → `docs.samt-bu.no` |

### Git-tilstand ved sesjonsavslutning

| Repo | Tilstand |
|------|----------|
| `hugo-theme-samt-bu` (submodule) | ✅ pushet |
| `samt-bu-docs` | ✅ pushet (HEAD: `474f645`) |
| `solution-samt-bu-docs` | ✅ pushet |

---

## Endringslogg – 2026-04-26

### PR-håndtering: rebase-flyt med fork-push (verifisert)

Etablert og testet arbeidsflyt for å behandle innkommende PR-er fra bidragsytere (fork-baserte PR-er).

#### Bakgrunn

Bidragsytere uten skrivetilgang sender forslag via det innebygde redigeringsgrensesnittet som pull requests fra sin fork. Disse PR-ene havner ofte i konflikt med `main` fordi `main` har beveget seg siden PR-en ble opprettet.

#### Nøkkelfunn: `maintainer_can_modify: true`

GitHub lar repo-maintainere pushe direkte til en bidragsyters fork-gren hvis PR-en er opprettet med «Allow edits from maintainers» (standard). Det innebygde redigeringsgrensesnittet setter alltid dette flagget. Dette er nøkkelen til en ren flyt.

#### Verifisert flyt (gir «Merged», ikke «Closed»)

```bash
# 1. Sjekk konfliktstatus og maintainer_can_modify
gh pr view <nr> --repo SAMT-X/samt-bu-docs --json mergeable,mergeStateStatus,maintainerCanModify

# 2. Hent fork-grenen
git remote add <login> https://github.com/<login>/samt-bu-docs.git
git fetch <login> <branchname>
git checkout -b pr-<nr> <login>/<branchname>

# 3. Rebase på main
git rebase origin/main
# løs eventuelle konflikter, git add, GIT_EDITOR=true git rebase --continue

# 4. Push rebased commits tilbake til fork-grenen
git push <login> pr-<nr>:<branchname> --force-with-lease

# 5. Merge via GitHub → gir "Merged" (lilla)
gh pr merge <nr> --repo SAMT-X/samt-bu-docs --merge

# 6. Rydd opp
git checkout main && git pull origin main
git branch -D pr-<nr>
git remote remove <login>
git push origin --delete pr-<nr>  # slett eventuelle temp-branches i origin
```

#### Brukervennlig kommentar – alltid

Legg alltid til to kommentarer via `gh pr comment`:
1. **Ved merge:** bekreft at forslaget er godkjent, si at nettstedet oppdateres om noen minutter
2. **Ved etterfølgende admin-endringer** (f.eks. weight-justering): forklar hva som ble endret og hvorfor – bruk `@<login>` for å sende e-post

Bidragsytere er typisk ikke-tekniske og forstår ikke GitHub-statusmeldinger. En kort, vennlig kommentar gjør hele opplevelsen bedre.

#### Fallback: hvis `maintainer_can_modify` er false

Push rebased branch til `origin` som temp-branch, merge lokalt med `--no-ff -m "... Closes #<nr>"`. PR vises som «Closed», ikke «Merged». Kompenser alltid med kommentar.

#### Dokumentert i

- `CLAUDE.md` (samt-bu-docs): «PR-håndtering»-seksjonen – trinn-for-trinn-flyt
- `memory/feedback_pr_merge_workflow.md`: atferdsregel for Claude

---

## Endringslogg – 2026-04-26/27 (sesjon 36)

### Bug 1: checkCollaboratorPermission returnerte false for org-eiere

**Symptom:** Brukere med skrivetilgang via org-eierskap (f.eks. `erikhag1git`) fikk fork/PR-flyt i stedet for direkte commit. Skapte 5 stale PRer på `team-pilot-1`.

**Rotårsak:** `checkCollaboratorPermission` brukte `GET /repos/SAMT-X/{repo}/collaborators/{login}` som kun returnerer 204 for *direkte* outside collaborators – ikke for org-eiere/-medlemmer.

**Fix:** Byttet til `GET /repos/SAMT-X/{repo}` og sjekker `data.permissions.push || data.permissions.admin`. Cache-nøkkel bumped fra `samtu-perm-` til `samtu-perm2-` for å ugyldiggjøre stale false-oppføringer.

**Fil:** `hugo-theme-samt-bu/layouts/partials/custom-footer.html` – funksjon `checkCollaboratorPermission`

### Bug 2: Pilot 1 viste ikke statusymbol i menyen

**Symptom:** `status: Pågår` satt i `team-pilot-1/_index.nb.md`, men menyen viste «Pilot 1» uten ◐-symbol.

**Rotårsak:** To sett rotfiler for Pilot 1-siden:
- Lokal fil i `samt-bu-docs/content/pilotering/pilot-1/_index.nb.md` (ingen `status`) – **Hugo bruker denne**
- Modulfil i `team-pilot-1/content/_index.nb.md` (har `status`) – **overstyres av lokal fil**

Edit-switcher pekte på modulfilen (`team-pilot-1`) mens Hugo viste den lokale filen. Alle redigeringer via editor havnet i feil fil.

**Fix:**
1. `status: Pågår` / `status: In progress` lagt i de lokale filene i `samt-bu-docs`
2. `team-pilot-1`-grenen fjernet fra edit-switcher (begge steder: hovedlogikk + søskendata) – `pilotering/pilot-1/` rutes nå korrekt til `samt-bu-docs`

**Lærdom:** Når en lokal fil og en modulfil finnes på samme sti, vinner alltid den lokale. Edit-switcher-ruting må reflektere dette – ikke moduloppsettet i `hugo.toml`.
