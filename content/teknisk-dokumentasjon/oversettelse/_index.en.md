---
# id: auto-generated – copied values are overwritten automatically on push
id: 39ea7bd9-ccd9-42ee-b60c-36a3d86c4ab6
title: Translation
linkTitle: Translation
weight: 35
lastmod: 2026-11-03T20:59:12+01:00
last_editor: Erik Hagen

---
The site is in Norwegian and English. Each page has a Norwegian file (`_index.nb.md`) and an English file (`_index.en.md`). Writers only need to write in one language. The other language version is updated afterwards.

For the time being, translation is done by Claude Code in Erik Hagen's working sessions. Automatic translation in GitHub, without a human in the loop, may come later.

## How it works

1. Someone creates or changes a page, in the browser or in git.
2. The workflow `translations.yml` in `samt-bu-docs` runs. It runs when a page changes in one of the content repositories, and otherwise once a day. It checks all the repositories and writes the list into [solution-samt-bu-docs#91](https://github.com/samt-x/solution-samt-bu-docs/issues/91), "Sider som må oversettes" (pages to be translated). The number in the title is the number of pages on the list.
3. At the start and end of each working session, Claude runs the check itself on the updated repositories (it takes a few seconds) and shows the result. That way, changes that are not yet in the issue are included too. If there are pages on the list, Claude asks whether to translate them straight away. The default answer is yes.
4. Claude translates, pushes and runs the check again. On the next run the pages are gone from the list.

## What the check looks for

The check is done by the script `.github/scripts/check-translations.sh` in `samt-bu-docs`. It sorts the pages into three groups:

| Group | When |
| --- | --- |
| **To English** | The English file is missing, has the placeholder "English translation TBD" on a line of its own, or the Norwegian file has changed since the last commit on the English one. |
| **To Norwegian** | The same the other way round. The placeholder is "Norsk oversettelse TBD". |
| **Check the structure** | A different number of headings, or one text is under 60 % of the length of the other. Catches a commit that touched both files without the other being translated. |

When someone creates a new page in the browser, the theme adds the placeholder in English. The page is then on the list straight away.

**What counts as a change.** The check looks at the git history, not at the content. Two kinds of commits do not count:

- **Automatic commits** from `github-actions[bot]` (`lastmod` and UUIDs). They touch both files.
- **Translations.** The commit message has the line `Oversatt-fra: nb` (or `en`). Otherwise the translation itself would make the original look out of date.

English to Norwegian is only checked for changes from 12:00 on 3 November 2026. Before that, Norwegian was always the original.

**Exceptions** are listed in `.github/translation-ignore.txt` in `samt-bu-docs`, with the reason on the line above. An exception for a page applies until one of the files changes again. An exception for a folder applies to everything under it. The test pages under `test-samt-bu-docs/` are checked like other pages, so they can also be used to test the translation.

## When Claude translates

- Norwegian and English are equal. The original is the file that was changed last.
- `id` is never changed. `weight` and `aliases` follow the original. `status` gets the value in the target language (Pågår ↔ In progress, see the [status symbols](/en/prosjektleveranser/loesninger/samhandlingsplattform/samt-bu-docs/brukerveiledning/innebygd-redigering/)).
- Internal links on the site get `/en/` in front in English. Links to Office documents use `ui=en-US` or `ui=nb-NO`.
- Content is not changed in the translation. Errors in the original are reported to Erik instead of being silently corrected.
- The commit message gets the line `Oversatt-fra: nb` or `Oversatt-fra: en`.

The translations are not proofread by a person before they are published (risk: [solution-samt-bu-docs#92](https://github.com/samt-x/solution-samt-bu-docs/issues/92)). Subject experts who spot errors can correct the other language version directly. The correction then goes on the list for translation back. If the original is already correct, the page can be added as an exception.

## Running the check yourself

```bash
bash .github/scripts/check-translations.sh --root <folder with all the content repositories>
bash .github/scripts/check-translations.sh --root <folder> --diff    # with the changes to be translated
```

In Erik's working folder there is a wrapper in the root: `check-translations.sh`.
