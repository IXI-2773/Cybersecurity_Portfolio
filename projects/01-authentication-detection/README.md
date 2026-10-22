# Authentication detection — reproducible synthetic lab

**Implemented:** Python detector and focused tests.  
**Not verified:** Splunk runtime behavior, SIEM deployment, detection accuracy on real logs.

## Run
```sh
python -m unittest discover -s projects/01-authentication-detection -v
python projects/01-authentication-detection/detect_auth.py projects/01-authentication-detection/auth_events.csv
```
No third-party libraries required. Python 3.10+.

The fabricated CSV has one suspicious sequence (alice / 192.0.2.15, six failures followed by success) plus other benign or non-qualifying sequences. A finding supports triage, **not a claim that the account was compromised**.

## Rule
Group by username and source IP. Count failures in the preceding ten-minute window. At the next success, flag if count is at least five. Clear that burst to suppress duplicate successes. Documented hypothesis: [MITRE ATT&CK T1110](https://attack.mitre.org/techniques/T1110/).

## Coverage & limits
No real users, infrastructure scanning, network I/O, MFA information, production telemetry, or evidence of attack attribution. Rotating-source attempts, absent data, clock skew and distributed login patterns can evade this heuristic. Validate the `splunk.spl` query independently; matching behavior has not yet been established.

The test suite covers positive fixture, negative threshold, expired window, per-key isolation, chronological sorting, inclusive time boundary, malformed time, invalid configuration, and duplicate-success suppression.

## SOC investigation expansion — v2.1

- [Simulated incident report](SOC_CASE_REPORT.md): observable timeline, hypothesis, gaps and explicitly synthetic disposition.
- [Splunk ingestion and comparison runbook](SPLUNK_RUNBOOK.md): required on-platform steps and artifact capture checklist.
- [Independent scenario fixture](validation_events.csv) and [expected findings](expected_findings.json): nine constructed scenario families, **five expected findings**.
- [Offline and optional CSV comparison tool](validate_matrix.py): `python projects/01-authentication-detection/validate_matrix.py`. This verifies Python behavior; it **does not** validate the Splunk runtime without a genuine Splunk export.
- [SPL design](splunk.spl): use one streak per account/source IP; **any** successful login closes the previous burst. Global chronological sort is required before a time-windowed `streamstats`. This remains a **draft pending real Splunk execution**.

The v2.1 tests add regressions for non-alerting success resets, independent identities, malformed CSV data and validation matrix expectations. The project now has **15** Python unit tests.
