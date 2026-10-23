# Recruiter journey review — 2026-10-23

## Method and limitation

Internal, task-based review of the current portfolio development branch. This is a heuristic review backed by source inspection and automated Chrome navigation—not an external recruiter study, a measured conversion test, a complete visual design audit, or WCAG certification.

The three tasks are:
1. **Find relevant work:** homepage → role-specific path → SOC/security/automation case study.
2. **Verify the claim:** role/evidence directory → underlying report, genuine Splunk observation, or public implementation → stated scope.
3. **Access application material:** homepage → actual SOC résumé download; one-page recruiter profile → résumé-choice page → SOC/Security Analyst text downloads.

## Material corrections

| Issue observed | Corrective action | Regression check |
| --- | --- | --- |
| Hero label "View resume" opened a one-page web profile, not an actual résumé | Relabel profile honestly and expose the existing SOC Analyst `.txt` download directly | Static CTA checks and existing relative-file/link audit |
| Recruiter profile label implied a download but opened a two-role selection page | Rename to "Choose ATS résumé" | Real browser navigation to both download choices |
| Several case/source links opened raw Markdown in the hosted site rather than a readable GitHub report | Link reports and analyst workflow documents to the existing GitHub source viewer | Source-link contract, local link audit and recorded path checks |
| Newly authored browser engine/test source links targeted `main`, where those files have not yet been merged | Point the relevant source links to an immutable, reviewable commit | Reviewable GitHub source pinned to previously passed application-code commit `d8aee1e38d4931e32a057980b4fdffbf82c68901` |
| Individual browser pages passed but the homepage-to-role and profile-to-download paths were not exercised end-to-end | Add two short real-browser journeys to the existing Chrome workflow | Chrome test follows both destinations and checks visible controls |

## Evidence boundary

The Splunk 5/5 result is a screenshot-reviewed match against a frozen synthetic set, not a production accuracy rate. The Windows/PCAP/HTTP labs are generated or localhost-only. Public browser teaching engines are independent of private CR and RAI implementations. Certification status is owner-reported, not independently verified. No result of the reviewer workflow is evidence of an external recruiter endorsement.

## Verification and release gate

The GitHub Actions validation and Chrome responsive-review workflows are the acceptance gates. Their exact run links and outcomes belong in the PR description after completion. This report documents what was changed; it does not assert that unrun tests have passed.

Before publishing, retain human review of the screenshots and print output, make an explicit merge decision, and verify the actual GitHub Pages deployment. The existing PR stays unmerged until authorized.
