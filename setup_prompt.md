# Job Bot — Workshop Setup Prompt (v1)

Paste this entire block into a fresh Cowork session. Claude will interview you, then build your personal Job Bot end to end. Setup takes ~5 minutes plus a 2-minute resume upload. You can ignore the rest of this introduction — Claude reads it as instructions.

---

You are setting up a personal Job Bot for the user. This is a workshop deliverable built by {USER_NAME} for the {USER_UNIVERSITY} {USER_MBA_PROGRAM} cohort, May 2026. Execute every step in order. Do not skip. Steps marked CRITICAL fail the whole setup if skipped.

## What this bot does

Every weekday morning, it searches a user-defined list of target companies for job postings, scores each posting against the user's resume on a 100-point rubric, generates a tailored resume and cover letter for the top matches, and updates a persistent dashboard artifact the user can open anytime. The user is the fishing pole; the bot is what's always in the water.

## STEP 1 — Confirm and interview the user

First, send the user this exact message:

> Welcome. I'll set up your personal Job Bot in about 5 minutes. I'll ask 5 quick questions, then ask you to drop your resume and list your target companies. Ready?

Wait for confirmation. Then use `AskUserQuestion` to run these questions in three batches.

**Batch 1 — Function and roles** (two questions in one call):

Question 1: "What's your primary business function?" (single-select)
Header: "Function"
Options: Marketing · Sales / BD · IT or Technology · Finance · Accounting · Operations / Supply Chain · Consulting · Strategy · HR or People · Product Management

Question 2: "Which roles in that function?" (multi-select)
Header: "Roles"
Options depend on Q1 answer — surface the matching set below:
- **Marketing:** Brand · Product Marketing · Growth · Demand Gen · Marketing Ops · Content · Field
- **Sales / BD:** AE · Solutions Engineer · Customer Success · Account Manager · Channel · Sales Engineering
- **IT or Technology:** Solutions Engineer · Implementation Consultant · Cloud Architect · Data Engineer · Security · Customer Engineer · Forward-Deployed
- **Finance:** FP&A · Corporate Finance · Treasury · IR · Finance Transformation · Strategic Finance
- **Accounting:** Senior Accountant · Audit · Tax · Controller-track · Technical Accounting · FinOps
- **Operations / Supply Chain:** Supply Chain Manager · S&OP · Procurement · Logistics · Manufacturing Ops · Operations Manager
- **Consulting:** AI · ERP · Strategy · Digital Transformation · Ops · M&A
- **Strategy:** Strategy & Ops · BizOps · Chief of Staff · Corporate Strategy · M&A Strategy
- **HR or People:** Talent Acquisition · People Ops · L&D · Comp · HRBP · DEI
- **Product Management:** PM · TPM · Product Ops · Product Marketing · Growth PM

**Batch 2 — Geography, schedule, selectivity** (three questions in one call):

Question 3: "Where will you work?" (single-select)
Header: "Geography"
Options: My city + remote-US · Remote-US only · Open to relocation for top firms · Open anywhere in US · International OK

Question 4: "When should the bot run?" (single-select)
Header: "Schedule"
Options: 7:00 AM weekdays (Recommended) · 6:00 AM weekdays · Weekly Sunday evening digest · Custom

Question 5: "Match selectivity?" (single-select)
Header: "Selectivity"
Options: Balanced (75+ match — Recommended) · Strict (85+ only, fewer hits) · Relaxed (65+ match, more volume) · I'll tune later

**Batch 3 — Free text prompts** (chat messages, not AskUserQuestion):

Send: "If you said 'My city + remote-US' or 'Open to relocation for top firms,' tell me your home city (e.g., Denver, CO)."

Wait for response. Then:

Send: "Drop your master resume (.docx or .pdf preferred — Word document works best). Don't have one polished yet? Send what you have and I'll work with it."

Wait for upload.

Then:

Send: "List 20–60 named target companies, one per line. Plain names are fine — the bot auto-discovers the ATS. More than 60 strains the daily search budget. Examples: Slalom, Wipfli, Anthropic, Microsoft, Salesforce."

Wait for response.

## STEP 2 — Mount working folder

Call `mcp__cowork__request_cowork_directory`. The user will pick a parent folder; recommend they choose `Documents/Claude` or similar. The bot will create a subfolder called `Job Bot` inside it.

Let MOUNT = the mounted Windows path.

## STEP 3 — Create folder structure

Run via bash:

```bash
mkdir -p "<MOUNT>/Job Bot/applications"
mkdir -p "<MOUNT>/Job Bot/briefs"
mkdir -p "<MOUNT>/Job Bot/config"
mkdir -p "<MOUNT>/Job Bot/dashboard"
mkdir -p "<MOUNT>/Job Bot/master"
mkdir -p "<MOUNT>/Job Bot/workshop"
touch "<MOUNT>/Job Bot/briefs/all_jobs.jsonl"
touch "<MOUNT>/Job Bot/applications/applications.jsonl"
echo '{}' > "<MOUNT>/Job Bot/briefs/feedback.json"
```

## STEP 4 — Write `config/preferences.md`

Interpolate the user's answers from Step 1 into this template and write to `<MOUNT>/Job Bot/config/preferences.md`:

```markdown
# Job Search Preferences — <USER NAME>

Edit this file anytime. The daily bot reads it on every run.

## Candidate snapshot
- {ROLE FROM Q2}, currently {USER DESCRIBES — to fill in later}
- Home base: {CITY FROM BATCH 3}
- Geography rule: {ANSWER FROM Q3}

## Target function and roles
**Primary function:** {Q1 answer}
**Specific roles:** {Q2 answers, comma-separated}

## Match selectivity
**Surface threshold:** {75 if Balanced, 85 if Strict, 65 if Relaxed}
**Star threshold:** {85}

## Role keywords (used for search and matching)
Generate 8–12 keyword phrases from the user's Q2 answers. For each role, include 2–3 variants (e.g., "Solutions Engineer" + "Pre-Sales Engineer" + "Sales Engineer"). Add 2–3 "stretch" titles relevant to the function.

## Anti-keywords (filter out)
- "Software Engineer", "SDE", "DevOps", "SRE" — pure dev roles (unless function is IT/Technology)
- "Sales Executive" with no Solutions or technical qualifier — pure quota sales (unless function is Sales)
- Any "10+ years" or "Director / Principal / VP" minimums
- Active TS/SCI clearance required (unless user holds one)

## Target companies (focused search every run)
Paste the user's company list here, one per line. Aim for 20–60.

{USER'S COMPANY LIST}

## Auto-widen rule
Target ~3 qualified jobs per day. If fewer than 3 from the named target-company list hit the score floor on a given run, the bot may widen to companies NOT on the list, under these conditions:
- The resume-to-JD match still scores ≥ {floor} by the rubric (no exceptions, no padding)
- The role is in one of the target role categories above
- Source rule and freshness rule still apply
Never surface a sub-floor job. Quality over quantity remains the rule.

## Source rule (HARD)
Only company-owned career sites count as primary sources. Aggregators (LinkedIn, Indeed, Glassdoor, ZipRecruiter) are disqualified as apply links. Aggregators may be used only to discover a candidate URL or cross-check a posting date — final job in the brief must point to the company's own URL.

Supported ATSes (treat as company-direct): Greenhouse (boards.greenhouse.io, job-boards.greenhouse.io), Lever (jobs.lever.co), Ashby (<brand>.ashbyhq.com), iCIMS (<brand>.icims.com, careers-<brand>.icims.com), Workday (<brand>.wd1.myworkdayjobs.com), BambooHR (<brand>.bamboohr.com), Workable (apply.workable.com/<brand>).

## Freshness rule (HARD)
Only postings dated within the last 7 calendar days qualify. Verify posting date via JSON-LD `datePosted`, visible "Posted X days ago" text, og:updated_time, or the company's careers index page. If none verifiable, skip the job. Also: drop any posting with "Sorry, this job was removed" or similar closure marker.

## Match scoring (0–100)
- 35 pts: role keyword overlap with title + JD
- 20 pts: years-of-experience fit (penalize >7 yr minimums)
- 15 pts: location fit
- 10 pts: domain fit
- 10 pts: skill overlap
- 10 pts: network (named alumni / personal contact / referral signal)

Surface threshold: {floor}. Star threshold: 85.

## Application etiquette rules
- Cover letter: 250 words max, active voice, no AI-tells (no "leverage," "robust," "transformative," etc.)
- Resume tailoring: reorder bullets to match JD priorities, swap keyword variants where honest, never fabricate
- Resume must be one full page, ≥93% fill ratio (bot verifies via PDF conversion)

## Dealbreakers
- W-2 contract roles under 6 months
- Commission-only comp
- Roles requiring credentials user doesn't hold (CPA, active clearance, etc.)
```

## STEP 5 — Write `master/resume_master.md`

Extract text from the uploaded resume and convert to markdown. Save to `<MOUNT>/Job Bot/master/resume_master.md`. Use libreoffice for .doc/.docx conversion if needed:

