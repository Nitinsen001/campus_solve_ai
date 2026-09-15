#!/usr/bin/env python3
"""
Comprehensive color re-theme script.
Transforms the dark green palette to a light neutral palette across all CSS and JS files.

Target Palette:
  #FFFFFF — Pure White / Main Background
  #E0E0E0 — Light Gray / Secondary Surface / Border
  #616161 — Medium Gray / Secondary Text / Icons
  #212121 — Dark Gray / Primary Text
"""
import re
from pathlib import Path

BASE = Path("/home/jatin/Desktop/campus_solve_ai/campus_solve_ai/static")

# ============================================================
# COLOR REPLACEMENT MAP — ordered from most specific to least
# ============================================================

# Hex color replacements (lowercase input → output)
# These are safe to replace globally in CSS/JS
HEX_REPLACEMENTS = {
    # ---- Status colors: KEEP semantic ----
    '#f59e0b': '#f59e0b',
    '#fbbf24': '#fbbf24',
    '#d97706': '#d97706',
    '#ca8a04': '#ca8a04',
    '#b45309': '#b45309',
    '#ef4444': '#ef4444',
    '#f87171': '#f87171',
    '#dc2626': '#dc2626',
    '#fecaca': '#fecaca',
    '#fde68a': '#fde68a',

    # ---- Green palette → light neutral ----
    '#051F20': '#212121',   # darkest → primary text
    '#0B2B26': '#FFFFFF',   # dark green bg → white
    '#163832': '#E0E0E0',   # primary green → light gray
    '#235347': '#212121',   # secondary green → primary text
    '#8EB69B': '#616161',   # sage → secondary text
    '#DAF1DE': '#FFFFFF',   # light mint → white

    # ---- Light backgrounds → light neutral ----
    '#f8fafc': '#FFFFFF',
    '#f8f9fa': '#FFFFFF',
    '#f5f7fa': '#FFFFFF',
    '#e8ecf3': '#E0E0E0',
    '#f1f5f9': '#F5F5F5',
    '#e2e8f0': '#E0E0E0',
    '#dee2e6': '#E0E0E0',
    '#f5f5f5': '#F5F5F5',

    # ---- Dark backgrounds → light ----
    '#111111': '#212121',
    '#0b0b0f': '#212121',
    '#050505': '#212121',
    '#0f172a': '#212121',

    # ---- Text colors ----
    '#1e293b': '#212121',
    '#334155': '#212121',
    '#475569': '#616161',
    '#64748b': '#616161',
    '#94a3b8': '#9E9E9E',
    '#495057': '#616161',
    '#6c757d': '#616161',

    # ---- White ----
    '#ffffff': '#FFFFFF',

    # ---- Misc accent colors → neutral ----
    '#065f46': '#212121',
    '#0e7490': '#212121',
    '#155e75': '#616161',
    '#92400e': '#92400e',

    # ---- Purple/pink/blue/green accents → neutral ----
    '#8b5cf6': '#212121',
    '#6d28d9': '#212121',
    '#4338ca': '#212121',
    '#f472b6': '#616161',
    '#db2777': '#212121',
    '#be185d': '#212121',
    '#ec4899': '#212121',
    '#0d6efd': '#212121',
    '#0dcaf0': '#616161',
    '#0ea5e9': '#212121',
    '#6366f1': '#616161',
    '#10b981': '#2E7D32',
    '#059669': '#212121',
    '#047857': '#212121',
    '#34d399': '#616161',
    '#4ade80': '#616161',
    '#14b8a6': '#212121',
    '#0d9488': '#212121',
    '#5eead4': '#616161',
}

