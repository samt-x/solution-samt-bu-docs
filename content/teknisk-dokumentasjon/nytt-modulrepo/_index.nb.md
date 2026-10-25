---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: ed2ee794-3c97-4e2d-959d-90b235a4f3d6
title: "Opprette nytt modulrepo – steg-for-steg"
linkTitle: "Nytt modulrepo"
weight: 25
lastmod: 2026-03-28T10:01:46+01:00
last_editor: Erik Hagen

---

Veiledning for å opprette et nytt innholdsrepo og montere det i nettstedet som Hugo-modul, fra tomt repo til publisert innhold.

*Oppdatert 2026-10-25 ([solution-samt-bu-docs#84](https://github.com/samt-x/solution-samt-bu-docs/issues/84)). Hvordan byggingen henger sammen, står på siden [CI/CD-pipeline](../ci-cd-pipeline/).*

Arbeidet gjøres i tre repoer: det nye modulrepoet, `samt-bu-docs` og temaet `hugo-theme-samt-bu`.

---

## Forutsetninger

- Admin i GitHub-organisasjonen `samt-x`, for å opprette repoet og legge inn en secret
- Hugo (0.155.3 extended) og Go installert lokalt, og `gh` innlogget
- Tokenen for `DOCS_REBUILD_TOKEN` fra Bitwarden

Navn: `samt-bu-` for publisert innhold (for eksempel `samt-bu-pilot-6`), `team-` for team, `solution-` for dokumentasjon av en løsning.

---

## Del 1 – Modulrepoet

### Steg 1 – Opprett og klon repoet

Opprett repoet i `samt-x` med en `README.md`, og klon det inn i arbeidsmappen ved siden av de andre repoene.

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

- Legg inn secreten `DOCS_REBUILD_TOKEN` i repoets *Settings → Secrets and variables → Actions*, med tokenen fra Bitwarden. Uten den bygges ikke nettstedet på nytt når noen lagrer i modulen.
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

---

## Del 3 – Temaet

### Steg 10 – Koble stien til repoet

Temaet har sammenhengen mellom sti og repo skrevet inn direkte, på sju steder i fire filer i `themes/hugo-theme-samt-bu/layouts/partials/`:

| Fil | Hva |
|---|---|
| `edit-switcher.html` | «Endre»-menyen (fire steder) |
| `header.html` | Kildelenken øverst på siden |
| `menu.html` | Ny side fra menyen |
| `custom-footer.html` | `SAMTBU_REPOS` og forslagslisten |

Kopier blokken for en eksisterende modul med samme type sti, for eksempel `pilot-4`. **Glemmes dette, peker «Endre» og kildelenken til `samt-bu-docs`**, og redigering i nettleseren virker ikke for modulen.

### Steg 11 – Sjekk lokalt

```bash
hugo
```

Sjekk at sidene i modulen har `data-repo="<repo>"` og lenker til riktig repo.

### Steg 12 – Commit og push i riktig rekkefølge

1. Commit og push temaet.
2. Oppdater submodule-pekeren i `samt-bu-docs` (`git add themes/hugo-theme-samt-bu`).
3. Commit `hugo.toml`, `go.mod`, `go.sum`, `hugo.yml` og submodule-pekeren, og push.

---

## Sjekk at alt virker

1. Bygget i `samt-bu-docs` går grønt (*Actions*).
2. Den nye seksjonen vises på nettstedet, med «Sist endret».
3. Lagre en liten endring i modulrepoet. Nettstedet skal bygges på nytt av seg selv, og kjøringen i `samt-bu-docs` får commitmeldingen som navn.
4. «Endre denne siden» på en side i modulen åpner riktig repo.
