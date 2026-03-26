---
id: 1cfce35d-fbef-467a-8853-fff18ae46d28
title: "Status reporting and GUI for build queues"
linkTitle: "Status reporting and build queues"
weight: 130
status: "Approved"
last_editor: erikhag1git (Erik Hagen)
lastmod: 2026-03-20T09:42:59+01:00

---

The goal is to give users a simple overview of their own and others' queued jobs – with a compact status indicator (bottom left) and an event feed (bottom right) with sound and history.

## Observed behaviour (starting point 2026-03-17, after session 5)

1. **Dialog open, build started:** «Website is updating (N sec)...» in the dialog header + sound signal on start. Works well.
2. **Dialog closed / navigated away:** `#qe-job-indicator` always shows a visible button – «Build history» in idle state, build status during active builds.
3. **Click on indicator:** Opens the job history dialog with the last 15 builds for the logged-in user (GitHub Actions API).
4. **Build complete:** Sound signal + automatic navigation, regardless of whether the dialog is open or closed.

---

## Step 1 – Sound signal on build complete after navigation ✅ DONE (2026-03-17)

**Root cause (resolved):**

1. `samtuPlaySuccess()` was never called in the `checkCompletions()` completion branch.
2. `_samtuAudioCtx` was `null` on the new page (only created during a user gesture on the previous page).

**Implemented fix:**

- `checkCompletions()` completion branch now calls `samtuPlaySuccess()` + 1800ms delay before reload.
- `_samtuPlayNotes()` attempts to create a new `AudioContext` if it is `null` (Chrome allows this for origins with high user engagement).
- `samtuShowDoneIndicator()` is always shown as a visual fallback.

**Files changed:**
- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html`

---

## Step 2 – Job history and improvements ✅ DONE (2026-03-17, session 5)

### 2a – Job history button always visible ✅

`#qe-job-indicator` is now shown permanently (not only during active builds). Idle state: clock icon + «Build history». Click opens `#job-history-dialog` with the last 15 builds for the logged-in user fetched from the GitHub Actions API.

**Implementation details:**
- `data-building="1"` is set on the indicator by `samtuShowPendingIndicatorWithTotal()`, removed by `samtuShowDoneIndicator()`
- Background poll (`setInterval` every 45 sec) checks `qeInd.dataset.building` instead of `display !== 'none'` – prevents the always-visible indicator from blocking the others'-changes banner
- `samtuIncrementPending()` now calls `samtuShowPendingIndicator(newCount)` immediately – the indicator updates the moment you click Save, not only after dialog close/refresh

### 2b – Minimise removed ✅

The minimise functionality (`qe-minimize-pill`, `minimizeQeDialog()`, `⊟` button) has been removed. Reason: the pill disappeared on navigation and only added noise with double status. The Cancel button is again labelled «Close this window» after saving.

### 2c – ETag timeout increased ✅

`if (++attempts > 90)` → `if (++attempts > 180)` (3 min max). Fixes the false «Build job failed» signal for builds taking > 90 sec.

**Files changed (session 5):**
- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html`
- `themes/hugo-theme-samt-bu/layouts/partials/edit-switcher.html`

---

## Step 3 – Second counting, queue status, and cancellation handling ✅ DONE (2026-03-17, session 6)

### 3a – Second counting for running jobs ✅

A running job (`status: in_progress`) now shows the number of seconds since start (e.g. «47 sec»). Updated live every second via a re-render timer in the history dialog (no new API fetch – calculated from `run.created_at`).

### 3b – «In queue» status for waiting jobs ✅

Queued jobs (`status: queued`, `waiting`, `pending`, `requested`) now show:
- Clock icon (grey `fa-clock-o`) instead of spinner
- The text «In queue» instead of «running…» or a timestamp

The GitHub Pages environment uses `waiting` in addition to `queued` for jobs waiting on the concurrency group. Both (and `pending`/`requested`) are now treated identically.

### 3c – Cancellation handling ✅

**Background:** GitHub Pages automatically cancels older queued jobs when a newer job with higher priority is waiting («Canceling since a higher priority waiting request for pages exists»). Occurs with 3+ rapid saves.

**Implemented:**
- `conclusion: cancelled` → grey `fa-check-circle` (not red `fa-exclamation-circle`) + text «Cancelled»
- `checkCompletions()`: counts cancelled as resolved, clears the entire pending state when at least one success exists and no active jobs remain – pending counter no longer hangs
- `startGhPoll()`: a cancelled run does not trigger wah-wah + error message, but keeps polling and waits for a new build
- User guide (om/hvordan-bidra/) updated with an explanation of cancelled jobs and queue behaviour

### 3d – Live update of job history dialog ✅

`loadHistory()` split into `fetchHistory()` + `renderHistory(runs)`:
- `renderHistory` re-renders every second from cache (live elapsed counter without API calls)
- `fetchHistory` is re-fetched automatically every 15 sec while the dialog is open
- `openHistory()` / `closeHistory()` correctly clears timers on open/close, ESC, and click outside

**Files changed (session 6):**
- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html`

---

## Step 2 (original) – Richer status information ⚠ ROLLED BACK (2026-03-17, session 4)

*(Historical reference – concepts can be reused)*

### 2a – Elapsed + actor ⚠ ROLLED BACK

Developed and tested, but rolled back due to bugs in combination with 2b/2c. Code available at commit `9593675` in `hugo-theme-samt-bu`. Can be restored with `git reset --hard 9593675 && git push --force` in the theme, followed by a submodule update in `samt-bu-docs`.

**Known bugs that must be resolved before re-deploying:**

