---
id: 6c9a0913-f680-4da8-9455-aef2996197e4
title: "Administrere medlemmer og tilgang – steg for steg"
linkTitle: "Medlemmer og tilgang"
weight: 22
lastmod: 2026-10-24T15:39:17+02:00
last_editor: Erik Hagen

---

Veiledning for kjerneteamet: slik tar du inn nye deltakere i GitHub-organisasjonen samt-x, følger dem opp og tar dem ut igjen. Hvordan teamene og tilgangene henger sammen, står i [Konsept for GitHub-organisasjoner og repoer](../github-struktur/#tilgangsmodell).

---

## To kilder

| Kilde | Hva den inneholder | Hvem vedlikeholder |
|---|---|---|
| **Medlemsoversikten** (medlemmer.md i det private repoet samt-bu-intern-admin) | Navn, e-post, firma, status og rolle i SAMT-BU | Kjerneteamet, manuelt, gjerne ved å be Claude |
| **GitHub** | Hvem som er med i orgen, org-rolle, team og tilganger | Settes i GitHub, leses av sjekkskriptet |
| **GitHub-profilen** | Navn og firma | Medlemmet selv, under profilbildet → Settings → Public profile. Leses av sjekkskriptet |

Sjekkskriptet sammenligner de to og skriver resultatet til tilgang.md i samme repo, med en liste over avvik. Personopplysninger står bare i medlemsoversikten, aldri i issues, commits eller på dette nettstedet.

Statusene i oversikten er: **potensiell** (ikke invitert ennå), **invitert**, **aktiv**, **inaktiv** (medlem, men ikke lenger med i arbeidet) og **fjernet**.

## Forutsetninger

- Du er med i kjerneteamet. Det gir tilgang til samt-bu-intern-admin
- Invitasjoner og fjerning fra orgen krever at du er **eier** av samt-x
- For å kjøre sjekken selv: en klon av samt-bu-intern-admin, GitHub CLI (gh) innlogget, og bash (Git Bash på Windows). Alternativt ber du Claude gjøre det

---

## Ny deltaker

1. **Finn GitHub-brukernavnet.** Personen må ha en GitHub-konto. Be om brukernavnet, ikke e-postadressen
2. **Legg personen i riktig team**, i GitHub under Organization → Teams. Velg fagteamet (for eksempel samt-bu-pilot-3) eller kjerneteamet. Er personen ikke med i noe fagteam, bruk samt-bu-alle. Tilgang til samt-bu-alle følger av at fagteamene ligger under det. Er personen ikke medlem av orgen fra før, sender GitHub en invitasjon automatisk. Den som skal være med i kjernearbeidet en periode, legges i kjerneteamet som alle andre der, og tas ut igjen etter fremgangsmåten for deltakere som slutter. Merk at kjerneteamet også ser medlemsoversikten
3. **Før personen inn i medlemsoversikten** med status «invitert» og dagens dato i «Fra» og «Endret»
4. **Si fra til personen** at invitasjonen ligger i e-posten, og på GitHub under profilbildet → Settings → Organizations. Den kan også åpnes direkte på github.com/orgs/samt-x/invitation. **Invitasjonen utløper etter sju dager**, og må da sendes på nytt

## Invitasjonen er akseptert

1. Sett status til «aktiv» og oppdater «Endret»
2. Kjør sjekken. Den melder fra om noen har akseptert uten at lista er oppdatert

## Deltaker slutter

1. **Ta personen ut av teamene.** Skal personen fortsatt kunne lese og følge med, kan medlemskapet i orgen bli stående. Sett i så fall status «inaktiv»
2. **Skal personen helt ut:** Organization → People → personen → Remove from organization. Sett status «fjernet». Raden blir stående som historikk
3. Kjør sjekken

## Fast sjekk

Kjør sjekken etter hver endring, og ellers jevnlig, for eksempel månedlig:

```bash
bash sjekk-medlemmer.sh
```

Skriptet skriver tilgang.md og lister avvik, for eksempel en person som er med i orgen, men mangler i oversikten. Rett avvikene, og commit medlemmer.md og tilgang.md sammen.

tilgang.md viser også navn og firma fra GitHub-profilen, og lister hvem som mangler dem. Be de som står på den lista, om å fylle ut profilen.

---

## Fallgruver

- **Eiere har admin overalt**, uavhengig av team. Det synes ikke i teamstrukturen
- **Testkontoen erikhag1test** er en utenforstående med egen tilgang til samt-bu-docs, og skal ikke ryddes bort
- **Bot-kontoen samt-x-bot** eier nøklene som nettstedet bruker for å bygge og ta imot forslag. Den skal ikke fjernes
- **Gi tilgang via team, ikke til enkeltpersoner.** Direkte tilgang til et repo synes ikke i teamoversikten og blir lett glemt
