"""Pencil-sketch helpers for storybook art. Each function returns an SVG fragment string.

In a workspace scenes.py:
    import sys; sys.path.insert(0, '<skill>/scripts'); from art_lib import *
    save('art', 's01', person(145, 150, hair='puffs', extras=('glasses',)) + dog(220, 280))   # story page 290x338
    save('art', 'cover', ..., size=(650, 470))
then render:  python3 <skill>/scripts/wrap.py art cover s01

Classes (styled by wrap.py): s = pencil stroke, w = white fill (add to solid shapes), f = solid dark,
g = light gray shading, hx = light hatching, t = hand lettering, tb = marker lettering.
Keep everything 10+ units inside the canvas; label text 12+ units tall.
"""
import math, pathlib

def P(d, c='s', extra=''):
    return f'<path class="{c}" d="{d}"{extra}/>'

def T(x, y, s, size=16, c='t', anchor='middle', extra=''):
    return f'<text class="{c}" x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}"{extra}>{s}</text>'

def C(cx, cy, r, c='s w', extra=''):
    return f'<circle class="{c}" cx="{cx}" cy="{cy}" r="{r}"{extra}/>'

def save(art_dir, name, body, size=(290, 338)):
    """Write art/<name>.txt with its canvas size; render with wrap.py."""
    d = pathlib.Path(art_dir); d.mkdir(parents=True, exist_ok=True)
    (d / f'{name}.txt').write_text(f'<!-- size {size[0]}x{size[1]} -->\n' + body)

# ---------------------------------------------------------------- faces
EYES = {
    'dots': C(-8, -3, 2.4, 'f') + C(8, -3, 2.4, 'f'),
    'ring': C(-8, -3, 4.5, 's') + C(8, -3, 4.5, 's') + C(-8, -3, 1.6, 'f') + C(8, -3, 1.6, 'f'),
    'closed': P('M-12 -2 Q-8 -8 -4 -2 M4 -2 Q8 -8 12 -2'),
    'sleepy': P('M-12 -3 L-4 -3 M4 -3 L12 -3'),
    'side': C(-5, -3, 2.4, 'f') + C(11, -3, 2.4, 'f'),
}
BROWS = {'worried': P('M-15 -14 L-5 -11 M15 -14 L5 -11'), 'determined': P('M-15 -13 L-4 -9 M15 -13 L4 -9'),
         'up': P('M-14 -15 Q-9 -19 -4 -15 M4 -15 Q9 -19 14 -15'), 'think': P('M-14 -13 L-4 -13 M4 -16 Q9 -19 14 -15')}
MOUTHS = {'smile': P('M-10 8 Q0 18 10 8'), 'grin': P('M-10 6 Q0 20 10 6 Z', 's w'),
          'o': '<ellipse class="s w" cx="0" cy="12" rx="5" ry="6"/>', 'flat': P('M-7 11 L7 11'),
          'frown': P('M-8 14 Q0 7 8 14'), 'small': C(0, 11, 3, 's'),
          'wobbly': P('M-9 12 Q-5 9 -2 12 Q2 15 5 12 Q8 9 10 12'), 'smirk': P('M-6 11 Q2 15 9 8')}
MOODS = {'happy': ('dots', None, 'smile'), 'grin': ('dots', None, 'grin'), 'laugh': ('closed', None, 'grin'),
         'proud': ('closed', None, 'smile'), 'shock': ('ring', 'up', 'o'), 'worried': ('dots', 'worried', 'wobbly'),
         'sad': ('dots', 'worried', 'frown'), 'determined': ('dots', 'determined', 'flat'),
         'sleepy': ('sleepy', None, 'small'), 'think': ('side', 'think', 'smirk')}

def face(mood='happy', mouth=True, dy=0):
    e, b, m = MOODS[mood]
    s = EYES[e] + (BROWS[b] if b else '') + (MOUTHS[m] if mouth else '')
    return f'<g transform="translate(0,{dy})">{s}</g>' if dy else s

