# Authentication Export Employer Page Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans for this bounded presentation slice.

**Goal:** Put the approved skills-focused story into the existing SOC page and expose one verifiable, public-safe report excerpt.

**Architecture:** Keep the current static HTML/CSS layout. Project an allowlisted subset from the retained case, not a copy of its raw records. Display the 70-event result separately from the historical 20-row fixture walkthrough and the earlier scheduled-alert exercise.

**Tech Stack:** Static HTML, JSON, Python standard-library checks; existing portfolio CSS.

**Spec:** Approved slice-1 case-study draft in Cybersecurity-Projects commit `c2f53daccc458f0966f057fe273351e31e7b73e5`, `docs/employer-presentation/authentication-export-case-study.md`, and the user's approval to place it on the existing portfolio page.

## Global constraints

- No new Splunk query, replay, indexing, alert action or importer execution.
- No full-suite test, dependency installation or site-wide redesign.
- Synthetic lab scope remains explicit; candidates are not confirmed incidents.
- Preserve private originals and unrelated working changes.
- Reuse the existing page identity and support desktop employer browsing.

## Review focus

- A report link must not conflate the new 70-event run with the older fixture report.
- Public event references must resolve to the selected candidate's actual six records.
- Public data must contain no raw rows, private paths or original identity values.
- The excerpt must disclose its omitted records and display aliases.
- Counts, timestamps and provenance must agree between visible HTML and JSON.

### Task 1: Source-derived excerpt and scoped checks

Files: create `assets/evidence/soc-authentication-export-excerpt.json`; create `scripts/test_soc_export_presentation.py`.

Interface: summary fields `input_rows`, `accepted_events`, `duplicate_rows`, `rejected_rows`, `review_candidates`; one candidate with safe source references; six chronological events containing only UTC timestamp, event type and source references. Display aliases are explicit constants.

- [x] Write checks for projection privacy, provenance, sequence, source references, rendered rows and navigation.
- [x] Run only `python -B -m unittest discover -s scripts -p test_soc_export_presentation.py -v`; observe expected missing-artifact/page failures.
- [x] Verify retained case hash before projecting its first chronological authentication candidate; save only the allowlisted projection.

### Task 2: Existing case page

Files: modify `projects/soc-triage-automation.html` only; do not alter global CSS or other pages.

- [x] Lead with Splunk-to-case outcome and a skill-to-evidence summary.
- [x] Add one visible six-event excerpt with JSON download and explicit omissions/aliasing.
- [x] Keep the 20-row fixture report under a separate label and link to the separate scheduled-alert case.
- [x] Run the scoped checks; inspect desktop rendering and link targets, then one bounded correction pass if needed.
- [x] Obtain independent privacy/claims review.
- [ ] Publish through the existing reviewed-PR merge process after resolving the full-suite constraint below.

## Execution record — November 9, 2026

- Base: `277ac56874d2078a3571b7e8f49787ef32511ba6`. Isolated branch: `feat/splunk-case-evidence-20261109`; unrelated working changes were left untouched.
- Shared interface: the excerpt JSON's six event timestamps and source references are consumed by the static table and checked for equality.
- Source extraction was read-only, from the retained case after its SHA-256 matched the expected value. Only the allowlisted projection was saved for publication.
- Initial presentation checks: one pass and five expected missing-content failures. After implementation: six passes.
- The existing evidence checker also expects the historical fixture's `PARTIAL` scope. A new targeted check failed before that fixture-specific label was restored and passed after it; final focused result: **7/7 passed** in 0.025 seconds. No importer, Splunk run or full suite was rerun.
- Independent read-only review found no Critical, Important or Minor issues in the public content, privacy projection and source links. Private-source fidelity relied on the author's hash-verified extraction; production detection effectiveness is not claimed.
- Visual QA: the updated page and unchanged shared CSS were rendered in an isolated Edge preview at 1280 pixels wide. The complete desktop capture was inspected: readable heading, skill mapping, event table, distinct report links and scope disclosure; no visible overlap or clipping. This does not claim mobile or automated browser-metric verification.
- `git diff --check` passed. Local page links and anchors are covered by the focused checks; pinned code paths were independently checked against the source repository.
- Publication decision: the existing pull-request workflows launch repository-wide tests, additional analysis and browser checks. Opening a PR is held to respect the focused-only instruction. No checks were disabled, skipped or bypassed. A branch push alone does not match these workflows' push triggers; merge and live publication remain pending.
- Remaining next step: authorize the normal PR checks for this publication, or handle a separately scoped CI-efficiency change. No further evidence harvesting is needed for this page.
