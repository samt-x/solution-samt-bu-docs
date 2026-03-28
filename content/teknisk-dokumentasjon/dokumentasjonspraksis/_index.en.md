---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: b8bf5c67-7a5f-4de5-a3f4-232e7e60e725
title: "Documentation practice"
linkTitle: "Documentation practice"
weight: 30
status: "Early draft"
lastmod: 2026-03-27T23:29:13+01:00
last_editor: Erik Hagen

---

We develop best practice for documentation through good examples – not by locking ourselves into a rigid template from the start. This page collects experiences and patterns as they emerge.

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
