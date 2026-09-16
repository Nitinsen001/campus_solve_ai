"""Temp helper: dump hero-related CSS rules from templates."""
import re, pathlib

BASE = pathlib.Path(__file__).resolve().parent
ROOT = BASE / 'templates'
lines = []
for f in sorted(ROOT.rglob('*.html')):
    txt = f.read_text(encoding='utf-8', errors='ignore')
    blocks = re.findall(r'<style[^>]*>(.*?)</style>', txt, re.S)
    for block in blocks:
        for m in re.finditer(r'([^{}]+)\{([^{}]*)\}', block):
            sel = re.sub(r'\s+', ' ', m.group(1)).strip()
            if 'hero' not in sel:
                continue
            decl = re.sub(r'\s+', ' ', m.group(2)).strip()
            if any(k in decl for k in ('background', 'color', 'box-shadow', '--')):
                lines.append(f"{f.name} :: {sel}\n     {decl[:280]}")

(BASE / '_ui_heroes.txt').write_text('\n'.join(lines), encoding='utf-8')
print('rules:', len(lines))