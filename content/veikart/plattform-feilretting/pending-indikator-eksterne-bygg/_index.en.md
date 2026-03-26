---
id: f2ecebba-c800-416c-94fb-6e32d36576b2
title: "Pending indicator does not detect builds triggered outside the site editor"
linkTitle: "Pending indicator: external builds"
weight: 87
status: "Approved"
lastmod: 2026-03-21T01:11:16+01:00
last_editor: erikhag1git (Erik Hagen)

---

The pending indicator at the bottom left («1 change being built») only updates when the user saves via the site's built-in editor – because it is driven by `localStorage` state set by `samtuIncrementPending()`. Builds triggered externally – by a direct commit in the GitHub web UI, a local push, or an API call – are not shown in the indicator.

The build history dialog, however, correctly shows these jobs (with live second counting), because it fetches directly from the GitHub Actions API.

## Consequence

A user sitting on the site sees «Build history» in idle state even when a build is actually in progress. The indicator gives a misleading impression that everything is quiet – and the page is not automatically reloaded when the build finishes.

## Proposed solution

Extend the background polling (which already runs every 45 seconds for ETag changes) to also check the GitHub Actions API for active builds:

1. Fetch `/repos/SAMT-X/samt-bu-docs/actions/workflows/hugo.yml/runs?per_page=3&status=in_progress` (requires token)
2. If there are active runs that are **not** in `localStorage` pending state (i.e. not triggered by this browser):
   - Update the indicator to show «Build in progress» (without a pending counter – not our change)
   - Start URL poll / ETag poll to detect when the page is updated
   - Show auto-reload and sound signal as usual when the build finishes

### Distinguishing own vs. others' builds

| Source | Handling |
|--------|---------|
| Own build (via editor) | As today – `localStorage` pending state, counter, fanfare |
| Others' builds (external) | New flow – indicator without counter, discrete sound on completion |
| Own build directly in GitHub | Same as others' builds (no `localStorage` entry) |

### Prerequisite

The user must be logged in (token available) for the background polling to call the GitHub API. For non-logged-in users: no change from current behaviour.

## Implemented (2026-03-21) – theme commit `b600033`

> **Note – not yet tested in practice.** The feature is implemented and deployed, but has not been verified with an actual external build. Test by pushing a change directly to GitHub while another browser tab is open and logged in on the site.

**New function: `checkExternalBuilds()`** called from background polling every 45 seconds (when no own build is in progress and user is logged in):

1. Fetches `/actions/workflows/hugo.yml/runs?per_page=3` from GitHub API
2. If an active build (`in_progress`/`queued`) is found: shows a discrete `samtuShowExternalBuildIndicator()` and starts `startBgFastPoll()` (ETag poll every 5 seconds)
3. `bgFastTimer` detects ETag change → auto-reloads the page (no banner)
4. If build is complete by the next bgTimer tick and `bgExternalRun` is set: auto-reloads instead of showing banner

**Visual details:**
- External indicator: spinner + «Site updating…» with `opacity: .7` (vs. full opacity for own builds)
- External indicator uses `data-external` attribute, not `data-building` → does not block background polling
- No fanfare or sound signal (silent auto-reload)

**Limitation (as planned):** Requires a logged-in user (token) to call the GitHub API. Non-logged-in users: unchanged behaviour.

## Related

- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html` – `checkExternalBuilds()`, `startBgFastPoll()`, `stopBgFastPoll()`, `samtuShowExternalBuildIndicator()`
- Roadmap: [False build failure on timeout](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/veikart/bygg-feil-timeout/) – related GitHub API polling
- Roadmap: [Status reporting and build queues](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/veikart/statusrapportering-gui/) – background
