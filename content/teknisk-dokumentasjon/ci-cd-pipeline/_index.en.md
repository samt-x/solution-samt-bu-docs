---
# id: auto-generated – copied values are overwritten automatically on push
id: 9641ada5-80e0-4700-a6c6-0929fd961409
title: "CI/CD pipeline"
linkTitle: "CI/CD pipeline"
weight: 10
lastmod: 2026-10-25T22:38:08+01:00
last_editor: Erik Hagen

---

This page documents the build pipeline that keeps the site up to date, also when content in the module repos changes.

*Reviewed and updated 2026-10-25 ([solution-samt-bu-docs#84](https://github.com/samt-x/solution-samt-bu-docs/issues/84)).*

---

## Overview

The site is built with Hugo in GitHub Actions and published to Cloudflare Pages at `https://docs.samt-bu.no/`. The content comes from several repos:

| Repo | Type | Starts a rebuild? |
|------|------|-------------------|
| `samt-bu-docs` | Main repo: configuration, local content, CI | Yes, on push |
| `team-architecture`, `team-semantics` | Hugo modules under Architecture | Yes, through `repository_dispatch` |
| `samt-bu-pilot-1` … `samt-bu-pilot-6` | Hugo modules, one per pilot | Yes, through `repository_dispatch` |
| `samt-bu-drafts`, `samt-bu-market-engagement` | Hugo modules: drafts and external market dialogue | Yes, through `repository_dispatch` |
| `solution-samt-bu-docs`, `solution-task-management` | Hugo modules: documentation of the solutions | Yes, through `repository_dispatch` |
| `hugo-theme-samt-bu` | Git submodule: theme and layout | No. Updated through the submodule pointer in `samt-bu-docs` |

Where each module is mounted is set in `[[module.imports]]` in `hugo.toml`.

---

## Build workflow (`hugo.yml`)

The file `.github/workflows/hugo.yml` in `samt-bu-docs`:

1. **Installs Hugo** (version 0.155.3 extended), with three attempts
2. **Checks out** `samt-bu-docs` with full history and submodules (the theme)
3. **Ensures UUIDs** in front matter (only on push to `samt-bu-docs`)
4. **Fetches the latest version of each module** with `hugo mod get …@latest`, with three attempts per module (the function `hent`)
5. **Builds with Hugo** through `.github/scripts/build-with-fallback.py`. If the build fails on one content file, the file is set aside and the rest is built (see [When a build fails](#when-a-build-fails))
6. **Writes the build receipt** `/build.json` (`write-build-info.py`)
7. **Deploys** to Cloudflare Pages with `wrangler`, with three attempts
8. **Reports** on solution-samt-bu-docs#83 if a file was set aside

Because the modules are fetched with `@latest` in every build, CI always uses the **latest version** from `main`, regardless of the version in `go.mod`.

«Last modified» for local content comes from the git history (`enableGitInfo = true`). For module content the date is in the front matter (see [`inject-lastmod.py`](#inject-lastmodpy--last-modified-for-module-content)).

### Triggers

```yaml
on:
  push:
    branches: ["main"]       # Push to samt-bu-docs
  workflow_dispatch:          # Manual run from GitHub
  repository_dispatch:
    types: [module-updated]  # Signal from the module repos (see below)
```

Only one build runs at a time (`concurrency: pages`), and a running build is not cancelled. If several are waiting, only the last one runs. The others are shown as superseded, but their changes are included in the last build.

### The build receipt (`/build.json`)

`write-build-info.py` writes which commits are included in the build, per repo. The browser uses it to see when a saved change is published, and to detect changes that were set aside (see below).

---

## When a build fails

Built in [solution-samt-bu-docs#83](https://github.com/samt-x/solution-samt-bu-docs/issues/83). Before this, one broken file stopped every change, including other people's, until someone fixed it. What the user sees is described in the [user guide for inline editing](../../brukerveiledning/innebygd-redigering/#status-indicator-and-build-history).

### The failing file is set aside

Hugo stops at the first error and usually gives the file, line and column. `build-with-fallback.py` runs Hugo and reads the error message. If it points to a content file (`content/…` in `samt-bu-docs` or in a module):

1. The script finds the **previously published version** of the file: the commit for the repo in the published `/build.json`. If the file was already set aside in the previous build, `published_sha` from there is used. Otherwise the next build would fetch the broken version.
2. That version is fetched with `git show` (`samt-bu-docs`) or the GitHub API (modules) and written over the file **for this build only**. Nothing is committed.
3. If the file did not exist in the previous build, it is left out.
4. The build runs again.

At most three files are set aside per build. If the same file fails again, or the error points to a template, the theme or the configuration, the build stops as before. Such errors should be caught before they reach `main` ([solution-samt-bu-docs#27](https://github.com/samt-x/solution-samt-bu-docs/issues/27)).

### Errors that no longer stop the build

- **Broken `relref` links** give a warning, not an error (`refLinksErrorLevel = "WARNING"` in `hugo.toml`). Hugo only gives the page path for these errors, not the file, so they cannot be set aside. The page is built with a dead link.
- **`hugo mod get`** tries three times per module, so a passing network error does not stop the build.

### The build receipt

`/build.json` has the field `set_aside`, with one entry per file that was set aside:

```json
"set_aside": [
  {"repo": "samt-bu-docs", "path": "content/…/_index.nb.md", "published_sha": "002c5fb…"}
]
```

The browser uses this field. If the user's commit is in the receipt, but the commit changed a file that was set aside, the message «Your change could not be published» is shown instead of «published» (`samtbuSetAsideFor` in the theme's `custom-footer.html`).

### Report on #83

The step «Meld fra om filer satt til side» in `hugo.yml` writes a comment on solution-samt-bu-docs#83 with the file, the error message and a link to the run. Each file is reported once. A hidden marker (`repo:path@commit`) in the comment keeps later builds from reporting the same error again. If the token `BUILD_REPORT_TOKEN` is missing (see [Secrets](#secrets)), the step is skipped and the report is only in the job summary.

### Receipt when someone reports

The button «Report it here» in the browser links to #83. `build-report-receipt.yml` in `solution-samt-bu-docs` replies right away to new comments there. The reply has thanks, the status of the latest build, whether a build is running, and which files are set aside. Comments from bots and from the people who follow up get no reply. The people who follow up are listed in the workflow. The reply is posted with `GITHUB_TOKEN`, so no separate secret is needed.

### Testing changes to this

Test on a separate branch where the deploy step is removed, with a file that is broken on purpose, and run `gh workflow run hugo.yml --ref <branch>`. Note that the report step writes a real comment on #83. Delete the branch afterwards. Test the receipt with a comment on #83 from an account that is not in the list in the workflow.

---

## Cross-repo triggering (`repository_dispatch`)

Without this mechanism, a save in a module repo would not start a rebuild, and the site would not be updated.

**With the mechanism:** push to a module repo → `trigger-docs-rebuild.yml` in the module repo → signal to `samt-bu-docs` → `hugo.yml` builds again.

All the module repos have `.github/workflows/trigger-docs-rebuild.yml` with these steps:

1. **Checks out** the repo with full history (`fetch-depth: 0`), which `inject-lastmod.py` needs.
2. **Ensures UUIDs** in front matter (`ensure-uuids.py`). Changes are committed as «Auto: legg til manglende UUID-er i frontmatter [skip ci]».
3. **Sets «Last modified»** (`inject-lastmod.py`, see below). Changes are committed as «Auto: oppdater lastmod i frontmatter [skip ci]».
4. **Sends `repository_dispatch`** to `samt-bu-docs` with the type `module-updated`. `client_payload` has the repo name (`source`) and the commit message (`message`), which is shown as the name of the run in `samt-bu-docs`.

The job skips pushes from `github-actions[bot]`, so the automatic commits do not start new rounds. Copy the workflow from an existing module repo and change the repo name in `source`. Do not copy it from this page.

Because the module repos get automatic commits, always fetch the latest version (`git pull`) before changing anything locally.

---

## `inject-lastmod.py` – «Last modified» for module content

Hugo modules are fetched without git history, so Hugo cannot find the date of the last change by itself. Each module repo therefore writes the date into the file:

1. `inject-lastmod.py` finds the latest commit for each `.md` file that was not made by a bot.
2. `lastmod` (Norwegian time) and `last_editor` (GitHub user name and name) are written into the front matter. An existing `last_editor` that is not a bot is kept.
3. The change is committed in the module repo.

---

## Secrets

| Secret | Where | What | Expires |
|---|---|---|---|
| `DOCS_REBUILD_TOKEN` | **Organization secret** in `samt-x`, shared with the twelve module repos (*Selected repositories*) | Fine-grained token on `samt-x-bot`, only *Contents: Read and write* on `samt-bu-docs`, which is what `repository_dispatch` requires. If a repo lacks it, the dispatch step fails (red), and the change goes out with the next build. | 2027-10-25 |
| `BUILD_REPORT_TOKEN` | `samt-bu-docs` | Fine-grained token on `samt-x-bot`, only *Issues: Read and write* on `solution-samt-bu-docs`. Used for the report on #83. | 2027-10-25 |
| `CF_API_TOKEN`, `CF_ACCOUNT_ID` | `samt-bu-docs` | Deploy to Cloudflare Pages | See Cloudflare |

The tokens are kept in Bitwarden. `DOCS_REBUILD_TOKEN` is replaced in the organization's *Settings → Secrets and variables → Actions*, the others in the repo's. This requires admin. Do not add `DOCS_REBUILD_TOKEN` to a single repo: a repo secret takes precedence over the organization secret with the same name.

---

## Adding a new module repo

In short:

1. **The module repo:** `hugo mod init github.com/SAMT-X/<repo>`, `content/_index.nb.md` and `_index.en.md`. Copy `.github/` (workflow and scripts) from an existing module repo, and change the repo name in the workflow. Tick the repo in the organization secret `DOCS_REBUILD_TOKEN`, and give the teams access as for the other module repos.
2. **`hugo.toml`** in `samt-bu-docs`: a new `[[module.imports]]` block with `source = "content"` and `target = "content/<path>/"`.
3. **`go.mod`/`go.sum`:** `hugo mod get github.com/SAMT-X/<repo>@latest`.
4. **`hugo.yml`:** a new line `hent github.com/SAMT-X/<repo>@latest` in the step that fetches modules.
5. **The theme:** the link between path and repo is written into `edit-switcher.html`, `header.html`, `menu.html` and `custom-footer.html`. If this is forgotten, «Edit» and the source link point to the wrong repo.
6. **Check** with a local `hugo` build that the pages in the module link to the right repo. Commit the theme, update the submodule pointer, and commit `hugo.toml`, `go.mod`, `go.sum` and `hugo.yml`.

The detailed recipe is on the page [Create a new module repo](../nytt-modulrepo/).

---

## Rolling back – theme or content

### Why theme changes are safe to roll back

Theme and content are in separate repos:

| What | Repo | Contains |
|-----|------|------------|
| **Look and logic** | `hugo-theme-samt-bu` (submodule) | `custom-footer.html` (JavaScript), `edit-switcher.html`, `custom-head.html` (CSS) and more |
| **Content** | `samt-bu-docs` and the module repos | All `.md` files |

The repos share no git history. A `git revert` in the theme never touches the content, and the other way round. An error in the theme can therefore be rolled back in a couple of minutes without changing a single line of content.

### How to roll back the theme

```bash
# 1. Revert the latest commit in the theme
git -C samt-bu-docs/themes/hugo-theme-samt-bu revert HEAD
git -C samt-bu-docs/themes/hugo-theme-samt-bu push

# 2. Update the submodule pointer in samt-bu-docs
git -C samt-bu-docs add themes/hugo-theme-samt-bu
git -C samt-bu-docs commit -m "Tema: tilbakestilt til forrige versjon"
git -C samt-bu-docs push
```

CI builds and deploys, and the site has its previous look again within a couple of minutes.

### The only real risk

Committing a content file (`content/`) by mistake instead of a theme file. Avoid it by checking `git status` and `git diff` before you commit.

---

## Manual rebuild

To start a rebuild without pushing anything:

1. Go to `https://github.com/samt-x/samt-bu-docs/actions/workflows/hugo.yml`
2. Click **Run workflow** → **Run workflow**

Or with `gh`:

```bash
gh workflow run hugo.yml --repo samt-x/samt-bu-docs
```
