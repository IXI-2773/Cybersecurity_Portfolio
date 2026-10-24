# Evidence-First Security Case Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish three newly completed reproducible investigations, upgrade the E3 case with real forensic evidence, add honest VM/CTF experience, and replace conceptual employer-facing imagery with evidence-backed visuals.

**Architecture:** Each executable case owns a deterministic fixture, standard-library Python analyzer, frozen JSON result, focused tests, README, and report. A shared SVG renderer consumes a small evidence-summary schema so employer visuals are derived from the checked result rather than composed independently. Static portfolio pages link directly to the underlying artifacts and distinguish current reproducible evidence from owner-confirmed prior experience.

**Tech Stack:** Python 3 standard library, static HTML/CSS/SVG, existing repository validation scripts and GitHub Actions.

**Spec:** `docs/superpowers/specs/2026-10-24-evidence-expansion-design.md`

## Global Constraints

- Preserve `resumes/Don_Lopez_Cybersecurity_Resume.pdf` and the private transcript unchanged and unpublished.
- No AI-generated image may be presented as evidence.
- `Actual lab screenshot` is reserved for the existing genuine Splunk capture; new analyzer-derived visuals use `Reproducible lab result`; third-party images use `Attributed reference image`; unsupported historical detail is not invented.
- Transcript data supports only degree, course, term, and honors facts; specific assignment and tool claims require separate owner confirmation or new reproducible evidence.
- All active work is local-only and deterministic; no public target may be scanned, tested, or exploited.
- Use Python's standard library only; do not add runtime dependencies.
- Keep the home page concise and put the complete catalog on `explore.html`.

## Review Focus

- Malformed or missing fixture fields must fail closed with a useful error instead of silently lowering finding counts; pinned in Tasks 2–5 tests.
- URLs and attack strings must be displayed defanged/escaped and must never become clickable attack targets; pinned in Tasks 2 and 4 tests.
- Re-running a case must reproduce the committed JSON and SVG byte-for-byte; pinned in Tasks 1–5 regeneration tests.
- Historical Necromancer/HackThisSite copy must not acquire exact flags, commands, scores, or dates absent first-party evidence; pinned in Task 6 evidence-contract tests.
- Mobile employer pages must not overflow when evidence labels, hashes, and timelines are long; pinned in Task 7 responsive review.

---

### Task 1: Evidence contract and shared visual renderer

**Files:**
- Create: `scripts/evidence_visuals.py`
- Create: `scripts/test_evidence_visuals.py`
- Modify: `scripts/check_case_evidence.py`
- Modify: `portfolio.css`

**Interfaces:**
- Consumes: JSON objects with `case_id: str`, `title: str`, `status: str`, `metrics: list[{label,value}]`, `timeline: list[{time,label,state}]`, and `findings: list[{id,label,severity}]`.
- Produces: `render_case_visual(data: dict) -> str`, a deterministic accessible SVG with escaped text and no scripts or external resources.

- [ ] **Step 1: Write failing renderer and portfolio-contract tests**

Assert schema rejection for missing keys, XML escaping for hostile text, deterministic bytes across two renders, readable SVG title/description, and new evidence-contract requirements for completed phishing, enterprise-account, web-log, forensic, and offensive-experience pages.

- [ ] **Step 2: Run tests and observe the expected failures**

Run: `python scripts/test_evidence_visuals.py && python scripts/check_case_evidence.py`

Expected: FAIL because the renderer and completed-case contracts do not exist.

- [ ] **Step 3: Implement the minimal shared renderer and evidence-panel CSS**

Add `validate_summary(data: dict) -> None`, `render_case_visual(data: dict) -> str`, and CLI `python scripts/evidence_visuals.py INPUT_JSON OUTPUT_SVG`. Add responsive `.evidence-console`, `.artifact-links`, and long-hash wrapping styles without changing the established visual identity.

- [ ] **Step 4: Run the focused renderer tests**

Run: `python scripts/test_evidence_visuals.py`

Expected: PASS.

- [ ] **Step 5: Commit**

Commit message: `feat: add deterministic evidence visual renderer`

### Task 2: Completed phishing-email investigation

**Files:**
- Create: `projects/05-phishing-email/sample_message.eml`
- Create: `projects/05-phishing-email/analyze_email.py`
- Create: `projects/05-phishing-email/test_email_analysis.py`
- Create: `projects/05-phishing-email/expected_analysis.json`
- Create: `projects/05-phishing-email/analysis.json`
- Create: `projects/05-phishing-email/evidence-summary.json`
- Create: `projects/05-phishing-email/CASE_REPORT.md`
- Create: `projects/05-phishing-email/README.md`
- Create: `assets/evidence/phishing-investigation.svg`
- Modify: `projects/phishing-investigation.html`
- Modify: `projects/phishing-investigation.md`

