---
id: 88a7cc4a-b428-488f-b159-1696bbc68594
title: "Pull request support in the Edit menu"
linkTitle: "Pull request flow"
weight: 95
status: "New"
lastmod: 2026-03-20T09:42:59+01:00
last_editor: Erik Hagen

---

Currently, editing via the Edit menu requires the user to have direct push access to the repository. External contributors – subject-matter experts, pilot participants, and others without repo access – cannot contribute via the built-in interface.

Pull request support would allow any GitHub user to suggest changes with the same simple user experience as the current direct flow.

## Proposed flow

1. User opens the edit dialog and makes changes as normal
2. On save: GitHub API creates a new branch (`<login>/patch-<date>`) and commits there instead of directly to `main`
3. GitHub API then creates a pull request from this branch against `main`
4. User sees a confirmation with a link to the PR instead of the build indicator

### Permission detection

The GitHub API endpoint `GET /repos/SAMT-X/samt-bu-docs/collaborators/<login>/permission` returns the user's permission level (`admin`, `write`, `read`, `none`). This can be used to select the flow automatically:

| Permission level | Flow |
|-----------------|------|
| `write` / `admin` | Direct commit to `main` (current flow) |
| `read` / `none` | Branch + pull request |

Alternatively: always offer the PR flow as an option in the dialog, regardless of permissions.

## Technical feasibility

All required functionality is available in the GitHub REST API:

| Operation | Endpoint |
|-----------|----------|
| Get current SHA for `main` | `GET /repos/.../git/ref/heads/main` |
| Create branch | `POST /repos/.../git/refs` |
| Commit to branch | `PUT /repos/.../contents/<path>` with `branch` parameter |
| Create PR | `POST /repos/.../pulls` |

The existing `createFilesInOneCommit()` in `custom-footer.html` already uses most of these – branch support is largely an extension of what is already there.

## Challenges

- **Fork flow:** Users without read access to a private repo must fork first. Handled by `POST /repos/.../forks` + commit to fork + PR from fork. More complex flow.
- **Conflict handling:** A PR may have merge conflicts that the user cannot resolve via the interface.
- **Build status:** PR builds are not triggered by `hugo.yml` (only push to `main`) – the pending indicator does not make sense for the PR flow. Builds occur only after merge.

## Priority

Medium – significantly increases accessibility for contributors without changing the experience for existing users with push access.

## Related

- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html` – `createFilesInOneCommit()`, `doGitHubLogin()`
- `themes/hugo-theme-samt-bu/layouts/partials/edit-switcher.html` – Edit menu and dialogs
