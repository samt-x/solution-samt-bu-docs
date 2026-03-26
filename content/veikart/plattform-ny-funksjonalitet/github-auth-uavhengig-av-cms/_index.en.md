---
id: e40c2b29-8643-4556-9860-dc72cde6a1d4
title: "GitHub authentication independent of CMS choice"
linkTitle: "GitHub auth – CMS-agnostic"
weight: 120
status: "Approved"
# Valid values: New | Early draft | In progress | For QA | Approved | Cancelled
last_editor: erikhag1git (Erik Hagen)
lastmod: 2026-03-20T09:42:59+01:00

---

**Implemented 2026-03-11.** Alternative B (reuse OAuth proxy) was chosen and carried out, combined with the complete removal of Decap CMS.

## What was done

- `getDecapToken()` replaced with `getStoredToken()` + `storeToken()` + `doGitHubLogin(onSuccess)`
- Token stored in `samt-bu-gh-token` (localStorage) – a dedicated key, independent of Decap
- Fallback to Decap keys (`netlify-cms-user`, `decap-cms-user`) for users with an existing session
- All dialog openers automatically trigger the OAuth popup when a token is missing – no manual login sequence required
- Cloudflare Worker (`samt-bu-cms-auth.erik-hag1.workers.dev`) is unchanged – implements the `postMessage` protocol that the site itself now handles on the opener side
- All Decap CMS portals (`static/edit/`) and Decap menu items in the edit-switcher have been removed

## Technical detail: the postMessage protocol

```
Opener (the site)              Popup (Cloudflare Worker callback)
       |                              |
       |←── "authorizing:github" ────|  (popup tells opener it is ready)
       |──── "authorizing:github" ──→|  (opener responds – popup learns our origin)
       |←── "authorization:github:  |
       |     success:{token,...}" ───|  (popup sends token to our origin)
       |                              |
  storeToken() + onSuccess()    popup.close()
```