**Interfaces:**
- Consumes: a harmless RFC 5322 `.eml` containing controlled sender, Reply-To, Authentication-Results, Message-ID, and URL indicators.
- Produces: `analyze_message(path: Path) -> dict`, committed canonical `analysis.json`, and shared-renderer input `evidence-summary.json`.

- [ ] **Step 1: Write failing analysis tests**

Assert SHA-256 stability, sender/Reply-To domain mismatch, failed or absent authentication signals, one safely defanged URL, preserved Message-ID, no network requests, malformed-message rejection, and exact equality with `expected_analysis.json`.

- [ ] **Step 2: Run the focused test and observe failure**

Run: `python projects/05-phishing-email/test_email_analysis.py`

Expected: FAIL because the analyzer and fixture are absent.

- [ ] **Step 3: Implement and execute the analyzer**

Use `email`, `hashlib`, `html`, `re`, and `urllib.parse`; never resolve or request the extracted host. Generate `analysis.json`, convert its evidence summary with `scripts/evidence_visuals.py`, and write the report around observed evidence, interpretation, limitations, and recommended containment.

- [ ] **Step 4: Replace the planned page with the completed case**

Set `data-case-scope="completed-reproducible-lab"`; add the evidence visual, finding/timeline explanation, artifact links, IST 5250 academic foundation, and explicit lab-created-message scope.

- [ ] **Step 5: Verify reproducibility and commit**

Run: `python projects/05-phishing-email/test_email_analysis.py && python scripts/evidence_visuals.py projects/05-phishing-email/evidence-summary.json /tmp/phishing.svg && cmp /tmp/phishing.svg assets/evidence/phishing-investigation.svg`

Expected: PASS and byte-identical SVG.

Commit message: `feat: add reproducible phishing investigation`

### Task 3: Completed enterprise-account investigation

**Files:**
- Create: `projects/06-enterprise-account/account_events.csv`
- Create: `projects/06-enterprise-account/analyze_account.py`
- Create: `projects/06-enterprise-account/test_account_analysis.py`
- Create: `projects/06-enterprise-account/expected_analysis.json`
- Create: `projects/06-enterprise-account/analysis.json`
- Create: `projects/06-enterprise-account/evidence-summary.json`
- Create: `projects/06-enterprise-account/CASE_REPORT.md`
- Create: `projects/06-enterprise-account/README.md`
- Create: `assets/evidence/enterprise-account-investigation.svg`
- Modify: `projects/identity-mfa-investigation.html`
- Modify: `projects/identity-mfa-investigation.md`

**Interfaces:**
- Consumes: normalized CSV events with `timestamp_utc,event_id,account,source_ip,host,outcome,detail`.
- Produces: `analyze_events(path: Path) -> dict`, canonical timeline/finding JSON, and shared-renderer summary.

- [ ] **Step 1: Write failing account-analysis tests**

Assert a repeated-failure burst, subsequent successful sign-in, privileged group change, chronological ordering, alternative-explanation text, malformed timestamp/unknown-event rejection, exact expected JSON, and stable output.

- [ ] **Step 2: Run the focused test and observe failure**

Run: `python projects/06-enterprise-account/test_account_analysis.py`

Expected: FAIL because the implementation is absent.

- [ ] **Step 3: Implement, execute, and render the case**

Implement `load_events(path: Path) -> list[dict]` and `analyze_events(path: Path) -> dict` with UTC-aware parsing and deterministic rule IDs. Produce the report and SVG from the committed result.

- [ ] **Step 4: Convert the identity/MFA brief into the completed enterprise case**

Set `data-case-scope="completed-reproducible-lab"`; explain the event chain, evidence limits, containment, and its IST 4910/IST 5250 academic foundation.

- [ ] **Step 5: Verify and commit**

Run: `python projects/06-enterprise-account/test_account_analysis.py && python scripts/evidence_visuals.py projects/06-enterprise-account/evidence-summary.json /tmp/account.svg && cmp /tmp/account.svg assets/evidence/enterprise-account-investigation.svg`

Expected: PASS and byte-identical SVG.

Commit message: `feat: add enterprise account investigation`

### Task 4: Live local web attack-log investigation

