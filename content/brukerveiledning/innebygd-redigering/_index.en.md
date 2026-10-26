---
# id: auto-generated – copied values are overwritten automatically on push
id: "c95d738e-1fe5-43ac-94a8-80202e0a2faa"
title: "Built-in Editing in the Browser"
linkTitle: "Built-in editing"
weight: 5
aliases:
  - /en/om/hvordan-bidra/innebygd-redigering/
  - /en/hvordan-bidra/innebygd-redigering/
lastmod: 2026-10-26T23:36:02+01:00
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
| Build failed | «⚠ Build failed», with an explanation at the bottom right |
| Your file was held back | «Your change could not be published», with the file name at the bottom right |

> If you see «Superseded» in the build history, your change has not been lost – it was published by a newer job.

The site counts a change as published when it appears in the build receipt (`/build.json`), which is published together with the pages. It follows your own saves from this browser, also when you move to other pages while the build is running.

**Sound signals:**

| When | Sound |
| --- | --- |
| Build starts | Two short beeps |
| All your changes are published | Fanfare and «Your updated documentation is now online» – once, also when you have saved several times |
| Build failed | Falling tones and «Build job failed» |

**When a file has an error:** A build includes every change that has been saved, including other people's. If one file has an error that would stop the build, only that file is held back. The page then shows its previous version, or is left out if it is new, and the rest of the site is published as normal. Changes made by others therefore do not stop yours.

If your file was held back, you see the message **«Your change could not be published»** with the file name, instead of «published». The error is reported automatically to the people who follow up, so you do not need to do anything. If you fix the error and save again, the page is published with the next build.

**Build failed:** Some errors cannot be held back this way, for example errors in the look or the setup of the site. You then see «⚠ Build failed», and no changes are published until the error is fixed. This is rare.

In both cases you can use **«Report it here»** in the message. You get an automatic reply right away with the status of the build, and someone in the project follows up.

## Suggestion Flow for Users Without Write Access

Users with a GitHub account but without direct write access can contribute through exactly the same interface. The system detects permission level automatically when the Edit menu is opened:

| With write access | Without write access |
|-------------------|----------------------|
| Edit this page | Suggest edit to this page |
| New chapter after this | Suggest new chapter after this |
| New sub-chapter | Suggest new sub-chapter |
| Delete this page | Suggest deletion of this page |

Instead of committing directly to `main`, the system automatically creates a branch and a suggestion. After saving, a confirmation with a link to the suggestion is shown.

> **Note:** The Move function does not support the suggestion flow.

**You are not notified when you submit.** A single email arrives, and only once the suggestion has been handled – approved or set aside. No action is needed on your part; everything has already been done.

## For editors – handling incoming suggestions

Select **"Handle suggestions"** under Project in the Edit menu. The item is only shown to users with write access.

The dialog lists all open suggestions across every content repository, with who submitted them and when. Each can be approved or declined, both with a two-step confirmation.

There is no need to go to GitHub to handle suggestions.

Once you choose, three things happen automatically:

1. The suggestion is given an explanatory title, so the contributor's email has a subject line that makes sense
2. The change is included, and the site rebuilds
3. A friendly message is left for the contributor – **a couple of minutes later**, not immediately

The delay is deliberate: posted immediately, the contributor receives two emails instead of one. You do not have to wait or keep the tab open – the message is queued and sent even if you close the browser.

**If the suggestion conflicts** with content changed in the meantime, it cannot be merged automatically. For now, such cases have to be resolved in GitHub.

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

If you have a GitHub user, you can also report it directly with the form **Problem** in [solution-samt-bu-docs](https://github.com/samt-x/solution-samt-bu-docs/issues/new?template=6-problem.yml). Choose «Programvare eller verktøy virker ikke» (software or tool does not work) in the list of kinds of problem. See the [User guide for task management](https://docs.samt-bu.no/en/prosjektleveranser/loesninger/samhandlingsplattform/oppgavestyring/brukerveiledning/).

> A dedicated "Report a bug" menu option is being planned.
