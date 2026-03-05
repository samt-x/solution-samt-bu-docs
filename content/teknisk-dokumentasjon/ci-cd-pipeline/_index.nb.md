---
title: "CI/CD-pipeline"
linkTitle: "CI/CD-pipeline"
weight: 20
---

Denne siden dokumenterer byggepipelinen som holder `samt-bu-docs`-nettstedet oppdatert – inkludert automatisk gjenbygging når innhold i eksterne modulrepoer endres.

---

## Oversikt

Nettstedet er bygget med Hugo og publisert til GitHub Pages via GitHub Actions. Innhold hentes fra flere repoer:

| Repo | Type | Trigget av endringer? |
|------|------|-----------------------|
| `samt-bu-docs` | Hoved-repo – konfigurasjon, lokalt innhold, CI/CD | ✅ Ja – direkte push |
| `samt-bu-drafts` | Hugo-modul – utkast og innspill | ✅ Ja – via `repository_dispatch` |
| `team-architecture` | Hugo-modul – arkitektur-teamets innhold | ✅ Ja – via `repository_dispatch` |
| `hugo-theme-samt-bu` | Git submodule – tema og layout | Nei – oppdateres manuelt via submodule-peker |

---

## Byggeworkflow (`hugo.yml`)

Filen `.github/workflows/hugo.yml` i `samt-bu-docs` gjør følgende ved triggering:

1. **Installerer Hugo** (versjon 0.155.3 extended)
2. **Sjekker ut** `samt-bu-docs` med full historikk og submoduler
3. **Sjekker ut modulrepoer** direkte (ikke via Go-modulcache):
   - `SAMT-X/team-architecture` → `.hugo-modules/team-architecture/`
   - `SAMT-X/samt-bu-drafts` → `.hugo-modules/samt-bu-drafts/`
4. **Injiserer `lastmod`** i modulinnhold via `inject-lastmod.py` (Git-historikk → frontmatter)
5. **Bygger med Hugo** med `HUGO_MODULE_REPLACEMENTS` som peker til lokale kloner
6. **Deployer** til GitHub Pages

Fordi modulrepoene sjekkes ut fresh ved hvert bygg, bruker CI alltid **siste HEAD** fra `main` – uavhengig av pinnet versjon i `go.mod`.

### Triggere

```yaml
on:
  push:
    branches: ["main"]       # Push til samt-bu-docs
  workflow_dispatch:          # Manuell kjøring fra GitHub UI
  repository_dispatch:
    types: [module-updated]  # Signal fra modulrepoer (se under)
```

---

## Kryssrepo-triggering (`repository_dispatch`)

Uten denne mekanismen: en redaktør redigerer en side via Decap CMS → commit til `samt-bu-drafts` → ingenting skjer i `samt-bu-docs` → nettsiden oppdateres ikke.

**Med mekanismen:** push til `samt-bu-drafts` (eller `team-architecture`) → trigger-workflow sender signal → `samt-bu-docs` starter nybygg automatisk.

### Slik fungerer det

**Steg 1 – Push til modulrepo** (f.eks. via Decap CMS-redigering):

```
Redaktør lagrer i CMS
  → Decap committer til samt-bu-drafts/main
  → ensure-uuids.yml kjøres (legger til id-felt)
  → trigger-docs-rebuild.yml kjøres
```

**Steg 2 – `trigger-docs-rebuild.yml`** (i `samt-bu-drafts` og `team-architecture`):

```yaml
- name: Send repository_dispatch til samt-bu-docs
  run: |
    curl -X POST \
      -H "Authorization: token ${{ secrets.DOCS_REBUILD_TOKEN }}" \
      -H "Accept: application/vnd.github.v3+json" \
      https://api.github.com/repos/SAMT-X/samt-bu-docs/dispatches \
      -d '{"event_type":"module-updated","client_payload":{"source":"samt-bu-drafts"}}'
```

**Steg 3 – `hugo.yml`** i `samt-bu-docs` trigges av `repository_dispatch` med type `module-updated` → fullt nybygg og deploy.

### Secret: `DOCS_REBUILD_TOKEN`

Workflowen bruker et GitHub Personal Access Token (Classic) med **`workflow`-scope**, lagret som Actions Secret i hvert modulrepo.

