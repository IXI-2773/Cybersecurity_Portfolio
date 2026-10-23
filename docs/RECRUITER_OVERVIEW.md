# Don Lopez — Cybersecurity Portfolio Summary

**Academic background:** B.S. in Cybersecurity, December 2024.  
**Career targets:** SOC Analyst · Cybersecurity Analyst · Detection Engineering · Security Automation.  
**Certifications (owner-reported):** CompTIA Security+ and CompTIA CySA+. Public verification and renewal dates pending; see [credentials](CREDENTIALS.md).  
**Portfolio:** [GitHub repository](https://github.com/IXI-2773/Cybersecurity_Portfolio) · [Live portfolio website](https://ixi-2773.github.io/Cybersecurity_Portfolio/)

**For a fast review, start with the [one-page recruiter evidence brief](RECRUITER_QUICK_BRIEF.md).** It puts the real Splunk investigation and three supporting security investigations in one place.

## Featured Splunk case — real tool, synthetic data

**Quickest evidence path:** [Featured authentication investigation](https://ixi-2773.github.io/Cybersecurity_Portfolio/#featured-splunk) → [full case study](../projects/authentication-detection.html) → [screenshot-reviewed saved Splunk dashboard result](../splunk_workflow/NATIVE_DASHBOARD_RESULT_2026-10-23.md).

In Splunk Enterprise Search & Reporting, the original 64-event authentication correlation produced **3 of 5** expected matches. A bounded, explicit-inclusive 600-second correction produced a screenshot-consistent **5/5**, then the operator saved a **one-panel dashboard** displaying those rows. The data represent nine fabricated test scenarios, not real events; search SID, exports and indexed ingestion were not authenticated. The original mismatch remains preserved as a debugging example.

## SOC Analyst starting point

[Review the SOC Analyst evidence overview](https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/soc-analyst-evidence.html) for four source-linked synthetic investigations, or use the [GitHub-rendered evidence guide](SOC_ANALYST_EVIDENCE_GUIDE.md) for a five-minute verification path. Both distinguish the observed Splunk search/dashboard results from unperformed indexed data, Wireshark GUI verification, and production outcomes.

## SOC authentication analysis visuals

[The SOC authentication analysis page](../projects/splunk-synthetic-preview.html) presents login trends, source-IP activity, and a training alert walkthrough derived from the frozen 64-event CSV. These are lab visuals, not product screenshots or real alerts. Separately, the [five-row native Splunk dashboard](../splunk_workflow/NATIVE_DASHBOARD_RESULT_2026-10-23.md) was observed in-product.

## Prepared Splunk workflow (not executed in trial)

A [no-install dashboard fallback](../splunk_workflow/NO_APP_GUIDE.md) is also prepared because the installed custom app returned 404 in the user's instance. The **native one-panel Search & Reporting dashboard now displays 5/5 findings** in a [real screenshot review](../splunk_workflow/NATIVE_DASHBOARD_RESULT_2026-10-23.md); the six-panel XML, indexing and alerts remain unverified.

The [installable Splunk source kit](../splunk_workflow/README.md) adds a bundled lookup dashboard, an indexed-data dashboard, nine analyst SPL searches and a default-disabled alert definition. CI checks the app package and CSV-source integrity. **Actual in-product dashboard rendering, indexed ingestion and alert firing have not been verified** and are not portfolio accomplishments yet. These are separate from the screenshot-reviewed seven-event and 64-event in-memory detections.

## Demonstrable projects

| Competency | Evidence | Qualification |
| --- | --- | --- |
| Authentication log triage | [Synthetic login-detection lab](../projects/01-authentication-detection/), [LAB-AUTH-001 case report](../projects/01-authentication-detection/SOC_CASE_REPORT.md) | 31 Python tests and nine scenario families; Seven-event Splunk smoke screenshot reviewed PASS; full 64-event run exposed a 3/5 boundary mismatch, corrected screenshot matches 5/5; indexed data not tested |
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

- Optionally reproduce the [indexed Splunk validation runbook](../projects/01-authentication-detection/SPLUNK_RUNBOOK.md); the in-memory search and native one-panel dashboard are already screenshot-reviewed, while indexed ingestion, job exports and triggered alerts remain unverified.
- Analyze a licensed or owned packet capture and report evidence, uncertainty, and defensive observations.
- Publish practical investigation reports with sanitized screenshots and time-stamped findings.

**Evidence policy:** No invented certifications, real incidents, deployed security systems, production precision/recall results, or disclosure of private project source.

**Connect:** [GitHub profile](https://github.com/IXI-2773)
