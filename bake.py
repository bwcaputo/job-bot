#!/usr/bin/env python3
"""Embed the Job Bot ledger, feedback, and applications in dashboard.html.

Lives at Job Bot/dashboard/bake.py. Reads:
  briefs/all_jobs.jsonl            every posting the daily runs examined
  briefs/feedback.json             Applied / Save / Skip marks, keyed by job URL
  applications/applications.jsonl  submitted applications and their status
  config/preferences.md            score floor and star threshold

Writes the result into the <script id="baked-data"> block of dashboard/dashboard.html.
Safe to re-run; each run replaces the previous block.

The page carries the last 31 days in detail, every older role that has a mark, and
lifetime totals, so it stays about the same size all semester. Exits non-zero when
dashboard.html is incomplete, so a broken page never gets published with fresh data.
"""
import datetime
import json
import math
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
WINDOW_DAYS = 31                       # covers the dashboard's 30-day views
SURFACED = {'qualified', 'stepping-stone'}
END_MARKER = '<!-- job-bot:end -->'
BLOCK = re.compile(r'(<script id="baked-data" type="application/json">)(.*?)(</script>)', re.DOTALL)


def warn(message):
    print(f'warning: {message}', file=sys.stderr)


def finite_or_none(text):
    value = float(text)
    return value if math.isfinite(value) else None


# NaN, Infinity, and overflowing numbers become null; browsers reject them in JSON.
DECODER = json.JSONDecoder(parse_constant=lambda _: None, parse_float=finite_or_none)


def load_records(path):
    """Read JSON objects one after another. Tolerates pretty-printed rows and skips junk."""
    if not path.exists():
        return []
    text = path.read_text(encoding='utf-8-sig')
    rows, i, end = [], 0, len(text)
    while i < end:
        while i < end and text[i].isspace():
            i += 1
        if i >= end:
            break
        try:
            obj, i = DECODER.raw_decode(text, i)
        except json.JSONDecodeError as e:
            warn(f'skipped unreadable text at line {text.count(chr(10), 0, i) + 1} of {path.name}: {e.msg}')
            newline = text.find('\n', i)
            if newline == -1:
                break
            i = newline + 1
            continue
        if isinstance(obj, dict):
            rows.append(obj)
        else:
            warn(f'skipped a non-object entry in {path.name}')
    return rows


def load_feedback(path):
    if not path.exists():
        return {}
    try:
        data = DECODER.decode(path.read_text(encoding='utf-8-sig').strip() or '{}')
    except json.JSONDecodeError as e:
        warn(f'{path.name} is not valid JSON, baking without feedback: {e}')
        return {}
    if not isinstance(data, dict):
        return {}
    return {url: mark for url, mark in data.items() if isinstance(mark, dict)}


def read_threshold(text, label, default):
    # Matches "Surface threshold: 75", "**Surface threshold:** 75", "Surface threshold: **75**"
    m = re.search(re.escape(label) + r'\W{0,6}(\d{2,3})\b', text, re.IGNORECASE)
    return int(m.group(1)) if m else default


def day(row):
    return str(row.get('scored_date') or '')[:10]


def text_field(row, key):
    value = row.get(key)
    return value if isinstance(value, str) and value else None


def latest_per_day(jobs):
    """A posting re-scored on the same day keeps only its last row."""
    last = {}
    for n, j in enumerate(jobs):
        if text_field(j, 'url'):
            last[(j['url'], day(j))] = n
    return [j for n, j in enumerate(jobs) if not text_field(j, 'url') or last[(j['url'], day(j))] == n]


def main():
    prefs = PREFERENCES.read_text(encoding='utf-8-sig') if PREFERENCES.exists() else ''
    jobs = latest_per_day(load_records(LEDGER))
    applications = load_records(APPLICATIONS)
    feedback = load_feedback(FEEDBACK)

    cutoff = (datetime.date.today() - datetime.timedelta(days=WINDOW_DAYS)).isoformat()
    kept = []
    for j in jobs:
        surfaced = text_field(j, 'outcome') in SURFACED
        if day(j) >= cutoff:
            # Dropped rows only feed the daily counts, so they travel as date and outcome.
            kept.append(j if surfaced else {'scored_date': j.get('scored_date'), 'outcome': text_field(j, 'outcome')})
        elif surfaced and text_field(j, 'url') in feedback:
            kept.append(j)  # older roles the user marked stay visible in the activity log

    days = sorted({day(j) for j in jobs if day(j)})
    baked = {
        'generated_at': datetime.datetime.now().astimezone().isoformat(timespec='seconds'),
        'floor': read_threshold(prefs, 'Surface threshold', DEFAULT_FLOOR),
        'star': read_threshold(prefs, 'Star threshold', DEFAULT_STAR),
        'lifetime': {
            'scanned': len(jobs),
            'qualified': len({text_field(j, 'url') for j in jobs if text_field(j, 'outcome') == 'qualified'} - {None}),
            'first_date': days[0] if days else None,
        },
        'jobs': kept,
        'applications': applications,
        'feedback': feedback,
    }

    # ASCII-only JSON, with <, >, & escaped, can't close the script tag or trip on odd characters.
    payload = (json.dumps(baked, ensure_ascii=True)
               .replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026'))

    html = HTML.read_text(encoding='utf-8-sig')
    if not html.rstrip().endswith(END_MARKER):
        sys.exit(f'error: {HTML} is incomplete (it should end with {END_MARKER}). '
                 'Restore it from Appendix G of the Job Bot setup prompt.')
    if not BLOCK.search(html):
        sys.exit(f'error: {HTML} has no <script id="baked-data" type="application/json"> block. '
                 'Restore it from Appendix G of the Job Bot setup prompt.')
    # A function replacement keeps re.sub from reading backslashes in the JSON as escapes.
    html = BLOCK.sub(lambda m: m.group(1) + payload + m.group(3), html, count=1)

    # Write to a temp file, then swap it in, so an interrupted bake never leaves a half-written page.
    tmp = HTML.with_name(HTML.name + '.tmp')
    try:
        with open(tmp, 'w', encoding='utf-8', newline='') as f:
            f.write(html)
        os.replace(tmp, HTML)
    finally:
        if tmp.exists():
            tmp.unlink()

    print(f'baked {len(kept)} of {len(jobs)} ledger rows, {len(applications)} applications, '
          f'{len(feedback)} marks (floor {baked["floor"]}, star {baked["star"]}); '
          f'{HTML.name} is {len(html) // 1024} KB')


if __name__ == '__main__':
    main()
