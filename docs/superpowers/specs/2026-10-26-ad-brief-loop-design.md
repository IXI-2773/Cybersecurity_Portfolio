# AD analyst brief and looping Signal to Case

The owner approved a concise brief within the AD investigation and requested that
the homepage animation loop. This supersedes the one-cycle motion decision in
2026-10-26-homepage-animation-design.md; the original art and 4.8-second cycle stay.

Place the brief immediately after the AD introduction. Reuse CASE_REPORT.md and
its source chronology for assessment, observed scope, priority/impact reasoning,
key times, evidence strength and recommended follow-up. Link to the existing
workbench, source index and full report. Preserve independent recorded-emulation
scope, legitimate administration alternatives, and the distinction between event
and collection time. No new incident result, severity score or impact is invented.

Build a GIF with infinite repetition, retaining the payload budget. The controller
loops while visible, pauses offscreen/hidden and resumes on return. Manual stop
and interactive-inspector selection persist until Play. Reduced motion uses the
poster; without JavaScript the initial image is also static, avoiding an
uncontrollable loop. Reuse one cached GIF URL rather than fetching each cycle.

Implement inline in projects/ad-attack-chain.html, portfolio.css, index.html,
assets/js/signal-animation.js and scripts/build_signal_animation.py. Extend the
existing Chrome checks for activity past one cycle, persistent manual stop,
visibility resume, reduced-motion and no-script alternatives. Verify source
chronology, static structure, links and generated GIF metadata; review the diff
independently and inspect desktop/mobile once before automatic merge.
