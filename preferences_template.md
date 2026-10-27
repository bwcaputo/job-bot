# Job Search Preferences — {USER_NAME}

Every run reads this file. Edit it anytime, or tell Claude what to change.

## Candidate snapshot
- {One line, e.g. "Full-time MBA, Class of 2027, five years in supply chain operations"}
- Home base: {City, State}
- Contact line for cover letters: {email} | {phone} | {LinkedIn URL}

## Dashboard
- URL: {DASHBOARD_URL}
- Schedule: {e.g. Weekdays at 7:00 AM}

## Target function and roles
- Function: {e.g. Finance}
- Roles, in priority order: {e.g. FP&A, Strategic Finance, Corporate Development}

## Role keywords
Search phrases, 8–12, with common variants of each title.
- {e.g. "FP&A Manager", "Senior Financial Analyst", "Finance Business Partner"}

## Title synonym map
Titles that count as a match for the roles above.
- {e.g. "Finance Business Partner" → FP&A}
- {e.g. "Customer Engineer" / "Implementation Consultant" → Solutions Engineer}

## Anti-keywords
Postings containing these drop before scoring.
- {e.g. "10+ years", "Director", "Vice President"}
- {e.g. "Active TS/SCI clearance" unless you hold one}

## Target companies
One per line, 20–60 total. Add `also_search_as:` for alternate names. Runs record each company's careers site as `verified:` once they find it.
- {Company}
- {e.g. PwC (also_search_as: PricewaterhouseCoopers)}

## Stepping-stone tier
Companies where a role scoring 65 or more but under the surface threshold still shows up, with a yellow badge.
- None yet

## Network contacts
A named contact at a company earns full network points (10) on its roles. Format: Company — Person — Relationship.
- None yet

## Geography
- {Metro}: yes
- Remote-US: yes
- Hybrid {Metro}: yes
- On-site elsewhere: {yes/no}
- Travel: up to {X}%

## Scoring (0–100)
- 35: role keyword overlap with the title and description (title synonyms count)
- 20: experience fit (penalize minimums above 7 years)
- 15: location fit
- 10: domain fit
- 10: skill overlap
- 10: network (named contact, alumni at the firm, referral)

Surface threshold: {FLOOR}
Star threshold: 85

## Widening
Aim for about 3 qualified roles a day. When named targets come up short, runs may search beyond them; those roles meet the same threshold, source, and freshness rules.

## Source and freshness
- Apply links go to the employer's careers site or its applicant tracking system. Job boards only help find postings.
- Postings must be dated within the last 7 days.

## Writing rules
- Cover letter: 250 words max, active voice, specific to the posting.
- Resume: one full page (93% or more), tailored from the master resume, with every fact taken from it.

## Dealbreakers
- Credentials you don't hold (CPA, active clearance, and so on)
- W-2 contracts under 6 months
- Commission-only pay
- {Add your own}

## Compensation floor
- None set

## Industries to exclude
- None set
