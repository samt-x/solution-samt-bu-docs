---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: 2f548bce-3bc1-4603-806b-ff0347a5bdf5
title: "False «Build job failed» on long build jobs"
linkTitle: "False build failure on timeout"
weight: 85
status: "Approved"
lastmod: 2026-03-27T23:29:13+01:00
last_editor: Erik Hagen

---

The pending indicator reports «Build job failed» after the ETag polling has reached its maximum number of attempts – even though the build is still running or has completed successfully. The timeout (180 attempts × ~1 sec = 3 min) is not a reliable proxy for build failure.

## Root cause

`startGhPoll()` / ETag polling in `custom-footer.html` counts attempts and gives up after a fixed limit:

```javascript
if (++attempts > 180) {
    // shows "Build job failed"
}
```

This is a timeout heuristic, not an actual status check. Builds taking more than 3 minutes (e.g. with many module repos, a slow runner, or a queue) will always trigger a false failure.

## Correct solution

Replace the timeout logic with a direct check against the GitHub Actions API. Report failure only if GitHub itself says `conclusion: failure` (or `cancelled` without a subsequent success).

### Proposed flow

1. ETag poll detects that the page has changed (build complete) → continue as today
2. ETag poll reaches the maximum limit → do **not** report failure directly
3. Instead: make one call to `/repos/SAMT-X/samt-bu-docs/actions/workflows/hugo.yml/runs?per_page=1`
4. Check `conclusion` on the latest run:
   - `success` → show «Changes published», reload the page
   - `failure` → show error message
   - `null` (still running) → reset counter and continue polling
   - `cancelled` → handle as today (wait for new build)

### Alternative simplification

Remove the maximum limit entirely and rely solely on GitHub API polling (`checkCompletions()` / `startGhPoll()`). ETag polling is only for detecting that the page has actually updated – not for detecting failures.

## Implemented (2026-03-21) – theme commit `414fa54`

**ETag poll (editing, 180s limit):** On timeout, the poller now calls the GitHub Actions API and checks actual status:
- `in_progress` / `queued` → reset counter and continue ETag polling
- `completed/success` → call `onBuildDone()` directly
- `completed/cancelled` → reset and show «Cancelled – waiting for new build…»
- `completed/failure` → show actual error message

**URL poll (new page, 90s limit):** Same pattern introduced in `startUrlPoll()`. Now accepts an optional `startTime` parameter for correct run filtering; `npPollBuild()` passes `startTime` when calling.

A `_checkingApi` flag prevents concurrent API calls while the interval continues running.

## Related

- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html` – `startGhPoll()`, `startUrlPoll()`, ETag polling
- Roadmap: [Status reporting and build queues](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/veikart/statusrapportering-gui/) – background on current polling architecture
