---
id: e0e03dc4-b617-44cb-b829-a47ac7313a9d
title: "Concept for GitHub Organizations and Repositories"
linkTitle: "GitHub structure"
weight: 20
status: "Early draft"
lastmod: 2026-03-15T23:49:44+01:00

---

This page documents the principles for how we organize GitHub organizations (orgs) and repositories in the SAMT-BU platform – and lays the groundwork for the structure to scale to multiple projects under the SAMT umbrella.

> **Status:** Early draft. The concept is partially implemented but not fully thought through for the scenario of multiple parallel projects. This page is updated continuously.

---

## Core principle

We distinguish between two roles:

| Role | Responsibility | Example |
|------|----------------|---------|
| **Platform org** | Publishes websites, owns theme and infrastructure | `github.com/samt-x` |
| **Project org** | Owns content for one specific project | `github.com/samt-bu`, `github.com/samt-pb` |

`samt-x` is the platform organization – this is where published GitHub Pages sites live, and where the shared theme and CI/CD framework are managed. Project orgs are the content owners.

---

## Publishing via GitHub Pages

GitHub Pages publishes sites from repos in an org at `<org>.github.io/<repo>`. For a site to appear under `samt-x.github.io/`, the Hugo site repo must belong to the `samt-x` org:

```
github.com/samt-x/samt-bu-docs  →  samt-x.github.io/samt-bu-docs/
github.com/samt-x/samt-pb-docs  →  samt-x.github.io/samt-pb-docs/
```

Content repos (modules) can reside in **any org** – the Hugo Module system is org-agnostic.

---

## Hugo Modules are org-agnostic

`hugo.toml` references modules using the full `github.com/<org>/<repo>` path. The org boundary is invisible to Hugo:

```toml
[[module.imports]]
path = "github.com/samt-pb/team-architecture"
```

This means content repos can be freely organized in project-specific orgs without affecting the publishing structure.

---

## Current structure (samt-bu project)

Currently all repos reside in the `samt-x` org – both infrastructure and content:

| Repo | Type | Should belong to |
|------|------|-----------------|
| `hugo-theme-samt-bu` | Infrastructure | `samt-x` ✅ |
| `samt-bu-docs` | Published site | `samt-x` ✅ |
| `team-architecture` | Content | `samt-x` (for now) |
| `samt-bu-drafts` | Content | `samt-x` (for now) |
| `solution-samt-bu-docs` | Content | `samt-x` (for now) |
| `samt-bu-files` | Attachments | `samt-x` (for now) |

Content repos were created in `samt-x` early in the project. They work fine where they are, and migration is not a priority – but it is noted that they conceptually belong in a dedicated `samt-bu` org.

---

## Recommended principles going forward

1. **`samt-x` = platform.** Only infrastructure repos and Hugo site repos (one per published site) belong here.
2. **New projects = new org.** Create one org per project (`samt-pb`, `samt-pc`, ...) for content repos. This gives clear ownership and avoids naming clutter in `samt-x`.
3. **Shared resources – loosely coupled.** A repo like `team-architecture` can in principle be mounted by multiple Hugo sites (e.g., both `samt-bu-docs` and `samt-pb-docs`). The Hugo Modules system supports this without modification.
4. **Don't migrate what works.** Existing `samt-bu` content repos in `samt-x` are not moved unless there is a concrete reason.

---

## Open questions

- **Shared team repos:** Can e.g. `team-architecture` belong to one org but be mounted by sites in `samt-x`? Yes, technically – but ownership and access control should be clarified. Should the content be owned by the project or by the team across projects?
- **Naming conventions for shared repos:** If a team repo is to serve multiple projects, it should not carry a project-specific prefix.
- **Migration of existing repos:** Is it worth moving `team-architecture` etc. to a `samt-bu` org? This affects CI secrets, CMS config, and Hugo Module pointers.
- **Access control across orgs:** GitHub permissions are managed per org. How do we handle contributors from the `samt-bu` project needing write access to repos in `samt-x`?
