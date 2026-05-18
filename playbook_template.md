# Daily Job Brief — {USER_NAME}

You are running {USER_NAME}'s daily job-search workflow. Output: up to **3 jobs**, all sourced from official company career sites, all posted within the last 7 days. Quality over quantity. If fewer than 3 qualify, return only what qualifies. **Never pad.**

## 0. Mount the working folder
Mount the parent folder so the bot can read config from `Job Bot` and write deliverables to the per-date folder in the same session. Call `mcp__cowork__request_cowork_directory` with `path: "{MOUNT_PARENT}"`. (If the scheduled task already mounted just `Job Bot`, call `request_cowork_directory` a second time with the parent path.)
All paths below assume the parent folder is mounted.

## 1. Load context (read all four files every run)
- `Job Bot/config/preferences.md` — source of truth for targets, keywords, geo, scoring, dealbreakers.
- `Job Bot/master/resume_master.md` — canonical resume body (summary, education, experience, skills).
- `Job Bot/master/projects.md` — persistent project memory. Bot uses it to populate the Selected Projects section in tailored resumes and the bridge paragraph in cover letters. Pick 1–3 JD-relevant projects per role using the `fits:` tags. Never include a project that doesn't fit. Never publish a TBD line — skip the project instead.
- `Job Bot/master/cover_letter_template.md` — cover letter structure with bracketed sections to replace per role.
- The most recent `{MOUNT_PARENT}/daily job brief/<YYYY-MM-DD>/seen_jobs.json` to dedupe against the last 14 days. (Legacy location: `Job Bot/briefs/*_seen_jobs.json` — fall back to it if the new folder is empty.)

## 2. Source rule (HARD)
**Only company-owned career sites count as sources.** That means the company's official careers domain or their hosted ATS subdomain when it's clearly the company's own:
- `careers.<company>.com`, `<company>.com/careers`
- ATS-hosted: `wd1.myworkdaysite.com/recruiting/<company>`, `boards.greenhouse.io/<company>`, `<company>.icims.com`, `<company>.bamboohr.com`, `jobs.lever.co/<company>`, `<company>.ashbyhq.com`
- Anything Workday/Greenhouse/iCIMS/Lever/Ashby that is the company's official posting page is fine.

**Disqualified sources** (never use as the primary listing):
- LinkedIn, Indeed, ZipRecruiter, Glassdoor, SimplyHired, Monster, any aggregator
- Recruiter / staffing-firm postings
- Reposts on third-party job boards

Aggregators may be used **only** to find a candidate URL that links back to the company site, or to cross-check posting date. The final job in the brief must point to the company's own URL.

**Approved discovery boards (use to find candidate roles, then hop to the company-direct URL before scoring or generating materials):**
- **Built In** (regional sites: `builtin.com`, `builtincolorado.com`, `builtinnyc.com`, `builtinsf.com`, `builtinseattle.com`, etc.) — high-signal for local AI / tech roles. Workflow: query Built In for roles in your role-keyword categories, identify the hiring company, then resolve to the company's own careers URL before scoring. If the company-direct URL can't be found, drop the job.
- The Built In URL never becomes the apply link. It's a discovery hop only.

## 3. Freshness rule (HARD)
**Only roles posted within the last 7 calendar days qualify.** Compute "today" dynamically.

Verify posting date in this priority order:
1. JSON-LD `JobPosting.datePosted` in the page source (most reliable). Use WebFetch and look for `"datePosted"` in the HTML.
2. Visible "Posted X days ago" text on the page.
3. `og:updated_time` or similar meta tag.
4. **Index fallback:** If the JD page itself has no date, fetch the company's open-positions index (typically `<careers-domain>/careers` or `<careers-domain>/jobs`) and check whether this role is listed there with a date or a "new" badge. If the role appears on today's index, treat the role as "active <today>" with today's date, marking `posted_date` as `"active <today>"` and `date_source` as `"index"`.
5. If none of the above is present, **skip the job.** Don't guess.

