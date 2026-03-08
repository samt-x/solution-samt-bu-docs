---
id: 36ddabdf-4ceb-45bb-b55f-051cd9976078
title: "Add sub-chapter – option in the Edit menu"
linkTitle: "Add sub-chapter"
weight: 10
status: "Early draft"
---

When reading a page on the site, there is no easy way to create a new sub-chapter under the current page. This roadmap item describes the need, chosen solution, and the rationale behind the choice.

## Background

The «Edit» menu in the header currently offers two options: «This page» (deep-link to the Decap CMS editor for the current page) and «Other options» (CMS portal overview). A natural next step in the editorial workflow – creating a new sub-chapter under the page being read – is missing.

## Chosen solution

A dynamic link in `edit-switcher.html` that opens GitHub's «create file» interface at the correct path:

```
https://github.com/<org>/<repo>/new/main/content/<path-to-current-page>/
```

GitHub opens an empty file editor where the user types the filename (e.g. `new-chapter/_index.en.md`) and frontmatter. The link is built dynamically from `.File.Path` in the Hugo template, in the same way as the existing Decap deep-link.

**Remaining work:**

- Add new menu option in `edit-switcher.html` (the theme) for all four portal conditions
- Test that the link works correctly for module pages (where the repository differs from `samt-bu-docs`)
- Consider whether the option should appear on all pages, or only where it makes sense
- Corresponding «Legg til underkapittel» option for the Norwegian menu

## Alternatives considered

**Decap CMS «New» link** – link to `<portal>#/collections/<collection>/new`. Creates a new page in the Decap CMS editor.

**GitHub «create file» link** *(chosen)* – link to `github.com/<org>/<repo>/new/main/content/<path>/`. Opens GitHub's file editing interface directly at the correct path.

## Rationale

The Decap CMS alternative always creates at the root level of the collection – the user must then navigate manually to the correct subfolder, which is error-prone and unintuitive. The GitHub link places the user directly in the correct directory in the repository, without detours. Since the target audience (technical editors and developers) is already familiar with GitHub, this is an acceptable approach.
