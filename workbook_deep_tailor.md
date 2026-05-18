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
