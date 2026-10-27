# Daily Job Brief

You're running the daily job search for the person described in `config/preferences.md`. The goal is a short list they'll act on: up to 3 roles posted in the last 7 days on the employer's own site, each scored against their resume and paired with a tailored one-page resume and a cover letter. A thin day produces a short list; never fill it with weaker roles.

Everything lives in the `Job Bot` folder attached to this task. Work from that folder; paths below are relative to it. If the folder is on the user's computer, build and check documents wherever you have python-docx and LibreOffice, then save the results back into the folder. The run is unattended: make reasonable calls, note them in the summary, and finish.

## 1. Load context

Read these files:

- `config/preferences.md`: thresholds, targets, keywords, title synonyms, geography, dealbreakers, stepping-stone companies, network contacts, and the dashboard URL.
- `master/resume_master.md`: the only source of facts for tailored materials.
- `master/projects.md`: projects to draw on, picked by their `fits:` tags.
- `master/cover_letter_template.md`: cover letter structure and style rules.
- `briefs/feedback.json` and `applications/applications.jsonl`.

If the master resume is missing, stop and say so in the summary.

The ledger, `briefs/all_jobs.jsonl`, grows every run, so don't read it whole. Print the last 14 days of it for repeat checks:

```bash
python3 - <<'PY'
import datetime, json
cutoff = (datetime.date.today() - datetime.timedelta(days=14)).isoformat()
with open('briefs/all_jobs.jsonl', encoding='utf-8-sig') as f:
    for line in f:
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if isinstance(row, dict) and str(row.get('scored_date') or '')[:10] >= cutoff:
            print(str(row.get('scored_date'))[:10], row.get('outcome'), row.get('url'))
PY
```

## 2. Sync the dashboard marks

The dashboard stores the user's Applied, Save, and Skip clicks in its own database: a `feedback` collection with one document per job (`url`, `status`, `timestamp`, `day`). Read that collection from the dashboard artifact and merge it into `briefs/feedback.json`, keyed by URL, keeping whichever mark has the newer timestamp. A `status` of `null` means the user cleared the mark. If the dashboard's data isn't reachable, continue with feedback.json as it is.

Then add an application row (schema in §7) for every job marked `applied` that isn't in `applications/applications.jsonl` yet. Use the mark's `day` as `applied_at`; it's the user's local date. For a mark without one, convert its `timestamp` to the user's time zone.

## 3. What qualifies

- **Employer source.** The apply link is the company's own careers page or its hosted applicant tracking system: Workday (`*.myworkdayjobs.com`, `*.myworkdaysite.com`), Greenhouse, Lever, Ashby, iCIMS, BambooHR, Workable, or SmartRecruiters. Job boards, aggregators, and staffing firms (LinkedIn, Indeed, Glassdoor, ZipRecruiter, Built In) can point you to a posting; resolve it to the employer's URL or drop it.
- **Posted within 7 calendar days.** Find the date in this order: the posting's date in its applicant tracking system's job feed (§4), JSON-LD `datePosted` in the page source, visible "Posted X days ago" text, an `og:updated_time`-style meta tag, or the company's job index listing the role as new. For the index case, record `posted_date` as `"active YYYY-MM-DD"` and `date_source` as `"index"`. A posting with no verifiable date doesn't qualify.
- **Still open.** Drop pages that say the job was removed, expired, or closed, or is no longer accepting applications. Quote the page's wording in `drop_reason`.
- **Within the user's rules.** Geography, anti-keywords, dealbreakers, excluded industries, and the compensation floor from preferences.md. Apply the compensation floor only when the posting publishes a range.

## 4. Search

Budget: about 30 searches, 25 page fetches, and 12 minutes per run.

**Named targets first.** For each company in preferences.md:

1. Use its `verified:` careers URL if one is recorded. Otherwise find the careers site, trying `careers.<brand>.com`, `<brand>.com/careers`, `boards.greenhouse.io/<brand>`, `job-boards.greenhouse.io/<brand>`, `jobs.lever.co/<brand>`, `jobs.ashbyhq.com/<brand>`, `<brand>.wd1.myworkdayjobs.com`, `careers-<brand>.icims.com`, `<brand>.bamboohr.com/careers`, and `apply.workable.com/<brand>`. Record the hit in preferences.md as `verified: <url>` so later runs skip the lookup.
2. If the company hires through Greenhouse, Lever, or Ashby, fetch its public job feed instead of searching. One fetch lists every open role with a date:
   - Greenhouse: `https://boards-api.greenhouse.io/v1/boards/<board>/jobs`, dated by `first_published` when the feed has it, otherwise `updated_at`.
   - Lever: `https://api.lever.co/v0/postings/<company>?mode=json`, dated by `createdAt` (milliseconds since 1970).
   - Ashby: `https://api.ashbyhq.com/posting-api/job-board/<board>`, dated by `publishedAt`.
   
   Record `date_source` as `"feed"`. For other sites, search the careers site for the role keywords plus the user's location or "remote", and run the same search for any `also_search_as:` names.
3. Fetch each candidate posting for its title, location, and full description, confirm the date, then apply §3.

When the list is longer than one run's budget, start with stepping-stone and network companies, then rotate through the rest so every company gets checked every few days. Record the companies you searched in today's `seen_jobs.json`, and use the last few days of those files to pick up where the rotation left off.

**Widening.** If fewer than 3 roles from named targets qualify, search discovery boards (Built In and its regional sites, such as builtincolorado.com) for the role keywords. Resolve each hit to the employer's own posting within 2 lookups or drop it. Widened roles meet the same threshold and rules.

## 5. Score

Score each surviving posting from 0 to 100 using the rubric and thresholds in preferences.md. The defaults: role keyword overlap 35 (title synonyms count), experience fit 20, location fit 15, domain fit 10, skill overlap 10, network 10.

Give every posting you examine one outcome:

- `qualified`: at or above the surface threshold. A posting at a company where the user has a named network contact (full network points) also qualifies from 65 up, with `network_override: true`.
- `stepping-stone`: at a stepping-stone company, 65 or more but under the threshold.
- `below-floor`: scored, but under the threshold.
- `off-fit`: not one of the target roles, outside the user's geography, or caught by an anti-keyword or an excluded industry.
- `dealbreaker`: hits a dealbreaker or the compensation floor.
- `stale`: older than 7 days, undated, or closed.
- `dedup`: already in the ledger within the last 14 days, or already marked `skipped` or `applied`. When the user asks for a re-run after changing their preferences, re-score postings from the last 7 days that are still open instead of marking them `dedup`.

Surface the top 3 qualified roles plus up to 2 stepping stones. When feedback shows 3 or more skips that share a title pattern or company, point it out in the summary and suggest an anti-keyword.

## 6. Materials

