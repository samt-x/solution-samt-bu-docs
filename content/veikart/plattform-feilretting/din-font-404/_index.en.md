---
id: 50345854-27d8-4b1c-8f78-a6d036501284
title: "Remove 404 errors for DIN web fonts"
linkTitle: "DIN font 404 errors"
weight: 80
status: "New"
lastmod: 2026-03-26T16:32:48+01:00

---

`designsystem.css` contains `@font-face` declarations that attempt to load DIN web fonts from `/fonts/DINWeb.woff...` and `/fonts/DINWeb-Bold.woff...`. These files do not exist in the repo, causing two 404 errors in the browser console on **every** page.

## Impact

Cosmetic only – the site falls back to Helvetica/Arial as defined in `custom-head.html`, and nothing breaks visually. However, the errors add noise to the console and may obscure real errors.

## Recommended fix

Two options:

**A) Comment out `@font-face` blocks in `designsystem.css`**
Since fonts are already overridden in `custom-head.html`, the DIN declarations are unnecessary.

**B) Add the actual font files**
Obtain `DINWeb.woff`/`.woff2` and `DINWeb-Bold.woff`/`.woff2` from the Altinn Design System source and place them in `themes/hugo-theme-samt-bu/static/fonts/`.

Option A is fastest. Option B is correct if DIN font is actually desired.
