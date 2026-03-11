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

| Mappe | Repo | Språk | Dekker |
|-------|------|-------|--------|
| `static/edit/docs-nb/` | `samt-bu-docs` | nb | Lokalt innhold i samt-bu-docs |
| `static/edit/docs-en/` | `samt-bu-docs` | en | Lokalt innhold i samt-bu-docs |
| `static/edit/arkitektur-nb/` | `team-architecture` | nb | `content/teams/team-architecture/` |
| `static/edit/arkitektur-en/` | `team-architecture` | en | `content/teams/team-architecture/` |
| `static/edit/utkast-nb/` | `samt-bu-drafts` | nb | `content/utkast/` |
| `static/edit/utkast-en/` | `samt-bu-drafts` | en | `content/utkast/` |
| `static/edit/loesninger-nb/` | `solution-samt-bu-docs` | nb | `content/loesninger/cms-loesninger/samt-bu-docs/` |
| `static/edit/loesninger-en/` | `solution-samt-bu-docs` | en | `content/loesninger/cms-loesninger/samt-bu-docs/` |

> **Kritisk mønster:** Hvert Hugo-modulrepo som monterer innhold **må ha sin egen CMS-portal** som peker på det repoet. Hvis modulinnhold feilaktig rutes til `docs`-portalen (som peker på `samt-bu-docs`), finnes ikke filen der → CMS viser tomme felter uten feilmelding. Symptomet er: alle skjemafelter er tomme, men «CHANGES SAVED» vises.

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

### Edit-switcher – nåværende menyvalg (2026-03-11)

| Valg | Status | Implementasjon |
|------|--------|----------------|
| «Denne siden» | ✅ Virker | Decap deep-link til gjeldende side |
| «Side – samme nivå» | ✅ Virker | Åpner «Ny side»-dialog (se under) |
| «Underkapittel» | ⏳ Alert-popup (midlertidig) | `$addChildURL` beregnet med `?filename=nytt-kapittel/_index.nb.md`, men knappen viser kun popup. |
| «Slett denne siden» | ✅ Virker | Bekreftelsesdialog → atomisk slett nb+en i én commit → polling → auto-navigering |
| «Andre valg» | ✅ Virker | Lenke til CMS-portaloverside |

**Planlagt:** Erstatt popup for «Underkapittel» med ekte dialog. Veikart-oppføring finnes i `solution-samt-bu-docs/content/veikart/legg-til-underkapittel/`.

**Merk:** Knappene bruker `onclick="alert(this.getAttribute('data-msg').replace(/\\n/g,'\n')); return false;"` – `replace()`-trikset er nødvendig for at `\n` i `data-msg`-attributtet renderes som faktisk linjeskift i `alert()`.

### Decap CMS – kjent begrensning: «Ny side» og «Dupliser» feiler

**Symptom:** «Failed to persist entry: API_ERROR: Git Repository Error: path contains a malformed path component»

**Rotårsak:** `path: "{{dir}}/_index"` i nested collection. For nye oppføringer uten eksisterende mappekontest settes `{{dir}}` = `.` (punktum) → full sti blir `content/./_index.nb.md` → GitHub API avviser som ugyldig stikomponent.

**Redigering av eksisterende sider virker** – da hentes `{{dir}}` fra den faktiske filstien.

**Løsning fremover:** Implementer «+ Side – samme nivå»-knapp i Endre-menyen som bruker GitHub "create file"-URL direkte (omgår Decap). Se «Neste planlagte oppgaver» i MEMORY.md.

**Workaround nå:** Opprett nye filer manuelt via GitHub (se popup i «Legg til underkapittel»-valget).

### Rutinglogikk i edit-switcher (fire grener)

Basert på `path.Dir .File.Path` (normalisert, unngår Windows-backslash-problem):

- `hasPrefix "teams/"` → arkitektur-portal
- `eq/hasPrefix "utkast"` → utkast-portal
- `eq/hasPrefix "loesninger/cms-loesninger/samt-bu-docs"` → loesninger-portal
- Alt annet → docs-portal

**Entry-slug:** Full relativ sti inkl. `/_index`, relativt til modulens eget `content/`-rot. F.eks. gir `loesninger/cms-loesninger/samt-bu-docs/brukerveiledning` → slug `brukerveiledning/_index`.

**Når en ny modul legges til:** Legg til nytt grein i `edit-switcher.html` *før* `{{ else }}`-blokken. Se eksisterende grener for mønster.

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

**`getDecapToken` – global scope:**
Funksjonen ble løftet ut av np-dialog IIFE til global `<script>`-blokk øverst i `custom-footer.html`, slik at både «Ny side»-dialogen og «Slett»-dialogen kan dele den.

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
