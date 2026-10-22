# Cybersecurity Portfolio — Don Lopez

A public, static portfolio presenting **reproducible synthetic defensive security exercises** alongside **high-level case studies of private engineering work**.

## Open the case studies right now

**[View all six case studies in GitHub's readable format](projects/CASE_STUDIES.md).** This is the best option when browsing the repository; those pages display normally instead of exposing HTML source.

For the **full designed website without GitHub Pages**, download the **`cybersecurity-portfolio-site` artifact** from the [latest successful GitHub Actions run](https://github.com/IXI-2773/Cybersecurity_Portfolio/actions), extract `cybersecurity-portfolio-site.zip`, and open `index.html` in your browser. The ZIP is automatically generated and validated in CI; no Python installation is required to view the extracted HTML.

## Website versus source code

GitHub's **Code** tab shows HTML source rather than a rendered site. Enable GitHub Pages once using [Settings → Pages](https://github.com/IXI-2773/Cybersecurity_Portfolio/settings/pages) → **Deploy from branch → main → /(root)**. See the [site-launch guide](docs/SITE_LAUNCH.md).

**Rendered site (after publishing is enabled):** https://ixi-2773.github.io/Cybersecurity_Portfolio/  
**Rendered CR page (after publishing is enabled):** https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/celestial-resonance.html

Opening a `github.com/.../blob/main/...html` link will continue to display source; use `github.io` after Pages is active.

## Certifications

- **CompTIA Security+** — credential reported by the portfolio owner.
- **CompTIA CySA+** — credential reported by the portfolio owner.

Public badge URLs, exam versions, dates and renewal status have not been supplied. See the [credential record](docs/CREDENTIALS.md) for claim limits.

## Start here
- [GitHub-readable project gallery](projects/CASE_STUDIES.md) — all six case studies without raw HTML or a 404.
- [Authentication detection case study](projects/authentication-detection.md) — reproducible, synthetic Python lab, 31 authentication tests, a simulated SOC investigation report, and a **Splunk runtime qualification package (not yet executed in Splunk)**.
- [Windows process execution triage case study](projects/windows-process-triage.md) — synthetic Windows Event ID 4688 exercise, 11 tests, ATT&CK hypotheses T1059.001 and T1105.
- [Network Traffic Analysis](projects/network-traffic-analysis.md) — PCAP generator, DNS/HTTP inspection, 18 tests, synthetic case report, and three [offline evidence images](assets/network/pcap-evidence-overview.svg).
- [Vulnerability Assessment & Remediation](projects/vulnerability-remediation.md) — localhost-only before/after HTTP hardening, 4 synthetic findings fixed, 16 tests.
- [Recruiter overview](docs/RECRUITER_OVERVIEW.md) — skills mapped to public evidence.
- [SOC analyst workflow](docs/SOC_TRIAGE_PLAYBOOK.md), [incident triage playbook](docs/SOC_TRIAGE_PLAYBOOK.md), and [analyst handoff template](docs/ANALYST_HANDOFF_TEMPLATE.md).
- [Detection evidence matrix](docs/DETECTION_EVIDENCE_MATRIX.md) and [résumé-ready project bullets](docs/RESUME_PORTFOLIO_BULLETS.md).
- [Celestial Resonance case study](projects/celestial-resonance.md) — responsible high-level summary of reproducible software research, quality gates, and auditability.
- [RAI case study](projects/research-ai-infrastructure.md) — high-level summary of evidence provenance, permission boundaries, and governed research tooling.
- [Future lab backlog](projects/PLANNED.md) — **planned**, not claimed as completed.

## Run all four security labs
Requires Python 3.10+; no dependencies or cloud resources.

```bash
python -m unittest discover -s projects/01-authentication-detection -p 'test_*.py' -v
python -m unittest discover -s projects/02-windows-process-triage -p 'test_*.py' -v
python projects/01-authentication-detection/detect_auth.py projects/01-authentication-detection/auth_events.csv
python projects/01-authentication-detection/validate_matrix.py
# The next step requires an authorized Splunk instance; see SPLUNK_RUNBOOK.md
python projects/02-windows-process-triage/process_triage.py projects/02-windows-process-triage/events_4688.csv
python projects/03-network-pcap/generate_fixture.py --output projects/03-network-pcap/synthetic_traffic.pcap
python projects/03-network-pcap/analyze_pcap.py projects/03-network-pcap/synthetic_traffic.pcap
python -m unittest discover -s projects/03-network-pcap -p 'test_*.py' -v
python projects/04-local-vulnerability-assessment/audit_demo.py
python -m unittest discover -s projects/04-local-vulnerability-assessment -p 'test_*.py' -v
```

Expected: **76 Python tests across four synthetic exercises** (31 authentication, 11 Windows process, 18 network, 16 local vulnerability assessment). The authentication fixture flags one login sequence for `alice` from `192.0.2.15`; the process-creation fixture returns two triage candidates. None is proof of real intrusion or production security efficacy.

## Offline website archive

The [bundler source](scripts/build_site_bundle.py) also supports creating the same archive manually with:

```bash
python scripts/build_site_bundle.py --output cybersecurity-portfolio-site.zip
```

Extract the ZIP fully before opening `index.html`. GitHub Actions generates a ready-made copy automatically on every successful `main` build.

## Publish using GitHub Pages
Go to repository **Settings → Pages → Build and deployment → Deploy from a branch → main / (root)**. Save. After deployment, check the page in a private browser window. The website does not require JavaScript, frameworks, runtime credentials, analytics, third-party fonts, or paid hosting.

## Public disclosure and accuracy
- CR and RAI are **private** engineering projects. Do not publish their source, internal records, repository URLs, security-sensitive workflow details, or artifacts without a separate review.
- Case studies are based on high-level architecture and development methods, and **do not** establish a production security system, an independent penetration test, or quantified business/security gains.
- All four labs use synthetic events or localhost-only fixtures; no real systems are scanned and no real network packets are captured. The SPL query, upload-free smoke test and validation protocol are *drafts*, not an empirically validated deployed detection.
- Project status and evidence limitations are visible on each case-study page.
- CompTIA Security+ and CySA+ are listed based on the owner's report; no independent public verification or current-renewal status is asserted.

See [SECURITY.md](SECURITY.md) for disclosure handling and [PUBLICATION_CHECKLIST.md](PUBLICATION_CHECKLIST.md) before future updates.

## Structure
```text
index.html, styles.css               Static website
projects/*.html                    Designed Pages case studies
projects/*.md                      GitHub-native readable versions of all six case studies
projects/01-authentication-detection/   Executable authentication lab
projects/02-windows-process-triage/     Executable Windows event triage lab
projects/03-network-pcap/              Generated PCAP exercise with source, tests, case report
projects/04-local-vulnerability-assessment/ Toy localhost web hardening + before/after audit
docs/RECRUITER_OVERVIEW.md            Skills mapped to evidence
projects/PLANNED.md                Honest roadmap
.github/workflows/validate.yml      Small focused CI checks + offline site preview archive
```

## License
No public reuse license is granted at this time. All rights reserved unless specified otherwise.
