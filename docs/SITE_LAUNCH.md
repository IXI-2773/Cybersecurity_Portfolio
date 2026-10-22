# Portfolio website — published and source-code viewing

**Current Pages configuration:** Enabled. GitHub reported a successful Pages build and deployment for `IXI-2773/Cybersecurity_Portfolio` on October 22, 2026.

The source-code URL `github.com/IXI-2773/Cybersecurity_Portfolio/blob/main/projects/celestial-resonance.html` **always displays HTML source**. This is normal and separate from the published website.

## Open the rendered public site

- [Portfolio homepage](https://ixi-2773.github.io/Cybersecurity_Portfolio/)
- [Celestial Resonance](https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/celestial-resonance.html)
- [RAI](https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/research-ai-infrastructure.html)
- [Authentication detection](https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/authentication-detection.html)
- [Windows process triage](https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/windows-process-triage.html)
- [Network traffic analysis](https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/network-traffic-analysis.html)
- [Vulnerability remediation](https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/vulnerability-remediation.html)
- [SOC analyst workflow](https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/soc-analyst-workflow.html)

## Verify a future deployment

1. Review [GitHub Actions](https://github.com/IXI-2773/Cybersecurity_Portfolio/actions) for **pages build and deployment**. A successful status means GitHub reported publication success.
2. Inspect the separate **Verify live GitHub Pages site** workflow; this checks HTTP availability of the homepage, seven case-study pages, and two static assets.
3. If you see a browser 404, confirm the exact URL, clear a stale cache and check GitHub Pages settings/status. A completed normal Python CI workflow does **not** establish successful web hosting.

## Offline alternative

Download the `cybersecurity-portfolio-site` artifact from a successful [portfolio CI run](https://github.com/IXI-2773/Cybersecurity_Portfolio/actions); extract the ZIP and open `index.html`. This is an offline preview, not a publicly hosted domain.

## GitHub-native reading

All six project descriptions are also provided as [GitHub-rendered Markdown case studies](../projects/CASE_STUDIES.md). They work inside GitHub without GitHub Pages.

The public CR and RAI pages are safe high-level descriptions; private source and internal records remain undisclosed.
