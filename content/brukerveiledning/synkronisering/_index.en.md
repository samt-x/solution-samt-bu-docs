---
id: d9520a6b-e499-4554-961d-86a7bacc5550
title: "Synchronisation and Conflict Handling"
linkTitle: "Synchronisation"
weight: 20
last_editor: erikhag1git (Erik Hagen)
lastmod: 2026-03-15T23:49:44+01:00

---

Content in SAMT-BU Docs lives in Git repositories. When several contributors work at the same time – or when Decap CMS saves a change while you have a local copy – the repositories can fall out of sync. This page explains what happens and how to handle it.

## The Helper Scripts

Under `S:\app-data\github\samt-x-repos\` you will find three scripts that simplify working with all repositories together:

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

The most important rule is to **run sync-all before you start editing**, not just afterwards. This ensures you are always on top of what others have done, and the merging of your new changes will rarely fail.

## What `sync-all` Does – Step by Step

For each repository, the script determines the situation after fetching the remote status:

| Situation | Action |
|-----------|--------|
| Same locally and on GitHub | Nothing – already synchronised |
| Only GitHub ahead | `git pull` (fast-forward, no merge commit) |
| Only you ahead | `git push` |
| Both have new commits | Rebase – your commits are placed on top of the GitHub changes |
| You have uncommitted changes | Temporary stash → sync → stash pop |
| Conflict that cannot be resolved automatically | Stop, report, no data lost |

**Rebase** is used instead of a regular merge because it produces a clean, linear history without unnecessary merge commits.

## What is a Git Conflict?

A conflict occurs when **the same line in the same file** has been changed on both sides (locally and on GitHub) since the last sync. Git cannot determine which version is correct and stops.

Git is, however, good at merging changes that affect **different lines** in the same file automatically – this normally requires no action from you.

### Common scenarios where conflicts arise

- You edit a paragraph locally. At the same time, someone saves the same page via Decap CMS.
- Two contributors change the weight value (`weight`) on the same page independently.
- You and a colleague work on different parts of `hugo.toml` at the same time.

### The scenario that does *not* create a Git conflict, but is still a problem

**Cross-linking:** Someone adds a link in the `team-architecture` repository pointing to a page you have just renamed in `samt-bu-docs`. Git sees no conflict – both changes are valid. But the link is now broken. This is only detected when building (`hugo` reports broken internal links) or by manual inspection. Coordinate name changes with affected contributors.

## Manual Conflict Resolution

When `sync-all` reports a conflict, nothing has been changed – the rebase has been aborted and you are back to your starting point. The script shows which files conflicted.

**How to resolve it:**

```bash
cd "S:/app-data/github/samt-x-repos/<repo-name>"

# Start the rebase again
git pull --rebase

# Git stops and marks the conflicting files.
# Open the file(s) and look for the conflict markers:
#
#   <<<<<<< HEAD          ← your local version
#   Your content here
#   =======
#   Content from GitHub
#   >>>>>>> abc1234       ← remote commit
#
# Delete the markers and keep whatever is correct (can be both).

# Mark the file as resolved and continue
git add <filename>
git rebase --continue

# Push when the rebase is complete
git push
```

**Tip:** VS Code has a built-in merge tool. Open the conflicting file there and click "Accept Current", "Accept Incoming", or "Accept Both" for each conflict block.

## Special Cases

### `go.mod` and `go.sum` (Hugo module conflicts)

These files control which versions of content modules (team-architecture, samt-bu-drafts, etc.) are in use. Conflicts here are technical, not content-related.

**Solution:**

```bash
git pull --rebase
# Conflict in go.mod/go.sum → choose the remote version and regenerate:
git checkout --theirs go.mod go.sum
hugo mod tidy
git add go.mod go.sum
git rebase --continue
git push
```

### `hugo.toml` (configuration conflicts)

The configuration file is structured with sections. If two contributors have added **different** sections, both should be kept. Open the file, delete the conflict markers, and make sure both additions are present in the final file.

### Decap CMS vs. local editing

The CMS commits directly to `main`. If you have made local changes to the same file, this is the classic divergence scenario. It is resolved by `sync-all` via rebase – it works automatically unless you have changed exactly the same lines.

**Prevention:** Always run `sync-all` immediately before you start editing locally.

## Why Don't We Just "Always Keep My Version"?

It is possible to configure automatic conflict resolution that always chooses your local version (`-X ours`). We have opted against this because it **silently discards others' changes** – including valid CMS changes from colleagues. It is better to stop and let a human decide which version is correct.
