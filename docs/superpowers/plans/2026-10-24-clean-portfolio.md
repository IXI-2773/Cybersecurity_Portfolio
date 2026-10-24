# Clean Portfolio Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans. The owner requested implementation and review by the assistant alone; do not delegate.

**Goal:** Implement the approved readable portfolio with an employer choice page and seven case-study destinations.

**Architecture:** Keep static HTML and existing evidence. A small shared stylesheet serves the new home, catalog and case pages; legacy routes and technical demos remain available.

**Tech Stack:** HTML, CSS, Python checks, native details/summary navigation.

**Spec:** `docs/superpowers/specs/2026-10-24-clean-portfolio-design.md`

## Global Constraints

- Public identity: Don Lopez; master resume remains unchanged and outside git.
- No new lab execution, forecasting accuracy or learning-outcome claims.
- CR and RAI remain private-implementation summaries.
- Certification engines are independent study tools; SCCDA stays planned.
- All choice links work without JavaScript; retain old routes.
- No merge or deployment in this pass.

## Review Focus

- Employers can navigate from home to each of seven case pages without scripts.
- The certification-engine case links both real study repos and distinguishes the browser demo.
- Resume download opens the correct one-page PDF without private identity or phone.
- Long headings, mobile navigation and evidence images fit at 320px and 390px.
- Synthetic outcomes and private architecture never appear as production security results.

### Task 1: Implement the approved presentation and navigation

**Files:** `index.html`, `explore.html`, `portfolio.css`, six selected project HTML pages, new `projects/certification-learning-engine.html`, `projects/certification-learning-engine.md`, `resumes/Don_Lopez_Cybersecurity_Resume.pdf`.

**Interfaces:** Home links to the catalog; catalog links to four security exercises and three engineering/software cases. Primary Resume links target the new PDF.

- [x] Update the existing evidence check to assert the approved navigation and evidence boundaries; run it and observe the missing-route failure.
- [x] Implement the home, choice page, one-column cases and public resume.
- [x] Update the case-study index and stale Splunk stage summaries without changing historical observations.

### Task 2: Verify the complete first pass

**Files:** `scripts/check_case_evidence.py`, `scripts/visual_review.py`, `scripts/build_site_bundle.py`, `.github/workflows/visual-review.yml`, `sitemap.xml`, `README.md`.

**Interfaces:** Reuse existing source/evidence checks; include the new stylesheet, case and PDF in the offline bundle.

- [x] Run evidence, semantics, local-link and bundle checks; require success.
- [x] Check desktop, 390px and 320px rendering together, including no-JavaScript navigation and the PDF. Fix findings in one bounded pass and confirm.
- [x] Review the whole diff myself, record results, commit, push the feature branch and open a draft PR. Keep main unchanged.
