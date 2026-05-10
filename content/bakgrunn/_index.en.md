---
# id: auto-generated – copied values are overwritten automatically on push
id: 4fe26ad6-aa99-46b9-b522-b5f8bfa09bf7
title: "Background and rationale"
linkTitle: "Background"
weight: 5
lastmod: 2026-05-10T13:19:43+02:00
last_editor: Erik Hagen

---

This section explains the needs that motivated the development of SAMT-BU Docs, the alternatives that were evaluated, and why we chose to build a custom solution.

## The need

SAMT-BU is a cross-agency, cross-tier collaboration involving municipalities, directorates and county authorities. The documentation platform is intended to actively support this collaboration:

- **Non-technical subject-matter experts** – lawyers, information architects, service designers and municipal staff – must be able to read, comment and contribute content without knowing Git or command-line tools
- **External contribution** – people without direct repository access must be able to suggest changes that are then reviewed and approved by the project group
- **Bilingual interface** – both the website and the editor interface must work in Norwegian and English, to support international collaboration

## Alternatives evaluated

We evaluated two categories of solutions: wiki platforms and git-based CMS solutions.

### Wiki platforms

Wiki platforms are a natural candidate for documentation with many contributors. We evaluated two variants:

**MediaWiki** is the software behind Wikipedia. It is mature, well-documented and open source. **Semantic MediaWiki (SMW)** is an extension that adds structured, machine-readable properties to wiki pages – think RDF-like relations and cross-page queries. Given that SAMT-BU works with interconnected services with rich metadata needs, and has a dedicated team-semantics, this is particularly relevant to consider.

**Functional comparison:**

| Feature | Hugo + Git (chosen) | MediaWiki | Semantic MediaWiki |
|---|---|---|---|
| Hierarchical navigation | ✅ | ✅ | ✅ |
| Multilingual content | ✅ | ✅ (Translate extension) | ✅ |
| Web-based editing for non-technical users | ✅ (TipTap) | ✅ (VisualEditor) | ✅ |
| Contribution flow without direct access | ✅ (PR-based) | ⚠️ (discussion + approval) | ⚠️ |
| Version control and history | ⚠️ (git, not exposed to users) | ✅ (built-in, user-friendly) | ✅ |
| Stable links that survive renaming | ⚠️ (to be built) | ✅ (page ID redirects, automatic) | ✅ |
| Permalinks to specific versions | ⚠️ (to be built) | ✅ (oldid links, built-in) | ✅ |
| Diff view between versions | ❌ | ✅ | ✅ |
| Discussion and comments per page | ❌ (planned) | ✅ (talk pages) | ✅ |
| Search | ✅ (Lunr.js) | ✅ | ✅ + semantic queries |
| Semantic metadata and structured information | ⚠️ (frontmatter, manual) | ⚠️ (templates and categories) | ✅ (RDF properties, #ask) |
| Content from multiple repositories and teams | ✅ (Hugo Modules) | ⚠️ (interwiki, not seamless) | ⚠️ |
| Custom visual profile | ✅ | ⚠️ (possible, but complex) | ⚠️ |
| Automated publishing and CI/CD | ✅ | ⚠️ (not native) | ⚠️ |
| Access control per section | ⚠️ (GitHub level) | ✅ (granular, built-in) | ✅ |
| Bilingual editor interface | ✅ | ⚠️ (possible, but requires customisation) | ⚠️ |

It is worth noting that several features we plan to build (stable links, version links, per-page discussion) are already available out of the box in MediaWiki and SMW.

*Non-functional properties:* MediaWiki/SMW requires a PHP server and database (MySQL/MariaDB), whereas Hugo generates static files. This is not in itself decisive, but it affects the operational model, hosting choices and integration with the project's other tooling.

### Git-based CMS solutions

Within git-based solutions, we evaluated three established tools:

| Tool | External contribution flow | Norwegian/English UI | Assessment |
|--|--|--|--|
| **Decap CMS** | ✅ Via users' own GitHub forks | ❌ English only | Tested in practice. Non-technical users are confused by fork notifications and unexpected repositories appearing in their GitHub account. Too high a barrier. |
| **TinaCMS / Tina Cloud** | ✅ Via the vendor's service account | ❌ English only | Solves the contribution problem, but is a paid SaaS service ($49+/month for editorial workflow) with a closed editor interface available only in English and no option to embed it in the site. |
| **Keystatic** | ❌ Not supported | ❌ English only | Does not support external contribution at all – requires write access for all users. |

None of the alternatives covered all requirements simultaneously.

## Chosen approach and trade-offs

We built a custom solution based on git and Hugo:

- **Built-in editor** directly within the site's pages – no external portal, no redirection to a separate interface
- **Worker-based contribution flow** – a Cloudflare Worker creates a branch, commit and pull request on behalf of the contributor via a dedicated bot account. Contributors do not need write access to the repository
- **Bilingual editor interface** – all text in the editor dialogs is available in Norwegian and English, controlled by the site's active language
- **Content from multiple repositories** – Hugo Modules pulls content from team-architecture, team-semantics and other repositories into one unified site
- **Open source, no vendor lock-in** – we own the solution and can develop it freely

The primary argument against MediaWiki/SMW was not technical but organisational: the project's existing workflow is already git- and GitHub-based, and a wiki platform would have introduced a parallel system with a different user model and ownership structure. The federation of content from multiple repositories via Hugo Modules – which reflects the project's team structure – also has no good equivalent in MediaWiki.

The areas where MediaWiki/SMW is stronger (version history exposed to users, stable links, per-page discussion) have been identified as gaps and are planned to be addressed over time.

## A distinctive advantage: bilingual support

None of the tools we evaluated offer a fully multilingual editor interface. For SAMT-BU Docs, this is a significant advantage: Norwegian users work in Norwegian, while international partners – for example, those participating in initiatives such as Skills Dataspace in the EU – can use the same interface in English.

## Further reading

- [Technical architecture and key files](/prosjektleveranser/loesninger/cms-loesninger/samt-bu-docs/teknisk-dokumentasjon/) – component details, CI/CD and setup
- [Roadmap](/prosjektleveranser/loesninger/cms-loesninger/samt-bu-docs/veikart/) – planned improvements, including full benchmark comparison
