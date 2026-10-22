# Interview Evidence Brief — Don Lopez

**Audience:** SOC Analyst, junior Security Analyst, Detection Engineering and Security Automation interviewers  
**Positioning:** B.S. Cybersecurity (2024); CompTIA Security+ and CySA+ **reported by holder**, public verification pending. The four public security labs are **synthetic portfolio exercises**, not paid SOC incident experience.

## 45-second introduction

I built four independently reproducible defensive-security exercises covering authentication correlation, Windows process telemetry, network packet analysis and localhost HTTP hardening. Each includes source, tests, evidence boundaries and a case report. The design focus is to avoid escalating a rule match into a claim of compromise without corroboration. I also document test/regression engineering and authority boundaries from separate private software projects.

## Three evidence-backed interview stories

### Story 1 — Authentication triage and a corrected detection bug

**Question:** What do you do after failed logins followed by a success?

**Evidence:** [16-row synthetic timeline](../projects/01-authentication-detection/auth_events.csv), [LAB-AUTH-001](../projects/01-authentication-detection/SOC_CASE_REPORT.md), [31 focused tests](../projects/01-authentication-detection/test_detect_auth.py).

**What changed:** An early implementation incorrectly preserved failures across non-alerting successful logins. Now **every success resets the streak**, and negative tests cover the regression. The sample shows six failures and success for `alice` at 09:06 UTC, while below-threshold and unrelated-identity sequences do not alert.

**Decision:** Request actual MFA and session corroboration; no account compromise is claimed from fabricated data.

### Story 2 — Windows 4688 endpoint command-line triage

**Question:** Can a PowerShell encoded-command flag prove malicious behavior?

**Evidence:** [LAB-PROC-001](../projects/02-windows-process-triage/CASE_REPORT.md), [five invented Event 4688 rows](../projects/02-windows-process-triage/events_4688.csv), [11 unit tests](../projects/02-windows-process-triage/test_process_triage.py).

**Observed:** Two matching patterns at 10:02 and 10:04 UTC, with three nonmatching process-creation controls. The tool identifies candidate events; it does not decode scripts, verify a download, or classify malware.

**Decision:** Check process trees, parent/user context and independent endpoint or proxy telemetry under authorized procedures.

### Story 3 — Local vulnerability remediation and test boundaries

**Question:** How do you prove a change fixed an observed issue?

**Evidence:** [LAB-WEB-001](../projects/04-local-vulnerability-assessment/CASE_REPORT.md), [fixture source](../projects/04-local-vulnerability-assessment/fixture_app.py), [16 tests](../projects/04-local-vulnerability-assessment/test_vulnerability_lab.py).

**Observed:** Four deliberately missing or weak HTTP response controls on a local toy fixture; the same rules report zero after the remediated fixture. This establishes *predicate equivalence on the toy app*, not browser/TLS security or a real vulnerability scan.

**Decision:** Expand verification only in an owned, authorized environment; confirm browser behavior and regressions before any production claim.

## If asked about SIEM experience

The portfolio includes Splunk SPL drafts, a smoke test and a documented export-comparison protocol. **No genuine Splunk runtime results have been produced**, and the portfolio explicitly marks this as pending.

## Answers to common challenges

- **How many tests?** 76 Python unit tests, plus CI matrix, link, static accessibility and browser QA checks. This is a test count, **not** a measure of real-world detection accuracy.
- **Were these real incidents?** No. They use fabricated data in isolated environments.
- **What do the MITRE mappings prove?** They categorize possible behavior to investigate, not an adversary's intent or confirmed incident.
- **What is CR/RAI?** Private software-engineering projects discussed in public-safe architectural summaries. Their private implementations have not been independently validated as deployed security systems.

Use these statements only where they match the current code and public case evidence. Do not imply professional employment history, verified badge status or on-platform Splunk execution.
