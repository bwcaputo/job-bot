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

Tell Claude: "Re-run my Job Bot now with the updated settings." The run re-scores the last week's open postings against the new weights and contacts, then refreshes the dashboard.
