# Detection Evidence Matrix — Don Lopez

Public evidence is deliberately separated from interpretations, live execution, and private research.

| Rule / capability | Threat hypothesis | Inspectable input and implementation | Public verification | Still unverified |
| --- | --- | --- | --- | --- |
| AUTH-01: failed logins followed by success | ATT&CK T1110 | [Synthetic event CSV](../projects/01-authentication-detection/auth_events.csv), [Python detector](../projects/01-authentication-detection/detect_auth.py), [64-event matrix](../projects/01-authentication-detection/validation_events.csv) | [Unit tests](../projects/01-authentication-detection/test_detect_auth.py), [expected rows](../projects/01-authentication-detection/expected_findings.json) | Actual identity-provider security outcomes |
| PROC-01: encoded PowerShell | ATT&CK T1059.001 | [Synthetic 4688 events](../projects/02-windows-process-triage/events_4688.csv), [process rule](../projects/02-windows-process-triage/process_triage.py) | [11 focused tests](../projects/02-windows-process-triage/test_process_triage.py) | Real endpoint execution, script content, legitimate baseline |
| PROC-02: certutil URL-cache flags | ATT&CK T1105 | Same process-creation CSV and rule | Same focused tests | Actual file transfer, network context, malicious intent |
| SPLUNK-AUTH-01: translation of AUTH-01 | ATT&CK T1110 | [SPL query](../projects/01-authentication-detection/splunk.spl), [test runbook](../projects/01-authentication-detection/SPLUNK_RUNBOOK.md) | [Mocked REST runner tests](../projects/01-authentication-detection/test_live_smoke.py) | **Actual Splunk runtime and 64-event ingestion/results** |
| NET-DNS-01: NXDOMAIN burst | ATT&CK T1071.004 (hypothesis only) | [Synthetic PCAP generator](../projects/03-network-pcap/generate_fixture.py), [analyzer](../projects/03-network-pcap/analyze_pcap.py) | [18 packet tests](../projects/03-network-pcap/test_network_lab.py); [source-timed case](../projects/03-network-pcap/CASE_REPORT.md) | No live DNS logs, malicious tunneling or endpoint context |
| NET-HTTP-01: unusual HTTP POST | ATT&CK T1071.001 (hypothesis only) | [Same PCAP](../projects/03-network-pcap/README.md), [expected findings](../projects/03-network-pcap/expected_findings.json) | Same tests and [synthetic report](../projects/03-network-pcap/CASE_REPORT.md) | No evidence of exfiltration or malicious destination |
| WEB-01: synthetic response hardening | Missing security headers, cookie attributes and debug disclosure | [Toy loopback fixture](../projects/04-local-vulnerability-assessment/fixture_app.py) and [audit](../projects/04-local-vulnerability-assessment/audit_demo.py) | [16 focused tests](../projects/04-local-vulnerability-assessment/test_vulnerability_lab.py), [before/after case](../projects/04-local-vulnerability-assessment/CASE_REPORT.md); four expected rule findings before and none after | No real app, CVSS, HTTPS/browser validation, or external vulnerability scan |

**Status:** The public GitHub Actions workflow exercises **76 Python tests** and synthetic validation checks. A passing test asserts behavior on synthetic fixtures; it is **not** a measurement of production detection effectiveness.

## Promotion requirements for future claims

1. Confirm authorization and input provenance.
2. Freeze independent expected results and include negative cases.
3. Record runtime, exact inputs and exported results, time-zone interpretation and checksums.
4. Review deviations and compare to an independent baseline.
5. Change a claim from *prepared* to *demonstrated* only when genuine supporting artifacts exist.

For the analyst's response procedure, see the [SOC triage playbook](SOC_TRIAGE_PLAYBOOK.md).
