---
id: 5ca83efe-276a-4600-bd19-a2ff92deae32
title: "Grafiske kort"
linkTitle: "Grafiske kort"
weight: 40
---

Grafiske kort viser noen få valg eller deler side om side, med ikon, kort tekst og lenke. Kortene passer når en side skal vise leseren videre til to–seks undersider. For sammenligning av mange egenskaper er en tabell fortsatt bedre.

Eksempel i bruk: [SIMPL](/innsikt/eu-relatert/data-spaces/loesninger/simpl/), med de tre delene av programmet.

### Slik ser det ut

{{< kortrad >}}
{{< kort tittel="Første valg" ikon="flask" status="Valgfri statuslinje." >}}
Kort tekst om valget, gjerne én eller to setninger.
{{< /kort >}}
{{< kort tittel="Andre valg" ikon="rocket" >}}
Kort uten lenke og uten statuslinje.
{{< /kort >}}
{{< /kortrad >}}

### Slik skriver du det

Kortene skrives i Markdown-fila for siden, enten i den [innebygde redigeringen](../innebygd-redigering/), med «Endre i GitHub» (se [Redigering på GitHub](../github-redigering/)) eller i [lokalt oppsett](../lokal-oppsett/).

```
{{</* kortrad */>}}
{{</* kort tittel="Simpl-Labs" ikon="flask" lenke="simpl-labs/" status="Under oppbygging." */>}}
Sandkasse for å prøve ut et data space.
{{</* /kort */>}}
{{</* kort tittel="Simpl-Live" ikon="rocket" lenke="simpl-live/" */>}}
Støtte til utvalgte europeiske data spaces.
{{</* /kort */>}}
{{</* /kortrad */>}}
```

- **`kortrad`** samler kortene. De står ved siden av hverandre på bred skjerm og under hverandre på mobil.
- **`kort`** er ett kort. Teksten mellom start og slutt er vanlig Markdown.

| Felt | Påkrevd | Hva det gjør |
|---|---|---|
| `tittel` | ja | Overskriften på kortet. Bygget stopper hvis den mangler |
| `ikon` | nei | Navnet på et ikon fra [Font Awesome 4.7](https://fontawesome.com/v4/icons/), med eller uten «fa-», for eksempel `flask`, `code`, `rocket`, `users`, `book` |
| `lenke` | nei | Adressen kortet peker til. Relativ (`simpl-labs/`) for en underside, eller full adresse. Hele kortet blir klikkbart |
| `status` | nei | Kort statuslinje nederst på kortet |
| `etikett` | nei | Teksten over statuslinjen. Standard er «Status». Bruk for eksempel «Status november 2026» når opplysningen er tidsavhengig |

Kortene bruker nettstedets egne farger og ikoner, også når de omtaler et program eller en organisasjon med egen merkevare.

### Redigering i nettleseren

I den innebygde redigeringen vises kortene som en grå kodeblokk med teksten over. Du kan endre teksten i blokken, og blokken lagres slik den står. Det samme gjelder andre kortkoder som står på egen linje, for eksempel figurene på sidene «Oppgaver og framdrift».

Kortkoder **midt i en tekstlinje** beskyttes ikke og kan bli ødelagt hvis du lagrer siden i nettleseren. Sett dem på egen linje, eller rediger siden med «Endre i GitHub».
