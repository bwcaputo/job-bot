#!/usr/bin/env python3
"""Bake the current ledger + feedback + applications into the dashboard HTML.
Run after any change to all_jobs.jsonl, applications.jsonl, or feedback.json,
then call update_artifact.
Idempotent — re-running just replaces the previous baked block.
"""
import json, re, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent  # Job Bot/
HTML = ROOT / 'dashboard' / 'dashboard.html'
LEDGER = ROOT / 'briefs' / 'all_jobs.jsonl'
APPLICATIONS = ROOT / 'applications' / 'applications.jsonl'
FEEDBACK = ROOT / 'briefs' / 'feedback.json'


def load_jsonl(path):
    rows = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(f'skip bad line in {path.name}: {e}')
    return rows


jobs = load_jsonl(LEDGER)
applications = load_jsonl(APPLICATIONS)

feedback = {}
if FEEDBACK.exists():
    try:
        feedback = json.loads(FEEDBACK.read_text(encoding='utf-8') or '{}')
    except Exception:
        pass

baked = {
    'generated_at': datetime.datetime.now().isoformat(timespec='seconds'),
    'jobs': jobs,
    'applications': applications,
    'feedback': feedback,
}

# Encode as JSON. Escape </script> defensively so the JSON can't break out.
payload = json.dumps(baked, ensure_ascii=False).replace('</', '<\\/')
script_tag = f'<script id="baked-data" type="application/json">{payload}</script>\n'

html = HTML.read_text(encoding='utf-8')
# Strip any previous baked-data block
html = re.sub(r'<script id="baked-data"[^>]*>.*?</script>\n?', '', html, flags=re.DOTALL)
# Inject the new block right after the opening <meta>
html = html.replace('<meta charset="utf-8">\n', '<meta charset="utf-8">\n' + script_tag, 1)
HTML.write_text(html, encoding='utf-8')

print(f'baked {len(jobs)} jobs, {len(applications)} applications, '
      f'{len(feedback)} feedback entries into {HTML.name}')