# Specific regex-based replacements for context-sensitive values
# Pattern → replacement function(match)
CONTEXT_REPLACEMENTS = [
    # ---- PROPERTY-SPECIFIC: must run BEFORE hex replacements ----
    # Handle dual-use colors (bg vs text)
    
    # Text colors on light bg
    (r'(color:\s*)#0B2B26', r'\g<1>#212121'),
    (r'(color:\s*)#051F20', r'\g<1>#212121'),
    
    # Caret on light inputs
    (r'(caret-color:\s*)#DAF1DE', r'\g<1>#212121'),
    (r'(caret-color:\s*)#051F20', r'\g<1>#212121'),
    
    # Autofill text on light bg
    (r'(-webkit-text-fill-color:\s*)#DAF1DE', r'\g<1>#212121'),
    
    # Hero gradient → dark gray gradient
    (r'radial-gradient\(120% 140% at 0% 0%, #051F20 0%, #0B2B26 35%, #235347 70%, #051F20 100%\)',
     'linear-gradient(135deg, #212121 0%, #424242 100%)'),
    
    # Page header gradient → dark gray
    (r'linear-gradient\(135deg, #235347 0%, #163832 50%, #051F20 100%\)',
     'linear-gradient(135deg, #212121 0%, #424242 100%)'),
    
    # Green-tinted rgba shadows → neutral
    (r'rgba\(35,\s*83,\s*71,\s*([\d.]+)\)', lambda m: f'rgba(0, 0, 0, {min(float(m.group(1)) * 0.5, 0.2)})'),
    (r'rgba\(22,\s*56,\s*50,\s*([\d.]+)\)', lambda m: f'rgba(0, 0, 0, {min(float(m.group(1)) * 0.5, 0.15)})'),
    (r'rgba\(5,\s*31,\s*32,\s*([\d.]+)\)', lambda m: f'rgba(0, 0, 0, {min(float(m.group(1)) * 0.5, 0.12)})'),
    (r'rgba\(11,\s*43,\s*38,\s*([\d.]+)\)', lambda m: f'rgba(0, 0, 0, {min(float(m.group(1)) * 0.5, 0.12)})'),
    (r'rgba\(142,\s*182,\s*155,\s*([\d.]+)\)', lambda m: f'rgba(97, 97, 97, {m.group(1)})'),
    (r'rgba\(218,\s*241,\s*222,\s*([\d.]+)\)', lambda m: f'rgba(255, 255, 255, {m.group(1)})'),
    
    # Red-family rgba → keep semantic
    (r'rgba\(220,\s*38,\s*38,\s*([\d.]+)\)', lambda m: f'rgba(220, 38, 38, {m.group(1)})'),
    (r'rgba\(185,\s*28,\s*28,\s*([\d.]+)\)', lambda m: f'rgba(185, 28, 28, {m.group(1)})'),
    (r'rgba\(153,\s*27,\s*27,\s*([\d.]+)\)', lambda m: f'rgba(153, 27, 27, {m.group(1)})'),
    (r'rgba\(127,\s*29,\s*29,\s*([\d.]+)\)', lambda m: f'rgba(127, 29, 29, {m.group(1)})'),
    (r'rgba\(239,\s*68,\s*68,\s*([\d.]+)\)', lambda m: f'rgba(239, 68, 68, {m.group(1)})'),
    
    # Purple rgba → neutral
    (r'rgba\(139,\s*92,\s*246,\s*([\d.]+)\)', lambda m: f'rgba(33, 33, 33, {m.group(1)})'),
    (r'rgba\(124,\s*58,\s*237,\s*([\d.]+)\)', lambda m: f'rgba(33, 33, 33, {m.group(1)})'),
    (r'rgba\(109,\s*40,\s*217,\s*([\d.]+)\)', lambda m: f'rgba(33, 33, 33, {m.group(1)})'),
    
    # Pink rgba → neutral
    (r'rgba\(244,\s*114,\s*182,\s*([\d.]+)\)', lambda m: f'rgba(97, 97, 97, {m.group(1)})'),
    (r'rgba\(236,\s*72,\s*153,\s*([\d.]+)\)', lambda m: f'rgba(33, 33, 33, {m.group(1)})'),
    
    # Blue rgba → neutral
    (r'rgba\(13,\s*110,\s*253,\s*([\d.]+)\)', lambda m: f'rgba(97, 97, 97, {m.group(1)})'),
    
    # Green success rgba → keep semantic
    (r'rgba\(16,\s*185,\s*129,\s*([\d.]+)\)', lambda m: f'rgba(46, 125, 50, {m.group(1)})'),
    (r'rgba\(52,\s*211,\s*153,\s*([\d.]+)\)', lambda m: f'rgba(46, 125, 50, {m.group(1)})'),
    (r'rgba\(74,\s*222,\s*128,\s*([\d.]+)\)', lambda m: f'rgba(46, 125, 50, {m.group(1)})'),
    
    # Blue-gray rgba → neutral
    (r'rgba\(226,\s*232,\s*240,\s*([\d.]+)\)', lambda m: f'rgba(33, 33, 33, {m.group(1)})'),
    (r'rgba\(15,\s*23,\s*42,\s*([\d.]+)\)', lambda m: f'rgba(0, 0, 0, {m.group(1)})'),
    
    # High-opacity white bg → keep white
    (r'rgba\(255,\s*255,\s*255,\s*(0\.[89]\d?)\)', lambda m: f'rgba(255, 255, 255, {m.group(1)})'),
    # Medium-opacity white → keep white
    (r'rgba\(255,\s*255,\s*255,\s*(0\.[5-7]\d?)\)', lambda m: f'rgba(255, 255, 255, {m.group(1)})'),
]


