---
# id: auto-generated – copied values are overwritten automatically on push
id: "c95d738e-1fe5-43ac-94a8-80202e0a2faa"
title: "Built-in Editing in the Browser"
linkTitle: "Built-in editing"
weight: 5
aliases:
  - /en/om/hvordan-bidra/innebygd-redigering/
  - /en/hvordan-bidra/innebygd-redigering/
lastmod: 2026-05-05T00:41:49+02:00
last_editor: Erik Hagen

---

You edit content directly in the browser using a visual text editor – no knowledge of Markdown or Git required. All common editorial tasks are available from the **"Edit"** menu in the top-right corner of the header.

## What You Need

- A **GitHub account** (create one for free at [github.com](https://github.com)) – that is all you need

**Write access is not required.** Without it, your changes are automatically submitted as a *suggestion* (pull request) for an editor to review and approve. With write access, changes are published directly. Either way, the same interface is used – menu labels adjust automatically.

### About GitHub authorisation

The first time you use the editing features, SAMT-BU Docs will request access to your GitHub account via a login popup. SAMT-BU Docs uses a **GitHub App** that only has access to the specific repositories the app is installed on – not other repositories on your account.

#### Revoking authorisation

You can revoke access at any time:

1. Log in to [github.com](https://github.com)
2. Go to **Settings** (click your profile picture in the top right → *Settings*)
3. Select **Applications** in the left menu
4. Click the **Authorized GitHub Apps** tab
5. Find **SAMT-BU Docs** in the list and click **Revoke**

## Editing an Existing Page

1. Go to the page you wish to edit
2. Click the **"Edit"** menu in the top-right corner of the header
3. Select **"Edit this page"**
4. Log in with your GitHub account if you are not already logged in (pop-up window)
5. Make your changes in the visual editor
6. Click **"Save"**

If you have write access, the change is published directly. Without write access, a pull request is created automatically – you will receive a link to it after saving.

The website updates automatically after saving. A status indicator at the bottom left of the screen keeps you informed.

## Images

Paste images directly into the text field (Ctrl+V). They are uploaded automatically and embedded in the page.

Use PNG for screenshots and diagrams, JPEG for photographs.

## Creating a New Page

1. Navigate to the page you want to place the new page next to (sibling) or beneath (sub-chapter)
2. Click **"Edit"** and select:
   - **"New chapter after this"** – new page at the same level as the current one
   - **"New sub-chapter"** – new page one level down beneath the current one
3. Fill in the title and any content in the dialog
4. Click **"Save"**

## Moving a Chapter

1. Go to the page you want to move
2. Click the **"Edit"** menu in the top-right corner
3. Select **"Move this chapter"** – a dialog opens and the Edit menu is greyed out
4. Navigate in the menu to the desired location
5. Click **"Move here (before)"** or **"Move here (after)"**

> **Note:** The Move function requires write access and does not support the suggestion flow.

## Deleting a Page

1. Go to the page you want to delete
2. Click the **"Edit"** menu in the top-right corner
3. Select **"Delete this page"**
4. Confirm in the dialog

Both language versions are deleted in a single step.

> **Note:** Deletion cannot be immediately reversed through the interface. Contact an administrator if you have accidentally deleted a page.

## Give Feedback

Use **"Give feedback"** in the Edit menu to submit a comment without editing directly. The comment is registered as a GitHub Issue linked to the page.

## Status Indicator and Build History

The indicator at the bottom left shows build status. A build normally takes **about 1 minute**.

| State | Text |
|-------|------|
| No active job | «Build history» |
| Waiting for build | «N changes being built…» |
| Done | «Changes published – click to reload» |

> If you see «Superseded» in the build history, your change has not been lost – it was published by a newer job.

## Suggestion Flow for Users Without Write Access

Users with a GitHub account but without direct write access can contribute through exactly the same interface. The system detects permission level automatically when the Edit menu is opened:

| With write access | Without write access |
|-------------------|----------------------|
| Edit this page | Suggest change to this chapter |
| New chapter after this | Suggest new chapter after this |
| New sub-chapter | Suggest new sub-chapter |
| Delete this page | Suggest deletion of this page |

Instead of committing directly to `main`, the system automatically creates a branch and a pull request. After saving, the user sees «✓ Pull request sent» and a link to the PR.

> **Note:** The Move function does not support the suggestion flow.

**For editors – handling incoming suggestions:** Suggestions appear as open pull requests in the relevant repository on GitHub. Approve and merge the PR – the site builds automatically and the change is published within approximately 1 minute.

## Bilingual Editing

The site is bilingual (Norwegian and English). Each page exists in two versions linked via a shared UUID field. When you create or edit a page, you change only one language version at a time.

**Recommended workflow for a new page:**

1. Create the page in Norwegian
2. Add Norwegian content and save
3. Switch to English via the language selector in the header
4. Open the corresponding English page and edit it

The Move function and deletion operate on both language versions simultaneously.

## Status Field – Use Cases Only

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

All pages have a hidden `id` field set automatically. It is invisible in the editing dialog and links the Norwegian and English versions of the same page permanently.

## Sort Order (`weight`)

`weight` determines the order in the sidebar menu. Lower number = higher up. Use steps of ten (10, 20, 30 …) to leave room for later insertions.

## Report a Bug

If something does not work as expected, use **"Give feedback"** in the Edit menu and describe what happened. The report is registered as an issue and followed up by the team.

> A dedicated "Report a bug" menu option is being planned.
