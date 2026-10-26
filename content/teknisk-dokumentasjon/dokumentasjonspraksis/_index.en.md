---
# id: auto-generated – copied values are overwritten automatically on push
id: b8bf5c67-7a5f-4de5-a3f4-232e7e60e725
title: "Documentation practice"
linkTitle: "Documentation practice"
weight: 30
status: "Early draft"
lastmod: 2026-10-26T23:41:02+01:00
last_editor: Erik Hagen

---

We develop best practice for documentation through good examples – not by locking ourselves into a rigid template from the start. This page collects experiences and patterns as they emerge.

## Documentation follows the change

Standing rule from 2026-10-25: **Every change in functionality is checked against the documentation**, whether it resolves an issue or not. This also applies to changes in the theme, the build (CI), scripts, task management and the setup of the GitHub organization.

Check and update in the same working session as the change:

| What | Where |
| --- | --- |
| **Solution documentation** – how it works | The technical documentation for the solution, for example this section or [Task management](/en/prosjektleveranser/loesninger/samhandlingsplattform/oppgavestyring/) |
| **User guide** – what the user sees and does | [User guide](../../brukerveiledning/) |
| **Anything else affected** | Roadmap, README, instructions for Claude (`CLAUDE.md`) |

Pages on the site are updated **in Norwegian and English**.

**Continuously, not saved up.** The documentation is written when the change is **in use**, not after every intermediate step, and not saved for the end of the working session. A change is live at once, and the details are easiest to get right while they are fresh. While a design is still being discussed, the documentation waits.

**When something is renamed** (a type, a field, a page, a repository …), search for the old name in the content of **all** content repositories, not only where it is known to appear.

**The check is written down.** When an issue is closed, the closing comment has a line that starts with **«Documentation:»** (or «Dokumentasjon:»). It links to what was updated, or says why nothing had to change. Without that line the issue is not done.

## Approach

The structure of a documentation page should reflect the type of content. For decision documentation (such as roadmap items) we have drawn inspiration from the [ADR format (Architecture Decision Records)](https://adr.github.io/), adapted to our needs.

First example of this pattern: [Add sub-chapter – option in the Edit menu](../../veikart/legg-til-underkapittel/).

## Emerging pattern: decision documentation

Used for roadmap items and other choices where it is useful to document *why*, not just *what*.

| Section | Content |
|---------|---------|
| **Background** | The need to be addressed – short and concrete |
| **Chosen solution** | What we have decided, including remaining work |
| **Alternatives considered** | Other solutions that were evaluated, without assessment |
| **Rationale** | Why the chosen solution was preferred over the alternatives |

> This is not a binding template – it is a starting point. Adjust the structure where the content requires it, and update this page as the pattern evolves.
