---
id: 44fda0b1-9034-4924-a29b-d1823b800756
title: "Kjente problemer og løsninger"
linkTitle: "Kjente problemer"
weight: 40
lastmod: 2026-03-27T23:29:13+01:00
last_editor: Erik Hagen

---

Kronologisk logg over feil og problemer oppdaget og løst under utvikling av SAMT-BU Docs. For hvert problem dokumenteres symptom, rotårsak og løsning – slik at det er lettere å diagnostisere lignende problemer i fremtiden.

---

## ✅ LØST 2026-03-03: Ytelsesproblem – søk-defer henter indeks ved sidelasting

**Symptom:** Merkbar latency/forsinkelse ved sidelasting. Oppleves som «varierende responstid på deler av skjermbildet».

**Rotårsak bekreftet:** `search.js` lastet med `defer` kaller `$.getJSON()` som henter hele søkeindeksen (JSON-fil, kan være stor) umiddelbart etter sidelasting. Dette skjer på hvert sidebytte og gir tydelig forsinkelse. Bekreftet ved lokal testing: uten `defer` på search-scripts → perfekt ytelse. Med `defer` → treg.

**To separate ytelsesårsaker som ikke må blandes:**
1. **jQuery synkron lasting** blokkerer HTML-rendering → treg første sidevisning. Løst ved å gi jQuery `defer` (2026-02-28).
2. **Søk-defer** trigger `$.getJSON()`-kall ved sidelasting → treg etter lasting. **Løst 2026-03-03.**

**Fix:**
- `search.js`: Fjernet `initLunr()`-kall ved sidelasting. La til flagg `searchIndexLoaded`/`searchIndexLoading`. `initLunr()` kalles nå kun én gang, ved første `focus`-event på søkefeltet (`$.one("focus", ...)`).
- `search.html`: Lagt `defer` tilbake på `lunr.min.js`, `horsey.js` og `search.js` – garanterer korrekt rekkefølge etter jQuery (som også har `defer`).

**Lærdom:** Lazy-load løser problemet uten å ofre søkefunksjonalitet. Bruk `$.one("focus", initFn)` for å trigge tung initialisering kun ved faktisk bruk. Flagg (`loading`/`loaded`) forhindrer dobbelthenting.

---

## ✅ LØST 2026-03-03: Sidebar-scrollbar (venstre panel)

**Symptom:** Synlig scrollbar i venstre kolonne (`#sidebar`). Dukket opp selv om innholdet ikke fylte skjermen vertikalt.

**Rotårsak:** Delvis uklar (JS-innblanding fra Altinn-scripts ble mistenkt, men ikke bekreftet). CSS-reglene `scrollbar-width: none` og `display: none` på `::-webkit-scrollbar` var ikke sterke nok alene.

**Fix:**
1. CSS i `custom-head.html`: la til `!important` på `scrollbar-width: none`, utvidet webkit-scrollbar-regel til å dekke alle descendants (`#sidebar *::-webkit-scrollbar`), og la til `!important` på `.highlightable`-override.
2. JS-fallback i `footer.html`: `requestAnimationFrame` som etter sidelasting fjerner eventuelle inline `overflow`/`height`-stiler fra `.highlightable` (i tilfelle Altinn-scripts setter disse dynamisk).

**Lærdom:** For robuste scrollbar-skjulinger: bruk `!important`, dekk både elementet og alle children med webkit-regel, og kombiner med JS-fallback for å håndtere dynamisk stilsetting.

---

## ✅ LØST 2026-03-03: Sidebar scroll-fade viste solid hvit blokk

**Symptom:** Det hvite fader-feltet nederst i venstre panel skjulte siste linje helt (solid hvit), i motsetning til høyre panel (TOC) der tekst skinner gjennom (opacity-gradient).

**Rotårsak:** Sidebar-faden brukte `#sidebar::after` (pseudo-element på scroll-containeren), mens TOC-faden brukte et ekte DOM-element inne i scroll-containeren. `position: sticky; bottom: 0` på et pseudo-element som er direkte barn av scroll-containeren oppfører seg annerledes enn på et element inne i innholdsstrømmen – gir solid blokk i stedet for overlappende gradient.

**Fix:** Bytte til samme teknikk som TOC:
1. `menu.html`: la til `<div class="sidebar-scroll-fade hidden"></div>` som siste element inne i `.highlightable`
2. `custom-head.html`: erstattet `#sidebar::after`-regler med `.sidebar-scroll-fade`-regler (identisk med `.toc-scroll-fade`)
3. `footer.html`: oppdaterte JS til å toggle `.hidden` på `.sidebar-scroll-fade` i stedet for `.fade-hidden` på `#sidebar`

**Lærdom:** For scroll-fade inne i en scroll-container: bruk alltid et ekte DOM-element med `position: sticky; bottom: 0` plassert *inne i* innholdsstrømmen – ikke `::after` på containeren selv.

---

## ✅ LØST 2026-03-03: «Endre denne siden i GitHub»-lenke for langt ned i midtpanel

**Symptom:** Stor tom sone mellom innholdet i midtpanelet og «Endre denne siden i GitHub»-lenken nederst til høyre.

**Rotårsak (1):** `theme.css` definerer `#top-github-link { position: relative; top: 50%; transform: translateY(-50%) }` – en teknikk fra det opprinnelige temaet for å sentrere lenken vertikalt. I vår 3-kolonne-layout der `#body` er en høy scrollbar kolonne, dytte dette lenken ~50% av panelets høyde ned fra sin naturlige plassering.

**Rotårsak (2):** `.adocs-content` hadde `padding-bottom: 36px` og `margin-bottom: 12px` fra theme.css, pluss `#top-github-link` med `margin-top: 24px` og `padding-top: 12px` – tilsammen ~84px mellomrom.

