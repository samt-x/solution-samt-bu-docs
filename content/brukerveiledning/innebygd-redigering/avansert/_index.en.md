---
# id: auto-generated – copied values are overwritten automatically on push
id: 9080238f-b1aa-4a19-bc88-f27718fb6222
title: "Built-in Editor – Advanced Use"
linkTitle: "Advanced Use"
weight: 10
lastmod: 2026-05-04T22:59:22+02:00
last_editor: Erik Hagen

---

This page covers advanced aspects of the built-in editor. It assumes you are familiar with the basics from [Built-in Editor](../) and focuses on topics you will encounter as you use the tool more.

## Contribution Flow for Users Without Write Access

Users with a GitHub account but without direct write access to the repository can contribute through exactly the same interface. The system detects the permission level automatically when the Edit menu is opened and adjusts the menu labels accordingly:

| With write access | Without write access |
|-------------------|----------------------|
| Edit this page | Suggest change to this chapter |
| New chapter after this | Suggest new chapter after this |
| New sub-chapter | Suggest new sub-chapter |
| Delete this page | Suggest deletion of this page |

### What happens technically

Instead of committing directly to `main`, the system automatically creates a branch and a pull request. The user sees «✓ Pull request sent» and a clickable link to the PR after saving. An editor with write access reviews the suggestion and approves or rejects it on GitHub.

### Limitation: the Move function

«Move this chapter» does not support the suggestion flow and is only available to users with write access.

### Handling incoming suggestions (for editors)

Suggestions appear as open pull requests in the relevant repository on GitHub. When you approve and merge a PR, the site's build pipeline triggers automatically and the change is published within approximately 1 minute.

## Bilingual Editing

The site is bilingual (Norwegian and English). Each page exists in two versions – one Norwegian and one English – linked via a shared UUID field.

**Practical consequence:** When you create or edit a page, you change only one language version at a time. The other remains unchanged.

**Recommended workflow for a new page:**

1. Create the page in Norwegian (via «New chapter» or «New sub-chapter»)
2. Add Norwegian content and save
3. Switch to English via the language selector in the header
4. Open the corresponding English page and edit it in the same way

If you only create one language version, the other will show a blank page to visitors using that language.

## Bilingual Editing – Moving and Deleting

**Moving:** The Move function operates on both language versions simultaneously – one action covers both.

**Deleting:** Deletion always removes both language versions in a single step.

## The Status Field – Use Cases Only

Use-case pages (under «Behov») have a status field that controls the symbol shown in the menu. All other pages should have an empty status field.

| Symbol | Norwegian value | English value |
|--------|-----------------|---------------|
| ◍ | Ny | New |
| ◔ | Tidlig utkast | Early draft |
| ◐ | Pågår | In progress |
| ◕ | Til QA | For QA |
| ⏺ | Godkjent | Approved |
| ⨂ | Avbrutt | Cancelled |

## The UUID Field – Do Not Touch It

All pages have a hidden `id` field (UUID). It is invisible in the editing dialog and is set automatically. The UUID is permanent – it links the Norwegian and English versions of the same page.

## Sort Order (`weight`)

The `weight` field determines the order in the sidebar menu. Lower number = higher up.

**Rule of thumb:** Use steps of ten (10, 20, 30 …) to leave room for later insertions. You can adjust the `weight` field directly in the editing form to reorder a page without using the Move function.

## Images

Images can be pasted directly into the text field (Ctrl+V). They are uploaded automatically and embedded in the page.

For best quality: PNG for screenshots and diagrams, JPEG for photographs.

## Markdown in the Text Field

The text tool (TipTap) displays content visually but saves it as Markdown. You can use the toolbar buttons, or type Markdown syntax directly:

| Markdown | Result |
|----------|--------|
| `**text**` | **bold text** |
| `*text*` | *italic text* |
| `# Heading` | Heading level 1 |
| `## Heading` | Heading level 2 |
| `` `code` `` | `code` |
| `[link text](url)` | Clickable link |

## Pitfalls

### Change not published

If you close the editing dialog without clicking «Save», your changes are discarded. There is no autosave.

### Build fails

If the status indicator shows a warning icon after saving, the change has been registered in Git but not published. The change is not lost – it is in the commit history and can be published again. Contact an administrator.

### Page deleted by mistake

Deletion via the interface is not immediately reversible. Contact an administrator – the page exists in the Git history and can be restored.

### Sort order does not seem to change

The browser may cache the sidebar menu. A hard reload (Ctrl+Shift+R) usually resolves this.
