# Homepage animation

The employer-facing homepage needs a focal animation and a simpler AD case link.
Keep the existing green visual identity, authentic evidence images, three featured
investigations and interactive Signal to Case inspector.

## Direction

Use a locally authored, finite GIF in the existing Signal to Case visual area.
Five failure lanes and one success lane converge at the inclusive 600-second rule
window, then an amber review decision. Source: the canonical public synthetic
authentication boundary scenario. This explains a rule; it is not live telemetry
or proof of a fired alert. No new case results are claimed.

The main link becomes “View AD case study,” with no arrow icon. Keep its route.

## Implementation choices

An actual GIF satisfies the requested medium without a library, video service or
external asset. A purely decorative stock GIF would add download cost without
showing investigation reasoning. A second independent JavaScript workbench would
duplicate the existing inspector. Reuse its controls and chart instead.

Budget: under 250KB, 4.8 seconds, one automatic play on first visibility. Then a
static final frame; explicit replay and stop controls. Stop when hidden/offscreen,
with no automatic restart. Reduced motion uses a still image before scripts run.
Selecting the existing inspector controls switches to its actual fixture chart.
Animation replay resets the inspector so two independent replays never run at once.

Generate both assets with scripts/build_signal_animation.py; verify source counts,
group identity, boundary duration, finite playback and payload size. Extend the
existing Chrome check for playback/stop, inspector handoff, offscreen stopping and
reduced motion. Include the GIF in the offline bundle and deployed asset checks.
Inspect desktop/mobile together, batch any fixes, and merge after review and CI.
