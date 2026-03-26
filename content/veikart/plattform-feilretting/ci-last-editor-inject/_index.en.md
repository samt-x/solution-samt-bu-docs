---
id: 7ee1e5cc-73be-463b-99bd-913dbfc73076
title: "CI injection of last_editor for non-CMS edits"
linkTitle: "CI: last_editor for all edit channels"
weight: 75
status: "New"
last_editor: erikhag1git (Erik Hagen)
lastmod: 2026-03-20T09:42:59+01:00

---

## Background

The `last_editor` field in frontmatter is currently only set by the built-in CMS editor. Pages edited via the GitHub web UI, GitHub API, or a local clone → push have had the field set via `fix-last-editor.py` (a one-time batch run), but new edits through these channels will lack `last_editor` until they are edited again via the CMS.

## Goal

Ensure that `last_editor` is set correctly regardless of which editing channel is used – without the editor having to do anything extra.

## Proposed solution

A new step in `hugo.yml` (and `trigger-docs-rebuild.yml`):

When a human push triggers the workflow (`github.actor` ≠ `github-actions[bot]`):

1. Fetch the pusher's display name via GitHub API: `GET /users/{github.actor}`
2. Build the `last_editor` value: `login (name)` or `login (unknown name)`
3. For each `.md` file changed in the push (from `git diff --name-only HEAD~1 HEAD`):
   - Set `last_editor` if the field is missing or has a bot value
   - Retain existing human values
4. Commit with `[skip ci]` tag (same pattern as ensure-uuids)

## Covers all editing channels

| Editing channel | Covered by |
|----------------|-----------|
| Built-in CMS editor | Already implemented (writes `last_editor` on save) |
| GitHub web UI | This measure |
| GitHub API | This measure |
| Local clone → push | This measure |
| Bot commits | Filtered out (not injected, not shown) |

## Related

- `.github/scripts/fix-last-editor.py` – batch version of the same logic (run once)
- `.github/scripts/inject-lastmod.py` – equivalent pattern for the `lastmod` field
- `themes/hugo-theme-samt-bu/layouts/partials/header.html` – display logic
