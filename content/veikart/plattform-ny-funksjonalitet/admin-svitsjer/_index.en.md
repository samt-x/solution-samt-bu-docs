---
# id: auto-generated – copied values are overwritten automatically on push
id: 32d0f020-7521-4c07-8fba-c84100a5f7cb
title: "Admin switchers in the header"
linkTitle: "Admin switchers"
weight: 97
status: "New"
# Valid values: New | Early draft | In progress | For QA | Approved | Cancelled
lastmod: 2026-04-19T17:46:41+02:00
last_editor: Erik Hagen

---

A dedicated «Admin» dropdown in the header for users with write access, containing functionality that does not fit in the regular «Edit» menu.

## Proposed content

- **PR overview** – list of open pull requests across all module repos (`samt-bu-docs`, `samt-bu-drafts`, `team-architecture` etc.), with merge buttons directly in the interface
- **Build status** – overview of active and recent builds in GitHub Actions
- **Module update** – manual trigger of `hugo mod get` + rebuild for all modules

## Technical approach

- Shown only for users with `write`/`admin` permissions (reuse `checkCollaboratorPermission`)
- GitHub API: `GET /repos/SAMT-X/{repo}/pulls` for all relevant repos
- Merge via `PUT /repos/SAMT-X/{repo}/pulls/{number}/merge`
- Same dropdown pattern as existing «Edit» and «Content» switchers

## Dependency

Requires the PR flow («Pull request support in the Edit menu») to be complete and in use.

## Priority

Low – experimental idea. Evaluate after the PR flow has been thoroughly tested.
