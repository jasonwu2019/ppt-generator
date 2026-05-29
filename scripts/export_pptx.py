#!/usr/bin/env python3
"""
PPTX & PDF Export Script — Playwright Screenshot-Driven (v4.0)
==============================================================
Pixel-perfect export: opens the HTML in headless Chromium, captures
each <section class="slide"> as a 2x retina screenshot, and embeds
the images as full-slide backgrounds in PPTX + PDF.

Usage:
    python export_pptx.py <input_html> <output_file>

    Output format is detected from extension:
        .pptx  → PowerPoint
        .pdf   → PDF (uses Playwright's built-in PDF generator)

Dependencies:
    playwright, python-pptx, Pillow

Architecture:
    1. Launch headless Chromium via Playwright
    2. Set viewport to 1920×1080 @2x device scale factor (3840×2160 capture)
    3. Use JS to cycle through slide sections, making each active
    4. Screenshot each slide as a full-viewport PNG
    5. PPTX: embed each PNG as a full-slide background image
    6. PDF:  use Playwright's page.pdf() per slide → merged PDF
"""

import sys
import os
from pathlib import Path

PYTHON = sys.executable


# ── Helpers ──────────────────────────────────────────────────

def rel(path: str) -> Path:
    """Resolve a path relative to this script's directory."""
    return (Path(__file__).parent / path).resolve()


# ── Playwright screenshot capture ────────────────────────────

def capture_slides(html_path: str) -> list[bytes]:
    """Open HTML in headless Chromium, screenshot each slide. Returns list of PNG bytes."""
    from playwright.sync_api import sync_playwright

    abs_html = Path(html_path).resolve()
    if not abs_html.exists():
        print(f"ERROR: HTML file not found: {html_path}")
        sys.exit(1)

    file_url = abs_html.as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=2,  # retina-quality captures
        )
        page = context.new_page()

        # Navigate to HTML
        print(f"Loading: {file_url}")
        page.goto(file_url, wait_until="networkidle", timeout=60000)

        # Wait for Tailwind CDN + fonts
        page.wait_for_timeout(3000)

        # Count slides
        slide_count = page.evaluate(
            "() => document.querySelectorAll('.slide').length"
        )
        print(f"Found {slide_count} slides")

        screenshots: list[bytes] = []
        for i in range(slide_count):
            # Make this slide active, others above/below
            page.evaluate(
                f"""
                (() => {{
                    const slides = document.querySelectorAll('.slide');
                    slides.forEach((s, idx) => {{
                        s.classList.remove('active', 'above', 'below');
                        if (idx < {i}) s.classList.add('above');
                        else if (idx > {i}) s.classList.add('below');
                        else s.classList.add('active');
                    }});
                }})()
                """
            )
            # Let CSS transition settle
            page.wait_for_timeout(400)

            # Screenshot the full viewport
            png_bytes = page.screenshot(full_page=False, type="png")
            screenshots.append(png_bytes)
            print(f"  Slide {i + 1}/{slide_count} captured ({len(png_bytes) / 1024:.0f} KB)")

        browser.close()
    return screenshots


# ── PDF export ───────────────────────────────────────────────

def export_pdf(screenshots: list[bytes], output_path: str):
    """Create a PDF from slide screenshots — one image per page, 16:9 landscape."""
    from PIL import Image
    from io import BytesIO

    # Convert PNG bytes to PIL Images
    images: list[Image.Image] = []
    for i, png in enumerate(screenshots):
        img = Image.open(BytesIO(png))
        # Convert RGBA to RGB for PDF
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        images.append(img)
        print(f"  Slide {i + 1}/{len(screenshots)} → PDF page ({img.width}×{img.height})")

    if not images:
        print("ERROR: No slides to export")
        sys.exit(1)

    # Save as multi-page PDF
    first = images[0]
    rest = images[1:]
    first.save(
        output_path,
        save_all=True,
        append_images=rest,
        resolution=150.0,
    )
    print(f"\nPDF created: {output_path} ({os.path.getsize(output_path) / 1024:.0f} KB)")


# ── PPTX export ──────────────────────────────────────────────

def export_pptx(screenshots: list[bytes], output_path: str):
    """Embed screenshots as full-slide images in a PPTX."""
    from pptx import Presentation
    from pptx.util import Inches, Emu
    from pptx.dml.color import RGBColor
    from io import BytesIO

    prs = Presentation()
    # 16:9 = 13.333" x 7.5"
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    slide_w = prs.slide_width
    slide_h = prs.slide_height

    for i, png_bytes in enumerate(screenshots):
        blank_layout = prs.slide_layouts[6]  # blank layout
        slide = prs.slides.add_slide(blank_layout)

        # Insert image as full-slide background
        img_stream = BytesIO(png_bytes)
        slide.shapes.add_picture(
            img_stream,
            left=0,
            top=0,
            width=slide_w,
            height=slide_h,
        )
        print(f"  Slide {i + 1}/{len(screenshots)} embedded in PPTX")

    prs.save(output_path)
    print(f"\nPPTX created: {output_path} ({os.path.getsize(output_path) / 1024:.0f} KB)")


# ── Main ─────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        print("Examples:")
        print("  python export_pptx.py presentation.html output.pptx")
        print("  python export_pptx.py presentation.html output.pdf")
        sys.exit(1)

    input_html = sys.argv[1]
    output_path = sys.argv[2]
    ext = Path(output_path).suffix.lower()

    # ── Check dependencies ──
    deps_ok = True
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
    except ImportError:
        print("ERROR: playwright is not installed.")
        print("  Install: pip install playwright && python -m playwright install chromium")
        deps_ok = False

    try:
        from pptx import Presentation  # noqa: F401
    except ImportError:
        print("ERROR: python-pptx is not installed.")
        print("  Install: pip install python-pptx")
        deps_ok = False

    if not deps_ok:
        sys.exit(1)

    # ── Capture screenshots (shared for both PPTX and PDF) ──
    screenshots = capture_slides(input_html)

    # ── Export ──
    if ext == ".pdf":
        export_pdf(screenshots, output_path)
    elif ext in (".pptx", ".ppt"):
        export_pptx(screenshots, output_path)
    else:
        print(f"ERROR: Unsupported format '{ext}'. Use .pptx or .pdf")
        sys.exit(1)

    print("Done!")


if __name__ == "__main__":
    main()
