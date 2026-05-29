#!/usr/bin/env python3
"""
PPTX & PDF Export Script — 16:9 Full-Screen Viewport Screenshot (v6.0)
=======================================================================
Pixel-perfect export: opens the HTML in headless Chromium at 1920×1080
(FHD 16:9 — the standard full-screen presentation resolution), waits for
Tailwind CSS + all web fonts to fully load, then captures each
<section class="slide"> as a retina-quality (3840×2160) viewport screenshot.

Headless Chromium has NO browser chrome (no title bar, no tabs, no address
bar, no OS window decorations). The 1920×1080 viewport IS the entire visible
area — exactly what a user sees when they press F11 in a real browser at
1920×1080. The exported file is pixel-identical to the browser full-screen view.

Usage:
    python export_pptx.py <input_html> <output_file>

    Output format is detected from extension:
        .pptx  → PowerPoint
        .pdf   → PDF (multi-page, one screenshot per page)

Dependencies:
    playwright, python-pptx, Pillow

Architecture:
    1. Launch headless Chromium (no browser chrome — effectively full-screen)
    2. Set viewport to 1920×1080 (16:9 FHD) @2x device scale → 3840×2160 PNG
    3. Wait for Tailwind CDN to finish compiling CSS
    4. Wait for all web fonts (Google Fonts) to load via document.fonts.ready
    5. Cycle through slides via JS (sets .active class, others .above/.below)
    6. Wait for CSS transition (0.6s) to settle
    7. Screenshot the viewport (full_page=False) — this captures the exact
       1920×1080 visible area, which IS the full-screen browser view
    8. PPTX: embed each PNG as full-slide background (16:9, 13.333" × 7.5")
    9. PDF:  stitch screenshots into multi-page PDF at 150dpi
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
        # Headless Chromium has NO browser chrome — no title bar, tabs,
        # address bar, or OS window decorations. The viewport IS the
        # full visible area, exactly like F11 full-screen in a real browser.
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            # ^ 16:9 Full HD — the standard presentation resolution.
            #   In headless mode this IS the full visible canvas.
            device_scale_factor=2,  # retina-quality captures → 3840×2160 PNG
        )
        page = context.new_page()

        # Navigate to HTML
        print(f"Loading (16:9 FHD viewport): {file_url}")
        page.goto(file_url, wait_until="domcontentloaded", timeout=60000)

        # Wait for Tailwind CDN to finish compiling CSS + all fonts to load
        page.wait_for_function(
            """
            () => {
                // Wait for Tailwind to initialize (adds .tailwind-ready class or similar)
                // and all fonts to be available
                const ready = document.fonts ? document.fonts.ready : Promise.resolve();
                return ready.then(() => true);
            }
            """,
            timeout=30000,
        )
        # Extra buffer for Tailwind CDN to finish compiling utility classes
        page.wait_for_timeout(2000)

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

            # Screenshot the visible viewport (full_page=False = capture only
            # the 1920×1080 visible area, which is exactly what the user sees
            # in a browser at F11 full-screen on a 16:9 FHD display)
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