# ---------------------------------------------------------------- people
ARMS = 'M0 38 L-26 56 M0 38 L26 56'
LEGS = 'M0 70 L-16 104 M0 70 L16 104'
HAIR = {  # (behind head, on top of head)
    'none': ('', ''),
    'spiky': ('', P('M-17 -16 L-13 -34 L-5 -21 L2 -37 L9 -22 L17 -33 L19 -14')),
    'puffs': (C(-31, -6, 11) + C(31, -6, 11), P('M-21 -11 Q-15 -23 -6 -19 Q2 -27 10 -19 Q17 -21 21 -11')),
    'shaggy': ('', P('M-26 2 Q-31 -32 0 -33 Q31 -32 26 2 L21 -8 L16 -2 L11 -11 L5 -3 L0 -11 L-5 -3 L-11 -11 L-16 -2 L-21 -8 Z', 's w')),
    'curly': ('', P('M-22 -10 Q-26 -22 -16 -24 Q-14 -34 -4 -30 Q2 -38 10 -30 Q20 -32 18 -22 Q28 -18 22 -8')),
    'bob': ('', P('M-25 4 Q-28 -30 0 -30 Q28 -30 25 4 L20 4 Q20 -14 0 -16 Q-20 -14 -20 4 Z', 's w')),
    'long': (P('M-24 -4 Q-30 30 -22 44 L22 44 Q30 30 24 -4', 's w'), P('M-24 -4 Q-24 -28 0 -28 Q24 -28 24 -4 Q10 -18 -6 -16 Q-18 -14 -24 -4 Z', 's w')),
    'bun': (C(0, -32, 12) + P('M-8 -38 L8 -26 M-8 -26 L8 -38', 'hx'), P('M-23 -8 Q-29 -18 -19 -22 M23 -8 Q29 -18 19 -22')),
    'cap': ('', P('M-22 -10 Q-20 -30 0 -30 Q20 -30 22 -10 Z', 's w') + P('M22 -10 L40 -8')),
    'bald': ('', P('M-24 -4 Q-31 -8 -26 -15 M24 -4 Q31 -8 26 -15') + P('M-12 -15 Q-4 -20 4 -19', 'hx')),
    # history headwear
    'nemes': (P('M-30 -10 L-34 40 L-18 40 L-20 -4 M30 -10 L34 40 L18 40 L20 -4', 's w') + P('M-31 4 L-21 4 M-32 20 L-20 20 M31 4 L21 4 M32 20 L20 20', 'hx'),
              P('M-26 -6 Q-26 -32 0 -32 Q26 -32 26 -6 L20 -12 L-20 -12 Z', 's w') + P('M-18 -22 L18 -22', 'hx') + P('M0 -32 L0 -40 M-4 -38 L0 -42 L4 -38')),
    'wrap': ('', P('M-25 -6 Q-26 -30 0 -31 Q26 -30 25 -6 Q12 -14 0 -13 Q-12 -14 -25 -6 Z', 's w') + P('M-16 -24 Q0 -18 16 -24', 'hx')),
    'laurel': ('', P('M-22 -16 Q-20 -28 -8 -30 M22 -16 Q20 -28 8 -30') + ''.join(
        f'<ellipse class="s w" cx="{x}" cy="{y}" rx="4" ry="2.2" transform="rotate({r} {x} {y})"/>'
        for x, y, r in [(-20, -20, -60), (-15, -27, -35), (-7, -30, -10), (20, -20, 60), (15, -27, 35), (7, -30, 10)])),
    'helmet': ('', P('M-26 -2 Q-26 -34 0 -34 Q26 -34 26 -2 Z', 's w') + P('M0 -34 Q-6 -50 -2 -56 Q14 -52 18 -36', 's w') + P('M-4 -34 L-4 -2', 'hx')),
    'crown': ('', P('M-20 -18 L-20 -36 L-10 -26 L0 -40 L10 -26 L20 -36 L20 -18 Z', 's w')),
}
EXTRAS = {
    'glasses': C(-9, -3, 7.5, 's') + C(9, -3, 7.5, 's') + P('M-1.5 -4 L1.5 -4'),
    'freckles': ''.join(C(x, y, 1.3, 'f') for x, y in [(-15, 6), (-11, 9), (-16, 11), (15, 6), (11, 9), (16, 11)]),
    'cheeks': C(-14, 6, 4.5, 'g') + C(14, 6, 4.5, 'g'),
    'beard': P('M-22 4 Q-20 34 0 38 Q20 34 22 4 Q12 18 0 18 Q-12 18 -22 4 Z', 's w') + P('M-8 24 L-6 30 M0 26 L0 33 M8 24 L6 30', 'hx'),
    'stache': P('M-21 10 Q-12 -1 0 7 Q12 -1 21 10 Q15 16 6 12 Q0 15 -6 12 Q-15 16 -21 10 Z', 's', ' style="fill:#4a4a4a"'),
    'kohl': P('M-14 -3 L-17 -1 M14 -3 L17 -1'),
}
OUTFITS = {  # drawn after the limbs, before the head
    'none': '',
    'tunic': P('M-12 26 L12 26 L22 80 L-22 80 Z', 's w') + P('M-18 58 L18 58'),
    'robe': P('M-12 26 L12 26 L26 104 L-26 104 Z', 's w') + P('M-6 26 L4 104', 'hx'),
    'kilt': P('M-14 60 L14 60 L20 84 L-20 84 Z', 's w') + P('M-6 62 L-8 82 M0 62 L0 82 M6 62 L8 82', 'hx'),
    'toga': P('M-12 26 L12 26 L22 104 L-22 104 Z', 's w') + P('M-12 28 Q4 52 20 92', 's') + P('M-8 40 Q4 60 14 92', 'hx'),
    'apron': P('M-20 24 Q0 18 20 24 L28 92 L-28 92 Z', 's w') + P('M-10 60 L10 60 L10 74 L-10 74 Z'),
    'coat': P('M-12 26 L12 26 L20 78 L-20 78 Z', 's w') + P('M-15 56 L15 56 M-6 26 L0 40 L6 26'),
}

