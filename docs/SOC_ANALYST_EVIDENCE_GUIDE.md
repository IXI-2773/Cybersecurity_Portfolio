# SOC Analyst Evidence Guide — Don Lopez

**Public recruiter reference.** This portfolio documents independent analysis of OTRF’s recorded AD emulation, reproducible controlled security labs and private engineering summaries. They do **not** establish employment in a SOC, actual incident response, deployed detection efficacy or live security outcomes.

**Website:** [SOC Analyst evidence overview](https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/soc-analyst-evidence.html)

## Featured: recorded Active Directory investigation

I analyzed OTRF’s public recorded emulation: **25,993 host events and 1,121 packets**. The Python analysis links authentication failures, Kerberos service tickets, share checks and remote PowerShell using source references, same-host process GUIDs, logon sessions and bounded network context. Separating execution from collection time explains a **39.812-second delay** on the DC.

**Evidence:** [Interactive investigation](../projects/ad-attack-chain.html) · [Analyst report and reproduction](../projects/08-ad-investigation/CASE_REPORT.md) · [Source-reference index](../projects/08-ad-investigation/evidence.csv).

**Scope:** Independent analysis of OTRF’s recorded emulation, not an owner-operated capture or production incident. Six rule/context findings support investigation; legitimate administration remains a competing explanation. The Python implementation has source-linked correctness tests. SPL/Sigma translations remain unexecuted candidates; enterprise detection efficacy is unmeasured.

## Splunk application evidence

[Open the featured Splunk investigation on the live site](https://ixi-2773.github.io/Cybersecurity_Portfolio/#featured-splunk). The saved **one-panel** Splunk Search & Reporting dashboard was screenshot-reviewed, showing all five frozen expected findings over 64 artificial events. A previous search returned **3/5** due to boundary behavior; its failure and the correction are documented separately. No real incident, indexed CSV import or scheduled alert is claimed.

## Five-minute project review

| Investigation | Demonstrated behavior and input scope | Independent public evidence | Tests | Unverified |
| --- | --- | --- | --- | --- |
| Recorded AD emulation | Host/session/packet correlation across 25,993 host records and 1,121 packets | [AD report](../projects/08-ad-investigation/CASE_REPORT.md), [test suite](../projects/08-ad-investigation/test_analysis.py) | 23 | Enterprise efficacy and AD SPL/Sigma backend execution |
| Identity / authentication | Six failures followed by success for the same account/IP trigger a review finding | [LAB-AUTH-001 report](../projects/01-authentication-detection/SOC_CASE_REPORT.md), [test suite](../projects/01-authentication-detection/test_detect_auth.py) | 31 | Real identity-provider data; independent job provenance and indexed CSV (seven-event smoke passed; original 64-event 3/5; corrected screenshot 5/5) |
| Windows endpoint | Encoded PowerShell and certutil arguments produce two candidate matches among five fabricated events | [LAB-PROC-001 report](../projects/02-windows-process-triage/CASE_REPORT.md), [test suite](../projects/02-windows-process-triage/test_process_triage.py) | 11 | Process execution, malicious intent and endpoint telemetry |
| Network | Matched NXDOMAIN burst and reserved-host POST in a deterministic 20-frame PCAP | [LAB-NET-001 report](../projects/03-network-pcap/CASE_REPORT.md), [test suite](../projects/03-network-pcap/test_network_lab.py) | 18 | Wireshark runtime and any real network capture |
| HTTP hardening | Four intentional rule failures become zero after a localhost fixture change | [LAB-WEB-001 report](../projects/04-local-vulnerability-assessment/CASE_REPORT.md), [test suite](../projects/04-local-vulnerability-assessment/test_vulnerability_lab.py) | 16 | HTTPS, real browser enforcement, production risk |

**Original four-lab subtotal: 76 focused Python unit tests; AD analysis adds 23 separately scoped tests.** Later exercises have their own test suites. Counts represent defined behavior and evidence-join checks, not operational security accuracy.

## Current qualification boundary

**Supported now:** Recorded OTRF AD telemetry analysis, controlled synthetic/localhost labs, expected outputs, negative cases, source-linked analyst reports, automated code tests and a deployed static portfolio site.

**Partial evidence:** A [seven-event Splunk smoke search](../projects/01-authentication-detection/SPLUNK_SMOKE_OBSERVATION_2026-10-23.md) matched its expected result in the operator's real application screenshot on 2026-10-23; the image itself is not a publicly retained repository artifact.

**Observed full-matrix discrepancy:** The initial [64-event Splunk execution returned only 3 of 5 expected findings](../projects/01-authentication-detection/SPLUNK_MATRIX_FIRST_RUN_2026-10-23.md), with the missing detections both on the inclusive 10-minute boundary. [The later corrected-result screenshot shows all 5/5 rows](../projects/01-authentication-detection/SPLUNK_MATRIX_BOUNDARY_RETEST_RESULT_2026-10-23.md), consistent with the candidate fix; query and job SID are absent from the cropped image.

**Optional further qualification:** Full indexed CSV exports and independent search-job provenance, manual Wireshark GUI verification, independently verifiable certification badges, additional authorized enterprise telemetry and production incident outcomes.

**Interpretation:** A rule match leads to corroboration and a documented decision; it does not authorize containment or prove compromise. All published case studies preserve this distinction.

## Native Splunk dashboard: screenshot-reviewed

The [native Search & Reporting dashboard](../splunk_workflow/NATIVE_DASHBOARD_RESULT_2026-10-23.md) opened in Splunk Enterprise and displayed a saved table of **5/5 synthetic authentication findings**. Only the **one-panel** dashboard is verified by screenshot. The six-panel XML, indexed ingestion and scheduled alert are not validated. A [cropped genuine Splunk screenshot](../assets/evidence/splunk-native-dashboard-results.png) is now included publicly; the full original stays in the project conversation.

## Splunk development package — prepared, not deployed

[Inspect the complete Splunk app kit](../splunk_workflow/README.md). It packages a synthetic lookup-backed SOC dashboard, an indexed-data dashboard, nine SPL searches and a disabled alert definition. Source and package validation is automated. **These new components have not yet been installed or validated in the actual Splunk Enterprise user interface.**

## Further reading

- [Recruiter overview](RECRUITER_OVERVIEW.md)
- [Interview evidence brief](INTERVIEW_EVIDENCE_BRIEF.md)
- [Detection evidence matrix](DETECTION_EVIDENCE_MATRIX.md)
- [SOC investigation playbook](SOC_TRIAGE_PLAYBOOK.md)
- [GitHub-readable six-project index](../projects/CASE_STUDIES.md)
