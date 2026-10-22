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
