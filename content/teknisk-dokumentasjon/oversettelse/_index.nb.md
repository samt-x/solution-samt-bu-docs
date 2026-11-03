---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: 39ea7bd9-ccd9-42ee-b60c-36a3d86c4ab6
title: Oversettelse
linkTitle: Oversettelse
weight: 35
lastmod: 2026-11-03T20:59:12+01:00
last_editor: Erik Hagen

---
Nettstedet er på norsk og engelsk. Hver side har en norsk fil (`_index.nb.md`) og en engelsk fil (`_index.en.md`). Den som skriver, trenger bare skrive på ett språk. Den andre språkversjonen oppdateres etterpå.

Inntil videre gjøres oversettelsen av Claude Code, i Erik Hagens arbeidsøkter. En automatisk oversettelse i GitHub, uten et menneske i løkka, kan komme senere.

## Slik virker det

1. Noen lager eller endrer en side, i nettleseren eller i git.
2. Workflowen `translations.yml` i `samt-bu-docs` kjører. Den kjører når en side endres i et av innholdsrepoene, og ellers én gang i døgnet. Den sjekker alle repoene og skriver lista inn i [solution-samt-bu-docs#91](https://github.com/samt-x/solution-samt-bu-docs/issues/91), «Sider som må oversettes». Tallet i tittelen er antall sider på lista.
3. Ved starten og slutten av hver arbeidsøkt kjører Claude sjekken selv, på de oppdaterte repoene (den tar noen sekunder), og viser resultatet. Da kommer også endringer med som ennå ikke står i issuet. Er det sider på lista, spør Claude om de skal oversettes med en gang. Standardsvaret er ja.
4. Claude oversetter, pusher og kjører sjekken på nytt. Ved neste kjøring er sidene borte fra lista.

## Hva sjekken ser etter

Sjekken gjøres av skriptet `.github/scripts/check-translations.sh` i `samt-bu-docs`. Det deler sidene inn i tre grupper:

| Gruppe | Når |
| --- | --- |
| **Til engelsk** | Den engelske fila mangler, har plassholderen «English translation TBD» alene på en linje, eller den norske er endret etter siste commit på den engelske. |
| **Til norsk** | Det samme motsatt vei. Plassholderen er «Norsk oversettelse TBD». |
| **Sjekk strukturen** | Ulikt antall overskrifter, eller den ene teksten er under 60 % av den andres lengde. Fanger en commit som rørte begge filene, uten at den andre ble oversatt. |

Når noen lager en ny side i nettleseren, legger temaet inn plassholderen på engelsk. Siden kommer da på lista med en gang.

**Hva som telles som en endring.** Sjekken ser på git-historikken, ikke på innholdet. To typer commits teller ikke:

- **Automatiske commits** fra `github-actions[bot]` (`lastmod` og UUID-er). De rører begge filene.
- **Oversettelser.** Commit-meldingen har linjen `Oversatt-fra: nb` (eller `en`). Ellers ville selve oversettelsen få originalen til å se utdatert ut.

Engelsk til norsk sjekkes bare for endringer fra 3. november 2026 kl. 12. Før det var norsk alltid originalen.

**Unntak** står i `.github/translation-ignore.txt` i `samt-bu-docs`, med grunnen på linja over. Et unntak for en side gjelder til en av filene endres igjen. Et unntak for en mappe gjelder alt under den. Testsidene under `test-samt-bu-docs/` sjekkes som andre sider, så de også kan brukes til å teste oversettelsen.

## Når Claude oversetter

- Norsk og engelsk er likeverdige. Originalen er den fila som er endret sist.
- `id` endres aldri. `weight` og `aliases` følger originalen. `status` får verdien på målspråket (Pågår ↔ In progress, se [statussymbolene](../../brukerveiledning/innebygd-redigering/)).
- Lenker internt på nettstedet får `/en/` foran på engelsk. Lenker til Office-dokumenter bruker `ui=en-US` eller `ui=nb-NO`.
- Innhold endres ikke i oversettelsen. Feil i originalen meldes til Erik i stedet for å rettes i stillhet.
- Commit-meldingen får linjen `Oversatt-fra: nb` eller `Oversatt-fra: en`.

Oversettelsene leses ikke korrektur av et menneske før de publiseres (risiko: [solution-samt-bu-docs#92](https://github.com/samt-x/solution-samt-bu-docs/issues/92)). Fagfolk som ser feil, kan rette den andre språkversjonen direkte. Rettelsen kommer da på lista for oversettelse tilbake. Er originalen allerede riktig, kan siden føres opp som unntak.

## Kjøre sjekken selv

```bash
bash .github/scripts/check-translations.sh --root <mappe med alle innholdsrepoene>
bash .github/scripts/check-translations.sh --root <mappe> --diff    # med endringene som må oversettes
```

I Eriks arbeidsmappe er det en innpakning i roten: `check-translations.sh`.
