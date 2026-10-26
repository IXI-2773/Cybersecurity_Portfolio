"""Publish one source-backed incident brief as native HTML and a one-page PDF.

The JSON is the shared editorial source. No telemetry or findings are regenerated.
PDF authoring requires reportlab; --check-html uses only the standard library.
"""
from pathlib import Path
from html import escape
import argparse
import json

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'projects/08-ad-investigation/incident_brief.json'
HTML = ROOT / 'projects/ad-incident-report.html'
PDF = ROOT / 'projects/08-ad-investigation/AD_Incident_Report.pdf'


def content():
    data = json.loads(DATA.read_text())
    analysis = json.loads((DATA.parent / 'analysis.json').read_text())
    known = {r['id'] for r in analysis['records']} | {p['id'] for p in analysis['packets']}
    for row in data['timeline']:
        if not set(row['refs']) <= known:
            raise ValueError('Brief references unknown evidence')
    return data


def render_html(data):
    e = escape
    # Reuse the site's existing header and footer, including keyboard mobile menu.
    base = (ROOT / 'projects/linux-sql-access-audit.html').read_text()
    header = base[base.index('<header class="site-header">'):base.index('<main id="main">')]
    footer = base[base.index('<footer class="site-footer'):base.index('</body>')]
    timeline = ''.join(f'<li><strong>{e(r["time"])}</strong><p>{e(r["text"])}</p><small>Source records: {e(", ".join(r["refs"]))}</small></li>' for r in data['timeline'])
    decisions = ''.join(f'<p><strong>{e(r["title"])}.</strong> {e(r["text"])}</p>' for r in data['decisions'])
    actions = ''.join(f'<li><strong>{e(r["title"])}</strong><p>{e(r["text"])}</p></li>' for r in data['recommendations'])
    links = ''.join(f'<a href="{e(s["url"], quote=True)}">{e(s["label"])} ↗</a>' for s in data['sources'])
    title = e(data['title'])
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} | Don Lopez</title><meta name="description" content="A concise incident report sample: evidence, analyst decisions, conditional response recommendations and limits from a recorded AD emulation."><meta property="og:title" content="{title} | Don Lopez"><meta property="og:description" content="Source-backed incident review with analyst decisions and response recommendations."><meta property="og:type" content="website"><link rel="canonical" href="https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/ad-incident-report.html"><link rel="stylesheet" href="../portfolio.css"></head><body>
<a class="skip-link" href="#main">Skip to content</a>{header}
<main id="main"><article class="reading incident-report" data-case-scope="recorded-emulation-analysis">
<header class="case-intro"><a class="back-link" href="ad-attack-chain.html#analyst-brief">Back to the AD investigation</a><p class="project-meta">INCIDENT REPORT SAMPLE / {e(data['id'])}</p><h1>{title}</h1><p class="case-lead">{e(data['subtitle'])}</p><p class="project-meta">Prepared {e(data['prepared'])} · Capture {e(data['capture_date'])} · {e(data['author'])}</p><p class="case-result">{e(data['status'])}</p><div class="artifact-links"><a href="08-ad-investigation/AD_Incident_Report.pdf" download>Download one-page report <span class="file-type">PDF</span></a><a href="ad-attack-chain.html#ad-title">Inspect the underlying evidence</a></div></header>
<section class="case-section"><h2>Assessment and scope</h2><p>{e(data['summary'])}</p><p>{e(data['scope'])}</p></section>
<section class="case-section"><h2>Key evidence</h2><ol class="incident-list">{timeline}</ol></section>
<section class="case-section"><h2>Analyst decisions</h2>{decisions}</section>
<section class="case-section"><h2>Recommended handoff</h2><p>Proposed follow-up for a comparable live case; these actions were not performed.</p><ol class="incident-list">{actions}</ol></section>
<section class="scope-note"><h2>Evidence limits</h2><p>{e(data['limits'])}</p><div class="artifact-links">{links}</div></section>
<p class="case-back"><a href="../explore.html">Explore all work ↗</a></p></article></main>{footer}</body></html>
'''


def render_pdf(data):
    from reportlab.lib import colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    # Bundle ReportLab's own font to keep PDF metrics and rendering portable.
    import reportlab
    font_dir = Path(reportlab.__file__).parent / 'fonts'
    pdfmetrics.registerFont(TTFont('BriefSans', str(font_dir / 'Vera.ttf')))
    pdfmetrics.registerFont(TTFont('BriefSans-Bold', str(font_dir / 'VeraBd.ttf')))
    pdfmetrics.registerFontFamily('BriefSans', normal='BriefSans', bold='BriefSans-Bold')
    e = escape
    ink, accent = colors.HexColor('#213533'), colors.HexColor('#286b60')
    body = ParagraphStyle('body', fontName='BriefSans', fontSize=8.8, leading=11.6, textColor=ink, spaceAfter=5, alignment=TA_LEFT)
    small = ParagraphStyle('small', parent=body, fontSize=7.5, leading=9.5, textColor=colors.HexColor('#506361'))
    heading = ParagraphStyle('heading', parent=body, fontName='BriefSans-Bold', fontSize=10.5, leading=13, textColor=accent, spaceBefore=8, spaceAfter=4)
    title = ParagraphStyle('title', parent=body, fontName='BriefSans-Bold', fontSize=18.5, leading=23, spaceAfter=7)
    story = []
    def p(text, style=body): story.append(Paragraph(text, style))
    def section(name): p(e(name), heading)
    p('DON LOPEZ / INCIDENT REPORT SAMPLE / ' + e(data['id']), small)
    p(e(data['title']), title)
    p(e(data['subtitle']) + ' | Prepared ' + data['prepared'] + ' | Capture ' + data['capture_date'], small)
    p('<b>' + e(data['status']) + '</b>')
    story.append(HRFlowable(width='100%', thickness=1, color=accent, spaceAfter=4))
    section('Assessment and scope')
    p(e(data['summary']))
    p(e(data['scope']))
    section('Key evidence / UTC')
    for r in data['timeline']:
        p('<b>' + e(r['time']) + '.</b> ' + e(r['text']))
        p(e(', '.join(r['refs'])), small)
    section('Analyst decisions')
    for r in data['decisions']: p('<b>' + e(r['title']) + '.</b> ' + e(r['text']))
    section('Recommended handoff / proposed, not performed')
    for i,r in enumerate(data['recommendations'], 1): p('<b>' + str(i) + '. ' + e(r['title']) + '.</b> ' + e(r['text']))
    section('Evidence limits')
    p(e(data['limits']), small)
    story.append(Spacer(1, 5))
    p('Source links: ' + ' | '.join('<link href="'+e(s['url'],quote=True)+'" color="#286b60"><u>'+e(s['label'])+'</u></link>' for s in data['sources']), small)
    def footer(canvas, doc):
        canvas.setFont('BriefSans', 7)
        canvas.setFillColor(accent)
        url = 'https://ixi-2773.github.io/Cybersecurity_Portfolio/projects/ad-incident-report.html'
        canvas.drawString(42, 24, 'Portfolio / full report and evidence')
        canvas.linkURL(url, (42, 21, 220, 33), relative=0)
        canvas.drawRightString(570, 24, data['id'] + ' / ' + str(doc.page))
    doc = SimpleDocTemplate(str(PDF), pagesize=letter, rightMargin=42, leftMargin=42,
                           topMargin=30, bottomMargin=40, title=data['title'], author=data['author'], invariant=1)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check-html', action='store_true')
    args = parser.parse_args()
    data = content()
    rendered = render_html(data)
    if args.check_html:
        if HTML.read_text() != rendered:
            raise SystemExit('Incident HTML differs from canonical report source; regenerate')
        if not PDF.read_bytes().startswith(b'%PDF-'):
            raise SystemExit('Incident PDF missing or invalid')
        print('PASS: shared report source, evidence references, rendered HTML and PDF signature')
    else:
        HTML.write_text(rendered)
        render_pdf(data)
        print('Wrote native incident report and PDF from shared editorial source')


if __name__ == '__main__':
    main()
