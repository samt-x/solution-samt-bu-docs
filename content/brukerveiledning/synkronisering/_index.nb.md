---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: d9520a6b-e499-4554-961d-86a7bacc5550
title: "Synkronisering og konflikthåndtering"
linkTitle: "Synkronisering"
weight: 20
lastmod: 2026-03-27T23:29:13+01:00
last_editor: Erik Hagen

---

Innhold i SAMT-BU Docs lever i Git-repoer. Når flere bidragsytere jobber samtidig – eller når Decap CMS lagrer en endring mens du har en lokal kopi – kan repoene komme ut av synk. Denne siden forklarer hva som skjer, og hvordan du håndterer det.

## Hjelpeskriptene

Under `S:\app-data\github\samt-x-repos\` ligger tre skript som forenkler arbeidet med alle repoene samlet:

| Skript | Funksjon |
|--------|----------|
| `pull-all.sh` / `.bat` | Henter siste endringer fra GitHub for alle repoer |
| `push-all.sh` / `.bat` | Pusher upushede lokale commits til GitHub |
| `sync-all.sh` / `.bat` | Kombinert: henter, fletter og pusher i riktig rekkefølge |

Kjør `.bat`-filene fra Filutforsker (dobbeltklikk), eller `.sh`-filene fra Git Bash.

## Anbefalt arbeidsflyt

```
Før du begynner:    sync-all
Underveis:          commit hyppig  →  push-all
Når du er ferdig:   sync-all
```

Den viktigste regelen er å **kjøre sync-all før du begynner å redigere**, ikke bare etterpå. Da er du alltid på toppen av det andre har gjort, og sammenslåingen av dine nye endringer vil sjelden feile.

## Hva `sync-all` gjør – steg for steg

For hvert repo avgjør skriptet situasjonen etter å ha hentet remote-status:

| Situasjon | Handling |
|-----------|----------|
| Likt lokalt og på GitHub | Ingenting – allerede synkronisert |
| Kun GitHub foran | `git pull` (fast-forward, ingen merge-commit) |
| Kun du foran | `git push` |
| Begge har nye commits | Rebase – dine commits legges oppå GitHub-endringene |
| Du har ucommittede endringer | Midlertidig stash → sync → stash pop |
| Konflikt som ikke kan løses automatisk | Stopp, rapport, ingen data tapes |

**Rebase** brukes fremfor vanlig merge fordi det gir ren, lineær historikk uten unødvendige merge-commits.

## Hva er en Git-konflikt?

En konflikt oppstår når **den samme linjen i den samme filen** er endret på begge sider (lokalt og på GitHub) siden sist synk. Git klarer ikke avgjøre hvilken versjon som er riktig, og stopper.

Git er derimot flink til å flette endringer som berører **ulike linjer** i samme fil automatisk – det krever normalt ingen handling fra deg.

### Vanlige scenariet der konflikter oppstår

- Du redigerer et avsnitt lokalt. Samtidig lagrer noen den samme siden via Decap CMS.
- To bidragsytere endrer vekttallet (`weight`) på samme side uavhengig av hverandre.
- Du og en kollega jobber med ulike deler av `hugo.toml` samtidig.

### Scenariet som *ikke* lager Git-konflikt, men likevel er et problem

**Krysslenking:** Noen legger til en lenke i `team-architecture`-repoet som peker til en side du nettopp har omdøpt i `samt-bu-docs`. Git ser ingen konflikt – begge endringer er gyldige. Men lenken er nå brukket. Dette oppdages kun ved bygging (`hugo` rapporterer ødelagte interne lenker) eller ved manuell sjekk. Koordiner navneendringer med berørte bidragsytere.

## Manuell konfliktløsning

Når `sync-all` melder om konflikt, er ingenting endret – rebase er avbrutt og du er tilbake til utgangspunktet. Skriptet viser hvilke filer som konfliktet.

**Slik løser du det:**

```bash
cd "S:/app-data/github/samt-x-repos/<repo-navn>"

