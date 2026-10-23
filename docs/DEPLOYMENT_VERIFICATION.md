# Public Website Deployment Verification

**Owner:** Don Lopez  
**Hosting:** GitHub Pages, repository `IXI-2773/Cybersecurity_Portfolio`  
**Live origin:** https://ixi-2773.github.io/Cybersecurity_Portfolio/

## Two independent checks

**A. Source-code CI** (`.github/workflows/validate.yml`) verifies Python lab tests, static links, data fixtures, and offline website packaging. This does **not** prove that GitHub Pages serves the result.

**B. Pages publishing / live HTTP checks:**
- GitHub's **pages build and deployment** workflow provides deployment status.
- The separate [Verify live GitHub Pages site](../.github/workflows/check-live-pages.yml) workflow can be triggered manually, runs weekly, and attempts to run after Pages deployment completes.
- Its [fixed-origin Python healthcheck](../scripts/check_live_site.py) checks HTTP 200, HTML MIME, title and H1 for all 16 portfolio HTML pages; it also checks the homepage's core hiring/evidence links plus essential CSS, JavaScript engines and illustrations.
- Requests stay on the public Pages host; HTTP redirects are not followed. The checker allows limited retries for deployment propagation.

## What this proves — and what it does not

Passing all probes shows the listed public pages and essential static assets were served with expected content during the run. It does not establish visual layout in all browsers, WCAG compliance, service uptime guarantees, vulnerability resistance, or authenticity of synthetic security investigations.

The independent PCAP and localhost hardening labs remain artificial exercises. Likewise, publishing CR and RAI summaries does not disclose their private implementations.

## For troubleshooting a failed run

1. Confirm GitHub's Pages deployment actually completed on the intended `main` revision.
2. Inspect the failed path and error in the checker output.
3. Check for changed capitalization or missing relative links in the HTML.
4. Check whether GitHub Pages is still propagating; rerun the checker after verifying the new deployment.
5. Do not weaken expected page/title/asset assertions to conceal genuine failures.

## Source-to-deployment release order

1. Obtain explicit approval to merge PR #1; successful pull-request CI does not merge or deploy anything.
2. In repository **Settings → Pages**, verify a supported publishing source points to the intended branch and root. If this setting cannot be read, record it as unverified.
3. Confirm Pages build/deployment succeeded on the intended commit, rather than inferring production status from branch CI.
4. Run the read-only live-site workflow for all 16 HTML pages and public static assets and compare the deployed content against the expected release revision.
5. Keep the release on HOLD if Pages is unavailable, a live response check fails, source contents differ, or the privacy/issuer review is unresolved.

Review record: [2026-10-23 release readiness](RELEASE_READINESS_REVIEW_2026-10-23.md).
