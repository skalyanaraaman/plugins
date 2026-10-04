---
name: handwriting-storybook
description: Invent a fresh, funny story and build a printable college-ruled handwriting storybook PDF - dotted text to trace around pencil-sketch cartoons, a YOUR TURN writing prompt, a DRAW IT box and a WORD WIZARD vocabulary word on every page. No story idea needed. Use when someone asks for a handwriting storybook, tracing book, handwriting practice story, or a printable story diary for a child.
---

# Handwriting storybook (trace, write, draw)

The output is a Letter-size PDF that looks like a diary on college-ruled notebook paper: a cover, N story pages, and a
closing page. On every story page:
- The story text is printed as dotted outlines to TRACE. It wraps around a pencil-sketch cartoon, then keeps flowing
  full width under the art.
- A YOUR TURN writing prompt follows, with a traced sentence starter and blank ruled lines.
- An optional DRAW IT box.
- A WORD WIZARD vocabulary word, whose word and meaning are traced too.

Every baseline sits exactly on a ruled line (9/32 in = college ruled).

`<SKILL_DIR>` below means this skill's folder: the "Base directory for this skill" shown when the skill loads.

## 0. Setup (once)
Run `python3 <SKILL_DIR>/scripts/check_setup.py`. It prints OK, or the exact install command for each missing tool
(xelatex, pdftoppm, ImageMagick, Python playwright with Chromium). Tell the person what is missing, and install only
with their OK. The fonts ship in `<SKILL_DIR>/fonts/`, so nothing is downloaded for them.

Work in a new folder, for example `storybooks/<short-title>/`, with `art/` inside.

## 1. Invent the story (the person does NOT supply an idea)
They want a fun, creative, brand-new story every time. Never ask for a premise. Invent it yourself, then give the
title and a one-line pitch in your first message and start building. Use a premise only if they volunteer one.

Invent a fresh one deliberately, not the first idea that comes to mind:
1. **Pick a narrator and format,** and vary it from run to run: a funny middle-school diary (the default), a detective
   notebook, a space-cadet log, a pet's-eye diary, a mad-scientist lab journal, a camp or road-trip journal, a monster
   who just started school, a kid running a tiny business, a school-play disaster, or a time-traveling homework mishap.
2. **Pick a wild central problem that escalates** over the book: a runaway science project, a rumor that grows, a pet with
   a secret talent, a contest, a mix-up with a substitute teacher, or a lie that keeps getting bigger. Do not repeat a
   premise already used in the same conversation.
3. **Invent original characters** with silly, specific names. Never reuse characters, names or plots from existing books,
   shows or films.
4. **Shape:** a funny setup, steady escalation, a big comic peak around pages 9-11, and a warm ending where the hero
   learns or wins something small. Each page ends on a mini hook.
5. **Tone:** kid-funny (embarrassing moments, food, pets, siblings, school), wholesome and school-appropriate. Write at about a
   grade 5-7 reading level, with one new vocabulary word per page.

Defaults (change them only if the person asks):
- **Pages:** 13 story pages + cover + closing page = 15 total. The range is 8 to 16.
- **Density preset** (DENSE is the default, for lots of handwriting):
  - **DENSE:** single spacing, 140-160 words per page, 10 art rows, YOUR TURN + starter + 3-5 blank lines, a draw box on
    at most one or two pages, WORD WIZARD.
  - **BALANCED:** 100-120 words, YOUR TURN + 2 lines, a DRAW IT box of 6 rows, WORD WIZARD.
  - **ROOMY:** `"double": true`, which puts traced text on every OTHER ruled line in bigger letters. 60-75 words, one starter, a
    6-row draw box, WORD WIZARD. Use it when the person says the lines or letters feel too close.
- **Letter spacing** is already loosened. If it still feels tight, raise `LetterSpace` to 12 in `template.tex` and drop
  the trace font to 16pt.
- **Title:** a small first line plus a BIG second line. The big size is set from its length.

## 2. Plan the book: write book.json
Write the plan before any art. In the same message, also write a short character sheet (hair, one signature feature,
outfit) so each character is drawn the same on every page.
```json
{
  "title": "The Case of the Missing Meatloaf",
  "cover": {"small": "THE CASE OF THE MISSING", "big": "MEATLOAF", "art": "cover",
            "tagline": "A DETECTIVE NOTEBOOK TO TRACE, WRITE & DRAW"},
  "pages": [
    {"day": "MONDAY", "art": "s01", "side": "R", "text": "Dear Notebook, ... (one paragraph)",
     "turn": "What would you do if your lunch disappeared?", "starter": "If my lunch disappeared, I would",
     "lines": 5, "wizard": ["announced", "announced (verb): said something out loud to everyone."]},
    {"day": "SUNDAY", "art": "s07", "side": "L", "text": "...", "turn": "What would your disguise look like?",
     "lines": 3, "drawbox": [7, "your best detective disguise"], "wizard": ["disguise", "disguise (noun): ..."]}
  ],
  "closing": {"day": "THE END (OR IS IT?)", "art": "s14", "side": "L", "text": "Dear Notebook, I finished ...",
              "turn": "Write your own story below.", "lines": 8, "drawbox": [7, "your own book cover"], "signline": true}
}
```
Rules (`build_book.py` checks them before compiling):
- **Labels and prompts:** `day` up to 22 characters in caps; `turn` up to 55; `starter` up to 45; draw-box prompt up to 42.
- **WORD WIZARD:** the word must appear in that page's text. The meaning is one kid-friendly sentence of at most 55
  characters, in the format `word (noun): meaning.`
