---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: ed2ee794-3c97-4e2d-959d-90b235a4f3d6
title: "Opprette nytt modulrepo – steg-for-steg"
linkTitle: "Nytt modulrepo"
weight: 25
lastmod: 2026-11-15T16:36:30+01:00
last_editor: Erik Hagen

---

Veiledning for å opprette et nytt innholdsrepo og montere det i nettstedet som Hugo-modul, fra tomt repo til publisert innhold.

*Oppdatert 2026-10-25 ([solution-samt-bu-docs#84](https://github.com/samt-x/solution-samt-bu-docs/issues/84)). Hvordan byggingen henger sammen, står på siden [CI/CD-pipeline](../ci-cd-pipeline/).*

Arbeidet gjøres i to repoer: det nye modulrepoet og `samt-bu-docs`. Temaet `hugo-theme-samt-bu` trenger ingen endring (del 3).

---

## Forutsetninger

- Admin i GitHub-organisasjonen `samt-x`, for å opprette repoet og legge inn en secret
- Hugo (0.155.3 extended) og Go installert lokalt, og `gh` innlogget

Navn: `samt-bu-` for publisert innhold (for eksempel `samt-bu-pilot-6`), `team-` for team, `solution-` for dokumentasjon av en løsning.

---

## Del 1 – Modulrepoet

### Steg 1 – Opprett og klon repoet

Opprett repoet i `samt-x` med en `README.md`, og klon det inn i arbeidsmappen ved siden av de andre repoene.

Gi repoet topics etter [Konvensjoner](/prosjektleveranser/loesninger/samhandlingsplattform/oppgavestyring/konvensjoner/#navn-og-topics-på-repoer), for eksempel for en pilot: `gh repo edit samt-x/<repo> --add-topic project-samt-bu,scope-project,content,tasks,pilot`.

### Steg 2 – Gjør det til en Hugo-modul

```bash
hugo mod init github.com/SAMT-X/<repo>
```

Modulstien skrives med store bokstaver (`SAMT-X`), som for de andre modulene.

### Steg 3 – Lag startsidene

Lag `content/_index.nb.md` og `content/_index.en.md` med `title`, `linkTitle` og `weight`. Ikke sett `id`, det gjør CI.

### Steg 4 – Kopier `.github/` fra et eksisterende modulrepo

Kopier hele `.github/` fra et modulrepo med samme oppsett, for eksempel `samt-bu-pilot-6`:

- `.github/workflows/trigger-docs-rebuild.yml`
- `.github/scripts/ensure-uuids.py`
- `.github/scripts/inject-lastmod.py`

Bytt reponavnet i `--arg source '…'` i workflowen. Ikke skriv workflowen av fra dokumentasjonen, så du får siste versjon.

### Steg 5 – Secret og tilgang

- Huk av repoet i org-secreten `DOCS_REBUILD_TOKEN`: orgens *Settings → Secrets and variables → Actions* → `DOCS_REBUILD_TOKEN` → *Repository access* → tannhjulet. Du trenger ikke tokenen selv. Uten avhukingen bygges ikke nettstedet på nytt når noen lagrer i modulen, og dispatch-steget i workflowen blir rødt. Ikke legg secreten inn i repoet, for en repo-secret går foran org-secreten.
- Gi teamene samme tilgang som til de andre modulrepoene (*Settings → Collaborators and teams*).

### Steg 6 – Commit og push

Push til `main`. Workflowen legger inn `id`, `lastmod` og `last_editor` med automatiske commits, så hent dem (`git pull`) før du endrer mer.

---

## Del 2 – `samt-bu-docs`

### Steg 7 – Monter modulen i `hugo.toml`

```toml
[[module.imports]]
  path = "github.com/SAMT-X/<repo>"
  [[module.imports.mounts]]
    source = "content"
    target = "content/<sti-i-nettstedet>"
```

Stien bestemmer hvor innholdet havner, for eksempel `content/pilotering/pilot-6`. Ikke legg lokale filer under samme sti i `samt-bu-docs`. Lokale filer vinner over modulinnhold og skjuler det.

### Steg 8 – Hent modulen

```bash
hugo mod get github.com/SAMT-X/<repo>@latest
```

Dette oppdaterer `go.mod` og `go.sum`.

### Steg 9 – Legg modulen inn i `hugo.yml`

Legg til en linje i steget som henter modulene:

```bash
hent github.com/SAMT-X/<repo>@latest
```

Uten den bygger CI med versjonen i `go.mod`, ikke med siste versjon.

Legg også reponavnet inn i lista i steget «Hent innholdsrepoene» i `translations.yml`. Ellers blir modulen ikke sjekket for [oversettelse](../oversettelse/).

---

## Del 3 – Temaet

### Steg 10 – Ingenting å gjøre i temaet

Fra 14.11.2026 finner temaet repoet selv ([solution-samt-bu-docs#82](https://github.com/samt-x/solution-samt-bu-docs/issues/82)). Partialen `page-repo.html` leser stien til fila Hugo brukte. Moduler ligger i modulcachen som `…/<repo>@<versjon>/content/…`, lokale sider som `…/samt-bu-docs/content/…`. Resultatet brukes av «Endre»-menyen, kildelenken øverst på siden og modulmerket i menyen. Lista over repoer for forslagsbehandling (`SAMTBU_REPOS`) bygges fra modulene i `hugo.toml`.

Før dette måtte en ny modul legges inn på sju steder i fire filer i temaet. Ble det glemt, pekte «Endre» og kildelenken på feil repo.

En lokal fil under en modulsti får `samt-bu-docs` av seg selv, fordi lokal fil vinner i Hugo, og det er den fila som leses. Det skal likevel ikke finnes slike filer (se steg 7). Det siste tilfellet, Målbildet og Veikart under `arkitektur/overordnet-arkitektur/`, ble flyttet inn i `team-architecture` 15.11.2026. Finner temaet ikke mønsteret i stien, stopper bygget med en feilmelding i stedet for å rute til feil repo.

### Steg 11 – Sjekk lokalt

```bash
hugo
```

Sjekk at sidene i modulen har `"repo":"<repo>"` i `_samtbuThisPage` og kildelenke til riktig repo.

Push modulrepoet og kjør `hugo mod get` før du bygger lokalt. Lokal test med `HUGO_MODULE_REPLACEMENTS` har ikke virket på Windows, verken for nye eller eksisterende moduler.

### Steg 12 – Commit og push

Commit `hugo.toml`, `go.mod`, `go.sum` og `hugo.yml` i `samt-bu-docs`, og push.

---

## Sjekk at alt virker

1. Bygget i `samt-bu-docs` går grønt (*Actions*).
2. Den nye seksjonen vises på nettstedet, med «Sist endret».
3. Lagre en liten endring i modulrepoet. Nettstedet skal bygges på nytt av seg selv, og kjøringen i `samt-bu-docs` får commitmeldingen som navn.
4. «Endre denne siden» på en side i modulen åpner riktig repo.
