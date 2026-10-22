# Cybersecurity Portfolio — Brandon J. Lopez Moya

A public, static portfolio presenting **verified hands-on defensive security exercises** alongside **high-level case studies of private engineering work**.

**Live website (after GitHub Pages is enabled):** https://ixi-2773.github.io/Cybersecurity_Portfolio/

## Start here
- [Portfolio home](index.html) — skills and project index.
- [Authentication detection case study](projects/authentication-detection.html) — reproducible, synthetic Python lab, nine tests, and an **unvalidated** Splunk SPL example.
- [Celestial Resonance case study](projects/celestial-resonance.html) — responsible high-level summary of reproducible software research, quality gates, and auditability.
- [RAI case study](projects/research-ai-infrastructure.html) — high-level summary of evidence provenance, permission boundaries, and governed research tooling.
- [Future lab backlog](projects/PLANNED.md) — **planned**, not claimed as completed.

## Run the authentication lab
Requires Python 3.10+; no dependencies or cloud resources.

```bash
cd projects/01-authentication-detection
python -m unittest -v
python detect_auth.py auth_events.csv
```

Expected: nine focused passing tests and one flagged **synthetic** suspicious login sequence for `alice` from `192.0.2.15` after six failures. The output is a triage signal, **not evidence of a real intrusion**.

## Publish using GitHub Pages
Go to repository **Settings → Pages → Build and deployment → Deploy from a branch → main / (root)**. Save. After deployment, check the page in a private browser window. The website does not require JavaScript, frameworks, runtime credentials, analytics, third-party fonts, or paid hosting.

## Public disclosure and accuracy
- CR and RAI are **private** engineering projects. Do not publish their source, internal records, repository URLs, security-sensitive workflow details, or artifacts without a separate review.
- Case studies are based on high-level architecture and development methods, and **do not** establish a production security system, an independent penetration test, or quantified business/security gains.
- The lab uses fabricated events and reserved documentation IPs. The SPL query is a *concept*, not an empirically validated deployed detection.
- Project status and evidence limitations are visible on each case-study page.
- No certifications beyond the stated degree are asserted.

See [SECURITY.md](SECURITY.md) for disclosure handling and [PUBLICATION_CHECKLIST.md](PUBLICATION_CHECKLIST.md) before future updates.

## Structure
```text
index.html, styles.css               Static website
projects/*.html                    Employer-readable case studies
projects/01-authentication-detection/   Executable defensive lab
projects/PLANNED.md                Honest roadmap
.github/workflows/validate.yml      Small focused CI checks
```

## License
No public reuse license is granted at this time. All rights reserved unless specified otherwise.
