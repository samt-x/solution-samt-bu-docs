---
title: "User Guide"
linkTitle: "User Guide"
weight: 5
---

This section is a practical guide for editors and contributors working with content in SAMT-BU Docs. It goes deeper than the general [How to Contribute](/samt-bu-docs/om/hvordan-bidra/)-page and covers workflow, CMS functionality, and handling situations where multiple people edit at the same time.

## Who is this for?

| You are... | Start here |
|------------|-----------|
| An editor working in the browser (CMS) | [CMS in depth](cms-i-dybden/) |
| A contributor with a local copy of the repositories | [Synchronisation and conflict handling](synkronisering/) |
| New to the platform | Read both – start with CMS in depth |

## Quick orientation

SAMT-BU Docs is built on Hugo and published automatically to GitHub Pages via GitHub Actions. Content is edited in three ways:

1. **Decap CMS** (recommended for subject-matter experts) – visual browser-based editor
2. **GitHub** – direct editing in the browser on github.com
3. **Locally** – clone the repo, edit Markdown files, push

Content from several repositories is merged into a single website. Changes are published automatically 1–3 minutes after they are saved (commit pushed to `main`).
