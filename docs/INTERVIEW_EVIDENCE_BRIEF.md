# Interview Evidence Brief — Don Lopez

**Audience:** SOC Analyst, junior Security Analyst, Detection Engineering and Security Automation interviewers  
**Positioning:** B.S. Cybersecurity (2024); CompTIA Security+ and CySA+ **reported by holder**, public verification pending. The four public security labs are **synthetic portfolio exercises**, not paid SOC incident experience.

**Recruiter navigation:** [SOC Analyst evidence index](https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/soc-analyst-evidence.html) · [GitHub-readable evidence guide](SOC_ANALYST_EVIDENCE_GUIDE.md).

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

A screenshot from Splunk Enterprise, reviewed October 23, 2026, showed a seven-event synthetic authentication smoke test returning the expected single row with five failures. Full 64-event verification, exported results and job provenance remain pending. The screenshot has not been publicly committed; see the [observation record](../projects/01-authentication-detection/SPLUNK_SMOKE_OBSERVATION_2026-10-23.md).

## Answers to common challenges

- **How many tests?** 76 Python unit tests, plus CI matrix, link, static accessibility and browser QA checks. This is a test count, **not** a measure of real-world detection accuracy.
- **Were these real incidents?** No. They use fabricated data in isolated environments.
- **What do the MITRE mappings prove?** They categorize possible behavior to investigate, not an adversary's intent or confirmed incident.
- **What is CR/RAI?** Private software-engineering projects discussed in public-safe architectural summaries. Their private implementations have not been independently validated as deployed security systems.

Use these statements only where they match the current code and public case evidence. Do not imply professional employment history, verified badge status or on-platform Splunk execution.

## Story 4 — Network triage with source-level traceability

**Question:** Do repeated NXDOMAIN responses or an HTTP POST establish command-and-control?

**Evidence:** [LAB-NET-001](../projects/03-network-pcap/CASE_REPORT.md), [deterministic PCAP generator](../projects/03-network-pcap/generate_fixture.py), [frozen expected findings](../projects/03-network-pcap/expected_findings.json), and [18 tests](../projects/03-network-pcap/test_network_lab.py).

**Observed:** Four synthetic failed DNS replies trigger at 12:00:36.200 UTC (frame 8), and a reserved-host POST triggers at 12:01:15.030 UTC (frame 19). A separate client provides benign DNS and GET controls.

**Decision:** Investigate only on authorized real telemetry with endpoint and resolver/proxy corroboration. No C2, tunneling or exfiltration is established.

## Story 5 — What a zero-finding remediation report can and cannot prove

**Question:** Does adding Secure/HttpOnly/SameSite and CSP prove a web application is secure?

**Evidence:** [LAB-WEB-001](../projects/04-local-vulnerability-assessment/CASE_REPORT.md), [local fixture](../projects/04-local-vulnerability-assessment/fixture_app.py), and [16 tests](../projects/04-local-vulnerability-assessment/test_vulnerability_lab.py).

**Observed:** Four artificial HTTP response-control rules match the deliberately vulnerable localhost fixture. The same rules match zero after modification.

**Limit:** The cookie test checks attribute presence over HTTP without TLS. The CSP test checks whether a header exists, not its semantics or browser enforcement. Those findings must not be promoted to a production security sign-off.
