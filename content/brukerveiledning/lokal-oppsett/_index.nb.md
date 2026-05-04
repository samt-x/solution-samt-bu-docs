---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: "e26cb201-0841-46b2-8ac7-2ba3708edde6"
title: Lokalt oppsett
weight: 30
aliases:
  - /om/hvordan-bidra/lokal-oppsett/
  - /hvordan-bidra/lokal-oppsett/
lastmod: 2026-05-04T22:59:22+02:00
last_editor: Erik Hagen

---

Dette alternativet gir deg et fullt lokalt arbeidsmiljø der du kan forhåndsvise alle endringer i nettleseren mens du skriver. Anbefalt for strukturelle endringer, nytt innhold i større omfang eller teknisk utvikling.

## Hva du trenger

| Verktøy | Versjon | Formål |
| --- | --- | --- |
| [Git](https://git-scm.com/) | Siste stabile | Versjonskontroll |
| [Hugo Extended](https://gohugo.io/) | 0.155.3 eller nyere | Nettstedsgenerator |
| [Go](https://go.dev/) | 1.21 eller nyere | Kreves av Hugo Modules |
| Teksteditor | – | [VS Code](https://code.visualstudio.com/) anbefales |

## Installasjon på Windows

```powershell
winget install --id Git.Git
winget install --id Hugo.Hugo.Extended
winget install --id GoLang.Go
winget install --id Microsoft.VisualStudioCode
```

Start terminalen på nytt etterpå, slik at de nye programmene er tilgjengelige i PATH.

**Verifiser installasjonen:**

```powershell
git --version
hugo version
go version
```

## Installasjon på macOS

```bash
brew install git hugo go
```

## Installasjon på Linux (Ubuntu/Debian)

```bash
sudo apt install git golang
# Hugo Extended hentes fra GitHub Releases (apt-versjonen er ofte for gammel):
wget https://github.com/gohugoio/hugo/releases/download/v0.155.3/hugo_extended_0.155.3_linux-amd64.deb
sudo dpkg -i hugo_extended_0.155.3_linux-amd64.deb
```

## Innholdsstruktur – flere repos

SAMT-BU Docs er satt opp med **innholdsmoduler**: innhold fra ulike team og piloter ligger i egne GitHub-repoer og monteres automatisk inn i nettstedet ved publisering.

| Repo | Innhold | Montert under |
| --- | --- | --- |
| `samt-bu-docs` | Hoveddokumentasjon, konfigurasjon | *(rot)* |
| `samt-bu-pilot-1` | Pilot 1 | `pilotering/pilot-1/` |
| `samt-bu-pilot-2` | Pilot 2 | `pilotering/pilot-2/` |
| `samt-bu-pilot-3` | Pilot 3 | `pilotering/pilot-3/` |
| `samt-bu-pilot-4` | Pilot 4 | `pilotering/pilot-4/` |
| `team-architecture` | Overordnet arkitektur | `arkitektur/overordnet-arkitektur/` |
| `team-semantics` | Informasjonsarkitektur | `arkitektur/informasjonsarkitektur/` |
| `samt-bu-drafts` | Utkast og innspill | `utkast/` |
| `solution-samt-bu-docs` | Teknisk dokumentasjon | `prosjektleveranser/…` |

## Scenario A – Kun forhåndsvisning av hele nettstedet

```bash
git clone --recurse-submodules https://github.com/SAMT-X/samt-bu-docs.git
cd samt-bu-docs
hugo server
```

Åpne <http://localhost:1313/> i nettleseren.

## Scenario B – Redigere innhold i ett bestemt repo

```bash
git clone https://github.com/SAMT-X/samt-bu-pilot-2.git
cd samt-bu-pilot-2
# rediger filer i content/
git add .
git commit -m "Beskrivelse av endringen"
git push
```

Nettstedet oppdateres automatisk innen ca. ett minutt.

## Scenario C – Full lokal utvikling på tvers av alle repos

```bash
git clone --recurse-submodules https://github.com/SAMT-X/samt-bu-docs.git
git clone https://github.com/SAMT-X/samt-bu-pilot-1.git
# ... osv. for de modulene du vil jobbe med

cd samt-bu-docs
tools/hugo-local.sh
```

Scriptet finner lokale kloner automatisk og starter Hugo med disse. Moduler du ikke har klonet hentes fra GitHub.

```
samt-bu-docs/            ← klon alltid denne
samt-bu-pilot-1/         ← klon de du vil redigere
...
```

**Med utkast:**

```bash
tools/hugo-local.sh --drafts
```

## Skrive innhold

```markdown
---
title: "Sidetittel"
weight: 30
---

Her begynner innholdet ditt i vanlig Markdown.
```

- `title` – sidetittel som vises i menyen og øverst på siden
- `weight` – sorteringsrekkefølge (lavere tall = høyere opp i menyen)
- `draft: true` – skjuler siden fra publisering inntil den er klar

## Lagre og publisere endringer

```bash
git add content/sti/til/filen/_index.nb.md
git commit -m "Kort beskrivelse av hva du endret"
git pull --rebase
git push
```

GitHub Actions bygger og publiserer automatisk etter 1–2 minutter.

> **Uten skrivetilgang?** Opprett en branch og pull request: `git checkout -b mitt-bidrag` → gjør endringer → `git push origin mitt-bidrag` → åpne PR på GitHub.

## Nyttige kommandoer

| Kommando | Beskrivelse |
| --- | --- |
| `tools/hugo-local.sh` | Start lokal server med automatisk modulerstatning |
| `tools/hugo-local.sh --drafts` | Inkluder også utkast |
| `hugo server` | Start lokal server (henter moduler fra GitHub) |
| `hugo` | Bygg til `public/` (sjekk for feil) |
| `git pull --rebase` | Hent siste endringer og rebase |
