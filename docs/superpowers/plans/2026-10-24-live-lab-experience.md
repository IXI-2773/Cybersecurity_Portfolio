# Live Lab Experience Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Present completed Kali/VM/network experience with stronger real imagery and add a sourced CSUSB campus gallery.

**Architecture:** Reuse the existing Kali case route and public network artifacts, keeping owner-confirmed experience separate from reproducible fixture evidence. Add two licensed campus assets and a small responsive gallery without new dependencies.

**Tech Stack:** Static HTML/CSS, Python verification scripts, existing Selenium visual review, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-10-24-live-lab-experience-design.md`

## Global Constraints

- Preserve both résumé PDFs and keep the transcript outside git.
- Keep planned phishing, identity/MFA and SOC automation briefs marked planned.
- Never label a reference image as an original lab capture.
- Preserve the 20-packet public fixture boundary separately from the résumé-reported 5,000+ packet experience.
- Add no runtime dependency.

## Review Focus

- Completed experience must not retain “proposed” or “not executed” wording on the Kali/VM case.
- Reference images must retain attribution and visible scope labels.
- Network claims must distinguish owner-reported broader work from the reproducible public fixture.
- The image gallery must avoid horizontal overflow and retain useful alt text on mobile.
- New image files must stay below the existing live-response size ceiling.

---

### Task 1: Lock the experience and image boundaries

**Files:**
- Modify: `scripts/check_case_evidence.py`
- Test: `scripts/check_case_evidence.py`

### Task 2: Add licensed campus imagery

**Files:**
- Create: `assets/reference/csusb-jack-brown-hall.webp`
- Create: `assets/reference/csusb-university-entrance.webp`
- Modify: `education.html`
- Modify: `visual-credits.html`
- Modify: `portfolio.css`

### Task 3: Convert the Kali/VM case into completed experience

**Files:**
- Modify: `projects/kali-defender-visibility.html`
- Modify: `projects/kali-defender-visibility.md`
- Modify: `projects/network-intrusion-lab.html`
- Modify: `projects/network-intrusion-lab.md`

### Task 4: Promote the live experience on employer entry pages

**Files:**
- Modify: `index.html`
- Modify: `explore.html`
- Modify: `README.md`
- Modify: `projects/CASE_STUDIES.md`

### Task 5: Verify and publish

**Files:**
- Modify: `scripts/check_live_site.py`
- Modify: `scripts/visual_review.py`
- Modify: relevant workflow path filters when required.
