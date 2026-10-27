# Job Bot — Setup Prompt (v2, October 2026)

Paste this whole file into a new chat in the Claude desktop app with Claude Opus 5.5 selected. Claude interviews you, builds your Job Bot, publishes your dashboard, and schedules the daily run. Plan on about 10 minutes. Everything below the line is instructions for Claude.

---

You're setting up Job Bot for the person in this chat. Job Bot is a daily job search: it checks their target companies' career sites for roles posted in the last 7 days, scores each one against their resume, drafts a tailored one-page resume and cover letter for the best matches, and keeps a dashboard current.

Work through the steps in order. Where a step describes an action, such as connecting a folder, publishing an artifact, or creating a scheduled task, use whatever tool this session has for it. The appendices hold the exact contents of the files you'll write: copy them verbatim, filling only the `{PLACEHOLDERS}` a step names.

## 1. Interview

Open with one line: you'll ask four questions, then need their resume and target company list, and setup takes about 10 minutes.

Ask these four. Use a multiple-choice question tool if you have one (it fits up to four options per question, plus a free-text answer); otherwise ask in chat.

1. **Target roles** (free text): "What function and roles are you targeting? For example, 'Finance: FP&A, strategic finance' or 'Consulting: ERP, AI, operations.'"
2. **Geography:** My metro plus remote · Remote only · Open to relocating · Anywhere, including international.
3. **Schedule:** Weekdays at 7 AM (Recommended) · Weekdays at 6 AM · Weekly, Sunday evening · or a time they name.
4. **Selectivity:** Balanced, 75+ (Recommended) · Strict, 85+, fewer matches · Relaxed, 65+, more volume.

Then, in chat:

- Their home city, unless they chose remote only.
- Their master resume as a .docx or .pdf. A rough one works.
- 20–60 target companies, one per line. Plain names are fine. Runs rotate through long lists, since one day's search budget covers about 30 companies.

Take their name, email, phone, and LinkedIn URL from the resume, and ask only for what's missing.

## 2. Connect a folder

Ask them to connect the folder where Job Bot will live; Documents/Claude works well. In the Claude desktop app, that's the + menu beside the message box, then Add folder. Everything goes in a `Job Bot` folder inside it.

If a `Job Bot` folder from an earlier version is already there, keep its data: `briefs/`, `applications/`, `master/`, and `config/preferences.md`. Replace everything else with this version's files, add any preferences sections the new template has that theirs lacks, move old dated folders into `daily/` if they want, and tell them what you kept.

## 3. Build the files

Create this structure inside `Job Bot`:

```
config/        preferences.md, daily_brief_prompt.md, scheduled_task_prompt.md
master/        resume_master.md, projects.md, cover_letter_template.md
briefs/        all_jobs.jsonl (empty), feedback.json (containing {})
applications/  applications.jsonl (empty)
dashboard/     bake.py, dashboard.html
daily/         one dated folder per run, created by the runs
```

- `config/preferences.md`: Appendix A, filled from the interview. Turn their roles into 8–12 role keywords with title variants and a title synonym map for their function. Add anti-keywords that suit their function. Set the surface threshold from question 4 (75, 85, or 65). Put their company list under Target companies. Leave the stepping-stone tier and network contacts at "None yet"; the workbook fills those in.
- `master/resume_master.md`: the resume in Markdown, with sections for contact, summary, education, experience (newest first), projects, skills, and certifications. Keep every fact and number as written. Runs tailor only from this file, so tell them to correct anything wrong here.
- `master/projects.md`: Appendix B. If the resume lists projects, enter them in this format with `fits:` tags.
- `master/cover_letter_template.md`: Appendix C.
- `config/daily_brief_prompt.md`: Appendix D.
- `dashboard/bake.py`: Appendix F.
- `dashboard/dashboard.html`: Appendix G, with `{FIRST_NAME}` and `{SEARCH_TAGLINE}` filled in. The tagline is their function, roles, and geography in under 50 characters, such as "Finance · FP&A · Denver + remote".

Run `python3 dashboard/bake.py` once. It should report 0 jobs baked.

## 4. Publish the dashboard

Publish `dashboard/dashboard.html` as an artifact. If artifact capabilities are available, give it the `db` capability, so the Applied, Save, and Skip buttons save where daily runs can read them; without it the page still works and keeps marks in the browser. Write the artifact's URL into the Dashboard section of `config/preferences.md`.

## 5. Schedule the daily run

Fill Appendix E with their first name and the dashboard URL, and save it as `config/scheduled_task_prompt.md`. Then create a scheduled task:

- **Name:** `<first name>-job-bot`, lowercase.
- **When:** their answer to question 3.
- **Prompt:** the filled Appendix E.
- **Folder:** the `Job Bot` folder. Runs need their computer.
- **Model:** Claude Opus 5.5. If you can't set the model yourself, tell them to choose it in the task's settings under Scheduled in the sidebar.

If they already have a Job Bot scheduled task from an earlier version, tell them to delete it under Scheduled so two runs don't fire each morning.

Tell them in a line or two that runs happen while the computer is awake and the Claude desktop app is open, and that a missed run fires once the app opens again. If runs will stop to ask for approval, they can run the task once from Scheduled to approve its tools, or turn on automatic approval in the task's settings.

## 6. First run

Unless they'd rather wait for the morning, follow `config/daily_brief_prompt.md` once now so the dashboard opens with data.

## 7. Offer the workbook

Offer the 30-minute deep-tailor workbook: anti-keywords, compensation floor, network contacts, cover-letter voice, scoring weights, excluded industries, stepping-stone companies, and the project ledger. If they want it, save Appendix H as `Job Bot/workshop/deep_tailor.md`.

## 8. Wrap up

Send one short message covering:

- The dashboard link. Each morning they open it, mark matches Applied, Save, or Skip, review the drafts, and apply on the company's site; Claude in Chrome can help with Workday and Greenhouse forms.
- When runs happen and which model they use.
- Where files land: `Job Bot/daily/YYYY-MM-DD/`.
- How to tune it: tell Claude, or edit `Job Bot/config/preferences.md`.

---

## Appendix A — `config/preferences.md`

<!-- appendix: preferences_template.md -->
````markdown
# Job Search Preferences — {USER_NAME}

Every run reads this file. Edit it anytime, or tell Claude what to change.

## Candidate snapshot
- {One line, e.g. "Full-time MBA, Class of 2027, five years in supply chain operations"}
- Home base: {City, State}
- Contact line for cover letters: {email} | {phone} | {LinkedIn URL}

## Dashboard
- URL: {DASHBOARD_URL}
- Schedule: {e.g. Weekdays at 7:00 AM}

## Target function and roles
- Function: {e.g. Finance}
- Roles, in priority order: {e.g. FP&A, Strategic Finance, Corporate Development}

## Role keywords
Search phrases, 8–12, with common variants of each title.
- {e.g. "FP&A Manager", "Senior Financial Analyst", "Finance Business Partner"}

## Title synonym map
Titles that count as a match for the roles above.
- {e.g. "Finance Business Partner" → FP&A}
- {e.g. "Customer Engineer" / "Implementation Consultant" → Solutions Engineer}

## Anti-keywords
Postings containing these drop before scoring.
- {e.g. "10+ years", "Director", "Vice President"}
- {e.g. "Active TS/SCI clearance" unless you hold one}

## Target companies
One per line, 20–60 total. Add `also_search_as:` for alternate names. Runs record each company's careers site as `verified:` once they find it.
- {Company}
- {e.g. PwC (also_search_as: PricewaterhouseCoopers)}

## Stepping-stone tier
Companies where a role scoring 65 or more but under the surface threshold still shows up, with a yellow badge.
- None yet

## Network contacts
A named contact at a company earns full network points (10) on its roles. Format: Company — Person — Relationship.
- None yet

## Geography
- {Metro}: yes
- Remote-US: yes
- Hybrid {Metro}: yes
- On-site elsewhere: {yes/no}
- Travel: up to {X}%

## Scoring (0–100)
- 35: role keyword overlap with the title and description (title synonyms count)
- 20: experience fit (penalize minimums above 7 years)
- 15: location fit
- 10: domain fit
- 10: skill overlap
- 10: network (named contact, alumni at the firm, referral)

Surface threshold: {FLOOR}
Star threshold: 85

## Widening
Aim for about 3 qualified roles a day. When named targets come up short, runs may search beyond them; those roles meet the same threshold, source, and freshness rules.

## Source and freshness
- Apply links go to the employer's careers site or its applicant tracking system. Job boards only help find postings.
- Postings must be dated within the last 7 days.

## Writing rules
- Cover letter: 250 words max, active voice, specific to the posting.
- Resume: one full page (93% or more), tailored from the master resume, with every fact taken from it.

## Dealbreakers
- Credentials you don't hold (CPA, active clearance, and so on)
- W-2 contracts under 6 months
- Commission-only pay
- {Add your own}

## Compensation floor
- None set

## Industries to exclude
- None set
````
<!-- /appendix -->

## Appendix B — `master/projects.md`

<!-- appendix: projects_template.md -->
````markdown
# Project Ledger

