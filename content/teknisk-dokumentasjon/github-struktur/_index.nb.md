---
id: e0e03dc4-b617-44cb-b829-a47ac7313a9d
title: "Konsept for GitHub-organisasjoner og repoer"
linkTitle: "GitHub-struktur"
weight: 30
status: "Tidlig utkast"
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

## Åpne spørsmål

- **Delte team-repoer:** Kan f.eks. `team-architecture` tilhøre én org men monteres av sites i `samt-x`? Ja, teknisk sett – men eierskap og tilgangsstyring bør avklares. Skal innholdet eies av prosjektet eller av teamet på tvers av prosjekter?
- **Navnekonvensjon for delte repoer:** Hvis et team-repo skal tjene flere prosjekter, bør det ikke ha prosjektspesifikt prefiks.
- **Migrasjon av eksisterende repoer:** Er det verdt å flytte `team-architecture` o.l. til en `samt-bu`-org? Påvirker CI-secrets, CMS-config og Hugo Module-pekere.
- **Tilgangsstyring på tvers av orger:** GitHub-rettigheter styres per org. Hvordan håndterer vi at bidragsytere fra `samt-bu`-prosjektet trenger skrivetilgang til repoer i `samt-x`?
