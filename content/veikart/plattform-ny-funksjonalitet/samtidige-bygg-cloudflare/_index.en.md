---
id: 7a4bb610-b4ef-416a-855a-ab251a5eff45
title: "Enabling concurrent builds through Cloudflare Pages"
linkTitle: "Concurrent builds via Cloudflare"
weight: 92
status: "In progress"
lastmod: 2026-03-20T09:42:59+01:00
last_editor: Erik Hagen
---

GitHub Pages automatically cancels older queued builds when a newer, higher-priority build is waiting («Canceling since a higher priority waiting request for pages exists»). This means that with three or more rapid saves in sequence, only the last build will complete – the intermediate ones are cancelled.

Cloudflare Pages native build with Git integration supports up to 6 concurrent builds (Workers Paid plan).

## What has been done (session 13, 2026-03-19)

### Alternative B implemented ✅

`lastmod` injection has been moved into the module repos:

- `inject-lastmod.py` created in all 4 module repos (team-architecture, samt-bu-drafts, solution-samt-bu-docs, team-pilot-1) under `.github/scripts/`
- `trigger-docs-rebuild.yml` in all 4 module repos updated: `fetch-depth: 0` + new inject-lastmod step that commits with `[skip ci]`
- Bot commits are skipped when determining the lastmod timestamp (new `get_lastmod` logic)
- `hugo.yml` in samt-bu-docs simplified: removed multi-repo checkout, inject-lastmod, and `HUGO_MODULE_REPLACEMENTS`
- Replaced with `hugo mod get @latest` + `hugo mod tidy` for all modules – fetches the latest version including injected lastmod directly from the Go module proxy
- `build.sh` created in the samt-bu-docs root – ready for CF Pages native build

### Partially resolved: cancel-in-progress ✅

`concurrency: cancel-in-progress: false` → `true` in `hugo.yml`. Resolves the queue problem in practice:
- 4 rapid edits → 3 cancelled, 1 builds (all changes included in the single build)
- Tested and confirmed: ~1 minute build time (significantly faster than before)
- Applies to all users – builds from different GitHub users are combined in the same way

### Blocked: CF Pages Git integration ❌

CF Pages does not support adding Git integration to an existing Direct Upload project:
- The `settings/builds-deployments` dashboard page crashes with «Refresh the page to try again» for Direct Upload projects
- The CF API does not expose the GitHub OAuth connection (`/pages/git/github/installations` → 404)
- Build config and env vars were set via API (✅), but Git connection requires a new project

### CF Pages configuration set via API ✅

The following is already configured on the existing `samt-bu-docs` project:
- Build command: `bash build.sh`
- Output directory: `public`
- Env vars (production + preview): `HUGO_VERSION=0.155.3`, `HUGO_ENVIRONMENT=production`, `TZ=Europe/Oslo`, `GONOSUMDB=*`, `GOPROXY=direct`

## Remaining steps for full implementation

### Step 1 – Create a new CF Pages project with Git integration

Can be done in parallel while the existing site continues to work on `samt-bu-docs.pages.dev`.

1. Go to [CF Pages → Create application → Pages → Connect to Git](https://dash.cloudflare.com/11cfadda66cca20b7736f23e40a070ef/workers-and-pages/create/pages/setup)
2. Select **SAMT-X/samt-bu-docs**, branch **main**
3. Build command: `bash build.sh`, output: `public`
4. Env vars: `HUGO_VERSION=0.155.3`, `HUGO_ENVIRONMENT=production`, `TZ=Europe/Oslo`, `GONOSUMDB=*`, `GOPROXY=direct`
5. Enable **«Include Git submodules»**
6. Give a temporary name, e.g. `samt-bu-docs-git`

### Step 2 – Create a deploy hook and add as a GitHub secret

- CF Pages → samt-bu-docs-git → Settings → Deploy hooks → Create hook (`github-actions`, branch `main`)
- Add URL as secret `CF_PAGES_DEPLOY_HOOK` in SAMT-X/samt-bu-docs

### Step 3 – Update hugo.yml

Change the `trigger-cf-pages` job (repository_dispatch) to use the deploy hook instead of wrangler deploy. The entire wrangler deploy step can be removed from the `build` job once CF native build is verified.

### Step 4 – Rename project

- Rename `samt-bu-docs` → `samt-bu-docs-old` (or delete)
- Rename `samt-bu-docs-git` → `samt-bu-docs`
- The subdomain `samt-bu-docs.pages.dev` follows the project name automatically

## Important clarification: Workers Paid ≠ Direct Upload

The Workers Paid plan's «6 concurrent build slots» apply **only to CF-side native builds** (Git integration). Direct Upload (`wrangler pages deploy`) does not use these slots – builds happen in GitHub Actions. Purchasing Workers Paid therefore has no effect on the Direct Upload flow.

## Related

- `samt-bu-docs/.github/workflows/hugo.yml` – current build and deploy flow
- `samt-bu-docs/build.sh` – ready for CF native build
- Roadmap: [Status reporting and build queues](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/veikart/statusrapportering-gui/)
- Roadmap: [False build failure on timeout](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/veikart/bygg-feil-timeout/)
