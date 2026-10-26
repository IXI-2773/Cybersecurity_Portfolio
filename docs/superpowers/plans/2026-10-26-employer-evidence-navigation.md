# Employer Evidence Navigation Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans inline; one final independent review.

**Goal:** Let employers map skills to existing proof and follow one coherent visual portfolio.
**Architecture:** Static links, shared existing header/footer and scoped additions to portfolio.css. Preserve public workbench JavaScript and factual content.
**Tech Stack:** HTML, CSS, existing Python/Selenium checks.
**Spec:** ../specs/2026-10-26-employer-evidence-navigation-design.md

## Global Constraints

- Four homepage skill destinations; no ratings or unsupported execution claims.
- Restyle roles.html, verify.html, apply.html, recruiter.html and test-lab.html.
- Preserve IDs, source/download links, controls, disclosures and résumé files.
- Keep GIF and live-Splunk-pending status intact; no dependencies or backend work.

## Review Focus

- No-script skill and employer navigation reaches the promised page.
- Mobile controls, long addresses and tables stay inside the viewport.
- Public teaching-engine baseline, changed window and hold scenarios still work.
- Recruiter print preserves text and hides browser-only controls.
- Evidence distinctions and link destinations survive visual cleanup.

## Task 1: Homepage skill navigation and employer presentation

- [ ] Add four semantic skill links in index.html, reusing the approved cases.
- [ ] Share homepage chrome across five employer pages; add current-page employer navigation.
- [ ] Style the skill list and scoped employer layouts in portfolio.css; keep form and disclosure behavior native.
- [ ] Update visual-review page coverage, exercise skill navigation without scripts, and check actual public engine controls.
- [ ] Run existing static/evidence/bundle checks and required Chrome CI; review desktop/mobile and print output once.
- [ ] Independent whole-diff review, batch consequential fixes, then merge the reviewed head after checks pass.

## Progress

Planning complete. Reversible presentation work uses existing static checks and
real browser journeys; no tests will merely assert CSS implementation details.
Ruling: keep one shared stylesheet, matching the existing deployment validator's
single-stylesheet contract and avoiding an extra asset on every route.
