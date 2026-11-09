# Cybersecurity portfolio benchmark and next development decisions

**Date:** 2026-10-23  
**Inspected release:** `25807b908b08dadb848ad4cbb7ae29f16008b19f` (PR #1 merged into `main`)  
**Objective:** improve recruiter comprehension, technical credibility, and visual polish without overstating what public evidence establishes.

## Method and limitations

Compared the public-facing content and/or source README of six real portfolios on 2026-10-23. These are **qualitative, feature-level comparisons**, not controlled hiring experiments, Lighthouse results, employer endorsements, market rankings, or verification of competitors' self-reported experience.

Inspected our own homepage, role paths, project explorer, case studies, printable recruiter page, live-check workflow and CSS from the exact merged GitHub source tree. GitHub Pages deployment and a post-merge fixed-origin live HTTP check succeeded against the merge commit. This study does **not** claim measured visitor conversion, search ranking, load times, or complete accessibility.

## External portfolios — what is worth borrowing

| Reference | Directly observable approach | Applicable lesson for this portfolio | Do not copy |
| --- | --- | --- | --- |
| [Samuel Mendieta](https://samuelmendieta.com/) | Immediate Security Engineer identity, direct project/story actions, interactive terminal narrative, self-described achievements and a contact destination | Make **role identity and project proof instantly recognizable**; an optional, genuinely useful interactive narrative can be distinctive | Unverified professional impact statistics, playful interaction that obstructs recruiting, invented work history |
| [Eren Ergen](https://erenergen.com/) | Compact certification and technical-arsenal groupings (SOC/SIEM, endpoint, network, web) | Make validated skills and evidence domains browsable at a glance | Calling holder-reported credentials issuer-verified without proof |
| [Anish Kumar Vedant](https://anishvedant.github.io/Portfolio/) | Detailed security-job positioning, enterprise-tool families, cloud/identity/detection projects and career context | Expose which security domains are **actually demonstrated**; prioritize a future validated cloud/identity/IR exercise if the goal is broader security engineering roles | Reusing another person's enterprise scale, work claims, tooling or credentials |
| [Jamie Christian II portfolio](https://github.com/JamieChristian22/cybersecurity-analyst-portfolio) | End-to-end simulated enterprise-security capstone with detection, response, controls and executive reporting | Build one **source-connected synthetic incident/capstone** that demonstrates how our four public labs inform an analyst decision—*only once executed and tested* | Rebranding disconnected labs as a tested integrated response before that integration exists |
| [Massimo Romeo](https://github.com/MassimoRomeo/cybersecurity-portfolio) | Public blue-team investigation writeups that include phishing, web logs, malicious documents and packet evidence | A future genuine phishing or incident-response investigation would diversify analyst evidence more than extra decorative pages | Padding a portfolio with unexecuted tasks or generic walkthroughs |
| [Brittany Chiang](https://brittanychiang.com/) | Curated selected projects, concise role statement, accessible navigation, visible résumé and writing | Keep a **curated three-to-four-project hiring view**; move deep technical pages behind clear links; use writing for substantive analysis, not filler | Copying visual branding or fabricating publications |

These competitors have very different career histories and audiences; **portfolio presentation** can be benchmarked independently of their experience depth. Some published claims are self-reported and were not independently verified.

### UX and publishing principles used for evaluation

- [W3C WAI page structure](https://www.w3.org/WAI/tutorials/page-structure/) and [headings](https://www.w3.org/WAI/tutorials/page-structure/headings/): logical headings and landmarks reduce navigation difficulty.
- [W3C clear page structure](https://www.w3.org/WAI/WCAG2/supplemental/patterns/o2p03-page-structure/): avoid dense text and excessive visual indicators; differentiate sections.
- [Google Search: title links](https://developers.google.com/search/docs/appearance/title-link) and [meta descriptions](https://developers.google.com/search/docs/appearance/snippet): specific, credible page summaries, not keyword stuffing.

## What is already distinctive in the merged portfolio

1. Four documented public Python defensive labs, with **76 focused tests** and a browser-friendly evidence trail; controlled inputs and failed/negative controls are disclosed.
2. A genuine, screenshot-reviewed Splunk one-panel result for frozen authentication training data. The scope explicitly excludes claims of live alerts, production incidents and verified indexing.
3. Two *independently authored* public browser teaching engines, nine baseline checks and a downloadable computed receipt. They are separate from private CR/RAI work.
4. A role-focused route page, project search/filter controls, an evidence review directory and two ATS résumé text options.
5. A printable recruiter profile that passed Chrome's US-letter one-page output checks; responsive screenshots, keyboard navigation, broken-link and source-claim checks are in CI.

Do **not** downgrade these into generic stock illustrations or pretend that all six case studies are equally independently executable: CR/RAI are architectural summaries.

## Specific current gaps and supporting observations

| Gap | Observed in merged source | Effect or risk | Status of claim |
| --- | --- | --- | --- |
| Role is not in the main `h1` | Homepage headline is “Find the signal. Follow the evidence.” while “SOC analysis” sits in the paragraph | Recruiter may need extra reading to determine job fit | Source-backed UX hypothesis, not user-tested |
| Dense homepage with several overlapping routing surfaces | Hero actions, proof band, three hiring routes, Splunk feature, separate replay, four lab cards, two CR/RAI cards, method, bio and contact | Competing requests for attention may reduce scan efficiency | Structure observed; impact unmeasured |
| Inconsistent prominence of real versus generated visual evidence | Home shows an actual Splunk screenshot plus generated diagrams; cases vary in visible proof formats | Reviewer may not instantly know which image is real evidence | Source-backed presentation opportunity |
| Limited cross-domain security narrative | Four independent controlled investigations are shown as separate labs | No independently verified capstone demonstrates end-to-end triage-to-remediation links | Concrete evidence gap |
| Limited breadth in public runnable labs | No current public verified phishing/IR or cloud IAM lab within the four defensive exercises | Competition for broader analyst/cloud roles depends on evidence beyond these four | Specific to portfolio, not an employability judgment |
| Style-rule accumulation | `styles.css` has **115,968 UTF-8 text characters** and roughly **937 simple rule-block starts** by a rough source scan; some selectors are repeated across media queries and upgrades | Harder to maintain safely; potential unused CSS | Size/source finding, **not** a measured render or Lighthouse slowdown |
| Link previews / share previews | Homepage defines `og:title`, `og:description` and Twitter summary but no `og:image` | Social cards may lack a designed preview | Metadata observed; platform result not tested |
| Independent credentials | Site explicitly labels Security+ and CySA+ holder-reported until verification | Do not promote issuer badge or dates without evidence | Correct existing honesty boundary |

## Prioritized development queue

### P0 — next implementation PR: hiring clarity and proof priority

1. **Rework only the top hiring viewport:** visible “SOC Analyst / Security Analyst” positioning in the `h1` or near-identical title hierarchy, one primary “Investigations” action and one résumé/profile action. Keep the distinctive evidence-first tone as a subtitle. Don't invent job titles or full-time experience.
2. **Curate the first project pass:** lead with authentication/Splunk, Windows triage and network traffic; keep vulnerability and CR/RAI available, but reduce duplicate invitations to visit the same section.
3. **Standardize a “Claim → Evidence → Limit” compact visible first fold** across the three most recruitment-relevant case pages, prioritizing the genuine Splunk screenshot, controlled event/log excerpts, and source citations. No screenshot or output may be misrepresented as live telemetry.
4. **Focused usability assertions:** actual Chrome at 320/390/1280; first-screen role + primary CTA discoverable, correct visible evidence labels, keyboard focus and no horizontal overflow. Run the existing targeted CI; do not add a costly general-purpose test suite.

**Completion criteria:** screenshots show job fit and best public proof without scrolling through unrelated sections; three sample recruiter tasks (“find Splunk proof”, “download SOC résumé”, “open a lab source”) have short, explicit paths; scope caveats remain adjacent to claims; no regression to the currently observed cases.

### P1 — engineering-quality and accessibility pass

5. Consolidate CSS by component/source section and remove truly superseded rules **only with screenshot comparison**; record before/after stylesheet bytes, computed visual diffs, and focus checks. Do not claim speed wins from file size alone.
6. Test browser zoom, contrast and focus in representative pages with actual computed browser styles. Add a modest, page-scoped regression check; describe remaining human screen-reader validation honestly.
7. Produce a *purpose-built* social sharing image using existing authorized illustration or genuine sanitized evidence; test card previews before adding `og:image`.
8. Make case-study decision summaries and source links consistently visible (with different treatment for public labs versus private CR/RAI design summaries).

### P2 — new verified capabilities, not artificial breadth

9. Design **one synthetic end-to-end analyst capstone** that connects existing fixture families and demonstrates a triage timeline, evidence links, disposition and follow-up actions. Keep its synthetic nature obvious; execute all joins/claims and add small deterministic tests before publication.
10. Then choose **one** new practical lab with greatest role payoff: phishing-email triage / documented IR OR cloud IAM / identity exposure, depending on verified execution resources. Do not create screenshots, statistics or résumé claims before real completion.
11. Consider a compact “Engineering notes” section only after there are at least two original, sourced technical articles worth publishing (e.g., time-boundary logic and evidence attribution). Avoid a placeholder blog.

## What not to do

- No fabricated SIEM ingestion, real attack/incident, threat intelligence, production network, company employment or credentials.
- No needless new page count: use the 16 current pages and make their paths clearer.
- No full rewrite to React/WebGL, no RPG or heavy terminal animation just to look sophisticated; the existing static site is inspectable and accessible.
- Do not equate a larger lab count, self-reported claims, or flashy effects with higher job eligibility.
- No direct edits to `main` without code review; the merged release stays stable. Next design work belongs in a separate PR.

## Practical sequence

**Next:** implement P0 first on a new feature branch, then compare fresh viewport screenshots to merged baseline `25807b9`; verify source labels and only merge after exact-head CI. P1 is a separate refactoring pass. New labs and integrated capstones start only after authoring and executing real controlled inputs.

**Confidence:** high for source-inventory counts and observed content, medium for likely UX improvements, **unknown** for recruiting impact or performance until measured.