def person(x, y, mood='happy', s=0.85, hair='none', extras=(), outfit='none', arms=ARMS, legs=LEGS,
           torso='M0 24 L0 70', flip=False, rot=0, front='', mouth=True):
    """Stick person, head centre at (x, y), about 140*s tall. hair: see HAIR. extras: see EXTRAS. outfit: see OUTFITS.
    Long outfits (robe, toga) hide the legs; set legs='M-10 104 L-10 110 M10 104 L10 110' for feet."""
    behind, top = HAIR[hair]
    ex = ''.join(EXTRAS[e] for e in extras)
    no_mouth = any(e in extras for e in ('stache', 'beard'))
    sx = -s if flip else s
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({sx},{s})">{behind}'
            f'{P(torso + " " + arms + " " + legs)}{OUTFITS[outfit]}{C(0, 0, 24)}{top}'
            f'{face(mood, mouth and not no_mouth)}{ex}{front}</g>')

def head(x, y, mood='laugh', s=0.6, hair='curly', extras=()):
    """Just a head (crowds, reaction rows)."""
    behind, top = HAIR[hair]
    return f'<g transform="translate({x},{y}) scale({s})">{behind}{C(0, 0, 24)}{top}{face(mood)}{"".join(EXTRAS[e] for e in extras)}</g>'

# ---------------------------------------------------------------- comic devices
def bubble(x, y, w, h, tx, ty, lines, size=17, c='t'):
    """Rounded speech bubble with a tail pointing at (tx, ty)."""
    bx = min(max(tx, x + 24), x + w - 24); by = y + h
    out = f'<rect class="s w" x="{x}" y="{y}" width="{w}" height="{h}" rx="16"/>'
    out += P(f'M{bx-9} {by-2} L{tx} {ty} L{bx+9} {by-2} Z', 'w', ' style="stroke:none"') + P(f'M{bx-9} {by} L{tx} {ty} L{bx+9} {by}')
    lh = size * 1.15; y0 = y + h / 2 - lh * (len(lines) - 1) / 2 + size * 0.35
    return out + ''.join(T(x + w / 2, f'{y0 + i * lh:.1f}', s, size, c) for i, s in enumerate(lines))

def burst(tx, ty, sc, lines, size=24):
    """Shout starburst; about 175 x 120 units at sc=1."""
    b = P('M145 8 L162 24 L188 12 L192 36 L222 34 L208 56 L236 72 L206 82 L216 108 L186 100 L172 124 L152 104 '
          'L126 122 L120 98 L88 106 L96 82 L64 70 L90 56 L74 32 L104 36 L112 12 L132 24 Z', 's w')
    lh = size * 1.05; y0 = 70 - lh * (len(lines) - 1) / 2 + size * 0.3
    return f'<g transform="translate({tx-64*sc},{ty}) scale({sc})">{b}' + ''.join(T(150, f'{y0 + i * lh:.1f}', s, size, 'tb') for i, s in enumerate(lines)) + '</g>'

def note(x, y, w, h, lines, size=14, rot=0):
    """Taped paper note / sign."""
    cx, cy = x + w / 2, y + h / 2
    lh = size * 1.1; y0 = cy - lh * (len(lines) - 1) / 2 + size * 0.35
    t = ''.join(T(cx, f'{y0 + i * lh:.1f}', s, size) for i, s in enumerate(lines))
    return (f'<g transform="rotate({rot} {cx} {cy})"><rect class="s w" x="{x}" y="{y}" width="{w}" height="{h}"/>{t}'
            + P(f'M{cx-12} {y-5} L{cx+12} {y-5} L{cx+12} {y+6} L{cx-12} {y+6} Z', 's w') + '</g>')

