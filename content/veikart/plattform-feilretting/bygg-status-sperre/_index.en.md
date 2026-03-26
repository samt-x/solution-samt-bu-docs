---
id: f9cbe239-500e-4760-882e-e3a5dd7c3b71
title: "Build status lock and correct Close button"
linkTitle: "Build status and Close button"
weight: 70
status: "Approved"
last_editor: erikhag1git (Erik Hagen)
lastmod: 2026-03-20T09:42:59+01:00

---

**Implemented 2026-03-12.** Both parts have been completed in the theme (`custom-footer.html` and `edit-switcher.html`).

When the user clicks Save in the editing dialog, a commit is sent to GitHub and a build starts automatically. The button currently labelled **«Cancel»** is misleading because the commit cannot be undone – the build job continues regardless of whether the dialog is closed.

## Problem 1: «Cancel» promises something it cannot deliver

After the user has clicked Save, the button should no longer say «Cancel». A more accurate label: **«Close this window»**, supplemented by a small information text explaining that the job continues in the background even if the dialog is closed.

## Problem 2: No warning when a build is in progress

If a user (same or different) tries to edit a page while a build job is already running due to a recent save on that page, a new commit will either:
- create a **race condition** against the ensure-uuids bot, or
- produce an «Update is not a fast forward» conflict

(We have added automatic retry, but that is a workaround, not a solution.)

## Proposed solution

### Part 1 – Rename Cancel → Close button with explanation

After Save has been clicked and the commit has been sent:
- Button text changes from «Cancel» to «Close this window»
- A small grey information text appears below the status field: «The job continues in the background. You can close this window safely.»

### Part 2 – Build status check when opening the edit dialog

When `openQuillEditDialog()` is called, the GitHub Actions API is checked for ongoing builds:

```javascript
GET /repos/SAMT-X/samt-bu-docs/actions/workflows/hugo.yml/runs?per_page=1
```

If the latest run has `status: "in_progress"` or `status: "queued"` and was created within the last ~10 minutes:
- Show a warning at the top of the dialog: «⚠ A build is currently in progress. Saving may cause a conflict – wait until the build is finished.»
- The button can still be used (not blocked), but the warning is prominent.

### Technical feasibility

| Check | Method | CORS | Token |
|-------|--------|------|-------|
| GitHub Actions runs | `GET /repos/.../actions/workflows/hugo.yml/runs` | ✅ allowed | Already in use |
| Cloudflare Pages deployments | `GET api.cloudflare.com/...` | ❌ blocked | Not applicable |

The GitHub Actions API is therefore the only option – but it is sufficient, and users are already logged in with a GitHub token.

The check is **cross-user**: if user A saves and user B opens the edit dialog seconds later, B will see the warning.

## Priority

Low – automatic retry handles most cases in practice. But should be done to:
- give users the correct expectation of what «Cancel» does
- make the multi-user scenario safer

## Related

- `custom-footer.html`: `openQuillEditDialog`, `pollQeBuild`, `startGhPoll`
- MEMORY.md: «Delete page with sub-pages» (similar pattern – blocking on unfavourable state)
