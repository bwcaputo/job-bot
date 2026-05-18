# Project Ledger

Canonical list of your active and recent projects. The daily job bot reads this file on every run and uses it as the source for the **Selected Projects** section in tailored resumes and the **bridge paragraph** in cover letters. The bot picks 1–3 projects per role based on JD relevance.

**How to update:** Edit this file directly, or tell Claude in chat: *"Add this project to my job bot memory: [details]."* New projects go at the top of the relevant section. Roll old or irrelevant projects to the **Archive** at the bottom (don't delete — past work still backs up the resume).

**Format per project:** name, dates, one-line summary, what was built, quantified outcomes, technologies, and `fits:` tags so the bot knows which JD types to surface it for.

---

## Active

### {Project name 1}
- **Dates:** {Start – End or Ongoing}
- **Role:** {Your role on the project}
- **Built:** {1-2 sentences on what you built}
- **Why it matters:** {1 sentence on what the work demonstrated}
- **Tech:** {Technologies / methodologies / tools}
- **fits:** {comma-separated tags matching the JD types the bot should surface this for, e.g., AI consulting, finance transformation, supply chain, GenAI}
- **Verify before use:** {any numbers or claims that need confirmation before going on a resume}

### {Project name 2}
- **Dates:**
- **Role:**
- **Built:**
- **Why it matters:**
- **Tech:**
- **fits:**

### {Project name 3 — optional}
- **Dates:**
- **Role:**
- **Built:**
- **Why it matters:**
- **Tech:**
- **fits:**

---

## Archive

*(Empty for now. Move projects here when they're 12+ months old or no longer relevant. Keep them in the file — past work backs up resume claims and gives the bot more raw material.)*

---

## Bot usage rules

When tailoring a resume for a specific JD:
1. Read this file in full.
2. **Skip any project tagged `exclude_from_outputs: true`.** These are internal tools or items you explicitly do not want surfaced. Never reference excluded projects in resumes, cover letters, the bridge paragraph, or any external deliverable — not even as a passing example.
3. Score each remaining Active project against the JD using the `fits:` tags and the project description.
4. Pick the top 1–3 by relevance. **Never include a project that doesn't fit the JD** — leave the Selected Projects section short or omit it entirely if no project applies.
5. **Never publish a TBD line.** If a project description has TBD content, either skip the project or use the surrounding context to write a clean version. Flag the gap in the daily brief so you can fill it in.
6. **Never fabricate.** If you don't have a verified number, don't invent one.

When drafting the cover-letter bridge paragraph:
1. Pick the single most JD-relevant project from this file.
2. Lead with what was built and the quantified outcome.
3. Keep it to two sentences max.

## Aim for

3–6 projects in Active. Mix of professional, academic, and personal projects. Each one needs a quantified outcome ("X% accuracy lift," "$Y savings," "Z customers onboarded"). Vague projects don't sell.