def sparkle(x, y, s=1):
    return f'<g transform="translate({x},{y}) scale({s})">' + P('M0 -16 L4 -4 L16 0 L4 4 L0 16 L-4 4 L-16 0 L-4 -4 Z', 's w') + '</g>'

def heart(x, y, s=1):
    return f'<g transform="translate({x},{y}) scale({s})">' + P('M0 6 Q-14 -4 -8 -10 Q-3 -14 0 -7 Q3 -14 8 -10 Q14 -4 0 6 Z', 's w') + '</g>'

def lightbulb(x, y, s=1):
    return f'<g transform="translate({x},{y}) scale({s})">' + C(0, 0, 15) + P('M-6 14 L6 14 M-5 19 L5 19 M0 -24 L0 -32 M-20 -16 L-27 -22 M20 -16 L27 -22') + '</g>'

def magnifier(cx, cy, hx, hy, r=12):
    """Magnifying glass: lens centred at (cx, cy), handle ending at the hand (hx, hy)."""
    dx, dy = hx - cx, hy - cy; d = math.hypot(dx, dy)
    ex, ey = cx + dx / d * r, cy + dy / d * r
    return (P(f'M{ex:.1f} {ey:.1f} L{hx} {hy}', 's', ' style="stroke-width:4.5"') + C(cx, cy, r, 's w', ' style="fill-opacity:.55"')
            + P(f'M{cx-r*0.5:.1f} {cy-r*0.2:.1f} Q{cx-r*0.4:.1f} {cy-r*0.55:.1f} {cx-r*0.05:.1f} {cy-r*0.6:.1f}', 'hx'))

def dog(x, y, s=1, flip=False, mood='happy'):
    """Dog facing right (flip=True faces left), body centre at (x, y)."""
    mouth = {'happy': P('M50 -3 Q56 2 62 -4'), 'eat': P('M50 -3 L62 -3')}[mood]
    body = ('<ellipse class="s w" rx="36" ry="17"/><ellipse class="g" cx="-10" cy="-5" rx="11" ry="7"/>'
            + P('M-34 -6 Q-56 -20 -46 -38') + P('M-20 14 L-20 32 M-6 16 L-6 32 M14 16 L14 32 M28 12 L28 32')
            + P('M40 -28 L46 -42 L52 -27', 's w') + C(40, -15, 15) + '<ellipse class="s w" cx="55" cy="-9" rx="9" ry="7"/>'
            + P('M30 -26 Q20 -16 25 0 Q33 -4 36 -24 Z', 's w') + C(44, -19, 2.2, 'f') + C(62, -11, 3, 'f') + mouth)
    return f'<g transform="translate({x},{y}) scale({-s if flip else s},{s})">{body}</g>'

def cat(x, y, s=1, flip=False):
    b = ('<ellipse class="s w" rx="28" ry="15"/>' + P('M-26 -4 Q-48 -10 -44 -34') + P('M-14 12 L-14 28 M-2 13 L-2 28 M12 13 L12 28 M22 10 L22 28')
         + P('M24 -26 L28 -42 L36 -30 M42 -30 L50 -42 L52 -24', 's w') + C(38, -16, 14) + C(33, -18, 2, 'f') + C(44, -18, 2, 'f')
         + P('M36 -10 Q38 -7 40 -10 M28 -10 L16 -12 M28 -8 L16 -6 M48 -10 L60 -12 M48 -8 L60 -6', 'hx'))
    return f'<g transform="translate({x},{y}) scale({-s if flip else s},{s})">{b}</g>'

# ---------------------------------------------------------------- history props
def scroll(x, y, w, h, lines=(), size=14):
    """Unrolled scroll with curled ends; optional text lines."""
    out = (P(f'M{x} {y} L{x+w} {y} L{x+w} {y+h} L{x} {y+h} Z', 's w')
           + f'<ellipse class="s w" cx="{x}" cy="{y+h/2}" rx="7" ry="{h/2+6}"/><ellipse class="s w" cx="{x+w}" cy="{y+h/2}" rx="7" ry="{h/2+6}"/>')
    lh = size * 1.2; y0 = y + h / 2 - lh * (len(lines) - 1) / 2 + size * 0.35
    out += ''.join(T(x + w / 2, f'{y0 + i * lh:.1f}', s, size) for i, s in enumerate(lines))
    if not lines:
        out += ''.join(P(f'M{x+12} {y+12+i*10} L{x+w-12} {y+12+i*10}', 'hx') for i in range(int((h - 16) / 10)))
    return out