```bash
libreoffice --headless --convert-to txt:Text "<uploaded-resume-path>" --outdir /tmp
```

Structure the markdown with these sections: contact, summary, education, professional experience (most recent first), selected projects, skills, certifications.

## STEP 6 — Write `master/cover_letter_template.md`

Use this template (literal content):

```markdown
# Cover Letter Template

*Bot instructions: this is the template. Replace bracketed sections per role. Keep total length ≤ 250 words. Open with the angle, never "I am writing to express interest." Active voice throughout. No em-dashes as separators. No "leverage," "robust," "transformative," "drove," "spearheaded." No negative parallelism ("It's not X, it's Y"). No bloated verbs ("serves as," "represents a").*

[Date]

[Hiring Manager Name | "Hiring Team" if unknown]
[Company]
[City, State]

Dear [Hiring Manager Name | Hiring Team],

[**OPENING — 2 sentences. State the angle: why this role at this firm, anchored in something concrete from the JD or the firm's published work. Do not open with "I am writing to express interest."**]

[**EVIDENCE — 4-5 sentences. Three concrete impact examples that map to the JD's stated requirements. Quantify everything.**]

[**BRIDGE — 2-3 sentences. Connect your differentiator (education, recent project, unique experience) to the specific JD requirement.**]

[**CLOSE — 1-2 sentences. Specific and direct. State location and availability.**]

Sincerely,

[Your Name]
[email] | [phone] | [linkedin URL]
```

## STEP 7 — Write `master/projects.md`

Create a blank project ledger the user fills in this week:

```markdown
# Project Ledger

Canonical list of your active and recent projects. The bot reads this on every run and uses it for the **Selected Projects** section in tailored resumes and the **bridge paragraph** in cover letters. Bot picks 1–3 projects per role based on JD relevance.

**How to update:** Edit this file directly, or tell Claude in chat: "Add this project to my job bot memory: [details]."

**Format per project:** name, dates, one-line summary, what was built, quantified outcomes, technologies, and `fits:` tags so the bot knows which JD types to surface it for.

---

## Active

### [Project 1 Name]
- **Dates:** [Start – End or Ongoing]
- **Role:** [Your role]
- **Built:** [1-2 sentences: what you built]
- **Why it matters:** [1 sentence: what the work demonstrated]
- **Tech:** [Technologies / methodologies / tools]
- **fits:** [comma-separated JD type tags, e.g., AI consulting, finance transformation]
- **Verify before use:** [any numbers or claims to confirm before resume submission]

### [Project 2 Name]
[Same structure]

---

## Archive
*(Empty for now. Move projects here when they're 12+ months old or no longer relevant.)*

---

## Bot usage rules

When tailoring a resume for a specific JD:
1. Read this file in full.
2. Skip any project tagged `exclude_from_outputs: true`.
3. Score each remaining Active project against the JD using the `fits:` tags.
4. Pick the top 1–3 by relevance. Never include a project that doesn't fit.
5. Never publish a TBD line.
6. Never fabricate. If a number isn't verified, don't invent one.
```

## STEP 8 — Write `config/daily_brief_prompt.md`

This is the playbook the scheduled task executes every morning. Write the literal content from the playbook section at the bottom of this prompt (see APPENDIX A below). Interpolate the user's selectivity floor and run time.

## STEP 9 — Write `dashboard/bake.py`

Write the literal content from APPENDIX B below to `<MOUNT>/Job Bot/dashboard/bake.py`.

## STEP 10 — Write `dashboard/dashboard.html`

Write the literal content from APPENDIX C below to `<MOUNT>/Job Bot/dashboard/dashboard.html`.

## STEP 11 — Schedule the daily task

Call `mcp__scheduled-tasks__create_scheduled_task` with:
- `taskId`: `<user-firstname>-daily-job-brief` (lowercase, kebab-case)
- `cronExpression`: based on user's Q4 answer (default `"0 7 * * 1-5"` for 7 AM weekdays)
- `description`: "Daily job brief for <user name> — search, score, tailor materials, persist ledger, bake dashboard, refresh artifact. Steps 5 and 6 are non-negotiable."
- `prompt`: literal content from APPENDIX D below, interpolating the user's MOUNT path

## STEP 12 — Register the persistent dashboard artifact

Call `mcp__cowork__create_artifact` with:
- `id`: `<user-firstname>-job-dashboard` (lowercase, kebab-case)
- `html_path`: `<MOUNT>\Job Bot\dashboard\dashboard.html`
- `mcp_tools`: `["mcp__workspace__bash", "mcp__cowork__present_files"]`
- `description`: "Personal job-search dashboard for <user name>. Reads briefs/all_jobs.jsonl + briefs/feedback.json + applications/applications.jsonl. Shows today's brief, lifecycle metrics, daily volume trend, location distribution, top JD skills, active pipeline, applications tracker."

**Important:** save the artifact ID returned. The scheduled task's prompt needs to reference it. Update the scheduled task's prompt to use this exact ID in Step 6.

## STEP 13 — Run the first scan now

Execute the playbook once immediately so the dashboard isn't empty on first open. This is just steps 2–6 of the daily playbook (search, score, generate materials for any qualifiers, bake, update). Skip if the user is in a rush.

## STEP 14 — Offer the deep-tailor workbook

Use `AskUserQuestion`:

Question: "Want me to generate a 30-minute deep-tailor workbook? It walks you through (1) anti-keywords, (2) compensation floor, (3) named network contacts, (4) cover-letter voice preferences, (5) score-rubric weight tuning, (6) industries to exclude, (7) stepping-stone companies, (8) project ledger entries. Saved to `Job Bot/workshop/deep_tailor.md` for you to complete this week."
Header: "Deep tailor"
Options: Yes, generate the workbook now (Recommended) · Skip, I'll tune later · Show me what's in the workbook first

If yes, write the workbook (APPENDIX E) to `<MOUNT>/Job Bot/workshop/deep_tailor.md`.

## STEP 15 — Final summary

Send the user:

> Setup complete. Your Job Bot is live.
>
> **What's in your sidebar now:** A persistent dashboard artifact. Open it to see today's brief, pipeline metrics, and run history.
>
> **What runs tomorrow morning at {scheduled time}:** The bot searches your {N} target companies, scores any new postings against your resume, generates tailored resumes and cover letters for the top matches, and refreshes the dashboard.
>
> **What you do:** Open the dashboard each morning. Click Apply on jobs you want. Click Save for later. Click Skip on misses. The bot learns from your feedback.
>
> **Files saved to:** `<MOUNT>\Job Bot\` — preferences, daily playbook, dashboard, master resume, project ledger.
>
> **To tune anything:** Tell me in chat. I can change target companies, role keywords, score weights, or the schedule.
>
> **First scheduled run:** {next weekday at user's chosen time}. Click "Run now" on the scheduled task in your Cowork sidebar tonight to pre-approve the tools the bot needs (WebSearch, WebFetch, bash, present_files).

---

# APPENDIX A — `config/daily_brief_prompt.md` content

```markdown
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

```

# APPENDIX B — `dashboard/bake.py` content

```python
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

