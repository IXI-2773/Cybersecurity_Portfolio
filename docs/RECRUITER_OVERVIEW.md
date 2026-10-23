# Don Lopez — Cybersecurity Portfolio Summary

**Academic background:** B.S. in Cybersecurity, December 2024.  
**Career targets:** SOC Analyst · Cybersecurity Analyst · Detection Engineering · Security Automation.  
**Certifications (owner-reported):** CompTIA Security+ and CompTIA CySA+. Public verification and renewal dates pending; see [credentials](CREDENTIALS.md).  
**Portfolio:** [GitHub repository](https://github.com/IXI-2773/Cybersecurity_Portfolio) · [Live portfolio website](https://ixi-2773.github.io/Cybersecurity_Portfolio/)

## Demonstrable projects

| Competency | Evidence | Qualification |
| --- | --- | --- |
| Authentication log triage | [Synthetic login-detection lab](../projects/01-authentication-detection/), [LAB-AUTH-001 case report](../projects/01-authentication-detection/SOC_CASE_REPORT.md) | 31 Python tests and nine scenario families; SPL requires on-platform validation |
| Windows process telemetry triage | [Synthetic Event 4688 lab](../projects/02-windows-process-triage/), [LAB-PROC-001 case report](../projects/02-windows-process-triage/CASE_REPORT.md) | 11 Python tests; rule findings, not deployed |
| Network packet analysis | [Synthetic PCAP](../projects/03-network-pcap/) and [investigation report](../projects/03-network-pcap/CASE_REPORT.md) | Source-linked 20-packet timeline, two candidate rules and 18 tests; no real capture |
| Python automation | Four synthetic standard-library security labs and JSON outputs | No third-party application dependencies |
| SOC evidence handling & handoff | [Read-only analyst workflow](../projects/soc-analyst-workflow.html), [triage playbook](SOC_TRIAGE_PLAYBOOK.md) | Demonstrated documentation, not a claim of live incident-response employment |
| Local vulnerability assessment | [Before/after web security exercise](../projects/04-local-vulnerability-assessment/) and [synthetic case report](../projects/04-local-vulnerability-assessment/CASE_REPORT.md) | Four deliberately introduced rule findings cleared in the second localhost fixture; no TLS/browser validation |
| Reproducible verification | 76 unit tests, offline SOC scenario checker, and [CI workflow](../.github/workflows/validate.yml) | CI status must be checked independently |
| Engineering quality and safeguards | [Celestial Resonance case study](../projects/celestial-resonance.html) | High-level private-project description |
| Evidence provenance and permission boundaries | [RAI case study](../projects/research-ai-infrastructure.html) | Not a production security agent |

## Fast evidence walkthrough for recruiters

**SOC Analyst / Cybersecurity Analyst:** Start with [LAB-AUTH-001](../projects/01-authentication-detection/SOC_CASE_REPORT.md) and [LAB-PROC-001](../projects/02-windows-process-triage/CASE_REPORT.md). Each identifies an alerting condition, source event timeline, alternate explanation, missing corroboration and a provisional disposition. All inputs are fabricated.

**Detection Engineering / Security Automation:** Review the [authentication detector](../projects/01-authentication-detection/detect_auth.py), [unit tests](../projects/01-authentication-detection/test_detect_auth.py), [validation oracle](../projects/01-authentication-detection/expected_findings.json), and [focused CI workflow](../.github/workflows/validate.yml). The success-reset regression demonstrates why negative test cases matter.

**Network Investigation:** Review [LAB-NET-001](../projects/03-network-pcap/CASE_REPORT.md) for packet/frame traceability, clear separation between DNS/HTTP anomaly predicates and maliciousness claims, and missing corroboration.

**Vulnerability Management:** Review [localhost hardening before/after](../projects/04-local-vulnerability-assessment/CASE_REPORT.md), with four deliberate predicate hits reduced to zero after modification. Do not confuse this with a third-party scan.

See [interview discussion guide](INTERVIEW_EVIDENCE_BRIEF.md) for short, evidence-supported explanations.

## Work in progress

- Execute the [documented Splunk verification runbook](../projects/01-authentication-detection/SPLUNK_RUNBOOK.md) in an authorized instance; publish genuine, scrubbed evidence and tuning notes.
- Analyze a licensed or owned packet capture and report evidence, uncertainty, and defensive observations.
- Publish practical investigation reports with sanitized screenshots and time-stamped findings.

**Evidence policy:** No invented certifications, real incidents, deployed security systems, production precision/recall results, or disclosure of private project source.

**Connect:** [GitHub profile](https://github.com/IXI-2773)
