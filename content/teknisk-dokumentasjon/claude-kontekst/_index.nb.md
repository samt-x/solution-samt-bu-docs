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

### Edit-switcher – nåværende menyvalg (2026-03-10)

| Valg | Status | Implementasjon |
|------|--------|----------------|
| «Denne siden» | ✅ Virker | Decap deep-link til gjeldende side |
| «Side – samme nivå» | ⏳ Alert-popup (midlertidig) | `$addSiblingURL` beregnet i edit-switcher.html, men knappen viser kun popup. Skjules på rotnivå-sider (`$entrySlug == ""`). |
| «Underkapittel» | ⏳ Alert-popup (midlertidig) | `$addChildURL` beregnet med `?filename=nytt-kapittel/_index.nb.md`, men knappen viser kun popup. |
| «Andre valg» | ✅ Virker | Lenke til CMS-portaloverside |

**Popup-tekst (begge + knapper):** Tittel «Oppdatert implementering i arbeid», tekst «I påvente av oppdatert implementering kan du gjøre dette via GitHub.»

**Planlagt:** Erstatt popup med ekte GitHub create file-URL for begge knapper. Veikart-oppføringer finnes i `solution-samt-bu-docs/content/veikart/ny-side-samme-nivaa/` og `legg-til-underkapittel/`.

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

### «Ny side – samme nivå»-dialog: tre forbedringer
Alle endringer i `hugo-theme-samt-bu/layouts/partials/` (`edit-switcher.html` + `custom-footer.html`):

1. **Blank status-valg:** `<option value="">–</option>` øverst i status-dropdown. Hvis blank velges utelates `status:`-feltet helt fra frontmatter (begge nb og en).
2. **Defaultvekt = gjeldende side + 1:** Hugo sender `.Weight` til `openNewSiblingDialog(repo, parentPath, lang, currentWeight)`. Vekt-feltet forhåndsutfylles ved åpning.
3. **Auto-shift av nabosider:** Etter at de to nye filene er opprettet via GitHub API, kjøres `shiftSiblings(token, repo, parentPath, minWeight, excludeSlug)` som:
   - Henter directory listing av `parentPath` fra GitHub Contents API
   - Leser `_index.nb.md` + `_index.en.md` for alle undermapper parallelt (`Promise.all`)
   - Øker `weight` med 1 for alle filer med `weight >= minWeight` (unntatt den nye siden)
   - Bruker `atob`/`btoa` + regex for å parse og oppdatere YAML frontmatter in-memory
   - Committer én fil av gangen med melding «Auto: juster vekt etter ny side»
   - Ignorer feil for enkeltfiler (`.catch(() => {})`) – siden dette er et best-effort-steg
