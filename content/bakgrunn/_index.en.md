---
# id: auto-generated – copied values are overwritten automatically on push
id: 4fe26ad6-aa99-46b9-b522-b5f8bfa09bf7
title: "Background and rationale"
linkTitle: "Background"
weight: 5
lastmod: 2026-05-04T18:20:02+02:00
last_editor: Erik Hagen

---

This section explains the needs that motivated the development of SAMT-BU Docs, the alternatives that were evaluated, and why we chose to build a custom solution.

## The need

SAMT-BU is a cross-agency, cross-tier collaboration involving municipalities, directorates and county authorities. The documentation platform is intended to actively support this collaboration:

- **Non-technical subject-matter experts** – lawyers, information architects, service designers and municipal staff – must be able to read, comment and contribute content without knowing Git or command-line tools
- **External contribution** – people without direct repository access must be able to suggest changes that are then reviewed and approved by the project group
- **Bilingual interface** – both the website and the editor interface must work in Norwegian and English, to support international collaboration

## Alternatives evaluated

We evaluated three established tools in the category of *git-based CMS solutions*:

| Alternative | External contribution flow | Norwegian/English UI | Assessment |
|--|--|--|--|
| **Alternative A** – fork-based CMS | ✅ Via users' own GitHub forks | ❌ English only | Tested in practice. Non-technical users are confused by fork notifications and unexpected repositories appearing in their GitHub account. Too high a barrier. |
| **Alternative B** – hosted CMS services | ✅ Via the vendor's service account | ❌ English only | Solves the contribution problem, but is a paid SaaS service with a closed editor interface available only in English and no option to embed it in the site. |
| **Alternative C** – CMS requiring write access | ❌ Not supported | ❌ English only | Does not support external contribution at all. |

None of the alternatives covered all requirements simultaneously.

## Chosen approach

We built a custom solution drawing on the best elements of the alternatives above:

- **Built-in editor** directly within the site's pages – no external portal, no redirection to a separate interface
- **Worker-based contribution flow** – a Cloudflare Worker creates a branch, commit and pull request on behalf of the contributor via a dedicated bot account. Contributors do not need write access to the repository
- **Bilingual editor interface** – all text in the editor dialogs is available in Norwegian and English, controlled by the site's active language
- **Open source, no vendor lock-in** – we own the solution and can develop it freely

## A distinctive advantage: bilingual support

None of the tools we evaluated offer a multilingual editor interface. For SAMT-BU Docs, this is a significant advantage: Norwegian users work in Norwegian, while international partners – for example, those participating in initiatives such as Skills Dataspace in the EU – can use the same interface in English.

## Further reading

- [Technical architecture and key files](/prosjektleveranser/loesninger/cms-loesninger/samt-bu-docs/teknisk-dokumentasjon/) – component details, CI/CD and setup
- [Roadmap](/prosjektleveranser/loesninger/cms-loesninger/samt-bu-docs/veikart/) – planned improvements, including full benchmark comparison
