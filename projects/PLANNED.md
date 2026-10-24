# Next Cybersecurity Labs (Not Completed)

These are **planned exercises**, not delivered portfolio evidence. Do not present them as finished in a résumé.

1. **Splunk validation of the authentication rule** — run the already prepared [smoke test](01-authentication-detection/SPLUNK_SMOKE_TEST.spl), [raw+findings export comparison](01-authentication-detection/qualify_exports.py), and [ingestion and comparison runbook](01-authentication-detection/SPLUNK_RUNBOOK.md) in a real authorized Splunk instance, compare its exported results to the frozen expected corpus, and document divergences and tuning. Offline preparation and structural verification are complete; smoke and corrected 64-event result screenshots have been reviewed. Indexed ingestion, authenticated job exports, and alert firing remain open.
2. **Wireshark GUI validation** — open the [offline-generated synthetic PCAP](03-network-pcap/README.md), verify display filters, and capture genuine screenshots. The offline Python and PCAP lab is implemented; Wireshark manual evidence remains pending.
3. **Real vulnerability management qualification** — the [localhost-only remediation exercise](04-local-vulnerability-assessment/README.md) and [synthetic report](04-local-vulnerability-assessment/CASE_REPORT.md) are implemented. Browser/TLS validation or scanning a real owned application remains **planned and requires authorization**.
4. **Security automation mini-service** — log normalization, data schema checks, malicious input handling, audit-friendly reporting, negative tests.
5. **AI answer evidence checker** — small synthetic source-attribution exercise inspired by RAI, fully independent of private source or fixtures.

## Completion criteria
Each lab needs a reproducible environment and commands, minimal dependencies, safe/synthetic or authorized inputs, a hypothesis, expected output, negative test cases, documented results, and candid coverage limits.

Do not run scans or access systems without permission. Publish only scrubbed evidence.

Runtime smoke execution: a [read-only token-based Splunk REST runner](01-authentication-detection/run_live_splunk_smoke.py) with deterministic CSV checks is prepared. **Mocked tests passing do not establish any real Splunk execution.**
