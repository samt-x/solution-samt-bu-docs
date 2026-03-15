---
id: ed2ee794-3c97-4e2d-959d-90b235a4f3d6
title: "Opprette nytt modulrepo – steg-for-steg"
linkTitle: "Nytt modulrepo"
weight: 30
status: "Ny"
last_editor: Erik Hagen

---

**Behov:** Det finnes ingen samlet, trinnvis veiledning for å opprette et nytt Hugo-modulrepo fra bunnen og koble det til nettstedet. Prosessen krever koordinering på tvers av flere repoer og konfigurasjonsfilene.

## Planlagt innhold

Veiledningen skal dekke hele flyten fra tomt repo til publisert innhold:

1. Opprette repo i riktig GitHub-org
2. `hugo mod init github.com/<org>/<repo>`
3. Opprette innholdsstruktur (`content/_index.nb.md`, `_index.en.md`)
4. Registrere modulen i `samt-bu-docs/hugo.toml` (`[[module.imports]]`)
5. Kjøre `hugo mod get @latest` og committe `go.mod`/`go.sum`
6. Legge til i `HUGO_MODULE_REPLACEMENTS` og `inject-lastmod.py` i CI
7. Opprette kryssrepo-trigger-workflow i modulrepoet
8. Opprette CMS-portal (nb + en) i `samt-bu-docs`
9. Legge til nytt grein i `edit-switcher.html`

*Ikke påbegynt.*
