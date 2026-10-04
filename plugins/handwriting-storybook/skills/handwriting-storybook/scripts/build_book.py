#!/usr/bin/env python3
"""Build a handwriting storybook PDF from book.json.

usage: python3 build_book.py path/to/book.json
Reads art PNGs from <book dir>/art/. Writes <book dir>/out/<Title>.pdf and previews in <book dir>/_build/.
Checks the plan first (field lengths, vocabulary word in text, row budget), then compiles twice and checks
the page count, text overflow and missing characters. Exits non-zero on any failure.
"""
import json, math, re, shutil, subprocess, sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TEMPLATE = (SKILL / 'template.tex').read_text()
FONTDIR = SKILL / 'fonts'
ROWS_PER_PAGE = 33

def tex(s):
    """Escape plain text for LaTeX; straight double quotes become curly quotes."""
    s = str(s)
    for a, b in [('\\', ''), ('&', r'\&'), ('%', r'\%'), ('$', r'\$'), ('#', r'\#'), ('_', r'\_'), ('{', ''), ('}', ''),
                 ('~', '-'), ('^', '')]:
        s = s.replace(a, b)
    s = re.sub(r'"(\S[^"]*?)"', r"``\1''", s)
    return s.replace('"', "''")

def text_rows(words, art_rows, double=False):
    """Estimate ruled rows for the traced text (from the skill's row-budget rule)."""
    def single(w, a):
        return a + math.ceil((w - 5.5 * a) / 9) if w > 5.5 * a else math.ceil(w / 5.5)
    if double:
        return 2 * single(words / 0.55, art_rows / 2)
    return single(words, art_rows)

def big_size(title):
    n = len(title)
    return 78 if n <= 8 else 62 if n <= 10 else 48 if n <= 13 else 40

def check_plan(book):
    problems = []
    pages = book['pages'] + ([book['closing']] if book.get('closing') else [])
    for i, p in enumerate(pages):
        tag = f"page {i + 1} ({p.get('day', '?')})"
        for key, limit in [('day', 22), ('turn', 55), ('starter', 45)]:
            if p.get(key) and len(p[key]) > limit:
                problems.append(f'{tag}: "{key}" is {len(p[key])} characters; the limit is {limit}')
        if p.get('drawbox') and len(p['drawbox'][1]) > 42:
            problems.append(f'{tag}: draw-box prompt is longer than 42 characters')
        w = p.get('wizard')
        if w:
            if w[0].lower() not in p['text'].lower():
                problems.append(f'{tag}: WORD WIZARD word "{w[0]}" does not appear in the page text')
            if len(w[1]) > 55:
                problems.append(f'{tag}: WORD WIZARD meaning is {len(w[1])} characters; the limit is 55')
        a = p.get('rows', book.get('art_rows', 10))
        words = len(p['text'].split())
        L = max(a, text_rows(words, a, p.get('double', book.get('double'))))
        turn = (2 + (1 if p.get('starter') else 0) + p.get('lines', 0)) if p.get('turn') else 0
        box = (2 + p['drawbox'][0]) if p.get('drawbox') else 0
        total = 1 + L + turn + box + (4 if w else 0) + (2 if p.get('signline') else 0)
        if total > ROWS_PER_PAGE:
            problems.append(f'WARN {tag}: estimated {total} rows (limit {ROWS_PER_PAGE}, {words} words); '
                            'the estimate is rough, the page-count check after compiling decides')
    sides = [p.get('side', 'R') for p in book['pages']]
    if any(a == b for a, b in zip(sides, sides[1:])):
        problems.append('WARN art sides do not alternate R/L on consecutive pages')
    return problems

def body(book):
    c = book['cover']
    out = [r'\coverpage{%s}{%s}{%d}{%s}{%s}' % (tex(c['small']), tex(c['big']), c.get('size', big_size(c['big'])),
                                                c.get('art', 'cover'), tex(c.get('tagline', 'A DIARY TO TRACE, WRITE & DRAW')))]
    for p in book['pages'] + ([book['closing']] if book.get('closing') else []):
        cmd = r'\entryd' if p.get('double', book.get('double')) else r'\entry'
        out.append('%s{%s}{%s}{%s}{%d}\n{%s}' % (cmd, tex(p['day']), p['art'], p.get('side', 'R'),
                                                 p.get('rows', book.get('art_rows', 10)), tex(p['text'])))
        if p.get('turn'):
            out.append(r'\turnhead{%s}' % tex(p['turn']))
        if p.get('starter'):
            out.append(r'\starter{%s}' % tex(p['starter']))
        if p.get('lines'):
            out.append(r'\lines{%d}' % p['lines'])
        if p.get('drawbox'):
            out.append(r'\drawbox{%d}{%s}' % (p['drawbox'][0], tex(p['drawbox'][1])))
        if p.get('wizard'):
            out.append(r'\wizard{%s}{%s}' % (tex(p['wizard'][0]), tex(p['wizard'][1])))
        if p.get('signline'):
            out.append(r'\signline')
        out.append('')
    return '\n'.join(out)

