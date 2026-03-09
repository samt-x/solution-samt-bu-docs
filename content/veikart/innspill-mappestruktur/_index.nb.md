---
title: "Mappestruktur for innspill i samt-bu-files"
linkTitle: "Innspill – mappestruktur"
weight: 40
status: Ny
# Gyldige statusverdier: Ny | Tidlig utkast | Pågår | Til QA | Godkjent | Avbrutt
---

## Dagens løsning

Innspill til SAMT-BU lagres i `samt-bu-files/drafts/` som enkeltfiler med dato-prefix:

```
drafts/
  2026-03-09 Prosjektforslag - felles prosjekt Novari-HK-dir.docx
  Prosjektbeskrivelse SAMT Barn og unge.docx
  Påls arkitektur og målbilde - SAMT-BU 2026-02-24.docx
```

Dette fungerer greit for enkle innspill med én fil.

## Ønsket forbedring

Vurdere å innføre én mappe per innspill, slik at hvert innspill kan romme flere filer – f.eks. vedlegg, presentasjoner, diskusjonsnotater og oppfølgingsdokumenter:

```
drafts/
  2026-03-09 Prosjektforslag Novari-HK-dir/
    Prosjektforslag - felles prosjekt Novari-HK-dir.docx
    [eventuelle vedlegg og oppfølgingsdokumenter]
  2026-03-09 Prosjektbeskrivelse SAMT-BU/
    ...
```

Dato-prefixet på mappen sikrer kronologisk sortering.

## Vurderinger

- Eksisterende enkeltfiler i `drafts/` bør ikke flyttes uten at lenker fra `samt-bu-drafts` oppdateres tilsvarende
- Navngivingskonvensjonen `yyyy-mm-dd Tittel` beholdes – nå på mappenivå i stedet for filnivå
- Enkeltfiler uten behov for vedlegg kan eventuelt beholde flat struktur