def apply_hex_replacements(content: str) -> str:
    """Apply hex color replacements, case-insensitive."""
    for old, new in HEX_REPLACEMENTS.items():
        content = re.sub(re.escape(old), new, content, flags=re.IGNORECASE)
    return content


def apply_context_replacements(content: str) -> str:
    """Apply context-sensitive regex replacements."""
    for pattern, replacement in CONTEXT_REPLACEMENTS:
        content = re.sub(pattern, replacement, content)
    return content


def process_css_file(filepath: Path) -> None:
    """Process a single CSS file."""
    content = filepath.read_text(encoding='utf-8')
    original = content
    # Context-aware replacements FIRST (property-specific patterns)
    # must run before global hex replacements to avoid double-conversion
    content = apply_context_replacements(content)
    content = apply_hex_replacements(content)
    if content != original:
        filepath.write_text(content, encoding='utf-8')
        print(f"  ✅ Updated: {filepath.relative_to(BASE.parent)}")
    else:
        print(f"  ⚪ No changes: {filepath.relative_to(BASE.parent)}")


def process_js_file(filepath: Path) -> None:
    """Process a single JS file."""
    content = filepath.read_text(encoding='utf-8')
    original = content
    # Context-aware replacements FIRST (property-specific patterns)
    # must run before global hex replacements to avoid double-conversion
    content = apply_context_replacements(content)
    content = apply_hex_replacements(content)
    if content != original:
        filepath.write_text(content, encoding='utf-8')
        print(f"  ✅ Updated: {filepath.relative_to(BASE.parent)}")
    else:
        print(f"  ⚪ No changes: {filepath.relative_to(BASE.parent)}")


def main():
    print("🎨 Green Palette Re-theme Script")
    print("=" * 60)

    # Process page CSS files
    print("\n📄 Processing page CSS files...")
    pages_css = BASE / "css" / "pages"
    for f in sorted(pages_css.glob("*.css")):
        process_css_file(f)

    # Process main.css (already partially done, apply remaining)
    print("\n📄 Processing main.css...")
    process_css_file(BASE / "css" / "main.css")

    # Process JS files
    print("\n📄 Processing JS files...")
    pages_js = BASE / "js" / "pages"
    for f in sorted(pages_js.glob("*.js")):
        process_js_file(f)

    # Process main.js
    process_js_file(BASE / "js" / "main.js")

    print("\n" + "=" * 60)
    print("✅ Re-theme complete!")


if __name__ == "__main__":
    main()
