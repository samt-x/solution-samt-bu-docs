---
id: 3326656d-f862-4309-a590-ee44ee42c43a
title: "Work-in-progress sign"
linkTitle: "Work-in-progress sign"
weight: 45
lastmod: 2026-11-18T23:02:15+01:00
last_editor: Erik Hagen

---

A "work in progress" sign (road works sign) tells readers that a chapter is not finished. Put it directly below the heading of chapters that only contain keywords or have not been assessed yet, and remove it when the chapter is finished.

Example in use: [Relevance for Norwegian actors](/en/innsikt/eu-relatert/data-spaces/loesninger/simpl/relevans-for-norge/) under Simpl.

### What it looks like

{{< i-arbeid >}}

{{< i-arbeid tekst="Work in progress – keywords only" >}}

### How to write it

Write the shortcode on its own line directly below the heading:

```
### Criticism

{{</* i-arbeid */>}}

The text of the chapter …
```

| Field | Required | What it does |
|---|---|---|
| `tekst` | no | The text next to the sign. The default is "I arbeid" on Norwegian pages and "Work in progress" on English pages |

To mark the whole page as well, use the `status` field in the front matter (for example `status: In progress`), which shows the symbol ◐ next to the title in the menu.

### Editing in the browser

The shortcode survives the built-in editor when it is on its own line, in the same way as [graphic cards](../grafiske-kort/). In the middle of a line of text it may be broken when saving.
