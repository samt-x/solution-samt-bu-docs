---
# id: auto-generated – copied values are overwritten automatically on push
id: c794131f-0639-4f6f-b87e-4031deea5a65
title: "«Add comment» in the Edit menu via GitHub Issues"
linkTitle: "Add comment (issues)"
weight: 96
status: "New"
# Valid values: New | Early draft | In progress | For QA | Approved | Cancelled
lastmod: 2026-04-19T00:00:00+02:00
last_editor: Erik Hagen

---

A new «Add comment» menu item in the Edit menu lets logged-in users submit feedback on a page without editing the content directly. The comment is created as a GitHub Issue in the correct repo.

## User flow

1. User clicks «Add comment» in the Edit menu
2. A simple dialog opens with a free-text field
3. Title is pre-filled with the page title and a link to the page
4. On submit: `POST /repos/SAMT-X/{repo}/issues` creates the issue
5. User sees confirmation with a link to the created issue

## Technical

- Same authentication and permission pattern as other operations
- Only requires the user to be logged in – not necessarily write access to the repo
- GitHub Issues are open for all authenticated users to create (if the repo has issues enabled)
- Pre-filled body: page title + URL + free text from user

## Related

- Can be combined with conflict notifications in the PR flow
- Foundation for a future «Admin» switcher showing open issues per page
