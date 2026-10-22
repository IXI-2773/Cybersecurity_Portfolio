# Cybersecurity Portfolio — Don Lopez

A public, static portfolio presenting **reproducible synthetic defensive security exercises** alongside **high-level case studies of private engineering work**.

**Live website (after GitHub Pages is enabled):** https://ixi-2773.github.io/Cybersecurity_Portfolio/

## Certifications

- **CompTIA Security+** — credential reported by the portfolio owner.
- **CompTIA CySA+** — credential reported by the portfolio owner.

Public badge URLs, exam versions, dates and renewal status have not been supplied. See the [credential record](docs/CREDENTIALS.md) for claim limits.

## Start here
- [Portfolio home](index.html) — skills and project index.
- [Authentication detection case study](projects/authentication-detection.html) — reproducible, synthetic Python lab, 31 authentication tests, a simulated SOC investigation report, and a **Splunk runtime qualification package (not yet executed in Splunk)**.
- [Windows process execution triage case study](projects/windows-process-triage.html) — synthetic Windows Event ID 4688 exercise, 11 tests, ATT&CK hypotheses T1059.001 and T1105.
- [Network Traffic Analysis](projects/network-traffic-analysis.html) — PCAP generator, DNS/HTTP inspection, 18 tests, synthetic case report.
- [Recruiter overview](docs/RECRUITER_OVERVIEW.md) — skills mapped to public evidence.
- [SOC analyst workflow](projects/soc-analyst-workflow.html), [incident triage playbook](docs/SOC_TRIAGE_PLAYBOOK.md), and [analyst handoff template](docs/ANALYST_HANDOFF_TEMPLATE.md).
- [Detection evidence matrix](docs/DETECTION_EVIDENCE_MATRIX.md) and [résumé-ready project bullets](docs/RESUME_PORTFOLIO_BULLETS.md).
- [Celestial Resonance case study](projects/celestial-resonance.html) — responsible high-level summary of reproducible software research, quality gates, and auditability.
- [RAI case study](projects/research-ai-infrastructure.html) — high-level summary of evidence provenance, permission boundaries, and governed research tooling.
- [Future lab backlog](projects/PLANNED.md) — **planned**, not claimed as completed.

## Run all three security labs
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
```

Expected: **60 Python tests across three synthetic exercises** (31 authentication, 11 Windows process, 18 network). The authentication fixture flags one login sequence for `alice` from `192.0.2.15`; the process-creation fixture returns two triage candidates. None is proof of real intrusion or production security efficacy.

## Publish using GitHub Pages
Go to repository **Settings → Pages → Build and deployment → Deploy from a branch → main / (root)**. Save. After deployment, check the page in a private browser window. The website does not require JavaScript, frameworks, runtime credentials, analytics, third-party fonts, or paid hosting.

## Public disclosure and accuracy
- CR and RAI are **private** engineering projects. Do not publish their source, internal records, repository URLs, security-sensitive workflow details, or artifacts without a separate review.
- Case studies are based on high-level architecture and development methods, and **do not** establish a production security system, an independent penetration test, or quantified business/security gains.
- All three labs use synthetic events and reserved IPs/domains. No live network packets were captured or sent. The SPL query, upload-free smoke test and validation protocol are *drafts*, not an empirically validated deployed detection.
- Project status and evidence limitations are visible on each case-study page.
- CompTIA Security+ and CySA+ are listed based on the owner's report; no independent public verification or current-renewal status is asserted.

See [SECURITY.md](SECURITY.md) for disclosure handling and [PUBLICATION_CHECKLIST.md](PUBLICATION_CHECKLIST.md) before future updates.

## Structure
```text
index.html, styles.css               Static website
projects/*.html                    Employer-readable case studies
projects/01-authentication-detection/   Executable authentication lab
projects/02-windows-process-triage/     Executable Windows event triage lab
projects/03-network-pcap/              Generated PCAP exercise with source, tests, case report
docs/RECRUITER_OVERVIEW.md            Skills mapped to evidence
projects/PLANNED.md                Honest roadmap
.github/workflows/validate.yml      Small focused CI checks
```

## License
No public reuse license is granted at this time. All rights reserved unless specified otherwise.
