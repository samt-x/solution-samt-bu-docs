---
id: e40c2b29-8643-4556-9860-dc72cde6a1d4
title: "GitHub-autentisering uavhengig av CMS-valg"
linkTitle: "GitHub-auth – CMS-uavhengig"
weight: 50
status: "Ny"
# Gyldige verdier: Ny | Tidlig utkast | Pågår | Til QA | Godkjent | Avbrutt
---

## Problem

Funksjonene for inline-redigering direkte fra nettstedet («Ny side», «Slett siden», fremtidig «Rediger») er avhengige av et GitHub OAuth-token for å kalle GitHub API. Per i dag hentes dette tokenet fra Decap CMS sin localStorage-lagring:

```javascript
function getDecapToken() {
  var keys = ['netlify-cms-user', 'decap-cms-user'];
  // ...leser Decap-spesifikke nøkler
}
```

**Konsekvens:** Dersom Decap CMS byttes ut med en annen WYSIWYG-løsning (f.eks. TinaCMS, Keystatic, eller noe egenutviklet), vil disse funksjonene slutte å virke – selv om GitHub-integrasjonen i seg selv er helt uavhengig av CMS-valget.

## Ønsket løsning

Implementer en **selvstendig GitHub OAuth-flyt** for nettstedet, uavhengig av hvilket CMS som er i bruk. Token lagres under en nøytral nøkkel (f.eks. `samt-bu-github-token`) i localStorage.

### Alternativer

| Alternativ | Beskrivelse | Kompleksitet |
|------------|-------------|--------------|
| **A – Eget token-input** | Enkel dialog der brukeren limer inn et GitHub Personal Access Token | Lav |
| **B – Gjenbruk OAuth-proxy** | Bruk eksisterende Cloudflare Worker (`samt-bu-cms-auth`) til en selvstendig OAuth-flyt, lagre token under nøytral nøkkel | Middels |
| **C – Parallell token-lesing** | `getDecapToken()` utvides til å også sjekke en nøytral nøkkel – CMS-spesifikke nøkler som fallback | Lav (overgangsløsning) |

Alternativ C er en rask overgangsløsning som reduserer risikoen uten å kreve ny infrastruktur. Alternativ B er den rette langsiktige løsningen.

## Gjenstående arbeid

- Vurdere og velge alternativ
- Implementere valgt løsning
- Oppdatere `getDecapToken()` (ev. gi funksjonen et mer nøytralt navn)
- Teste at inline-redigering fungerer uten aktiv Decap-innlogging
