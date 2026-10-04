#!/usr/bin/env python3
"""Render art/<name>.txt (inner SVG, pencil style) to art/<name>.png with a transparent background.

usage: python3 wrap.py <art dir> name1 name2 ...
Canvas size comes from an optional first line in the .txt:  <!-- size 400x300 -->  (default 290x338, a story page).
100 units = 1 inch at print size; rendered at 300 dpi.
"""
import re, sys, pathlib
from playwright.sync_api import sync_playwright
FONTS = pathlib.Path(__file__).resolve().parent.parent / 'fonts'
ART = pathlib.Path(sys.argv[1]).resolve()
DEFAULT = (290, 338)
K = 3
CSS = f"""
@font-face{{font-family:'PH';src:url('file://{FONTS}/patrick-hand-400.ttf')}}
@font-face{{font-family:'PM';src:url('file://{FONTS}/permanent-marker-400.ttf')}}
.s{{fill:none;stroke:#2f2f2f;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}
.w{{fill:#fff}}
.f{{fill:#2f2f2f;stroke:none}}
.g{{fill:#2f2f2f;fill-opacity:.17;stroke:none}}
.hx{{fill:none;stroke:#2f2f2f;stroke-width:1.1;stroke-opacity:.5;stroke-linecap:round}}
.t{{font-family:'PH';fill:#2f2f2f;font-size:16px}}
.tb{{font-family:'PM';fill:#2f2f2f;font-size:20px}}
"""
def svg(body, w, h):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w*K}" height="{h*K}" viewBox="0 0 {w} {h}">
<style>{CSS}</style>
<defs><filter id="pn" filterUnits="userSpaceOnUse" x="-10" y="-10" width="{w+20}" height="{h+20}">
<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4" result="wv"/>
<feDisplacementMap in="SourceGraphic" in2="wv" scale="2.6" xChannelSelector="R" yChannelSelector="G" result="d"/>
<feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="9" result="gr"/>
<feColorMatrix in="gr" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.4 2.0" result="ga"/>
<feComposite in="d" in2="ga" operator="in"/></filter></defs>
<g filter="url(#pn)">{body}</g></svg>"""
with sync_playwright() as p:
    b = p.chromium.launch()
    for n in sys.argv[2:]:
        body = (ART / f'{n}.txt').read_text()
        m = re.match(r'\s*<!--\s*size\s+(\d+)x(\d+)\s*-->', body)
        w, h = (int(m.group(1)), int(m.group(2))) if m else DEFAULT
        tmp = ART / f'_{n}.html'
        tmp.write_text(f"<html><body style='margin:0;background:transparent'>{svg(body, w, h)}</body></html>")
        pg = b.new_page(viewport={'width': w * K, 'height': h * K})
        pg.goto('file://' + str(tmp))  # must be a file:// page or the fonts do not load
        pg.wait_for_timeout(700)
        pg.screenshot(path=str(ART / f'{n}.png'), omit_background=True)
        pg.close(); tmp.unlink(); print('rendered', n, f'{w}x{h}')
    b.close()
