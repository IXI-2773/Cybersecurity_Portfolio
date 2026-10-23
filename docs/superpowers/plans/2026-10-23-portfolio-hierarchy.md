# Portfolio Hierarchy Implementation Plan

> Execute inline, using the existing portfolio validation and Chrome review.

**Goal:** Make project proof easier to scan while reducing CSS maintenance.
**Architecture:** Existing dependency-free HTML, shared stylesheet and native links.
**Tech Stack:** HTML, CSS, existing Python checks and Selenium CI.
**Spec:** `docs/superpowers/specs/2026-10-23-portfolio-hierarchy-design.md`

## Global constraints

- Retain Don Lopez, existing pages, evidence qualifiers and private-project limits.
- Add no dependencies to the site and make no new security or credential claims.
- Continue PR #3 without merging or deploying it.

## Review focus

320px overflow, first-screen primary action, keyboard navigation, genuine versus
synthetic evidence, and printable résumé regressions are covered by existing
`scripts/visual_review.py` and `scripts/check_case_evidence.py`.

## Tasks

- [x] Remove rules requiring classes absent from every HTML/JS/SVG source; retain
  selector functions conservatively. Remove earlier declarations superseded by
  the same selector/property/importance/condition. Preserve surviving order.
- [x] Run existing source/link/accessibility/evidence checks; commit CSS cleanup.
- [ ] Edit `index.html` and existing component CSS: remove repeated proof band,
  move replay after gallery, improve card result/evidence hierarchy and actions.
- [ ] Run focused checks and offline packaging; update the existing PR branch.
- [ ] Run existing Chrome CI, inspect screenshots and print artifacts, and review
  the final diff. Record verification and remaining limits in the PR.
