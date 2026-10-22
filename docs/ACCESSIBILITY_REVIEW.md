# Website Accessibility & Responsive Review

**Scope:** Public portfolio homepage, its project pages, and navigation on narrow screens. This review uses static analysis and live HTTP checks; it is **not** a complete WCAG conformance assessment.

## Improvements shipped

- A responsive **native HTML details/summary mobile menu** on all public HTML pages. It requires no JavaScript and can be opened using keyboard controls.
- The desktop navigation is hidden at viewports under 800px; the mobile menu contains **exactly the same destinations**.
- The evidence table supports keyboard focus and is labeled as a horizontally scrollable region.
- A clear focus outline on the menu, evidence table, and other interactive links.
- Sticky header anchor offsets so section navigation does not conceal headings.
- Additional reduced-motion handling for hover effects.
- Corrected a stale homepage authentication test count (31 rather than 21) and a stale count of analyst examples (three rather than two).

## Fast regression checks

Run:

```sh
python scripts/check_accessibility.py
python scripts/check_links.py
```

These checks enforce document language, viewport settings, main/H1/skip semantics, mobile/desktop navigation parity, descriptive image alt presence, safe new-tab links, functional local fragment destinations, and availability of essential CSS rules. They run without installing browsers or new Python libraries.

## Remaining validation (not claimed complete)

- Browser screenshots at 320px, 390px, 768px, 1280px and 1440px widths.
- VoiceOver/NVDA keyboard and reading-order review.
- Automated contrast analysis with actual computed CSS colors and browser focus states.
- Browser zoom up to 200%, text spacing and OS-level high-contrast modes.

Live GitHub Pages HTTP verification is handled by a separate workflow; it checks that public pages and assets are served, but **cannot establish responsive visual quality**.

## Browser screenshots and width checks

A separate **Review responsive website in Chrome** workflow runs only for changes to HTML/CSS or the visual-check tooling, not for ordinary detection-lab changes. It uses a headless Chrome/ChromeDriver installation included on the GitHub Ubuntu 24.04 runner, plus a small Selenium library.

The [responsive checker](../scripts/visual_review.py) tests four homepage widths (**320, 390, 768 and 1280 pixels**) and mobile/desktop widths for three project case studies. It checks:
- Whether the native mobile navigation can open and close using keyboard Enter.
- Whether mobile and desktop navigation are shown at the appropriate breakpoint.
- Whether main page headings are visible.
- Whether the document introduces unintended horizontal overflow.

Results and **10 actual browser screenshots** are uploaded as the `responsive-website-review` Actions artifact when the job executes. This is a real headless Chrome rendering, not a synthetic visualization; however, screenshots still require human visual review and do not establish WCAG conformance or full accessibility.

## Human screenshot review — October 22, 2026

The ten screenshots from workflow run [39854646324](https://github.com/IXI-2773/Cybersecurity_Portfolio/actions/runs/39854646324) were inspected, not just counted. They include the homepage at 320, 390, 768 and 1280 pixels, and CR, Network and Vulnerability pages at 390 and 1280 pixels.

**Observed issues and corrections:**
- At 1280px, the synthetic detector's green status line was cut off after the explanation of a non-incident. The terminal status is now allowed to wrap rather than inherit `white-space: nowrap`.
- At 320px, the homepage headline and upper whitespace consumed most of the initial viewport. Mobile spacing and heading sizing were reduced to make the main project action easier to find.

The Chrome workflow now checks the terminal status element for internal overflow and tests whether the primary project action starts within the first small-mobile viewport. It still cannot guarantee visual perfection or complete WCAG conformance.

**No observed issue:** The sampled case-study screenshots show readable titles, appropriate native mobile navigation and consistent visual hierarchy. Browser automation previously reported zero page-level horizontal overflow.

## Screenshot comparison follow-up

A before/after review of the real 320px, 390px and 1280px Chrome snapshots confirmed that mobile whitespace and headline height were reduced and the desktop detector disclaimer now wraps rather than being truncated.

**Remaining observation at 320px:** The primary project action was still at the very bottom of the initial viewport. The hero introduction has been shortened to make the action easier to reach, and the browser regression now requires that the **entire button** fit within the initial 320 × 720 viewport, not just its top edge.

This visual review is limited to the captured viewports. Full keyboard navigation beyond the compact menu, contrast at every state, and screen-reader testing remain open work.
