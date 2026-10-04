#!/usr/bin/env python3
"""Check the tools the storybook needs. Prints OK or the exact install command for each missing tool.

usage: python3 check_setup.py        (exit code 0 = ready)
Nothing is installed by this script.
"""
import importlib.util, platform, shutil, subprocess, sys

mac = platform.system() == 'Darwin'
missing = []

def need(ok, name, mac_cmd, linux_cmd, why):
    print(f"{'OK     ' if ok else 'MISSING'} {name:22} {why}")
    if not ok:
        missing.append((name, mac_cmd if mac else linux_cmd))

need(shutil.which('xelatex') is not None, 'xelatex',
     'brew install --cask basictex   (or TinyTeX, which needs no admin rights)',
     'apt-get install -y texlive-xetex texlive-latex-extra   (run as administrator)',
     'typesets the book')
if shutil.which('kpsewhich'):
    for pkg in ('fontspec', 'tikz', 'eso-pic', 'geometry', 'xcolor'):
        r = subprocess.run(['kpsewhich', f'{pkg}.sty'], capture_output=True, text=True)
        need(bool(r.stdout.strip()), f'  LaTeX package {pkg}', f'tlmgr install {"pgf" if pkg == "tikz" else pkg}',
             f'tlmgr install {"pgf" if pkg == "tikz" else pkg}', '')
need(shutil.which('pdftoppm') is not None, 'pdftoppm (poppler)', 'brew install poppler', 'apt-get install -y poppler-utils   (run as administrator)',
     'page previews and checks')
need(bool(shutil.which('magick') or shutil.which('convert')), 'ImageMagick', 'brew install imagemagick',
     'apt-get install -y imagemagick   (run as administrator)', 'contact sheets')
pw = importlib.util.find_spec('playwright') is not None
need(pw, 'Python playwright', 'python3 -m pip install --user playwright', 'python3 -m pip install --user playwright',
     'renders the pencil-sketch art')
if pw:
    r = subprocess.run([sys.executable, '-c', 'from playwright.sync_api import sync_playwright as s\n'
                        'with s() as p: p.chromium.launch().close()'], capture_output=True, text=True)
    need(r.returncode == 0, '  Chromium for playwright', 'python3 -m playwright install chromium',
         'python3 -m playwright install --with-deps chromium', 'one-time browser download (about 100 MB)')

if missing:
    print('\nInstall the missing tools:')
    for name, cmd in missing:
        print(f'  {name.strip()}: {cmd}')
    sys.exit(1)
print('\nReady.')
