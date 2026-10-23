# Portfolio recruiter refresh

Goal: make the existing GitHub Pages portfolio easier for a hiring manager to scan and inspect.

Approach: retain the static HTML/CSS architecture, genuine Splunk screenshot, all six case studies, approved contact and current credentials wording. Consolidate repeated homepage summaries into one visual project gallery. A framework migration would add maintenance without improving this task; another new lab would leave the presentation problem unresolved.

- [x] Rework index.html into a clear introduction, featured investigation, four public labs, two smaller engineering summaries, methodology, background and contact.
- [x] Scope the new layout to the homepage in styles.css; keep existing case pages stable. Use existing evidence images and CSS data visuals; keep training data distinct from application screenshots.
- [x] Retain legacy anchor destinations, mobile navigation parity, keyboard focus, reduced motion and source links. Promote the existing recruiter profile and text resume download.
- [x] Run existing link, accessibility and evidence audits. Inspect the desktop browser rendering. Run the existing responsive workflow after pushing when available; do not rerun unrelated security-lab tests locally.
- [x] Commit and publish a reviewable branch/PR with exact verification limits.

Execution: inline, using the user's standing preference to proceed automatically. This is a reversible presentation edit, with no changes to detectors, lab fixtures or credential claims.

Local verification: all 12 HTML pages pass the structural accessibility audit; 200 local links resolve; evidence consistency passes. Desktop hero and gallery visually inspected through the browser. Responsive checks extended to exercise both native evidence disclosures and run on PRs; narrow-screen browser results pending CI.

PR #1 verification on bcac75d: both CI workflows passed. Chrome report: 18 page/viewport combinations, zero failures, actual homepage widths 320/390/768/1280 and matching document widths. Narrow-screen hero screenshots inspected. Independent review found one retained-anchor offset regression after moving IDs onto inner containers; corrected by applying the 100px scroll margin to those three targets. No other consequential findings. Update is on the PR branch, not deployed to main.