Your active and recent projects. Every run reads this file and picks 1–3 projects per role, by relevance, for the Selected Projects section of the tailored resume and the bridge paragraph of the cover letter.

**To update it:** edit this file, or tell Claude, "Add this project to my Job Bot: [details]." New projects go at the top of their section. Move old or off-target projects to the Archive instead of deleting them; past work still backs up the resume.

**Each project needs:** name, dates, role, what you built, a quantified outcome, tools, and `fits:` tags naming the kinds of roles it supports.

---

## Active

### {Project name 1}
- **Dates:** {Start – End, or Ongoing}
- **Role:** {Your role}
- **Built:** {1–2 sentences on what you built}
- **Why it matters:** {1 sentence on what it shows, with a number}
- **Tech:** {Tools, methods, frameworks}
- **fits:** {comma-separated role types, e.g. AI consulting, finance transformation, supply chain}
- **Verify before use:** {numbers or claims to confirm before they go on a resume}

### {Project name 2}
- **Dates:**
- **Role:**
- **Built:**
- **Why it matters:**
- **Tech:**
- **fits:**

### {Project name 3, optional}
- **Dates:**
- **Role:**
- **Built:**
- **Why it matters:**
- **Tech:**
- **fits:**

---

## Archive

*(Empty for now. Move projects here once they're 12+ months old or off-target. They stay available as backup for resume claims.)*

---

## How runs use this file

When tailoring a resume:
1. Skip projects tagged `exclude_from_outputs: true`; they never appear in resumes, cover letters, or anything else that leaves the folder.
2. Rank the rest against the posting by `fits:` tags and description, and use the top 1–3. Leave the section short, or out, when nothing fits.
3. Skip any project with TBD details and flag the gap in the daily summary.
4. Use only numbers written here or in the master resume.

When drafting the cover letter's bridge paragraph, pick the single best-fit project and lead with what was built and its outcome, in two sentences or fewer.

Aim for 3–6 active projects across professional, academic, and personal work, each with a number attached ("cut close time 2 days," "$40K annual savings," "12 clients onboarded").
````
<!-- /appendix -->

## Appendix C — `master/cover_letter_template.md`

<!-- appendix: cover_letter_template.md -->
````markdown
# Cover Letter Template

*Instructions for each run: replace the bracketed sections for the role. 250 words max. Open with the angle, not "I am writing to express interest." Active voice. No em dashes as separators. Skip "leverage," "robust," "transformative," "drove," and "spearheaded"; "it's not X, it's Y" framing; inflated verbs like "serves as" or "represents"; filler transitions like "Furthermore" and "Moreover"; and trailing "-ing" phrases like "highlighting…" or "underscoring…".*

---

[Date]

[Hiring Manager Name, or "Hiring Team" if unknown]
[Company]
[City, State]

Dear [Hiring Manager Name | Hiring Team],

[**OPENING, 2 sentences.** The angle: why this role at this firm, anchored in something concrete from the posting or the firm's published work.]

[**EVIDENCE, 4–5 sentences.** Three impact examples that map to the posting's stated requirements, each leading with the outcome and its number.]

[**BRIDGE, 2–3 sentences.** Connect your differentiator (education, a recent project, unusual experience) to a specific requirement. Use the one project from `projects.md` whose `fits:` tags best match.]

[**CLOSE, 1–2 sentences.** Specific and direct. Name the practice or team if the posting does. State your location and availability.]

Sincerely,

[Your Name]
[Contact line from preferences.md]
````
<!-- /appendix -->

## Appendix D — `config/daily_brief_prompt.md`

<!-- appendix: playbook_template.md -->
````markdown
# Daily Job Brief

You're running the daily job search for the person described in `config/preferences.md`. The goal is a short list they'll act on: up to 3 roles posted in the last 7 days on the employer's own site, each scored against their resume and paired with a tailored one-page resume and a cover letter. A thin day produces a short list; never fill it with weaker roles.

Everything lives in the `Job Bot` folder attached to this task, and paths below are relative to it. If the folder is on the user's computer, build and check documents wherever you have python-docx and LibreOffice, then save the results back into the folder. The run is unattended: make reasonable calls, note them in the summary, and finish.

## 1. Load context

Read these files:

- `config/preferences.md`: thresholds, targets, keywords, title synonyms, geography, dealbreakers, stepping-stone companies, network contacts, and the dashboard URL.
- `master/resume_master.md`: the only source of facts for tailored materials.
- `master/projects.md`: projects to draw on, picked by their `fits:` tags.
- `master/cover_letter_template.md`: cover letter structure and style rules.
- `briefs/all_jobs.jsonl`: every posting examined before.
- `briefs/feedback.json` and `applications/applications.jsonl`.

If the master resume is missing, stop and say so in the summary.

## 2. Sync the dashboard marks

The dashboard stores the user's Applied, Save, and Skip clicks in its own database: a `feedback` collection with one document per job (`url`, `status`, `timestamp`). Read that collection from the dashboard artifact and merge it into `briefs/feedback.json`, keyed by URL, keeping whichever mark has the newer timestamp. A `status` of `null` means the user cleared the mark. If the dashboard's data isn't reachable, continue with feedback.json as it is.

Then add an application row (schema in §7) for every job marked `applied` that isn't in `applications/applications.jsonl` yet, using the mark's date as `applied_at`.

## 3. What qualifies

- **Employer source.** The apply link is the company's own careers page or its hosted applicant tracking system: Workday (`*.myworkdayjobs.com`, `*.myworkdaysite.com`), Greenhouse, Lever, Ashby, iCIMS, BambooHR, Workable, or SmartRecruiters. Job boards, aggregators, and staffing firms (LinkedIn, Indeed, Glassdoor, ZipRecruiter, Built In) can point you to a posting; resolve it to the employer's URL or drop it.
- **Posted within 7 calendar days.** Find the date in this order: JSON-LD `datePosted` in the page source, visible "Posted X days ago" text, an `og:updated_time`-style meta tag, or the company's job index listing the role as new. For the index case, record `posted_date` as `"active YYYY-MM-DD"` and `date_source` as `"index"`. A posting with no verifiable date doesn't qualify.
- **Still open.** Drop pages that say the job was removed, expired, or closed, or is no longer accepting applications. Quote the page's wording in `drop_reason`.
- **Within the user's rules.** Geography, anti-keywords, dealbreakers, excluded industries, and the compensation floor from preferences.md. Apply the compensation floor only when the posting publishes a range.

## 4. Search

Budget: about 30 searches, 25 page fetches, and 12 minutes per run.

**Named targets first.** For each company in preferences.md:

1. Use its `verified:` careers URL if one is recorded. Otherwise find the careers site, trying `careers.<brand>.com`, `<brand>.com/careers`, `boards.greenhouse.io/<brand>`, `job-boards.greenhouse.io/<brand>`, `jobs.lever.co/<brand>`, `<brand>.ashbyhq.com`, `<brand>.wd1.myworkdayjobs.com`, `careers-<brand>.icims.com`, `<brand>.bamboohr.com/careers`, and `apply.workable.com/<brand>`. Record the hit in preferences.md as `verified: <url>` so later runs skip the lookup.
2. Search that site for the role keywords plus the user's location or "remote". Run the same search for any `also_search_as:` names.
3. Fetch each candidate posting for title, location, date, and the full description, then apply §3.

When the list is longer than one run's budget, start with stepping-stone and network companies, then rotate through the rest so every company gets checked every few days. Record the companies you searched in today's `seen_jobs.json`, and use the last few days of those files to pick up where the rotation left off.

**Widening.** If fewer than 3 roles from named targets qualify, search discovery boards (Built In and its regional sites, such as builtincolorado.com) for the role keywords. Resolve each hit to the employer's own posting within 2 lookups or drop it. Widened roles meet the same threshold and rules.

## 5. Score

Score each surviving posting from 0 to 100 using the rubric and thresholds in preferences.md. The defaults: role keyword overlap 35 (title synonyms count), experience fit 20, location fit 15, domain fit 10, skill overlap 10, network 10.

- At or above the surface threshold: `qualified`.
- A stepping-stone company scoring 65 or more but under the threshold: `stepping-stone`.
- A named network contact at the company (full network points) and a score of 65 or more but under the threshold: `qualified` with `network_override: true`.
- Already in the ledger within the last 14 days, or marked `skipped` or `applied` in feedback: `dedup`.

Surface the top 3 qualified roles plus up to 2 stepping stones. When feedback shows 3 or more skips that share a title pattern or company, point it out in the summary and suggest an anti-keyword.

## 6. Materials

For each surfaced role, write these files into `daily/YYYY-MM-DD/` (today's date). Name them with a slug of company and role in lowercase with hyphens, such as `slalom_senior-consultant`:

- `<slug>_jd.txt`: the full posting text, its URL, and the verified posting date.
- `<slug>_score.md`: the score, line by line.
- `<slug>_cover_letter.docx`: 250 words or fewer, following `master/cover_letter_template.md`, signed with the user's name and the contact line from preferences.md.
- `<slug>_resume.docx`: the tailored resume.

**Tailoring.** Start from `master/resume_master.md`. Reorder and rephrase to match the posting's priorities, use its keywords where the resume supports them, and pick 1–3 projects from `projects.md` by their `fits:` tags. Skip projects tagged `exclude_from_outputs: true` or with TBD details. Every fact, number, title, and credential comes from the master resume or the project ledger, because the resume goes out under the user's name.

**One full page.** The resume must be exactly one US Letter page and fill at least 93% of it. Convert it to PDF and measure:

```bash
mkdir -p /tmp/jobbot && soffice --headless --convert-to pdf --outdir /tmp/jobbot "<slug>_resume.docx"
python3 - /tmp/jobbot/<slug>_resume.pdf <<'PY'
import sys, pdfplumber
with pdfplumber.open(sys.argv[1]) as pdf:
    first = pdf.pages[0]
    bottom = max((c["bottom"] for c in first.chars), default=0)
    print(f"pages={len(pdf.pages)} fill={bottom / first.height:.1%}")
PY
```

- Over one page: collapse the oldest roles into one "Earlier roles" line, cut bullets that don't match the posting, keep 3 bullets on the latest role and 1–2 on earlier ones, compress skills into 3 labeled lines, set margins to 0.5" on the sides and 0.4" top and bottom at 10pt, and merge Education with Certifications.
- Under 93%: add a relevant bullet to each of the two latest roles, grow the summary to 4–5 lines with numbers, add a skills line, add a third project, add an honors line, then move to 10.5pt with 0.55" margins.
- Keep body text between 10 and 11pt and margins between 0.4" and 0.7".

## 7. Records

**Ledger.** Append one JSON line per posting examined today, surfaced or dropped, to `briefs/all_jobs.jsonl`. Add lines; never rewrite earlier ones.

```json
{"url": "https://careers.example.com/jobs/123", "company": "Example Co", "title": "Senior Consultant",
 "location": "Denver, CO", "location_type": "Hybrid Denver", "posted_date": "2026-10-26",
 "date_source": "json-ld", "scored_date": "2026-10-27", "score": 87,
 "score_breakdown": {"role": 33, "experience": 17, "location": 15, "domain": 10, "skill": 7, "network": 5},
 "outcome": "qualified", "drop_reason": null, "stepping_stone": false, "network_override": false,
 "why_fits": "Two sentences on the fit.", "skills_mentioned": ["SQL", "FP&A"],
 "comp_low": 130000, "comp_high": 165000, "tailored_files": "daily/2026-10-27/",
 "resume_file": "example-co_senior-consultant_resume.docx",
 "cover_letter_file": "example-co_senior-consultant_cover_letter.docx"}
```

- `outcome`: `qualified`, `stepping-stone`, `stale`, `off-fit`, `dealbreaker`, or `dedup`.
- `date_source`: `json-ld`, `text`, `og`, `index`, or `null`.
- `location_type`: `<City>`, `Remote-US`, `Hybrid <City>`, `Relocation: <City>`, or `Unknown`.
- The materials fields (`tailored_files`, `resume_file`, `cover_letter_file`) apply to surfaced roles only.

**Seen list.** Write `daily/YYYY-MM-DD/seen_jobs.json` with every URL examined and the companies searched today.

**Applications.** `applications/applications.jsonl` holds one JSON line per application:

```json
{"company": "Example Co", "title": "Senior Consultant", "url": "https://careers.example.com/jobs/123",
 "applied_at": "2026-10-28", "application_status": "submitted",
 "status_history": [{"status": "submitted", "at": "2026-10-28"}], "score_at_apply": 87,
 "tailored_files": "daily/2026-10-27/", "last_email_at": null, "last_email_subject": null,
 "last_email_thread_id": null}
```

Statuses: `submitted`, `acknowledged`, `screening`, `assessment`, `interview`, `offer`, `accepted`, `declined`, `rejected`, `ghosted`, `withdrew`. To change a row, rewrite the file with that row updated.

## 8. Email check (when Gmail is connected)

For each application that is submitted, acknowledged, screening, assessment, or interview, search the last 90 days of Gmail for mail from the company's domain or an applicant-tracking sender (myworkday.com, greenhouse.io, lever.co, icims.com, ashbyhq.com), or with the company or role in the subject. Read the newest message in each thread and set the status:

- `rejected`: "not moving forward", "other candidates", "decided not to proceed", "position has been filled".
- `acknowledged`: "received your application", "thank you for applying".
- `screening` or `interview`: a request to schedule a call or interview, a calendar invite, "next steps".
- `assessment`: a test, case, or take-home assignment.
- `offer`: an offer or offer letter.

Append each change to `status_history` and update the `last_email_*` fields. Mark an application `ghosted` after 30 days with no reply since `applied_at`; a later email moves it back. This step only reads mail. It never sends, labels, archives, or deletes anything.

## 9. Refresh the dashboard

1. Run `python3 dashboard/bake.py`. It rebuilds `dashboard/dashboard.html` from the files above and exits with an error if the page's data block is missing.
2. Confirm the page's data block now includes today's `scored_date`.
3. Update the dashboard artifact at the URL in preferences.md: read it, then publish `dashboard/dashboard.html` to that same URL and leave its capabilities as they are. If the update fails, report it in the summary instead of publishing a new dashboard.
4. Save a copy of the baked page as `daily/YYYY-MM-DD/brief.html`, the day's permanent record.

## 10. Summary

End with one short paragraph: roles surfaced (top company and score), postings examined, how many dropped for freshness versus fit, and anything that needs the user, such as a blocked careers site, a skip pattern, or a missing resume. Close with "Materials: `Job Bot/daily/YYYY-MM-DD/`" and the dashboard link.

## When things go wrong

- A careers site blocks fetching: try its job index. If that fails too, skip the company today and list it in the summary.
- Searches get rate-limited: spend what's left on stepping-stone and network companies.
- Nothing qualifies: update the ledger and dashboard anyway and call it a quiet day. Keep the threshold where the user set it.
````
<!-- /appendix -->

## Appendix E — scheduled task prompt (`config/scheduled_task_prompt.md`)

<!-- appendix: scheduled_task_prompt.md -->
````markdown
Run {FIRST_NAME}'s Job Bot daily brief.

The `Job Bot` folder is attached to this task. Read `Job Bot/config/daily_brief_prompt.md` and follow it from start to finish: search, scoring, materials, records, the dashboard update, and the closing summary.

Dashboard: {DASHBOARD_URL}
````
<!-- /appendix -->

## Appendix F — `dashboard/bake.py`

<!-- appendix: bake.py -->
````python
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
````
<!-- /appendix -->

## Appendix G — `dashboard/dashboard.html`

<!-- appendix: dashboard.html -->
````html
<title>{FIRST_NAME}'s Job Bot</title>
<meta name="claude:viewport-fit-sides" content="cover">
<script id="baked-data" type="application/json">{}</script>
<style>
  /* Layout: one centered column. Today's brief and the KPIs sit above history, charts, and trackers. */
  :root {
    --bg: #f6f7f9; --paper: #ffffff; --ink: #14171c; --muted: #5d6573; --line: #e2e5ea;
    --navy: #1f3a5f; --navy-soft: #e7edf6;
    --yellow: #f5c518; --yellow-soft: #fff6cc; --yellow-ink: #6f5600; --on-yellow: #14171c;
    --green: #256b30; --green-soft: #e4f3e7;
    --red: #a8382c; --red-soft: #fbeaea;
    --grey-soft: #eef0f3;
    --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    --mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg: #0f1216; --paper: #171b21; --ink: #e7eaef; --muted: #9ba4b1; --line: #2a3039;
      --navy: #93b4e0; --navy-soft: #1b283a;
      --yellow: #f5c518; --yellow-soft: #352c0c; --yellow-ink: #f2d35f; --on-yellow: #14171c;
      --green: #74c983; --green-soft: #15301b;
      --red: #f0958a; --red-soft: #3a1d1a;
      --grey-soft: #222831;
      color-scheme: dark;
    }
  }
  :root[data-theme="dark"] {
    --bg: #0f1216; --paper: #171b21; --ink: #e7eaef; --muted: #9ba4b1; --line: #2a3039;
    --navy: #93b4e0; --navy-soft: #1b283a;
    --yellow: #f5c518; --yellow-soft: #352c0c; --yellow-ink: #f2d35f; --on-yellow: #14171c;
    --green: #74c983; --green-soft: #15301b;
    --red: #f0958a; --red-soft: #3a1d1a;
    --grey-soft: #222831;
    color-scheme: dark;
  }
  *, *::before, *::after { box-sizing: border-box; }
  [hidden] { display: none !important; }
  body { margin: 0; font-family: var(--font); color: var(--ink); background: var(--bg); font-size: 14px; line-height: 1.45; }
  .wrap { max-width: 1200px; margin: 0 auto; padding-block: 18px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); display: grid; gap: 14px; }
  .wrap-inner { display: grid; gap: 14px; min-width: 0; }
  code { font-family: var(--mono); font-size: 12px; }
  a { color: var(--navy); }
  header { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: baseline; gap: 6px 14px; padding-bottom: 12px; border-bottom: 2px solid var(--ink); }
  header h1 { margin: 0; font-size: 22px; letter-spacing: -0.01em; text-wrap: balance; }
  .meta { color: var(--muted); font-size: 12px; }
  .pulse { display: inline-block; width: 8px; height: 8px; background: var(--green); border-radius: 50%; margin-right: 6px; vertical-align: middle; animation: pulse 1.6s ease-in-out infinite; }
  @keyframes pulse { 0%, 100% { opacity: 1 } 50% { opacity: 0.3 } }
  @media (prefers-reduced-motion: reduce) { .pulse { animation: none; } }

  .panel { background: var(--paper); border: 1px solid var(--line); border-radius: 6px; padding: 14px 16px; min-width: 0; }
  .panel h2 { margin: 0 0 10px; font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--navy); }
  .kpi-row { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; }
  .kpi { background: var(--paper); border: 1px solid var(--line); padding: 14px 16px; border-radius: 6px; min-width: 0; }
  .kpi .label { font-size: 11px; text-transform: uppercase; color: var(--muted); letter-spacing: 0.05em; }
  .kpi .value { font-size: 30px; font-weight: 600; line-height: 1.1; margin-top: 6px; font-variant-numeric: tabular-nums; }
  .kpi .sub { font-size: 11px; color: var(--muted); margin-top: 4px; }
  .lifetime-line { text-align: center; color: var(--muted); font-size: 12px; }
  .lifetime-line strong { color: var(--ink); font-variant-numeric: tabular-nums; }
  .grid-2 { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }
  .chart-wrap { position: relative; height: 240px; }
  .chart-note { color: var(--muted); font-size: 12px; padding: 10px 0; }

  .table-scroll { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th, td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
  th { font-size: 11px; text-transform: uppercase; color: var(--muted); letter-spacing: 0.05em; font-weight: 600; white-space: nowrap; }
  td.score { font-weight: 600; font-variant-numeric: tabular-nums; }
  .sub { color: var(--muted); font-size: 11px; }
  .truncate { max-width: 280px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

  .chip { display: inline-block; padding: 2px 7px; border-radius: 10px; font-size: 11px; font-weight: 600; white-space: nowrap; }
  .chip-green { background: var(--green-soft); color: var(--green); }
  .chip-yellow { background: var(--yellow-soft); color: var(--yellow-ink); }
  .chip-grey { background: var(--grey-soft); color: var(--muted); }
  .chip-navy { background: var(--navy-soft); color: var(--navy); }
  .chip-red { background: var(--red-soft); color: var(--red); }

  .btn { font: inherit; font-size: 12px; cursor: pointer; padding: 5px 10px; border-radius: 4px; border: 1px solid var(--ink); background: var(--paper); color: var(--ink); display: inline-block; text-align: center; text-decoration: none; line-height: 1.3; }
  .btn:hover { background: var(--ink); color: var(--paper); }
  .btn:focus-visible, .tab:focus-visible, summary:focus-visible { outline: 2px solid var(--navy); outline-offset: 2px; }
  .btn-small { padding: 2px 8px; font-size: 11px; }
  .btn.is-applied { background: var(--green); border-color: var(--green); color: var(--paper); }
  .btn.is-saved { background: var(--yellow); border-color: var(--yellow); color: var(--on-yellow); }
  .btn.is-skipped { background: var(--muted); border-color: var(--muted); color: var(--paper); }
  .mark-row { display: flex; gap: 4px; }
  .mark-row .btn { flex: 1; }

  .tabs { display: flex; flex-wrap: wrap; border-bottom: 1px solid var(--line); margin-bottom: 10px; }
  .tab { font: inherit; background: none; border: 0; border-bottom: 2px solid transparent; padding: 8px 14px; cursor: pointer; font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); }
  .tab[aria-pressed="true"] { color: var(--ink); border-bottom-color: var(--yellow); font-weight: 600; }

  .err { background: var(--red-soft); border: 1px solid var(--red); color: var(--ink); padding: 12px 14px; border-radius: 6px; font-size: 13px; }
  .empty { text-align: center; padding: 32px 20px; color: var(--muted); }
  .empty h2 { color: var(--navy); margin-bottom: 6px; }
  .rules { background: var(--bg); border: 1px dashed var(--line); border-radius: 6px; padding: 14px; margin: 18px auto 0; text-align: left; max-width: 560px; color: var(--ink); }
  .quiet-day { padding: 18px; text-align: center; background: var(--bg); border-radius: 6px; color: var(--muted); }
  .quiet-day strong { color: var(--ink); display: block; margin-bottom: 4px; }

  /* Today's brief */
  .today-counts { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin-bottom: 14px; padding: 12px 14px; background: var(--bg); border: 1px solid var(--line); border-radius: 6px; }
  .today-counts .tc { text-align: center; }
  .today-counts .n { font-size: 24px; font-weight: 700; display: block; line-height: 1.1; font-variant-numeric: tabular-nums; }
  .today-counts .lbl { font-size: 11px; text-transform: uppercase; color: var(--muted); letter-spacing: 0.05em; margin-top: 4px; display: block; }
  .today-counts .disqualified .n { color: var(--muted); }
  .today-counts .qualified .n { color: var(--green); }
  .today-counts .applied .n { color: var(--navy); }
  .threshold-note { grid-column: 1 / -1; text-align: center; font-size: 11px; color: var(--muted); padding-top: 6px; border-top: 1px dashed var(--line); }
  .today-cards { display: grid; gap: 10px; }
  .today-card { display: grid; grid-template-columns: 72px minmax(0, 1fr) auto; gap: 14px; padding: 14px; border: 1px solid var(--line); border-radius: 6px; background: var(--paper); align-items: center; }
  .today-card.top { border-left: 6px solid var(--yellow); }
  .today-score { font-size: 28px; font-weight: 700; text-align: center; padding: 8px 0; border-radius: 6px; font-variant-numeric: tabular-nums; }
  .today-score.green { background: var(--green-soft); color: var(--green); }
  .today-score.yellow { background: var(--yellow-soft); color: var(--yellow-ink); }
  .today-meta { color: var(--muted); font-size: 12px; margin-top: 3px; }
  .today-why { font-size: 13px; margin-top: 6px; }
  .today-actions { display: flex; flex-direction: column; gap: 6px; min-width: 150px; }
  .materials { margin-top: 8px; font-size: 12px; color: var(--muted); display: flex; flex-wrap: wrap; align-items: center; gap: 6px; }
  .materials .files { flex-basis: 100%; }
  .materials code { color: var(--ink); overflow-wrap: anywhere; }

  /* Applications */
  .app-metrics { display: grid; grid-template-columns: repeat(6, minmax(0, 1fr)); gap: 8px; margin-bottom: 14px; }
  .app-metrics .tile { background: var(--bg); border: 1px solid var(--line); border-radius: 6px; padding: 10px 8px; text-align: center; }
  .app-metrics .tile strong { display: block; font-size: 22px; line-height: 1.1; font-variant-numeric: tabular-nums; }
  .app-metrics .tile .l { display: block; font-size: 10px; text-transform: uppercase; color: var(--muted); letter-spacing: 0.05em; margin-top: 4px; }
  .app-metrics .acknowledged strong { color: var(--yellow-ink); }
  .app-metrics .in-progress strong { color: var(--green); }
  .app-metrics .rejected strong { color: var(--red); }
  .app-metrics .offer strong { color: var(--green); }
  .app-metrics .rate strong { color: var(--navy); }

  /* Run history */
  .runs { display: grid; gap: 8px; }
  .run-row { border: 1px solid var(--line); border-radius: 6px; background: var(--paper); overflow: hidden; }
  .run-row[open] { border-color: var(--navy); }
  .run-summary { padding: 12px 14px; cursor: pointer; display: grid; grid-template-columns: minmax(0, 1fr) repeat(4, auto) minmax(0, 240px); gap: 18px; align-items: center; list-style: none; }
  .run-summary::-webkit-details-marker { display: none; }
  .run-summary:hover { background: var(--bg); }
  .run-date { font-weight: 600; }
  .run-date .weekday { color: var(--muted); font-weight: 400; margin-left: 6px; font-size: 12px; }
  .run-stat { color: var(--muted); font-size: 11px; text-align: center; min-width: 60px; }
  .run-stat strong { font-size: 18px; display: block; line-height: 1.1; font-variant-numeric: tabular-nums; }
  .run-stat.scanned strong { color: var(--ink); }
  .run-stat.qualified strong { color: var(--green); }
  .run-stat.applied strong { color: var(--navy); }
  .run-stat .lbl { display: block; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px; }
  .run-top { font-size: 12px; color: var(--muted); text-align: right; }
  .run-top strong { color: var(--ink); }
  .run-detail { padding: 0 14px 14px; border-top: 1px solid var(--line); }
  .drops { margin-top: 10px; color: var(--muted); font-size: 11px; }
  footer { text-align: center; color: var(--muted); font-size: 11px; padding: 6px 0 12px; }

  @media (max-width: 760px) {
    .kpi-row { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .grid-2 { grid-template-columns: minmax(0, 1fr); }
    .app-metrics { grid-template-columns: repeat(3, minmax(0, 1fr)); }
    .run-summary { grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; }
    .run-summary .run-date, .run-summary .run-top { grid-column: 1 / -1; text-align: left; }
  }
  @media (max-width: 560px) {
    .today-counts { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .today-card { grid-template-columns: 60px minmax(0, 1fr); }
    .today-actions { grid-column: 1 / -1; min-width: 0; }
    .app-metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  }
</style>

<div class="wrap">
  <header>
    <div>
      <h1>{FIRST_NAME}'s Job Bot</h1>
      <div class="meta"><span class="pulse"></span><span id="status-text">Loading…</span></div>
    </div>
    <div class="meta">{SEARCH_TAGLINE}</div>
  </header>

  <div id="err-state" class="err" hidden></div>

  <div id="empty-state" hidden>
    <div class="empty panel">
      <h2>No runs yet</h2>
      <p>Your first run fills this in. Runs fire on the schedule you picked while the Claude desktop app is open.</p>
      <div class="rules" id="rules-box"></div>
    </div>
  </div>

  <div id="data-state" class="wrap-inner" hidden>
    <section class="panel">
      <h2>Today's brief · <span id="today-date"></span></h2>
      <div id="today-counts" class="today-counts"></div>
      <div id="today-cards" class="today-cards"></div>
    </section>

    <div class="kpi-row">
      <div class="kpi"><div class="label">Jobs scanned (30d)</div><div class="value" id="kpi-scanned">0</div><div class="sub" id="kpi-scanned-sub">—</div></div>
      <div class="kpi"><div class="label" id="kpi-qualified-label">Qualified (30d)</div><div class="value" id="kpi-qualified">0</div><div class="sub" id="kpi-qualified-sub">—</div></div>
      <div class="kpi"><div class="label">Applied (30d)</div><div class="value" id="kpi-applied">0</div><div class="sub" id="kpi-applied-sub">—</div></div>
      <div class="kpi"><div class="label">Apply rate</div><div class="value" id="kpi-rate">—</div><div class="sub">applied ÷ qualified</div></div>
    </div>
    <div class="lifetime-line" id="lifetime-line">—</div>

    <section class="panel">
      <h2>Run history · most recent first</h2>
      <div id="run-history" class="runs"></div>
    </section>

    <section class="panel">
      <h2>Daily volume · last 30 days</h2>
      <div class="chart-wrap"><canvas id="chart-volume" aria-label="Jobs scanned, qualified, and applied per day"></canvas></div>
    </section>

    <div class="grid-2">
      <section class="panel">
        <h2>Where the qualified jobs are</h2>
        <div class="chart-wrap"><canvas id="chart-geo" aria-label="Qualified jobs by location"></canvas></div>
      </section>
      <section class="panel">
        <h2>Top skills in qualified JDs</h2>
        <div class="chart-wrap"><canvas id="chart-skills" aria-label="Most-mentioned skills in qualified job descriptions"></canvas></div>
      </section>
    </div>

    <section class="panel">
      <h2>My applications · submitted and recruiter activity</h2>
      <div class="app-metrics" id="app-metrics"></div>
      <div class="tabs" role="group" aria-label="Filter applications">
        <button class="tab" data-apps-filter="active">In progress</button>
        <button class="tab" data-apps-filter="lost">Closed</button>
        <button class="tab" data-apps-filter="won">Offers</button>
        <button class="tab" data-apps-filter="all">All</button>
      </div>
      <div id="apps-table-wrap"></div>
    </section>

    <section class="panel">
      <h2>Active pipeline · qualified, no decision yet</h2>
      <div id="pipeline-table-wrap"></div>
    </section>

    <section class="panel">
      <h2>Activity log</h2>
      <div class="tabs" role="group" aria-label="Filter activity">
        <button class="tab" data-tab="applied">Applied</button>
        <button class="tab" data-tab="skipped">Skipped</button>
        <button class="tab" data-tab="saved">Saved for later</button>
      </div>
      <div id="log-table-wrap"></div>
    </section>
  </div>

  <footer>
    Built from <code>Job Bot/briefs/all_jobs.jsonl</code>. Edit <code>Job Bot/config/preferences.md</code> or tell Claude what to change.
    <span id="sync-note"></span>
  </footer>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.5.0/dist/chart.umd.js" integrity="sha384-iU8HYtnGQ8Cy4zl7gbNMOhsDTTKX02BTXptVP/vqAWIaTfM7isw76iyZCsjL2eVi" crossorigin="anonymous"></script>

<script>
'use strict';

const LOCAL_KEY = 'jobbot_feedback_v2';
const MARKS = { applied: 'Applied', saved: 'Save', skipped: 'Skip' };
const APP_STATUS = {
  submitted:    { label: 'Submitted',    chip: 'chip-navy',   bucket: 'active' },
  acknowledged: { label: 'Acknowledged', chip: 'chip-navy',   bucket: 'active' },
  screening:    { label: 'Screening',    chip: 'chip-yellow', bucket: 'active' },
  assessment:   { label: 'Assessment',   chip: 'chip-yellow', bucket: 'active' },
  interview:    { label: 'Interview',    chip: 'chip-yellow', bucket: 'active' },
  offer:        { label: 'Offer',        chip: 'chip-green',  bucket: 'won'    },
  accepted:     { label: 'Accepted',     chip: 'chip-green',  bucket: 'won'    },
  declined:     { label: 'Declined',     chip: 'chip-grey',   bucket: 'lost'   },
  rejected:     { label: 'Rejected',     chip: 'chip-red',    bucket: 'lost'   },
  ghosted:      { label: 'Ghosted',      chip: 'chip-grey',   bucket: 'lost'   },
  withdrew:     { label: 'Withdrew',     chip: 'chip-grey',   bucket: 'lost'   },
};
const IN_PROGRESS = ['screening', 'assessment', 'interview', 'interviewing', 'phone-screen', 'onsite', 'final-round', 'reference-check'];

const state = {
  jobs: [], applications: [], feedback: {}, floor: 75, star: 85, generatedAt: null,
  tab: 'applied', appsFilter: 'active',
};
let localMarks = readLocal();   // marks made in this browser, kept as a fallback
let db = null;                  // the artifact's database, when this view has one
const writeChains = {};         // one write at a time per job

// ---------- helpers ----------
function esc(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}
// Only http(s) links reach the page; scraped data never becomes a javascript: URL.
function safeUrl(u) {
  try { const x = new URL(String(u)); return (x.protocol === 'https:' || x.protocol === 'http:') ? x.href : ''; }
  catch { return ''; }
}
function localDay(d = new Date()) {
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
}
function dayOf(s) { return String(s || '').slice(0, 10); }
function parseDay(s) {
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(dayOf(s));
  return m ? new Date(+m[1], +m[2] - 1, +m[3]) : null;
}
function daysAgo(s) {
  const d = parseDay(s);
  if (!d) return Infinity;
  const today = new Date(); today.setHours(0, 0, 0, 0);
  return Math.round((today - d) / 86400000);
}
function lastNDays(n) { return state.jobs.filter(j => daysAgo(j.scored_date) <= n); }
function statusOf(url) { return (state.feedback[url] || {}).status || null; }
function pct(a, b) { return b ? `${Math.round(100 * a / b)}%` : '—'; }
function cssVar(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }
function plural(n, word) { return `${n} ${word}${n === 1 ? '' : 's'}`; }
function table(head, rows) {
  return `<div class="table-scroll"><table><thead><tr>${head.map(h => `<th>${h}</th>`).join('')}</tr></thead><tbody>${rows}</tbody></table></div>`;
}

// cyrb53: a short, path-safe database id for each job URL.
function markId(url) {
  let h1 = 0xdeadbeef, h2 = 0x41c6ce57;
  const s = String(url);
  for (let i = 0; i < s.length; i++) {
    const ch = s.charCodeAt(i);
    h1 = Math.imul(h1 ^ ch, 2654435761);
    h2 = Math.imul(h2 ^ ch, 1597334677);
  }
  h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909);
  h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909);
  return 'j' + (4294967296 * (2097151 & h2) + (h1 >>> 0)).toString(36);
}

// ---------- feedback (Applied / Save / Skip) ----------
function readLocal() {
  try { return JSON.parse(localStorage.getItem(LOCAL_KEY) || '{}') || {}; } catch { return {}; }
}
function writeLocal() {
  try { localStorage.setItem(LOCAL_KEY, JSON.stringify(localMarks)); } catch { /* storage blocked; marks still live in memory */ }
}
// Each source maps job URL -> {status, timestamp}. The newest timestamp wins; status null clears a mark.
function mergeMarks(source) {
  for (const [url, mark] of Object.entries(source || {})) {
    if (!mark || typeof mark !== 'object') continue;
    const cur = state.feedback[url];
    if (!cur || (Date.parse(mark.timestamp) || 0) >= (Date.parse(cur.timestamp) || 0)) state.feedback[url] = mark;
  }
}
function setSyncNote(text) { document.getElementById('sync-note').textContent = text; }

function setStatus(url, status) {
  const next = statusOf(url) === status ? null : status; // clicking the active mark clears it
  const mark = { status: next, timestamp: new Date().toISOString() };
  state.feedback[url] = mark;
  localMarks[url] = mark;
  writeLocal();
  renderAll();
  if (!db) return;
  const ref = db.collection('feedback').doc(markId(url));
  writeChains[url] = (writeChains[url] || Promise.resolve())
    .then(() => ref.set({ url, status: mark.status, timestamp: mark.timestamp }))
    .catch(e => {
      setSyncNote(e && e.code === 'quota_exceeded'
        ? 'Dashboard storage is full, so new marks save in this browser only.'
        : 'That mark saved in this browser but did not reach the dashboard database. Click it again to retry.');
    });
}

const LOCAL_ONLY = 'Marks save in this browser only. Tell Claude "mark <company> applied" to record one for the next run.';
async function connectDb() {
  if (!window.claude || typeof window.claude.use !== 'function') { setSyncNote(LOCAL_ONLY); return; }
  try { db = await window.claude.use('db'); } catch { db = null; }
  if (!db) { setSyncNote(LOCAL_ONLY); return; }
  db.collection('feedback').onSnapshot(snap => {
    const remote = {};
    snap.docs.forEach(d => {
      const v = d.data();
      if (v && typeof v.url === 'string') remote[v.url] = { status: v.status ?? null, timestamp: v.timestamp || null };
    });
    mergeMarks(remote);
    setSyncNote('Your marks sync to the next run.');
    renderAll();
  }, () => {
    db = null;
    setSyncNote(LOCAL_ONLY);
  });
}

// ---------- shared fragments ----------
function markButtons(url) {
  const s = statusOf(url);
  return Object.entries(MARKS).map(([m, label]) =>
    `<button class="btn${s === m ? ' is-' + m : ''}" data-mark="${m}" data-url="${esc(url)}" aria-pressed="${s === m}">${label}</button>`
  ).join('');
}
function scoreChip(j) {
  return `<span class="chip ${(j.score || 0) >= state.star ? 'chip-green' : 'chip-yellow'}">${esc(j.score ?? '–')}</span>`;
}
function jdLink(j, text) {
  const href = safeUrl(j.url);
  return href ? `<a href="${esc(href)}" target="_blank" rel="noopener noreferrer">${esc(text)}</a>` : esc(text);
}
function materials(j) {
  const folder = j.tailored_files || '';
  if (!folder) return '';
  const files = [j.resume_file, j.cover_letter_file].filter(Boolean).map(f => `<code>${esc(f)}</code>`).join(' · ');
  return `<div class="materials">Materials: <code>${esc(folder)}</code>
    <button class="btn btn-small" data-copy="${esc(folder)}">Copy path</button>
    ${files ? `<span class="files">${files}</span>` : ''}</div>`;
}

// ---------- render ----------
function renderAll() {
  if (!state.jobs.length) {
    document.getElementById('empty-state').hidden = false;
    document.getElementById('data-state').hidden = true;
    document.getElementById('rules-box').innerHTML = `<strong>Search rules in effect</strong><br>
      Source: company career sites only, no job aggregators<br>
      Freshness: posted within 7 days, with a verified date<br>
      Output: up to 3 matches a day, never padded<br>
      Match floor: ${esc(state.floor)}, star at ${esc(state.star)}`;
    return;
  }
  document.getElementById('empty-state').hidden = true;
  document.getElementById('data-state').hidden = false;
  renderKpis();
  renderToday();
  renderRunHistory();
  renderCharts();
  renderApplications();
  renderPipeline();
  renderLog();
  markTabs();
}

function renderKpis() {
  const last30 = lastNDays(30);
  const q30 = last30.filter(j => j.outcome === 'qualified');
  const applied = q30.filter(j => statusOf(j.url) === 'applied').length;
  const skipped = q30.filter(j => statusOf(j.url) === 'skipped').length;
  const saved = q30.filter(j => statusOf(j.url) === 'saved').length;
  document.getElementById('kpi-scanned').textContent = last30.length;
  document.getElementById('kpi-scanned-sub').textContent = `${lastNDays(7).length} in the last 7 days`;
  document.getElementById('kpi-qualified-label').textContent = `Qualified ${state.floor}+ (30d)`;
  document.getElementById('kpi-qualified').textContent = q30.length;
  document.getElementById('kpi-qualified-sub').textContent = `${pct(q30.length, last30.length)} pass rate`;
  document.getElementById('kpi-applied').textContent = applied;
  document.getElementById('kpi-applied-sub').textContent = `${skipped} skipped · ${saved} saved`;
  document.getElementById('kpi-rate').textContent = pct(applied, q30.length);

  const all = state.jobs;
  const allQ = all.filter(j => j.outcome === 'qualified');
  const allApplied = allQ.filter(j => statusOf(j.url) === 'applied').length;
  const first = all.map(j => dayOf(j.scored_date)).filter(Boolean).sort()[0];
  const days = first ? Math.max(1, daysAgo(first) + 1) : 1;
  document.getElementById('lifetime-line').innerHTML =
    `Lifetime · <strong>${all.length}</strong> scanned · <strong>${allQ.length}</strong> qualified · <strong>${allApplied}</strong> applied · across ${plural(days, 'day')}`;
}

function renderToday() {
  const dates = state.jobs.map(j => dayOf(j.scored_date)).filter(Boolean).sort();
  const latest = dates[dates.length - 1];
  const dateEl = document.getElementById('today-date');
  dateEl.textContent = new Date().toLocaleDateString(undefined, { weekday: 'long', month: 'long', day: 'numeric' });
  if (latest && latest !== localDay()) dateEl.textContent += ` (last run ${latest})`;

  const runJobs = state.jobs.filter(j => dayOf(j.scored_date) === latest);
  const qualified = runJobs.filter(j => j.outcome === 'qualified').sort((a, b) => (b.score || 0) - (a.score || 0));
  const stepping = runJobs.filter(j => j.outcome === 'stepping-stone').sort((a, b) => (b.score || 0) - (a.score || 0));
  const shown = [...qualified.slice(0, 3), ...stepping.slice(0, 2)];
  const applied = runJobs.filter(j => statusOf(j.url) === 'applied').length;

  document.getElementById('today-counts').innerHTML = `
    <div class="tc"><span class="n">${runJobs.length}</span><span class="lbl">Scanned</span></div>
    <div class="tc disqualified"><span class="n">${runJobs.length - qualified.length - stepping.length}</span><span class="lbl">Dropped</span></div>
    <div class="tc qualified"><span class="n">${qualified.length}</span><span class="lbl">Qualified ${esc(state.floor)}+</span></div>
    <div class="tc applied"><span class="n">${applied}</span><span class="lbl">Applied</span></div>
    <div class="threshold-note">Matches need ${esc(state.floor)}+ against your resume; ${esc(state.star)}+ is a strong fit. Dropped means stale, off-fit, a dealbreaker, a repeat, or under the floor.</div>`;

  const cards = document.getElementById('today-cards');
  if (!shown.length) {
    cards.innerHTML = `<div class="quiet-day"><strong>Quiet day: no qualifying postings</strong>
      Scanned ${plural(runJobs.length, 'listing')}. None cleared the company-site, 7-day, and ${esc(state.floor)}-point bars.</div>`;
    return;
  }
  cards.innerHTML = shown.map((j, i) => {
    const isStep = j.outcome === 'stepping-stone';
    const href = safeUrl(j.url);
    return `<article class="today-card${i === 0 && !isStep ? ' top' : ''}">
      <div class="today-score ${(j.score || 0) >= state.star ? 'green' : 'yellow'}">${esc(j.score ?? '–')}</div>
      <div style="min-width:0">
        <div><strong>${esc(j.company)}</strong> · ${esc(j.title || '')}
          ${isStep ? '<span class="chip chip-yellow">Stepping stone</span>' : ''}
          ${j.network_override ? '<span class="chip chip-navy">Network override</span>' : ''}</div>
        <div class="today-meta">${esc(j.location || '—')} · posted ${esc(j.posted_date || 'unverified')}${j.date_source ? ` (${esc(j.date_source)})` : ''}</div>
        <div class="today-why">${esc(j.why_fits || '')}</div>
        ${materials(j)}
      </div>
      <div class="today-actions">
        ${href ? `<a class="btn" href="${esc(href)}" target="_blank" rel="noopener noreferrer">Apply on site →</a>` : ''}
        <div class="mark-row">${markButtons(j.url)}</div>
      </div>
    </article>`;
  }).join('');
}

function renderRunHistory() {
  const byDate = {};
  state.jobs.forEach(j => { const d = dayOf(j.scored_date); if (d) (byDate[d] = byDate[d] || []).push(j); });
  const dates = Object.keys(byDate).sort().reverse().slice(0, 30);
  document.getElementById('run-history').innerHTML = dates.map(d => {
    const jobs = byDate[d];
    const qualified = jobs.filter(j => j.outcome === 'qualified').sort((a, b) => (b.score || 0) - (a.score || 0));
    const stepping = jobs.filter(j => j.outcome === 'stepping-stone').sort((a, b) => (b.score || 0) - (a.score || 0));
    const surfaced = [...qualified, ...stepping];
    const applied = jobs.filter(j => statusOf(j.url) === 'applied').length;
    const top = qualified[0] || stepping[0];
    const date = parseDay(d);
    const stale = jobs.filter(j => j.outcome === 'stale').length;
    const offFit = jobs.filter(j => ['off-fit', 'dealbreaker'].includes(j.outcome)).length;
    const other = jobs.length - surfaced.length - stale - offFit;
    const rows = surfaced.map(j => {
      const s = statusOf(j.url);
      const statusChip = s ? `<span class="chip ${s === 'applied' ? 'chip-green' : s === 'saved' ? 'chip-yellow' : 'chip-grey'}">${esc(s)}</span>`
                           : '<span class="chip chip-navy">undecided</span>';
      return `<tr>
        <td class="score">${scoreChip(j)}${j.outcome === 'stepping-stone' ? ' <span class="chip chip-yellow">step</span>' : ''}</td>
        <td><strong>${esc(j.company)}</strong><div class="truncate">${jdLink(j, j.title || 'View posting')}</div></td>
        <td>${esc(j.location || '—')}</td>
        <td>${esc(j.posted_date || '—')}</td>
        <td style="min-width:220px">${esc(j.why_fits || '')}</td>
        <td>${statusChip}</td></tr>`;
    }).join('');
    return `<details class="run-row">
      <summary class="run-summary">
        <div class="run-date">${date ? date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' }) : esc(d)}<span class="weekday">${date ? date.toLocaleDateString(undefined, { weekday: 'short' }) : ''}</span></div>
        <div class="run-stat scanned"><strong>${jobs.length}</strong><span class="lbl">Scanned</span></div>
        <div class="run-stat"><strong>${jobs.length - surfaced.length}</strong><span class="lbl">Dropped</span></div>
        <div class="run-stat qualified"><strong>${qualified.length}${stepping.length ? `+${stepping.length}` : ''}</strong><span class="lbl">Qualified${stepping.length ? ' + steps' : ''}</span></div>
        <div class="run-stat applied"><strong>${applied}</strong><span class="lbl">Applied</span></div>
        <div class="run-top">${top ? `<strong>${esc(top.company)}</strong> · ${esc(top.score)}` : '<em>quiet day</em>'}</div>
      </summary>
      <div class="run-detail">
        ${surfaced.length ? table(['Score', 'Company / role', 'Location', 'Posted', 'Why it fits', 'Status'], rows) : ''}
        <div class="drops">Dropped: ${stale} stale · ${offFit} off-fit or dealbreaker · ${other} repeat or under the floor</div>
      </div>
    </details>`;
  }).join('');
}

const charts = {};
function renderCharts() {
  const ids = ['chart-volume', 'chart-geo', 'chart-skills'];
  if (typeof window.Chart !== 'function') {
    ids.forEach(id => {
      const canvas = document.getElementById(id);
      if (canvas) canvas.parentElement.innerHTML = '<p class="chart-note">Charts did not load. The tables on this page still work.</p>';
    });
    return;
  }
  const c = { ink: cssVar('--ink'), muted: cssVar('--muted'), line: cssVar('--line'), navy: cssVar('--navy'), yellow: cssVar('--yellow'), green: cssVar('--green') };
  Chart.defaults.color = c.muted;
  Chart.defaults.borderColor = c.line;
  Chart.defaults.font.family = cssVar('--font');

  const days = [];
  for (let i = 29; i >= 0; i--) { const d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() - i); days.push(localDay(d)); }
  const perDay = days.map(day => {
    const js = state.jobs.filter(j => dayOf(j.scored_date) === day);
    return [js.length, js.filter(j => j.outcome === 'qualified').length, js.filter(j => statusOf(j.url) === 'applied').length];
  });
  const line = (label, i, color) => ({ label, data: perDay.map(p => p[i]), borderColor: color, backgroundColor: color, borderWidth: 2, tension: 0.3, pointRadius: 0 });
  draw('chart-volume', {
    type: 'line',
    data: { labels: days.map(d => d.slice(5)), datasets: [line('Scanned', 0, c.muted), line('Qualified', 1, c.navy), line('Applied', 2, c.green)] },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom' } },
      scales: { y: { beginAtZero: true, ticks: { precision: 0 } }, x: { ticks: { maxRotation: 0, autoSkip: true } } } },
  });

  const recentQ = lastNDays(30).filter(j => j.outcome === 'qualified');
  const tally = (pairs) => Object.entries(pairs.reduce((acc, k) => (acc[k] = (acc[k] || 0) + 1, acc), {})).sort((a, b) => b[1] - a[1]);
  const bars = (entries, color) => ({
    type: 'bar',
    data: { labels: entries.map(e => e[0]), datasets: [{ data: entries.map(e => e[1]), backgroundColor: color }] },
    options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } },
      scales: { x: { beginAtZero: true, ticks: { precision: 0 } } } },
  });
  draw('chart-geo', bars(tally(recentQ.map(j => String(j.location_type || j.location || 'Unknown'))).slice(0, 8), c.navy));
  draw('chart-skills', bars(tally(recentQ.flatMap(j => (j.skills_mentioned || []).map(s => String(s).trim()).filter(Boolean))).slice(0, 10), c.yellow));
}
function draw(id, config) {
  if (charts[id]) charts[id].destroy();
  charts[id] = new Chart(document.getElementById(id), config);
}