1. **Race condition:** `pollQeBuild` (ETag poll in dialog) and `checkCompletions` (GitHub API poll on page load) run in parallel on the last saved page. Both decrement the pending counter, `seenCompleted` goes wrong.
2. **ETag banner after own build:** After pending state is cleared and the page reloads, ETag poll detects that the page has changed (from *our own* build) and shows «Page updated» as if it were someone else's change. Partially fixed with `sessionStorage._samtuOwnBuildDone`, but not sufficiently tested.
3. **Stuck count with multiple concurrent builds:** Pending counter never reached 0 with 4 rapid saves in sequence.

**Recommended approach on re-implementation:**
- Remove `seenCompleted` logic entirely from `checkCompletions`
- Use a «queue empty» strategy: when `inProgress=0 && queued=0 && myCompleted > 0` → everything done, clean up and reload
- Ensure `checkCompletions` does NOT start if `_samtuDialogPollActive` is set

`samtuShowPendingIndicatorWithTotal` now shows:

| Scenario | Text |
|---|---|
| 1 change, running | `⟳ Your change is building · 45 sec` |
| 1 change, in queue | `⟳ Your change in queue · 12 sec` |
| N changes, all running | `⟳ N changes building · 1 min` |
| N running, M in queue | `⟳ N building · M in queue · 55 sec` |

Elapsed is calculated from `pending.lastSaveAt` and updated automatically every 3 sec (same as the poll cycle).

### 2b – Split inProgress/queued ⚠ ROLLED BACK (see 2a)

`checkCompletions()` now counts `inProgress` and `queued` separately (instead of `totalActive`). Works regardless of whether Cloudflare is on free tier (1 parallel) or Pro (5 parallel) – the GitHub Actions API reflects the truth in both cases.

**New signature:** `samtuShowPendingIndicatorWithTotal(count, inProgress, queued)`

### 2c – Event feed + pling (bottom right)

**Concept:** Separate *status* (bottom left, ongoing state) from *events* (bottom right, things that have happened).

**Bottom right – event pill:**
- Shows latest event as a compact pill: `🔔 Erik Hagen changed /om-samt-bu (2 min ago)`
- Click → dropdown with last 5–10 events (stored in localStorage)
- Pling sound (one note) on others' event; fanfare on own (existing)
- Replaces today's green `#page-update-banner` (which only shows "Page updated" without context)

**Data sources:**
- Own events: already known (actor, url, timestamp from pending state)
- Others' events: ETag polling detects change → API call to `/actions/runs?status=completed&per_page=3` for `triggering_actor.login`

**Files to change:**
- `custom-footer.html`: ETag poll → event log + pling
- `edit-switcher.html`: new HTML element for pill + dropdown

---

## Step 4 – «Mine»/«All» tabs in build history dialog ✅ DONE (2026-03-17, session 7)

Subtabs in the dialog header let the user switch between own and all builds:

- **«Mine»** (default): filters by logged-in user via `&actor=` – same as before
- **«All»**: fetches the last 15 builds in the repo, shows actor as a sub-line per row
- **Name cache:** `/users/{login}` fetched once per unique login per page visit, cached in a JS dict. Shows `login (Full Name)` when name is available – requires that the GitHub profile has the Name field set
- **Tab switch** resets cache and re-fetches immediately
- **Files changed:** `edit-switcher.html` (HTML), `custom-footer.html` (JS)

> **Note:** `data.name` from the GitHub API is `null` if the user has not set a name in their GitHub profile (`github.com/settings/profile`). The display name in Hugo content (`last_editor` field) is set manually and is not connected to the GitHub profile.

---

## Step 5 – Overall status overview for all users

**Status:** Under consideration – may be added to roadmap

Real-time overview of all active builds across users. Poll the GitHub Actions API + present `triggering_actor.login` per run. Possible implementation: clicking the indicator opens a dropdown with all active runs.

**Dependency:** Requires a GitHub token (already available for logged-in users).

---

## Technical context

Key functions in `custom-footer.html`:

| Function | Signature | Role |
|----------|-----------|------|
| `samtuIncrementPending()` | – | Increases pending counter in localStorage **and updates the indicator immediately** |
| `samtuDecrementPending()` | – | Called on build complete – decrements counter |
| `samtuShowPendingIndicator(count)` | – | Shorthand, calls below with `null` |
| `samtuShowPendingIndicatorWithTotal` | `(count, totalActive)` | Updates `#qe-job-indicator` with text + sets `data-building="1"` |
| `samtuShowDoneIndicator()` | – | Shows «Changes published – click to reload» + removes `data-building` |
| `samtuPlaySuccess()` | – | Plays victory fanfare + speech |
| `samtuUnlockAudio()` | – | Unlocks AudioContext during user gesture |
| `startGhPoll()` | – | GitHub Actions polling (runs on the page where Save was clicked) |
| `checkCompletions()` | – | Resume polling on page load (runs on new page) |

**`localStorage` pending state:**
```json
{
  "count": 1,
  "firstSaveAt": 1710638400000,
  "lastSaveAt": 1710638400000,
  "seenCompleted": 0,
  "actor": "erikhag1git"
}
```

**`#qe-job-indicator`** (bottom left, always visible): Idle → clock icon + «Build history». During build → spinner + «N changes building». Done → link «Changes published – click to reload». Click opens `#job-history-dialog`. Background poll uses the `data-building` attribute to avoid conflict with others'-changes detection.

**`#page-update-banner`** (bottom right, green): ETag-based background polling every 45 sec. Shown only for others' changes (when no own pending). Candidate for replacement by an event pill in a future step (see Step 3).
