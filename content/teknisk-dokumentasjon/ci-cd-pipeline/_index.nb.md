---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: 9641ada5-80e0-4700-a6c6-0929fd961409
title: "CI/CD-pipeline"
linkTitle: "CI/CD-pipeline"
weight: 10
lastmod: 2026-03-27T23:29:13+01:00
last_editor: Erik Hagen

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
| `team-semantics` | Hugo-modul – semantikk-teamets innhold | ⚠ Ikke koblet (ingen trigger-workflow) |
| `team-pilot-1` | Hugo-modul – pilot 1-teamets innhold | ✅ Ja – via `repository_dispatch` |
| `solution-samt-bu-docs` | Hugo-modul – teknisk dokumentasjon for SAMT-BU Docs | ✅ Ja – via `repository_dispatch` |
| `hugo-theme-samt-bu` | Git submodule – tema og layout | Nei – oppdateres manuelt via submodule-peker |

---

## Byggeworkflow (`hugo.yml`)

Filen `.github/workflows/hugo.yml` i `samt-bu-docs` gjør følgende ved triggering:

1. **Installerer Hugo** (versjon 0.155.3 extended)
2. **Sjekker ut** `samt-bu-docs` med full historikk og submoduler
3. **Sjekker ut modulrepoer** direkte (ikke via Go-modulcache):
   - `SAMT-X/team-architecture` → `.hugo-modules/team-architecture/`
   - `SAMT-X/team-pilot-1` → `.hugo-modules/team-pilot-1/`
   - `SAMT-X/samt-bu-drafts` → `.hugo-modules/samt-bu-drafts/`
   - `SAMT-X/solution-samt-bu-docs` → `.hugo-modules/solution-samt-bu-docs/`
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

Uten denne mekanismen: en redaktør lagrer en side → commit til modulrepoet → ingenting skjer i `samt-bu-docs` → nettsiden oppdateres ikke.

**Med mekanismen:** push til et modulrepo → trigger-workflow sender signal → `samt-bu-docs` starter nybygg automatisk.

### Slik fungerer det

**Steg 1 – Push til modulrepo** (f.eks. via innebygd editor):

```
Redaktør lagrer siden
  → commit til modulrepo/main
  → ensure-uuids i trigger-docs-rebuild.yml kjøres (sikrer id-felt i frontmatter)
  → repository_dispatch sendes til samt-bu-docs
```

**Steg 2 – `trigger-docs-rebuild.yml`** (finnes i hvert modulrepo som er koblet):

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

**Steg 3 – `hugo.yml`** i `samt-bu-docs` trigges av `repository_dispatch` med type `module-updated` → fullt nybygg og deploy.

### Secret: `DOCS_REBUILD_TOKEN`

Workflowen bruker et GitHub Personal Access Token (Classic) med **`workflow`-scope**, lagret som Actions Secret i hvert modulrepo.

| Repo | Secretnavn | Verdi |
|------|------------|-------|
| `samt-bu-drafts` | `DOCS_REBUILD_TOKEN` | PAT med `workflow`-scope |
| `team-architecture` | `DOCS_REBUILD_TOKEN` | Samme PAT |
| `team-pilot-1` | `DOCS_REBUILD_TOKEN` | Samme PAT |
| `solution-samt-bu-docs` | `DOCS_REBUILD_TOKEN` | Samme PAT |

**Administrere tokenet:**
- Opprett/forny på: `https://github.com/settings/tokens`
- Sett secret: `gh secret set DOCS_REBUILD_TOKEN --repo SAMT-X/<repo>`
- Tokenet trenger **ikke** lagres etter at det er satt som secret

---

## Legge til et nytt modulrepo i pipelinen

Se den fullstendige veiledningen: [Opprette nytt modulrepo – steg-for-steg](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/veikart/nytt-modulrepo/).

Kortversjon – hva som må gjøres i `samt-bu-docs` når modulrepoet er klart:

### 1. I `hugo.toml` – registrer modulen