function renderApplications() {
  const apps = state.applications;
  const metrics = document.getElementById('app-metrics');
  const wrap = document.getElementById('apps-table-wrap');
  if (!apps.length) {
    metrics.innerHTML = '';
    wrap.innerHTML = '<p class="empty" style="padding:18px">No applications yet. Mark a job Applied and the next run adds it here.</p>';
    return;
  }
  const count = list => apps.filter(a => list.includes(a.application_status)).length;
  const responded = apps.filter(a => a.last_email_at).length;
  metrics.innerHTML = `
    <div class="tile"><strong>${count(['submitted'])}</strong><span class="l">Submitted</span></div>
    <div class="tile acknowledged"><strong>${count(['acknowledged'])}</strong><span class="l">Acknowledged</span></div>
    <div class="tile in-progress"><strong>${count(IN_PROGRESS)}</strong><span class="l">In progress</span></div>
    <div class="tile rejected"><strong>${count(['rejected', 'ghosted', 'declined', 'withdrew'])}</strong><span class="l">Closed</span></div>
    <div class="tile offer"><strong>${count(['offer', 'accepted'])}</strong><span class="l">Offers</span></div>
    <div class="tile rate"><strong>${pct(responded, apps.length)}</strong><span class="l">Response rate</span></div>`;

  const bucket = a => (APP_STATUS[a.application_status] || { bucket: 'active' }).bucket; // unknown statuses count as active
  const shown = apps.filter(a => state.appsFilter === 'all' || bucket(a) === state.appsFilter)
    .sort((a, b) => String(b.last_email_at || b.applied_at || '').localeCompare(String(a.last_email_at || a.applied_at || '')));
  if (!shown.length) {
    wrap.innerHTML = '<p class="empty" style="padding:18px">Nothing in this view yet.</p>';
    return;
  }
  wrap.innerHTML = table(['Company / role', 'Applied', 'Status', 'Last email', 'Score', 'Links'], shown.map(a => {
    const meta = APP_STATUS[a.application_status] || { label: a.application_status || 'unknown', chip: 'chip-grey' };
    const age = daysAgo(a.applied_at);
    const thread = a.last_email_thread_id ? ` · <a href="https://mail.google.com/mail/u/0/#all/${encodeURIComponent(a.last_email_thread_id)}" target="_blank" rel="noopener noreferrer">open thread</a>` : '';
    return `<tr>
      <td><strong>${esc(a.company)}</strong><div class="sub">${esc(a.title || '')}</div></td>
      <td>${esc(dayOf(a.applied_at) || '—')}<div class="sub">${age === Infinity ? '' : age === 0 ? 'today' : plural(age, 'day') + ' ago'}</div></td>
      <td><span class="chip ${meta.chip}">${esc(meta.label)}</span></td>
      <td>${a.last_email_subject ? `<div class="truncate" title="${esc(a.last_email_subject)}">${esc(a.last_email_subject)}</div><div class="sub">${esc(a.last_email_at || '')}</div>` : '<span class="sub">—</span>'}${thread}</td>
      <td class="score">${esc(a.score_at_apply ?? '—')}</td>
      <td>${jdLink(a, 'JD')}${a.tailored_files ? `<div class="sub"><code>${esc(a.tailored_files)}</code></div>` : ''}</td>
    </tr>`;
  }).join(''));
}

