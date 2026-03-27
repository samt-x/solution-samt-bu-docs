---
id: ed2ee794-3c97-4e2d-959d-90b235a4f3d6
title: "Opprette nytt modulrepo – steg-for-steg"
linkTitle: "Nytt modulrepo"
weight: 25
lastmod: 2026-03-26T16:27:46+01:00

---

Fullstendig veiledning for å opprette et nytt Hugo-modulrepo fra bunnen og koble det til SAMT-BU Docs – fra tomt GitHub-repo til publisert innhold under `/teams/<repo-navn>/` (eller annen valgfri sti).

Prosessen krever endringer i to repoer: selve modulrepoet og `samt-bu-docs`.

---

## Forutsetninger

- Tilgang til GitHub-org `samt-x` (eller aktuell org)
- Hugo installert lokalt
- `gh` CLI autentisert
- PAT med `workflow`-scope (samme token som brukes i `DOCS_REBUILD_TOKEN` i eksisterende repoer)

---

## Del 1 – Sett opp modulrepoet

### Steg 1 – Opprett repo på GitHub

Opprett et nytt tomt repo under `samt-x`-orgen (eller aktuell org). Legg til en enkel `README.md` så repoet ikke er helt tomt.

Navnekonvensjon:
- `team-`-prefiks for interne arbeidsrepoer for team
- `samt-bu-`-prefiks for publisert innhold/produkt

### Steg 2 – Klon repoet lokalt

```bash
cd "S:/app-data/github/samt-x-repos"
git clone https://github.com/samt-x/<repo-navn>.git
cd <repo-navn>
```

### Steg 3 – Initialiser som Hugo-modul

```bash
hugo mod init github.com/SAMT-X/<repo-navn>
```

Dette oppretter `go.mod` i rotmappen.

### Steg 4 – Opprett innholdsfiler

```bash
mkdir content
```

Opprett `content/_index.nb.md`:

```yaml
---
title: "<Tittel på norsk>"
linkTitle: "<Kort tittel>"
weight: 30
status: ""
draft: false
---

Kort beskrivelse av innholdet i dette repoet.
```

Opprett `content/_index.en.md`:

```yaml
---
title: "<Title in English>"
linkTitle: "<Short title>"
weight: 10
status: ""
draft: false
---

Short description of the content in this repo.
```

**Merk:** `id`-feltet (UUID) skal **ikke** settes manuelt – det legges til automatisk av `ensure-uuids.py` i CI ved første push.

### Steg 5 – Legg til `ensure-uuids.py`

Kopier skriptet fra et eksisterende modulrepo:

```bash
mkdir -p .github/scripts
cp ../team-architecture/.github/scripts/ensure-uuids.py .github/scripts/
```

### Steg 6 – Legg til `trigger-docs-rebuild.yml`

Opprett `.github/workflows/trigger-docs-rebuild.yml`:

```yaml
name: Trigger rebuild av samt-bu-docs

on:
  push:
    branches: [main]

permissions:
  contents: write

jobs:
  trigger:
    if: github.actor != 'github-actions[bot]'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Sikre UUID-er i frontmatter
        run: |
          python3 .github/scripts/ensure-uuids.py
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add content/
          if git diff --staged --quiet; then
            echo "Ingen endringer – alle UUID-er var på plass"
          else
            git commit -m "Auto: legg til manglende UUID-er i frontmatter [skip ci]"
            for i in 1 2 3; do
              git pull --rebase origin main && git push && break
              sleep 3
            done
          fi

      - name: Send repository_dispatch til samt-bu-docs
        run: |
          curl -X POST \
            -H "Authorization: token ${{ secrets.DOCS_REBUILD_TOKEN }}" \
            -H "Accept: application/vnd.github.v3+json" \
            https://api.github.com/repos/SAMT-X/samt-bu-docs/dispatches \
            -d '{"event_type":"module-updated","client_payload":{"source":"<repo-navn>"}}'
```

Husk å bytte ut `<repo-navn>` med faktisk reponavn i siste linje.

### Steg 7 – Commit og push modulrepoet

```bash
git add go.mod content/ .github/
git commit -m "Hugo-modul init: <repo-navn> med innholdssider (nb+en)"
git push
```

### Steg 8 – Legg til `DOCS_REBUILD_TOKEN` secret

```bash
"/c/Program Files/GitHub CLI/gh.exe" secret set DOCS_REBUILD_TOKEN --repo SAMT-X/<repo-navn>
# Lim inn PAT-verdien (samme som i de andre modulrepoene) når du blir bedt om det
```

---

## Del 2 – Koble modulen til `samt-bu-docs`

Alle disse endringene gjøres i `S:/app-data/github/samt-x-repos/samt-bu-docs/`.

### Steg 9 – Legg til modulen i `hugo.toml`

Legg til en ny blokk under `[module]`:

```toml
[[module.imports]]
  path = "github.com/SAMT-X/<repo-navn>"
  [[module.imports.mounts]]
    source = "content"
    target = "content/teams/<repo-navn>"
```

Juster `target` til ønsket sti i nettstedet (f.eks. `content/teams/<repo-navn>/` for team-repoer).

### Steg 10 – Oppdater `go.mod`/`go.sum`

```bash
cd "S:/app-data/github/samt-x-repos/samt-bu-docs"
GONOSUMDB=* GOPROXY=direct hugo mod get github.com/SAMT-X/<repo-navn>@latest
```

### Steg 11 – Legg til checkout-steg i `hugo.yml`

I `.github/workflows/hugo.yml`, legg til en ny checkout-blokk etter de eksisterende modulrepo-checkout-stegene:

```yaml
- name: Checkout <repo-navn> module
  uses: actions/checkout@v4
  with:
    repository: SAMT-X/<repo-navn>
    path: .hugo-modules/<repo-navn>
    fetch-depth: 0
```

### Steg 12 – Legg til i `HUGO_MODULE_REPLACEMENTS`

I samme fil, under `HUGO_MODULE_REPLACEMENTS`, legg til på slutten (husk komma etter forrige linje):

```yaml
github.com/SAMT-X/<repo-navn> ->
${{ github.workspace }}/.hugo-modules/<repo-navn>
```

### Steg 13 – Legg til i `inject-lastmod.py`

I `.github/scripts/inject-lastmod.py`, legg til stien i `MODULE_PATHS`-listen:

```python
'.hugo-modules/<repo-navn>',
```

### Steg 14 – Verifiser lokalt og push

```bash
hugo  # Sjekk at det bygger uten feil
git add hugo.toml go.mod go.sum .github/workflows/hugo.yml .github/scripts/inject-lastmod.py
git commit -m "Ny Hugo-modul: <repo-navn> montert under teams/<repo-navn>"
git push
```

---

## Resultat

Etter neste CI-bygg vil innholdet fra modulrepoet være tilgjengelig på nettstedet. Videre push til modulrepoet vil automatisk trigge nybygg via `repository_dispatch`.

For å verifisere at alt er koblet riktig:
1. Gå til `https://github.com/SAMT-X/samt-bu-docs/actions` – se at et bygg startes
2. Åpne nettstedet og naviger til den nye seksjonen
3. Gjør en testendring i modulrepoet og sjekk at nettstedet oppdateres automatisk (~2 min)
