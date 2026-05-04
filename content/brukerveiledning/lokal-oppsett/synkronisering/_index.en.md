---
# id: auto-generated – copied values are overwritten automatically on push
id: d9520a6b-e499-4554-961d-86a7bacc5550
title: "Synchronisation and Conflict Handling"
linkTitle: "Synchronisation"
weight: 10
lastmod: 2026-05-04T22:59:22+02:00
last_editor: Erik Hagen

---

Content in SAMT-BU Docs lives in Git repositories. When several contributors work at the same time – or when someone saves a change via the browser interface while you have a local copy – the repositories can fall out of sync. This page explains what happens and how to handle it.

## The Helper Scripts

In the root folder of your local clones you will find three scripts that simplify working with all repositories together:

| Script | Function |
|--------|----------|
| `pull-all.sh` / `.bat` | Fetches the latest changes from GitHub for all repositories |
| `push-all.sh` / `.bat` | Pushes unpushed local commits to GitHub |
| `sync-all.sh` / `.bat` | Combined: fetches, merges, and pushes in the correct order |

Run the `.bat` files from File Explorer (double-click), or the `.sh` files from Git Bash.

## Recommended Workflow

```
Before you start:   sync-all
While working:      commit frequently  →  push-all
When you are done:  sync-all
```

The most important rule is to **run sync-all before you start editing**, not just afterwards.

## What `sync-all` Does – Step by Step

| Situation | Action |
|-----------|--------|
| Same locally and on GitHub | Nothing – already synchronised |
| Only GitHub ahead | `git pull` (fast-forward) |
| Only you ahead | `git push` |
| Both have new commits | Rebase – your commits placed on top |
| You have uncommitted changes | Temporary stash → sync → stash pop |
| Unresolvable conflict | Stop, report, no data lost |

**Rebase** is used instead of a regular merge to produce clean, linear history.

## What is a Git Conflict?

A conflict occurs when **the same line in the same file** has been changed on both sides since the last sync. Git cannot determine which version is correct and stops.

### Common scenarios

- You edit a paragraph locally. At the same time, someone saves the same page via the browser editor.
- Two contributors change the `weight` value on the same page independently.
- You and a colleague work on different parts of `hugo.toml` at the same time.

### The scenario that does *not* create a Git conflict, but is still a problem

**Cross-linking:** Someone adds a link pointing to a page you have just renamed. Git sees no conflict, but the link is broken. Coordinate name changes with affected contributors.

## Manual Conflict Resolution

```bash
cd "<path to repo>"

git pull --rebase
# Open the file(s) and look for conflict markers:
#
#   <<<<<<< HEAD          ← your local version
#   Your content
#   =======
#   Content from GitHub
#   >>>>>>> abc1234
#
# Delete the markers and keep what is correct.

git add <filename>
git rebase --continue
git push
```

**Tip:** VS Code has a built-in merge tool – click «Accept Current», «Accept Incoming», or «Accept Both» per conflict block.

## Special Cases

### `go.mod` and `go.sum`

```bash
git pull --rebase
git checkout --theirs go.mod go.sum
hugo mod tidy
git add go.mod go.sum
git rebase --continue
git push
```

### `hugo.toml`

If two contributors have added **different** sections, both should be kept. Delete the conflict markers and ensure both additions are present.

### UUID workflow and rejected pushes

When you push new Markdown files, GitHub Actions runs automatically and commits UUID fields. If you push twice in quick succession you may get a rejection:

```bash
git pull --rebase
git push
```

**Prevention:**

```bash
git add <files>
git commit -m "..."
git pull --rebase
git push
```

### Browser editing vs. local editing

Editing via the «Edit» menu commits directly to `main`. Resolved by `sync-all` via rebase – works automatically unless you have changed exactly the same lines. **Always run `sync-all` immediately before starting local edits.**

## Why Not Just "Always Keep My Version"?

It is possible to configure automatic conflict resolution that always chooses your local version (`-X ours`). We have opted against this because it **silently discards others' changes**. Better to stop and let a human decide.
