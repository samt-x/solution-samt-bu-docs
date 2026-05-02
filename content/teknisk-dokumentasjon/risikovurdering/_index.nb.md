---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: 07e39938-5a25-44e2-8df9-d869da75683b
title: "Risikovurdering (ROS) – innebygd redigering"
linkTitle: "Risikovurdering"
weight: 45
lastmod: 2026-05-02T18:30:00+02:00
last_editor: Erik Hagen

---

Denne siden dokumenterer risikovurderingen for den serverside-komponenten i den innebygde redigeringsflyten – spesifikt bruk av `WORKER_PAT` i Cloudflare Worker-en (`auth.samt-bu.no`).

## Kontekst

Når en ekstern bidragsyter uten skrivetilgang bruker «Foreslå endring»-funksjonaliteten, utfører Cloudflare Worker-en GitHub-operasjoner (branch, commit, pull request) på vegne av brukeren. For dette kreves et GitHub-token med skrivetilgang til SAMT-X-repoene – lagret som Worker secret `WORKER_PAT`.

## Nåværende løsning

| Komponent | Verdi |
|-----------|-------|
| Token-type | Klassisk GitHub PAT, `repo`-scope |
| Konto | `samt-x-bot` – dedikert bot-konto |
| Org-tilknytning | Kun `SAMT-X`-org, ingen andre org-er eller private repoer |
| Skrivetilgang | 9 SAMT-X-innholdsrepoer via team `content-bots` |
| Lagring | Kryptert Cloudflare Worker secret – aldri eksponert i kode |

## Risikovurdering

### Risiko 1 – Lekkasje av WORKER_PAT

**Sannsynlighet:** Lav. Token er kryptert i Cloudflare, aldri i kildekode eller logger.

**Konsekvens ved lekkasje:** En angriper kan opprette branches, commits og pull requests i de 9 SAMT-X-innholdsrepoene. Ingen sletting av data eller tilgang til sensitive repoer. Alt er sporbart i GitHub audit-logg og synlig som PR.

**Kompenserende kontroller:**
- Worker-koden er hardkodet til kun å kalle `api.github.com/repos/SAMT-X/…`
- Worker krever gyldig GitHub App-token fra kaller (format-validering av `ghu_`/`ghp_`-prefiks)
- Alle operasjoner er sporbare i GitHub audit-logg
- `samt-x-bot`-kontoen er kun tilknyttet SAMT-X – ingen bredere nedslagsfelt

**Restrisiko:** Akseptabel.

### Risiko 2 – Klassisk PAT fremfor fine-grained

**Bakgrunn:** Fine-grained PAT og GitHub App user-to-server tokens ble forsøkt, men begge ga 403 på git-ref-endepunktet – trolig relatert til GitHub App-arkitektur for denne use-casen. Klassisk PAT ble valgt som pragmatisk løsning.

**Konsekvens:** Klassisk PAT med `repo`-scope gir tilgang til *alle* repoer `samt-x-bot` har tilgang til – ikke bare en eksplisitt liste. Hvis `samt-x-bot` i fremtiden gis tilgang til repoer utenfor SAMT-X (f.eks. sensitive private repoer), øker nedslagsfeltet.

**Kompenserende kontroll:** `samt-x-bot` er en dedikert konto som kun er tilknyttet SAMT-X-org. Aldri gi denne kontoen tilgang til repoer utenfor SAMT-X.

**Restrisiko:** Akseptabel så lenge kontoen holdes ren.

### Risiko 3 – Bot-konto uten organisasjonseierskap

`samt-x-bot`-kontoen er tilknyttet e-postadressen `nasjonal.arkitektur@gmail.com`. Hvis tilgangen til denne e-posten går tapt, kan PAT-en ikke roteres uten ekstra tiltak.

**Kompenserende kontroll:** Logg inn som `samt-x-bot` og roter PAT ved behov. Lagre ny PAT i Bitwarden under «Cloudflare Worker secret WORKER_PAT (samt-x-bot)».

**Fremtidig tiltak:** Flytt e-posttilknytning til en delt postboks (f.eks. `operations@samt-bu.no`) når dette er tilgjengelig.

## Rotasjon av WORKER_PAT

Hvis PAT-en må roteres (ved lekkasje eller utløp):

1. Logg inn på GitHub som `samt-x-bot`
2. Settings → Developer settings → Personal access tokens → Tokens (classic)
3. Generer nytt token (`repo`-scope, no expiration)
4. Oppdater Cloudflare Worker secret:
   ```bash
   printf "<nytt-token>" | CLOUDFLARE_API_TOKEN=<cf-token> npx wrangler secret put WORKER_PAT --config cloudflare-worker/wrangler.toml
   ```
5. Oppdater Bitwarden-noten «Cloudflare Worker secret WORKER_PAT (samt-x-bot)»
6. Slett gammelt token i GitHub
