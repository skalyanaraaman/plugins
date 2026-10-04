# Handwriting Storybook

Ask for a storybook and get a printable, brand-new story that a child traces, finishes and colors in. Every run
invents a fresh, funny, school-appropriate story: a detective notebook, a space-cadet log, a pet's diary and more.
You do not need to supply an idea.

![Cover and first page of a sample storybook](assets/sample-pages.png)

## What you get
A Letter-size PDF on college-ruled notebook paper:
- **Cover** with the title, a pencil-sketch cast to color, and a "This diary belongs to" line.
- **Story pages** (13 by default). The story is printed as dotted letters to trace, wrapped around a cartoon. Each page
  has a **YOUR TURN** writing prompt with a traced sentence starter, an optional **DRAW IT** box, and a
  **WORD WIZARD** vocabulary word to trace.
- **Closing page** where the child writes their own entry and signs as the author.

Every line of text sits exactly on a ruled line, so tracing feels like real handwriting practice.

## Try it
- "Make a handwriting storybook."
- "Make a storybook for my 8-year-old who loves cats. Roomier lines, 10 pages."
- "Another one, but as a space-cadet log."

Print at 100% scale on Letter paper.

## What this plugin runs
The skill works with local files only. It does not send data anywhere.
- **xelatex** typesets the PDF, using the three bundled fonts (Delius, Patrick Hand, Permanent Marker).
- **Python 3 with Playwright and Chromium** renders the pencil-sketch drawings from SVG to PNG.
- **pdftoppm** (poppler) and **ImageMagick** make page previews, which Claude checks before delivering.
- `scripts/check_setup.py` reports missing tools and prints install commands. Nothing is installed without your OK.
  First-time setup can download TeX (about 100 MB), Playwright, and Chromium (about 100 MB).
- On claude.ai, these tools run in Claude's code-execution sandbox.

## Bundled files
The plugin ships three TrueType fonts. The LaTeX template and the drawing renderer load them to set the letters.
They are data only. Nothing executes them. Each one is the Google Fonts design from the @fontsource package,
converted from WOFF2 to TrueType with no other change.

| Font | License | SHA-256 |
|---|---|---|
| Delius | SIL OFL 1.1 | 20e2527a8e616dbdd65a45aab9e079cb2156b8452c33e2ad8fc13d9a4e3f7a4b |
| Patrick Hand | SIL OFL 1.1 | f4368b19bd9b8096bac2224a8d7ed9a4e1580a3a120a95001ec613afd944ff81 |
| Permanent Marker | Apache 2.0 | c7827fe87873e2a0de1af16f50b37a8ccd27e10e9b9890296c2881936bc10e72 |

## License
PolyForm Noncommercial 1.0.0. It is free for personal use, families, teachers, schools and other noncommercial
organizations. For commercial use, contact hello@pori.dev. The bundled fonts keep their own open licenses,
listed above.

Made by [Spark Labs](https://pori.dev).