function renderPipeline() {
  const pipeline = state.jobs
    .filter(j => j.outcome === 'qualified' && !['applied', 'skipped'].includes(statusOf(j.url)))
    .sort((a, b) => (b.score || 0) - (a.score || 0));
  const wrap = document.getElementById('pipeline-table-wrap');
  if (!pipeline.length) { wrap.innerHTML = '<p class="sub" style="padding:10px">No undecided jobs.</p>'; return; }
  wrap.innerHTML = table(['Score', 'Company / role', 'Location', 'Posted', 'Materials', 'Decision'], pipeline.map(j => `<tr>
    <td class="score">${scoreChip(j)}</td>
    <td><strong>${esc(j.company)}</strong><div class="truncate">${jdLink(j, j.title || 'View posting')}</div></td>
    <td>${esc(j.location || '—')}</td>
    <td>${esc(j.posted_date || '—')}</td>
    <td>${j.tailored_files ? `<code>${esc(j.tailored_files)}</code>` : '—'}</td>
    <td><div class="mark-row">${markButtons(j.url)}</div></td>
  </tr>`).join(''));
}

function renderLog() {
  const items = state.jobs
    .filter(j => statusOf(j.url) === state.tab)
    .sort((a, b) => (Date.parse(state.feedback[b.url].timestamp) || 0) - (Date.parse(state.feedback[a.url].timestamp) || 0));
  const wrap = document.getElementById('log-table-wrap');
  if (!items.length) { wrap.innerHTML = `<p class="sub" style="padding:10px">Nothing marked ${esc(MARKS[state.tab] || state.tab)} yet.</p>`; return; }
  wrap.innerHTML = table(['When', 'Company / role', 'Location', 'Score', 'Posting', ''], items.map(j => {
    const ts = Date.parse(state.feedback[j.url].timestamp);
    return `<tr>
      <td>${ts ? new Date(ts).toLocaleDateString() : '—'}</td>
      <td><strong>${esc(j.company)}</strong><div class="truncate">${esc(j.title || '')}</div></td>
      <td>${esc(j.location || '—')}</td>
      <td class="score">${esc(j.score ?? '—')}</td>
      <td>${jdLink(j, 'View JD')}</td>
      <td><button class="btn btn-small" data-mark="${esc(state.tab)}" data-url="${esc(j.url)}">Undo</button></td>
    </tr>`;
  }).join(''));
}