def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

def main():
    bookfile = Path(sys.argv[1]).resolve()
    book = json.loads(bookfile.read_text())
    root = bookfile.parent
    work, out = root / '_build', root / 'out'
    work.mkdir(exist_ok=True); out.mkdir(exist_ok=True)

    problems = check_plan(book)
    hard = [p for p in problems if not p.startswith('WARN')]
    for p in problems:
        print(('WARN ' if p.startswith('WARN') else 'PLAN ') + p.removeprefix('WARN '))
    if hard:
        print('FAIL fix the story plan above, then build again'); sys.exit(1)

    art = root / 'art'
    needed = [book['cover'].get('art', 'cover')] + [p['art'] for p in book['pages']] + ([book['closing']['art']] if book.get('closing') else [])
    missing = [n for n in needed if not (art / f'{n}.png').exists()]
    if missing:
        print('FAIL missing art PNGs (render them with wrap.py): ' + ', '.join(missing)); sys.exit(1)
    shutil.rmtree(work / 'art', ignore_errors=True); shutil.copytree(art, work / 'art')

    title = book.get('title') or f"{book['cover']['small']} {book['cover']['big']}".title()
    src = TEMPLATE.replace('@FONTDIR@', str(FONTDIR)).replace('@BOOKTITLE@', tex(title)).replace('@BODY@', body(book))
    (work / 'story.tex').write_text(src)
    for _ in range(2):  # two passes: the page overlays need them
        r = run(['xelatex', '-interaction=nonstopmode', '-halt-on-error', 'story.tex'], work)
    log = (work / 'story.log').read_text(errors='replace')
    fails = []
    if r.returncode != 0:
        err = re.findall(r'^! .*(?:\n.*){0,3}', log, re.M)
        fails.append('LaTeX error: ' + (err[0] if err else r.stdout[-600:]))
    expect = 1 + len(book['pages']) + (1 if book.get('closing') else 0)
    m = re.search(r'Output written on .*?\((\d+) pages?', log)
    pages = int(m.group(1)) if m else 0
    if pages and pages != expect:
        fails.append(f'{pages} pages, expected {expect}: a page spilled over. Shorten that page (text, lines or box rows)')
    for m in re.finditer(r'Overfull \\hbox \((\d+\.\d+)pt', log):
        if float(m.group(1)) > 4:
            fails.append(f'a line sticks out of the margin by {m.group(1)}pt: shorten a very long word')
    miss = set(re.findall(r'Missing character: There is no (.) ', log))
    if miss:
        fails.append('fonts are missing characters (use Latin text only, no emoji): ' + ' '.join(sorted(miss)))

    if (work / 'story.pdf').exists():
        pdf = out / (re.sub(r'[^A-Za-z0-9]+', '-', title).strip('-') + '.pdf')
        shutil.copy(work / 'story.pdf', pdf)
        for old in work.glob('pg-*.png'):
            old.unlink()
        run(['pdftoppm', '-r', '62', '-png', 'story.pdf', 'pg'], work)
        im = shutil.which('magick') or shutil.which('convert')
        pngs = sorted(work.glob('pg-*.png'))
        for i in range(0, len(pngs), 5):
            run([im, *map(str, pngs[i:i + 5]), '-background', 'white', '-alpha', 'remove', '+append', f'sheet{i // 5 + 1}.png'], work)
        for p in pngs:
            p.unlink()
        run(['pdftoppm', '-r', '200', '-png', '-f', '2', '-l', '2', '-x', '200', '-y', '150', '-W', '1500', '-H', '700', 'story.pdf', 'zoom'], work)
        print(f'PDF:      {pdf}')
        print(f'Previews: {work}/sheet*.png (5 pages each) and {work}/zoom-*.png (text must sit ON the blue rules)')
    print(('FAIL ' if fails else 'OK   ') + f'{pages} page(s), expected {expect}' + ''.join(f'\n     - {f}' for f in fails))
    sys.exit(1 if fails else 0)

if __name__ == '__main__':
    main()
