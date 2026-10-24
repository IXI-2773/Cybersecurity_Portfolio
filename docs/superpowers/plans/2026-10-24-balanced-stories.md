# Balanced portfolio stories Implementation Plan

> Execute inline with superpowers:executing-plans. The owner requires the same assistant to implement and review; do not delegate.

**Goal:** Make the portfolio explain Don Lopez's qualifications and work with substantial cases and meaningful interaction.

**Architecture:** Retain static HTML/CSS and existing routes. A small shared JS module owns pure demo decisions and progressively enhanced UI; content stays readable without scripts.

**Tech Stack:** HTML, CSS, SVG geometry, vanilla JavaScript, Node assertions, Python/Selenium CI.

**Spec:** `docs/superpowers/specs/2026-10-24-balanced-stories-design.md`

## Global Constraints

- Preserve master and public resume PDFs; private identity and source remain outside public content.
- Preserve existing labs, fixtures, routes and approved light/green reading style.
- Label example data and private-demo boundaries; separate resume labs and planned projects.
- No new runtime dependencies or fake awards, screenshots, metrics or completed projects.
- Same assistant performs implementation and review; publish only after checks pass.

## Review Focus

- A late revision requested before release must HOLD, including exact release-date acceptance.
- Missing evidence and attribution mismatch must not become supported conclusions.
- Play/Step/Reset, repeated use and reduced motion must remain deterministic.
- Small screens and no-script readers must retain all content and navigation.
- New content must not claim missing original evidence or planned work was executed.

## Tasks

- [x] 1. Add `scripts/test_portfolio_systems.cjs` before `assets/js/portfolio-systems.js`; observe RED, then implement pure `evaluateCR` and `evaluateRAI` decisions and progressive controls. Test malformed dates, exact release date, missing coverage, conflict, invalid attribution and supported records.
- [x] 2. Update `index.html`, `explore.html`, CR/RAI and existing security case HTML; create three resume-lab and three planned-project pages plus `awards.html`. Extend `portfolio.css` for finite system motion, reading hierarchy, responsive diagrams and empty state. Create a maintainer awards guide.
- [x] 3. Update sitemap, evidence index, packaging/live checks, CI and browser review. Check all new destinations without scripts and the two interactive demos with scripts, keyboard and reduced motion.
- [ ] 4. Run focused local checks, publish isolated PR, inspect desktop/mobile browser artifacts in one batch, repair any defects, verify exact-head CI, merge and confirm live deployment.

## Execution record

- Approved balanced direction and direct execution in the conversation.
- Existing checkout is isolated and clean; branch starts at published main.
- Native skill launchers are unavailable in this environment; use the read skill guidance and repo tools directly.
- Spec and implementation plan share the catalog/demonstration interfaces above; no interface conflicts found.
