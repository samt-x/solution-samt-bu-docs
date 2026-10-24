---
id: 6c9a0913-f680-4da8-9455-aef2996197e4
title: "Managing members and access – step by step"
linkTitle: "Members and access"
weight: 22
lastmod: 2026-10-24T15:39:17+02:00
last_editor: Erik Hagen

---

A guide for the core team: how to bring new participants into the GitHub organisation samt-x, keep track of them and remove them again. How the teams and permissions fit together is described in [Concept for GitHub organisations and repositories](../github-struktur/#access-model).

---

## Two sources

| Source | What it holds | Maintained by |
|---|---|---|
| **The member list** (medlemmer.md in the private repository samt-bu-intern-admin) | Name, email, company, status and role in SAMT-BU | The core team, manually, preferably by asking Claude |
| **GitHub** | Who is in the organisation, organisation role, teams and permissions | Set in GitHub, read by the check script |

The check script compares the two and writes the result to tilgang.md in the same repository, with a list of discrepancies. Personal data is kept only in the member list, never in issues, commits or on this site.

The statuses in the list are: **potensiell** (potential, not yet invited), **invitert** (invited), **aktiv** (active), **inaktiv** (inactive: a member, but no longer part of the work) and **fjernet** (removed).

## Prerequisites

- You are in the core team. This gives access to samt-bu-intern-admin
- Inviting and removing organisation members requires you to be an **owner** of samt-x
- To run the check yourself: a clone of samt-bu-intern-admin, GitHub CLI (gh) logged in, and bash (Git Bash on Windows). Alternatively, ask Claude to do it

---

## New participant

1. **Get the GitHub username.** The person needs a GitHub account. Ask for the username, not the email address
2. **Add the person to the right team**, in GitHub under Organization → Teams. Choose the subject team (for example samt-bu-pilot-3) or the core team. If the person is not in any subject team, use samt-bu-alle. Access to samt-bu-alle follows from the subject teams being nested under it. If the person is not already an organisation member, GitHub sends an invitation automatically. Anyone taking part in the core work for a period is added to the core team like everyone else there, and removed again following the procedure for participants who leave. Note that the core team can also see the member list
3. **Add the person to the member list** with status "invitert" and today's date in "Fra" and "Endret"
4. **Tell the person** that the invitation is in their email, and on GitHub under the profile picture → Settings → Organizations. It can also be opened directly at github.com/orgs/samt-x/invitation. **The invitation expires after seven days** and must then be sent again

## The invitation has been accepted

1. Set the status to "aktiv" and update "Endret"
2. Run the check. It reports anyone who has accepted without the list being updated

## Participant leaves

1. **Remove the person from the teams.** If the person should still be able to read and follow along, the organisation membership can stay. In that case, set the status to "inaktiv"
2. **If the person should leave completely:** Organization → People → the person → Remove from organization. Set the status to "fjernet". The row stays as history
3. Run the check

## Regular check

Run the check after every change, and otherwise regularly, for example monthly:

```bash
bash sjekk-medlemmer.sh
```

The script writes tilgang.md and lists discrepancies, for example a person who is in the organisation but missing from the list. Fix them, and commit medlemmer.md and tilgang.md together.

---

## Pitfalls

- **Owners have admin everywhere**, regardless of teams. This does not show in the team structure
- **The test account erikhag1test** is an outside collaborator with its own access to samt-bu-docs, and must not be cleaned up
- **The bot account samt-x-bot** owns the keys the site uses to build and to receive suggestions. It must not be removed
- **Grant access through teams, not to individuals.** Direct access to a repository does not show in the team overview and is easily forgotten
