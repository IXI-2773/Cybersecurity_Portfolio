"""Produce an inspectable, offline HTML portfolio ZIP from public repo sources.

No network use, third-party packages, template execution, or generated credentials.
Open index.html after extracting the ZIP. GitHub Pages is not required.
"""
from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_DATE = (2026, 10, 22, 0, 0, 0)
ALLOWED = {
    "assets": {".svg", ".png", ".jpg", ".jpeg", ".webp", ".js"},
    "docs": {".md"},
    "resumes": {".txt"},
    "projects": {".html", ".md", ".py", ".json", ".csv", ".spl"},
}
ROOT_FILES = {
    "index.html", "apply.html", "recruiter.html", "explore.html", "test-lab.html", "verify.html", "styles.css", "README.md", "SECURITY.md",
    "PUBLICATION_CHECKLIST.md",
}
REQUIRED_SITE_FILES = {
    "index.html", "apply.html", "recruiter.html", "explore.html", "test-lab.html", "verify.html", "styles.css",
    "resumes/Don_Lopez_SOC_Analyst.txt",
    "resumes/Don_Lopez_Security_Analyst.txt",
    "assets/evidence/splunk-native-dashboard-results.png",
    "assets/js/explorer.js", "assets/js/lab-data.js", "assets/js/test-engine.js", "assets/js/lab-ui.js",
    "projects/celestial-resonance.html",
    "projects/research-ai-infrastructure.html",
    "projects/authentication-detection.html",
    "projects/windows-process-triage.html",
    "projects/network-traffic-analysis.html",
    "projects/vulnerability-remediation.html",
    "projects/CASE_STUDIES.md",
}


def public_files() -> list[Path]:
    found = [ROOT / name for name in sorted(ROOT_FILES) if (ROOT / name).is_file()]
    for directory, extensions in ALLOWED.items():
        folder = ROOT / directory
        if not folder.is_dir():
            continue
        for path in sorted(folder.rglob("*")):
            if (path.is_file() and not path.is_symlink()
                    and path.suffix.lower() in extensions
                    and "__pycache__" not in path.parts):
                found.append(path)
    return found


def make_bundle(destination: Path) -> dict:
    all_files = public_files()
    names = {str(file.relative_to(ROOT)).replace("\\", "/") for file in all_files}
    missing = sorted(REQUIRED_SITE_FILES - names)
    if missing:
        raise ValueError("Missing required public pages: " + ", ".join(missing))
    if destination.resolve() in (file.resolve() for file in all_files):
        raise ValueError("Destination must not overwrite a portfolio source file")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9, allowZip64=False) as archive:
        for file in all_files:
            relative = file.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(relative, date_time=ARCHIVE_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, file.read_bytes(), compress_type=zipfile.ZIP_DEFLATED,
                             compresslevel=9)
        instructions = (
            "DON LOPEZ — OFFLINE CYBERSECURITY PORTFOLIO\n\n"
            "1. Extract this ZIP to a directory; do not open files directly inside the archive.\n"
            "2. Double-click index.html to open the designed portfolio in a web browser.\n"
            "3. The HTML pages and CSS/images work locally; links to GitHub or MITRE require internet.\n"
            "4. Markdown case reports are also readable directly in GitHub and many Markdown viewers.\n"
            "5. Offline preview does not activate GitHub Pages or prove a live site is hosted.\n"
        )
        info = zipfile.ZipInfo("START_HERE.txt", date_time=ARCHIVE_DATE)
        info.compress_type = zipfile.ZIP_DEFLATED
        archive.writestr(info, instructions.encode("utf-8"))
    with zipfile.ZipFile(destination, "r") as check:
        if check.testzip() is not None:
            raise ValueError("ZIP checksum check failed")
        if len(check.namelist()) != len(set(check.namelist())):
            raise ValueError("Archive contains duplicate paths")
        for path in check.namelist():
            if path.startswith("/") or ".." in Path(path).parts:
                raise ValueError("Unsafe archive path: " + path)
        for file in ("apply.html", "recruiter.html", "resumes/Don_Lopez_SOC_Analyst.txt",
                     "resumes/Don_Lopez_Security_Analyst.txt"):
            if file not in check.namelist():
                raise ValueError("Missing offline application file: " + file)
        if not check.read("index.html").startswith(b"<!doctype html>"):
            raise ValueError("Expected root HTML entry point missing")
    return {"status": "OFFLINE_PREVIEW_CREATED", "files": len(all_files),
            "size_bytes": destination.stat().st_size,
            "pages_hosted": False, "destination": str(destination)}


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", type=Path, default=Path("cybersecurity-portfolio-site.zip"))
    args = p.parse_args()
    print(json.dumps(make_bundle(args.output), indent=2))


if __name__ == "__main__":
    main()
