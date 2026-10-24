#!/usr/bin/env python3
"""Render deterministic, accessible SVG summaries from checked case results."""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path


TOP_LEVEL = {
    "case_id": str,
    "title": str,
    "status": str,
    "metrics": list,
    "timeline": list,
    "findings": list,
}
NESTED = {
    "metrics": {"label": str, "value": str},
    "timeline": {"time": str, "label": str, "state": str},
    "findings": {"id": str, "label": str, "severity": str},
}


def validate_summary(data: dict) -> None:
    if not isinstance(data, dict):
        raise ValueError("summary must be an object")
    for key, expected_type in TOP_LEVEL.items():
        if key not in data:
            raise ValueError(f"missing required key: {key}")
        if not isinstance(data[key], expected_type):
            raise ValueError(f"{key} must be {expected_type.__name__}")
        if isinstance(data[key], str) and not data[key].strip():
            raise ValueError(f"{key} must not be empty")
    limits = {"metrics": (1, 4), "timeline": (1, 6), "findings": (1, 4)}
    for group, fields in NESTED.items():
        minimum, maximum = limits[group]
        if not minimum <= len(data[group]) <= maximum:
            raise ValueError(f"{group} must contain {minimum} to {maximum} items")
        for index, item in enumerate(data[group]):
            if not isinstance(item, dict):
                raise ValueError(f"{group}[{index}] must be an object")
            for field, expected_type in fields.items():
                if field not in item or not isinstance(item[field], expected_type) or not item[field].strip():
                    raise ValueError(f"{group}[{index}] requires non-empty {field}")


def _safe(value: str, maximum: int = 58) -> str:
    compact = " ".join(value.split())
    if len(compact) > maximum:
        compact = compact[: maximum - 1].rstrip() + "…"
    return html.escape(compact, quote=True)


def render_case_visual(data: dict) -> str:
    validate_summary(data)
    case_id = _safe(data["case_id"], 30)
    title = _safe(data["title"], 56)
    status = _safe(data["status"], 46)
    metric_width = 1040 / len(data["metrics"])

    metrics = []
    for index, metric in enumerate(data["metrics"]):
        x = 56 + index * metric_width
        metrics.append(
            f'<rect x="{x:.1f}" y="174" width="{metric_width - 14:.1f}" height="106" rx="12" '
            'fill="#102f3a" stroke="#315460"/>'
            f'<text x="{x + 22:.1f}" y="222" class="metric">{_safe(metric["value"], 15)}</text>'
            f'<text x="{x + 22:.1f}" y="252" class="metric-label">{_safe(metric["label"], 24)}</text>'
        )

    timeline = []
    timeline_count = len(data["timeline"])
    start_x, end_x = 92.0, 1108.0
    step = 0 if timeline_count == 1 else (end_x - start_x) / (timeline_count - 1)
    for index, item in enumerate(data["timeline"]):
        x = start_x + index * step
        color = "#f4b86b" if item["state"].lower() == "finding" else "#63d4bc"
        timeline.append(
            f'<circle cx="{x:.1f}" cy="376" r="10" fill="{color}" stroke="#071820" stroke-width="4"/>'
            f'<text x="{x:.1f}" y="344" class="time" text-anchor="middle">{_safe(item["time"], 13)}</text>'
            f'<text x="{x:.1f}" y="414" class="event" text-anchor="middle">{_safe(item["label"], 20)}</text>'
        )

    findings = []
    for index, finding in enumerate(data["findings"]):
        y = 482 + index * 54
        severity = _safe(finding["severity"].upper(), 10)
        findings.append(
            f'<text x="72" y="{y}" class="finding-id">{_safe(finding["id"], 18)}</text>'
            f'<text x="242" y="{y}" class="finding">{_safe(finding["label"], 60)}</text>'
            f'<text x="1118" y="{y}" class="severity" text-anchor="end">{severity}</text>'
        )

    height = 520 + max(0, len(data["findings"]) - 1) * 54
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="case-title case-desc">',
        f'<title id="case-title">{title}</title>',
        f'<desc id="case-desc">Evidence summary for {case_id}: {status}</desc>',
        '<style>.label{font:700 15px Inter,Segoe UI,Arial,sans-serif;letter-spacing:1.6px}.title{font:800 40px Inter,Segoe UI,Arial,sans-serif}.status{font:500 17px Inter,Segoe UI,Arial,sans-serif}.metric{font:800 34px Inter,Segoe UI,Arial,sans-serif;fill:#75e0ca}.metric-label{font:700 14px Inter,Segoe UI,Arial,sans-serif;fill:#b7ced3;letter-spacing:.6px}.section{font:700 14px Inter,Segoe UI,Arial,sans-serif;fill:#8db1b9;letter-spacing:1px}.time{font:700 13px Inter,Segoe UI,Arial,sans-serif;fill:#cce0e4}.event{font:600 13px Inter,Segoe UI,Arial,sans-serif;fill:#a9c1c7}.finding-id{font:800 14px ui-monospace,SFMono-Regular,Consolas,monospace;fill:#75e0ca}.finding{font:600 16px Inter,Segoe UI,Arial,sans-serif;fill:#eaf4f2}.severity{font:800 13px Inter,Segoe UI,Arial,sans-serif;fill:#f4c686;letter-spacing:1px}</style>',
        f'<rect width="1200" height="{height}" fill="#071820"/>',
        f'<text x="56" y="54" class="label" fill="#63d4bc">DON LOPEZ / {case_id}</text>',
        f'<text x="56" y="112" class="title" fill="#f3faf8">{title}</text>',
        f'<text x="56" y="148" class="status" fill="#a8c2c7">{status}</text>',
        *metrics,
        '<text x="56" y="326" class="section">EVIDENCE TIMELINE</text>',
        '<line x1="92" y1="376" x2="1108" y2="376" stroke="#355963" stroke-width="2"/>',
        *timeline,
        '<text x="56" y="452" class="section">FINDINGS</text>',
        *findings,
        '</svg>',
        '',
    ])


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: evidence_visuals.py INPUT_JSON OUTPUT_SVG", file=sys.stderr)
        return 2
    source, output = map(Path, argv[1:])
    data = json.loads(source.read_text(encoding="utf-8"))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_case_visual(data), encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
