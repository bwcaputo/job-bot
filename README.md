# Job Bot

A daily job search that runs in the Claude desktop app. Each weekday morning it checks your target companies' career sites for roles posted in the last 7 days, scores each one against your resume on a 100-point rubric, drafts a tailored one-page resume and a cover letter for the best matches, and refreshes a dashboard you open from Claude.

It doesn't apply for you. You review the drafts and submit on the company's site.

## What you need

- A paid Claude plan (Pro, Max, Team, or Enterprise). Scheduled tasks aren't on the free plan.
- The Claude desktop app, open on a computer that's awake when the run fires. A missed run fires once the app opens again.
- Claude Opus 5.5, selected for setup and for the scheduled task.
- Your resume (.docx or .pdf) and 20–60 target companies.

## Setup (about 10 minutes)

1. Open the Claude desktop app, start a new chat, and pick Claude Opus 5.5 in the model menu.
2. Open [`setup_prompt.md`](setup_prompt.md), click **Copy raw file**, and paste it into the chat.
3. Answer four questions, upload your resume, and paste your company list.
4. Connect a folder when Claude asks. Documents/Claude works well.
5. Claude builds your files, publishes your dashboard, schedules the daily run, and runs the first search.

**Set up in May?** Re-run setup and point it at the same folder. It keeps your ledger, resume, projects, and preferences, and sets up a new playbook, dashboard, and scheduled task. Delete the old task under Scheduled so two runs don't fire.

## Each morning

Open the dashboard. Each match shows its score, why it fits, and where its tailored resume and cover letter landed (`Job Bot/daily/YYYY-MM-DD/`). Mark it Applied, Save, or Skip. The next run picks up your marks: applied jobs move into the applications tracker, and skipped ones stay out of future briefs. With Gmail connected, the tracker also follows recruiter replies. When you're ready to apply, Claude in Chrome can work through Workday or Greenhouse forms with you.

## How matches are scored

| Dimension | Points |
|---|---|
| Role keyword overlap (title synonyms count) | 35 |
| Experience fit | 20 |
| Location fit | 15 |
| Domain fit | 10 |
| Skill overlap | 10 |
| Network (named contact, alumni, referral) | 10 |

You pick the floor at setup: 75 by default, 85 for strict, 65 for relaxed. Scores of 85 and up get a star. Two cases surface roles scoring 65 or more but under the floor: companies on your stepping-stone list, and companies where you have a named contact.

## What the bot holds to

- **Employer links only.** Apply links go to the company's careers site or its applicant tracking system (Workday, Greenhouse, Lever, Ashby, iCIMS). Job boards can help find a posting; they never become the link.
- **Fresh postings.** Posted within 7 days, with a date it can verify.
- **One full page.** Tailored resumes fit exactly one page and fill at least 93% of it. The run converts each one to PDF and measures.
- **Your facts.** Tailoring reorders and rephrases your master resume. Every number, title, and credential comes from it.
- **Three a day, at most.** A thin day stays thin.

## Tuning

Tell Claude what to change, or edit `Job Bot/config/preferences.md`. [`workbook_deep_tailor.md`](workbook_deep_tailor.md) walks through eight short tune-ups; the project ledger and network contacts move scores the most.

## Troubleshooting

- **No run this morning.** The app was closed or the computer was asleep. Scheduled in the Claude sidebar shows run history and has Run now.
- **Runs stop to ask for approval.** Run the task once from Scheduled and approve its tools, or turn on automatic approval in the task's settings.
- **Hitting usage limits on Pro.** Switch the scheduled task to Claude Sonnet 5.5 or trim the company list toward 20.
- **Dashboard marks don't reach the next run.** Your account doesn't offer artifact data storage yet, so marks stay in that browser. Tell Claude "mark Slalom applied" instead.

## What's in this repo

| File | Purpose |
|---|---|
| `setup_prompt.md` | The paste-and-go setup. Carries full copies of the files below as appendices. |
| `playbook_template.md` | What each daily run does: search, score, tailor, record, refresh the dashboard. |
| `scheduled_task_prompt.md` | The short prompt the scheduled task runs; it points at the playbook. |
| `preferences_template.md` | Targets, keywords, geography, scoring, and dealbreakers. |
| `projects_template.md` | Project ledger that feeds Selected Projects and the cover letter's bridge paragraph. |
| `cover_letter_template.md` | Cover letter structure and style rules. |
| `dashboard.html` | The dashboard. `bake.py` fills its data block. |
| `bake.py` | Embeds the ledger, feedback, and applications in `dashboard.html`. |
| `workbook_deep_tailor.md` | Optional 30-minute tuning workbook. |
| `build_setup_prompt.py` | Rebuilds the appendices in `setup_prompt.md` after you edit a source file. |

## Editing the templates

`setup_prompt.md` embeds the other files, so edit the source file, then run `python build_setup_prompt.py`. `python build_setup_prompt.py --check` exits non-zero when the prompt is out of date.

## License

MIT. See [LICENSE](LICENSE).

## Credits

Built by [Brian Caputo](https://github.com/bwcaputo) for his MBA cohort at the University of Denver, May 2026. Updated October 2026 for the merged Claude app and Claude Opus 5.5. Contributions welcome.
