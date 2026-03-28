---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: 661b950a-3938-4e30-a5b4-f5d5d3a603c4
title: "Slett side – håndtering av undermapper"
linkTitle: "Slett side med undermapper"
weight: 60
status: "Godkjent"
lastmod: 2026-03-27T23:29:13+01:00
last_editor: Erik Hagen

---

«Slett denne siden» sletter kun `_index.nb.md` og `_index.en.md` i gjeldende mappe, men lar undermapper stå igjen i Git. Dette gir to problemer.

## Problem

`deleteFilesInOneCommit()` i `custom-footer.html` sletter kun de to indeksfilene. Hvis siden har undermapper (underkapitler), vil disse bli liggende som foreldreløse noder i repoet – uten en foreldresides `_index.nb.md`. Hugo kan håndtere dette (lager autogenerert listenode), men resultatet er uønsket innhold.

## To mulige løsninger

### A – Blokker sletting hvis siden har barn

Sjekk om `.Children` eller `.Pages` er ikke-tomme i Hugo-templaten. Vis i så fall «Slett siden»-valget som deaktivert med forklaring: «Siden har underkapitler – slett disse først».

```hugo
{{ $hasChildren := gt (len .Pages) 0 }}
{{ if $hasChildren }}
  <li class="disabled"><span>Kan ikke slette – siden har underkapitler</span></li>
{{ else }}
  <li><a href="#" onclick="openDeleteDialog(...)">Slett denne siden</a></li>
{{ end }}
```

**Fordel:** Enkelt å implementere. Brukeren tvinges til å rydde opp manuelt – tryggere.
**Ulempe:** Mer friksjon for brukeren.

### B – Slett hele mappetre rekursivt

Bruk GitHub Trees API til å liste alle filer under gjeldende mappe og inkluder dem i `deleteFilesInOneCommit`-kallet (sett `sha: null` for alle).

**Fordel:** Ett klikk, ryddig.
**Ulempe:** Mer kompleks. Risiko for utilsiktet massesletting.

## Anbefalt løsning

**Alternativ A** som første steg – enkelt og trygt. Alternativ B kan vurderes hvis bruksmønsteret viser at det er behov for det.

## Relatert

- `edit-switcher.html`: `openDeleteDialog`-kallet og Hugo-betingelsene for synlighet
- `custom-footer.html`: `deleteFilesInOneCommit`-funksjonen
