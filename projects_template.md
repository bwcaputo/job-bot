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
