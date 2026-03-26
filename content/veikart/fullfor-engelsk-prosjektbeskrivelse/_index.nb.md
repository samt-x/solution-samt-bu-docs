---
id: 7ea3ed96-637f-4003-9212-56a886f78f86
title: "Fullfør engelsk oversettelse av prosjektbeskrivelse"
linkTitle: "Engelsk prosjektbeskrivelse"
weight: 170
status: "Pågår"
last_editor: erikhag1git (Erik Hagen)
lastmod: 2026-03-26T00:00:00+01:00

---

Engelsk oversettelse av prosjektbeskrivelsen er påbegynt, men ikke fullstendig.

## Hva er gjort

- Norsk Word-dokument (`Prosjektbeskrivelse SAMT Barn og unge.docx`) oversatt maskinelt til engelsk via pandoc + Claude
- Engelsk fil publisert i `samt-bu-files/drafts/Project description SAMT Children and Young People.docx`
- Lenket opp under [Se også / See also](/samt-bu-docs/om/om-samt-bu/) på den engelske siden

## Hva gjenstår

- **Bilder mangler:** Den engelske .docx mangler de innebygde bildene fra originalen. Pandoc fant ikke `media/`-mappen ved konvertering. Bildene må trekkes ut av original-docx og legges inn i den engelske versjonen.
- **Kvalitetssikring:** Maskinoversettelse bør gjennomgås av prosjektdeltaker med god norsk/engelsk fagkunnskap. Særlig:
  - Partnerroller og rollebeskrivelser
  - Juridiske og tekniske begreper
  - Tabeller med detaljert innhold (Digitaliseringssirkelen)
- **EN-versjon av Se også-lenke** på norsk side bør dobbeltsjekkes

## Teknisk oppskrift for å legge inn bilder

```bash
# Pakk ut media-mappe fra original-docx (en docx er en zip)
cd "S:/app-data/github/samt-x-repos/samt-bu-files/drafts"
unzip -o "Prosjektbeskrivelse SAMT Barn og unge.docx" "word/media/*" -d orig_media

# Flytt til pandoc-forventet sti og rekjør konvertering
# (forutsetter at translated_en.md finnes)
mkdir -p media
cp orig_media/word/media/* media/
pandoc "C:/Users/Win11_local/.claude/.../translated_en.md" \
  -o "Project description SAMT Children and Young People.docx" \
  --resource-path=. --wrap=none
```

## Prioritet

Middels – bør gjøres før neste eksternpresentasjon av prosjektet på engelsk.
