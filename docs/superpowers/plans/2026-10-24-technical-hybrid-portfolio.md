# Technical Hybrid Portfolio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace shallow diagrams with inspectable technical walkthroughs while retaining genuine images and completed cybersecurity experience.

**Architecture:** Retain the static site. Generate public replay data from the canonical authentication corpus, use pure decision functions for deterministic inspectors, and share only playback behavior between local components. Keep independent CR/RAI example fixtures separate from their private implementations and from security evidence.

**Tech Stack:** HTML, CSS, SVG, plain JavaScript, Python fixture generation, Node built-in assertions; no new runtime dependencies.

**Spec:** `docs/superpowers/specs/2026-10-24-technical-hybrid-portfolio-design.md`

## Global Constraints

- Preserve the white, charcoal, and forest-green visual identity; retain the dark green Signal to Case panel.
- Show genuine captures and explanatory animations together.
- No invented original lab screenshots, event sets, exploit outcomes, production incidents, accuracy, or employment claims.
- Use static HTML/CSS/plain JavaScript; no framework, new runtime dependency, live service, external API, private-source publication, or backend change.
- Preserve existing demo APIs and compatibility anchors.
- Do not alter either résumé PDF or expose the transcript.
- Pause offscreen and when the document is hidden; do not unexpectedly restart.
- Without JavaScript, show a complete representative state, captions, code excerpts, and normal links.

## Review Focus

- A failure exactly 600 seconds old must be included; 601 seconds must be excluded (Task 1).
- Different username/source-IP streams and intervening successes must not leak into one finding (Task 1).
- Invalid dates, future observations, and conflicting tied latest vintages must not enter a CR dataset (Task 2).
- Different measurement scopes must not be called consensus or a resolved contradiction (Task 2).
- Mobile, keyboard, hidden/offscreen, reduced-motion, and no-JavaScript visitors retain the evidence and controls they can use (Task 3).

---

### Task 1: Fixture-backed detection laboratory and Signal to Case

**Files:**
- Create: `scripts/build_technical_fixture.py`, `assets/js/technical-fixtures.js`, `assets/js/detection-lab.js`, `assets/js/portfolio-replay.js`, `scripts/test_detection_lab.cjs`, `scripts/test_technical_fixture.py`.
- Modify: `projects/detection-engineering.html`, `assets/js/signal-display.js`, `index.html`, `portfolio.css`.
- Read: `projects/01-authentication-detection/validation_events.csv`, `expected_findings.json`, `detect_auth.py`, `SPLUNK_MATRIX_BOUNDARY_RETEST.spl`, `splunk_workflow/NATIVE_DASHBOARD_RESULT_2026-10-23.md`.

**Interfaces:**
- Generator: `build_fixture() -> dict` produces canonical event IDs, parsed UTC milliseconds, exact SPL excerpt, source links, source SHA-256, and frozen expected findings. CLI `--check` compares generated JS bytes and exits nonzero on drift.
- Data export: `PortfolioTechnicalFixtures.authentication = {events, expectedFindings, sourceHash, splExcerpt, sources}`; export via CommonJS as well as browser global.
- Detector: `evaluateAuthentication(events, {windowSeconds = 600, threshold = 5} = {}) -> {findings, decisions}`. Each success decision names contributing event IDs and inclusion/exclusion reasons. Throw for malformed required fields or nonfinite time; do not silently drop invalid data. Inputs remain unmodified; stable chronological sorting preserves input order on ties.
- Replay: `createReplay({count, intervalMs, onChange}) -> {play, pause, step, reset, select, dispose}`. `onChange(index, running)` reports state. Start at zero paused; finish at `count - 1`; manual selection pauses. Controller owns timers, reduced motion, visibility, and optional element visibility observation.
- Both the rule workbench and homepage replay consume this one fixture and evaluator. The homepage exposes no separate invented incident result.

