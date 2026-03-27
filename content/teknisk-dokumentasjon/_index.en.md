---
id: 398605d7-71ab-4678-84f7-2b605b181bff
title: "Technical Documentation"
linkTitle: "Technical Documentation"
weight: 20
lastmod: 2026-03-20T09:42:59+01:00

---

This page documents what is "under the bonnet" of the SAMT-BU platform. The intended audience is developers and architects who need to understand, maintain, or further develop the solution – including AI assistants such as Claude Code.

## Contents

- **Known issues and solutions** – bug log with symptom, root cause, and fix
- **CI/CD pipeline** – GitHub Actions workflow, inject-lastmod, cross-repo triggering
- **GitHub structure** – concept for organising GitHub organisations and repos (`samt-x` as platform org, project orgs for content)
- **Developer notes and Claude context** – architectural decisions, conventions, theme.css pitfalls, and context for new developers and AI assistants

Topics covered in Developer notes: Hugo architecture, theme (submodule), 3-column layout, Hugo Modules, CI/CD pipeline, Cloudflare Worker OAuth proxy, search system.
