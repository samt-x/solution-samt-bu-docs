#!/usr/bin/env python3
"""Kvittering når noen melder fra om et feilet bygg på solution-samt-bu-docs#83 (punkt C2).

Svarer med takk og status akkurat nå: siste bygg av samt-bu-docs, om et bygg pågår, og
filer som er satt til side (set_aside i /build.json).

Kjøres fra build-report-receipt.yml. Lokalt: --dry-run <login> skriver bare svaret,
og tokenen hentes fra gh hvis GITHUB_TOKEN mangler.
"""
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

DOCS_REPO = 'samt-x/samt-bu-docs'
ISSUE_REPO = 'samt-x/solution-samt-bu-docs'
ISSUE = 83
BUILD_INFO_URL = 'https://docs.samt-bu.no/build.json'
try:
    OSLO = ZoneInfo('Europe/Oslo')
except ZoneInfoNotFoundError:  # Windows uten tzdata: maskinens lokale tid
    OSLO = None


def token():
    t = os.environ.get('GITHUB_TOKEN')
    if t:
        return t
    return subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True, check=True).stdout.strip()


def api(path, data=None):
    req = urllib.request.Request(
        'https://api.github.com/' + path,
        data=json.dumps(data).encode() if data is not None else None,
        headers={'Authorization': 'Bearer ' + token(),
                 'Accept': 'application/vnd.github+json',
                 'User-Agent': 'samt-bu-docs-ci'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def runs(status):
    return api(f'repos/{DOCS_REPO}/actions/workflows/hugo.yml/runs'
               f'?branch=main&status={status}&per_page=1')['workflow_runs']


def build_info():
    # Cloudflare avviser Pythons standard User-Agent
    req = urllib.request.Request(BUILD_INFO_URL, headers={'User-Agent': 'samt-bu-docs-ci'})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except Exception as e:
        print(f'Kunne ikke lese {BUILD_INFO_URL}: {e}')
        return {}


def when(iso):
    t = datetime.fromisoformat(iso.replace('Z', '+00:00')).astimezone(OSLO)
    return t.strftime('%d.%m. kl. %H:%M')


def body(login):
    last = runs('completed')
    in_progress = runs('in_progress') or runs('queued')
    set_aside = build_info().get('set_aside') or []

    lines = [f'Takk for at du meldte fra, @{login}! Dette er et automatisk svar med status akkurat nå.', '']
    ok = None
    if last:
        run = last[0]
        ok = run['conclusion'] == 'success'
        result = 'vellykket' if ok else 'feilet'
        lines.append(f'- Siste bygg av nettstedet: **{result}** {when(run["updated_at"])} ([kjøring]({run["html_url"]})).')
    if in_progress:
        lines.append(f'- Et nytt bygg pågår nå ([kjøring]({in_progress[0]["html_url"]})). Det tar vanligvis et par minutter.')
    if set_aside:
        lines.append('- Disse filene har en feil og er holdt tilbake. Forrige versjon vises til feilen er rettet:')
        lines += [f'  - `{s["path"]}` i `{s["repo"]}`' for s in set_aside]
    lines.append('')
    if ok is False:
        lines.append('Bygget stopper fortsatt. Feilen er kjent og blir fulgt opp.')
    elif set_aside:
        lines.append('Resten av nettstedet er oppdatert. Gjelder meldingen din en av filene over, blir den rettet så snart som mulig.')
    else:
        lines.append('Nettstedet bygger normalt. Last siden på nytt for å se om endringen din er med.')
    lines.append('Noen i prosjektet ser på meldingen din og svarer her om det trengs.')
    return '\n'.join(lines) + '\n'


def main():
    if len(sys.argv) == 3 and sys.argv[1] == '--dry-run':
        print(body(sys.argv[2]))
        return
    text = body(os.environ['COMMENT_AUTHOR'])
    api(f'repos/{ISSUE_REPO}/issues/{ISSUE}/comments', {'body': text})
    print(text)


if __name__ == '__main__':
    main()
