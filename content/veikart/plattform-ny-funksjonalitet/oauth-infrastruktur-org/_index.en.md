---
# id: auto-generated – copied values are overwritten automatically on push
id: aebdf240-bc40-43a5-a547-50139b0a6400
title: "Move OAuth infrastructure to organization account"
linkTitle: "OAuth infrastructure – org"
weight: 125
status: "New"
# Valid values: New | Early draft | In progress | For QA | Approved | Cancelled
lastmod: 2026-04-19T14:04:31+02:00
last_editor: Erik Hagen

---

The Cloudflare Worker (`samt-bu-cms-auth.erik-hag1.workers.dev`) and GitHub OAuth App («SAMT-X Docs») currently run on personal accounts belonging to a single developer. If this person leaves the project or changes accounts, login and editing will stop working for all users.

## What needs to be done

1. **Cloudflare Worker** – move `samt-bu-cms-auth` to a shared Cloudflare account or organization account owned by the SAMT-X project
2. **GitHub OAuth App** – the existing «SAMT-X Docs» app is already owned by the `samt-x` organization ✅ – but the callback URL points to the personal Worker (point 1 resolves this)
3. **Cloudflare API keys** – update GitHub Actions secrets (`CF_ACCOUNT_ID`, `CF_API_TOKEN`) to the new account

## Risk of not doing it

- Loss of access to one personal account → all editors lose the ability to log in
- No alerting mechanism – the problem is only discovered when users report that editing is not working

## Priority

**Medium** – `erik-hag1` is explicitly shown as the redirect URL in GitHub's authorization dialog for all users who log in. This appears unprofessional and confusing. Should be resolved before the project is opened to wider use.
