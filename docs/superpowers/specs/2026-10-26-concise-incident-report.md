# Concise incident report

User requested a concise report showing analysis, decisions and recommendations,
within 15-16 minutes. Reuse the completed AD analysis; do not start a new lab.
Produce a native employer-facing report and one-page downloadable PDF, linked
from the homepage, AD analyst brief and work-directory employer resources.

Use one editorial JSON source for both formats. Keep capture date distinct from
report preparation, source-reference links visible, compromise unconfirmed and
follow-up recommendations conditional. Do not imply containment, remediation,
notification, business impact or AD SPL/Sigma execution occurred.

Verify source references and HTML consistency, inspect the rendered one-page PDF,
check links and packaging, get bounded independent review, run existing Chrome
checks including PDF content/page count, then automatically merge and check live.

Rebuild with ReportLab 4.4.9: `python scripts/build_incident_brief.py`.
Read-only check: `python scripts/build_incident_brief.py --check-html`.
The PDF embeds ReportLab's bundled Bitstream Vera fonts for portable rendering.
