---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: e0e03dc4-b617-44cb-b829-a47ac7313a9d
title: Konsept for GitHub-organisasjoner og repoer
linkTitle: GitHub-struktur
weight: 20
status: null
lastmod: 2026-10-31T00:12:59+01:00
last_editor: Erik Hagen

---

Denne siden dokumenterer prinsippene for hvordan vi organiserer GitHub-organisasjoner (orgs) og repoer i SAMT-BU-plattformen – og legger grunnlaget for at strukturen skal skalere til flere prosjekter under SAMT-paraplyen.

> **Status:** Tidlig utkast. Konseptet er delvis implementert, men ikke fullt ut gjennomtenkt for scenariet med flere parallelle prosjekter. Siden oppdateres løpende.

---

## Overordnet prinsipp

Vi skiller mellom to roller:

| Rolle | Ansvar | Eksempel |
|-------|--------|---------|
| **Plattformorg** | Publiserer nettsteder, eier tema og infrastruktur | `github.com/samt-x` |
| **Prosjektorg** | Eier innholdet for ett konkret prosjekt | `github.com/samt-bu`, `github.com/samt-pb` |

`samt-x` er plattformorganisasjonen – det er her publiserte GitHub Pages-nettsteder bor, og herfra styres felles tema og CI/CD-rammeverk. Prosjektorgene er innholdseierne.

---

## Publisering via GitHub Pages

GitHub Pages publiserer nettsteder fra repoer i en org under `<org>.github.io/<repo>`. For at et nettsted skal ligge under `samt-x.github.io/`, må det tilhørende Hugo-siterepoet ligge i `samt-x`-orgen:

```
github.com/samt-x/samt-bu-docs  →  samt-x.github.io/samt-bu-docs/
github.com/samt-x/samt-pb-docs  →  samt-x.github.io/samt-pb-docs/
```

Innholdsrepoer (moduler) kan derimot ligge i **hvilken som helst org** – Hugo Module-systemet er org-agnostisk.

---

## Hugo Modules er org-agnostiske

`hugo.toml` refererer til moduler med full `github.com/<org>/<repo>`-sti. Org-grensen er usynlig for Hugo:

```toml
[[module.imports]]
path = "github.com/samt-pb/team-architecture"
```

Dette betyr at innholdsrepoene kan organiseres fritt i prosjektspesifikke orger, uten at det påvirker publiseringsstrukturen.

---

## Nåværende struktur (samt-bu-prosjektet)

Per i dag bor alle repoer i `samt-x`-orgen – både infrastruktur og innhold:

| Repo | Type | Burde ligge i |
|------|------|---------------|
| `hugo-theme-samt-bu` | Infrastruktur | `samt-x` ✅ |
| `samt-bu-docs` | Publisert site | `samt-x` ✅ |
| `team-architecture` | Innhold | `samt-x` (enn så lenge) |
| `samt-bu-drafts` | Innhold | `samt-x` (enn så lenge) |
| `solution-samt-bu-docs` | Innhold | `samt-x` (enn så lenge) |
| `samt-bu-files` | Vedlegg | `samt-x` (enn så lenge) |

Innholdsrepoene ble opprettet i `samt-x` tidlig i prosjektet. De fungerer der de er, og migrasjon er ikke prioritert – men det er notert at de konseptuelt hører hjemme i en dedikert `samt-bu`-org.

---

## Anbefalte prinsipper fremover

1. **`samt-x` = plattform.** Kun infrastrukturrepoer og Hugo site-repoer (ett per publisert nettsted) hører hjemme her.
2. **Nye prosjekter = ny org.** Opprett en org per prosjekt (`samt-pb`, `samt-pc`, ...) for innholdsrepoer. Dette gir tydelig eierskap og unngår navnekaos i `samt-x`.
3. **Delte ressurser – løst koblede.** Et repo som `team-architecture` kan i prinsippet monteres av flere Hugo-sites (f.eks. både `samt-bu-docs` og `samt-pb-docs`). Hugo Modules-systemet støtter dette uten tilpasning.
4. **Ikke migrer det som virker.** Eksisterende `samt-bu`-innholdsrepoer i `samt-x` flyttes ikke, med mindre det er en konkret grunn.

---

## Tilgangsmodell

