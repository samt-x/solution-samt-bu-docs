---
id: 44fda0b1-9034-4924-a29b-d1823b800756
title: "Kjente problemer og løsninger"
linkTitle: "Kjente problemer"
weight: 80
---

Kronologisk logg over feil og problemer oppdaget og løst under utvikling av SAMT-BU Docs. For hvert problem dokumenteres symptom, rotårsak og løsning – slik at det er lettere å diagnostisere lignende problemer i fremtiden.

---

## 🔴 ÅPEN 2026-03-03: Ytelsesproblem – søk-defer henter indeks ved sidelasting

**Symptom:** Merkbar latency/forsinkelse ved sidelasting. Oppleves som «varierende responstid på deler av skjermbildet».

**Rotårsak bekreftet:** `search.js` lastet med `defer` kaller `$.getJSON()` som henter hele søkeindeksen (JSON-fil, kan være stor) umiddelbart etter sidelasting. Dette skjer på hvert sidebytte og gir tydelig forsinkelse. Bekreftet ved lokal testing: uten `defer` på search-scripts → perfekt ytelse. Med `defer` → treg.

**To separate ytelsesårsaker som ikke må blandes:**
1. **jQuery synkron lasting** blokkerer HTML-rendering → treg første sidevisning. Løst ved å gi jQuery `defer` (2026-02-28).
2. **Søk-defer** trigger `$.getJSON()`-kall ved sidelasting → treg etter lasting. Dette er det nåværende problemet.

**Nåværende tilstand:**
- Online (`main`): har ytelsesproblem – search-scripts har `defer`, jQuery har `defer`
- Lokalt (`local-fixes`-branch i temaet): god ytelse – search-defer revertert, søk virker ikke

**Anbefalt løsning:** Lazy-load søkeindeksen – endre `search.js` til å ikke hente JSON-indeksen ved sidelasting, men først når brukeren fokuserer/klikker søkefeltet. Da unngås både render-blokkering og indeks-lasting ved sidelast.

**Filer å endre:** `themes/hugo-theme-samt-bu/static/js/search.js`, muligens `search.html`

---

## ✅ DELVIS LØST 2026-03-03: Altinn-scripts + dropdown-feil (jQuery defer-kaskade)

**Symptomer (nå løst):**
- Stor tom sone under innholdet i midtpanel
- Dropdowns (språk, Innhold, Endre) virket ikke
- Scroll-fade og sidebar-toggle mislyktes

**Rotårsak:** `altinninfoportal.js`, `altinndocs.js` og `altinndocs-learn.js` bruker alle jQuery (`$()`) direkte uten `$(document).ready()`. Lastet synkront mens jQuery var `defer` → `$` undefined → alle tre scripts feilet. Spesielt kritisk: `altinndocs.js` linje 2 kjørte `$('.js-moveChildrenFrom').insertAfter('.js-moveChildrenTo')` øyeblikkelig → DOM-manipulasjon mislyktes → stor tom sone.

`custom-footer.html` brukte `$(document).ready(...)` – inline scripts kan ikke ha `defer` → dropdowns virket ikke.

**Fix:**
1. `footer.html`: Lagt til `defer` på `altinninfoportal.js`, `altinndocs.js`, `altinndocs-learn.js`
2. `custom-footer.html`: Konvertert fra jQuery til vanilla JS (IIFE med direkte DOM-tilgang)

**Gjenstår:** Sidebar-scrollbar (se neste oppføring). Scroll-fade er ikke verifisert etter fix.

**Lærdom:** Når jQuery er `defer`, MÅ alle jQuery-avhengige externe scripts ha `defer`. Inline scripts må skrives om til vanilla JS.

---

## 🔴 ÅPEN 2026-03-03: Sidebar-scrollbar (venstre panel)

**Symptom:** Synlig scrollbar i venstre kolonne (`#sidebar`). Dukker opp selv om innholdet ikke fyller skjermen vertikalt («for tidlig»).

**Bekreftet:** Problemet eksisterer i alle testede tilstander – predaterer alle endringer gjort 2026-03-03. Verifisert ved lokal test på commit `74f2c31`.

**Forsøkte CSS-fixes (ingen virket):**
- `scrollbar-width: none !important` på `#sidebar`
- `display: none !important; width: 0 !important` på `#sidebar::-webkit-scrollbar`
- `overflow: visible !important` + `height: auto !important` på `#sidebar .highlightable`
- Samme regler på `#sidebar .highlightable::-webkit-scrollbar`

