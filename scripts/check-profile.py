"""Validate PDF content and render review images; requires pymupdf and pypdf."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.tools' / 'pdf'))
import pymupdf
from pypdf import PdfReader

profile = ROOT / 'site/assets/puspamitra-mishra-profile.pdf'
reader = PdfReader(profile)
assert len(reader.pages) == 3
content = '\n'.join(page.extract_text() for page in reader.pages)
for expected in ['Puspamitra Mishra', 'MetLife', 'Citigroup', 'Citibank', 'CVS Health',
                 'Utkal University', 'Claude Certified', 'TCS Generative AI', 'AWS Solutions',
                 'Sun Certified', '$3.8M', '$15.0M', '$14.3M', '$14.7M', 'CONCEPTUAL WORKFLOW']:
    assert expected in content, f'Missing content: {expected}'
assert len(reader.pages[0].images) >= 3, 'Missing portrait or badges'
assert all(len(page.images) >= 2 for page in reader.pages[1:]), 'Missing project photos'
assert all(page.get('/Annots') for page in reader.pages), 'Missing clickable links'
out = ROOT / 'qa' / 'pdf'
out.mkdir(parents=True, exist_ok=True)
doc = pymupdf.open(profile)
for i, page in enumerate(doc):
    page.get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5)).save(out / f'page-{i+1}.png')
print('PASS: three pages, career and credentials, four projects, photos, badges, and links.')
print(f'Rendered pages for visual review: {out}')