**Fix i `custom-head.html`:**
```css
#top-github-link {
  position: static !important;
  top: auto !important;
  transform: none !important;
  margin-top: 8px;
  padding-top: 8px;
}
.adocs-content {
  padding-bottom: 12px !important;
  margin-bottom: 4px !important;
}
```

---

## ✅ LØST 2026-03-03: Sidebar-meny – inkonsistent klikkatferd (tekst vs. pil)

**Symptom:** Klikk på menyteksten for en seksjon med barn (f.eks. «SAMT-BU Docs») ga annen atferd enn klikk på pilen til høyre for samme element.

**Rotårsak:** `altinndocs-learn.js` hadde click-handleren på `.category-icon` (selve `<i>`-ikonet) med `return false`. Klikk på ikonet → handler + `return false` → akkordeon-toggle, ingen navigasjon. Klikk på teksten (`<span>`) → ingen handler → bublet til `<a>` → navigerte til ny side → inkonsistent atferd.

**Første forsøk (feil):** Endret selektoren til `#sidebar .dd-item > a` med `return false` for alle `<a>` med barn. Dette gav konsistent oppførsel for pilen, men blokkerte navigasjon til seksjonsindeks-sider for ALLE mellomnivåer i menyen.

**Endelig fix:** Beholdt handleren på `.category-icon`, men brukte `e.stopPropagation()` i stedet for `return false`:
```javascript
jQuery('#sidebar .category-icon').on('click', function(e) {
    e.stopPropagation();  // forhindrer klikket i å nå <a> → ingen navigasjon
    $(this).toggleClass('fa-sort-down fa-caret-right');
    $(this).closest('li').children('ul').toggle();
});
```

Resultat:
- Klikk på pilen → akkordeon-toggle, ingen navigasjon
- Klikk på teksten → navigerer til seksjonsindeks-siden normalt

**Lærdom:** `e.stopPropagation()` på et child-element inne i `<a>` stopper klikket i å boble opp til `<a>`, og forhindrer dermed navigasjon – uten å bruke `return false` på `<a>` selv. Seksjonssider med barn forblir navigerbare via tekstklikk.

---

## ✅ LØST 2026-03-03: Altinn-scripts + dropdown-feil (jQuery defer-kaskade)

**Symptomer (løst):**
- Stor tom sone under innholdet i midtpanel
- Dropdowns (språk, Innhold, Endre) virket ikke
- Scroll-fade og sidebar-toggle mislyktes

**Rotårsak:** `altinninfoportal.js`, `altinndocs.js` og `altinndocs-learn.js` bruker alle jQuery (`$()`) direkte uten `$(document).ready()`. Lastet synkront mens jQuery var `defer` → `$` undefined → alle tre scripts feilet. Spesielt kritisk: `altinndocs.js` linje 2 kjørte `$('.js-moveChildrenFrom').insertAfter('.js-moveChildrenTo')` øyeblikkelig → DOM-manipulasjon mislyktes → stor tom sone.

`custom-footer.html` brukte `$(document).ready(...)` – inline scripts kan ikke ha `defer` → dropdowns virket ikke.

**Fix:**
1. `footer.html`: Lagt til `defer` på `altinninfoportal.js`, `altinndocs.js`, `altinndocs-learn.js`
2. `custom-footer.html`: Konvertert fra jQuery til vanilla JS (IIFE med direkte DOM-tilgang)

**Lærdom:** Når jQuery har `defer`, MÅ alle jQuery-avhengige externe scripts ha `defer`. Inline scripts må skrives om til vanilla JS.

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

## ✅ LØST 2026-03-08: solution-samt-bu-docs manglet HUGO_MODULE_REPLACEMENTS i CI

**Symptom:** Nytt innhold pushet til `solution-samt-bu-docs` viste seg ikke på nettstedet selv etter at CI-rebuild kjørte. Kryssrepo-triggering fungerte (rebuild ble trigget), men Hugo brukte gammel, pinnet versjon av modulen.

**Rotårsak:** `hugo.yml` satte `HUGO_MODULE_REPLACEMENTS` kun for `team-architecture` og `samt-bu-drafts`. For `solution-samt-bu-docs` ble ingen lokal kloning gjort – Hugo brukte versjonen pinnet i `go.mod`.

**Fix (2026-03-08):** `solution-samt-bu-docs` lagt til i alle tre steder i `samt-bu-docs`:
1. Ny `actions/checkout`-blokk i `hugo.yml`
2. Lagt til i `HUGO_MODULE_REPLACEMENTS` i `hugo.yml`
3. Lagt til i `MODULE_PATHS` i `inject-lastmod.py`

Push til `solution-samt-bu-docs` → kryssrepo-trigger → CI kloner siste commit direkte. Manuell `hugo mod get @latest` er ikke lenger nødvendig.

> **NOTE – verifiser neste gang et nytt modulrepo legges til:**
> Opplegget er bekreftet å fungere for de tre nåværende modulene, men er ikke testet for et fjerde. Neste gang et nytt modulrepo kobles til nettstedet, verifiser at:
> - CI-bygget fortsatt er grønt etter at nytt checkout-steg er lagt til
> - Innhold fra det nye repoet faktisk dukker opp på nettstedet etter push
> - «Sist endret»-tidsstempler vises korrekt for det nye innholdet
>
> Se kommentarblokken i `hugo.yml` og `inject-lastmod.py` for mønsteret (3 steg).

---

## Windows: `git mv` feiler for mapper med mange filer

**Symptom:** `git mv gammel-mappe/ ny-mappe/` feiler med feilmelding om at kildemappen ikke finnes.

**Workaround:**

```bash
cp -r gammel-mappe/ ny-mappe/
git rm -r gammel-mappe/
git add ny-mappe/
```
