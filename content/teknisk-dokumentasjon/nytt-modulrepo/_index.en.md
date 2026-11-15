---
# id: auto-generated – copied values are overwritten automatically on push
id: ed2ee794-3c97-4e2d-959d-90b235a4f3d6
title: "Creating a new module repository – step by step"
linkTitle: "New module repo"
weight: 25
lastmod: 2026-11-14T23:30:24+01:00
last_editor: Erik Hagen

---

Guide for creating a new content repo and mounting it in the site as a Hugo module, from an empty repo to published content.

*Updated 2026-10-25 ([solution-samt-bu-docs#84](https://github.com/samt-x/solution-samt-bu-docs/issues/84)). How the build fits together is described on the page [CI/CD pipeline](../ci-cd-pipeline/).*

The work is done in two repos: the new module repo and `samt-bu-docs`. The theme `hugo-theme-samt-bu` needs no change (part 3).

---

## Prerequisites

- Admin in the GitHub organization `samt-x`, to create the repo and add a secret
- Hugo (0.155.3 extended) and Go installed locally, and `gh` signed in

Names: `samt-bu-` for published content (for example `samt-bu-pilot-6`), `team-` for teams, `solution-` for documentation of a solution.

---

## Part 1 – The module repo

### Step 1 – Create and clone the repo

Create the repo in `samt-x` with a `README.md`, and clone it into the working folder next to the other repos.

Give the repo topics following [Conventions](/en/prosjektleveranser/loesninger/samhandlingsplattform/oppgavestyring/konvensjoner/#repository-names-and-topics), for example for a pilot: `gh repo edit samt-x/<repo> --add-topic project-samt-bu,scope-project,content,tasks,pilot`.

### Step 2 – Make it a Hugo module

```bash
hugo mod init github.com/SAMT-X/<repo>
```

The module path is written in capitals (`SAMT-X`), like the other modules.

### Step 3 – Create the start pages

Create `content/_index.nb.md` and `content/_index.en.md` with `title`, `linkTitle` and `weight`. Do not set `id`; CI does that.

### Step 4 – Copy `.github/` from an existing module repo

Copy all of `.github/` from a module repo with the same setup, for example `samt-bu-pilot-6`:

- `.github/workflows/trigger-docs-rebuild.yml`
- `.github/scripts/ensure-uuids.py`
- `.github/scripts/inject-lastmod.py`

Change the repo name in `--arg source '…'` in the workflow. Do not copy the workflow from the documentation, so that you get the latest version.

### Step 5 – Secret and access

- Tick the repo in the organization secret `DOCS_REBUILD_TOKEN`: the organization's *Settings → Secrets and variables → Actions* → `DOCS_REBUILD_TOKEN` → *Repository access* → the gear. You do not need the token itself. Without it the site is not rebuilt when someone saves in the module, and the dispatch step in the workflow turns red. Do not add the secret to the repo, since a repo secret takes precedence over the organization secret.
- Give the teams the same access as to the other module repos (*Settings → Collaborators and teams*).

### Step 6 – Commit and push

Push to `main`. The workflow adds `id`, `lastmod` and `last_editor` with automatic commits, so fetch them (`git pull`) before you change anything else.

---

## Part 2 – `samt-bu-docs`

### Step 7 – Mount the module in `hugo.toml`

```toml
[[module.imports]]
  path = "github.com/SAMT-X/<repo>"
  [[module.imports.mounts]]
    source = "content"
    target = "content/<path-in-the-site>"
```

The path decides where the content ends up, for example `content/pilotering/pilot-6`. Do not put local files under the same path in `samt-bu-docs`. Local files win over module content and hide it.

### Step 8 – Fetch the module

```bash
hugo mod get github.com/SAMT-X/<repo>@latest
```

This updates `go.mod` and `go.sum`.

### Step 9 – Add the module to `hugo.yml`

Add a line in the step that fetches the modules:

```bash
hent github.com/SAMT-X/<repo>@latest
```

Without it CI builds with the version in `go.mod`, not with the latest version.

Also add the repository name to the list in the step «Hent innholdsrepoene» in `translations.yml`. Otherwise the module is not checked for [translation](/en/prosjektleveranser/loesninger/samhandlingsplattform/samt-bu-docs/teknisk-dokumentasjon/oversettelse/).

---

## Part 3 – The theme

### Step 10 – Nothing to do in the theme

From 14 November 2026 the theme finds the repo by itself ([solution-samt-bu-docs#82](https://github.com/samt-x/solution-samt-bu-docs/issues/82)). The partial `page-repo.html` reads the path of the file Hugo used. Modules live in the module cache as `…/<repo>@<version>/content/…`, local pages as `…/samt-bu-docs/content/…`. The result is used by the «Edit» menu, the source link at the top of the page and the module marker in the menu. The list of repos for handling suggestions (`SAMTBU_REPOS`) is built from the modules in `hugo.toml`.

Before this, a new module had to be added in seven places in four files in the theme. If that was forgotten, «Edit» and the source link pointed to the wrong repo.

A local file under a module path gets `samt-bu-docs` by itself, because a local file wins in Hugo, and that is the file that is read. There should still be no such files (see step 7). The last case, Target Architecture and Roadmap under `arkitektur/overordnet-arkitektur/`, was moved into `team-architecture` on 15 November 2026. If the theme does not find the pattern in the path, the build stops with an error message instead of routing to the wrong repo.

### Step 11 – Check locally

```bash
hugo
```

Check that the pages in the module have `"repo":"<repo>"` in `_samtbuThisPage` and a source link to the right repo.

Push the module repo and run `hugo mod get` before building locally. Local testing with `HUGO_MODULE_REPLACEMENTS` has not worked on Windows, neither for new nor for existing modules.

### Step 12 – Commit and push

Commit `hugo.toml`, `go.mod`, `go.sum` and `hugo.yml` in `samt-bu-docs`, and push.

---

## Check that everything works

1. The build in `samt-bu-docs` is green (*Actions*).
2. The new section shows on the site, with «Last modified».
3. Save a small change in the module repo. The site should rebuild by itself, and the run in `samt-bu-docs` gets the commit message as its name.
4. «Edit this page» on a page in the module opens the right repo.
