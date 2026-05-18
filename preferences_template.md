# Job Search Preferences — {USER_NAME}

Edit this file anytime. The daily bot reads it on every run.

## Candidate snapshot
- {SHORT BIO — e.g., "Full-time MBA candidate, Class of 2027, concentrating in Strategy"}
- {YEARS OF EXPERIENCE — e.g., "8 years in operations management"}
- {CURRENT FOCUS — e.g., "Headed into AI consulting / management consulting"}
- {HOME CITY}, {STATE}. {REMOTE PREFERENCE — e.g., "Remote-US OK. No relocation."}

## Network signals
Bot uses these to award Network points (see scoring section). Expand as the search develops.

- {ALUMNI / INSTITUTIONAL NETWORK — e.g., "MBA program alumni at target firms"}
- {NAMED CONNECTIONS BY COMPANY}
- {AFFINITY GROUPS — e.g., "Veteran network", "Society of Women Engineers"}
- {MBA COHORT REFERRALS — log as you identify them}

## Target roles (ranked)
1. {PRIMARY ROLE TARGET — e.g., "AI consulting — Senior Consultant / Consultant / Associate"}
2. {SECONDARY ROLE TARGET}
3. {TERTIARY ROLE TARGET}

## Title synonym map
When matching JD titles against role keywords, the bot treats these as equivalents. Catches AI-startup naming conventions and Big 4 internal title variants.

- "AI Partner Lead" / "AI Partner" → AI consultant (Senior)
- "Member of Technical Staff" / "MTS" / "Founding Engineer" → Solutions Engineer / Forward-deployed
- "Customer Engineer" / "Field Engineer" / "Implementation Engineer" → Solutions Engineer
- "AI Transformation Consultant" / "GenAI Consultant" → AI consultant
- "Solutions Architect" / "Sales Engineer" (with AI/LLM JD content) → Forward-deployed engineer
- {ADD YOUR OWN MAPPINGS}

## Role keywords (used for search and matching)
- {ROLE KEYWORD FAMILY 1 — e.g., "AI consultant", "AI consulting", "applied AI"}
- {ROLE KEYWORD FAMILY 2 — e.g., "Senior Consultant", "Associate Consultant"}
- {ROLE KEYWORD FAMILY 3}

## Anti-keywords (filter out)
- "Software Engineer", "SDE", "DevOps", "SRE" — pure dev roles (unless target)
- Any "10+ years" or "Director / Principal / VP" minimums
- {ADD YOUR OWN}

## Target companies (focused search every run)

### {CATEGORY 1 — e.g., AI consulting}
- {COMPANY 1}
- {COMPANY 2}
- {COMPANY 3}

### {CATEGORY 2 — e.g., ERP consulting}
- {COMPANY 1}
- {COMPANY 2}

### {CATEGORY 3 — e.g., AI labs and major tech (relocation OK)}
- {COMPANY 1}
- {COMPANY 2}

Aim for 20–60 total. More than 60 strains the daily search budget (~30 WebSearch queries per run).

## Source rule (HARD)
Only company-owned career sites (or the company's hosted ATS subdomain — Workday/Greenhouse/iCIMS/Lever/Ashby/etc.) count as a primary source. Aggregators (LinkedIn, Indeed, Glassdoor, ZipRecruiter) are disqualified as apply links. Aggregators may be used only to discover a candidate URL or cross-check a posting date.

## Freshness rule (HARD)
Only postings dated within the last 7 calendar days qualify. If posting date can't be verified, skip the job.

## Geography rules
- {YOUR HOME CITY METRO}: yes
- Remote-US: yes
- Hybrid {YOUR HOME CITY}: yes
- On-site outside {YOUR HOME CITY} metro: {yes/no}
- Travel: up to {X}% acceptable for consulting roles

## Match scoring (0–100)
- 35 pts: role keyword overlap with title + JD (uses the title synonym map above)
- 20 pts: years-of-experience fit (penalize >7 yr minimums)
- 15 pts: location fit
- 10 pts: domain fit
- 10 pts: skill overlap
- 10 pts: network (named alumni / personal contact at the firm)

Surface threshold: 75. Star threshold: 85.

## Stepping-stone tier
For these companies, the bot surfaces sub-75 roles (65–74) with a yellow "Stepping stone" badge instead of dropping. Use for high-value firms where you'd take a junior-tier role to get inside.

- {DREAM COMPANY 1}
- {DREAM COMPANY 2}

## Auto-widen rule
Target ~3 qualified jobs per day. If fewer than 3 from the named target-company list hit the score floor on a given run, the bot may widen to companies NOT on the list, under these conditions:
- The resume-to-JD match still scores ≥ floor by the rubric (no exceptions, no padding)
- The role is in one of the target role categories above
- Source rule and freshness rule still apply
Never surface a sub-floor job. Quality over quantity remains the rule.

## Application etiquette rules
- Cover letter: 250 words max, active voice, no AI-tells
- Resume tailoring: reorder bullets to match JD priorities, swap keyword variants where honest, never fabricate
- Resume: one full page, ≥93% fill ratio (bot verifies via PDF conversion)

## Dealbreakers
- Roles requiring credentials you don't hold (CPA, active TS/SCI clearance, etc.)
- W-2 contract roles under 6 months
- Commission-only comp
- {YOUR DEALBREAKERS}
