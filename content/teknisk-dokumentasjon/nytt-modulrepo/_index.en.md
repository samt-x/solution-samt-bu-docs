---
id: ed2ee794-3c97-4e2d-959d-90b235a4f3d6
title: "Creating a new module repository – step by step"
linkTitle: "New module repo"
weight: 25
lastmod: 2026-03-27T23:29:13+01:00
last_editor: Erik Hagen

---

**Need:** There is no consolidated, step-by-step guide for creating a new Hugo module repository from scratch and connecting it to the site. The process requires coordination across multiple repositories and configuration files.

## Planned content

The guide will cover the full flow from empty repo to published content:

1. Create repo in the correct GitHub org
2. `hugo mod init github.com/<org>/<repo>`
3. Create content structure (`content/_index.nb.md`, `_index.en.md`)
4. Register the module in `samt-bu-docs/hugo.toml` (`[[module.imports]]`)
5. Run `hugo mod get @latest` and commit `go.mod`/`go.sum`
6. Add to `HUGO_MODULE_REPLACEMENTS` and `inject-lastmod.py` in CI
7. Create cross-repo trigger workflow in the module repo
8. Create CMS portal (nb + en) in `samt-bu-docs`
9. Add new branch in `edit-switcher.html`

*Not started.*
