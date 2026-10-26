"""Read-only smoke test of the published portfolio on GitHub Pages.

Fetches only known public URL paths from the fixed GitHub Pages origin.
No account access, login, arbitrary target input, scanning or page mutation.
"""
from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://ixi-2773.github.io/Cybersecurity_Portfolio/"
EXPECTED_PAGES = {
    "education.html": "Academic Experience",
    "visual-credits.html": "Image Credits",
    "projects/e3-digital-forensics.html": "Forensic Evidence",
    "projects/offensive-security-vm-labs.html": "Offensive Security",
    "projects/kali-defender-visibility.html": "Kali",
    "projects/splunk-threat-hunting.html": "Splunk Threat",
    "awards.html": "Awards",
    "projects/detection-engineering.html": "Detection Engineering",
    "projects/splunk-siem-investigation.html": "Splunk Investigation & Evidence Correlation",
    "projects/splunk-execution-workflow.html": "Splunk Execution Workflow",
    "projects/network-intrusion-lab.html": "Network Intrusion",
    "projects/phishing-investigation.html": "Phishing",
    "projects/identity-mfa-investigation.html": "Enterprise Account",
    "projects/soc-triage-automation.html": "Python SOC",
    "": "Don Lopez",
    "apply.html": "Application Toolkit",
    "resume-soc.html": "SOC Analyst Résumé",
    "resume-security.html": "Security Analyst Résumé",
    "explore.html": "Explore the work",
    "recruiter.html": "SOC Analyst Recruiter Profile",
    "roles.html": "Role Paths",
    "test-lab.html": "Verification Workbench",
    "verify.html": "Evidence Review",
    "projects/splunk-synthetic-preview.html": "Synthetic SOC Dashboard Preview",
    "projects/authentication-detection.html": "Authentication",
    "projects/windows-process-triage.html": "Windows",
    "projects/network-traffic-analysis.html": "Network",
    "projects/vulnerability-remediation.html": "Web Attack-Log",
    "projects/celestial-resonance.html": "Celestial Resonance",
    "projects/research-ai-infrastructure.html": "RAI",
    "projects/certification-learning-engine.html": "Certification Learning Engines",
    "projects/soc-analyst-workflow.html": "SOC",
    "projects/soc-analyst-evidence.html": "SOC Analyst",
}
STATIC_ASSETS = (
    "assets/animation/signal-to-case.gif", "assets/animation/signal-to-case-still.png",
    "assets/js/signal-animation.js",
    "assets/reference/kali-desktop-2020.4.png", "assets/reference/forensic-write-blocker.webp", "assets/reference/csusb-pfau-library.webp",
    "assets/reference/csusb-jack-brown-hall.webp", "assets/reference/csusb-university-entrance.webp",
    "assets/evidence/splunk-native-dashboard-results.png",
    "assets/evidence/phishing-investigation.svg",
    "assets/evidence/enterprise-account-investigation.svg",
    "assets/evidence/web-attack-log-investigation.svg",
    "assets/evidence/forensic-evidence-examination.svg",
    "assets/js/signal-display.js",
    "assets/js/portfolio-systems.js",
    "styles.css",
    "portfolio.css",
    "resumes/Don_Lopez_Cybersecurity_Resume.pdf",
    "assets/evidence/sc900-practice-linux.png",
    "assets/network/pcap-evidence-overview.svg",
    "assets/js/explorer.js",
    "assets/js/lab-data.js",
    "assets/js/test-engine.js",
    "assets/js/lab-ui.js",
    "assets/js/home-replay.js",
)
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
        if path in ("", "explore.html"):
            required = ("explore.html", "resumes/Don_Lopez_Cybersecurity_Resume.pdf")
            if path == "explore.html":
                required += (
                    "projects/authentication-detection.html",
                    "projects/windows-process-triage.html",
                    "projects/network-traffic-analysis.html",
                    "projects/vulnerability-remediation.html",
                    "projects/phishing-investigation.html",
                    "projects/identity-mfa-investigation.html",
                    "projects/e3-digital-forensics.html",
                    "projects/offensive-security-vm-labs.html",
                    "projects/celestial-resonance.html",
                    "projects/research-ai-infrastructure.html",
                    "projects/certification-learning-engine.html",
                )
            for value in required:
                if value not in parser.links:
                    raise ValueError(f"{path or '/'} missing employer navigation link: {value}")
        return {"path": path or "/", "status": "PASS", "title": title}
    if path.endswith(".css"):
        if "text/css" not in content_type.lower():
            raise ValueError("Stylesheet served with wrong MIME type")
        tokens = (b"--ink", b"--accent") if path == "portfolio.css" else (b"--bg", b"--teal")
        if any(token not in body for token in tokens):
            raise ValueError("Stylesheet contents did not match portfolio styles")
    elif path.endswith(".pdf"):
        if "application/pdf" not in content_type.lower() or not body.startswith(b"%PDF-"):
            raise ValueError("Public resume was not served as a PDF")
    elif path.endswith(".webp"):
        if "image/webp" not in content_type.lower() or body[:4] != b"RIFF" or body[8:12] != b"WEBP":
            raise ValueError("Conceptual artwork was not served as a WebP image")
    elif path.endswith(".png"):
        if "image/png" not in content_type.lower() or not body.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError("Application screenshot was not served as a PNG")
    elif path.endswith(".gif"):
        if "image/gif" not in content_type.lower() or body[:6] not in (b"GIF87a", b"GIF89a"):
            raise ValueError("Animation was not served as a GIF")
    elif path.endswith(".svg"):
        if "svg" not in content_type.lower():
            raise ValueError("SVG asset served with unexpected MIME type")
        if b"<svg" not in body or not (b"OFFLINE VISUALIZATION" in body or (b"<title" in body and b"<desc" in body)):
            raise ValueError("SVG evidence content missing")
    elif path.endswith(".js"):
        if "javascript" not in content_type.lower():
            raise ValueError("Browser test code served with incorrect MIME type")
        if not body.strip():
            raise ValueError("Browser test code response was empty")
    return {"path": path, "status": "PASS", "content_type": content_type}


