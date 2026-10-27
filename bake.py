#!/usr/bin/env python3
"""Embed the Job Bot ledger, feedback, and applications in dashboard.html.

Lives at Job Bot/dashboard/bake.py. Reads:
  briefs/all_jobs.jsonl            every posting the daily run examined
  briefs/feedback.json             Applied / Save / Skip marks, keyed by job URL
  applications/applications.jsonl  submitted applications and their status
  config/preferences.md            score floor and star threshold

Writes the result into the <script id="baked-data"> block of dashboard/dashboard.html.
Safe to re-run; each run replaces the previous block. Exits non-zero if the
dashboard has no data block, so a broken template fails loudly instead of
publishing stale data.
"""
import datetime
import json
import os
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent  # the Job Bot folder
HTML = ROOT / 'dashboard' / 'dashboard.html'
LEDGER = ROOT / 'briefs' / 'all_jobs.jsonl'
FEEDBACK = ROOT / 'briefs' / 'feedback.json'
APPLICATIONS = ROOT / 'applications' / 'applications.jsonl'
PREFERENCES = ROOT / 'config' / 'preferences.md'

DEFAULT_FLOOR, DEFAULT_STAR = 75, 85
BLOCK = re.compile(r'(<script id="baked-data" type="application/json">)(.*?)(</script>)', re.DOTALL)


def load_jsonl(path):
    rows = []
    if not path.exists():
        return rows
    for n, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(f'warning: skipped bad line {n} in {path.name}: {e}', file=sys.stderr)
    return rows


def load_feedback(path):
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding='utf-8') or '{}')
    except json.JSONDecodeError as e:
        print(f'warning: {path.name} is not valid JSON, baking without feedback: {e}', file=sys.stderr)
        return {}
    return data if isinstance(data, dict) else {}


def read_threshold(text, label, default):
    # Matches "Surface threshold: 75" and "**Surface threshold:** 75"
    m = re.search(label + r':\**\s*(\d{2,3})', text, re.IGNORECASE)
    return int(m.group(1)) if m else default


def main():
    prefs = PREFERENCES.read_text(encoding='utf-8') if PREFERENCES.exists() else ''
    jobs = load_jsonl(LEDGER)
    applications = load_jsonl(APPLICATIONS)
    feedback = load_feedback(FEEDBACK)

    baked = {
        'generated_at': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
        'floor': read_threshold(prefs, 'Surface threshold', DEFAULT_FLOOR),
        'star': read_threshold(prefs, 'Star threshold', DEFAULT_STAR),
        'jobs': jobs,
        'applications': applications,
        'feedback': feedback,
    }

    # Escape <, >, & so scraped text can never close the script tag early.
    payload = (json.dumps(baked, ensure_ascii=False)
               .replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026'))

    html = HTML.read_text(encoding='utf-8')
    if not BLOCK.search(html):
        sys.exit(f'error: {HTML} has no <script id="baked-data" type="application/json"> block. '
                 'Restore dashboard.html from the Job Bot setup prompt.')
    # A function replacement keeps re.sub from reading backslashes in the JSON as escapes.
    html = BLOCK.sub(lambda m: m.group(1) + payload + m.group(3), html, count=1)

    # Write to a temp file, then swap it in, so an interrupted bake never leaves a half-written page.
    tmp = HTML.with_name(HTML.name + '.tmp')
    tmp.write_text(html, encoding='utf-8')
    os.replace(tmp, HTML)

    print(f'baked {len(jobs)} jobs, {len(applications)} applications, {len(feedback)} feedback marks '
          f'(floor {baked["floor"]}, star {baked["star"]}) into {HTML.name}')


if __name__ == '__main__':
    main()
