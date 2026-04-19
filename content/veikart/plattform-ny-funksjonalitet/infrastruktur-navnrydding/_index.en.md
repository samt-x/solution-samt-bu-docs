---
# id: auto-generated – copied values are overwritten automatically on push
id: c5145be6-1a5d-42bb-b037-54bfed670ed6
title: "Name cleanup: infrastructure and services"
linkTitle: "Infrastructure – name cleanup"
weight: 126
status: "New"
# Valid values: New | Early draft | In progress | For QA | Approved | Cancelled
lastmod: 2026-04-19T14:07:55+02:00
last_editor: Erik Hagen

---

There is currently an inconsistency between the names of the website, infrastructure components, and OAuth app. This should be resolved in a consolidated review.

## Inconsistencies

| Component | Current name | Desired direction |
|-----------|-------------|-------------------|
| Website | SAMT-BU Docs (`samt-bu-docs.pages.dev`) | Keep – specific to this project |
| Cloudflare Worker | `samt-bu-cms-auth.erik-hag1.workers.dev` | Should be moved and possibly renamed (see also «OAuth infrastructure – org») |
| GitHub OAuth App | «SAMT-X Docs» (owned by `samt-x` org) | Generic for the whole org – fine as is |

## What needs to be clarified

- Should the Worker be named `samt-bu-auth` (project-specific) or `samt-x-auth` (generic for org)?
- If one Worker is to serve multiple future sites under SAMT-X, it should have a generic name
- Callback URL in OAuth App must be updated if the Worker gets a new domain

## Dependency

Should be coordinated with «Move OAuth infrastructure to organization account».