For each surfaced role, write these files into `daily/YYYY-MM-DD/` (today's date). Name them with a slug of company and role in lowercase with hyphens, such as `slalom_senior-consultant`:

- `<slug>_jd.txt`: the full posting text, its URL, and the verified posting date.
- `<slug>_score.md`: the score, line by line.
- `<slug>_cover_letter.docx`: 250 words or fewer, following `master/cover_letter_template.md`, signed with the user's name and the contact line from preferences.md.
- `<slug>_resume.docx`: the tailored resume.

**Tailoring.** Start from `master/resume_master.md`. Reorder and rephrase to match the posting's priorities, use its keywords where the resume supports them, and pick 1–3 projects from `projects.md` by their `fits:` tags. Skip projects tagged `exclude_from_outputs: true` or with TBD details. Every fact, number, title, and credential comes from the master resume or the project ledger, because the resume goes out under the user's name. When you use a claim a project lists under "Verify before use", name it in the summary so the user confirms it before sending.

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

**Ledger.** Append one row per posting examined today, surfaced or dropped, to `briefs/all_jobs.jsonl`. Each row is a single line of JSON (Python's `json.dumps(row)` writes one); add lines and never rewrite earlier ones.

```json
{"url": "https://careers.example.com/jobs/123", "company": "Example Co", "title": "Senior Consultant", "location": "Denver, CO", "location_type": "Hybrid Denver", "posted_date": "2026-10-26", "date_source": "json-ld", "scored_date": "2026-10-27", "score": 87, "score_breakdown": {"role": 33, "experience": 17, "location": 15, "domain": 10, "skill": 7, "network": 5}, "outcome": "qualified", "drop_reason": null, "stepping_stone": false, "network_override": false, "why_fits": "Two sentences on the fit.", "skills_mentioned": ["SQL", "FP&A"], "comp_low": 130000, "comp_high": 165000, "tailored_files": "daily/2026-10-27/", "resume_file": "example-co_senior-consultant_resume.docx", "cover_letter_file": "example-co_senior-consultant_cover_letter.docx"}
```

- `outcome`: `qualified`, `stepping-stone`, `below-floor`, `off-fit`, `dealbreaker`, `stale`, or `dedup` (defined in §5).
- `date_source`: `feed`, `json-ld`, `text`, `og`, `index`, or `null`.
- `location_type`: `<City>`, `Remote-US`, `Hybrid <City>`, `Relocation: <City>`, or `Unknown`.
- `skills_mentioned` is a list of strings.
- The materials fields (`tailored_files`, `resume_file`, `cover_letter_file`) apply to surfaced roles only.

**Seen list.** Write `daily/YYYY-MM-DD/seen_jobs.json` with every URL examined and the companies searched today.

**Applications.** `applications/applications.jsonl` holds one JSON line per application:

```json
{"company": "Example Co", "title": "Senior Consultant", "url": "https://careers.example.com/jobs/123", "applied_at": "2026-10-28", "application_status": "submitted", "status_history": [{"status": "submitted", "at": "2026-10-28"}], "score_at_apply": 87, "tailored_files": "daily/2026-10-27/", "last_email_at": null, "last_email_subject": null, "last_email_thread_id": null}
```

Statuses: `submitted`, `acknowledged`, `screening`, `assessment`, `interview`, `offer`, `accepted`, `declined`, `rejected`, `ghosted`, `withdrew`. To change a row, rewrite the file with that row updated.

## 8. Email check (when Gmail is connected)

For each application that is submitted, acknowledged, screening, assessment, interview, or ghosted, search the last 90 days of Gmail for mail from the company's domain or an applicant-tracking sender (myworkday.com, greenhouse.io, lever.co, icims.com, ashbyhq.com), or with the company or role in the subject. Applicant-tracking senders mail for many employers, so count a message only when its sender domain, subject, or body names this company or this role. Read the newest message that does and set the status:

- `rejected`: "not moving forward", "other candidates", "decided not to proceed", "position has been filled".
- `acknowledged`: "received your application", "thank you for applying".
- `screening` or `interview`: a request to schedule a call or interview, a calendar invite, "next steps".
- `assessment`: a test, case, or take-home assignment.
- `offer`: an offer or offer letter.

Append each change to `status_history` and update the `last_email_*` fields. Mark an application `ghosted` after 30 days with no reply since `applied_at`; a later matching email moves it to that email's status. This step only reads mail. It never sends, labels, archives, or deletes anything.

## 9. Refresh the dashboard

1. Run `python3 dashboard/bake.py`. It rebuilds `dashboard/dashboard.html` from the files above and exits with an error if the page is incomplete or missing its data block.
2. Confirm the page's data block now includes today's `scored_date`.
3. Update the dashboard artifact at the URL in preferences.md: read it, then publish `dashboard/dashboard.html` to that same URL and leave its capabilities as they are. If the update fails, report it in the summary instead of publishing a new dashboard.
4. Save a copy of the baked page as `daily/YYYY-MM-DD/brief.html`, the day's permanent record.

## 10. Summary

End with one short paragraph: roles surfaced (top company and score), postings examined, how many dropped for freshness versus fit, and anything that needs the user, such as a blocked careers site, a skip pattern, a claim to verify, or a missing resume. Close with "Materials: `Job Bot/daily/YYYY-MM-DD/`" and the dashboard link.

## When things go wrong

- A careers site blocks fetching: try its job feed or job index. If those fail too, skip the company today and list it in the summary.
- Searches get rate-limited: spend what's left on stepping-stone and network companies.
- Nothing qualifies: update the ledger and dashboard anyway and call it a quiet day. Keep the threshold where the user set it.
