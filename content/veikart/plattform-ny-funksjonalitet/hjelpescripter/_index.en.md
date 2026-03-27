---
id: 12f44a07-413c-49f7-b755-895bcdb9d429
title: "Helper scripts"
linkTitle: "Helper scripts"
weight: 90
status: "New"
lastmod: 2026-03-26T16:32:48+01:00

---

**Need:** Several common operations (initialising a new module repository, creating a new page with the correct frontmatter template, synchronising module pointers) are done manually today and are error-prone. Helper scripts will reduce friction and ensure consistency.

## Planned content

Candidate scripts:

- **New module repo:** Initialises folder structure, `hugo mod init`, `_index.nb.md`/`_index.en.md` template with correct frontmatter
- **New page:** Creates folder and both language files with UUID placeholder, title, weight, and empty content
- **Sync module pointer:** Equivalent to `hugo mod get @latest` + commit of `go.mod`/`go.sum` for one or all module repos

Implementation form to be decided: shell script, Python script, or GitHub Actions workflow.

*Not started.*
