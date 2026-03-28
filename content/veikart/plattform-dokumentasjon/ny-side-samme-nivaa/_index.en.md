---
# id: auto-generated – copied values are overwritten automatically on push
id: 3b8fe53a-65b0-46cd-ad31-ef3847775772
title: "New page at the same level – option in the Edit menu"
linkTitle: "New page – same level"
weight: 20
status: "Early draft"
lastmod: 2026-03-28T10:12:28+01:00
last_editor: Erik Hagen

---

When reading a page, there is no easy way to create a new page at the same level (a sibling page). This roadmap item is closely related to [Add sub-chapter](../legg-til-underkapittel/) and should be resolved in the same iteration.

## Chosen solution

The same approach as for sub-chapters: a dynamic GitHub «create file» link, but pointing to the **parent folder** instead of the current folder:

```
https://github.com/<org>/<repo>/new/main/content/<parent-path>/
```

The parent path is computed in the Hugo template as `path.Dir` of the current page's relative path.

**The option is hidden** on root-level pages (where creating siblings does not make sense).

## Remaining work

- Replace the current alert popup with an actual GitHub link in `edit-switcher.html`
- Test for all four portal conditions (docs, arkitektur, utkast, loesninger)
- Coordinate with the implementation of «Add sub-chapter» – should be done at the same time
