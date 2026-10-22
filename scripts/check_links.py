"""Check that relative URLs in static portfolio HTML resolve locally."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {"href", "src"} and value:
                self.paths.append(value)


def main():
    broken = []
    checked = 0
    for page in ROOT.rglob("*.html"):
        parser = LinkParser()
        parser.feed(page.read_text(encoding="utf-8"))
        for url in parser.paths:
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc or url.startswith(("#", "mailto:", "tel:", "//")):
                continue
            target = (page.parent / unquote(parsed.path)).resolve()
            try:
                target.relative_to(ROOT)
            except ValueError:
                broken.append(f"{page.relative_to(ROOT)}: path escapes site: {url}")
                continue
            if not target.exists():
                broken.append(f"{page.relative_to(ROOT)}: missing {url}")
            checked += 1
    if broken:
        raise SystemExit("\n".join(broken))
    print(f"{checked} relative HTML links resolved")


if __name__ == "__main__":
    main()
