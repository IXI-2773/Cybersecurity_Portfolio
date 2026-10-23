# Portfolio release checklist — evidence-backed status

**Review date:** 2026-10-23  
**Candidate:** PR #1, `codex/portfolio-recruiter-refresh`  
**Release policy:** validate exact source revision, then obtain explicit publication/merge approval. A green PR does not establish a successful GitHub Pages deployment.

## Completed on the development branch

- [x] Keep a public-facing display name and contact address previously approved for the portfolio; do not add personal phone numbers.
- [x] Keep all four defensive exercises clearly described as synthetic or localhost-only and CR/RAI as summaries of private projects.
- [x] Exercise the 31 authentication, 11 endpoint, 18 packet, and 16 localhost-hardening Python tests in CI; preserve frozen fixture/data constraints.
- [x] Validate local page links, main navigation semantics, source-claim boundaries, and downloadable offline website bundle.
- [x] Review genuine Chrome captures for the main hiring surfaces and fix capture location so screenshot artifacts show the top of each page.
- [x] Generate and manually inspect a real Chrome **US-letter, one-page** recruiter PDF. A separate PDF-library CI check guards page count, size, and key content.
- [x] Maintain a source-backed live-site healthcheck covering all 16 HTML documents and essential CSS, diagrams, and public JavaScript modules. Its offline self-test is part of PR validation.

## Remaining publication gates

- [ ] Review the final exact-head Chrome screenshots and the new recruiter print artifact following the last typography adjustment.
- [ ] Confirm issuer-backed Security+ and CySA+ validity privately, or continue labeling them holder-reported without claiming independent verification.
- [ ] Perform a final manual privacy/source review (including internal URLs and third-party content); passing automated tests is not a substitute.
- [ ] Confirm the currently configured GitHub Pages publishing source in repository settings. No administrative publishing configuration was changed during this review.
- [ ] Approve and merge PR #1; **no merge authorization is implied by design-review requests**.
- [ ] After the intended Pages deployment, run the fixed-origin live check; verify the deployed commit and browser pages. Source CI and offline previews are not a live deployment test.
- [ ] Optional: screen-reader, zoom, and human-device visual review beyond the automated viewport checks.

## Source and claim guardrails

The five-of-five Splunk dashboard observation concerns frozen training events; indexing, scheduled alert firing, and production detection were not verified. The two public browser test engines are not the private CR or RAI runtime. Published certificates lack issuer-backed public validation. These qualifications must remain visible in the released pages and role-specific materials.

See `docs/RELEASE_READINESS_REVIEW_2026-10-23.md` for the actual screenshot/print review and `docs/DEPLOYMENT_VERIFICATION.md` for deployment checks.