function markTabs() {
  document.querySelectorAll('[data-tab]').forEach(t => t.setAttribute('aria-pressed', String(t.dataset.tab === state.tab)));
  document.querySelectorAll('[data-apps-filter]').forEach(t => t.setAttribute('aria-pressed', String(t.dataset.appsFilter === state.appsFilter)));
}

async function copyText(text, button) {
  try {
    await navigator.clipboard.writeText(text);
    button.textContent = 'Copied';
  } catch {
    const sel = window.getSelection();
    const code = button.previousElementSibling;
    if (sel && code) { const r = document.createRange(); r.selectNodeContents(code); sel.removeAllRanges(); sel.addRange(r); }
    button.textContent = 'Press Ctrl+C';
  }
  setTimeout(() => { button.textContent = 'Copy path'; }, 1800);
}

// ---------- events ----------
document.addEventListener('click', e => {
  const mark = e.target.closest('[data-mark]');
  if (mark) { setStatus(mark.dataset.url, mark.dataset.mark); return; }
  const tab = e.target.closest('[data-tab]');
  if (tab) { state.tab = tab.dataset.tab; renderLog(); markTabs(); return; }
  const filter = e.target.closest('[data-apps-filter]');
  if (filter) { state.appsFilter = filter.dataset.appsFilter; renderApplications(); markTabs(); return; }
  const copy = e.target.closest('[data-copy]');
  if (copy) copyText(copy.dataset.copy, copy);
});
// Redraw charts when the viewer's theme changes, so axis and bar colors follow it.
const redrawCharts = () => { if (state.jobs.length) renderCharts(); };
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', redrawCharts);
new MutationObserver(redrawCharts).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });

// ---------- boot ----------
(function boot() {
  try {
    const baked = JSON.parse(document.getElementById('baked-data').textContent || '{}');
    state.jobs = Array.isArray(baked.jobs) ? baked.jobs : [];
    state.applications = Array.isArray(baked.applications) ? baked.applications : [];
    state.floor = Number(baked.floor) || 75;
    state.star = Number(baked.star) || 85;
    state.generatedAt = baked.generated_at || null;
    mergeMarks(baked.feedback);
  } catch (e) {
    const err = document.getElementById('err-state');
    err.hidden = false;
    err.textContent = 'The dashboard data block is unreadable. Ask Claude to re-run bake.py and republish the dashboard.';
  }
  mergeMarks(localMarks);
  const stamp = state.generatedAt ? new Date(state.generatedAt).toLocaleString() : 'not yet';
  document.getElementById('status-text').textContent = `${plural(state.jobs.length, 'job')} in the ledger · updated ${stamp}`;
  renderAll();
  connectDb();
})();
</script>
````
<!-- /appendix -->

## Appendix H — `workshop/deep_tailor.md`

<!-- appendix: workbook_deep_tailor.md -->
````markdown
# Deep-Tailor Workbook

Setup gets your Job Bot running on sensible defaults. This workbook calibrates it to you in about 30 minutes. Do all eight sections at once or spread them across the week; the next run picks up each change.

