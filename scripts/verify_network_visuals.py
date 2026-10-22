"""Validate static vector evidence without treating it as independent packet analysis.

Does not replace the deterministic PCAP unit tests or Wireshark manual inspection.
"""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "assets/network/pcap-evidence-overview.svg",
    ROOT / "assets/network/dns-nxdomain-investigation.svg",
    ROOT / "assets/network/http-request-comparison.svg",
]
NS = "{http://www.w3.org/2000/svg}"


def main():
    for path in FILES:
        body = path.read_text(encoding="utf-8")
        root = ET.fromstring(body)
        assert root.tag == NS + "svg", f"{path}: unexpected root element"
        assert root.get("viewBox") == "0 0 1200 700", f"{path}: unexpected geometry"
        assert root.get("role") == "img" and root.get("aria-label"), f"{path}: accessibility label missing"
        assert "OFFLINE VISUALIZATION" in body, f"{path}: missing synthetic evidence disclosure"
        assert "<script" not in body.lower() and "javascript:" not in body.lower(), f"{path}: SVG must be static"
        print("Validated synthetic vector illustration:", path.relative_to(ROOT))
    page = (ROOT / "projects/network-traffic-analysis.html").read_text(encoding="utf-8")
    for path in FILES:
        assert path.name in page, f"Site is not referencing {path.name}"


if __name__ == "__main__":
    main()
