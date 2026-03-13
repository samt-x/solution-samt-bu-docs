---
id: a1dec965-c693-4bbd-a231-1162fb4306ef
title: "Utviklernotater og Claude-kontekst"
linkTitle: "Utviklernotater"
weight: 90
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

**URL-polling (cases 2+3):** `HEAD` mot ny side-URL. HTTP 200 → siden finnes. Krever ingen token.

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
