---
# id: auto-generated – copied values are overwritten automatically on push
id: 07b4e68b-a7d0-40ca-bd54-4e2ab3f92e95
title: "SAMT-BU Docs"
linkTitle: "SAMT-BU Docs"
weight: 10
lastmod: 2026-03-28T10:12:28+01:00
last_editor: Erik Hagen

---

This section documents the technical solutions used to build and operate the SAMT-BU documentation platform. The content is aimed at future developers, architects, and administrators who need to understand, maintain, or further develop the solution.

The platform is composed of the following components:

| Component | Role |
|-----------|------|
| **Hugo** | Static site generator – builds HTML from Markdown |
| **Built-in editor (TipTap)** | Browser-based content editing directly in the website – no external CMS |
| **Hugo Modules** | Content modules from separate repositories are mounted into the site |
| **GitHub Actions** | CI/CD pipeline – builds and deploys on push to `main` |
| **Cloudflare Workers** | OAuth proxy for secure authentication against GitHub |
| **Cloudflare Pages** | Hosting of the finished website |

See the sub-chapters for technical documentation and administration guides.
