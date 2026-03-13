---
id: ""
title: "Fjern 404-feil for DIN-webfonter"
linkTitle: "DIN-font 404-feil"
weight: 35
status: "Ny"
---

`designsystem.css` inneholder `@font-face`-deklarasjoner som prøver å laste DIN-webfonter fra `/fonts/DINWeb.woff...` og `/fonts/DINWeb-Bold.woff...`. Disse filene finnes ikke i repoet, noe som gir to 404-feil i nettleserkonsollen på **alle** sider.

## Konsekvens

Rent kosmetisk – nettstedet faller tilbake til Helvetica/Arial som definert i `custom-head.html`, og ingenting brekker visuelt. Men feilene støyer i konsollen og kan skjule ekte feil.

## Anbefalt løsning

To alternativer:

**A) Kommenter ut `@font-face`-blokkene i `designsystem.css`**
`designsystem.css` ligger i `themes/hugo-theme-samt-bu/static/css/`. Siden vi uansett overstyrer fontene i `custom-head.html`, er DIN-deklarasjonene unødvendige. Kommenter ut `@font-face`-blokkene for `DINWeb` og `DINWeb-Bold`.

**B) Legg inn de faktiske fontfilene**
Hent `DINWeb.woff`/`DINWeb.woff2` og `DINWeb-Bold.woff`/`DINWeb-Bold.woff2` fra Altinn Design System-kilden og plasser dem i `themes/hugo-theme-samt-bu/static/fonts/`. Gir korrekt typografi uten overstyringer.

Alternativ A er raskest. Alternativ B er mer korrekt hvis DIN-fonten faktisk skal brukes.