def fetch_once(path: str) -> dict:
    url = BASE + path
    parts = urllib.parse.urlsplit(url)
    if parts.scheme != "https" or parts.hostname != "ixi-2773.github.io":
        raise ValueError("Unexpected target host")
    opener = urllib.request.build_opener(BlockRedirect)
    request = urllib.request.Request(url, headers={
        "User-Agent": "DonLopezPortfolioHealthcheck/1.0",
        "Accept": "text/html,text/css,image/svg+xml,image/png,application/pdf",
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
    assert verify_response("assets/js/test-engine.js", 200, "text/javascript",
                           b"globalThis.PortfolioEngine = {}")["status"] == "PASS"
    try:
        verify_response("assets/js/test-engine.js", 200, "text/plain", b"test")
    except ValueError:
        pass
    else:
        raise AssertionError("Unsafe JavaScript content type passed")
    # Exercise the real release documents too, so stale routes/titles cannot
    # pass the offline check and fail only after deployment.
    root = Path(__file__).resolve().parents[1]
    for path in EXPECTED_PAGES:
        verify_response(path, 200, "text/html", (root / (path or "index.html")).read_bytes())
    verify_response("portfolio.css", 200, "text/css", (root / "portfolio.css").read_bytes())
    resume = "resumes/Don_Lopez_Cybersecurity_Resume.pdf"
    verify_response(resume, 200, "application/pdf", (root / resume).read_bytes())
    screenshot = "assets/evidence/sc900-practice-linux.png"
    verify_response(screenshot, 200, "image/png", (root / screenshot).read_bytes())
    animation = "assets/animation/signal-to-case.gif"
    verify_response(animation, 200, "image/gif", (root / animation).read_bytes())
    broken_catalog = (root / "explore.html").read_bytes().replace(
        b"projects/certification-learning-engine.html", b"missing-case.html")
    for path, mime, body in [
        ("explore.html", "text/html", broken_catalog),
        (resume, "text/html", b"<!doctype html>not a resume"),
        (screenshot, "text/html", b"<!doctype html>missing image"),
        (animation, "text/html", b"<!doctype html>missing animation"),
        (animation, "image/gif", b"not a GIF"),
    ]:
        try:
            verify_response(path, 200, mime, body)
        except ValueError:
            continue
        raise AssertionError(f"Invalid release response passed: {path}")
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
