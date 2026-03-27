---
id: e40c2b29-8643-4556-9860-dc72cde6a1d4
title: "GitHub-autentisering uavhengig av CMS-valg"
linkTitle: "GitHub-auth – CMS-uavhengig"
weight: 120
status: "Godkjent"
# Gyldige verdier: Ny | Tidlig utkast | Pågår | Til QA | Godkjent | Avbrutt
lastmod: 2026-03-27T23:29:13+01:00
last_editor: Erik Hagen

---

**Implementert 2026-03-11.** Alternativ B (gjenbruk OAuth-proxy) ble valgt og gjennomført, kombinert med fullstendig fjerning av Decap CMS.

## Hva som ble gjort

- `getDecapToken()` erstattet med `getStoredToken()` + `storeToken()` + `doGitHubLogin(onSuccess)`
- Token lagres i `samt-bu-gh-token` (localStorage) – eget nøkkel, uavhengig av Decap
- Fallback til Decap-nøkler (`netlify-cms-user`, `decap-cms-user`) for brukere med eksisterende sesjon
- Alle dialog-åpnere trigger OAuth-popup automatisk når token mangler – ingen manuell innloggingssekvens
- Cloudflare Worker (`samt-bu-cms-auth.erik-hag1.workers.dev`) er uendret – implementerer `postMessage`-protokollen som nettstedet nå selv håndterer på åpner-siden
- Alle Decap CMS-portaler (`static/edit/`) og Decap-menypunkter i edit-switcher er fjernet

## Teknisk detalj: postMessage-protokollen

```
Åpner (nettstedet)         Popup (Cloudflare Worker callback)
       |                              |
       |←── "authorizing:github" ────|  (popup forteller åpner den er klar)
       |──── "authorizing:github" ──→|  (åpner svarer – popup lærer vår origin)
       |←── "authorization:github:  |
       |     success:{token,...}" ───|  (popup sender token til vår origin)
       |                              |
  storeToken() + onSuccess()    popup.close()
```
