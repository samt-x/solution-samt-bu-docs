---
id: 3326656d-f862-4309-a590-ee44ee42c43a
title: "I arbeid-skilt"
linkTitle: "I arbeid-skilt"
weight: 45
lastmod: 2026-11-18T23:02:15+01:00
last_editor: Erik Hagen

---

Et «I arbeid»-skilt (veiarbeidsskilt) viser leseren at et kapittel ikke er ferdig. Sett det rett under overskriften på kapitler som bare har stikkord eller ikke er vurdert ennå, og fjern det når kapitlet er ferdig.

Eksempel i bruk: [Relevans for Norge](/innsikt/eu-relatert/data-spaces/loesninger/simpl/relevans-for-norge/) under Simpl.

### Slik ser det ut

{{< i-arbeid >}}

{{< i-arbeid tekst="I arbeid – bare stikkord" >}}

### Slik skriver du det

Skriv kortkoden på egen linje rett under overskriften:

```
### Kritikk

{{</* i-arbeid */>}}

Teksten i kapitlet …
```

| Felt | Påkrevd | Hva det gjør |
|---|---|---|
| `tekst` | nei | Teksten ved skiltet. Standard er «I arbeid» på norske sider og «Work in progress» på engelske |

Skal hele siden merkes, bruk i tillegg feltet `status` i frontmatter (for eksempel `status: Pågår`), som gir symbolet ◐ ved tittelen i menyen.

### Redigering i nettleseren

Kortkoden tåler den innebygde redigeringen når den står på egen linje, på samme måte som [grafiske kort](../grafiske-kort/). Midt i en tekstlinje kan den bli ødelagt ved lagring.
