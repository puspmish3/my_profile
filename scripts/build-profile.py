"""Rebuild the website and its three-page, illustrated downloadable profile.

Install scripts/requirements-pdf.txt first. No PDF dependencies are needed to serve
the committed website. Project content is shared with the website builder.
"""
from pathlib import Path
import runpy
import shutil
import sys
from html import escape

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.tools' / 'pdf'))
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageOps

ASSETS = ROOT / 'site' / 'assets'
OUTPUT = ROOT / 'output' / 'pdf' / 'puspamitra-mishra-profile.pdf'
W, H = 612, 792
INK, TEAL, MUTED, PALE = '#182f34', '#176761', '#52646b', '#eef4f2'
WEB = 'https://myprofile.puspamitramishra.fyi/'
AWS_BADGE = 'https://www.credly.com/badges/07dc9b54-49b2-461e-a9d6-54759287af67/public_url'
CLAUDE_BADGE = 'https://www.credly.com/badges/764b629f-2a50-4570-b988-5cd7cc30ea04'


def text(value, x, top, width, size=10, color=INK, bold=False, max_height=None):
    value = value.replace('\u2011', '-').replace('\u2013', '-').replace('\u2014', '-')
    style = ParagraphStyle('copy', fontName='Helvetica-Bold' if bold else 'Helvetica',
                           fontSize=size, leading=size * 1.34, textColor=HexColor(color))
    p = Paragraph(value, style)
    _, height = p.wrap(width, H)
    if max_height is not None and height > max_height:
        raise ValueError(f'Text overflow ({height} > {max_height}): {value}')
    if top + height > 750:
        raise ValueError(f'Page overflow: {value}')
    p.drawOn(c, x, H - top - height)
    return height


def box(x, top, width, height, color=PALE):
    c.setFillColor(HexColor(color))
    c.rect(x, H - top - height, width, height, stroke=0, fill=1)


def photo(name, x, top, width, height, crop=True):
    with Image.open(ASSETS / name) as im:
        if crop:
            im = ImageOps.fit(im.convert('RGB'), (int(width * 3), int(height * 3)),
                              method=Image.Resampling.LANCZOS, centering=(0.5, 0.3))
        c.drawImage(ImageReader(im), x, H - top - height, width, height,
                    preserveAspectRatio=not crop, anchor='c', mask='auto')


def footer(number):
    box(36, 757, 540, 1, '#d8e3e0')
    text('PUSPAMITRA MISHRA  /  EXECUTIVE PROFILE', 36, 735, 400, 7, MUTED)
    c.setFont('Helvetica', 8)
    c.setFillColor(HexColor(MUTED))
    c.drawRightString(576, 23, f'{number} / 3')
    # Footer name only. A wider rect overlaps the contact line and steals the LinkedIn link.
    c.linkURL(WEB, (36, 18, 230, 32), relative=0)
    c.showPage()


def metric(value, label, x, top, width):
    text(value, x, top, width, 20, TEAL, True)
    text(label, x, top + 28, width - 4, 7.6, MUTED, max_height=34)


def overview():
    box(0, 0, W, 8, TEAL)
    text('ENTERPRISE SOLUTIONS ARCHITECT', 36, 29, 420, 9, TEAL, True)
    text('Puspamitra Mishra', 36, 49, 420, 29, INK, True)
    text('Engineering leadership. Applied AI. Enterprise impact.', 36, 94, 408, 11, MUTED)
    text('Dallas, USA · +1 (469) 955-4740<br/>'
         '<link href="mailto:puspamitra.mishra@gmail.com">puspamitra.mishra@gmail.com</link><br/>'
         '<link href="https://www.linkedin.com/in/puspamitra-mishra-6b186b29/">LinkedIn</link>'
         f' · <link href="{WEB}">Project portfolio</link>', 36, 118, 410, 9, MUTED)
    photo('portrait.png', 471, 29, 105, 130)
    text('PROFILE SUMMARY', 36, 183, 540, 9, TEAL, True)
    text('Enterprise solutions architect and senior engineering leader with 24+ years across banking, '
         'insurance, healthcare, and life sciences. Connects architecture with executive delivery: '
         'scaling global teams, modernizing cloud and API platforms, and turning AI adoption into '
         'measurable business outcomes.', 36, 201, 540, 10, max_height=43)
    box(36, 252, 540, 86)
    for i, (v, label) in enumerate([('24+', 'Years in leading, managing and transforming enterprise IT'),
                                   ('350+', 'Engineers led during various transformation initiatives'),
                                   ('$48M', 'Saved through AI-led transformations across industries'),
                                   ('$6M', 'Cloud spend saved through modernization')]):
        metric(v, label, 48 + i * 132, 260, 124)
    text('WORK EXPERIENCE', 36, 352, 540, 9, TEAL, True)
    roles = [
        ('Aug 2024 - Present', 'Senior Engineering Leader', 'CVS Health / Aetna / McKesson, via TCS',
         'API platform modernization across Azure and GCP; APIC-to-Kong migration, millions of daily transactions, and observability supporting 99.99% availability.'),
        ('Mar 2021 - Jul 2024', 'Senior Engineering Leader', 'MetLife, via TCS',
         'Led 350+ engineers. GCP-to-Azure optimization saved ~$500K/month; integration modernization eliminated ~$1M/year in ACE licensing and cut maintenance 30%.'),
        ('Feb 2017 - Feb 2021', 'Senior Engineering Manager', 'Citigroup, via TCS',
         'Migrated core Java banking systems to Spring Boot microservices on PCF, AWS, and OpenShift; governed releases and critical payment applications.'),
        ('Dec 2005 - Oct 2017', 'Solutions Architect / Senior Developer', 'Citibank, via TCS',
         'Led 35-50 developers on banking and mortgage integration; designed underwriting rules and modernized fees and pricing platforms.')]
    for i, (dates, role, org, summary) in enumerate(roles):
        top = 372 + i * 63
        text(dates, 36, top, 117, 8, MUTED)
        text(role, 163, top, 413, 10, INK, True)
        text(org, 163, top + 14, 413, 8, TEAL)
        text(summary, 163, top + 27, 413, 8.6, max_height=35)
    box(36, 633, 540, 1, '#d8e3e0')
    text('EDUCATION & PROFESSIONAL CREDENTIALS', 36, 643, 540, 9, TEAL, True)
    photo('claude-certified.png', 36, 665, 48, 48, crop=False)
    photo('aws-certified.png', 91, 665, 48, 48, crop=False)
    c.linkURL(CLAUDE_BADGE, (36, H - 665 - 48, 36 + 48, H - 665), relative=0)
    c.linkURL(AWS_BADGE, (91, H - 665 - 48, 91 + 48, H - 665), relative=0)
    text('<b>B.E., Electronics & Telecommunication</b> · Utkal University, India<br/>'
         f'<link href="{CLAUDE_BADGE}">Claude Certified Architect - Professional (2026)</link><br/>'
         f'TCS Generative AI Executive Level (2025) · <link href="{AWS_BADGE}">AWS Solutions Architect - Associate (2024)</link><br/>'
         'Sun Certified Java Programmer (SCJP - SE 5.0)', 153, 665, 423, 8.2, max_height=55)
    footer(1)