**Mistanke:** `altinndocs-learn.js`, når det nå kjøres korrekt (med jQuery tilgjengelig via defer), resetter `overflow`-property via JavaScript etter at CSS er satt. Inline style overstyrer stylesheet-regler.

**Neste steg:**
1. Åpne DevTools → Inspect `#sidebar` og `.highlightable` → sjekk hvilken regel som faktisk vinner
2. Sjekk om `altinndocs-learn.js` setter `style="overflow: auto"` direkte på elementet
3. Hvis JS-årsak: overstyr med `el.style.overflow = ''` etter at altinn-script kjører, eller patch altinn-script

**Filer:** `themes/hugo-theme-samt-bu/layouts/partials/custom-head.html`, muligens `altinndocs-learn.js`

---

## 2026-03-02: Søk virket ikke (jQuery defer-konflikt)

**Symptom:** Søkefeltet i headeren aksepterte input, men viste ingen resultater.

**Rotårsak:** jQuery ble lastet med `defer` i `header.html` (innført 2026-02-26 for ytelsesoptimalisering). `search.js` og avhengighetene `lunr.min.js` og `horsey.js` ble derimot lastet synkront i `<body>`. Nettleseren kjørte `search.js` umiddelbart under sideparsing – på det tidspunktet var `$` (jQuery) ikke tilgjengelig ennå. Kallet `$.getJSON(...)` kastet en feil, `lunrIndex` forble `null`, og alle søk returnerte tomt resultat uten synlig feilmelding.

**Fix:** `defer`-attributt lagt til på alle tre search-scripts i `layouts/partials/search.html` (temaet). Med `defer` garanterer nettleseren utføringsrekkefølge basert på dokumentrekkefølge:

1. jQuery (`header.html`, defer)
2. `lunr.min.js` (`search.html`, defer)
3. `horsey.js` (`search.html`, defer)
4. `search.js` (`search.html`, defer)

Inline `<script>var baseurl = "...";</script>` kjøres fortsatt synkront – korrekt, siden variabelen settes under parsing og er tilgjengelig når de deferred scriptene kjøres.

**Filer endret:** `themes/hugo-theme-samt-bu/layouts/partials/search.html`

**Lærdom:** Når ett script lastes med `defer`, må *alle* scripts som avhenger av det også ha `defer`.

---

## 2026-02-xx: Sidebar-ikon ute av sync med CSS

**Symptom:** Aktiv side viste `fa-caret-right` (lukket) i stedet for `fa-sort-down` (åpen) i sidebaren.

**Rotårsak:** `menu.html` manglet betingelsen `eq .RelPermalink $currentNode.RelPermalink` i ikonlogikken. `IsAncestor` er bare `true` for *forfedre* til gjeldende side, ikke for selve siden. På aktiv side var ingen betingelse oppfylt → feil ikon vises, men CSS viser siden som aktiv (ute av sync).

**Fix:** Lagt til `eq .RelPermalink $currentNode.RelPermalink` i betingelsen i `menu.html`. Korrekt logikk: `fa-sort-down` vises når `IsAncestor` ELLER `eq .RelPermalink` ELLER `alwaysopen`.

**Filer endret:** `themes/hugo-theme-samt-bu/layouts/partials/menu.html`

---

## Prosedyre: GitHub Pages stuck deploy

Av og til havner GitHub Pages i en tilstand der deployer kjøres uten effekt (siden ser ut til å deploye, men endringer dukker ikke opp).

**Fremgangsmåte for reset:**

```bash
"/c/Program Files/GitHub CLI/gh.exe" api -X DELETE repos/SAMT-BU/samt-bu-docs/pages
"/c/Program Files/GitHub CLI/gh.exe" api -X POST repos/SAMT-BU/samt-bu-docs/pages \
  --field build_type=workflow \
  --field source[branch]=main \
  --field source[path]="/"
git commit --allow-empty -m "Reset Pages"
git push
```

---

## Windows: `git mv` feiler for mapper med mange filer

**Symptom:** `git mv gammel-mappe/ ny-mappe/` feiler med feilmelding om at kildemappen ikke finnes.

**Workaround:**

```bash
cp -r gammel-mappe/ ny-mappe/
git rm -r gammel-mappe/
git add ny-mappe/
```
