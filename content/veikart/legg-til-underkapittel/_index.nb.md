---
id: 36ddabdf-4ceb-45bb-b55f-051cd9976078
title: "Legg til underkapittel – valg i Endre-menyen"
linkTitle: "Legg til underkapittel"
weight: 10
status: "Tidlig utkast"
---

Når man leser en side i nettstedet, er det ingen enkel vei til å opprette et nytt underkapittel under denne siden. Dette roadmap-elementet beskriver behovet, valgt løsning og begrunnelsen for valget.

## Bakgrunn

«Endre»-menyen i headeren tilbyr i dag to valg: «Denne siden» (deep-link til Decap CMS-editor for gjeldende side) og «Andre valg» (CMS-portaloversikt). Et naturlig neste steg i redigeringsarbeidsflyten – å opprette et nytt underkapittel under siden man leser – mangler.

## Valgt løsning

En dynamisk lenke i `edit-switcher.html` som åpner GitHubs «create file»-grensesnitt på riktig sti:

```
https://github.com/<org>/<repo>/new/main/content/<sti-til-gjeldende-side>/
```

GitHub åpner et tomt filredigeringsvindu der brukeren skriver filnavnet (f.eks. `nytt-kapittel/_index.nb.md`) og frontmatter. Lenken bygges dynamisk fra `.File.Path` i Hugo-templaten, på samme måte som eksisterende Decap-deep-link.

**Gjenstående arbeid:**

- Legge til nytt menyvalg i `edit-switcher.html` (temaet) for alle fire portalbetingelser
- Teste at lenken fungerer korrekt for modul-sider (der repo-et er et annet enn `samt-bu-docs`)
- Vurdere om valget skal vises på alle sider, eller bare der det gir mening
- Tilsvarende «Add sub-chapter»-valg for engelsk meny

## Alternativer vurdert

**Decap CMS «New»-lenke** – lenke til `<portal>#/collections/<collection>/new`. Oppretter en ny side i Decap CMS-editoren.

**GitHub «create file»-lenke** *(valgt)* – lenke til `github.com/<org>/<repo>/new/main/content/<sti>/`. Åpner GitHubs filredigeringsgrensesnitt direkte på riktig sti.

## Begrunnelse

Decap CMS-alternativet oppretter alltid på rotnivå i samlingen – brukeren må deretter navigere manuelt til riktig undermappe, noe som er feilutsatt og lite intuitivt. GitHub-lenken setter brukeren direkte i riktig katalog i repo-et, uten omveier. Siden målgruppen (tekniske redaktører og utviklere) uansett er kjent med GitHub, er dette akseptabelt.
