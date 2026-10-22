# Detection Evidence Matrix — Don Lopez

Public evidence is deliberately separated from interpretations, live execution, and private research.

| Rule / capability | Threat hypothesis | Inspectable input and implementation | Public verification | Still unverified |
| --- | --- | --- | --- | --- |
| AUTH-01: failed logins followed by success | ATT&CK T1110 | [Synthetic event CSV](../projects/01-authentication-detection/auth_events.csv), [Python detector](../projects/01-authentication-detection/detect_auth.py), [64-event matrix](../projects/01-authentication-detection/validation_events.csv) | [Unit tests](../projects/01-authentication-detection/test_detect_auth.py), [expected rows](../projects/01-authentication-detection/expected_findings.json) | Actual identity-provider security outcomes |
| PROC-01: encoded PowerShell | ATT&CK T1059.001 | [Synthetic 4688 events](../projects/02-windows-process-triage/events_4688.csv), [process rule](../projects/02-windows-process-triage/process_triage.py) | [11 focused tests](../projects/02-windows-process-triage/test_process_triage.py) | Real endpoint execution, script content, legitimate baseline |
| PROC-02: certutil URL-cache flags | ATT&CK T1105 | Same process-creation CSV and rule | Same focused tests | Actual file transfer, network context, malicious intent |
| SPLUNK-AUTH-01: translation of AUTH-01 | ATT&CK T1110 | [SPL query](../projects/01-authentication-detection/splunk.spl), [test runbook](../projects/01-authentication-detection/SPLUNK_RUNBOOK.md) | [Mocked REST runner tests](../projects/01-authentication-detection/test_live_smoke.py) | **Actual Splunk runtime and 64-event ingestion/results** |

**Status:** The public GitHub Actions workflow exercises **42 Python tests** and synthetic validation checks. A passing test asserts behavior on synthetic fixtures; it is **not** a measurement of production detection effectiveness.

## Promotion requirements for future claims

1. Confirm authorization and input provenance.
2. Freeze independent expected results and include negative cases.
3. Record runtime, exact inputs and exported results, time-zone interpretation and checksums.
4. Review deviations and compare to an independent baseline.
5. Change a claim from *prepared* to *demonstrated* only when genuine supporting artifacts exist.

For the analyst's response procedure, see the [SOC triage playbook](SOC_TRIAGE_PLAYBOOK.md).
