# Don Lopez | SOC Analyst & Security Analyst — Evidence Brief

**Career focus:** SOC Analyst · Cybersecurity Analyst · Junior Detection Engineering  
**Education:** B.S. Cybersecurity, December 2024  
**Certifications:** CompTIA Security+ and CySA+ (owner-reported; public badges/validity dates not independently available)

[**Two résumé versions and application toolkit**](https://ixi-2773.github.io/Cybersecurity_Portfolio/apply.html) · [**Printable recruiter profile**](https://ixi-2773.github.io/Cybersecurity_Portfolio/recruiter.html) · [**Live portfolio**](https://ixi-2773.github.io/Cybersecurity_Portfolio/) · [**Featured Splunk investigation**](https://ixi-2773.github.io/Cybersecurity_Portfolio/#featured-splunk) · [**GitHub source**](https://github.com/IXI-2773/Cybersecurity_Portfolio)

## Primary technical example — real Splunk Enterprise UI, controlled training data

**Goal:** Detect successful logins following at least five failures from the same user and source IP within an **inclusive ten-minute** period.

**Evidence trail:** [Frozen 64-event CSV](../projects/01-authentication-detection/validation_events.csv) → [Five expected findings](../projects/01-authentication-detection/expected_findings.json) → [Observed original 3/5 parity failure](../projects/01-authentication-detection/SPLUNK_MATRIX_FIRST_RUN_2026-10-23.md) → [Explicit-boundary SPL correction](../projects/01-authentication-detection/SPLUNK_MATRIX_BOUNDARY_RETEST.spl) → [Screenshot-reviewed native Splunk dashboard showing 5/5 rows](../splunk_workflow/NATIVE_DASHBOARD_RESULT_2026-10-23.md).

**What this demonstrates:** SPL event correlation, negative/boundary-case debugging, discrepancy investigation, test-oracle comparison, and saving a working dashboard in **Splunk Enterprise Search & Reporting**.

**What this does not establish:** Live enterprise incidents, indexed ingestion, a six-panel Splunk dashboard, production alert performance, authenticated job SID or complete SIEM deployment. A [cropped genuine Splunk dashboard screenshot](../assets/evidence/splunk-native-dashboard-results.png) is now public; the original full-sized capture remains in the project conversation.

## Three supporting reproducible investigations

| Capability | Public evidence | Verification |
| --- | --- | --- |
| Windows process telemetry | [Windows Event ID 4688 triage report](../projects/02-windows-process-triage/CASE_REPORT.md) | Two rule candidates across five fabricated events; 11 focused tests |
| Network packet review | [DNS/HTTP PCAP report](../projects/03-network-pcap/CASE_REPORT.md) | 20 generated packets; two rule candidates; 18 tests |
| HTTP response hardening | [Local before/after report](../projects/04-local-vulnerability-assessment/CASE_REPORT.md) | Four deliberate violations reduced to zero in a localhost toy app; 16 tests |

Authentication lab adds **31 focused tests**, bringing the four-lab total to **76 Python tests**. Tests validate the defined exercise behavior, not real-world detection accuracy.

## SOC investigation method

**Validate the signal → confirm source and event timing → correlate identity/host/network context → rule out benign explanations → document confidence and missing evidence → escalate only with authorization.**

[Read the triage playbook](SOC_TRIAGE_PLAYBOOK.md) · [Interview evidence examples](INTERVIEW_EVIDENCE_BRIEF.md) · [Resume-ready project bullets](RESUME_PORTFOLIO_BULLETS.md)

*All lab data are deliberately fabricated or localhost-only. Celestial Resonance and Research AI Infrastructure are separate, privately implemented engineering projects described publicly only at a high level.*
