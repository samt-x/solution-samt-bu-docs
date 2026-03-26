---
id: 6600fd23-52ac-42cd-8a38-0eaa8ef08e51
title: "Warning on simultaneous editing of the same page"
linkTitle: "Conflict warning on editing"
weight: 150
status: "New"
lastmod: 2026-03-20T09:42:59+01:00
last_editor: Erik Hagen

---

If two users open the edit dialog for the same page simultaneously, the last one to save will overwrite the other's changes without warning. A simple «someone is already editing this page» message would reduce the risk of lost changes.

## Challenge

The conflict warning requires some form of shared state: one browser being able to see that another browser has opened the edit dialog for a specific page. `localStorage` is user-local and does not work across users.

## Possible solutions

### A – Cloudflare Workers KV (lightweight presence register)

When the edit dialog opens: write `{ user, page, openedAt }` to KV with a TTL of e.g. 10 minutes.
When another user opens the same page: read KV and show warning if the entry exists and has not expired.
When the dialog is closed or saved: delete the entry.

**Advantages:** Low latency, no external dependency beyond existing CF infrastructure. KV is free on the CF Workers free tier.
**Disadvantages:** Requires a change to the Cloudflare Worker + new KV binding. TTL-based – stale locks if the browser crashes without deleting.

### B – GitHub file as a lock register

Write a small JSON file (e.g. `.editing-locks.json`) to a branch in the repo via the GitHub API. Read by other users when opening a dialog.

**Advantages:** No new infrastructure.
**Disadvantages:** GitHub API calls are slow for this purpose. Risk of conflicts on the lock file itself.

### C – Warn based on active builds only

A simpler approach: show a warning if there is an active build recently triggered from the same page (inferred from the commit message). Not a real lock, but covers the most common case.

**Advantages:** Uses existing GitHub Actions API – no new infrastructure.
**Disadvantages:** Does not cover the case where a user has opened the dialog but not yet saved.

## Recommended approach

**Option A** (CF Workers KV) is the cleanest solution and fits well with the existing architecture. Option C can be considered as a quick first step.

## Related

- `cloudflare-worker/oauth-worker.js` – existing CF Worker that can be extended
- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html` – `openQuillEditDialog()`
- Roadmap: [Build status and Close button](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/veikart/bygg-status-sperre/) – related problem
