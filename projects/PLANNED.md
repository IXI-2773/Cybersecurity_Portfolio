# Next Cybersecurity Labs (Not Completed)

These are **planned exercises**, not delivered portfolio evidence. Do not present them as finished in a résumé.

1. **Splunk validation of the authentication rule** — run the already prepared [smoke test](01-authentication-detection/SPLUNK_SMOKE_TEST.spl), [raw+findings export comparison](01-authentication-detection/qualify_exports.py), and [ingestion and comparison runbook](01-authentication-detection/SPLUNK_RUNBOOK.md) in a real authorized Splunk instance, compare its exported results to the frozen expected corpus, and document divergences and tuning. Offline preparation and structural verification are complete; runtime access, genuine Splunk execution and screenshot evidence remain open.
2. **Packet analysis case study** — analyze a permissibly sourced PCAP in Wireshark; report timeline, observable facts, ambiguities and any privacy limitations.
3. **Vulnerability management lab** — scan owned or expressly authorized lab services; document findings, validation, severity rationale, remediation and rescan.
4. **Security automation mini-service** — log normalization, data schema checks, malicious input handling, audit-friendly reporting, negative tests.
5. **AI answer evidence checker** — small synthetic source-attribution exercise inspired by RAI, fully independent of private source or fixtures.

## Completion criteria
Each lab needs a reproducible environment and commands, minimal dependencies, safe/synthetic or authorized inputs, a hypothesis, expected output, negative test cases, documented results, and candid coverage limits.

Do not run scans or access systems without permission. Publish only scrubbed evidence.
