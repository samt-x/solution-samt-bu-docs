---
id: 36ddabdf-4ceb-45bb-b55f-051cd9976078
title: "Legg til underkapittel – valg i Endre-menyen"
linkTitle: "Legg til underkapittel"
weight: 10
status: "Godkjent"
last_editor: Erik Hagen

---

**Implementert 2026-03-11.** «Underkapittel»-valget i Endre-menyen åpner samme dialog som «Ny side – samme nivå», men bruker gjeldende side som forelder.

## Implementasjon

Dialog gjenbruker `#np-overlay` fra «Ny side – samme nivå». Ny global funksjon `openNewChildDialog(repo, dirPath, lang, currentPermalink)` i `custom-footer.html`. Ny variabel `npMode = 'sibling' | 'child'` styrer URL-beregning og dialogtittel.

- **URL child:** `currentPermalink + slug + '/'`
- **URL sibling:** `parentUrl + slug + '/'` (strip siste segment)
- Standardvekt: 10
- Knapp-tekst: «Opprett underkapittel» / «Create sub-chapter»
- Vises på alle sider med `.File` unntatt rot (`ne $dirPath "content"`)

## Begrunnelse for valg

Samme dialog som «Ny side» – brukeren kjenner grensesnittet, og `fetchSiblingWeightUpdates` + `createFilesInOneCommit` gjenbrukes uendret.
