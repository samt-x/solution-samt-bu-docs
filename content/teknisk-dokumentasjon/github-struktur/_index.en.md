---
# id: auto-generated – copied values are overwritten automatically on push
id: e0e03dc4-b617-44cb-b829-a47ac7313a9d
title: "Concept for GitHub Organizations and Repositories"
linkTitle: "GitHub structure"
weight: 20
status: "Early draft"
lastmod: 2026-08-12T17:59:09+02:00
last_editor: Erik Hagen

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

## Access model

Established 12 August 2026. Background and rationale in
[issue #69](https://github.com/SAMT-X/solution-samt-bu-docs/issues/69).

Access is granted to **teams**, never to individuals:

| Team | Members | Write on |
|------|---------|----------|
| `samt-bu-core-team` | Core participants | All repos except the three frozen ones |
| `samt-bu-alle` | All organisation members | `samt-bu-docs`, `samt-bu-drafts`, `samt-bu-files` |
| Subject teams (`samt-bu-pilot-1…4`, `-architecture`, `-semantics`, `-market`) | Participants in that work | Their own repo |

**Three frozen repos** have no editorial team access, only personal grants:
`hugo-theme-samt-bu`, `samt-x.github.io` and `information-models`.
They are not intended for editing in a documentation context. (`demo-repository`
was the fourth, and was deleted on 2026-10-23.)

**Pilot teams do not grant access to the shared documentation.** `samt-bu-docs`
was previously attached to the `samt-bu-pilot-1` team, which gave pilot 1
participants write access the other pilots lacked. That link has been removed.

### Maintenance

- New person on the project → add to `samt-bu-alle` (and `samt-bu-core-team` if
  they are a core participant)
- New module repo → add it to `samt-bu-core-team`

### Why not an org-level base permission

The org-level base permission is a **floor**, not a starting point. Setting it
to `write` gives everyone write access to everything – and it cannot be lowered
per repo. As long as the three repos are to be kept out, this is ruled out.

### Note

- **Organisation owners have admin everywhere**, regardless of teams. That is
  an access path not visible in the team structure.
- **`erikhag1test` has a direct grant on `samt-bu-docs`** and is not an
  organisation member. The grant is that account's only access path, and it is
  used for testing. It **must not be removed** in a cleanup of direct grants.

---

## Open questions

- **Shared team repos:** Can e.g. `team-architecture` belong to one org but be mounted by sites in `samt-x`? Yes, technically – but ownership and access control should be clarified. Should the content be owned by the project or by the team across projects?
- **Naming conventions for shared repos:** If a team repo is to serve multiple projects, it should not carry a project-specific prefix.
- **Migration of existing repos:** Is it worth moving `team-architecture` etc. to a `samt-bu` org? This affects CI secrets, CMS config, and Hugo Module pointers.
- **Access control across orgs:** GitHub permissions are managed per org. Within `samt-x` this is now solved by the team model above. The question only returns once content repos are actually moved to a dedicated `samt-bu` org – the team structure would then have to be mirrored in both orgs.
