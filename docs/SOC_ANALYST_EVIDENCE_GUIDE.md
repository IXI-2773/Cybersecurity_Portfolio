# SOC Analyst Evidence Guide — Don Lopez

**Public recruiter reference.** This portfolio documents four reproducible *synthetic* security exercises and private engineering summaries. They do **not** establish employment in a SOC, actual incident response, deployed detection efficacy or live security outcomes.

**Website:** [SOC Analyst evidence overview](https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/soc-analyst-evidence.html)

## Five-minute project review

| Investigation | Demonstrated synthetic behavior | Independent public evidence | Tests | Unverified |
| --- | --- | --- | --- | --- |
| Identity / authentication | Six failures followed by success for the same account/IP trigger a review finding | [LAB-AUTH-001 report](../projects/01-authentication-detection/SOC_CASE_REPORT.md), [test suite](../projects/01-authentication-detection/test_detect_auth.py) | 31 | Real identity-provider data; independent job provenance and indexed CSV (seven-event smoke passed; original 64-event 3/5; corrected screenshot 5/5) |
| Windows endpoint | Encoded PowerShell and certutil arguments produce two candidate matches among five fabricated events | [LAB-PROC-001 report](../projects/02-windows-process-triage/CASE_REPORT.md), [test suite](../projects/02-windows-process-triage/test_process_triage.py) | 11 | Process execution, malicious intent and endpoint telemetry |
| Network | Matched NXDOMAIN burst and reserved-host POST in a deterministic 20-frame PCAP | [LAB-NET-001 report](../projects/03-network-pcap/CASE_REPORT.md), [test suite](../projects/03-network-pcap/test_network_lab.py) | 18 | Wireshark runtime and any real network capture |
| HTTP hardening | Four intentional rule failures become zero after a localhost fixture change | [LAB-WEB-001 report](../projects/04-local-vulnerability-assessment/CASE_REPORT.md), [test suite](../projects/04-local-vulnerability-assessment/test_vulnerability_lab.py) | 16 | HTTPS, real browser enforcement, production risk |

**Total: 76 focused Python unit tests.** Counts represent fixture/test coverage, not operational security accuracy.

## Current qualification boundary

**Supported now:** Offline code, synthetic data, expected outputs, negative cases, source-linked analyst reports, automated code tests, and a deployed static portfolio site.

**Partial evidence:** A [seven-event Splunk smoke search](../projects/01-authentication-detection/SPLUNK_SMOKE_OBSERVATION_2026-10-23.md) matched its expected result in the operator's real application screenshot on 2026-10-23; the image itself is not a publicly retained repository artifact.

**Observed full-matrix discrepancy:** The initial [64-event Splunk execution returned only 3 of 5 expected findings](../projects/01-authentication-detection/SPLUNK_MATRIX_FIRST_RUN_2026-10-23.md), with the missing detections both on the inclusive 10-minute boundary. [The later corrected-result screenshot shows all 5/5 rows](../projects/01-authentication-detection/SPLUNK_MATRIX_BOUNDARY_RETEST_RESULT_2026-10-23.md), consistent with the candidate fix; query and job SID are absent from the cropped image.

**Optional further qualification:** Full indexed CSV exports and independent search-job provenance, manual Wireshark GUI verification, independently verifiable certification badges, real enterprise telemetry, and production incident outcomes.

**Interpretation:** A rule match leads to corroboration and a documented decision; it does not authorize containment or prove compromise. All published case studies preserve this distinction.

## Native Splunk dashboard: screenshot-reviewed

The [native Search & Reporting dashboard](../splunk_workflow/NATIVE_DASHBOARD_RESULT_2026-10-23.md) opened in Splunk Enterprise and displayed a saved table of **5/5 synthetic authentication findings**. Only the **one-panel** dashboard is verified by screenshot. The six-panel XML, indexed ingestion and scheduled alert are not validated. The screenshot remains in chat rather than the public repository.

## Splunk development package — prepared, not deployed

[Inspect the complete Splunk app kit](../splunk_workflow/README.md). It packages a synthetic lookup-backed SOC dashboard, an indexed-data dashboard, nine SPL searches and a disabled alert definition. Source and package validation is automated. **These new components have not yet been installed or validated in the actual Splunk Enterprise user interface.**

## Further reading

- [Recruiter overview](RECRUITER_OVERVIEW.md)
- [Interview evidence brief](INTERVIEW_EVIDENCE_BRIEF.md)
- [Detection evidence matrix](DETECTION_EVIDENCE_MATRIX.md)
- [SOC investigation playbook](SOC_TRIAGE_PLAYBOOK.md)
- [GitHub-readable six-project index](../projects/CASE_STUDIES.md)