```toml
[[module.imports]]
  path = "github.com/SAMT-X/<repo-navn>"
  [[module.imports.mounts]]
    source = "content"
    target = "content/<sti-i-nettstedet>/"
```

### 2. Oppdater `go.mod`/`go.sum`

```bash
GONOSUMDB=* GOPROXY=direct hugo mod get github.com/SAMT-X/<repo-navn>@latest
```

### 3. I `hugo.yml` – legg til checkout-steg

```yaml
- name: Checkout <repo-navn> module
  uses: actions/checkout@v4
  with:
    repository: SAMT-X/<repo-navn>
    path: .hugo-modules/<repo-navn>
    fetch-depth: 0
```

### 4. I `hugo.yml` – legg til i `HUGO_MODULE_REPLACEMENTS`

Legg til på slutten av den eksisterende listen (husk komma etter forrige linje):

```yaml
github.com/SAMT-X/<repo-navn> ->
${{ github.workspace }}/.hugo-modules/<repo-navn>
```

### 5. I `inject-lastmod.py` – legg til modulstien

```python
'.hugo-modules/<repo-navn>',
```

---

## `inject-lastmod.py` – tidsstempler for modulinnhold

Hugo-moduler leveres som zip-arkiv uten Git-historikk, og `Sist endret`-datoen ville aldri vises. CI løser dette:

1. Modulrepoene sjekkes ut med `fetch-depth: 0` (full historikk)
2. `inject-lastmod.py` leser `git log -1 --format=%cI` for hver `.md`-fil
3. `lastmod: <ISO-tidsstempel>` skrives inn i frontmatter i CI-workspace
4. Endringen commites **ikke** – kun midlertidig før bygg

Gjelder per nå: `team-architecture`, `team-pilot-1`, `samt-bu-drafts` og `solution-samt-bu-docs`.

---

## Tilbakerulling – GUI vs. innhold

### Hvorfor temaendringer er trygge å rulle tilbake

Arkitekturen har en skarp separasjon mellom to uavhengige git-repoer:

| Hva | Repo | Inneholder |
|-----|------|------------|
| **GUI og logikk** | `hugo-theme-samt-bu` (submodule) | `custom-footer.html` (JS), `edit-switcher.html`, `custom-head.html` (CSS) |
| **Dokumentasjonsinnhold** | `samt-bu-docs`, `team-architecture`, `team-pilot-1`, `samt-bu-drafts`, `solution-samt-bu-docs` | Alle `.md`-filer |

Disse repoene deler ingen git-historikk. En `git revert` i temaet berører aldri innholdsrepoene – og omvendt. Det betyr at feilaktige GUI-endringer kan rulles tilbake på ~2 minutter uten at én linje innhold røres.

### Tilbakerullingsoppskrift (GUI/tema)

```bash
# 1. Reverter siste commit i temaet
cd "S:/app-data/github/samt-x-repos/samt-bu-docs/themes/hugo-theme-samt-bu"
git revert HEAD
git push

# 2. Oppdater submodule-pekeren i samt-bu-docs
cd "S:/app-data/github/samt-x-repos/samt-bu-docs"
git add themes/hugo-theme-samt-bu
git commit -m "Tema: tilbakestilt til forrige versjon"
git push
```

CI bygger og deployer → nettstedet er tilbake til forrige GUI-tilstand innen ~2 minutter.

### Den eneste reelle risikoen

At man ved en feil committer til en innholdsfil (`content/`) i stedet for en temafil. Dette er en menneskelig feil, ikke en arkitektonisk svakhet – og unngås ved å sjekke `git diff` og `git status` før commit.

---

## Manuelt nybygg

Hvis noe er galt og du vil tvinge et nybygg uten å pushe kode:

1. Gå til: `https://github.com/SAMT-X/samt-bu-docs/actions/workflows/hugo.yml`
2. Klikk **Run workflow** → **Run workflow**

Eller via CLI:
```bash
"/c/Program Files/GitHub CLI/gh.exe" workflow run hugo.yml --repo SAMT-X/samt-bu-docs
```
