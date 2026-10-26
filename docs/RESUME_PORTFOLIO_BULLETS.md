# Résumé Project Bullets — Don Lopez

These are evidence-limited wording options. They describe public projects, not invented professional employment, production security deployments or live incidents.

## Credentials
- CompTIA Security+ — held according to portfolio owner; issuer verification URL pending.
- CompTIA CySA+ — held according to portfolio owner; issuer verification URL pending.
- B.S. in Cybersecurity, December 2024.

## Projects
- Analyzed 25,993 host events and 1,121 packets from OTRF’s recorded Active Directory emulation; correlated process GUIDs, logon sessions and packet references, and explained a 39.812-second collection delay. Published reproducible Python analysis with source-linked correctness tests and competing administration explanations. [Inspect the case](../projects/ad-attack-chain.html).
- Built a Python authentication-correlation lab with negative tests for success/reset boundaries, source isolation and malformed inputs; documented findings using synthetic login events.
- Developed a Windows process-creation triage exercise using fabricated Event ID 4688 records, identifying two PowerShell/certutil command-pattern candidates and documenting a source-attributed five-event synthetic investigation.
- Built a deterministic 20-packet PCAP generator and a bounded Python DNS/HTTP analyzer, verified through 18 focused tests; produced a frame-attributed synthetic DNS/HTTP case report.
- Built a localhost-only HTTP response-hardening exercise with four intentional misconfigurations, verified the four-to-zero reduction in fixed rule violations with 16 regression tests and a documented limits assessment.
- Configured GitHub Actions for the original four-lab suite’s **76 focused Python tests**, an offline validation matrix and link-integrity checks; additional cases retain separately scoped tests.
- Executed an authentication-correlation search in **Splunk Enterprise Search & Reporting** against 64 fabricated events; investigated a **3/5** result discrepancy at the inclusive ten-minute boundary, revised SPL and documented a saved native dashboard displaying **5/5** expected synthetic findings (screenshot-reviewed; no production telemetry or indexed ingestion).
- Prepared an optional Splunk dashboard and disabled-alert configuration package; distinguished packaged source validation from unperformed indexed-data and scheduled-alert runtime tests.
- Documented high-level engineering techniques for evidence provenance, controlled authority and software quality using public-safe summaries of private CR and RAI projects.

## Selecting two or three bullets per application

**SOC Analyst:** Lead with recorded AD host/packet correlation, the actual Splunk investigation and SOC evidence handling. **Security Automation / Detection Engineering:** Lead with the Splunk boundary fix, the 31-test authentication lab, and the focused CI pipeline. Avoid listing every exercise if a job posting emphasizes only one security domain. Never label synthetic exercises as work employment.

[One-page evidence brief](RECRUITER_QUICK_BRIEF.md) links the claims to public source material.

## Discussion points for interviews
- Why should any successful authentication reset a failed-login sequence?
- How could legitimate administration produce a false positive for encoded PowerShell?
- What evidence is required before an alert should be escalated as a likely incident?
- What do negative tests prove, and what can they not establish about production detection?
- How do research provenance and execution permissions translate to security operations?

Public résumé use should remain limited to what the linked sources demonstrate.
