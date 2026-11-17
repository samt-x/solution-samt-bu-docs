---
title: "Graphic cards"
linkTitle: "Graphic cards"
weight: 40
---

Graphic cards show a few options or parts side by side, with an icon, a short text and a link. Cards are a good fit when a page should guide the reader on to two to six subpages. For comparing many properties, a table is still better.

Example in use: [SIMPL](/en/innsikt/eu-relatert/data-spaces/loesninger/simpl/), with the three parts of the programme.

### What it looks like

{{< kortrad >}}
{{< kort tittel="First option" ikon="flask" status="Optional status line." >}}
A short text about the option, preferably one or two sentences.
{{< /kort >}}
{{< kort tittel="Second option" ikon="rocket" >}}
A card without a link and without a status line.
{{< /kort >}}
{{< /kortrad >}}

### How to write it

Cards are written in the page's Markdown file, either in the [built-in editor](../innebygd-redigering/), with «Edit in GitHub» (see [Editing on GitHub](../github-redigering/)) or in a [local setup](../lokal-oppsett/).

```
{{</* kortrad */>}}
{{</* kort tittel="Simpl-Labs" ikon="flask" lenke="simpl-labs/" status="Being built." */>}}
A sandbox for trying out a data space.
{{</* /kort */>}}
{{</* kort tittel="Simpl-Live" ikon="rocket" lenke="simpl-live/" */>}}
Support for selected European data spaces.
{{</* /kort */>}}
{{</* /kortrad */>}}
```

- **`kortrad`** (card row) groups the cards. They sit side by side on wide screens and stack on mobile.
- **`kort`** (card) is a single card. The text between the start and end tags is ordinary Markdown.

The field names are Norwegian, as in the example above.

| Field | Required | What it does |
|---|---|---|
| `tittel` (title) | yes | The heading of the card. The build stops if it is missing |
| `ikon` (icon) | no | The name of an icon from [Font Awesome 4.7](https://fontawesome.com/v4/icons/), with or without «fa-», for example `flask`, `code`, `rocket`, `users`, `book` |
| `lenke` (link) | no | The address the card points to. Relative (`simpl-labs/`) for a subpage, or a full address. The whole card becomes clickable |
| `status` | no | A short status line at the bottom of the card |
| `etikett` (label) | no | The text above the status line. The default is «Status». Use for example «Status November 2026» when the information depends on time |

The cards use the site's own colours and icons, also when they describe a programme or an organisation with its own brand.

### Editing in the browser

In the built-in editor, the cards are shown as a grey code block containing the text above. You can change the text in the block, and the block is saved as it stands. The same applies to other shortcodes on a line of their own, such as the figures on the «Tasks and progress» pages.

Shortcodes **in the middle of a line of text** are not protected and may be broken if you save the page in the browser. Put them on a line of their own, or edit the page with «Edit in GitHub».