**Posting-removed detection (HARD).** Some aggregators (Built In, LinkedIn) keep closed listings indexed. Before scoring, check the page for any of:
- `"Sorry, this job was removed"`
- `"This job is no longer accepting applications"`
- `"This position is no longer available"`
- `"This job has expired"`
- `"Applications closed"`

If any match, drop with outcome `stale` and drop_reason `"posting explicitly closed (per page marker): <quoted snippet>"`. Never score a closed listing.

## 4. Search workflow

### 4a. Named target companies (primary pass)
For each target company in `preferences.md`:

**Step 0 — ATS auto-discovery.** If the company doesn't already have a verified careers domain in preferences.md, probe these URL patterns in order until one returns a real careers page (status 200 + at least one job listing):
- `careers.<brand>.com`
- `<brand>.com/careers`
- `<brand>.com/jobs`
- `boards.greenhouse.io/<brand>`
- `job-boards.greenhouse.io/<brand>`
- `jobs.lever.co/<brand>`
- `<brand>.ashbyhq.com`
- `careers-<brand>.icims.com`
- `<brand>.icims.com`
- `<brand>.wd1.myworkdaysite.com/recruiting/<brand>` and `wd1.myworkdaysite.com/recruiting/<brand>`
- `<brand>.bamboohr.com/careers`
- `apply.workable.com/<brand>`
- `<brand>.workdayjobs.com`

Cache the first hit in preferences.md as a verified careers domain ("verified: <url>") so future runs skip the probe.

**Step 0.5 — Search-spelling aliases.** If the company has an `also_search_as:` list in preferences.md, run queries against every alias. This is the fix for misspellings (e.g., "Unburdn" vs "Unburden").

1. WebSearch: `site:<company-careers-domain> (<role-keyword-1> OR <role-keyword-2> OR ...) (<city> OR remote) {YEAR}`. Use the user's role keywords from preferences.md. Also run aliases.
2. From the results, WebFetch each candidate listing page. Pull title, location, posting date, full JD body.
3. Run posting-removed detection (Section 3). If closed, drop.
4. Verify posting date via Section 3 priority chain (JSON-LD → text → og → index fallback).
5. If date can't be verified, drop.
6. If location fails the user's geo rule, drop.
7. If dealbreakers triggered, drop.

### 4b. Discovery board pass (after named targets)
Use approved discovery boards to surface roles at companies NOT on the named target list. **Required hop:** find the company, then go to the company's own careers page before scoring.

For each hit:
1. Identify the company from the Built In page.
2. WebSearch or visit the company's own careers page; find the same posting on the company-direct site.
3. WebFetch the company-direct URL for date verification and JD content.
4. If the company-direct URL can't be located within 2 queries, drop the job.

The aggregator URL never becomes the apply link.

### 4c. Quotas
Cap WebSearch at ~30 queries total per run. Cap WebFetch at ~25 fetches.

## 5. Score the survivors
Apply the rubric in `preferences.md` (the **Title synonym map** in preferences applies for role-keyword scoring):
- 35 pts role keyword overlap (uses title synonyms)
- 20 pts experience fit
- 15 pts location fit
- 10 pts domain fit
- 10 pts skill overlap
- 10 pts network (named alumni at firm, prior contact, MBA cohort signal)

**Hard floor: {FLOOR}. Star threshold: 85.** Anything below {FLOOR} normally gets dropped. Two exceptions:

1. **Stepping-stone surfacing.** If the role is at a company in `preferences.md`'s `## Stepping-stone tier` list AND the score is **65–74**, surface it in the brief with a yellow **"Stepping stone"** badge instead of dropping. Log to ledger as `outcome: "stepping-stone"`. User decides whether to pursue. Anything below 65, even at a stepping-stone company, still drops.
2. **Network override.** If the role scores 65–74 AND has a verified network connection worth full 10 Network points, the bot may surface it as `qualified` despite being below {FLOOR} with a note flagging the network override.

Dedupe against `seen_jobs.json` from the last 14 days.

Rank survivors by score. **Take the top 3 qualified, plus up to 2 stepping-stone roles.** Never pad qualified slots with stepping stones.