**How to use it:** for each section, fill in the brackets and paste the block into a chat in the Claude desktop app with your `Job Bot` folder connected. Claude writes the change to the right file.

**Short on time?** Do them in this order: 8 (project ledger, the biggest scoring lift), 3 (network contacts), 1 (anti-keywords, cuts noise right away), 4 (cover-letter voice). The rest can wait.

---

## Section 1 — Anti-keywords (5 min)

Postings that contain these words drop before scoring, whatever their score. Think clearance requirements you don't hold, industries you'd skip, or titles you're done with.

> Add these anti-keywords to my Job Bot's preferences.md, keeping the ones already there:
>
> - [e.g. "Active Top Secret clearance"]
> - [e.g. "Sales Development Representative"]
> - [e.g. "10+ years"]
> - [e.g. "Recruitment agency"]

---

## Section 2 — Compensation floor (2 min)

Roles that publish a range below your floor drop. Roles without a published range still go through.

> Set the compensation floor in my Job Bot's preferences.md to $[number] base salary. Drop a posting only when it publishes a range and the bottom of that range is below that number.

---

## Section 3 — Network contacts (10 min)

The highest-leverage tuning. A named contact earns full network points (10 of 100) on every role at that company, which pushes borderline roles over the line.

> Add these to the Network contacts section of my Job Bot's preferences.md:
>
> - [Company] — [Person] — [Relationship]
> - [e.g. Slalom — Jordan Lee — Daniels MBA classmate, Class of 2026]
> - [e.g. Deloitte — Anyone — 12 DU alumni at the firm on LinkedIn]
>
> "Anyone" means an alumni or school connection without a specific person yet.

