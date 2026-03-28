---
# id: auto-generert – kopierte verdier overskrives automatisk ved push
id: 4b8f4c1b-8472-468d-9cd0-37dca86564e8
title: "Legge til ny CMS-portal"
linkTitle: "Ny CMS-portal"
weight: 40
status: "Ny"
lastmod: 2026-03-27T23:29:13+01:00
last_editor: Erik Hagen

---

**Behov:** Når et nytt modulrepo kobles til nettstedet, må det opprettes en tilhørende CMS-portal (nb + en) slik at innholdet kan redigeres via Decap CMS. Det finnes ingen samlet mal eller sjekkliste for dette.

## Planlagt innhold

Sjekklisten skal dekke:

1. Opprette `static/edit/<navn>-nb/` og `<navn>-en/` med `index.html` og `config.yml`
2. `config.yml`-mal: `repo`, `branch`, `locales`, `locale`, `sortable_fields`, felter inkl. `status`
3. Registrere portalen i `static/edit/index.html` (NB) og `static/edit/en/index.html` (EN)
4. Legge til nytt grein i `edit-switcher.html` (temaet) før `{{ else }}`-blokken
5. Committe temaendring → push → oppdatere submodule-peker i `samt-bu-docs`

*Ikke påbegynt.*
