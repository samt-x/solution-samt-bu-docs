---
id: 3b8fe53a-65b0-46cd-ad31-ef3847775772
title: "Ny side på samme nivå – valg i Endre-menyen"
linkTitle: "Ny side – samme nivå"
weight: 20
status: "Tidlig utkast"
last_editor: erikhag1git (Erik Hagen)
lastmod: 2026-03-15T23:49:44+01:00

---

Når man leser en side, er det ingen enkel vei til å opprette en ny side på samme nivå (søskenside). Dette roadmap-elementet henger tett sammen med [Legg til underkapittel](../legg-til-underkapittel/) og bør løses i samme iterasjon.

## Valgt løsning

Samme tilnærming som for underkapittel: en dynamisk GitHub «create file»-lenke, men pekende på **foreldremappen** i stedet for gjeldende mappe:

```
https://github.com/<org>/<repo>/new/main/content/<foreldressti>/
```

Foreldrestien beregnes i Hugo-templaten som `path.Dir` av gjeldende sides relative sti.

**Valget skjules** på rot-sider (der det ikke gir mening å opprette søsken).

## Gjenstående arbeid

- Erstatte nåværende alert-popup med faktisk GitHub-lenke i `edit-switcher.html`
- Teste for alle fire portalbetingelser (docs, arkitektur, utkast, loesninger)
- Koordinere med implementering av «Legg til underkapittel» – bør gjøres samtidig
