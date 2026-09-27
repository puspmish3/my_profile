from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote

errors = []
class CheckLinks(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('src', 'href') and value and not urlsplit(value).scheme:
                parsed = urlsplit(value)
                target = self.path.parent / unquote(parsed.path) if parsed.path else self.path
                if not target.is_file():
                    errors.append((str(self.path), value))
                elif parsed.fragment and target.suffix == '.html':
                    text = target.read_text(encoding='utf-8')
                    if f'id="{parsed.fragment}"' not in text:
                        errors.append((str(self.path), value, 'Missing anchor'))

files = list(Path('site').rglob('*.html'))
for file in files:
    parser = CheckLinks()
    parser.path = file
    parser.feed(file.read_text(encoding='utf-8'))
print(f'Checked {len(files)} HTML pages. Broken local references: {errors}')
raise SystemExit(bool(errors))
