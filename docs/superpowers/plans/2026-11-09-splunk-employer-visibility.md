# Splunk Employer Visibility Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans for this single focused task.

**Goal:** Make the completed Splunk authentication investigation easy to find without adding homepage clutter.

**Architecture:** Retain the static site and existing visual styles. Move the existing triage feature to the first project position and align its directory and employer-overview summaries with the published case.

**Tech Stack:** HTML, existing CSS, Python standard-library navigation checks.

**Spec:** The user's approved employer-visibility slice, with the explicit requirement that the page remain appealing, simple and easy for an employer to scan.

## Global Constraints

- Keep three homepage project features; preserve the hero, palette, type, animation and unrelated content.
- Use the existing case at `projects/soc-triage-automation.html` and its `#report-excerpt` anchor.
- Describe 70 accepted events, zero rejected rows and six review candidates from synthetic lab data processed through Splunk; do not conflate candidates with scheduled alerts or confirmed incidents.
- Keep the earlier fixture report available within the case study.
- Preserve unrelated edits in the original checkout. This branch starts from `ef5452b985d5dc85b679270bf6ad2b9780a2e16b` in an already-isolated worktree.
- Run focused checks only. PR creation triggers broader CI and therefore needs a new user exception before publication.

## Review Focus

- The first homepage project is the completed investigation, with no fourth feature added.
- Each entry point offers a full investigation and a readable excerpt, not an unexpected raw-data download.
- The separate scheduled-alert case and historical fixture remain distinct and accessible.
- Long project names and both actions fit the desktop layout and have usable keyboard focus.
- Existing homepage navigation, qualifications and unrelated case links remain intact.

## Task 1: Clarify the three employer entry points

**Files:** `index.html`, `explore.html`, `recruiter.html`; add `scripts/test_splunk_employer_navigation.py`. Reuse `portfolio.css` without changes unless rendering proves a defect.

**Interfaces:** Consume the published case page and `report-excerpt` anchor. Produce static, keyboard-accessible links from all three entry points.

- [x] Add focused navigation checks for homepage ordering, both destinations from each entry, resolved local anchors, and retained case evidence paths.
- [x] Run `python -m unittest discover -s scripts -p test_splunk_employer_navigation.py -v`; observed four expected missing-link/order failures before implementation.
- [x] Replace the old fixture-first summary with the completed Splunk workflow and reorder only the homepage feature. Align related directory and employer summaries.
- [x] Run the new checks plus the existing presentation and nearby navigation checks; 17 tests passed (4 navigation, 7 presentation, 3 firewall navigation, 3 IAM navigation). Accessibility structure checks passed for the three modified pages.
- [x] Inspect desktop renders in one batch and confirm. Homepage verified at 1280 and 1440 pixels; employer overview and directory at 1440 pixels. No new assets, dependencies or live Splunk runs.
- [x] Obtain an independent diff review. No critical or important findings; removed one redundant generic-wrapper aria-label. Hand off the checked change without triggering broader CI.

## Execution Record

- Pre-flight: one task, no shared interfaces. The existing main-branch case and its retained evidence are reused without rerunning the lab.
- Implementation choice: retain the existing visual identity; make the evidence action open the readable excerpt, where the structured download remains available.
- Verification limit: screenshots and static structure/link checks, not a screen-reader or complete WCAG audit. Mobile redesign, external-link revalidation and lab re-execution were outside this slice; existing evidence was reused.
- Preview note: initial fragment-based headless captures were incomplete; unfragmented captures confirmed both affected views. No production CSS or JavaScript change was needed.
- Publication remains pending a one-time exception for the existing broad PR and post-merge workflows. No CI configuration was weakened or bypassed.