| Repo | Secretnavn | Verdi |
|------|------------|-------|
| `samt-bu-drafts` | `DOCS_REBUILD_TOKEN` | PAT med `workflow`-scope |
| `team-architecture` | `DOCS_REBUILD_TOKEN` | Samme PAT |

**Administrere tokenet:**
- Opprett/forny på: `https://github.com/settings/tokens`
- Sett secret: `gh secret set DOCS_REBUILD_TOKEN --repo SAMT-X/<repo>`
- Tokenet trenger **ikke** lagres etter at det er satt som secret

---

## Legge til et nytt modulrepo i pipelinen

Når et nytt Hugo-modulrepo skal kobles til `samt-bu-docs` slik at endringer der automatisk publiseres:

### 1. I modulrepoet – legg til trigger-workflow

Opprett `.github/workflows/trigger-docs-rebuild.yml`:

```yaml
name: Trigger rebuild av samt-bu-docs

on:
  push:
    branches: [main]

jobs:
  trigger:
    runs-on: ubuntu-latest
    steps:
      - name: Send repository_dispatch til samt-bu-docs
        run: |
          curl -X POST \
            -H "Authorization: token ${{ secrets.DOCS_REBUILD_TOKEN }}" \
            -H "Accept: application/vnd.github.v3+json" \
            https://api.github.com/repos/SAMT-X/samt-bu-docs/dispatches \
            -d '{"event_type":"module-updated","client_payload":{"source":"<repo-navn>"}}'
```

### 2. I modulrepoet – legg til secret

```bash
gh secret set DOCS_REBUILD_TOKEN --repo SAMT-X/<repo-navn>
# Lim inn PAT-verdien når du blir bedt om det
```

### 3. I `samt-bu-docs/hugo.yml` – legg til checkout av nytt repo

```yaml
- name: Checkout <repo-navn> module
  uses: actions/checkout@v4
  with:
    repository: SAMT-X/<repo-navn>
    path: .hugo-modules/<repo-navn>
    fetch-depth: 0
```

### 4. I `samt-bu-docs/hugo.yml` – legg til i `HUGO_MODULE_REPLACEMENTS`

```yaml
HUGO_MODULE_REPLACEMENTS: >-
  github.com/SAMT-X/team-architecture ->
  ${{ github.workspace }}/.hugo-modules/team-architecture,
  github.com/SAMT-X/samt-bu-drafts ->
  ${{ github.workspace }}/.hugo-modules/samt-bu-drafts,
  github.com/SAMT-X/<repo-navn> ->
  ${{ github.workspace }}/.hugo-modules/<repo-navn>
```

### 5. I `inject-lastmod.py` – legg til modulstien (valgfritt)

Hvis `Sist endret`-tidsstempler skal fungere for innholdet fra det nye repoet, legg til stien i `inject-lastmod.py`.

### 6. I `hugo.toml` – registrer modulen

```toml
[[module.imports]]
  path = "github.com/SAMT-X/<repo-navn>"
  [[module.imports.mounts]]
    source = "content"
    target = "content/<sti-i-nettstedet>/"
```

### 7. Oppdater `go.mod`/`go.sum`

```bash
GONOSUMDB=* GOPROXY=direct hugo mod get github.com/SAMT-X/<repo-navn>@latest
hugo  # Verifiser at det bygger
git add go.mod go.sum && git commit -m "Legg til <repo-navn> som Hugo-modul"
git push
```

---

## `inject-lastmod.py` – tidsstempler for modulinnhold

Hugo-moduler leveres som zip-arkiv uten Git-historikk, og `Sist endret`-datoen ville aldri vises. CI løser dette:

1. Modulrepoene sjekkes ut med `fetch-depth: 0` (full historikk)
2. `inject-lastmod.py` leser `git log -1 --format=%cI` for hver `.md`-fil
3. `lastmod: <ISO-tidsstempel>` skrives inn i frontmatter i CI-workspace
4. Endringen commites **ikke** – kun midlertidig før bygg

Gjelder per nå: `team-architecture` og `samt-bu-drafts`.

---

## Manuelt nybygg

Hvis noe er galt og du vil tvinge et nybygg uten å pushe kode:

1. Gå til: `https://github.com/SAMT-X/samt-bu-docs/actions/workflows/hugo.yml`
2. Klikk **Run workflow** → **Run workflow**

Eller via CLI:
```bash
"/c/Program Files/GitHub CLI/gh.exe" workflow run hugo.yml --repo SAMT-X/samt-bu-docs
```
