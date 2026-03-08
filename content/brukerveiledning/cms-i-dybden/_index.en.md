---
id: 9080238f-b1aa-4a19-bc88-f27718fb6222
title: "CMS in Depth"
linkTitle: "CMS in Depth"
weight: 10
---

Decap CMS is the browser-based editing tool for SAMT-BU Docs. This page covers functionality and pitfalls that are not immediately obvious at first glance.

## The Six CMS Portals

Content is distributed across six portals – one per repository and language. There is no single "super-portal" covering everything; you must use the correct portal for the correct content.

| Portal | Language | Covers | Open via |
|--------|----------|--------|----------|
| Docs (nb) | Norwegian | Main part of the samt-bu-docs repository | "Endre" → "Andre valg" |
| Docs (en) | English | Main part of the samt-bu-docs repository | "Edit" → "Other options" |
| Architecture (nb) | Norwegian | The team-architecture repository | "Endre" → "Andre valg" |
| Architecture (en) | English | The team-architecture repository | "Edit" → "Other options" |
| Drafts (nb) | Norwegian | The samt-bu-drafts repository | "Endre" → "Andre valg" |
| Drafts (en) | English | The samt-bu-drafts repository | "Edit" → "Other options" |

**The "This page" shortcut** in the Edit menu takes you directly to the current page in the correct portal, regardless of which portal and section is involved. This is the fastest way to edit an existing page.

## Bilingual Editing

The website is bilingual (Norwegian and English). CMS portals are separated by language – there is no automatic translation.

**What this means in practice:**

- Create the page in the Norwegian portal (e.g. Docs nb) and save
- Switch to the English portal (Docs en) and create the same page with English content
- The UUID field (`id`) links the two language versions – it is set automatically and must not be changed

If you only create one language version, the page will be missing content in the other language (users who switch language will see a blank page or an error).

## The Status Field and Status Symbols

Only use-case pages (under "Behov") use the status field. Valid values:

| Symbol | Norwegian value | English value |
|--------|-----------------|---------------|
| ◍ | Ny | New |
| ◔ | Tidlig utkast | Early draft |
| ◐ | Pågår | In progress |
| ◕ | Til QA | For QA |
| ⏺ | Godkjent | Approved |
| ⨂ | Avbrutt | Cancelled |

The symbol is generated automatically from the value – you only need to select the correct text in the CMS. All other pages should have an empty status field.

## Saving and Publishing – the Timeline

```
You click "Save" in the CMS
    ↓  (a few seconds)
Decap CMS creates a commit on GitHub
    ↓  (1–3 minutes)
GitHub Actions builds the website
    ↓
New version is live at samt-x.github.io/samt-bu-docs/
```

You can monitor the build under the **Actions** tab in the GitHub repository. If the build fails (red X), the change has not been published – contact an administrator.

## The UUID Field – Do Not Touch It

All pages have a hidden `id` field (UUID). It is invisible in the CMS editor (`widget: hidden`) and is set automatically by a GitHub Actions workflow. The UUID is permanent – it links the Norwegian and English versions of the same page and may be used for cross-references.

You will never see this field in the CMS, and you do not need to think about it.

## Pitfalls and Known Limitations

### Test content after a CMS session

Decap CMS saves directly to the `main` branch. If you have tested features or written incomplete drafts without deleting them, these may end up on the website. **Always check `git diff` (or the GitHub commit history) after a CMS session** if you are unsure what was saved.

### Sort order (`weight`)

Pages in the CMS list can be sorted by the `weight` field (which corresponds to the order in the sidebar menu). Lower number = higher up. If you do not set `weight`, the page will appear at the bottom.

### New page vs. new folder

In Hugo, each page is a **folder** containing an `_index.en.md` file. The CMS does **not** create folders automatically – you must create the folder structure manually (e.g. via GitHub or locally) and then edit the content in the CMS.

A folder containing only `_index` file(s) but no body text will be displayed as a normal page with a title, "Last modified" date, and UUID – but with an empty content area. This is not an error, simply a page that has not yet received any content.

### Local test environment

The CMS supports local testing: run `hugo server` and open the portal in the browser, then click "Work with Local Repository". Changes are then saved directly to your local file system (not GitHub) and you can see them live in the preview without committing.