def project(p, index, top):
    photo(p['image'] + '.jpg', 36, top, 156, 108)
    text(f'0{index} / {escape(p["domain"].upper())}', 208, top, 368, 8, TEAL, True)
    text(escape(p['full']), 208, top + 18, 368, 17, INK, True, max_height=48)
    text(escape(p['role']), 208, top + 70, 368, 9, TEAL, True)
    text(escape(p['tags']), 208, top + 87, 368, 8, MUTED, max_height=23)
    summaries = [
        'Architected a GxP-validated copilot combining RAG, multi-agent drafting, and a cell and gene therapy knowledge graph across six programs. Medical writers retain accountability for clinical and regulatory content.',
        'Architected segment-aware pricing for ~1,200 generic pharmaceutical SKUs. Demand and bid-win models feed Gurobi optimization, with LLM explanations in Salesforce CPQ and early warnings of competitive price erosion.',
        'Designed an AWS event-driven agent pipeline for 6.5M claims annually, gathering API evidence and checking policy and coding. Exceptions reach evaluators with reasoning; the rules engine remains the system of record and humans review every denial.',
        'Architected document AI, income and asset verification agents, a guideline copilot, and conditions automation inside Encompass for ~38,000 loans annually. Human underwriters retain credit decisions, with fair-lending testing and SR 11-7 controls.']
    text(summaries[index - 1], 36, top + 119, 540, 9.4, max_height=51)
    box(36, top + 177, 540, 58)
    selected = [p['metrics'][0], p['metrics'][1], p['metrics'][3]]
    for i, (v, label) in enumerate(selected):
        text(escape(v), 47 + i * 178, top + 183, 168, 19, TEAL, True)
        text(escape(label), 47 + i * 178, top + 211, 168, 8, MUTED)
    text('CONCEPTUAL WORKFLOW', 36, top + 245, 540, 7, MUTED, True)
    for i, step in enumerate(p['steps']):
        x = 36 + i * 139
        box(x, top + 260, 123, 33)
        text(escape(step), x + 7, top + 266, 109, 8, TEAL, max_height=24)
        if i < 3:
            text('>', x + 127, top + 267, 12, 10, TEAL, True)
    text(f'<link href="{WEB}projects/{p["slug"]}.html">Read full case study online &gt;</link>',
         36, top + 300, 540, 8, TEAL)


if __name__ == '__main__':
    projects = runpy.run_path(str(ROOT / 'scripts' / 'build.py'))['PROJECTS']
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(OUTPUT), pagesize=(W, H), pageCompression=1, invariant=1)
    c.setTitle('Puspamitra Mishra | Executive Profile & Selected AI Projects')
    c.setAuthor('Puspamitra Mishra')
    c.setSubject('Career summary, education, credentials, and four enterprise AI case studies')
    overview()
    for page in range(2):
        box(0, 0, W, 8, TEAL)
        text('SELECTED AI PROJECTS', 36, 25, 540, 9, TEAL, True)
        text(['Life sciences & pharmaceutical intelligence', 'Insurance & lending intelligence'][page],
             36, 43, 540, 19, INK, True)
        for j in range(2):
            index = page * 2 + j
            project(projects[index], index + 1, 84 + j * 320)
        text('Source: supplied Project Highlights Summary; outcomes are reported. Photos are illustrative (Unsplash).',
             36, 719, 540, 7, MUTED)
        footer(page + 2)
    c.save()
    shutil.copyfile(OUTPUT, ASSETS / OUTPUT.name)
    print(f'Built {OUTPUT} and copied to site/assets/ ({OUTPUT.stat().st_size:,} bytes).')
