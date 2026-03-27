---
id: 12f44a07-413c-49f7-b755-895bcdb9d429
title: "Hjelpescripter"
linkTitle: "Hjelpescripter"
weight: 90
status: "Ny"
lastmod: 2026-03-27T23:29:13+01:00
last_editor: Erik Hagen

---

**Behov:** Flere vanlige operasjoner (initialisere nytt modulrepo, opprette ny side med korrekt frontmatter-mal, synkronisere modulpekere) gjøres manuelt i dag og er feilutsatte. Hjelpescripter vil redusere friksjon og sikre konsistens.

## Planlagt innhold

Aktuelle scripter:

- **Nytt modulrepo:** Initialiserer mappestruktur, `hugo mod init`, `_index.nb.md`/`_index.en.md`-mal med korrekt frontmatter
- **Ny side:** Oppretter mappe og begge språkfiler med UUID-placeholder, title, weight og tomt innhold
- **Synkroniser modulpeker:** Tilsvarer `hugo mod get @latest` + commit av `go.mod`/`go.sum` for ett eller alle modulrepoer

Implementasjonsform vurderes: shell-script, Python-script eller GitHub Actions workflow.

*Ikke påbegynt.*