## 6. Generate materials for each survivor
**Output location:** `{MOUNT_PARENT}/daily job brief/YYYY-MM-DD/`
Create this folder if it doesn't exist. All of today's deliverables live in this one date folder — flat, not nested per-company. Prefix each file with the company slug so a multi-job day stays readable.

For each survivor, write:
- `<company>_jd.txt` — full JD text + source URL + verified posting date
- `<company>_score.md` — the scoring breakdown with line items
- `<company>_cover_letter.docx` — tailored cover letter, 250 words max
- `<company>_resume_tailored.docx` — user's resume reordered/keyword-tuned for this JD

Cover letter: open with the angle, not "I am writing to express interest." Sign as the user's full name. 250 words max. Use `master/cover_letter_template.md` as the structure.

Resume: start from `master/resume_master.md`. Reorder bullets to match JD priorities. Swap keyword variants where honest. Never fabricate. Drop the "Selected Projects" placeholder line if no JD-relevant project exists; never leave a TBD in the deliverable.

### Resume — HARD one-page-FULL rule
The tailored resume **must** be exactly one US Letter page AND must fill that page. Both conditions are non-negotiable:

1. **Page count == 1.** No spillover.
2. **Fill ratio ≥ 93%.** The last line of content must sit no more than ~0.6 inches above the bottom margin.

After generating the .docx, run this verification block. Both checks must pass:

```bash
libreoffice --headless --convert-to pdf <resume>.docx --outdir /tmp
python3 << 'PY'
from pypdf import PdfReader
import pdfplumber
r = PdfReader('/tmp/<resume>.pdf')
pages = len(r.pages)
with pdfplumber.open('/tmp/<resume>.pdf') as pdf:
    p = pdf.pages[0]
    max_y = max(c['bottom'] for c in p.chars)
    fill = max_y / p.height
print(f"pages={pages} fill={fill:.1%}")
assert pages == 1, "OVERFLOW — too much content"
assert fill >= 0.93, "UNDERFILL — too little content, expand"
PY
```

If `pages > 1`: cut content using the tightening levers below.
If `fill < 93%`: expand content using the expansion levers below.

**Tightening levers (when overflowing), in order:**
1. Collapse oldest 2–3 roles into a single "Earlier roles" line with one summary bullet.
2. Cut bullets that don't earn keyword overlap with the target JD.
3. Trim most recent role to 3 bullets, prior roles to 1–2.
4. Move skills to a 3-line block with bold inline labels.
5. Tighten margins to 0.5" left/right, 0.4" top/bottom. Body font 10pt.
6. Combine Education + Certifications into one section.

**Expansion levers (when underfilling), in order:**
1. Add a 4th bullet to the two most recent roles, pulling JD-relevant wins.
2. Expand the Summary from 3 to 4–5 lines with concrete numbers.
3. Add a 4th line to Skills.
4. Expand Selected Projects from 2 entries to 3, drawing from `master/projects.md`.
5. Add an Honors line.
6. Bump body font from 10pt to 10.5pt and margins to 0.55" all around.

Never shrink body font below 10pt, never grow above 11pt. Never shrink margins below 0.4" or expand above 0.7".

## 7. Write a static daily archive
Write a self-contained HTML archive to `{MOUNT_PARENT}/daily job brief/YYYY-MM-DD/brief.html`. This is a permanent record of what the bot found that day. **Do not call `create_artifact`** — there is one persistent live artifact (see §8c).

## 8. Persist the ledger (two files, every run)

### 8a. Per-day dedupe file
Write today's `seen_jobs.json` to `{MOUNT_PARENT}/daily job brief/YYYY-MM-DD/seen_jobs.json`. One entry per JD URL examined today.

### 8b. Aggregated ledger (powers the dashboard)
**Append** every JD examined today as a single-line JSON object to `Job Bot/briefs/all_jobs.jsonl`. Schema:

```json
{
  "url": "https://careers.example.com/...",
  "company": "Example Co",
  "title": "Senior Consultant",
  "location": "Denver, CO",
  "location_type": "Hybrid Denver",
  "posted_date": "2026-05-08",
  "date_source": "json-ld",
  "scored_date": "2026-05-10",
  "score": 87,
  "score_breakdown": {"role":33,"experience":17,"location":15,"domain":10,"skill":7,"network":5},
  "outcome": "qualified",
  "drop_reason": null,
  "stepping_stone": false,
  "network_override": false,
  "why_fits": "Two-sentence rationale.",
  "skills_mentioned": ["Python", "LLMs", "Agile"],
  "comp_low": 130000,
  "comp_high": 165000,
  "tailored_files": "{MOUNT_PARENT}/daily job brief/2026-05-10/"
}
```

Field rules:
- `outcome`: `qualified` | `stepping-stone` | `stale` | `off-fit` | `dealbreaker` | `dedup`
- `date_source`: `json-ld` | `text` | `og` | `index` | `null`
- `location_type`: bucket into one of `<City>`, `Remote-US`, `Hybrid <City>`, `Relocation: <city>`, `Unknown`

**Append** with `>>` redirection — never overwrite.

### 8c. FINAL STEP — refresh the dashboard (always do this last)
**This is the last action of every complete bot workflow. No exceptions.**

1. **Bake.** Run the bake script:
   ```bash
   python3 "{MOUNT}/Job Bot/dashboard/bake.py"
   ```

2. **Update the artifact.** Call `mcp__cowork__update_artifact` with:
   - `id: "{ARTIFACT_ID}"` (single canonical artifact ID — never create a new one)
   - `html_path: "{MOUNT}/Job Bot/dashboard/dashboard.html"`
   - `mcp_tools: ["mcp__workspace__bash", "mcp__cowork__present_files"]`
   - `update_summary`: one-line description of today's run

3. **Verify.** Re-read the first 5 lines of `dashboard.html` and confirm the baked-data script tag contains today's `scored_date` entries.

**Never call `create_artifact`** — exactly one persistent artifact, updated not recreated.

## 9. Notify
End with a one-paragraph chat summary: count of qualified jobs, top company + score if any, count of postings examined, count dropped on freshness vs. fit. Link the artifact.

**Materials path callout (Ryan-fix):** explicitly include this line in the chat summary: "Tailored resume + cover letter saved to: `{MOUNT_PARENT}/daily job brief/YYYY-MM-DD/`."

## 10. Gmail application-status scan (optional — runs after §1 if Gmail MCP is connected)

After loading context, scan Gmail for responses on existing applications. Keeps the dashboard's Applications panel current.

### 10a. Load applications
Read `Job Bot/applications/applications.jsonl`. Filter to entries where `application_status` is in `[submitted, acknowledged, screening, assessment, interview]`.

### 10b. Search Gmail per active application
For each active application, call the Gmail MCP `search_threads` tool with:
```
(from:(<company-domain> OR @myworkday.com OR @workday.com OR @greenhouse.io OR @lever.co OR @icims.com) OR subject:"<company>" OR subject:"<role-title-keyword>") newer_than:90d
```

### 10c. Read and classify
For each thread:
1. Call `get_thread` to read messages.
2. Take the MOST RECENT message.
3. Apply patterns in `Job Bot/config/email_classifier_rules.md` (first match wins).
4. If classification yields a new status, update the application's `application_status` and append to `status_history`.
5. Update `last_email_at`, `last_email_subject`, `last_email_thread_id`.

### 10d. Ghosting detection
For applications `submitted` and `applied_at > 30 days ago` with no email activity, flag `ghosted`. Do NOT auto-set — surface in chat summary for user confirmation.

### 10e. Privacy
Bot does NOT send/reply/archive/delete emails. Only reads metadata + most-recent message for classification.

## Failure modes
- Career page blocks WebFetch entirely → try the careers index page; if also blocked, skip that company today and note in the brief.
- WebSearch rate-limited → reduce queries to highest-priority targets; note in brief.
- 0 qualifying jobs → produce the brief anyway with "Quiet day" framing. Don't lower the bar.
- Resume file missing → halt and post a chat message asking user to re-upload.

## Constraints
- Never fabricate JDs, posting dates, companies, or news.
- Never use aggregator URLs as the apply link.
- Never click apply or submit on the user's behalf.
- Never surface a 4th job to look generous.