**Files:**
- Create: `projects/04-local-vulnerability-assessment/run_request_lab.py`
- Create: `projects/04-local-vulnerability-assessment/analyze_access_log.py`
- Create: `projects/04-local-vulnerability-assessment/test_attack_log_lab.py`
- Create: `projects/04-local-vulnerability-assessment/request_manifest.json`
- Create: `projects/04-local-vulnerability-assessment/access.log`
- Create: `projects/04-local-vulnerability-assessment/attack_log_analysis.json`
- Create: `projects/04-local-vulnerability-assessment/evidence-summary.json`
- Create: `assets/evidence/web-attack-log-investigation.svg`
- Modify: `projects/04-local-vulnerability-assessment/CASE_REPORT.md`
- Modify: `projects/04-local-vulnerability-assessment/README.md`
- Modify: `projects/vulnerability-remediation.html`
- Modify: `projects/vulnerability-remediation.md`

**Interfaces:**
- Consumes: a fixed request manifest sent only to an ephemeral `127.0.0.1` HTTP server.
- Produces: `run_lab(manifest: Path, output: Path) -> None`, `analyze_log(path: Path) -> dict`, canonical log/result files, and shared-renderer summary.

- [ ] **Step 1: Write failing local-lab tests**

Assert the server binds to loopback, receives exactly the manifest requests, preserves benign and suspicious rows, detects traversal/SQL-injection/scanner patterns, defangs displayed strings, rejects non-loopback configuration, reproduces committed outputs, and leaves no server thread running.

- [ ] **Step 2: Run the focused test and observe failure**

Run: `python projects/04-local-vulnerability-assessment/test_attack_log_lab.py`

Expected: FAIL because the live request runner and analyzer are absent.

- [ ] **Step 3: Implement and execute the bounded lab**

Use `http.server`, `threading`, and `urllib.request`; bind to port `0` on `127.0.0.1`, normalize timestamps from the manifest, stop in `finally`, and write the committed access log and analysis.

- [ ] **Step 4: Upgrade the existing web-hardening case**

Add the new evidence visual and a request-to-finding narrative while preserving the existing before/after hardening evidence and IST 5930/IST 5250 foundation.

- [ ] **Step 5: Verify and commit**

Run: `python projects/04-local-vulnerability-assessment/test_vulnerability_lab.py && python projects/04-local-vulnerability-assessment/test_attack_log_lab.py`

Expected: PASS.

Commit message: `feat: add live local web attack log evidence`

### Task 5: Reproducible forensic evidence examination and E3 upgrade

**Files:**
- Create: `projects/07-forensic-evidence/build_evidence.py`
- Create: `projects/07-forensic-evidence/examine_evidence.py`
- Create: `projects/07-forensic-evidence/test_forensic_lab.py`
- Create: `projects/07-forensic-evidence/evidence-source/`
- Create: `projects/07-forensic-evidence/evidence-package.zip`
- Create: `projects/07-forensic-evidence/manifest.json`
- Create: `projects/07-forensic-evidence/examination.json`
- Create: `projects/07-forensic-evidence/evidence-summary.json`
- Create: `projects/07-forensic-evidence/CASE_REPORT.md`
- Create: `projects/07-forensic-evidence/README.md`
- Create: `assets/evidence/forensic-evidence-examination.svg`
- Modify: `projects/e3-digital-forensics.html`
- Modify: `projects/e3-digital-forensics.md`
- Modify: `visual-credits.html`

**Interfaces:**
- Consumes: a deterministic ZIP evidence package with fixed file content, paths, timestamps, and a SHA-256 acquisition manifest.
- Produces: `build_package(source: Path, output: Path) -> dict`, `examine_package(path: Path, expected_sha256: str) -> dict`, preserved original/working-copy hashes, inventory, timeline, finding references, and shared-renderer summary.

- [ ] **Step 1: Write failing forensic tests**

Assert deterministic package bytes, matching original/working-copy hashes, read-only analysis behavior, inventory/timeline ordering, tamper rejection before examination, path-traversal rejection, exact expected result, and stable SVG input.

- [ ] **Step 2: Run the focused test and observe failure**

Run: `python projects/07-forensic-evidence/test_forensic_lab.py`

Expected: FAIL because the package builder and examiner are absent.

- [ ] **Step 3: Implement and execute the forensic lab**

Use `zipfile`, `hashlib`, `json`, `tempfile`, and `pathlib`. Analyze only a verified working copy, cite every finding to an artifact path and timestamp, and preserve the build/examination manifests.

- [ ] **Step 4: Replace the E3 reference visual and rewrite the case**

Show the reproducible forensic result in the hero and home/explore cards. Present E3 as owner-confirmed classroom experience and the new evidence package as independent current work. Credit Chuck Easttom's fourth edition and link the official publisher page; apply collect/analyze/present, minimal original handling, analysis planning, and documented findings without reproducing the book.