def pyramid(x, y, w, h=None, shade=True):
    """Pyramid with base centred at (x, y)."""
    h = h or w * 0.62
    out = P(f'M{x-w/2} {y} L{x} {y-h} L{x+w/2} {y} Z', 's w')
    if shade:
        out += P(f'M{x} {y-h} L{x+w*0.12} {y} L{x+w/2} {y} Z', 'g') + ''.join(
            P(f'M{x-w/2+w*k/10} {y-h*k/5} L{x+w/2-w*k/10} {y-h*k/5}', 'hx') for k in range(1, 5))
    return out

def column(x, y, h, w=18):
    """Greek/Roman column, base centred at (x, y)."""
    return (P(f'M{x-w/2-5} {y} L{x+w/2+5} {y} L{x+w/2+5} {y-6} L{x-w/2-5} {y-6} Z', 's w')
            + P(f'M{x-w/2} {y-6} L{x-w/2} {y-h+8} L{x+w/2} {y-h+8} L{x+w/2} {y-6} Z', 's w')
            + P(f'M{x-w/2-6} {y-h+8} L{x+w/2+6} {y-h+8} L{x+w/2+6} {y-h} L{x-w/2-6} {y-h} Z', 's w')
            + ''.join(P(f'M{x-w/2+k*w/4} {y-10} L{x-w/2+k*w/4} {y-h+12}', 'hx') for k in (1, 2, 3)))

def sun(x, y, r=16):
    return C(x, y, r) + ''.join(P(f'M{x+math.cos(a)*(r+5):.1f} {y+math.sin(a)*(r+5):.1f} L{x+math.cos(a)*(r+12):.1f} {y+math.sin(a)*(r+12):.1f}')
                                for a in [i * math.pi / 4 for i in range(8)])

def palm(x, y, h=70):
    return (P(f'M{x} {y} Q{x+6} {y-h/2} {x+2} {y-h}', 's', ' style="stroke-width:3"')
            + ''.join(P(f'M{x+2} {y-h} Q{x+dx/2} {y-h-14} {x+dx} {y-h+dy}') for dx, dy in [(-30, 10), (-22, 22), (28, 8), (24, 22), (2, -6)]))

def boat(x, y, w=80, sail=True):
    out = P(f'M{x-w/2} {y} Q{x} {y+18} {x+w/2} {y} L{x+w/2-8} {y-4} L{x-w/2+8} {y-4} Z', 's w')
    if sail:
        out += P(f'M{x} {y-4} L{x} {y-56}') + P(f'M{x+2} {y-54} Q{x+26} {y-34} {x+2} {y-12} Z', 's w')
    return out

def waves(x, y, w, rows=1, gap=10):
    return ''.join(P(' '.join(f'M{x+i*20} {y+r*gap} q5 -5 10 0 q5 5 10 0' for i in range(int(w // 20))), 'hx') for r in range(rows))

def hieroglyphs(x, y, s=1):
    """A small column of hieroglyph-like doodles (decorative only, not real text)."""
    g = (C(0, 0, 5, 's') + P('M-6 14 L6 14 L0 22 Z', 's') + P('M-6 32 Q0 26 6 32 Q0 38 -6 32') + P('M-5 44 L5 44 M0 40 L0 52'))
    return f'<g transform="translate({x},{y}) scale({s})">{g}</g>'

# ---------------------------------------------------------------- maps
def compass(x, y, r=18):
    return (P(f'M{x} {y-r} L{x+5} {y} L{x} {y+r} L{x-5} {y} Z', 's w') + P(f'M{x} {y-r} L{x+5} {y} L{x-5} {y} Z', 'g')
            + P(f'M{x-r} {y} L{x+r} {y}', 'hx') + T(x, y - r - 5, 'N', 14))

def marker(x, y, n, r=11):
    """Numbered map marker for a label-the-map activity."""
    return C(x, y, r, 's w') + T(x, y + 5, str(n), 15, 'tb')

def river(points, width=2.6):
    """Smooth river through a list of (x, y) points."""
    d = f'M{points[0][0]} {points[0][1]}' + ''.join(
        f' Q{points[i][0]} {points[i][1]} {(points[i][0]+points[i+1][0])/2} {(points[i][1]+points[i+1][1])/2}' for i in range(1, len(points) - 1))
    d += f' L{points[-1][0]} {points[-1][1]}'
    return P(d, 's', f' style="stroke-width:{width}"')

def coast(d):
    """Coastline / region outline from a path string; land gets white fill."""
    return P(d, 's w')
