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

| Fil | Rolle | Grense |
|-----|-------|--------|
| `C:\Users\Win11_local\.claude\projects\...\memory\MEMORY.md` | Automatisk lastet ved sesjonstart – kompakt indeks og kritiske "aldri glem"-punkter | 200 linjer |
| `content/loesninger/.../teknisk-dokumentasjon/` | Canonical kilde – leses eksplisitt ved behov, ingen linjegrense, versjonskontrollert i git | Ingen |

**Konvensjon:** Detaljer hører hjemme her (i repo). `MEMORY.md` peker hit. Ingenting viktig trimmes bort – det flyttes hit i stedet.

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
| `themes/hugo-theme-samt-bu/layouts/partials/edit-switcher.html` | Endre/Edit-dropdown med Decap-deeplink |
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

## Decap CMS

- **Norsk portal:** `/edit/`  |  **Engelsk portal:** `/edit/en/`
- **OAuth-proxy:** Cloudflare Worker `https://samt-bu-cms-auth.erik-hag1.workers.dev`
- **Lokal testing:** `hugo server` + `local_backend: true` i config.yml

### Aktive portaler

| Mappe | Repo | Språk |
|-------|------|-------|
| `static/edit/docs-nb/` | `samt-bu-docs` | nb |
| `static/edit/docs-en/` | `samt-bu-docs` | en |
| `static/edit/arkitektur-nb/` | `team-architecture` | nb |
| `static/edit/arkitektur-en/` | `team-architecture` | en |
| `static/edit/utkast-nb/` | `samt-bu-drafts` | nb |
| `static/edit/utkast-en/` | `samt-bu-drafts` | en |

### Tilbake-lenke i portaler (document.referrer)

Alle 6 portaler har en fast `«← Tilbake til nettstedet»`-lenke (bottom-right). Den bruker `document.referrer` for å returnere brukeren til den **spesifikke siden** de kom fra (ikke rotsiden). Fallback til `/samt-bu-docs/` (NB) / `/samt-bu-docs/en/` (EN) hvis referrer ikke er fra nettstedet eller er tom.

Implementert som inline `<script>` etter ankeret i `index.html` i hver portal:
```html
<script>
  (function() {
    var ref = document.referrer;
    if (ref && ref.indexOf('samt-bu-docs') !== -1 && ref.indexOf('/edit/') === -1) {
      document.getElementById('back-to-portal').href = ref;
    }
  })();
</script>
```

### Rutinglogikk i edit-switcher (tre grener)

Basert på `path.Dir .File.Path` (normalisert, unngår Windows-backslash-problem):

- `hasPrefix "teams/"` → arkitektur-portal
- `eq/hasPrefix "utkast"` → utkast-portal
- Alt annet → docs-portal

**Entry-slug:** Full relativ sti inkl. `/_index`. Rot-sider i moduler bruker `_index` alene.

### UUID (id-felt i frontmatter)

- UUID v4, samme verdi i nb og en for samme side – **aldri endres manuelt**
- Håndteres av `.github/workflows/ensure-uuids.yml` (finnes i alle tre repoer)
- `widget: hidden` + `i18n: duplicate` i alle Decap-portaler → usynlig for redaktøren
- Decap CMS 3.x CDN eksponerer ikke `window.React` → custom widget krever byggesteg, ikke verdt det

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

### pull-all – oppdater alle repoer på én gang

`S:\app-data\github\samt-x-repos\pull-all.bat` (Windows-launcher) → kaller `pull-all.sh`.

Kjører `git pull` for hvert repo under `samt-x-repos/`, pluss `git submodule update --recursive` for repos med `.gitmodules` (p.t. kun `samt-bu-docs`).

**Bruk:** Dobbeltklikk `pull-all.bat` i Utforsker, eller kjør fra bash:
```bash
bash "S:/app-data/github/samt-x-repos/pull-all.sh"
```

---

## GitHub CLI (gh)

- **Plassering:** `C:\Program Files\GitHub CLI\gh.exe` – ikke i PATH i bash fra Claude Code
- **Bruk alltid full sti:** `"/c/Program Files/GitHub CLI/gh.exe"`
- **Slette repos:** krever ekstra scope – kjør `gh auth refresh -h github.com -s delete_repo` og fullfør nettleserflyt

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
