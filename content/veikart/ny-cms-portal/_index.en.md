---
id: 4b8f4c1b-8472-468d-9cd0-37dca86564e8
title: "Adding a new CMS portal"
linkTitle: "New CMS portal"
weight: 40
status: "New"
last_editor: Erik Hagen

---

**Need:** When a new module repository is connected to the site, a corresponding CMS portal (nb + en) must be created so that the content can be edited via Decap CMS. No consolidated template or checklist currently exists for this.

## Planned content

The checklist will cover:

1. Create `static/edit/<name>-nb/` and `<name>-en/` with `index.html` and `config.yml`
2. `config.yml` template: `repo`, `branch`, `locales`, `locale`, `sortable_fields`, fields including `status`
3. Register the portal in `static/edit/index.html` (NB) and `static/edit/en/index.html` (EN)
4. Add new branch in `edit-switcher.html` (the theme) before the `{{ else }}` block
5. Commit theme change → push → update submodule pointer in `samt-bu-docs`

*Not started.*
