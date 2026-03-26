---
id: 7aa3bf53-2226-4a6b-a3ca-6a80309577aa
title: "Branch strategy for GUI development"
linkTitle: "Branch strategy for GUI development"
weight: 120
status: "New"
last_editor: erikhag1git (Erik Hagen)
lastmod: 2026-03-20T09:42:59+01:00

---

As users adopt the site, active GUI development should happen in a separate branch so that errors do not disturb production. Until this is set up, `main` is used with rapid rollback (see [CI/CD pipeline](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/teknisk-dokumentasjon/ci-cd-pipeline/)).

## Proposed setup

### Branches

| Repo | Branch | Purpose |
|------|--------|---------|
| `hugo-theme-samt-bu` | `dev` | GUI changes under development |
| `samt-bu-docs` | `dev` | Points to theme `dev`, any config changes |

### Preview URL

Cloudflare Pages automatically builds a preview deploy for all non-main branches:

```
dev.samt-bu-docs.pages.dev
```

This can be used to test the full edit flow (commit, build polling, pending indicator, OAuth) against real GitHub – without affecting production content on `main`.

## Complication: commit branch in JS

The JS code in `custom-footer.html` commits to `main` as the target branch. On the `dev` branch, test commits should go to `dev`, not `main`. Solution: inject the commit branch as a Hugo parameter from `hugo.toml` or as a CI environment variable, so the correct branch is used automatically depending on which branch is building.

## Workflow

1. Make changes to `hugo-theme-samt-bu` on the `dev` branch
2. Commit and push → CF Pages builds preview
3. Test the full edit flow on the preview URL
4. Merge `dev` → `main` in the theme when ready
5. Update submodule pointer in `samt-bu-docs/main`

## Priority

Low for now – the rollback strategy on `main` is sufficient for current usage patterns. Should be set up when GUI changes become more experimental or the user base grows.