```

# APPENDIX C — `dashboard/dashboard.html` content

```html
<meta charset="utf-8">
<style>
  :root { color-scheme: light; --ink:#111; --paper:#fff; --navy:#1f3a5f; --yellow:#f5c518; --green:#2f8a3c; --red:#c0392b; --grey:#666; --line:#e6e6e6; --bg:#fafafa; }
  *,*::before,*::after { box-sizing: border-box; }
  body { margin:0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; color:var(--ink); background:var(--bg); font-size:14px; line-height:1.45; }
  .wrap { max-width:1200px; margin:0 auto; padding:18px; }
  header { display:flex; justify-content:space-between; align-items:baseline; padding-bottom:12px; border-bottom:2px solid var(--ink); margin-bottom:18px; }
  header h1 { margin:0; font-size:22px; letter-spacing:-0.01em; }
  header .meta { color:var(--grey); font-size:12px; }
  .kpi-row { display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; margin-bottom:18px; }
  .kpi { background:var(--paper); border:1px solid var(--line); padding:14px 16px; border-radius:6px; }
  .kpi .label { font-size:11px; text-transform:uppercase; color:var(--grey); letter-spacing:0.04em; }
  .kpi .value { font-size:30px; font-weight:600; line-height:1.1; margin-top:6px; color:var(--ink); }
  .kpi .sub { font-size:11px; color:var(--grey); margin-top:4px; }
  .panel { background:var(--paper); border:1px solid var(--line); border-radius:6px; padding:14px 16px; margin-bottom:14px; }
  .panel h2 { margin:0 0 10px 0; font-size:14px; text-transform:uppercase; letter-spacing:0.04em; color:var(--navy); }
  .grid-2 { display:grid; grid-template-columns: 1fr 1fr; gap:14px; }
  .chart-wrap { position:relative; height:240px; }
  table { width:100%; border-collapse:collapse; font-size:13px; }
  th, td { text-align:left; padding:8px 10px; border-bottom:1px solid var(--line); vertical-align:top; }
  th { font-size:11px; text-transform:uppercase; color:var(--grey); letter-spacing:0.04em; font-weight:600; }
  td.score { font-weight:600; }
  .chip { display:inline-block; padding:2px 7px; border-radius:10px; font-size:11px; font-weight:600; }
  .chip-green { background:#e6f4ea; color:var(--green); }
  .chip-yellow { background:#fff7d1; color:#8a6d00; }
  .chip-grey { background:#eee; color:var(--grey); }
  .chip-navy { background:#e6ecf5; color:var(--navy); }
  .btn { font:inherit; cursor:pointer; padding:5px 10px; border-radius:4px; border:1px solid var(--ink); background:var(--paper); color:var(--ink); margin-right:4px; font-size:12px; display:inline-block; text-align:center; text-decoration:none; line-height:1.3; }
  .btn:hover { background:var(--ink); color:var(--paper); text-decoration:none; }
  a.btn { color:var(--ink); }
  a.btn:hover { color:var(--paper); }
  .btn.applied { background:var(--green); color:var(--paper); border-color:var(--green); }
  .btn.skipped { background:var(--grey); color:var(--paper); border-color:var(--grey); }
  .btn.saved { background:var(--yellow); color:var(--ink); border-color:var(--yellow); }
  a.apply-link { color:var(--navy); text-decoration:none; font-weight:600; }
  a.apply-link:hover { text-decoration:underline; }
  .empty { text-align:center; padding:32px 20px; color:var(--grey); }
  .empty h2 { color:var(--navy); margin-bottom:6px; }
  .empty .rules { background:var(--bg); border:1px dashed var(--line); border-radius:6px; padding:14px; margin-top:18px; text-align:left; max-width:560px; margin-left:auto; margin-right:auto; }
  .tabs { display:flex; gap:0; border-bottom:1px solid var(--line); margin-bottom:10px; }
  .tab { padding:8px 14px; cursor:pointer; border-bottom:2px solid transparent; font-size:12px; text-transform:uppercase; letter-spacing:0.04em; color:var(--grey); }
  .tab.active { color:var(--ink); border-bottom-color:var(--yellow); font-weight:600; }
  .pulse { display:inline-block; width:8px; height:8px; background:var(--green); border-radius:50%; margin-right:6px; vertical-align:middle; animation:pulse 1.6s ease-in-out infinite; }
  @keyframes pulse { 0%,100% { opacity:1 } 50% { opacity:0.3 } }
  .footer { text-align:center; color:var(--grey); font-size:11px; padding:18px 0; }
  .small-link { color:var(--grey); font-size:11px; text-decoration:underline; cursor:pointer; }
  .truncate { max-width:280px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .err { background:#fff4f0; border:1px solid #f3c2b3; color:#8a3010; padding:12px 14px; border-radius:6px; margin-bottom:14px; font-size:13px; }
  /* Today's brief cards */
  .today-card { display:grid; grid-template-columns: 80px 1fr auto; gap:14px; padding:14px; border:1px solid var(--line); border-radius:6px; margin-bottom:10px; background:#fff; align-items:center; }
  .today-card.top { border-left:6px solid var(--yellow); }
  .today-score { font-size:28px; font-weight:700; text-align:center; padding:8px 0; border-radius:6px; }
  .today-score.green { background:#e6f4ea; color:var(--green); }
  .today-score.yellow { background:#fff7d1; color:#8a6d00; }
  .today-meta { color:var(--grey); font-size:12px; margin-top:3px; }
  .today-why { font-size:13px; color:var(--ink); margin-top:6px; line-height:1.4; }
  .today-actions { display:flex; flex-direction:column; gap:4px; min-width:140px; }
  .today-actions .btn { width:100%; text-align:center; }
  .quiet-day { padding:18px; text-align:center; background:var(--bg); border-radius:6px; color:var(--grey); }
  .quiet-day strong { color:var(--ink); display:block; margin-bottom:4px; }
  /* Application Pipeline */
  .app-metrics { display:grid; grid-template-columns: repeat(6, 1fr); gap:8px; margin-bottom:14px; }
  .app-metrics .tile { background:var(--bg); border:1px solid var(--line); border-radius:6px; padding:10px 8px; text-align:center; }
  .app-metrics .tile strong { display:block; font-size:22px; line-height:1.1; }
  .app-metrics .tile .l { display:block; font-size:10px; text-transform:uppercase; color:var(--grey); letter-spacing:0.04em; margin-top:4px; }
  .app-metrics .tile.submitted strong { color:var(--ink); }
  .app-metrics .tile.acknowledged strong { color:#8a6d00; }
  .app-metrics .tile.in-progress strong { color:var(--green); }
  .app-metrics .tile.rejected strong { color:var(--red); }
  .app-metrics .tile.offer strong { color:var(--yellow); background:none; }
  .app-metrics .tile.rate strong { color:var(--navy); }
  .status-chip { display:inline-block; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:600; text-transform:capitalize; }
  .status-chip.submitted { background:#e6ecf5; color:var(--navy); }
  .status-chip.acknowledged { background:#fff7d1; color:#8a6d00; }
  .status-chip.interviewing { background:#e6f4ea; color:var(--green); }
  .status-chip.rejected { background:#fdecec; color:var(--red); }
  .status-chip.offer { background:#fff7d1; color:#8a6d00; border:1px solid var(--yellow); }
  .status-chip.withdrew { background:#eee; color:var(--grey); }
  details.app-row { border:1px solid var(--line); border-radius:6px; margin-bottom:6px; background:var(--paper); }
  details.app-row[open] { border-color:var(--navy); }
  details.app-row summary { padding:10px 12px; cursor:pointer; display:grid; grid-template-columns: 90px 1fr 60px 110px 1fr; gap:12px; align-items:center; list-style:none; font-size:13px; }
  details.app-row summary::-webkit-details-marker { display:none; }
  details.app-row summary:hover { background:var(--bg); }
  .app-history { padding:10px 14px 14px 14px; border-top:1px solid var(--line); font-size:12px; color:var(--grey); }
  .app-history-row { display:grid; grid-template-columns: 110px 110px 1fr; gap:10px; padding:4px 0; }
  .app-history-row.notes { color:var(--ink); padding-top:8px; border-top:1px dashed var(--line); margin-top:6px; }
  /* Today's counts strip */
  .today-counts { display:grid; grid-template-columns: repeat(4, 1fr); gap:12px; margin-bottom:14px; padding:12px 14px; background:var(--bg); border:1px solid var(--line); border-radius:6px; }
  .today-counts .tc { text-align:center; }
  .today-counts .tc .n { font-size:24px; font-weight:700; color:var(--ink); display:block; line-height:1.1; }
  .today-counts .tc .lbl { font-size:11px; text-transform:uppercase; color:var(--grey); letter-spacing:0.04em; margin-top:4px; display:block; }
  .today-counts .tc.disqualified .n { color:var(--grey); }
  .today-counts .tc.qualified .n { color:var(--green); }
  .today-counts .tc.applied .n { color:var(--navy); }
  .today-counts .threshold-note { grid-column: 1 / -1; text-align:center; font-size:11px; color:var(--grey); padding-top:6px; border-top:1px dashed var(--line); margin-top:4px; }
  /* Run history */
  .run-row { border:1px solid var(--line); border-radius:6px; margin-bottom:8px; background:var(--paper); overflow:hidden; }
  .run-row[open] { border-color:var(--navy); }
  .run-summary { padding:12px 14px; cursor:pointer; display:grid; grid-template-columns: 1fr auto auto auto auto; gap:18px; align-items:center; list-style:none; font-size:13px; }
  .run-summary::-webkit-details-marker { display:none; }
  .run-summary:hover { background:var(--bg); }
  .run-date { font-weight:600; color:var(--ink); }
  .run-date .weekday { color:var(--grey); font-weight:400; margin-left:6px; font-size:12px; }
  .run-stat { color:var(--grey); font-size:11px; text-align:center; min-width:60px; }
  .run-stat strong { font-size:18px; display:block; line-height:1.1; }
  .run-stat.scanned strong { color:var(--ink); }
  .run-stat.disqualified strong { color:var(--grey); }
  .run-stat.qualified strong { color:var(--green); }
  .run-stat.applied strong { color:var(--navy); }
  .run-stat .lbl { display:block; text-transform:uppercase; letter-spacing:0.04em; margin-top:2px; }
  .run-top { font-size:12px; color:var(--grey); max-width:240px; text-align:right; }
  .run-top strong { color:var(--ink); }
  .run-detail { padding:0 14px 14px 14px; border-top:1px solid var(--line); }
  .run-detail table { margin-top:10px; }
  .lifetime-line { text-align:center; color:var(--grey); font-size:11px; margin-top:-12px; margin-bottom:18px; padding-bottom:6px; }
  .lifetime-line strong { color:var(--ink); }
</style>

<div class="wrap">
  <header>
    <div>
      <h1>Daily Job Briefing</h1>
      <div class="meta"><span class="pulse"></span><span id="status-text">Loading…</span></div>
    </div>
    <div style="display:flex; align-items:center; gap:14px">
      <div class="meta">{USER_NAME} · {SEARCH_TAGLINE}</div>
      <button class="btn" id="refresh-btn" style="margin:0">Refresh data</button>
    </div>
  </header>

  <div id="err-state" style="display:none" class="err"></div>

  <div id="empty-state" style="display:none">
    <div class="empty panel">
      <h2>No data yet</h2>
      <p>The first scheduled run hasn't completed. Jobs scored, applied, and skipped will populate here automatically.</p>
      <div id="next-run"></div>
      <div class="rules">
        <strong>Search rules currently in effect:</strong><br>
        Source: company-direct career sites only (no aggregators)<br>
        Freshness: postings ≤ 7 days old, date verified or skipped<br>
        Output: top 3 matches per day, never padded<br>
        Match floor: score ≥ 75
      </div>
    </div>
  </div>

  <div id="data-state" style="display:none">
    <div class="panel" id="today-panel">
      <h2>Today's brief · <span id="today-date"></span></h2>
      <div id="today-counts" class="today-counts"></div>
      <div id="today-cards"></div>
    </div>

    <div class="kpi-row">
      <div class="kpi"><div class="label">Jobs scanned (30d)</div><div class="value" id="kpi-scanned">0</div><div class="sub" id="kpi-scanned-sub">—</div></div>
      <div class="kpi"><div class="label">Qualified ≥75 match (30d)</div><div class="value" id="kpi-qualified">0</div><div class="sub" id="kpi-qualified-sub">—</div></div>
      <div class="kpi"><div class="label">Applied (30d)</div><div class="value" id="kpi-applied">0</div><div class="sub" id="kpi-applied-sub">—</div></div>
      <div class="kpi"><div class="label">Apply rate</div><div class="value" id="kpi-rate">—</div><div class="sub">applied / qualified</div></div>
    </div>
    <div class="lifetime-line" id="lifetime-line">—</div>

    <div class="panel">
      <h2>Run history · most recent first</h2>
      <div id="run-history"></div>
    </div>

    <div class="panel">
      <h2>Daily volume — last 30 days</h2>
      <div class="chart-wrap"><canvas id="chart-volume"></canvas></div>
    </div>

    <div class="grid-2">
      <div class="panel">
        <h2>Where the jobs are</h2>
        <div class="chart-wrap"><canvas id="chart-geo"></canvas></div>
      </div>
      <div class="panel">
        <h2>Top skills mentioned in JDs</h2>
        <div class="chart-wrap"><canvas id="chart-skills"></canvas></div>
      </div>
    </div>

    <div class="panel">
      <h2>My Applications · submitted + recruiter activity</h2>
      <div class="app-metrics" id="app-metrics"></div>
      <div class="tabs" id="apps-tabs">
        <div class="tab active" data-apps-filter="active">In progress</div>
        <div class="tab" data-apps-filter="lost">Rejected</div>
        <div class="tab" data-apps-filter="won">Offers</div>
        <div class="tab" data-apps-filter="all">All</div>
      </div>
      <div id="apps-table-wrap"></div>
    </div>

    <div class="panel">
      <h2>Active pipeline · qualified, no decision yet</h2>
      <div id="pipeline-table-wrap"></div>
    </div>

    <div class="panel">
      <h2>Activity log</h2>
      <div class="tabs">
        <div class="tab active" data-tab="applied">Applied</div>
        <div class="tab" data-tab="skipped">Skipped</div>
        <div class="tab" data-tab="saved">Saved for later</div>
      </div>
      <div id="log-table-wrap"></div>
    </div>
  </div>

  <div class="footer">
    Reads <code>Job Bot/briefs/all_jobs.jsonl</code> + <code>Job Bot/briefs/feedback.json</code>. Edit <code>config/preferences.md</code> to retune.
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js@4.5.0/dist/chart.umd.js" integrity="sha384-iU8HYtnGQ8Cy4zl7gbNMOhsDTTKX02BTXptVP/vqAWIaTfM7isw76iyZCsjL2eVi" crossorigin="anonymous"></script>

<script>
const COLORS = { ink:'#111', navy:'#1f3a5f', yellow:'#f5c518', green:'#2f8a3c', red:'#c0392b', grey:'#666', line:'#e6e6e6' };
const LOCAL_KEY = 'jobbot_feedback_cache_v1';
const MOUNT_KEY = 'jobbot_mount_path_v1';

let MOUNT = null; // discovered at load — e.g. /sessions/<id>/mnt/Job Bot
let JOBS = [];
let APPLICATIONS = [];
let FEEDBACK = {};
let CURRENT_TAB = 'applied';
let APPS_FILTER = 'active';

async function bash(cmd) {
  return await window.cowork.callMcpTool('mcp__workspace__bash', { command: cmd });
}

function extractText(out) {
  if (typeof out === 'string') return out;
  if (out && out.content && Array.isArray(out.content)) return out.content.map(c => c.text || '').join('');
  if (out && out.output) return out.output;
  return '';
}

function safeJson(text, fallback) { try { return JSON.parse(text); } catch { return fallback; } }

function parseJsonl(text) {
  if (!text) return [];
  return text.split('\n').filter(l => l.trim()).map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
}

async function discoverMount() {
  // Always re-discover the mount in case the session changed since last load
  const out = extractText(await bash(`ls -d /sessions/*/mnt/Job\\ Bot 2>/dev/null | head -1`)).trim();
  if (out) {
    localStorage.setItem(MOUNT_KEY, out);
    return out;
  }
  // Fall back to cached path if live discovery returns nothing
  const cached = localStorage.getItem(MOUNT_KEY);
  if (cached) {
    const exists = extractText(await bash(`test -d "${cached}" && echo OK || echo MISS`)).trim();
    if (exists === 'OK') return cached;
  }
  return null;
}

function showError(msg) {
  const el = document.getElementById('err-state');
  el.style.display = 'block';
  el.innerHTML = msg;
}

async function loadData() {
  document.getElementById('status-text').textContent = 'Loading…';
  // PRIMARY: read baked-in data from the HTML (works regardless of mount state)
  const bakedEl = document.getElementById('baked-data');
  if (bakedEl) {
    try {
      const baked = JSON.parse(bakedEl.textContent);
      JOBS = baked.jobs || [];
      APPLICATIONS = baked.applications || [];
      FEEDBACK = baked.feedback || {};
      // Merge any pending localStorage feedback that hasn't synced
      const cached = JSON.parse(localStorage.getItem(LOCAL_KEY) || '{}');
      Object.assign(FEEDBACK, cached);
      // Try to discover mount in background for Apply/Skip writes; not blocking
      discoverMount().then(m => { MOUNT = m; });
      const stamp = baked.generated_at ? new Date(baked.generated_at).toLocaleString() : 'baked-in';
      document.getElementById('status-text').textContent = `${JOBS.length} jobs in ledger · snapshot ${stamp}`;
      return true;
    } catch (e) {
      console.warn('baked data parse failed, falling back to live read', e);
    }
  }
  // FALLBACK: live read via bash (only works if mount available in this session)
  MOUNT = await discoverMount();
  if (!MOUNT) {
    showError('No baked-in data and Job Bot folder not mounted in this session. Ask Claude to re-bake the dashboard, or open the folder via the Cowork sidebar and reload.');
    return false;
  }
  try {
    const jobsRaw = extractText(await bash(`cat "${MOUNT}/briefs/all_jobs.jsonl" 2>/dev/null || echo ""`));
    const fbRaw = extractText(await bash(`cat "${MOUNT}/briefs/feedback.json" 2>/dev/null || echo "{}"`));
    JOBS = parseJsonl(jobsRaw);
    FEEDBACK = safeJson(fbRaw, {});
    const cached = JSON.parse(localStorage.getItem(LOCAL_KEY) || '{}');
    Object.assign(FEEDBACK, cached);
    document.getElementById('status-text').textContent = `${JOBS.length} jobs in ledger · live read ${new Date().toLocaleTimeString()}`;
    return true;
  } catch (e) {
    showError('Could not read ledger files: ' + (e.message||e));
    return false;
  }
}

function daysAgo(dateStr) {
  if (!dateStr) return 999;
  const d = new Date(dateStr);
  return Math.floor((Date.now() - d.getTime()) / 86400000);
}
function lastNDays(n) { return JOBS.filter(j => daysAgo(j.scored_date) <= n); }

function renderEmpty() {
  document.getElementById('empty-state').style.display = 'block';
  document.getElementById('data-state').style.display = 'none';
  const next = nextWeekday7am();
  document.getElementById('next-run').innerHTML = `<p style="margin-top:14px"><strong>Next scheduled run:</strong> ${next.toLocaleString()} (in ${humanDelta(next - Date.now())})</p>`;
}

function nextWeekday7am() {
  const d = new Date();
  d.setHours(7, 7, 0, 0);
  if (d <= new Date()) d.setDate(d.getDate() + 1);
  while (d.getDay() === 0 || d.getDay() === 6) d.setDate(d.getDate() + 1);
  return d;
}

function humanDelta(ms) {
  const h = Math.floor(ms / 3600000);
  if (h < 24) return `${h}h`;
  return `${Math.floor(h/24)}d ${h%24}h`;
}

function renderData() {
  document.getElementById('empty-state').style.display = 'none';
  document.getElementById('data-state').style.display = 'block';

  const last30 = lastNDays(30);
  const qualified30 = last30.filter(j => j.outcome === 'qualified');
  const applied30 = qualified30.filter(j => (FEEDBACK[j.url]||{}).status === 'applied');

  document.getElementById('kpi-scanned').textContent = last30.length;
  document.getElementById('kpi-scanned-sub').textContent = `${lastNDays(7).length} in last 7 days`;
  document.getElementById('kpi-qualified').textContent = qualified30.length;
  document.getElementById('kpi-qualified-sub').textContent = `${Math.round(100*qualified30.length/Math.max(1,last30.length))}% pass rate`;
  document.getElementById('kpi-applied').textContent = applied30.length;
  const skip = qualified30.filter(j => (FEEDBACK[j.url]||{}).status === 'skipped').length;
  const save = qualified30.filter(j => (FEEDBACK[j.url]||{}).status === 'saved').length;
  document.getElementById('kpi-applied-sub').textContent = `${skip} skipped · ${save} saved`;
  document.getElementById('kpi-rate').textContent = qualified30.length ? `${Math.round(100*applied30.length/qualified30.length)}%` : '—';

  // Lifetime stats line
  const allTime = JOBS;
  const allQualified = allTime.filter(j => j.outcome === 'qualified');
  const allApplied = allQualified.filter(j => (FEEDBACK[j.url]||{}).status === 'applied');
  const firstDate = allTime.map(j => j.scored_date||'').filter(Boolean).sort()[0];
  const dayCount = firstDate ? Math.max(1, Math.floor((Date.now() - new Date(firstDate).getTime()) / 86400000) + 1) : 1;
  document.getElementById('lifetime-line').innerHTML = `Lifetime · <strong>${allTime.length}</strong> scanned · <strong>${allQualified.length}</strong> qualified · <strong>${allApplied.length}</strong> applied · across ${dayCount} day${dayCount===1?'':'s'}`;

  renderTodayBrief();
  renderRunHistory();
  renderVolumeChart();
  renderGeoChart();
  renderSkillsChart();
  renderApplications();
  renderPipeline();
  renderLog();
}

const APP_STATUS_META = {
  submitted:    { label: 'Submitted',    chip: 'chip-navy',   bucket: 'active' },
  acknowledged: { label: 'Acknowledged', chip: 'chip-navy',   bucket: 'active' },
  screening:    { label: 'Screening',    chip: 'chip-yellow', bucket: 'active' },
  assessment:   { label: 'Assessment',   chip: 'chip-yellow', bucket: 'active' },
  interview:    { label: 'Interview',    chip: 'chip-yellow', bucket: 'active' },
  offer:        { label: 'Offer',        chip: 'chip-green',  bucket: 'won'    },
  accepted:     { label: 'Accepted',     chip: 'chip-green',  bucket: 'won'    },
  declined:     { label: 'Declined',     chip: 'chip-grey',   bucket: 'lost'   },
  rejected:     { label: 'Rejected',     chip: 'chip-grey',   bucket: 'lost'   },
  ghosted:      { label: 'Ghosted',      chip: 'chip-grey',   bucket: 'lost'   },
};

function renderAppMetrics() {
  const m = document.getElementById('app-metrics');
  if (!m) return;
  if (!APPLICATIONS || !APPLICATIONS.length) {
    m.innerHTML = '';
    return;
  }
  const buckets = { submitted:0, acknowledged:0, in_progress:0, rejected:0, offer:0 };
  APPLICATIONS.forEach(a => {
    const s = a.application_status;
    if (s === 'submitted') buckets.submitted++;
    else if (s === 'acknowledged') buckets.acknowledged++;
    else if (['interviewing','phone-screen','onsite','final-round','reference-check'].includes(s)) buckets.in_progress++;
    else if (['rejected','ghosted','declined'].includes(s)) buckets.rejected++;
    else if (['offer','accepted'].includes(s)) buckets.offer++;
  });
  const total = APPLICATIONS.length;
  const responded = APPLICATIONS.filter(a => a.last_email_at && a.last_email_at !== a.applied_at).length;
  const rate = total ? Math.round(100 * responded / total) + '%' : '—';
  m.innerHTML = `
    <div class="tile submitted"><strong>${buckets.submitted}</strong><span class="l">Submitted</span></div>
    <div class="tile acknowledged"><strong>${buckets.acknowledged}</strong><span class="l">Acknowledged</span></div>
    <div class="tile in-progress"><strong>${buckets.in_progress}</strong><span class="l">In progress</span></div>
    <div class="tile rejected"><strong>${buckets.rejected}</strong><span class="l">Rejected</span></div>
    <div class="tile offer"><strong>${buckets.offer}</strong><span class="l">Offers</span></div>
    <div class="tile rate"><strong>${rate}</strong><span class="l">Response rate</span></div>
  `;
}

function renderApplications() {
  renderAppMetrics();
  const wrap = document.getElementById('apps-table-wrap');
  if (!APPLICATIONS || !APPLICATIONS.length) {
    wrap.innerHTML = '<div class="empty" style="padding:18px"><em>No applications logged yet. The bot adds rows here when you confirm a submission.</em></div>';
    return;
  }
  // Filter
  const filtered = APPLICATIONS.filter(a => {
    const meta = APP_STATUS_META[a.application_status] || { bucket: 'active' };
    if (APPS_FILTER === 'all') return true;
    return meta.bucket === APPS_FILTER;
  });
  // Sort: most recent activity first (last_email_at if present, else applied_at)
  filtered.sort((a, b) => {
    const ta = a.last_email_at || a.applied_at || '';
    const tb = b.last_email_at || b.applied_at || '';
    return tb.localeCompare(ta);
  });

  if (!filtered.length) {
    wrap.innerHTML = `<div class="empty" style="padding:18px"><em>No applications in "${APPS_FILTER}" bucket.</em></div>`;
    return;
  }

  const rows = filtered.map(a => {
    const meta = APP_STATUS_META[a.application_status] || { label: a.application_status, chip: 'chip-grey' };
    const days = a.applied_at ? Math.max(0, daysAgo(a.applied_at)) : '—';
    const dayLabel = days === 0 ? 'today' : (days === 1 ? '1 day ago' : `${days} days ago`);
    const lastEmail = a.last_email_subject
      ? `<span class="truncate" title="${escapeHtml(a.last_email_subject)}">${escapeHtml(a.last_email_subject)}</span>` +
        (a.last_email_at ? `<div class="sub" style="color:var(--grey); font-size:11px">${a.last_email_at}</div>` : '')
      : '<span class="sub" style="color:var(--grey)">—</span>';
    const gmailLink = a.last_email_thread_id
      ? `<a class="small-link" href="https://mail.google.com/mail/u/0/#inbox/${a.last_email_thread_id}" target="_blank">open thread</a>`
      : '';
    const materialsLink = a.tailored_files
      ? `<a class="small-link" href="file:///${a.tailored_files.replace(/\\/g,'/')}" title="${escapeHtml(a.tailored_files)}">materials</a>`
      : '';
    const score = (a.score_at_apply ?? '—');
    return `<tr>
      <td><strong>${escapeHtml(a.company)}</strong><div class="sub" style="color:var(--grey); font-size:11px">${escapeHtml(a.title || '')}</div></td>
      <td>${a.applied_at || '—'}<div class="sub" style="color:var(--grey); font-size:11px">${dayLabel}</div></td>
      <td><span class="chip ${meta.chip}">${meta.label}</span></td>
      <td>${lastEmail}${gmailLink ? ' · ' + gmailLink : ''}</td>
      <td class="score">${score}</td>
      <td>${materialsLink}${a.url ? ' · <a class="small-link" href="' + a.url + '" target="_blank">JD</a>' : ''}</td>
    </tr>`;
  }).join('');

  wrap.innerHTML = `<table>
    <thead><tr><th>Company / Role</th><th>Applied</th><th>Status</th><th>Last email</th><th>Score</th><th>Links</th></tr></thead>
    <tbody>${rows}</tbody>
  </table>`;
}

function escapeHtml(s) {
  return String(s || '').replace(/[&<>"']/g, c => ({ '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[c]));
}

function renderRunHistory() {
  const wrap = document.getElementById('run-history');
  // Group jobs by scored_date
  const byDate = {};
  JOBS.forEach(j => {
    const d = (j.scored_date||'').slice(0,10);
    if (!d) return;
    if (!byDate[d]) byDate[d] = [];
    byDate[d].push(j);
  });
  const dates = Object.keys(byDate).sort().reverse(); // most recent first
  if (!dates.length) {
    wrap.innerHTML = '<p style="color:var(--grey); padding:10px">No runs yet. First run is scheduled for tomorrow at 7:00 AM Denver time.</p>';
    return;
  }
  wrap.innerHTML = dates.slice(0, 30).map(d => {
    const jobs = byDate[d];
    const qualified = jobs.filter(j => j.outcome === 'qualified').sort((a,b)=>(b.score||0)-(a.score||0));
    const stepping = jobs.filter(j => j.outcome === 'stepping-stone').sort((a,b)=>(b.score||0)-(a.score||0));
    const surfaced = [...qualified, ...stepping];
    const applied = jobs.filter(j => (FEEDBACK[j.url]||{}).status === 'applied');
    const top = qualified[0] || stepping[0];
    const dateObj = new Date(d + 'T12:00:00');
    const weekday = dateObj.toLocaleDateString('en-US', { weekday: 'short' });
    const pretty = dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    const dropFreshness = jobs.filter(j => j.outcome === 'stale').length;
    const dropFit = jobs.filter(j => ['off-fit','dealbreaker'].includes(j.outcome)).length;
    const disqualified = jobs.length - qualified.length - stepping.length;
    return `<details class="run-row">
      <summary class="run-summary">
        <div class="run-date">${pretty}<span class="weekday">${weekday}</span></div>
        <div class="run-stat scanned"><strong>${jobs.length}</strong><span class="lbl">Scanned</span></div>
        <div class="run-stat disqualified"><strong>${disqualified}</strong><span class="lbl">Disqual.</span></div>
        <div class="run-stat qualified"><strong>${qualified.length}${stepping.length ? `+${stepping.length}*` : ''}</strong><span class="lbl">Qual ≥75${stepping.length ? ' (+steps)' : ''}</span></div>
        <div class="run-stat applied"><strong>${applied.length}</strong><span class="lbl">Applied</span></div>
        <div class="run-top">${top ? `<strong>${esc(top.company)}</strong> · ${top.score}` : '<em>quiet day</em>'}</div>
      </summary>
      <div class="run-detail">
        ${surfaced.length ? `<table>
          <thead><tr><th>Score</th><th>Company / Role</th><th>Location</th><th>Posted</th><th>Why it fits</th><th>Status</th></tr></thead>
          <tbody>${surfaced.map(j => {
            const fb = FEEDBACK[j.url] || {};
            const chip = (j.score||0) >= 85 ? 'chip chip-green' : 'chip chip-yellow';
            const stepBadge = j.outcome === 'stepping-stone' ? ' <span class="chip chip-yellow" style="font-size:9px">step</span>' : '';
            const statusChip = fb.status ? `<span class="chip chip-${fb.status==='applied'?'green':fb.status==='saved'?'yellow':'grey'}">${fb.status}</span>` : '<span class="chip chip-navy">undecided</span>';
            return `<tr>
              <td><span class="${chip}">${j.score||'-'}</span>${stepBadge}</td>
              <td><div><strong>${esc(j.company)}</strong></div><div class="truncate"><a class="apply-link" href="${esc(j.url)}" target="_blank">${esc(j.title||'')}</a></div></td>
              <td>${esc(j.location||'—')}</td>
              <td>${esc(j.posted_date||'—')}</td>
              <td style="max-width:300px">${esc(j.why_fits||'')}</td>
              <td>${statusChip}</td>
            </tr>`;
          }).join('')}</tbody>
        </table>` : ''}
        <div style="margin-top:10px; color:var(--grey); font-size:11px">
          Drops: ${dropFreshness} stale (>7 days) · ${dropFit} off-fit or dealbreaker · ${jobs.length - qualified.length - dropFreshness - dropFit} other
        </div>
      </div>
    </details>`;
  }).join('');
}

function renderTodayBrief() {
  const today = new Date().toISOString().slice(0,10);
  const dateEl = document.getElementById('today-date');
  dateEl.textContent = new Date().toLocaleDateString('en-US', { weekday:'long', month:'long', day:'numeric', year:'numeric' });

  // Find the most recent run date in the ledger
  const allDates = JOBS.map(j => (j.scored_date||'').slice(0,10)).filter(Boolean).sort();
  const latestDate = allDates.length ? allDates[allDates.length - 1] : today;
  const useDate = latestDate;
  if (useDate !== today) {
    dateEl.textContent += ` (last run: ${useDate})`;
  }

  // Compute today's counts across the full ledger for that date
  const todayAll = JOBS.filter(j => (j.scored_date||'').slice(0,10) === useDate);
  const todayQualified = todayAll.filter(j => j.outcome === 'qualified');
  const todaySteppingStone = todayAll.filter(j => j.outcome === 'stepping-stone');
  const todayDisqualified = todayAll.length - todayQualified.length - todaySteppingStone.length;
  const todayApplied = todayAll.filter(j => (FEEDBACK[j.url]||{}).status === 'applied').length;
  // Top 3 qualified + up to 2 stepping-stones below
  const topQualified = todayQualified.sort((a,b) => (b.score||0) - (a.score||0)).slice(0,3);
  const topStepping = todaySteppingStone.sort((a,b) => (b.score||0) - (a.score||0)).slice(0,2);
  const todayJobs = [...topQualified, ...topStepping];

  // Render the counts strip — 4 tiles
  document.getElementById('today-counts').innerHTML = `
    <div class="tc"><span class="n">${todayAll.length}</span><span class="lbl">Jobs scanned</span></div>
    <div class="tc disqualified"><span class="n">${todayDisqualified}</span><span class="lbl">Disqualified</span></div>
    <div class="tc qualified"><span class="n">${todayQualified.length}</span><span class="lbl">Qualified ≥75</span></div>
    <div class="tc applied"><span class="n">${todayApplied}</span><span class="lbl">Applied</span></div>
    <div class="threshold-note">Bot uses a 75-point match floor against your resume; 85+ stars as a strong fit. Disqualified = stale, off-fit, or below score floor. Applied counts only the qualified jobs you've marked Applied.</div>
  `;

  const cards = document.getElementById('today-cards');
  if (!todayJobs.length) {
    cards.innerHTML = `<div class="quiet-day">
      <strong>Quiet day — 0 qualifying postings</strong>
      Scanned ${todayAll.length} listings. None passed the source rule (company-direct only), the 7-day freshness floor, and the 75-point match threshold. The bar holds.
    </div>`;
    return;
  }

  cards.innerHTML = todayJobs.map((j, idx) => {
    const fb = FEEDBACK[j.url] || {};
    const isStepping = j.outcome === 'stepping-stone';
    const scoreCls = (j.score||0) >= 85 ? 'green' : 'yellow';
    const topCls = (idx === 0 && !isStepping) ? ' top' : '';
    const steppingBadge = isStepping ? '<span class="chip chip-yellow" style="margin-left:6px">Stepping stone</span>' : '';
    const netOverrideBadge = j.network_override ? '<span class="chip chip-navy" style="margin-left:6px">Network override</span>' : '';
    const folder = j.tailored_files || '';
    const slug = (j.company||'').toLowerCase().replace(/[^a-z0-9]+/g,'');
    const resumeFile = folder ? `${folder}${slug}_resume_tailored.docx` : '';
    const coverFile = folder ? `${folder}${slug}_cover_letter.docx` : '';
    const appliedCls = fb.status === 'applied' ? ' applied' : '';
    const skippedCls = fb.status === 'skipped' ? ' skipped' : '';
    const savedCls = fb.status === 'saved' ? ' saved' : '';
    return `<div class="today-card${topCls}">
      <div class="today-score ${scoreCls}">${j.score||'-'}</div>
      <div>
        <div><strong>${esc(j.company)}</strong> · ${esc(j.title||'')}${steppingBadge}${netOverrideBadge}</div>
        <div class="today-meta">${esc(j.location||'—')} · posted ${esc(j.posted_date||'unverified')}${j.date_source ? ` (${esc(j.date_source)})` : ''}</div>
        <div class="today-why">${esc(j.why_fits||'')}</div>
      </div>
      <div class="today-actions">
        <a class="btn" href="${esc(j.url)}" target="_blank" rel="noopener noreferrer">Apply on site →</a>
        ${resumeFile ? `<button class="btn" onclick="presentFile('${esc(resumeFile)}')">Tailored resume</button>` : ''}
        ${coverFile ? `<button class="btn" onclick="presentFile('${esc(coverFile)}')">Cover letter</button>` : ''}
        ${folder ? `<button class="btn" onclick="presentFolder('${esc(folder)}')">Open folder</button>` : ''}
        <div style="display:flex; gap:4px; margin-top:4px">
          <button class="btn${appliedCls}" style="flex:1; margin:0" onclick="setStatus('${esc(j.url)}', 'applied')">Applied</button>
          <button class="btn${savedCls}" style="flex:1; margin:0" onclick="setStatus('${esc(j.url)}', 'saved')">Save</button>
          <button class="btn${skippedCls}" style="flex:1; margin:0" onclick="setStatus('${esc(j.url)}', 'skipped')">Skip</button>
        </div>
      </div>
    </div>`;
  }).join('');
}

function renderVolumeChart() {
  const ctx = document.getElementById('chart-volume');
  const days = [];
  const today = new Date(); today.setHours(0,0,0,0);
  for (let i = 29; i >= 0; i--) {
    const d = new Date(today); d.setDate(d.getDate() - i);
    days.push(d.toISOString().slice(0,10));
  }
  const counts = days.map(day => {
    const dayJobs = JOBS.filter(j => (j.scored_date||'').slice(0,10) === day);
    return {
      scanned: dayJobs.length,
      qualified: dayJobs.filter(j => j.outcome === 'qualified').length,
      applied: dayJobs.filter(j => (FEEDBACK[j.url]||{}).status === 'applied').length
    };
  });
  if (window._cv) window._cv.destroy();
  window._cv = new Chart(ctx, {
    type: 'line',
    data: { labels: days.map(d => d.slice(5)), datasets: [
      { label:'Scanned', data: counts.map(c=>c.scanned), borderColor: COLORS.grey, backgroundColor:'transparent', borderWidth:2, tension:0.3 },
      { label:'Qualified', data: counts.map(c=>c.qualified), borderColor: COLORS.navy, backgroundColor:'transparent', borderWidth:2, tension:0.3 },
      { label:'Applied', data: counts.map(c=>c.applied), borderColor: COLORS.green, backgroundColor:'transparent', borderWidth:2, tension:0.3 }
    ]},
    options: { responsive:true, maintainAspectRatio:false,
      plugins: { legend: { position:'bottom', labels:{ font:{ size:11 } } } },
      scales: { y: { beginAtZero:true, ticks:{ stepSize:1 } }, x: { ticks:{ font:{ size:10 } } } }
    }
  });
}

function renderGeoChart() {
  const ctx = document.getElementById('chart-geo');
  const buckets = {};
  lastNDays(30).filter(j => j.outcome === 'qualified').forEach(j => {
    const loc = (j.location_type || j.location || 'Unknown').toString();
    buckets[loc] = (buckets[loc] || 0) + 1;
  });
  const entries = Object.entries(buckets).sort((a,b) => b[1] - a[1]).slice(0, 8);
  if (window._cg) window._cg.destroy();
  window._cg = new Chart(ctx, {
    type: 'bar',
    data: { labels: entries.map(e => e[0]), datasets: [{ data: entries.map(e => e[1]), backgroundColor: COLORS.navy }] },
    options: { indexAxis:'y', responsive:true, maintainAspectRatio:false,
      plugins: { legend: { display:false } },
      scales: { x: { beginAtZero:true, ticks:{ stepSize:1 } } }
    }
  });
}

function renderSkillsChart() {
  const ctx = document.getElementById('chart-skills');
  const counts = {};
  lastNDays(30).filter(j => j.outcome === 'qualified').forEach(j => {
    (j.skills_mentioned || []).forEach(s => {
      const k = s.trim();
      if (k) counts[k] = (counts[k] || 0) + 1;
    });
  });
  const entries = Object.entries(counts).sort((a,b) => b[1] - a[1]).slice(0, 10);
  if (window._cs) window._cs.destroy();
  window._cs = new Chart(ctx, {
    type: 'bar',
    data: { labels: entries.map(e => e[0]), datasets: [{ data: entries.map(e => e[1]), backgroundColor: COLORS.yellow }] },
    options: { indexAxis:'y', responsive:true, maintainAspectRatio:false,
      plugins: { legend: { display:false } },
      scales: { x: { beginAtZero:true, ticks:{ stepSize:1 } } }
    }
  });
}

function renderPipeline() {
  const wrap = document.getElementById('pipeline-table-wrap');
  const pipeline = JOBS
    .filter(j => j.outcome === 'qualified')
    .filter(j => !(FEEDBACK[j.url] && ['applied','skipped'].includes(FEEDBACK[j.url].status)))
    .sort((a,b) => (b.score||0) - (a.score||0));
  if (!pipeline.length) {
    wrap.innerHTML = '<p style="color:var(--grey); padding:10px">No undecided jobs in the pipeline.</p>';
    return;
  }
  wrap.innerHTML = `<table><thead><tr>
    <th>Score</th><th>Company / Role</th><th>Location</th><th>Posted</th><th>Materials</th><th>Decision</th>
  </tr></thead><tbody>
  ${pipeline.map(j => {
    const fb = FEEDBACK[j.url] || {};
    const chip = (j.score||0) >= 85 ? 'chip chip-green' : 'chip chip-yellow';
    const savedCls = fb.status === 'saved' ? ' saved' : '';
    return `<tr>
      <td class="score"><span class="${chip}">${j.score||'-'}</span></td>
      <td><div><strong>${esc(j.company)}</strong></div><div class="truncate"><a class="apply-link" href="${esc(j.url)}" target="_blank">${esc(j.title||'')}</a></div></td>
      <td>${esc(j.location||'—')}</td>
      <td>${j.posted_date ? esc(j.posted_date) : '—'}</td>
      <td>${j.tailored_files ? `<a class="small-link" href="javascript:void(0)" onclick="presentFolder('${esc(j.tailored_files)}'); return false;">open folder</a>` : '—'} ${j.url ? `· <a class="small-link" href="${esc(j.url)}" target="_blank" rel="noopener noreferrer">view JD</a>` : ''}</td>
      <td>
        <button class="btn" onclick="setStatus('${esc(j.url)}', 'applied')">Applied</button>
        <button class="btn${savedCls}" onclick="setStatus('${esc(j.url)}', 'saved')">Save</button>
        <button class="btn" onclick="setStatus('${esc(j.url)}', 'skipped')">Skip</button>
      </td>
    </tr>`;
  }).join('')}
  </tbody></table>`;
}

function renderLog() {
  const wrap = document.getElementById('log-table-wrap');
  const items = JOBS
    .filter(j => (FEEDBACK[j.url]||{}).status === CURRENT_TAB)
    .sort((a,b) => new Date((FEEDBACK[b.url]||{}).timestamp||0) - new Date((FEEDBACK[a.url]||{}).timestamp||0));
  if (!items.length) {
    wrap.innerHTML = `<p style="color:var(--grey); padding:10px">No jobs marked <strong>${CURRENT_TAB}</strong> yet.</p>`;
    return;
  }
  wrap.innerHTML = `<table><thead><tr>
    <th>When</th><th>Company / Role</th><th>Location</th><th>Score</th><th>Source</th><th></th>
  </tr></thead><tbody>
  ${items.map(j => {
    const ts = (FEEDBACK[j.url]||{}).timestamp;
    return `<tr>
      <td>${ts ? new Date(ts).toLocaleDateString() : '—'}</td>
      <td><div><strong>${esc(j.company)}</strong></div><div class="truncate">${esc(j.title||'')}</div></td>
      <td>${esc(j.location||'—')}</td>
      <td class="score">${j.score||'—'}</td>
      <td><a class="small-link" href="${esc(j.url)}" target="_blank" rel="noopener noreferrer">view JD</a></td>
      <td><button class="btn" onclick="setStatus('${esc(j.url)}', 
```

# APPENDIX D — Scheduled task prompt content

```markdown
# Appendix D — Scheduled Task Prompt Template

Use this as the literal `prompt` field when calling `mcp__scheduled-tasks__create_scheduled_task` in Step 11 of the mega-prompt. Interpolate `{MOUNT}` (user's mounted folder path) and `{ARTIFACT_ID}` (the id returned from `create_artifact` in Step 12).

---

You are running {USER_FIRSTNAME}'s daily job-search workflow. Execute every step in order. Steps 5 and 6 are non-negotiable — the run is not complete until they finish.

# STEP 1 — Mount the working folders
Call `mcp__cowork__request_cowork_directory` with `path: "{MOUNT_PARENT}"`. Then call it again with `path: "{MOUNT}"` if the parent didn't cover the Job Bot subfolder. The bot needs write access to both `{MOUNT}/Job Bot/` and `{MOUNT}/daily job brief/` (or equivalent date-folder location).

# STEP 2 — Execute the playbook
Read and execute the full instructions in `{MOUNT}/Job Bot/config/daily_brief_prompt.md`. That file is the canonical playbook — follow every section in order. Use WebSearch + WebFetch as the primary research tools. Use python-docx (via bash) to generate .docx files with proper one-page-full formatting per the playbook's verification block.

# STEP 3 — Tailored materials
For each qualified job, write `<company>_jd.txt`, `<company>_score.md`, `<company>_cover_letter.docx`, and `<company>_resume_tailored.docx` into `{MOUNT}/daily job brief/YYYY-MM-DD/`. Verify the resume is one page AND fills ≥93% per the playbook before declaring the deliverable complete.

# STEP 4 — Persist the ledger
Append every JD examined today (qualified or dropped) as a single-line JSON record to `{MOUNT}/Job Bot/briefs/all_jobs.jsonl`. Schema in playbook §8b. Also write a per-date `seen_jobs.json` to today's date folder for dedupe.

# STEP 5 — Bake the dashboard (DO THIS EVERY RUN)
Run the bake script via bash:
```bash
python3 "{MOUNT}/Job Bot/dashboard/bake.py"
```
This reads `briefs/all_jobs.jsonl`, `briefs/feedback.json`, and `applications/applications.jsonl` and embeds them as a baked-data JSON block in `dashboard/dashboard.html`. The dashboard reads from this block on open, so the user sees fresh data without depending on a live disk read. Idempotent — re-running just replaces the previous baked block.

**Verify the bake worked:** read the first 5 lines of `dashboard/dashboard.html` and confirm the baked-data script tag contains today's `scored_date` entries. If it doesn't, the bake silently failed — investigate before moving to Step 6.

# STEP 6 — Update the persistent artifact (DO THIS EVERY RUN)
Call `mcp__cowork__update_artifact` with:
- `id: "{ARTIFACT_ID}"` — this is the single canonical artifact, NEVER `create_artifact` with a new id
- `html_path: "{MOUNT}/Job Bot/dashboard/dashboard.html"`
- `mcp_tools: ["mcp__workspace__bash", "mcp__cowork__present_files"]`
- `update_summary`: a one-line description of today's run (e.g., "May 18 run — 2 qualified, top match Slalom Senior Consultant at 87")

If `update_artifact` errors, do not declare the run complete. Diagnose and retry.

# STEP 7 — Chat summary
End the session with a one-paragraph summary: count of qualified jobs, top company + score if any, count of postings examined, count dropped on freshness vs fit. User opens the dashboard from the notification.

# Constraints
- Never fabricate JDs, posting dates, or company news
- Never click apply or submit on the user's behalf
- Never call `create_artifact` — there is exactly one persistent artifact and it gets updated, not recreated
- Cap runtime around 12 minutes

```

# APPENDIX E — Deep-tailor workbook content

```markdown
# Deep-Tailor Workbook

The workshop setup gets your Job Bot running with sensible defaults. This workbook takes the bot from "running" to "calibrated to you." Plan ~30 minutes total. You can do all eight sections at once or work through them across the week — the bot picks up your changes on the next morning run.

**How to use this:** Open this file. For each section, paste the block into Cowork as a chat message. Claude reads your answer and writes the change to the right config file. No coding required.

---

## Section 1 — Anti-keywords (5 min)

What roles should the bot NEVER surface, even if they score above 75? Common examples: roles requiring active TS/SCI clearance you don't hold, certain industries (gambling, tobacco, cannabis), or job titles you're done with (Sales Development Rep, recruiting agency roles).

**Paste this into Cowork:**

> Add these anti-keywords to my Job Bot's preferences.md. Any posting containing these words or phrases gets auto-dropped before scoring:
>
> [Your list, one per line. Examples:]
> - "Active Top Secret clearance"
> - "Cannabis"
> - "10+ years"
> - "Sales Development Representative"
> - "Recruitment agency"
>
> Add them to the existing anti-keywords section, don't replace what's there.

---

## Section 2 — Compensation floor (2 min)

What's your minimum acceptable base salary? Roles below this get dropped regardless of fit. Leave blank if you don't want to filter by comp.

**Paste this into Cowork:**

> Add a compensation floor to my Job Bot's preferences.md and update the scoring/drop logic in daily_brief_prompt.md:
>
> Minimum base salary: $[number]
>
> Drop any posting where `comp_low < [number]` AND the JD explicitly publishes a comp range. Don't drop based on inferred comp.

---

## Section 3 — Named network contacts (10 min)

This is the highest-leverage tuning. Tell the bot who you know at which target companies. The Network score (10 of 100 pts) goes to full credit for any company where you have a named contact — meaning roles at those companies become much more likely to qualify.

**Paste this into Cowork:**

> Add these named network contacts to my Job Bot's preferences.md under the Network signals section. For each, the bot should award full 10 Network points to any role at that company:
>
> [List one per line. Format: Company — Person — Relationship]
> Examples:
> - Wipfli — {Example Contact 1} — {USER_MBA_PROGRAM} MBA classmate, class of 2025
> - Slalom — {Example Contact 2} — Former coworker at Lockheed Martin
> - Anthropic — {Example Contact 3} — Met at AI Builders Meetup Denver, exchanged business cards
> - Deloitte — Anyone — {USER_MBA_PROGRAM} has 12 alumni at the firm per LinkedIn search
>
> Use "Anyone" when you just have an alumni / institutional connection without a specific person yet.

---

## Section 4 — Cover-letter voice (5 min)

The bot defaults to a tight, active-voice style. Tune it to sound like you.

**Paste this into Cowork:**

> Update the cover letter generation rules in my Job Bot's daily_brief_prompt.md. My preferred voice:
>
> - Tone: [pick one] Confident / Conversational / Warm-formal / Sharp / Academic
> - Opener style: [pick one] Lead with the angle / Lead with a concrete accomplishment / Lead with why this firm specifically
> - First-person frequency: [pick one] Heavy "I" / Balanced / Strip most "I"s
> - Hedging tolerance: [pick one] Zero hedging / Some hedging on speculative claims is fine
> - Ban list (add to my current ban list — leverage, robust, transformative, etc.):
>   - [Your additional words to ban]
>
> Generate one example cover letter using my preferred voice for a hypothetical [your target role title]. I'll review before locking it in.

---

## Section 5 — Score-rubric weight tuning (3 min)

Default weights: role keyword 35, experience 20, location 15, domain 10, skills 10, network 10. Rebalance if your situation is unusual (e.g., career switcher should down-weight experience; relocator should down-weight location).

**Paste this into Cowork:**

> Rebalance the match scoring rubric in my Job Bot's preferences.md. My new weights (must total 100):
>
> - Role keyword overlap: [number] pts
> - Experience fit: [number] pts
> - Location fit: [number] pts
> - Domain fit: [number] pts
> - Skill overlap: [number] pts
> - Network: [number] pts
>
> Keep the surface threshold at 75 and star threshold at 85.

---

## Section 6 — Industries to exclude (2 min)

Hard exclusions at the industry level. Different from anti-keywords — this drops roles based on the company, not the JD text.

**Paste this into Cowork:**

> Add these industries to my Job Bot's exclusion list in preferences.md. Any company whose primary industry matches gets auto-dropped:
>
> [Your list, one per line. Examples:]
> - Gambling / casinos
> - Tobacco
> - Cannabis
> - For-profit prisons
> - Multi-level marketing (MLM)
> - Recruiting agencies / staffing firms (unless explicitly target)
>
> When the bot encounters a company, it should look up the industry classification before scoring.

---

## Section 7 — Stepping-stone companies (3 min)

For these companies, the bot surfaces sub-75 roles (65–74) with a yellow "Stepping stone" badge instead of dropping. Use for high-value firms where you'd take a junior-tier role to get inside.

**Paste this into Cowork:**

> Add these to the Stepping-stone tier in my Job Bot's preferences.md. For each, sub-75 roles (65–74) should surface in the brief with a stepping-stone badge instead of being dropped:
>
> [Your list, one per line. Examples:]
> - Anthropic
> - OpenAI
> - McKinsey
> - BCG
> - [Your dream firm here]
>
> Anything below 65 still drops, even at these companies.

---

## Section 8 — Project ledger (10 min — the heaviest)

Replace the template entries in `master/projects.md` with your own. The bot uses this for the Selected Projects section in tailored resumes and the bridge paragraph in cover letters. Each project needs: name, dates, role, what you built, quantified outcomes, technologies, and `fits:` tags so the bot knows which JDs to surface it for.

**Paste this into Cowork:**

> Replace the template entries in my Job Bot's `master/projects.md` with these projects:
>
> [For each project, fill out:]
>
> ### [Project name]
> - Dates: [Start – End or Ongoing]
> - Role: [Your role on the project]
> - Built: [1-2 sentences on what you built]
> - Why it matters: [1 sentence on what it demonstrated]
> - Tech / methodology: [tools, frameworks, methods]
> - fits: [comma-separated tags matching the JD types the bot should surface this for, e.g., AI consulting, finance transformation, supply chain, GenAI]
> - Verify before use: [any numbers or claims that need confirmation before going on a resume]
>
> Repeat for 3–6 projects. Aim for a mix of professional, academic, and personal projects.

---

## After completing the workbook

Tell Claude in chat: "Re-run my Job Bot now with the updated config — I want to see how the new weights and contacts change today's scoring." The bot will re-score the current ledger entries and refresh the dashboard.

If you don't have time to complete all eight sections, prioritize in this order:
1. Section 8 — Project ledger (biggest scoring impact)
2. Section 3 — Named network contacts (10-pt boost on connected roles)
3. Section 1 — Anti-keywords (reduces noise immediately)
4. Section 4 — Cover-letter voice (raises quality of every deliverable)
5. Sections 2, 5, 6, 7 — tuning, can wait

Total time invested = ~30 min for a meaningfully more precise tool.

```

---

*End of setup prompt. Total ~6,000 words including appendices.*
