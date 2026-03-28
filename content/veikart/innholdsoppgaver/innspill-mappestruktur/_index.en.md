---
# id: auto-generated – copied values are overwritten automatically on push
id: b8d34d8b-1d6c-47d8-bbb6-da553b138c56
title: "Folder structure for inputs in samt-bu-files"
linkTitle: "Inputs – folder structure"
weight: 100
status: New
# Valid status values: Ny | Tidlig utkast | Pågår | Til QA | Godkjent | Avbrutt
lastmod: 2026-03-28T10:01:46+01:00
last_editor: Erik Hagen

---

## Current approach

Inputs to SAMT-BU are stored in `samt-bu-files/drafts/` as individual files with a date prefix:

```
drafts/
  2026-03-09 Prosjektforslag - felles prosjekt Novari-HK-dir.docx
  Prosjektbeskrivelse SAMT Barn og unge.docx
  Påls arkitektur og målbilde - SAMT-BU 2026-02-24.docx
```

This works well for simple inputs with a single file.

## Desired improvement

Consider introducing one folder per input, allowing each input to contain multiple files — e.g. attachments, presentations, discussion notes and follow-up documents:

```
drafts/
  2026-03-09 Prosjektforslag Novari-HK-dir/
    Prosjektforslag - felles prosjekt Novari-HK-dir.docx
    [possible attachments and follow-up documents]
  2026-03-09 Prosjektbeskrivelse SAMT-BU/
    ...
```

The date prefix on the folder ensures chronological sorting.

## Considerations

- Existing files in `drafts/` should not be moved without updating links in `samt-bu-drafts` accordingly
- The naming convention `yyyy-mm-dd Title` is retained — now at folder level rather than file level
- Single-file inputs with no attachments may optionally retain a flat structure
