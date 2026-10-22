# Don Lopez — Cybersecurity Portfolio Case Studies

**GitHub-readable edition.** These Markdown pages display properly in GitHub **today**. They are an alternative to HTML files, which GitHub's Code tab displays as raw source until the separate Pages website is published.

| Case study | Public evidence | Status |
| --- | --- | --- |
| [Authentication detection and triage](authentication-detection.md) | Synthetic login correlation, expected findings, case report, 31 tests | Offline verified; Splunk pending |
| [Windows process execution triage](windows-process-triage.md) | Fabricated Windows Event 4688 data and rule analyzer, 11 tests | Offline verified |
| [Network traffic analysis](network-traffic-analysis.md) | Generated PCAP, visual evidence, incident report, 18 tests | Offline verified; Wireshark GUI pending |
| [Vulnerability remediation](vulnerability-remediation.md) | Loopback-only before/after assessment, four resolved toy findings, 16 tests | Offline verified |
| [Celestial Resonance](celestial-resonance.md) | Review-safe engineering principles | Private implementation; no production security claim |
| [Research AI Infrastructure](research-ai-infrastructure.md) | Evidence provenance, uncertainty and authority controls | Private implementation; no autonomous SOC claim |

**Credentials:** [CompTIA Security+ and CySA+](../docs/CREDENTIALS.md), reported by the portfolio owner; public badge verification not yet linked.

**Total:** 76 automated Python tests across four public synthetic labs. The [GitHub CI workflow](../.github/workflows/validate.yml) runs them.

For the fully styled HTML site, use [GitHub Pages](../docs/SITE_LAUNCH.md) once enabled in repository settings. For an **offline styled preview** that does not require Pages, download `cybersecurity-portfolio-site.zip` from the latest successful [GitHub Actions run](https://github.com/IXI-2773/Cybersecurity_Portfolio/actions) and open `index.html` inside the extracted folder.