- [ ] **Step 1: Write focused failing behavior tests.** In `scripts/test_detection_lab.cjs`, assert the canonical replay produces exactly the frozen finding identities/counts; 600 is included and 601 excluded; another username or IP cannot contribute; every success resets its stream; interleaved streams stay independent. Assert invalid data throws, ties are deterministic, and evaluation does not mutate input. In `scripts/test_technical_fixture.py`, compare generator events and expected findings to canonical files and ensure stale output fails `--check`.
- [ ] **Step 2: Run the new tests and confirm failure because the implementations are missing.** `node scripts/test_detection_lab.cjs`; `python -m unittest discover -s scripts -p 'test_technical_fixture.py'`.
- [ ] **Step 3: Implement the interfaces and generate the fixture.** Source excerpts must come from committed files. Keep the historical 3/5→5/5 observation separate from current browser evaluation. Do not recreate a purported Splunk execution in JavaScript.
- [ ] **Step 4: Implement the actual interface.** Timeline, scenario selector, selected event inspector, required-fields explanation, SPL/Python source links, validation comparison, tuning/limitations, and the four-stage Signal to Case replay. Use the exact default/counterexample dispositions from the spec. Keep original detection experience and public fixture scope readable. Link Windows, network, phishing, account/MFA, and forensic cases where relevant without merging their evidence.
- [ ] **Step 5: Run focused proof.** `python scripts/build_technical_fixture.py --check`; new Node/Python tests; `python projects/01-authentication-detection/validate_matrix.py`; `python scripts/check_case_evidence.py`; `python scripts/check_links.py` must pass. Run replay timer/state tests with a small injected scheduler or deterministic fake timer environment; verify no double timers and pause-at-end.
- [ ] **Step 6: Commit the completed detection/replay slice.** `git add` only named task files; commit as `feat: add inspectable authentication rule replay`.

### Task 2: Point-in-time and claim/evidence inspectors

**Files:**
- Create: `assets/js/research-workbenches.js`, `assets/js/research-fixtures.js`, `scripts/test_research_workbenches.cjs`.
- Modify: `projects/celestial-resonance.html`, `projects/research-ai-infrastructure.html`, `index.html`, `portfolio.css`.
- Preserve: `assets/js/portfolio-systems.js`, `scripts/test_portfolio_systems.cjs`.

**Interfaces:**
- `resolveVintage(records, decisionTime) -> {state, selectedId, exclusions}`: state is `selected`, `unavailable`, `ambiguous`, or `invalid`. Validate the complete candidate set; malformed dates/IDs produce `invalid`. Both observation and availability must be no later than cutoff. Among time-eligible records of the same indicator, select latest `available_at`; conflicting tied latest records produce `ambiguous` with no selection. Older eligible records are `superseded`. Duplicate IDs are invalid.
- `traceClaim(scenario) -> {state, passageIds, explanation}`: fixture state is `supported`, `conflict`, `missing`, `attribution`, or `not-comparable`; all passage IDs resolve to actual passages in that fixture. Missing citation coverage and invalid attribution prevent support. Comparability comes before agreement. The function evaluates authored structured records, not arbitrary prose.
- `PortfolioResearchFixtures = {versions, claims, sourceHash}` contains independent fictional examples, explicit scope/date fields, exact short passages, and fixture hash provenance. Use local generation or canonical fixture bytes to compute the hash, not hand-entered provenance.
- Shared playback uses Task 1's `createReplay`; existing `evaluateCR/evaluateRAI` exports retain old behavior.

- [ ] **Step 1: Write failing tests.** CR: exact-cutoff acceptance; both time constraints enforced; latest eligible revision selected; pre-release excluded; previous version retained in input; malformed dates and duplicate IDs invalid; conflicting latest ties held; older eligible versions superseded. RAI: support, true comparable conflict, missing coverage, bad passage attribution, scope mismatch, and date-period mismatch; assert different scopes cannot yield support or resolved consensus.
- [ ] **Step 2: Run `node scripts/test_research_workbenches.cjs` and confirm missing implementation failure.**
- [ ] **Step 3: Implement pure functions and fixtures.** Add two-lane CR timeline, record/exclusion inspector, canonical fixture receipt, claim/evidence graph, exact passage inspector, and answer-change explanation. Use short authored public passages, not private source extracts. Neither component makes network calls or runs a model/forecast.
- [ ] **Step 4: Rewrite supporting explanations and homepage previews.** Retain CR acquisition/preservation/normalization/reproducibility story and RAI retrieval/provenance/contradiction/bounded-tools story. Keep private implementation claims distinct from public examples. Preserve `#cr-demo-title` and `#rai-demo-title` anchors even when the displayed headings change.
- [ ] **Step 5: Run new tests plus `node scripts/test_portfolio_systems.cjs`, `python scripts/check_accessibility.py`, and `python scripts/check_links.py`.** No regression in existing exports or routes.
- [ ] **Step 6: Commit as `feat: add research lineage and evidence inspectors`.**