- **Text:** one paragraph per page, with dialogue inline. Use plain text with straight quotes; the build makes them
  curly. Latin letters only, no emoji.
- **Art sides** alternate R and L. `rows` (art height in ruled rows, default 10) gives a 2.4 in wide picture.
- **Row budget:** 33 ruled rows fit on a page: 1 (day) + text rows + turn block + draw box + wizard.
  - Text beside the art holds about 5-6 words per row; below the art, about 9.
  - The turn block is 2 + (1 if there is a starter) + lines. The draw box is 2 + its rows. The wizard is 4.
  - The build warns when a page looks over budget. The page-count check after compiling decides.

## 3. Draw the pencil-sketch art (one transparent PNG per page)
All art is hand-authored SVG in a simple stick-figure doodle style: round heads, dot eyes, line bodies, speech bubbles
and hatching. Chromium renders it with a pencil filter.
- **Sizes:** story pages and the closing page are 290 x 338 units (portrait); the cover is 650 x 470.
- **Write the scenes** in a `scenes.py` with the helpers in `<SKILL_DIR>/scripts/art_lib.py`. Read its docstring.
  ```python
  import sys; sys.path.insert(0, '<SKILL_DIR>/scripts'); from art_lib import *
  save('art', 's01', bubble(20, 14, 250, 44, 150, 112, ["I'LL TAKE THE CASE!"], 20)
                     + person(140, 172, 'determined', 0.84, hair='puffs', extras=('glasses',)) + dog(230, 280, 0.8))
  save('art', 'cover', ..., size=(650, 470))
  ```
- **Helpers available:**
  - People: `person(x, y, mood, scale, hair, extras, outfit, arms, legs, flip, rot)` and `head()`. Moods: happy,
    grin, laugh, proud, shock, worried, sad, determined, sleepy, think. Hair: spiky, puffs, shaggy, curly, bob, long,
    bun, cap, bald and more. Extras: glasses, freckles, cheeks, beard, stache.
  - Animals: `dog()` and `cat()`.
  - Comic devices: `bubble()`, `burst()`, `note()`, `sparkle()`, `heart()`, `lightbulb()`, `magnifier()`.
  - Basic shapes: `P()` (path), `T()` (text), `C()` (circle).
  - Classes: `s` stroke, `w` white fill (add it to solid shapes so the ruled lines don't show through), `f` solid,
    `g` gray shading, `hx` hatching, `t` hand lettering, `tb` marker lettering.
- **Render:** write all scene files in one batch, then render once:
  `python3 <SKILL_DIR>/scripts/wrap.py art cover s01 s02 ...`.
- **Rules:**
  - Keep everything at least 10 units inside the frame, and label text at least 12 units tall.
  - Nothing may overlap a label.
  - Use 3-6 characters or props per scene, with one clear joke or action that matches the page text. A dashed comic
    vignette box (`style="stroke-dasharray:7 5"`) works for a second moment.
  - Original characters only: no logos, brands or known cartoon characters. Grayscale pencil only; the child colors it in.
  - **Cover:** the hero holds the story's key prop high, with side characters, a prop stack and a row of small cheering
    heads along the bottom. Leave the top 110 units empty, because the title is typeset there.
  - **Closing page art:** a friendly animal with a pencil and a "YOUR TURN" bubble.
- **Check:** build contact sheets (`magick s01.png s02.png s03.png s04.png -background white -alpha remove +append -resize
  50% sheet.png`, or `convert` instead of `magick`) and look at them. Fix overlapping text, clipped shapes, missing
  bodies, and labels that cross limbs.

## 4. Build and check (this loop is not optional)
```bash
python3 <SKILL_DIR>/scripts/build_book.py book.json
```
It checks the plan, compiles twice, and prints `OK` or `FAIL` with the reason. It writes the PDF to `out/`, contact
sheets (`_build/sheet*.png`, 5 pages each), and a zoomed crop of page 2 (`_build/zoom-*.png`).
- **FAIL "N pages, expected M":** a page spilled over. Shorten that page's text, lines or draw-box rows, then rebuild.
- **Look at every contact sheet:**
  - The traced text ends above YOUR TURN.
  - Nothing overlaps the art.
  - The WORD WIZARD lines are fully on the page.
  - A page with a lot of empty space can take 1-2 more blank lines.
- **Look at the zoomed crop:** the text must sit ON the blue rules, with crisp dots.
- Fix, rebuild, and re-render only the art you changed.

## 5. Deliver
- On claude.ai, send the PDF with SendUserFile. Elsewhere, give the path in `out/` (and run `open` on it on a Mac).
- In 2-3 sentences, give:
  - the title
  - what is inside (cover, N story pages, closing page; trace, write, draw and vocabulary)
  - a reminder to print at 100% scale on Letter paper
  - one next step, such as roomier double-spaced tracing, a different density, or a brand-new story in another style
- Keep `book.json`, `scenes.py` and `art/`, so edits only need a rebuild.
