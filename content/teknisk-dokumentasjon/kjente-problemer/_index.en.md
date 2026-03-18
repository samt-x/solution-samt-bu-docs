---
id: 44fda0b1-9034-4924-a29b-d1823b800756
title: "Known issues and solutions"
linkTitle: "Known issues"
weight: 40
last_editor: erikhag1git (Erik Hagen)
lastmod: 2026-03-15T23:49:44+01:00

---

Chronological log of bugs and issues discovered and resolved during development of SAMT-BU Docs. Each entry documents symptom, root cause, and fix — making it easier to diagnose similar problems in the future.

See the Norwegian version (`_index.nb.md`) for full details. Key entries summarised below.

---

## ✅ 2026-03-03: Sidebar menu – inconsistent click behaviour (text vs. arrow)

**Symptom:** Clicking the menu item text for a section with children behaved differently from clicking its arrow icon.

**Root cause:** Click handler on `.category-icon` with `return false` → icon click toggled accordion (no navigation), text click bubbled to `<a>` → navigation. Inconsistent.

**First attempt (wrong):** Changed selector to `#sidebar .dd-item > a` with `return false` for all `<a>` with children. Consistent arrow behaviour, but blocked navigation to section index pages for all intermediate menu levels.

**Final fix:** Kept handler on `.category-icon`, used `e.stopPropagation()` instead:
```javascript
jQuery('#sidebar .category-icon').on('click', function(e) {
    e.stopPropagation();
    $(this).toggleClass('fa-sort-down fa-caret-right');
    $(this).closest('li').children('ul').toggle();
});
```

Result: arrow click → accordion toggle only; text click → navigates to section index page normally.

**Lesson:** `e.stopPropagation()` on a child element inside `<a>` prevents the click from bubbling to `<a>`, blocking navigation — without applying `return false` to the `<a>` itself. Section pages with children remain navigable via text click.

---

## ✅ 2026-03-03: Performance issue – search index loaded at page load

**Symptom:** Noticeable latency on every page load.

**Root cause:** `search.js` with `defer` called `$.getJSON()` immediately after page load, fetching the entire search index on every page visit.

**Fix:** Lazy-load the index — `initLunr()` is now called only on the first `focus` event on the search field (`$.one("focus", initLunr)`). Flags `searchIndexLoading`/`searchIndexLoaded` prevent double-fetching. All search scripts retain `defer` to preserve execution order relative to jQuery.

**Lesson:** Use `$.one("focus", initFn)` to defer heavy initialisation until the user actually interacts with the feature.

---

## ✅ 2026-03-03: Sidebar scrollbar visible

**Fix:** Added `!important` to `scrollbar-width: none`, extended webkit rule to cover all descendants (`#sidebar *::-webkit-scrollbar`), and added a JS fallback in `footer.html` to clear inline `overflow`/`height` styles set by Altinn scripts.

---

## ✅ 2026-03-03: Scroll-fade showed solid white block in sidebar

**Root cause:** Used `#sidebar::after` (pseudo-element on scroll container). `position: sticky` on a pseudo-element behaves differently — produces a solid block instead of a gradient overlay.

**Fix:** Replaced with a real DOM element (`<div class="sidebar-scroll-fade hidden">`) inside `.highlightable`, matching the technique already used for the TOC fade.

---

## ✅ 2026-03-03: GitHub edit link displaced far down in centre panel

**Root cause:** `theme.css` sets `#top-github-link { top: 50%; transform: translateY(-50%) }`, pushing the link ~50% of the panel height below its natural position.

**Fix:** Override in `custom-head.html`: `position: static !important; top: auto !important; transform: none !important`.

---

## ✅ 2026-03-03: Dropdowns and JS broken when jQuery has `defer`

**Root cause:** Altinn scripts (`altinndocs.js` etc.) use `$()` directly without `.ready()`. When jQuery was `defer` but these scripts were synchronous, `$` was undefined and DOM manipulation failed silently. `custom-footer.html` used `$(document).ready()` — invalid in an inline script when jQuery is deferred.

**Fix:** Added `defer` to all Altinn scripts. Rewrote `custom-footer.html` from jQuery to vanilla JS.

---

## 2026-03-02: Search not working (jQuery defer conflict)

**Symptom:** Search field accepted input but returned no results.

**Root cause:** jQuery loaded with `defer` in `header.html`, but `search.js`, `lunr.min.js`, and `horsey.js` were loaded synchronously. `search.js` ran before `$` (jQuery) was available → `$.getJSON()` threw an error → `lunrIndex` remained `null` → silent failure.

**Fix:** Added `defer` to all three search scripts in `layouts/partials/search.html`.

**Lesson:** When one script has `defer`, all scripts depending on it must also have `defer`.

---

## Procedure: GitHub Pages stuck deploy

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

## Windows: `git mv` fails for directories with many files

Use `cp -r` + `git rm` + `git add` instead.
