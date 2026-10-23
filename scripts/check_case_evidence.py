"""Focused, offline verification of evidence claims in published case studies.

Keeps public synthetic-case summaries aligned with frozen JSON expectations and
underlying source constants. Does not repeat Python security-lab tests.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def get(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def required(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    net = json.loads(get("projects/03-network-pcap/expected_findings.json"))
    reqs = net["findings"]
    required(net["packet_count"] == 20 and net["decoded_event_count"] == 12,
             "Network fixture counts changed; review public case")
    required(len(reqs) == 2 and {x["rule_id"] for x in reqs} ==
             {"NET_DNS_NXDOMAIN_BURST", "NET_HTTP_POST_RESERVED_HOST"},
             "Network expected finding IDs changed")
    net_doc = get("projects/03-network-pcap/CASE_REPORT.md")
    net_html = get("projects/network-traffic-analysis.html")
    for finding in reqs:
        for key in ("rule_id", "observed_at_utc"):
            required(finding[key] in net_doc,
                     f"Network report missing expected {key}: {finding[key]}")
    for value in ("LAB-NET-001", "Four", "POST"):
        required(value.lower() in net_html.lower(),
                 f"Network rendered case missing {value}")
    required("projects/03-network-pcap/CASE_REPORT.md" in net_html,
             "Network page no longer links to GitHub-rendered report")

    web = json.loads(get("projects/04-local-vulnerability-assessment/expected_assessment.json"))
    required(len(web["expected_before_findings"]) == 4 and not web["expected_after_findings"],
             "Web hardening expected finding counts changed")
    web_doc = get("projects/04-local-vulnerability-assessment/CASE_REPORT.md")
    web_html = get("projects/vulnerability-remediation.html")
    for rule in web["expected_before_findings"]:
        required(rule in web_doc, f"Web case report missing rule identifier: {rule}")
    required("LAB-WEB-001" in web_html and
             "projects/04-local-vulnerability-assessment/CASE_REPORT.md" in web_html,
             "Web page missing case ID or full rendered evidence link")
    for source in (net_doc, web_doc):
        required("not" in source.lower() and "synthetic" in source.lower(),
                 "Evidence boundary disclosure missing")

    print("PASS: 2 source-linked case reports, frozen rule IDs/times, and webpage links")
    print("Scope: static evidence consistency; not a live security assessment")


if __name__ == "__main__":
    main()
