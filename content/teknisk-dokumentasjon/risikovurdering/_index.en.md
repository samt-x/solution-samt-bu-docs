---
# id: auto-generated – copied values are overwritten automatically on push
id: 07e39938-5a25-44e2-8df9-d869da75683b
title: "Risk Assessment (ROS) – Built-in Editing"
linkTitle: "Risk assessment"
weight: 45
lastmod: 2026-05-02T17:55:45+02:00
last_editor: Erik Hagen

---

This page documents the risk assessment for the server-side component of the built-in editing flow – specifically the use of `WORKER_PAT` in the Cloudflare Worker (`auth.samt-bu.no`).

## Context

When an external contributor without write access uses the "Suggest change" feature, the Cloudflare Worker performs GitHub operations (branch, commit, pull request) on behalf of the user. This requires a GitHub token with write access to the SAMT-X repositories – stored as the Worker secret `WORKER_PAT`.

## Current Solution

| Component | Value |
|-----------|-------|
| Token type | Classic GitHub PAT, `repo` scope |
| Account | `samt-x-bot` – dedicated bot account |
| Org membership | SAMT-X org only – no other orgs or private repositories |
| Write access | 9 SAMT-X content repositories via team `content-bots` |
| Storage | Encrypted Cloudflare Worker secret – never exposed in code |

## Risk Assessment

### Risk 1 – WORKER_PAT Leakage

**Likelihood:** Low. Token is encrypted in Cloudflare, never in source code or logs.

**Impact if leaked:** An attacker can create branches, commits and pull requests in the 9 SAMT-X content repositories. No data deletion or access to sensitive repositories. All activity is traceable in the GitHub audit log and visible as PRs.

**Compensating controls:**
- Worker code is hardcoded to only call `api.github.com/repos/SAMT-X/…`
- Worker requires a valid GitHub App token from the caller (format validation of `ghu_`/`ghp_` prefix)
- All operations are traceable in the GitHub audit log
- `samt-x-bot` account is only associated with SAMT-X – no broader attack surface

**Residual risk:** Acceptable.

### Risk 2 – Classic PAT instead of fine-grained

**Background:** Fine-grained PATs and GitHub App user-to-server tokens were attempted, but both returned 403 on the git-ref endpoint – likely related to GitHub App architecture for this use case. A classic PAT was chosen as a pragmatic solution.

**Impact:** A classic PAT with `repo` scope grants access to *all* repositories `samt-x-bot` has access to – not just an explicit list. If `samt-x-bot` is granted access to repositories outside SAMT-X in the future (e.g. sensitive private repos), the attack surface increases.

**Compensating control:** `samt-x-bot` is a dedicated account associated only with the SAMT-X org. Never grant this account access to repositories outside SAMT-X.

**Residual risk:** Acceptable as long as the account is kept clean.

### Risk 3 – Bot account without organisational ownership

The `samt-x-bot` account is linked to the email address `nasjonal.arkitektur@gmail.com`. If access to this email is lost, the PAT cannot be rotated without additional measures.

**Compensating control:** Log in as `samt-x-bot` and rotate the PAT when needed. Store the new PAT in Bitwarden under "Cloudflare Worker secret WORKER_PAT (samt-x-bot)".

**Future action:** Move the email association to a shared mailbox (e.g. `operations@samt-bu.no`) when available.

## Rotating WORKER_PAT

If the PAT must be rotated (due to leakage or expiry):

1. Log in to GitHub as `samt-x-bot`
2. Settings → Developer settings → Personal access tokens → Tokens (classic)
3. Generate a new token (`repo` scope, no expiration)
4. Update the Cloudflare Worker secret:
   ```bash
   printf "<new-token>" | CLOUDFLARE_API_TOKEN=<cf-token> npx wrangler secret put WORKER_PAT --config cloudflare-worker/wrangler.toml
   ```
5. Update the Bitwarden note "Cloudflare Worker secret WORKER_PAT (samt-x-bot)"
6. Delete the old token in GitHub
