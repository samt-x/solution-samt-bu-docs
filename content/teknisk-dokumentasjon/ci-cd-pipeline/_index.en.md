---
# id: auto-generated – copied values are overwritten automatically on push
id: 9641ada5-80e0-4700-a6c6-0929fd961409
title: "CI/CD pipeline"
linkTitle: "CI/CD pipeline"
weight: 10
lastmod: 2026-10-25T22:01:18+01:00
last_editor: Erik Hagen

---

This page documents the build pipeline that keeps the site up to date. So far only the section on failed builds has been translated. The full description is on the Norwegian page.

## Build workflow (`hugo.yml`)

*Updated 2026-10-25 after solution-samt-bu-docs#83.*

The file `.github/workflows/hugo.yml` in `samt-bu-docs`:

1. **Installs Hugo** (version 0.155.3 extended), with three attempts
2. **Checks out** `samt-bu-docs` with full history and submodules (the theme)
3. **Ensures UUIDs** in front matter (only on push to `samt-bu-docs`)
4. **Fetches the latest version of each module** with `hugo mod get …@latest`, with three attempts per module
5. **Builds with Hugo** through `.github/scripts/build-with-fallback.py`. If the build fails on one content file, the file is set aside and the rest is built (see [When a build fails](#when-a-build-fails))
6. **Writes the build receipt** `/build.json` (`write-build-info.py`)
7. **Deploys** to Cloudflare Pages with `wrangler`, with three attempts
8. **Reports** on solution-samt-bu-docs#83 if a file was set aside

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

The step «Meld fra om filer satt til side» in `hugo.yml` writes a comment on solution-samt-bu-docs#83 with the file, the error message and a link to the run. Each file is reported once. A hidden marker (`repo:path@commit`) in the comment keeps later builds from reporting the same error again.

| Secret | Repo | What |
|---|---|---|
| `BUILD_REPORT_TOKEN` | `samt-bu-docs` | Fine-grained token on `samt-x-bot`, only *Issues: Read and write* on `solution-samt-bu-docs`. Expires 2027-10-25. Kept in Bitwarden. |

If the token is missing, the step is skipped and the report is only in the job summary.

### Receipt when someone reports

The button «Report it here» in the browser links to #83. `build-report-receipt.yml` in `solution-samt-bu-docs` replies right away to new comments there. The reply has thanks, the status of the latest build, whether a build is running, and which files are set aside. Comments from bots and from the people who follow up get no reply. The people who follow up are listed in the workflow. The reply is posted with `GITHUB_TOKEN`, so no separate secret is needed.

### Testing changes to this

Test on a separate branch where the deploy step is removed, with a file that is broken on purpose, and run `gh workflow run hugo.yml --ref <branch>`. Note that the report step writes a real comment on #83. Delete the branch afterwards. Test the receipt with a comment on #83 from an account that is not in the list in the workflow.