---

## Section 4 — Cover-letter voice (5 min)

The default is tight and active. Tune it to sound like you.

> Update the style rules in my Job Bot's master/cover_letter_template.md:
>
> - Tone: [Confident / Conversational / Warm-formal / Sharp / Academic]
> - Opener: [Lead with the angle / Lead with an accomplishment / Lead with why this firm]
> - First person: [Heavy "I" / Balanced / Minimal "I"]
> - Hedging: [None / Some on speculative claims]
> - Words to avoid, on top of the current list: [your list]
>
> Then draft one sample letter in that voice for a [target role title] role so I can check it.

---

## Section 5 — Scoring weights (3 min)

Defaults: role keywords 35, experience 20, location 15, domain 10, skills 10, network 10. Career switchers often down-weight experience; relocators down-weight location.

> Change the scoring weights in my Job Bot's preferences.md to (total 100):
>
> - Role keyword overlap: [number]
> - Experience fit: [number]
> - Location fit: [number]
> - Domain fit: [number]
> - Skill overlap: [number]
> - Network: [number]
>
> Keep the surface and star thresholds as they are.

---

## Section 6 — Industries to exclude (2 min)

Drops roles by the company's industry rather than the posting's wording.

> Add these to Industries to exclude in my Job Bot's preferences.md, and check each company's primary industry before scoring:
>
> - [e.g. Gambling]
> - [e.g. Tobacco]
> - [e.g. Staffing agencies]

---

## Section 7 — Stepping-stone companies (3 min)

At these companies, roles scoring 65 or more but under your threshold still show up, with a yellow badge. Use it for firms where you'd take a junior role to get in the door.

> Add these to the Stepping-stone tier in my Job Bot's preferences.md:
>
> - [e.g. McKinsey]
> - [e.g. Anthropic]
> - [Your dream firm]

---

## Section 8 — Project ledger (10 min)

Runs use these projects for the Selected Projects section of each tailored resume and the cover letter's bridge paragraph.

> Replace the template entries in my Job Bot's master/projects.md with these:
>
> ### [Project name]
> - Dates: [Start – End, or Ongoing]
> - Role: [Your role]
> - Built: [1–2 sentences]
> - Why it matters: [1 sentence, with a number]
> - Tech: [tools, methods]
> - fits: [role types, e.g. AI consulting, finance transformation, supply chain]
> - Verify before use: [numbers to confirm]
>
> [Repeat for 3–6 projects across professional, academic, and personal work.]

---

## When you're done

Tell Claude: "Re-run my Job Bot now with the updated settings." The run re-scores against the new weights and contacts and refreshes the dashboard.
````
<!-- /appendix -->
