# Don Lopez | SOC Analyst & Security Analyst — Evidence Brief

**Career focus:** SOC Analyst · Cybersecurity Analyst · Junior Detection Engineering  
**Email:** [frailtycraven@gmail.com](mailto:frailtycraven@gmail.com)  
**Education:** B.S. Information Systems & Technology (Cybersecurity), California State University, San Bernardino, December 2024  
**Certifications:** CompTIA Security+ and CySA+ (owner-résumé-reported; CySA+ earned October 2026 according to résumé; issuer badges not independently available). SCCDA planned, not earned. [Verification scope](CREDENTIALS.md)

[**Two résumé versions and application toolkit**](https://ixi-2773.github.io/Cybersecurity_Portfolio/apply.html) · [**Printable recruiter profile**](https://ixi-2773.github.io/Cybersecurity_Portfolio/recruiter.html) · [**Live portfolio**](https://ixi-2773.github.io/Cybersecurity_Portfolio/) · [**Recorded AD investigation**](https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/ad-attack-chain.html) · [**GitHub source**](https://github.com/IXI-2773/Cybersecurity_Portfolio)

## Professional security experience

The supplied October 2026 résumé lists **Security Officer, Allied Universal (2019–present)**, involving secure-environment monitoring, incident documentation and escalation. This is résumé-reported physical-security experience, separate from the independent recorded-capture analysis and controlled labs and not a claim of paid SOC analyst tenure.

## Featured: recorded Active Directory investigation

I analyzed OTRF’s public recorded emulation: **25,993 host events and 1,121 packets**. The Python analysis links authentication failures, Kerberos service tickets, share checks and remote PowerShell using source references, same-host process GUIDs, logon sessions and bounded network context. Separating execution from collection time explains a **39.812-second delay** on the DC.

**Evidence:** [Interactive investigation](../projects/ad-attack-chain.html) · [Analyst report and reproduction](../projects/08-ad-investigation/CASE_REPORT.md) · [Source-reference index](../projects/08-ad-investigation/evidence.csv).

**Scope:** Independent analysis of OTRF’s recorded emulation, not an owner-operated capture or production incident. Six rule/context findings support investigation; legitimate administration remains a competing explanation. The Python implementation has source-linked correctness tests. SPL/Sigma translations remain unexecuted candidates; enterprise detection efficacy is unmeasured.

## Splunk example — real tool, controlled training data

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

Authentication lab adds **31 focused tests**, bringing the original four-lab subtotal to **76 Python tests**; AD and later exercises have separate tests. Tests validate the defined exercise behavior, not real-world detection accuracy.

## SOC investigation method

**Validate the signal → confirm source and event timing → correlate identity/host/network context → rule out benign explanations → document confidence and missing evidence → escalate only with authorization.**

[Read the triage playbook](SOC_TRIAGE_PLAYBOOK.md) · [Interview evidence examples](INTERVIEW_EVIDENCE_BRIEF.md) · [Resume-ready project bullets](RESUME_PORTFOLIO_BULLETS.md)

*The AD investigation analyzes OTRF’s public recorded emulation. Other reproducible exercises use synthetic, generated or localhost inputs. Celestial Resonance and Research AI Infrastructure are separate, privately implemented engineering projects described publicly only at a high level.*