- [ ] **Step 5: Verify and commit**

Run: `python projects/07-forensic-evidence/test_forensic_lab.py && python scripts/evidence_visuals.py projects/07-forensic-evidence/evidence-summary.json /tmp/forensic.svg && cmp /tmp/forensic.svg assets/evidence/forensic-evidence-examination.svg`

Expected: PASS and byte-identical SVG.

Commit message: `feat: publish reproducible forensic examination`

### Task 6: Offensive-security experience and employer navigation

**Files:**
- Create: `projects/offensive-security-vm-labs.html`
- Create: `projects/offensive-security-vm-labs.md`
- Modify: `index.html`
- Modify: `explore.html`
- Modify: `projects/CASE_STUDIES.md`
- Modify: `projects/PLANNED.md`
- Modify: `README.md`
- Modify: `sitemap.xml`
- Modify: `scripts/check_live_site.py`
- Modify: `scripts/check_case_evidence.py`

**Interfaces:**
- Consumes: completed case pages/artifacts from Tasks 2–5 plus owner-confirmed Kali/VM/Necromancer/HackThisSite experience.
- Produces: a complete no-JavaScript employer navigation path and accurate case-status catalog.

- [ ] **Step 1: Extend failing navigation and claim-boundary tests**

Assert the new page appears in the catalog, sitemap, and live target set; home detection/E3 cards use evidence assets; phishing and enterprise pages are no longer planned; the offensive page contains `Owner-confirmed prior training`, `Necromancer`, `HackThisSite`, `VMware`, and official references; reject exact flag/score/date/command claims and public-target instructions.

- [ ] **Step 2: Run the evidence check and observe failure**

Run: `python scripts/check_case_evidence.py`

Expected: FAIL on missing navigation and offensive page.

- [ ] **Step 3: Build the offensive experience page**

Use the existing attributed Kali reference image, describe the safe isolated workflow at a high level, cite the official VulnHub and HackThisSite pages, and state that original personal screenshots are unavailable without describing the experience as planned or fake.

- [ ] **Step 4: Integrate completed work across the portfolio**

Replace the home detection SVG with `splunk-native-dashboard-results.png`, replace all employer-facing E3 reference-photo uses with `forensic-evidence-examination.svg`, promote phishing and enterprise cases to completed work, and keep planned SOC automation separate.

- [ ] **Step 5: Run navigation/evidence checks and commit**

Run: `python scripts/check_case_evidence.py && python scripts/check_links.py && python scripts/check_accessibility.py`

Expected: PASS.

Commit message: `feat: integrate evidence-first security experience`

### Task 7: Full verification, visual review, and publication

**Files:**
- Modify only if the bounded visual review finds defects: `portfolio.css` and affected HTML.
- Preserve: `resumes/Don_Lopez_Cybersecurity_Resume.pdf`

**Interfaces:**
- Consumes: complete exact branch head from Tasks 1–6.
- Produces: reviewed PR, successful CI, merged exact head, and passing live-site receipt.

- [ ] **Step 1: Run every case test and the full static suite**

Run all `test_*.py` files under `projects/`, `python scripts/test_evidence_visuals.py`, `node scripts/test_browser_engine.cjs`, `node scripts/test_portfolio_systems.cjs`, `python scripts/check_case_evidence.py`, `python scripts/check_splunk_workflow.py`, `python scripts/verify_splunk_screenshot.py`, `python scripts/verify_network_visuals.py`, `python scripts/check_accessibility.py`, `python scripts/check_links.py`, `python scripts/check_live_site.py --self-test`, and `python scripts/build_site_bundle.py --output /tmp/portfolio-evidence-expansion.zip`.

Expected: all PASS; the bundle has ZIP integrity; the résumé SHA-256 matches the pre-change value.

- [ ] **Step 2: Open a draft PR for the exact tested head**

Push `codex/evidence-expansion-006`, create the PR against `main`, and record local test totals and evidence boundaries.

- [ ] **Step 3: Review CI desktop, mobile, and small-mobile captures once**

Inspect the home page and each changed case. Check long hashes, event timelines, visual labels, link hierarchy, and the 320px layout. If defects appear, fix them in one batch and run one confirmation capture.

- [ ] **Step 4: Merge the exact reviewed head and verify publication**

Require validation, responsive Chrome, Pages deployment, and live-site workflows to pass. Confirm every configured live target returns successfully before reporting completion.

- [ ] **Step 5: Preserve the implementation worktree**

Do not delete branches or worktrees automatically; retain them for follow-up evidence updates.
