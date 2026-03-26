---
id: c5e5948f-2ac0-46f7-b27e-43a14f614046
title: "AI-skrivehjelp i editoren"
linkTitle: "AI-skrivehjelp"
weight: 160
status: "Ny"
lastmod: 2026-03-21T01:30:22+01:00
last_editor: erikhag1git (Erik Hagen)

---

Brukere av det innebygde redigeringsgrensesnittet kan spare tid på skriving, oversettelse og språkvask ved hjelp av AI direkte i editoren – uten at SAMT-BU-prosjektet trenger å betale for API-bruk.

## Konsept

Brukeren oppgir sin egen API-nøkkel fra en AI-leverandør de allerede har konto hos. Nøkkelen lagres lokalt i nettleseren (`localStorage`) og brukes til å kalle leverandørens API **direkte** – ingen CF Worker eller server-side komponent er nødvendig.

```
Nettleser  →  [valgt AI-leverandørs API]
               (nøkkel i localStorage, aldri sendt til SAMT-BU-infrastruktur)
```

## Støttede leverandører (planlagt)

| Leverandør | API | CORS fra nettleser | Notat |
|------------|-----|--------------------|-------|
| Anthropic Claude | `api.anthropic.com/v1/messages` | ✅ med `anthropic-dangerous-direct-browser-calls: true` | claude-haiku er billigst |
| OpenAI / ChatGPT | `api.openai.com/v1/chat/completions` | ✅ | gpt-4o-mini = lav kostnad |
| Google Gemini | `generativelanguage.googleapis.com` | ✅ via `?key=` | gratis tier finnes |
| Ollama (lokal) | `localhost:11434` | ✅ (lokal) | gratis, krever lokal installasjon |

## UX i TipTap-editoren

Tre knapper i editor-toolbar + innstillingsknapp:

```
[ Forbedre ]  [ Oversett til EN ]  [ Forkort ]  [⚙ AI-innstillinger]
```

Hvis ingen nøkkel er satt → klikk åpner innstillingsdialogen direkte.

## Teknisk implementasjon

Alle endringer i `custom-footer.html` (tema):

1. **`aiComplete(instruction, text)`** – felles funksjon som delegerer til riktig adapter
2. **Én adapter per leverandør** – pakker kallet i leverandørens format, returnerer tekst (~20 linjer per adapter)
3. **AI-innstillingsdialog** – velg leverandør, skriv inn nøkkel, velg modell, test-knapp; lagres i `localStorage`
4. **AI-toolbar i TipTap** – tre handlingsknapper + innstillingsknapp

### localStorage-nøkler

| Nøkkel | Innhold |
|--------|---------|
| `samtu-ai-provider` | `anthropic` / `openai` / `gemini` / `ollama` |
| `samtu-ai-key` | API-nøkkel |
| `samtu-ai-model` | Valgt modell (f.eks. `claude-haiku-4-5-20251001`) |

## Fordeler

- **Ingen kostnad for prosjektet** – brukeren bruker sin egen konto
- **Ingen ny infrastruktur** – ingen CF Worker-endring nødvendig
- **Utvidbart** – nye leverandører legges til som én adapter uten strukturendringer
- **Fungerer offline** for Ollama-brukere

## Prioritet

Lav – nyttig tilleggsfeature, men ikke kritisk for kjerneflyt.

## Relatert

- `themes/hugo-theme-samt-bu/layouts/partials/custom-footer.html` – TipTap-editoren og `openQuillEditDialog()`
- Veikart: [Konfliktvarsel ved redigering](/samt-bu-docs/loesninger/cms-loesninger/samt-bu-docs/veikart/rediger-konfliktvarsel/)
