"""Focused, dependency-free accessibility STRUCTURE audit for the portfolio.

This is NOT an automated WCAG conformance claim, contrast measurement, or
screen-reader/browser-level inspection. It guards important semantics and links.
"""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Structure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids: list[str] = []
        self.html_lang = ""
        self.h1 = 0
        self.mains = 0
        self.skips = 0
        self.metas: list[dict[str, str]] = []
        self.title_count = 0
        self.images: list[dict[str, str]] = []
        self.external_blank: list[dict[str, str]] = []
        self.anchors: list[str] = []
        self.details = 0
        self.summaries = 0
        self.navs: dict[str, list[str]] = {}
        self.current_nav: str | None = None
        self.focusable_tables = 0
        self.heading_counts: dict[str, int] = {"h2": 0, "h3": 0}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or "") for k, v in attrs}
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "html":
            self.html_lang = a.get("lang", "")
        if tag == "h1":
            self.h1 += 1
        if tag in self.heading_counts:
            self.heading_counts[tag] += 1
        if tag == "main":
            self.mains += 1
        if tag == "title":
            self.title_count += 1
        if tag == "meta":
            self.metas.append(a)
        if tag == "img":
            self.images.append(a)
        if tag == "details" and "mobile-nav" in a.get("class", "").split():
            self.details += 1
        if tag == "summary":
            self.summaries += 1
        if tag == "nav":
            self.current_nav = a.get("aria-label", "")
            self.navs.setdefault(self.current_nav, [])
        if tag == "a":
            href = a.get("href", "")
            self.anchors.append(href)
            if href == "#main" and "skip-link" in a.get("class", "").split():
                self.skips += 1
            if self.current_nav is not None:
                self.navs[self.current_nav].append(href)
            if a.get("target") == "_blank":
                self.external_blank.append(a)
        if tag == "div" and "evidence-scroll" in a.get("class", "").split():
            if a.get("role") == "region" and a.get("tabindex") == "0" and a.get("aria-label"):
                self.focusable_tables += 1

    def handle_endtag(self, tag: str) -> None:
        if tag == "nav":
            self.current_nav = None


def check_page(path: Path, targets: dict[Path, set[str]]) -> list[str]:
    page = Structure()
    page.feed(path.read_text(encoding="utf-8"))
    rel = path.relative_to(ROOT).as_posix()
    errors: list[str] = []

    def expect(condition: bool, message: str) -> None:
        if not condition:
            errors.append(f"{rel}: {message}")

    expect(page.html_lang == "en", "missing document language")
    expect(page.title_count == 1, "expected one page title")
    expect(page.h1 == 1 and page.mains == 1, "expected one H1 and one main landmark")
    expect(page.skips == 1 and "main" in page.ids, "missing functional skip-to-main link")
    expect(len(page.ids) == len(set(page.ids)), "duplicate HTML IDs")
    expect(any(a.get("name") == "viewport" for a in page.metas), "missing responsive viewport")
    expect(any(a.get("name") == "description" and a.get("content") for a in page.metas),
           "missing page description")
    expect(sum(a.get("rel") == "canonical" for a in page.metas) <= 1,
           "duplicate canonical meta tag")  # link tags checked separately by normal link audit
    expect(page.details == 1 and page.summaries >= 1,
           "expected one semantic details/summary mobile menu")
    desktop = page.navs.get("Main navigation", [])
    mobile = page.navs.get("Mobile navigation", [])
    expect(bool(desktop) and desktop == mobile,
           "desktop and mobile navigation destinations must match")
    for image in page.images:
        expect("alt" in image, f"image missing alt attribute: {image.get('src', '')}")
    for anchor in page.external_blank:
        expect({"noopener", "noreferrer"}.issubset(set(anchor.get("rel", "").split())),
               "target=_blank link missing noreferrer and noopener")
    if "evidence-scroll" in path.read_text(encoding="utf-8"):
        expect(page.focusable_tables >= 1, "evidence table not keyboard focusable")

    for href in page.anchors:
        split = urlsplit(href)
        if not split.fragment or split.scheme or split.netloc:
            continue
        dest = (path.parent / unquote(split.path)).resolve() if split.path else path.resolve()
        if dest not in targets:
            # Non-HTML links with fragments are not document landmarks.
            continue
        if unquote(split.fragment) not in targets[dest]:
            errors.append(f"{rel}: broken page landmark in {href}")
    return errors


def main() -> None:
    pages = sorted(ROOT.rglob("*.html"))
    targets = {}
    for page in pages:
        parser = Structure()
        parser.feed(page.read_text(encoding="utf-8"))
        targets[page.resolve()] = set(parser.ids)
    errors = []
    for path in pages:
        errors.extend(check_page(path, targets))
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    for rule in (".mobile-nav", ".evidence-scroll:focus-visible",
                 "prefers-reduced-motion", "@media(max-width:800px)"):
        if rule not in css:
            errors.append(f"styles.css: missing accessibility rule {rule}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {len(pages)} HTML pages audited for core semantics, "
          "mobile menu link parity, accessible image labels, and local landmarks")
    print("LIMIT: static structure review, NOT a browser/screen-reader/WCAG audit")


if __name__ == "__main__":
    main()
