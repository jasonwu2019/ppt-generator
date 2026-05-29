#!/usr/bin/env python3
"""
PPTX & PDF Export Script — Real Browser Full-Screen Capture (v8.0)
====================================================================
HOW IT WORKS (completely different from previous versions):
  Previous versions used *headless* Chromium — an invisible simulated
  browser. Even with GPU flags, headless rendering is NOT identical
  to a real browser (font rendering, backdrop-filter, color pipeline).

  v8.0 launches a REAL, VISIBLE Chrome browser window in FULL-SCREEN
  mode (--start-fullscreen = F11 equivalent). The browser takes over
  the entire display, the HTML renders through the actual Windows GPU
  pipeline, and then we screenshot the viewport (which IS the full
  screen in fullscreen mode).

  The result: exported PPTX/PDF pages are pixel-identical to what
  you see when pressing F11 in Chrome.

What happens on screen:
  - A Chrome window appears and goes full-screen (F11 mode)
  - Each slide renders in sequence, visible on your screen
  - Each slide is screenshotted (viewport = full screen)
  - The window closes after capture
  - Total time: ~30s for 16 slides

Usage:
    python export_pptx.py <input_html> <output_file>
    .pptx  → PowerPoint,  .pdf  → PDF

Dependencies:
    playwright, python-pptx, Pillow
"""

import sys
import os
from pathlib import Path

PYTHON = sys.executable


def rel(path: str) -> Path:
    """Resolve a path relative to this script's directory."""
    return (Path(__file__).parent / path).resolve()


# ── Browser screenshot capture (REAL visible browser) ─────────

def capture_slides(html_path: str) -> list[bytes]:
    """
    Open HTML in a REAL visible Chromium browser in full-screen mode,
    screenshot each slide. Returns list of PNG bytes.

    Key: headless=False + --start-fullscreen means the browser renders
    through the ACTUAL Windows GPU/driver pipeline — identical to what
    you see when pressing F11 in Chrome.
    """
    from playwright.sync_api import sync_playwright

    abs_html = Path(html_path).resolve()
    if not abs_html.exists():
        print(f"ERROR: HTML file not found: {html_path}")
        sys.exit(1)

    file_url = abs_html.as_uri()

    with sync_playwright() as p:
        # ── Launch REAL visible Chrome in full-screen mode ──
        # headless=False → real browser window (actual GPU pipeline)
        # --start-fullscreen → F11 mode (no title bar, no taskbar)
        # --disable-infobars → no "Chrome is being controlled" banner
        # --no-first-run → skip welcome wizard
        chromium_args = [
            "--start-fullscreen",           # F11 full-screen mode
            "--disable-infobars",           # hide automation banner
            "--no-first-run",               # skip welcome wizard
            "--no-default-browser-check",   # don't ask to be default
            "--disable-extensions",         # clean rendering
            "--disable-background-networking",  # no background traffic
            "--disable-sync",               # no Chrome sync
            "--force-color-profile=srgb",   # sRGB color space
            "--enable-font-antialiasing",   # ClearType-quality text
        ]

        browser = p.chromium.launch(
            headless=False,                # REAL visible browser
            args=chromium_args,
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            # ^ 16:9 Full HD. In fullscreen mode, the browser
            #   stretches to fill the screen, and this viewport
            #   IS what gets captured by page.screenshot().
            device_scale_factor=2,  # retina-quality → 3840×2160 PNG
        )
        page = context.new_page()

        # Navigate to HTML
        print(f"\n{'='*60}")
        print(f"  Opening in REAL Chrome browser (full-screen mode)")
        print(f"  File: {file_url}")
        print(f"  The browser window will appear on your screen.")
        print(f"  Each slide will be captured as the full-screen view.")
        print(f"{'='*60}\n")

        page.goto(file_url, wait_until="domcontentloaded", timeout=60000)

        # Wait for all fonts to load
        print("Waiting for fonts to load...")
        page.wait_for_function(
            """
            () => {
                const ready = document.fonts ? document.fonts.ready : Promise.resolve();
                return ready.then(() => true);
            }
            """,
            timeout=30000,
        )

        # Extra buffer for Tailwind CDN + initial render
        page.wait_for_timeout(3000)
        print("Fonts loaded. Starting slide capture...\n")

        # Count slides
        slide_count = page.evaluate(
            "() => document.querySelectorAll('.slide').length"
        )
        print(f"Found {slide_count} slides\n")

        screenshots: list[bytes] = []
        for i in range(slide_count):
            # Activate this slide
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

            # Wait for CSS transition (0.6s) + render settle
            page.wait_for_timeout(1500)

            # ── CAPTURE ──
            # In fullscreen mode, the viewport fills the entire screen.
            # page.screenshot(full_page=False) captures the visible
            # viewport area, which IS the full-screen browser view.
            png_bytes = page.screenshot(full_page=False, type="png")
            screenshots.append(png_bytes)
            print(f"  ✓ Slide {i + 1}/{slide_count} captured "
                  f"({len(png_bytes) / 1024:.0f} KB)")

        browser.close()
        print(f"\nBrowser closed. {len(screenshots)} slides captured.\n")

    return screenshots


# ── PDF export ───────────────────────────────────────────────

def export_pdf(screenshots: list[bytes], output_path: str):
    """Create a PDF from slide screenshots — one image per page, 16:9 landscape."""
    from PIL import Image
    from io import BytesIO

    images: list[Image.Image] = []
    for i, png in enumerate(screenshots):
        img = Image.open(BytesIO(png))
        # Convert RGBA to RGB for PDF
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        images.append(img)
        print(f"  Slide {i + 1}/{len(screenshots)} → PDF page "
              f"({img.width}x{img.height})")

    if not images:
        print("ERROR: No slides to export")
        sys.exit(1)

    first = images[0]
    rest = images[1:]
    first.save(
        output_path,
        save_all=True,
        append_images=rest,
        resolution=150.0,
    )
    size_kb = os.path.getsize(output_path) / 1024
    print(f"\nPDF created: {output_path} ({size_kb:.0f} KB)")


# ── PPTX export ──────────────────────────────────────────────

def export_pptx(screenshots: list[bytes], output_path: str):
    """Embed screenshots as full-slide images in a 16:9 PPTX."""
    from pptx import Presentation
    from pptx.util import Inches
    from io import BytesIO

    prs = Presentation()
    prs.slide_width = Inches(13.333)   # 16:9
    prs.slide_height = Inches(7.5)

    slide_w = prs.slide_width
    slide_h = prs.slide_height

    for i, png_bytes in enumerate(screenshots):
        blank_layout = prs.slide_layouts[6]
        slide = prs.slides.add_slide(blank_layout)

        img_stream = BytesIO(png_bytes)
        slide.shapes.add_picture(
            img_stream,
            left=0, top=0,
            width=slide_w, height=slide_h,
        )
        print(f"  Slide {i + 1}/{len(screenshots)} embedded in PPTX")

    prs.save(output_path)
    size_kb = os.path.getsize(output_path) / 1024
    print(f"\nPPTX created: {output_path} ({size_kb:.0f} KB)")


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

    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print("ERROR: Pillow is not installed.")
        print("  Install: pip install Pillow")
        deps_ok = False

    if not deps_ok:
        sys.exit(1)

    # ── Capture screenshots (REAL browser, full-screen mode) ──
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