### Task 3: Genuine images, responsive interaction, and release proof

**Files:**
- Modify: `index.html`, `projects/detection-engineering.html`, `portfolio.css`, `visual-credits.html` only if credits change, `scripts/check_case_evidence.py`, `.github/workflows/validate.yml`.
- Create: `scripts/test_technical_workbenches_browser.py` for the bounded target routes using the existing Selenium convention.
- Retain: existing images in the spec's inventory; `education.html`; VM/network/phishing/account/web/forensic cases; source fixtures; both résumé PDFs.

**Interfaces:**
- Browser check targets only homepage, detection engineering, CR, and RAI at 1280px and 390px; add 320px overflow assertions. Reuse existing browser tooling rather than adding a framework.
- The visible image gallery uses ordinary `<figure>`, `<img>`, `<figcaption>`, and full-size image links; scope captions match the spec's inventory. Controls are native buttons/selects with visible focus; the static state remains readable without JS.
- CI runs generated-fixture freshness plus the two new Node behavior suites and Python fixture tests alongside existing checks. Browser checks run in the existing visual-review workflow/environment where available.

- [ ] **Step 1: Add focused browser assertions.** Keyboard-select an event and inspect reasons; change CR cutoff and inspect exclusions; select a RAI passage and inspect exact source; play/step/reset and pause when hidden/offscreen; reduced-motion mode has no travelling animation but still supports selection/step. With JS disabled, all case/source/image links and a representative explanation are visible. Assert all images load, screenshots open full-size, and document width does not overflow at target widths.
- [ ] **Step 2: Integrate the genuine image strip.** Retain the real Splunk capture near detection analysis rather than replacing it with animation. Preserve campus gallery and captioned Kali reference. Keep reproducible visuals distinct from screenshots. Preserve the forensic textbook reference and completed VM/network experience. Never create placeholder “original” captures.
- [ ] **Step 3: Wire CI and run the changed behavior tests.** Add fixture freshness, detector tests, and research tests to `validate.yml`. Run `python scripts/check_case_evidence.py`, `python scripts/check_accessibility.py`, `python scripts/check_links.py`, and `python scripts/verify_splunk_screenshot.py`. Existing security lab engines are unchanged; do not repeatedly rerun unrelated suites unless an actual regression requires it.
- [ ] **Step 4: Inspect desktop/mobile renders in one batch.** Include default and selected inspector states, a held CR state, a RAI scope mismatch, genuine image loading, keyboard focus, and no-JS fallback. Batch material fixes and confirm once. Report browser verification unavailable if the runtime lacks a working browser; do not represent static checks as visual verification.
- [ ] **Step 5: Obtain one bounded whole-change review, then commit as `feat: retain genuine evidence across technical portfolio views`.** Review truthfulness, fixture correspondence, timers, accessibility, and mobile readability; fix material defects only. Record verification results and remaining image availability limits.
- [ ] **Step 6: Open/update a reviewable PR with the exact tested head.** Do not claim the deployed site changed until integration and GitHub Pages deployment are verified. Preserve the repository's normal integration workflow and user authorization boundary.

## Execution handoff

The earlier portfolio spec uses the same assistant for implementation. Recommend native execution for this small static site: shared fixture and replay interfaces make a single implementation context economical. Review this detailed plan before implementation; the selected hybrid concept is already settled and does not need to be chosen again.
