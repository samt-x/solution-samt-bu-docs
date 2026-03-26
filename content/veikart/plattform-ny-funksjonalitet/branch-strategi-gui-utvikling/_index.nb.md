---
id: 7aa3bf53-2226-4a6b-a3ca-6a80309577aa
title: "Branch-strategi for GUI-utvikling"
linkTitle: "Branch-strategi for GUI-utvikling"
weight: 120
status: "Ny"
last_editor: erikhag1git (Erik Hagen)
lastmod: 2026-03-16T23:56:44+01:00

---

Etter hvert som brukere tar nettstedet i bruk, bør aktiv GUI-utvikling skje i en separat branch slik at feil ikke forstyrrer produksjon. Inntil dette er satt opp, brukes `main` med rask tilbakerulling (se [CI/CD-pipeline](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/teknisk-dokumentasjon/ci-cd-pipeline/)).

## Foreslått oppsett

### Brancher

| Repo | Branch | Formål |
|------|--------|--------|
| `hugo-theme-samt-bu` | `dev` | GUI-endringer under utvikling |
| `samt-bu-docs` | `dev` | Peker på tema-`dev`, eventuelle konfig-endringer |

### Preview-URL

Cloudflare Pages bygger automatisk en preview-deploy for alle non-main branches:

```
dev.samt-bu-docs.pages.dev
```

Denne kan brukes til å teste hele edit-flyten (commit, build-polling, pending-indikator, OAuth) mot ekte GitHub – uten å berøre produksjonsinnhold på `main`.

## Komplikasjon: commit-branch i JS

JS-koden i `custom-footer.html` committer til `main` som målbranch. På `dev`-branchen bør test-commits gå til `dev`, ikke `main`. Løsning: injiser commit-branch som en Hugo-parameter fra `hugo.toml` eller som en CI-miljøvariabel, slik at riktig branch brukes automatisk avhengig av hvilken branch som bygger.

## Arbeidsflyt

1. Gjør endringer i `hugo-theme-samt-bu` på `dev`-branch
2. Commit og push → CF Pages bygger preview
3. Test hele edit-flyten på preview-URL
4. Merge `dev` → `main` i temaet når klar
5. Oppdater submodule-peker i `samt-bu-docs/main`

## Prioritet

Lav inntil videre – tilbakerullingsstrategien på `main` er tilstrekkelig for nåværende bruksmønster. Bør settes opp når GUI-endringene blir mer eksperimentelle eller brukerbasen vokser.
