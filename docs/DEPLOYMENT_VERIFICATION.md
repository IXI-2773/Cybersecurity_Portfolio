# Public Website Deployment Verification

**Owner:** Don Lopez  
**Hosting:** GitHub Pages, repository `IXI-2773/Cybersecurity_Portfolio`  
**Live origin:** https://ixi-2773.github.io/Cybersecurity_Portfolio/

## Two independent checks

**A. Source-code CI** (`.github/workflows/validate.yml`) verifies Python lab tests, static links, data fixtures, and offline website packaging. This does **not** prove that GitHub Pages serves the result.

**B. Pages publishing / live HTTP checks:**
- GitHub's **pages build and deployment** workflow provides deployment status.
- The separate [Verify live GitHub Pages site](../.github/workflows/check-live-pages.yml) workflow can be triggered manually, runs weekly, and attempts to run after Pages deployment completes.
- Its [fixed-origin Python healthcheck](../scripts/check_live_site.py) checks HTTP 200, HTML MIME, document title, H1, CSS, the homepage's CR/vulnerability links, and selected shared assets.
- Requests stay on the public Pages host; HTTP redirects are not followed. The checker allows limited retries for deployment propagation.

## What this proves — and what it does not

Passing all probes shows the public pages and essential static assets were served with expected content during the run. It does not establish visual layout in all browsers, WCAG compliance, service uptime guarantees, vulnerability resistance, or authenticity of synthetic security investigations.

The independent PCAP and localhost hardening labs remain artificial exercises. Likewise, publishing CR and RAI summaries does not disclose their private implementations.

## For troubleshooting a failed run

1. Confirm GitHub's Pages deployment actually completed on the intended `main` revision.
2. Inspect the failed path and error in the checker output.
3. Check for changed capitalization or missing relative links in the HTML.
4. Check whether GitHub Pages is still propagating; rerun the checker after verifying the new deployment.
5. Do not weaken expected page/title/asset assertions to conceal genuine failures.
