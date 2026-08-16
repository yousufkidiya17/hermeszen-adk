#!/usr/bin/env python3
"""markdown-toc: insert a nested table of contents into a Markdown file."""
import re
import sys
import unicodedata
from pathlib import Path

START = '<!-- toc -->'
END = '<!-- /toc -->'


def slugify(title, used):
    s = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode()
    s = re.sub(r'[^\w\s-]', '', s).lower().strip()
    s = re.sub(r'[-\s]+', '-', s)
    base, n = s, 1
    while s in used:
        n += 1
        s = '%s-%d' % (base, n)
    used.add(s)
    return s


def find_headings(text):
    out, used, in_code = [], set(), False
    for i, ln in enumerate(text.splitlines()):
        if ln.strip().startswith('```'):
            in_code = not in_code
        if in_code or not ln.startswith('#'):
            continue
        m = re.match(r'(#{1,6})\s+(.*)', ln)
        if m:
            lvl = len(m.group(1))
            title = re.sub(r'[`*_\[\]]', '', m.group(2)).strip()
            out.append((lvl, title, slugify(title, used), i))
    return out


def render_toc(headings):
    if not headings:
        return ''
    base = headings[0][0]
    return '\n'.join('%s- [%s](#%s)' % ('  ' * (lvl - base), t, a)
                     for lvl, t, a, _ in headings)


def insert_toc(text, toc, headings):
    lines = text.splitlines(keepends=True) or ['']
    s = next((i for i, l in enumerate(lines) if l.strip() == START), None)
    if s is not None:
        e = next((i for i in range(s + 1, len(lines)) if lines[i].strip() == END), None)
        inner = ('%s\n' % toc) if toc else ''
        tail = lines[s + 1:] if e is None else lines[e + 1:]
        return ''.join(lines[:s + 1]) + inner + END + '\n' + ''.join(tail)
    if not headings:
        return text
    block = '%s\n%s\n%s\n' % (START, toc, END)
    idx = headings[0][3]
    return ''.join(lines[:idx + 1]) + block + ''.join(lines[idx + 1:])


def main(argv):
    if len(argv) < 2:
        sys.stderr.write('usage: markdown-toc INPUT.md [OUTPUT.md]\n')
        return 2
    src = Path(argv[1])
    dst = Path(argv[2]) if len(argv) > 2 else src
    text = src.read_text(encoding='utf-8')
    headings = find_headings(text)
    toc = render_toc(headings)
    dst.write_text(insert_toc(text, toc, headings), encoding='utf-8')
    plural = '' if len(headings) == 1 else 's'
    print('Wrote %s (%d heading%s)' % (dst, len(headings), plural))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
