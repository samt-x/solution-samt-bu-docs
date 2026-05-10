---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: 4fe26ad6-aa99-46b9-b522-b5f8bfa09bf7
title: "Bakgrunn og begrunnelse"
linkTitle: "Bakgrunn"
weight: 5
lastmod: 2026-05-05T00:41:49+02:00
last_editor: Erik Hagen

---

Denne seksjonen forklarer behovet som lå bak utviklingen av SAMT-BU Docs, hvilke alternativer som ble vurdert, og hvorfor vi endte opp med å bygge en egentilpasset løsning.

## Behovet

SAMT-BU er et samarbeidsprosjekt på tvers av etater, forvaltningsnivåer og kommuner. Dokumentasjonsplattformen skal støtte dette samarbeidet konkret:

- **Ikke-tekniske fagpersoner** – jurister, informasjonsarkitekter, tjenestedesignere og kommuneansatte – skal kunne lese, kommentere og bidra med innhold uten å kjenne til Git eller kommandolinjeverktøy
- **Eksternt bidrag** – personer uten direkte tilgang til repoet skal kunne foreslå endringer som deretter godkjennes av prosjektgruppen
- **Tospråklighet** – nettstedet og redaktørgrensesnittet skal fungere på både norsk og engelsk, med tanke på internasjonalt samarbeid

## Vurderte alternativer

Vi evaluerte to kategorier av løsninger: wiki-plattformer og git-baserte CMS-løsninger.

### Wiki-plattformer

Wiki-plattformer er en naturlig kandidat for dokumentasjon med mange bidragsytere. Vi vurderte to varianter:

**MediaWiki** er programvaren bak Wikipedia. Den er moden, veldokumentert og åpen kildekode. **Semantic MediaWiki (SMW)** er en utvidelse som legger strukturerte, maskinlesbare egenskaper på wiki-sider – tenk RDF-lignende relasjoner og spørringer på tvers av sider. Gitt at SAMT-BU jobber med sammenhengende tjenester med rike metadatabehov, og har et eget team-semantics, er dette særlig relevant å vurdere.

**Funksjonell sammenligning:**