# Start rebase på nytt
git pull --rebase

# Git stopper og markerer konfliktfilene.
# Åpne filen(e) og se etter konfliktmarkørene:
#
#   <<<<<<< HEAD          ← din lokale versjon
#   Ditt innhold her
#   =======
#   Innhold fra GitHub
#   >>>>>>> abc1234       ← remote-commit
#
# Slett markørene og behold det som er riktig (kan være begge deler).

# Marker filen som løst og fortsett
git add <filnavn>
git rebase --continue

# Push når rebase er ferdig
git push
```

**Tips:** VS Code har innebygd merge-verktøy. Åpne konfliktfilen der og klikk «Accept Current», «Accept Incoming» eller «Accept Both» per konfliktblokk.

## Spesialtilfeller

### `go.mod` og `go.sum` (Hugo-modulkonflikter)

Disse filene styrer hvilke versjoner av innholdsmoduler (team-architecture, samt-bu-drafts osv.) som er i bruk. Konflikter her er tekniske, ikke innholdsmessige.

**Løsning:**

```bash
git pull --rebase
# Konflikt i go.mod/go.sum → velg remote-versjonen og regenerer:
git checkout --theirs go.mod go.sum
hugo mod tidy
git add go.mod go.sum
git rebase --continue
git push
```

### `hugo.toml` (konfigurasjonskonflikter)

Konfigurasjonsfilen er strukturert med seksjoner. Hvis to bidragsytere har lagt til **ulike** seksjoner, skal begge beholdes. Åpne filen, slett konfliktmarkørene, og sørg for at begge tilleggene er med i den endelige filen.

### UUID-workflow og avviste pushes

Når du pusher nye Markdown-filer, kjører GitHub Actions-workflowen `ensure-uuids.yml` automatisk. Den sjekker om nye filer mangler `id`-felt (UUID), og committer dem inn direkte på `main` – gjerne i løpet av sekunder.

Hvis du pusher to ganger raskt etter hverandre (eller gjør en lokal endring rett etter første push), kan dette skje:

```
Du:       push 1 (nye filer uten id)
GitHub:   UUID-workflow committer id-felt → main er nå 1 commit foran deg
Du:       push 2 → AVVIST ("Updates were rejected because the remote contains work...")
```

**Løsning:**

```bash
git pull --rebase
git push
```

Rebase legger din commit oppå UUID-workflowens commit, og push går igjennom. Ingen data tapes – UUID-workflowens `id`-felt blir automatisk med i din lokale kopi.

**Forebygging – anbefalt arbeidsflyt:** Gjør `git pull --rebase` til en fast del av push-rutinen, ikke bare en redning etterpå:

```bash
git add <filer>
git commit -m "..."
git pull --rebase
git push
```

Dette fanger opp alt remote har fått siden sist (UUID-commits, CMS-endringer, andres commits) og minimerer avvisninger. Det eliminerer ikke alle tilfeller – UUID-workflow kan fortsatt rekke å kjøre mellom to pushes i samme sesjon – men reduserer frekvensen betydelig.

### Decap CMS vs. lokal redigering

CMS-en committer direkte til `main`. Hvis du har gjort lokale endringer på samme fil, er dette det klassiske divergens-scenariet. Løses av `sync-all` via rebase – fungerer automatisk med mindre dere har endret nøyaktig de samme linjene.

**Forebygging:** Kjør alltid `sync-all` rett før du begynner å redigere lokalt.

## Hvorfor velger vi ikke bare «behold alltid min versjon»?

Det er mulig å konfigurere automatisk konfliktløsning som alltid velger din lokale versjon (`-X ours`). Vi har valgt bort dette fordi det **stille kaster bort andres endringer** – inkludert gyldige CMS-endringer fra kollegaer. Bedre å stoppe og la et menneske bestemme hvilken versjon som er riktig.
