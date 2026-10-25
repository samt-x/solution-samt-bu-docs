---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: 9641ada5-80e0-4700-a6c6-0929fd961409
title: "CI/CD-pipeline"
linkTitle: "CI/CD-pipeline"
weight: 10
lastmod: 2026-10-25T22:20:00+01:00
last_editor: Erik Hagen

---

Denne siden dokumenterer byggepipelinen som holder nettstedet oppdatert, også når innhold i modulrepoene endres.

*Gjennomgått og oppdatert 2026-10-25 ([solution-samt-bu-docs#84](https://github.com/samt-x/solution-samt-bu-docs/issues/84)).*

---

## Oversikt

Nettstedet bygges med Hugo i GitHub Actions og publiseres til Cloudflare Pages på `https://docs.samt-bu.no/`. Innholdet kommer fra flere repoer:

| Repo | Type | Starter nybygg? |
|------|------|-----------------|
| `samt-bu-docs` | Hovedrepo: konfigurasjon, lokalt innhold, CI | Ja, ved push |
| `team-architecture`, `team-semantics` | Hugo-moduler under Arkitektur | Ja, via `repository_dispatch` |
| `samt-bu-pilot-1` … `samt-bu-pilot-6` | Hugo-moduler, én per pilot | Ja, via `repository_dispatch` |
| `samt-bu-drafts`, `samt-bu-market-engagement` | Hugo-moduler: utkast og ekstern markedsdialog | Ja, via `repository_dispatch` |
| `solution-samt-bu-docs`, `solution-task-management` | Hugo-moduler: dokumentasjon av løsningene | Ja, via `repository_dispatch` |
| `hugo-theme-samt-bu` | Git submodule: tema og layout | Nei. Oppdateres via submodule-pekeren i `samt-bu-docs` |

Hvor hver modul monteres, står i `[[module.imports]]` i `hugo.toml`.

---

## Byggeworkflow (`hugo.yml`)

Filen `.github/workflows/hugo.yml` i `samt-bu-docs`:

1. **Installerer Hugo** (versjon 0.155.3 extended), med tre forsøk
2. **Sjekker ut** `samt-bu-docs` med full historikk og submoduler (temaet)
3. **Sikrer UUID-er** i frontmatter (bare ved push til `samt-bu-docs`)
4. **Henter siste versjon av hver modul** med `hugo mod get …@latest`, med tre forsøk per modul (funksjonen `hent`)
5. **Bygger med Hugo** via `.github/scripts/build-with-fallback.py`. Feiler bygget på én innholdsfil, settes fila til side og resten bygges (se [Når et bygg feiler](#når-et-bygg-feiler))
6. **Skriver byggkvitteringen** `/build.json` (`write-build-info.py`)
7. **Deployer** til Cloudflare Pages med `wrangler`, med tre forsøk
8. **Melder fra** på solution-samt-bu-docs#83 hvis en fil ble satt til side

Fordi modulene hentes med `@latest` ved hvert bygg, bruker CI alltid **siste versjon** fra `main`, uavhengig av versjonen i `go.mod`.

«Sist endret» for lokalt innhold kommer fra git-historikken (`enableGitInfo = true`). For modulinnhold står datoen i frontmatter (se [`inject-lastmod.py`](#inject-lastmodpy--sist-endret-for-modulinnhold)).

### Triggere

```yaml
on:
  push:
    branches: ["main"]       # Push til samt-bu-docs
  workflow_dispatch:          # Manuell kjøring fra GitHub
  repository_dispatch:
    types: [module-updated]  # Signal fra modulrepoene (se under)
```

Bare ett bygg kjører om gangen (`concurrency: pages`), og et bygg som kjører, avbrytes ikke. Venter flere, kjøres bare det siste. De andre vises som avløst, men endringene deres er med i det siste bygget.

### Byggkvitteringen (`/build.json`)

`write-build-info.py` skriver hvilke commits som er med i bygget, per repo. Nettleseren bruker den for å se når en lagret endring er publisert, og for å oppdage endringer som er satt til side (se under).

---

## Når et bygg feiler

Laget i [solution-samt-bu-docs#83](https://github.com/samt-x/solution-samt-bu-docs/issues/83). Før dette stoppet én ødelagt fil alle endringer, også andres, til noen rettet den. Hvordan brukeren opplever det, står i [brukerveiledningen for innebygd redigering](../../brukerveiledning/innebygd-redigering/#statusindikator-og-jobbhistorikk).

### Fila med feilen settes til side

Hugo stopper ved første feil og oppgir som regel fil, linje og kolonne. `build-with-fallback.py` kjører Hugo og leser feilmeldingen. Peker den på en innholdsfil (`content/…` i `samt-bu-docs` eller i en modul), skjer dette:

1. Skriptet finner **forrige publiserte versjon** av fila: commiten for repoet i den publiserte `/build.json`. Var fila satt til side allerede i forrige bygg, brukes `published_sha` derfra. Ellers ville neste bygg hentet den ødelagte versjonen.
2. Versjonen hentes med `git show` (`samt-bu-docs`) eller med GitHub-API-et (moduler), og skrives over fila **bare i dette bygget**. Ingenting committes.
3. Fantes ikke fila i forrige bygg, holdes den utenfor.
4. Bygget kjøres på nytt.

Det settes til side høyst tre filer per bygg. Feiler samme fil igjen, eller peker feilen på en mal, temaet eller konfigurasjonen, stopper bygget som før. Slike feil skal fanges før de kommer til `main` ([solution-samt-bu-docs#27](https://github.com/samt-x/solution-samt-bu-docs/issues/27)).

### Feil som ikke lenger stopper bygget

- **Ødelagte `relref`-lenker** gir en advarsel, ikke en feil (`refLinksErrorLevel = "WARNING"` i `hugo.toml`). Hugo oppgir bare sidestien for slike feil, ikke fila, så de kan ikke settes til side. Siden bygges med en død lenke.
- **`hugo mod get`** prøver tre ganger per modul, så en forbigående nettverksfeil ikke stopper bygget.

### Byggkvitteringen

`/build.json` har feltet `set_aside`, med én oppføring per fil som er satt til side:

```json
"set_aside": [
  {"repo": "samt-bu-docs", "path": "content/…/_index.nb.md", "published_sha": "002c5fb…"}
]
```

Nettleseren bruker feltet. Står brukerens commit i kvitteringen, men commiten endret en fil som er satt til side, vises «Endringen din kunne ikke publiseres» i stedet for «publisert» (`samtbuSetAsideFor` i temaets `custom-footer.html`).

### Melding på #83

Steget «Meld fra om filer satt til side» i `hugo.yml` skriver en kommentar på solution-samt-bu-docs#83 med fila, feilmeldingen og lenke til kjøringen. Hver fil meldes én gang. En skjult markør (`repo:sti@commit`) i kommentaren gjør at senere bygg ikke melder den samme feilen igjen. Mangler tokenen `BUILD_REPORT_TOKEN` (se [Secrets](#secrets)), hoppes steget over, og rapporten står bare i jobbsammendraget.

### Kvittering når noen melder fra

Knappen «Meld fra her» i nettleseren lenker til #83. `build-report-receipt.yml` i `solution-samt-bu-docs` svarer med en gang på nye kommentarer der. Svaret har takk, status for siste bygg, om et bygg pågår, og hvilke filer som er satt til side. Kommentarer fra boter og fra dem som følger opp, får ikke svar. De som følger opp, står i en liste i workflowen. Svaret postes med `GITHUB_TOKEN`, så det trengs ingen egen secret.

### Teste endringer i dette

Test på en egen gren der deploy-steget er fjernet, med en fil som er ødelagt med vilje, og kjør `gh workflow run hugo.yml --ref <gren>`. Merk at kommentarsteget skriver en ekte kommentar på #83. Slett grenen etterpå. Kvitteringen testes med en kommentar på #83 fra en konto som ikke står i lista i workflowen.

---

## Kryssrepo-triggering (`repository_dispatch`)

Uten denne mekanismen ville en lagring i et modulrepo ikke ført til noe nybygg, og nettstedet ville ikke blitt oppdatert.

**Med mekanismen:** push til et modulrepo → `trigger-docs-rebuild.yml` i modulrepoet → signal til `samt-bu-docs` → `hugo.yml` bygger på nytt.

Alle modulrepoene har `.github/workflows/trigger-docs-rebuild.yml` med disse stegene:

1. **Sjekker ut** repoet med full historikk (`fetch-depth: 0`), som `inject-lastmod.py` trenger.
2. **Sikrer UUID-er** i frontmatter (`ensure-uuids.py`). Endringer committes som «Auto: legg til manglende UUID-er i frontmatter [skip ci]».
3. **Setter «Sist endret»** (`inject-lastmod.py`, se under). Endringer committes som «Auto: oppdater lastmod i frontmatter [skip ci]».
4. **Sender `repository_dispatch`** til `samt-bu-docs` med typen `module-updated`. `client_payload` har reponavnet (`source`) og commitmeldingen (`message`), som vises som navn på kjøringen i `samt-bu-docs`.

Jobben hopper over push fra `github-actions[bot]`, så de automatiske commitene ikke starter nye runder. Hent workflowen fra et eksisterende modulrepo og bytt reponavnet i `source`. Ikke skriv den av fra denne siden.

Fordi modulrepoene får automatiske commits, må du alltid hente siste versjon (`git pull`) før du endrer noe lokalt.

---

## `inject-lastmod.py` – «Sist endret» for modulinnhold

Hugo-moduler hentes uten git-historikk, så Hugo kan ikke selv finne datoen for siste endring. Derfor skriver hvert modulrepo datoen inn i fila:

1. `inject-lastmod.py` finner siste commit for hver `.md`-fil som ikke er gjort av en bot.
2. `lastmod` (norsk tid) og `last_editor` (GitHub-brukernavn og navn) skrives inn i frontmatter. En eksisterende `last_editor` som ikke er en bot, beholdes.
3. Endringen committes i modulrepoet.

---

## Secrets

| Secret | Hvor | Hva | Utløper |
|---|---|---|---|
| `DOCS_REBUILD_TOKEN` | Hvert modulrepo | PAT på `samt-x-bot` som sender `repository_dispatch` til `samt-bu-docs`. Mangler den, feiler bare dette steget (401), og endringen kommer ut ved neste bygg. | Se Bitwarden |
| `BUILD_REPORT_TOKEN` | `samt-bu-docs` | Fine-grained token på `samt-x-bot`, bare *Issues: Read and write* på `solution-samt-bu-docs`. Brukes til meldingen på #83. | 2027-10-25 |
| `CF_API_TOKEN`, `CF_ACCOUNT_ID` | `samt-bu-docs` | Deploy til Cloudflare Pages | Se Cloudflare |

Tokenene ligger i Bitwarden. Sett eller bytt en secret i repoets *Settings → Secrets and variables → Actions*. Det krever admin på repoet.

---

## Legge til et nytt modulrepo

Kort fortalt:

1. **Modulrepoet:** `hugo mod init github.com/SAMT-X/<repo>`, `content/_index.nb.md` og `_index.en.md`. Kopier `.github/` (workflow og skript) fra et eksisterende modulrepo, og bytt reponavnet i workflowen. Legg inn secreten `DOCS_REBUILD_TOKEN`, og gi teamene tilgang som for de andre modulrepoene.
2. **`hugo.toml`** i `samt-bu-docs`: ny `[[module.imports]]`-blokk med `source = "content"` og `target = "content/<sti>/"`.
3. **`go.mod`/`go.sum`:** `hugo mod get github.com/SAMT-X/<repo>@latest`.
4. **`hugo.yml`:** ny linje `hent github.com/SAMT-X/<repo>@latest` i steget som henter moduler.
5. **Temaet:** sammenhengen mellom sti og repo er skrevet inn i `edit-switcher.html`, `header.html`, `menu.html` og `custom-footer.html`. Glemmes dette, peker «Endre» og kildelenken til feil repo.
6. **Sjekk** med et lokalt `hugo`-bygg at sidene i modulen lenker til riktig repo. Commit temaet, oppdater submodule-pekeren, og commit `hugo.toml`, `go.mod`, `go.sum` og `hugo.yml`.

Den detaljerte oppskriften står på siden [Opprette nytt modulrepo](../nytt-modulrepo/).

---

## Tilbakerulling – tema eller innhold

### Hvorfor temaendringer er trygge å rulle tilbake

Tema og innhold ligger i hvert sitt repo:

| Hva | Repo | Inneholder |
|-----|------|------------|
| **Utseende og logikk** | `hugo-theme-samt-bu` (submodule) | `custom-footer.html` (JavaScript), `edit-switcher.html`, `custom-head.html` (CSS) med flere |
| **Innhold** | `samt-bu-docs` og modulrepoene | Alle `.md`-filer |

Repoene deler ingen git-historikk. En `git revert` i temaet rører aldri innholdet, og omvendt. En feil i temaet kan derfor rulles tilbake på et par minutter uten at en eneste linje innhold endres.

### Slik ruller du tilbake temaet

```bash
# 1. Reverter siste commit i temaet
git -C samt-bu-docs/themes/hugo-theme-samt-bu revert HEAD
git -C samt-bu-docs/themes/hugo-theme-samt-bu push

# 2. Oppdater submodule-pekeren i samt-bu-docs
git -C samt-bu-docs add themes/hugo-theme-samt-bu
git -C samt-bu-docs commit -m "Tema: tilbakestilt til forrige versjon"
git -C samt-bu-docs push
```

CI bygger og deployer, og nettstedet har forrige utseende igjen innen et par minutter.

### Den eneste reelle risikoen

At man ved en feil committer en innholdsfil (`content/`) i stedet for en temafil. Det unngås ved å sjekke `git status` og `git diff` før commit.

---

## Manuelt nybygg

Slik starter du et nybygg uten å pushe noe:

1. Gå til `https://github.com/samt-x/samt-bu-docs/actions/workflows/hugo.yml`
2. Klikk **Run workflow** → **Run workflow**

Eller med `gh`:

```bash
gh workflow run hugo.yml --repo samt-x/samt-bu-docs
```