| Funksjon | Hugo + Git (valgt) | MediaWiki | Semantic MediaWiki |
|---|---|---|---|
| Hierarkisk navigasjon | ✅ | ✅ | ✅ |
| Flerspråklig innhold | ✅ | ✅ (Translate-utvidelse) | ✅ |
| Web-basert redigering for ikke-tekniske | ✅ (TipTap) | ✅ (VisualEditor) | ✅ |
| Bidragsflyt uten direkte tilgang | ✅ (PR-basert) | ⚠️ (diskusjon + godkjenning) | ⚠️ |
| Versjonskontroll og historikk | ⚠️ (git, ikke eksponert for brukere) | ✅ (innebygd, brukervenlig) | ✅ |
| Stabile lenker som overlever omdøping | ⚠️ (må bygges) | ✅ (page ID-redirects, automatisk) | ✅ |
| Permalenker til spesifikke versjoner | ⚠️ (må bygges) | ✅ (oldid-lenker, innebygd) | ✅ |
| Diff-visning mellom versjoner | ❌ | ✅ | ✅ |
| Diskusjon og kommentarer per side | ❌ (planlagt) | ✅ (diskusjonssider) | ✅ |
| Søk | ✅ (Lunr.js) | ✅ | ✅ + semantisk spørring |
| Semantiske metadata og strukturert informasjon | ⚠️ (frontmatter, manuelt) | ⚠️ (maler og kategorier) | ✅ (RDF-egenskaper, #ask) |
| Innhold fra flere repoer og team | ✅ (Hugo Modules) | ⚠️ (interwiki, ikke sømløst) | ⚠️ |
| Tilpasset visuell profil | ✅ | ⚠️ (mulig, men krevende) | ⚠️ |
| Automatisk publisering og CI/CD | ✅ | ⚠️ (ikke native) | ⚠️ |
| Tilgangskontroll per seksjon | ⚠️ (GitHub-nivå) | ✅ (granulær, innebygd) | ✅ |
| Tospråklig redaktørgrensesnitt | ✅ | ⚠️ (mulig, men krever tilpasning) | ⚠️ |

Det er verdt å merke seg at flere av funksjonene vi planlegger å bygge (stabile lenker, versjonslenker, diskusjon per side) finnes ferdig i MediaWiki og SMW.

*Ikke-funksjonelle egenskaper:* MediaWiki/SMW krever PHP-server og database (MySQL/MariaDB), mens Hugo genererer statiske filer. Dette er ikke i seg selv avgjørende, men påvirker driftsmodell, vertsvalg og integrasjon med øvrig verktøybruk i prosjektet.

### Git-baserte CMS-løsninger

Innenfor git-baserte løsninger evaluerte vi tre etablerte verktøy:

| Verktøy | Ekstern bidragsflyt | Norsk/engelsk UI | Vurdering |
|--|--|--|--|
| **Decap CMS** | ✅ Via brukernes egne GitHub-forks | ❌ Engelsk | Testet i praksis. Ikke-tekniske brukere forvirres av fork-varsler og uventede repoer i sin GitHub-konto. For høy terskel. |
| **TinaCMS / Tina Cloud** | ✅ Via leverandørens service account | ❌ Engelsk | Løser bidragsproblemet, men er en betalt SaaS-tjeneste ($49+/mnd for editorial workflow) med lukket redaktørgrensesnitt kun på engelsk og uten mulighet for innbygging i nettstedet. |
| **Keystatic** | ❌ Ikke støttet | ❌ Engelsk | Støtter ikke ekstern bidragsflyt – krever skrivetilgang for alle brukere. |

Ingen av alternativene dekket alle kravene samtidig.

## Valgt tilnærming og avveininger

Vi bygde en egentilpasset løsning basert på git og Hugo:

- **Innebygd editor** direkte i nettstedets sider – ingen ekstern portal, ingen omplanting til annet grensesnitt
- **Worker-basert bidragsflyt** – en Cloudflare Worker oppretter branch, commit og pull request på vegne av bidragsyteren, via en dedikert bot-konto. Bidragsyteren trenger ikke skrivetilgang til repoet
- **Tospråklig redaktørgrensesnitt** – alt tekst i editordialogene finnes på norsk og engelsk, styrt av nettstedets aktive språk
- **Innhold fra flere repoer** – Hugo Modules-systemet henter innhold fra team-architecture, team-semantics og andre repoer inn i ett samlet nettsted
- **Åpen kildekode, ingen leverandøravhengighet** – løsningen eier vi selv og kan videreutvikle fritt

Det viktigste argumentet mot MediaWiki/SMW var ikke teknisk, men organisatorisk: prosjektets øvrige arbeidsflyt er allerede git- og GitHub-basert, og en wiki-plattform ville innebåret et parallelt system med en annen brukermodell og en annen eierskapsstruktur. Sammenkoblingen av innhold fra flere repoer via Hugo Modules – som gjenspeiler teamstrukturen i prosjektet – har heller ingen god tilsvarende i MediaWiki.

Funksjonene der MediaWiki/SMW er sterkere (versjonskontroll eksponert for brukere, stabile lenker, diskusjon per side) er identifisert som mangler og planlagt bygd inn i løsningen over tid.

## Særlig fortrinn: tospråklighet

Ingen av de etablerte verktøyene vi evaluerte tilbyr fullt flerspråklig redaktørgrensesnitt. For SAMT-BU Docs er dette et vesentlig fortrinn: norske brukere jobber på norsk, mens internasjonale samarbeidspartnere – f.eks. ved deltakelse i initiativ som Skills Dataspace i EU – kan bruke det samme grensesnittet på engelsk.

## Mer informasjon

- [Teknisk arkitektur og nøkkelfiler](/prosjektleveranser/loesninger/cms-loesninger/samt-bu-docs/teknisk-dokumentasjon/) – detaljer om komponenter, CI/CD og oppsett
- [Veikart](/prosjektleveranser/loesninger/cms-loesninger/samt-bu-docs/veikart/) – planlagte forbedringer, inkludert fullstendig bransjebenchmark
