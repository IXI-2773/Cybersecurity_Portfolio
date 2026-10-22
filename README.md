# Cybersecurity Portfolio — Don Lopez

A public, static portfolio presenting **reproducible synthetic defensive security exercises** alongside **high-level case studies of private engineering work**.

**Live website (after GitHub Pages is enabled):** https://ixi-2773.github.io/Cybersecurity_Portfolio/

## Start here
- [Portfolio home](index.html) — skills and project index.
- [Authentication detection case study](projects/authentication-detection.html) — reproducible, synthetic Python lab, 31 authentication tests, a simulated SOC investigation report, and a **Splunk runtime qualification package (not yet executed in Splunk)**.
- [Windows process execution triage case study](projects/windows-process-triage.html) — synthetic Windows Event ID 4688 exercise, 11 tests, ATT&CK hypotheses T1059.001 and T1105.
- [Recruiter overview](docs/RECRUITER_OVERVIEW.md) — skills mapped to public evidence.
- [Celestial Resonance case study](projects/celestial-resonance.html) — responsible high-level summary of reproducible software research, quality gates, and auditability.
- [RAI case study](projects/research-ai-infrastructure.html) — high-level summary of evidence provenance, permission boundaries, and governed research tooling.
- [Future lab backlog](projects/PLANNED.md) — **planned**, not claimed as completed.

## Run both security labs
Requires Python 3.10+; no dependencies or cloud resources.

```bash
python -m unittest discover -s projects/01-authentication-detection -p 'test_*.py' -v
python -m unittest discover -s projects/02-windows-process-triage -p 'test_*.py' -v
python projects/01-authentication-detection/detect_auth.py projects/01-authentication-detection/auth_events.csv
python projects/01-authentication-detection/validate_matrix.py
# The next step requires an authorized Splunk instance; see SPLUNK_RUNBOOK.md
python projects/02-windows-process-triage/process_triage.py projects/02-windows-process-triage/events_4688.csv
```

Expected: 42 locally passing tests across two synthetic exercises. The authentication fixture flags one login sequence for `alice` from `192.0.2.15`; the process-creation fixture returns two triage candidates. None is proof of real intrusion or production security efficacy.

## Publish using GitHub Pages
Go to repository **Settings → Pages → Build and deployment → Deploy from a branch → main / (root)**. Save. After deployment, check the page in a private browser window. The website does not require JavaScript, frameworks, runtime credentials, analytics, third-party fonts, or paid hosting.

## Public disclosure and accuracy
- CR and RAI are **private** engineering projects. Do not publish their source, internal records, repository URLs, security-sensitive workflow details, or artifacts without a separate review.
- Case studies are based on high-level architecture and development methods, and **do not** establish a production security system, an independent penetration test, or quantified business/security gains.
- Both labs use fabricated events and reserved documentation IPs or domains. The SPL query, upload-free smoke test and validation protocol are *drafts*, not an empirically validated deployed detection.
- Project status and evidence limitations are visible on each case-study page.
- No certifications beyond the stated degree are asserted.

See [SECURITY.md](SECURITY.md) for disclosure handling and [PUBLICATION_CHECKLIST.md](PUBLICATION_CHECKLIST.md) before future updates.

## Structure
```text
index.html, styles.css               Static website
projects/*.html                    Employer-readable case studies
projects/01-authentication-detection/   Executable authentication lab
projects/02-windows-process-triage/     Executable Windows event triage lab
docs/RECRUITER_OVERVIEW.md            Skills mapped to evidence
projects/PLANNED.md                Honest roadmap
.github/workflows/validate.yml      Small focused CI checks
```

## License
No public reuse license is granted at this time. All rights reserved unless specified otherwise.
