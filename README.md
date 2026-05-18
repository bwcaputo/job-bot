# Job Bot

An automated daily job-search workflow built on Cowork scheduled tasks. Searches user-defined target companies every weekday morning, scores each posting against a master resume on a 100-point rubric, generates tailored cover letters and resumes for the top matches, and updates a persistent dashboard you can open from your Cowork sidebar.

## What it does

- Searches a list of 20–60 target companies every weekday at 7 AM
- Verifies each posting is on a company-owned career site (no LinkedIn / Indeed aggregators) and was posted within the last 7 days
- Scores each candidate role against your resume across six dimensions (role keyword overlap, experience fit, location fit, domain fit, skill overlap, named network)
- Generates a one-page-full tailored resume and a 250-word cover letter for each role that clears the score floor
- Logs every examined posting to a JSON ledger; the dashboard reads from that ledger
- Tracks application lifecycle (submitted, acknowledged, interviewing, rejected, offer) via optional Gmail scanning
- Refreshes a live dashboard artifact in your Cowork sidebar with KPIs, daily volume trend, location distribution, top JD skills, active pipeline, and applications tracker

## Human in the loop

The bot does not auto-apply. It handles discovery, scoring, and first-draft generation. Everything that requires judgment stays with you:

- Create the ATS / candidate profile on each company portal yourself
- Move the chat to [Claude in Chrome](https://claude.ai/chrome) when it's time to fill out Workday, Greenhouse, or Lever forms — the dashboard hands off, Claude in Chrome drives the form
- Review every tailored resume and cover letter before submission. For JDs with unusual asks, open the resume in Word and run another tailoring pass with Claude
- Hit Submit yourself

The bot surfaces and prepares. You apply.

## Setup — workshop / classroom path

This repo includes a paste-and-go setup prompt designed for non-technical users.

1. Open a fresh [Cowork](https://claude.ai/cowork) session
2. Open [`setup_prompt.md`](setup_prompt.md), copy the entire contents
3. Paste into the Cowork chat
4. Claude will interview you (5 questions, ~3 minutes), ask for your resume (upload as .docx or .pdf), and ask for your target company list (20–60 names, one per line)
5. Wait ~2 minutes for setup to finish
6. A persistent dashboard artifact appears in your sidebar
7. First scheduled run is the next weekday at 7:00 AM local time

## What's in this repo

| File | Purpose |
|---|---|
| `setup_prompt.md` | The 15-step paste-and-go prompt. Run-once to bootstrap a personal Job Bot. |
| `playbook_template.md` | The canonical daily playbook the scheduled task executes each morning. Parameterized — the setup prompt fills in your selectivity floor, mount path, and artifact ID. |
| `dashboard.html` | The persistent dashboard template. Empty baked-data block; `bake.py` fills it on every run. |
| `bake.py` | Reads `all_jobs.jsonl` + `applications.jsonl` + `feedback.json` and embeds them as a JSON script tag in `dashboard.html`. Idempotent. |
| `cover_letter_template.md` | The cover letter structure. Bracketed sections get replaced per role. |
| `preferences_template.md` | Where your target companies, role keywords, geo rules, scoring rubric, and dealbreakers live. |
| `projects_template.md` | Your project ledger. Bot reads this to populate the Selected Projects section in tailored resumes. |
| `workbook_deep_tailor.md` | Optional 30-minute post-setup tuning workbook. Eight sections: anti-keywords, comp floor, named contacts, cover-letter voice, rubric weight tuning, industries to exclude, stepping-stone companies, project ledger. |

## Match scoring (default)

| Dimension | Weight |
|---|---|
| Role keyword overlap | 35 |
| Experience fit | 20 |
| Location fit | 15 |
| Domain fit | 10 |
| Skill overlap | 10 |
| Network (named alumni / personal contact) | 10 |

Surface threshold: 75. Star threshold: 85. Anything below 75 drops, with two exceptions: a stepping-stone tier for high-value companies (65–74 surfaces with a yellow badge) and a network override (65–74 with a verified personal contact promotes to qualified).

## Hard rules (non-negotiable)

- **Source rule:** Apply links must point at the company's own career site. Aggregators are disqualified.
- **Freshness rule:** Postings must be dated within the last 7 days. If the date can't be verified, the role drops.
- **Page-fill rule:** Tailored resumes must be exactly one page AND fill ≥93% of the page. The bot converts to PDF and verifies programmatically.
- **Top 3, never padded.** If fewer than 3 roles qualify, the brief shows what qualifies. The bot will not fill slots to look generous.

## Architecture notes

- Built on Cowork scheduled tasks (cron-based, runs in isolated sessions)
- Uses `WebSearch` + `WebFetch` for posting discovery; `python-docx` via bash for resume generation; `pypdf` + `pdfplumber` for one-page verification
- Optional Gmail MCP integration for application-status tracking (rejection / acknowledgment / interview classification from inbox)
- Dashboard is a single self-contained HTML file with embedded CSS + JS, baked data injected as a `<script type="application/json">` tag
- No backend, no database — JSONL ledger is the source of truth

## License

MIT — see [LICENSE](LICENSE).

## Credits

Created by [Brian Caputo](https://github.com/bwcaputo) as a workshop project for an MBA cohort, May 2026. Contributions welcome.
