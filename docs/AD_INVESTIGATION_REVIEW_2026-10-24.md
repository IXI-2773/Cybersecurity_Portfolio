# Recorded Active Directory investigation review

Scope: independent analysis of pinned OTRF PurpleSharp AD Playbook I telemetry. Implementation plan: [2026-10-24-ad-investigation.md](superpowers/plans/2026-10-24-ad-investigation.md).

## Source verification

A fresh, read-only source reviewer independently checked the original archives against all 226 retained host field excerpts and original-line hashes, all 31 retained packet hashes/timestamps/request lines, and all 24 clock calibration pairs across four hosts. The reviewer confirmed direct GUID/session joins, missing client-IP handling, weaker network association language, and the twelve excluded ticket controls. No Critical or Important source/evidence issue was found.

The executed Python suite has 23 focused tests. Full-capture regeneration agrees with frozen source references and the committed JSON/CSV/browser artifacts. SPL and Sigma remain unexecuted candidate translations. Dataset limitations and alternative explanations appear in the public report.

## Browser and visual verification

Chrome checks cover 1280, 390 and 320-pixel viewports, source/target selection, collection-clock movement, packet tuple inspection, negative controls, focus retention, reduced motion, offscreen pause and no-script fallbacks. The first run passed all behavioral checks and site validation. One batched visual review of desktop/mobile panels found a material readability issue: mobile SVG labels scaled to approximately five pixels.

A rendered-label-size regression now requires a minimum 10-pixel height at each supported viewport. The regression failed as intended at 390px with a rendered label height of 6px (Chrome run40118829662). The bounded correction preserves the chart's width inside a keyboard-focusable horizontal scrolling region while containing page overflow. Final run/deployment references will be recorded after verification.

## Deferred minor

The generic packet request-line recognizer can accept an unterminated partial HTTP version/line. All 31 request lines used by this pinned case were independently verified complete in the original packets, so the published findings are unaffected. Reuse against a different capture should first require a complete version and CRLF-terminated request line.

## Explicit decisions

- Infer the capture-local UTC−04:00 offset only after checking all 24 Sysmon process-start pairs; retain native and collection clocks. An incorrect offset would distort cross-source ordering.
- Keep production detection performance, streaming behavior and SPL/Sigma backend deployment unvalidated. Capture correctness cannot establish deployment readiness.
- Leave encrypted/reassembled content and exhaustive payload analysis outside this bounded parser. Intent, password reuse/cracking, persistence and exfiltration remain unproven.
- Attribute capture creation to OTRF and independent analysis to the portfolio owner. Unread LinkedIn honors and unrelated portfolio content are unchanged.
