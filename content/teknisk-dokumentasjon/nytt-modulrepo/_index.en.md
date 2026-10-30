---
# id: auto-generated – copied values are overwritten automatically on push
id: ed2ee794-3c97-4e2d-959d-90b235a4f3d6
title: "Creating a new module repository – step by step"
linkTitle: "New module repo"
weight: 25
lastmod: 2026-10-25T23:08:04+01:00
last_editor: Erik Hagen

---

Guide for creating a new content repo and mounting it in the site as a Hugo module, from an empty repo to published content.

*Updated 2026-10-25 ([solution-samt-bu-docs#84](https://github.com/samt-x/solution-samt-bu-docs/issues/84)). How the build fits together is described on the page [CI/CD pipeline](../ci-cd-pipeline/).*

The work is done in three repos: the new module repo, `samt-bu-docs` and the theme `hugo-theme-samt-bu`.

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

---

## Part 3 – The theme

### Step 10 – Link the path to the repo

The theme has the link between path and repo written in directly, in seven places in four files in `themes/hugo-theme-samt-bu/layouts/partials/`:

| File | What |
|---|---|
| `edit-switcher.html` | The «Edit» menu (four places) |
| `header.html` | The source link at the top of the page |
| `menu.html` | New page from the menu |
| `custom-footer.html` | `SAMTBU_REPOS` and the suggestion list |

Copy the block for an existing module with the same kind of path, for example `pilot-4`. **If this is forgotten, «Edit» and the source link point to `samt-bu-docs`**, and editing in the browser does not work for the module.

### Step 11 – Check locally

```bash
hugo
```

Check that the pages in the module have `data-repo="<repo>"` and link to the right repo.

### Step 12 – Commit and push in the right order

1. Commit and push the theme.
2. Update the submodule pointer in `samt-bu-docs` (`git add themes/hugo-theme-samt-bu`).
3. Commit `hugo.toml`, `go.mod`, `go.sum`, `hugo.yml` and the submodule pointer, and push.

---

## Check that everything works

1. The build in `samt-bu-docs` is green (*Actions*).
2. The new section shows on the site, with «Last modified».
3. Save a small change in the module repo. The site should rebuild by itself, and the run in `samt-bu-docs` gets the commit message as its name.
4. «Edit this page» on a page in the module opens the right repo.
