---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: ad913fd8-a039-4bd6-9dca-05d50f457a07
title: "Brukerveiledning"
linkTitle: "Brukerveiledning"
weight: 10
lastmod: 2026-03-27T23:29:13+01:00
last_editor: Erik Hagen

---

Denne seksjonen er en praktisk veiledning for redaktører og bidragsytere som arbeider med innhold i SAMT-BU Docs. Her går vi dypere enn den generelle [Hvordan bidra](/samt-bu-docs/om/hvordan-bidra/)-siden og dekker arbeidsflyt, CMS-funksjonalitet og håndtering av situasjoner der flere redigerer samtidig.

## Hvem er dette for?

| Du er... | Start her |
|----------|-----------|
| Redaktør som bruker nettleseren (CMS) | [CMS i dybden](cms-i-dybden/) |
| Bidragsyter med lokal kopi av repoene | [Synkronisering og konflikthåndtering](synkronisering/) |
| Ny til plattformen | Les begge – start med CMS i dybden |

## Rask orientering

SAMT-BU Docs er bygget på Hugo og publiseres automatisk til GitHub Pages via GitHub Actions. Innhold redigeres på tre måter:

1. **Decap CMS** (anbefalt for fagpersoner) – visuell nettleserbasert editor
2. **GitHub** – direkte redigering i nettleseren på github.com
3. **Lokalt** – klon repo, rediger Markdown-filer, push

Innhold fra flere repoer slås sammen til ett nettsted. Endringer publiseres automatisk 1–3 minutter etter at de er lagret (commit pushet til `main`).
