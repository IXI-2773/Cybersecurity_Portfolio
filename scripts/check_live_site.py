"""Read-only smoke test of the published portfolio on GitHub Pages.

Fetches only known public URL paths from the fixed GitHub Pages origin.
No account access, login, arbitrary target input, scanning or page mutation.
"""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://ixi-2773.github.io/Cybersecurity_Portfolio/"
EXPECTED_PAGES = {
    "": "Don Lopez",
    "projects/authentication-detection.html": "Authentication",
    "projects/windows-process-triage.html": "Windows",
    "projects/network-traffic-analysis.html": "Network",
    "projects/vulnerability-remediation.html": "Vulnerability",
    "projects/celestial-resonance.html": "Celestial Resonance",
    "projects/research-ai-infrastructure.html": "RAI",
    "projects/soc-analyst-workflow.html": "SOC",
}
STATIC_ASSETS = ("styles.css", "assets/network/pcap-evidence-overview.svg")
MAX_BYTES = 1024 * 1024


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = []
        self.in_title = False
        self.h1_count = 0
        self.links = set()
        self.styles = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.h1_count += 1
        if tag == "a":
            self.links.add(a.get("href", ""))
        if tag == "link" and a.get("rel") == "stylesheet":
            self.styles.append(a.get("href"))

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)


class BlockRedirect(urllib.request.HTTPRedirectHandler):
    """Fail instead of silently following an unexpected redirect."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise ValueError("Unanticipated HTTP redirect during Pages check")


def verify_response(path: str, status: int, content_type: str, body: bytes) -> dict:
    if status != 200:
        raise ValueError(f"{path or '/'} returned HTTP {status}")
    if len(body) > MAX_BYTES:
        raise ValueError(f"{path or '/'} exceeds response byte limit")
    if path in EXPECTED_PAGES:
        if "text/html" not in content_type.lower():
            raise ValueError(f"{path or '/'} is not served as HTML ({content_type})")
        text = body.decode("utf-8-sig")
        if not text.lstrip().lower().startswith("<!doctype html>"):
            raise ValueError(f"{path or '/'} missing HTML document declaration")
        parser = PageParser()
        parser.feed(text)
        title = "".join(parser.title).strip()
        if EXPECTED_PAGES[path].lower() not in title.lower():
            raise ValueError(f"{path or '/'} missing expected page title")
        if parser.h1_count != 1:
            raise ValueError(f"{path or '/'} requires exactly one H1")
        if len(parser.styles) != 1:
            raise ValueError(f"{path or '/'} missing or duplicated CSS stylesheet")
        if path == "":
            for value in ("projects/celestial-resonance.html",
                          "projects/vulnerability-remediation.html"):
                if value not in parser.links:
                    raise ValueError(f"Homepage missing internal project link: {value}")
        return {"path": path or "/", "status": "PASS", "title": title}
    if path.endswith(".css"):
        if "text/css" not in content_type.lower():
            raise ValueError("Stylesheet served with wrong MIME type")
        if b"--bg" not in body or b"--teal" not in body:
            raise ValueError("Stylesheet contents did not match portfolio styles")
    elif path.endswith(".svg"):
        if "svg" not in content_type.lower():
            raise ValueError("SVG asset served with unexpected MIME type")
        if b"<svg" not in body or b"OFFLINE VISUALIZATION" not in body:
            raise ValueError("SVG evidence content missing")
    return {"path": path, "status": "PASS", "content_type": content_type}


def fetch_once(path: str) -> dict:
    url = BASE + path
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != "https" or parts.hostname != "ixi-2773.github.io":
        raise ValueError("Unexpected target host")
    opener = urllib.request.build_opener(BlockRedirect)
    request = urllib.request.Request(url, headers={
        "User-Agent": "DonLopezPortfolioHealthcheck/1.0",
        "Accept": "text/html,text/css,image/svg+xml",
    })
    try:
        with opener.open(request, timeout=15) as r:
            status = r.status
            mime = r.headers.get("Content-Type", "")
            body = r.read(MAX_BYTES + 1)
    except urllib.error.HTTPError as exc:
        raise ValueError(f"{path or '/'} returned HTTP {exc.code}") from None
    except urllib.error.URLError as exc:
        raise ValueError(f"Network/TLS access failed for {path or '/'}") from None
    return verify_response(path, status, mime, body)


def run(*, retries: int = 4, delay: float = 8) -> dict:
    if retries < 1 or retries > 6:
        raise ValueError("retries must be between 1 and 6")
    checked, failures = [], []
    for path in list(EXPECTED_PAGES) + list(STATIC_ASSETS):
        error = ""
        for n in range(retries):
            try:
                checked.append(fetch_once(path))
                error = ""
                break
            except (ValueError, UnicodeError) as exc:
                error = str(exc)
                if n + 1 < retries:
                    time.sleep(delay)
        if error:
            failures.append({"path": path or "/", "error": error})
    return {
        "schema": "portfolio.pages-healthcheck.v1",
        "base_url": BASE,
        "pages_checked": len(checked) + len(failures),
        "passing": len(checked),
        "failures": failures,
        "status": "PASS" if not failures else "FAIL",
        "note": "A successful smoke test confirms public HTML/asset responses, not screenshot appearance or security controls.",
    }


def self_test() -> None:
    sample = (b'<!doctype html><html lang="en"><head><title>Celestial Resonance | '
              b'Don Lopez</title><link rel="stylesheet" href="../styles.css"></head>'
              b'<body><h1>CR</h1></body></html>')
    assert verify_response("projects/celestial-resonance.html", 200, "text/html", sample)["status"] == "PASS"
    for ct, body in [("text/plain", sample), ("text/html", b"Not html")]:
        try:
            verify_response("projects/celestial-resonance.html", 200, ct, body)
        except ValueError:
            continue
        raise AssertionError("Invalid response passed healthcheck")
    assert verify_response("styles.css", 200, "text/css", b":root{--bg:black;--teal:green}")["status"] == "PASS"
    print("Local healthcheck self-tests: PASS; no external HTTP requests made")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true", help="Use sample HTML, no network")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    result = run()
    print(json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