Etablert 12. august 2026. Bakgrunn og begrunnelse i
[issue #69](https://github.com/SAMT-X/solution-samt-bu-docs/issues/69).

Tilgang gis til **team**, aldri til enkeltpersoner:

| Team | Medlemmer | Write på |
|------|-----------|----------|
| `samt-bu-core-team` | Kjernedeltakere | Alle repoer unntatt de to fredede og `information-models` |
| `samt-bu-alle` | Alle deltakere i SAMT-BU | `samt-bu-docs`, `samt-bu-drafts`, `samt-bu-files` (+ Read på `samt-bu-archi-models`) |
| `samt-bu-archimate` | ArchiMate-modellerere | `samt-bu-archi-models`, `kode-archiscripts` |
| Fagteam (`samt-bu-pilot-1…7`, `-architecture`, `-market`, `-editorial`, `-information-models`) | Deltakere i det aktuelle arbeidet | Sitt eget repo. `samt-bu-information-models` har både `information-models` og `team-semantics`, og `samt-bu-architecture` har også `team-semantics`. |

**Teamene for SAMT-BU er nøstet under `samt-bu-alle`** (fra 23. oktober 2026). Kjerneteamet og
alle fagteamene har `samt-bu-alle` som forelder. Undertemaene arver forelderens tilgang. Den som er med i et SAMT-BU-team, er
derfor automatisk med i «alle», uansett hvordan vedkommende kom inn. Teamene for plattformen
og andre formål (`solution-*`, `content-bots`, `samt-x`, `samt-bu-partners`,
`samt-bu-external-contributors`) ligger utenfor. Bakgrunn i
[issue #80](https://github.com/SAMT-X/solution-samt-bu-docs/issues/80).

**Ingen midlertidige kjernemedlemmer i eget team.** Den som skal være med i kjernearbeidet, kort
eller lenge, legges i kjerneteamet på lik linje med de andre, og tas ut igjen når perioden er over.
Rotasjonsteamet `samt-bu-core-team-rotating`, som var tenkt for dette, ble slettet 24. oktober 2026.

**To fredede repoer** har ingen redaksjonell teamtilgang, kun personlige
granter: `hugo-theme-samt-bu` og `samt-x.github.io`.
De er ikke ment å redigeres i dokumentasjonssammenheng. (`demo-repository` var
også fredet, og ble slettet 2026-10-23. `information-models` var fredet til oktober 2026, og har nå
Write for fagteamet `samt-bu-information-models`.)

Fagteamet `samt-bu-semantics` ble slått sammen med `samt-bu-information-models` 31. oktober 2026
([team-semantics#1](https://github.com/samt-x/team-semantics/issues/1)).

**Pilotteam gir ikke tilgang til fellesdokumentasjonen.** `samt-bu-docs` var
tidligere knyttet til `samt-bu-pilot-1`-teamet, noe som ga pilot 1-deltakere
skrivetilgang de andre pilotene manglet. Koblingen er fjernet.

### Vedlikehold

- Ny person i prosjektet → inn i fagteamet eller kjerneteamet. Da følger `samt-bu-alle`
  av nøstingen. Den som ikke hører til noe fagteam, legges direkte i `samt-bu-alle`
- Nytt SAMT-BU-team → sett `samt-bu-alle` som forelder (Settings → Parent team)
- Nytt modulrepo → legg det til `samt-bu-core-team`
- Nytt repo → gi det topics, se [Konvensjoner](/prosjektleveranser/loesninger/samhandlingsplattform/oppgavestyring/konvensjoner/#navn-og-topics-på-repoer)

### Medlemsoversikt

GitHub vet hvem som har tilgang, men ikke hvem personen er eller hvilken rolle den har i prosjektet.
Det står i en medlemsoversikt i det private repoet samt-bu-intern-admin, som bare kjerneteamet har
tilgang til. Oversikten vedlikeholdes manuelt, gjerne via Claude, og har navn, e-post, firma, status og
rolle i SAMT-BU. Personopplysninger står bare der.

Org-rolle, team og tilganger føres ikke for hånd. Et sjekkskript i samme repo henter dem fra GitHub,
skriver dem til en egen fil og melder avvik mot oversikten. Fremgangsmåten står i
[Administrere medlemmer og tilgang](../medlemmer-og-tilgang/).

### Hvorfor ikke org-nivå grunnrettighet

Grunnrettigheten på org-nivå er et **gulv**, ikke et utgangspunkt. Settes den
til `write`, får alle skrivetilgang til alt – og den kan ikke senkes per repo.
Så lenge de tre repoene skal holdes utenfor, er dette utelukket.

**Grunnrettigheten er «No permission»** (fra 23. oktober 2026). Den har bare
virkning for private repoer, siden alle kan lese de offentlige. Private repoer kan
derfor bare leses av team som har fått dem tildelt, og av eierne. Med Read fikk alle
medlemmer lese private repoer som `samt-bu-intern-admin`, som bare er for kjerneteamet.
Bakgrunn i [issue #72](https://github.com/SAMT-X/solution-samt-bu-docs/issues/72).

### Merk

- **Organisasjonseiere har admin overalt**, uavhengig av team. Det er en
  tilgangsvei som ikke synes i teamstrukturen.
- **`erikhag1test` har en direkte grant på `samt-bu-docs`** og er ikke
  organisasjonsmedlem. Granten er kontoens eneste tilgangsvei, og den brukes
  til testing. **Skal ikke fjernes** i en opprydding av direkte granter.

---

## Åpne spørsmål

- **Delte team-repoer:** Kan f.eks. `team-architecture` tilhøre én org men monteres av sites i `samt-x`? Ja, teknisk sett – men eierskap og tilgangsstyring bør avklares. Skal innholdet eies av prosjektet eller av teamet på tvers av prosjekter?
- **Navnekonvensjon for delte repoer:** Hvis et team-repo skal tjene flere prosjekter, bør det ikke ha prosjektspesifikt prefiks.
- **Migrasjon av eksisterende repoer:** Er det verdt å flytte `team-architecture` o.l. til en `samt-bu`-org? Påvirker CI-secrets, CMS-config og Hugo Module-pekere.
- **Tilgangsstyring på tvers av orger:** GitHub-rettigheter styres per org. Innenfor `samt-x` er dette nå løst med teammodellen over. Spørsmålet gjenstår først når innholdsrepoer faktisk flyttes til en egen `samt-bu`-org – da må teamstrukturen speiles i begge orger.

---

## Plattformvalg: GitHub vs. GitLab

> **Se [Introduksjon → Valg av git og git-plattform](/prosjektleveranser/loesninger/samhandlingsplattform/introduksjon/#valg-av-git-og-git-plattform)** for prosjektets samlede begrunnelse, avveiningene med digital suverenitet og hva som skal til for å bytte. Denne seksjonen beskriver hvordan valget påvirket teknikken bak docs.samt-bu.no, og skal krympes til det.

GitHub ble valgt fordi det er mest utbredt i Digdir og blant samarbeidspartnere (Altinn, Felles datakatalog og de fleste synlige open source-prosjekter i norsk offentlig sektor er der). Det er et pragmatisk valg – men ikke nødvendigvis det arkitektonisk sterkeste.

### Hvor GitLab hadde vært sterkere

| Parameter | GitHub | GitLab |
|-----------|--------|--------|
| Digital suverenitet | ❌ Microsoft/USA, CLOUD Act | ✅ Irsk selskap, fullt selvhostbart (CE) |
| Open source | ❌ Proprietært | ✅ Community Edition er open source |
| Hierarkisk tilgangskontroll | ⚠ Org → Teams (to nivåer, manuelt) | ✅ Groups → Subgroups → Repos med arv |
| Serverplassering | USA (primært) | Europa – bedre responstider fra Norge |

GitLabs group-hierarki ville passet naturlig til SAMT-BU-strukturen: plattformgroup → prosjektsubgroup → innholdsrepoer, med nedarvede rettigheter på hvert nivå.

### Konsekvens for Cloudflare-avhengigheten

Cloudflare ble introdusert av to grunner:

1. **OAuth-proxy (Cloudflare Worker):** GitHub OAuth krever server-side callback – Workers løser dette uten egen server. Med GitLab hadde dette sannsynligvis vært unødvendig: GitLab har innebygd OAuth-provider med finere token-scoping, og OAuth-flyten er enklere å implementere uten proxy.

2. **Cloudflare Pages (CDN/hosting):** Valgt for bedre responstider enn GitHub Pages. Med GitLab.com (europeiske servere) ville grunnresponstidene vært bedre fra Norge, og GitLab Pages + GitLab CI/CD er et fullgodt alternativ.

### Hva GitLab ikke løser

**Parallell push-problemet** («not a fast-forward» ved samtidige commits) er uavhengig av plattform – det er et fundamentalt git-problem. Løsningen er commit-batching på applikasjonsnivå, ikke et plattformbytte.

### Konklusjon

GitLab hadde gitt bedre suverenitet, bedre tilgangskontroll og trolig eliminert behovet for Cloudflare Worker. For fremtidige, lignende prosjekter i offentlig sektor bør GitLab (gjerne selvhostet) vurderes som førstevalg. For SAMT-BU er migrasjon ikke aktuelt på kort sikt – men lærdommen er notert.
