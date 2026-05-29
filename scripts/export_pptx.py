#!/usr/bin/env python3
"""
PPTX & PDF Export Script — True Browser Full-Screen Export (v7.0)
==================================================================
Goal: exported PPTX/PDF pages must be VISUALLY INDISTINGUISHABLE
from opening the HTML in a real browser and pressing F11 (full-screen).

Strategy:
  1. Launch headless Chromium with GPU-enabling flags so backdrop-filter
     (glassmorphism blur), gradients, and shadows render identically to
     a real browser.
  2. Force sRGB color profile for accurate color rendering.
  3. Wait for the FULL CSS transition (0.6s) + buffer before capturing.
  4. Screenshot at 1920×1080 @2x retina (3840×2160 PNG) — this is the
     raw full-screen view, embedded as-is into PPTX/PDF.

Headless vs real browser:
  - NO browser chrome in headless mode (no title bar, tabs, address bar,
    OS window decorations). The 1920×1080 viewport IS the full canvas.
  - GPU flags (--use-gl=angle, --use-angle=swiftshader) ensure
    backdrop-filter / glassmorphism / complex gradients render correctly.
  - --force-color-profile=srgb ensures colors match the real browser.

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
        # ── GPU / rendering flags for headless Chromium ──
        # Without GPU, backdrop-filter (glassmorphism blur) renders as a
        # flat background — the #1 reason exported PPTX looks "washed out"
        # compared to a real browser. These flags enable software GPU
        # (SwiftShader via ANGLE) so every CSS effect matches the browser.
        chromium_args = [
            "--headless=new",               # new headless = closer to real browser
            "--use-gl=angle",              # ANGLE backend (Windows-native OpenGL→D3D)
            "--use-angle=swiftshader",     # software GPU (no hardware GPU needed)
            "--force-color-profile=srgb",  # sRGB = standard Web color space
            "--enable-gpu-rasterization",  # GPU-accelerated 2D canvas
            "--enable-font-antialiasing",  # smooth font rendering
            "--disable-low-res-tiling",    # full-resolution compositing
            "--num-raster-threads=4",      # parallel rasterization
            "--force-device-scale-factor=2",  # retina-quality at the driver level
        ]

        browser = p.chromium.launch(headless=True, args=chromium_args)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            # ^ 16:9 Full HD (standard presentation resolution).
            #   No browser chrome in headless mode = this IS the full canvas.
            device_scale_factor=2,  # retina-quality → 3840×2160 PNG
        )
        page = context.new_page()

        # Navigate to HTML
        print(f"Loading (16:9 FHD viewport, GPU on): {file_url}")
        page.goto(file_url, wait_until="domcontentloaded", timeout=60000)

        # Wait for Tailwind CDN to finish compiling CSS + all fonts to load
        page.wait_for_function(
            """
            () => {
                const ready = document.fonts ? document.fonts.ready : Promise.resolve();
                return ready.then(() => true);
            }
            """,
            timeout=30000,
        )
        # Extra buffer for Tailwind CDN to finish compiling all utility classes
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
            # Let CSS transition fully settle (CSS transition = 0.6s,
            # wait 1.2s = 2× transition time for safety + reflow)
            page.wait_for_timeout(1200)

            # Screenshot the visible viewport (full_page=False = capture only
            # the 1920×1080 visible area — this is exactly the user's
            # full-screen browser view at F11, 16:9 FHD)
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
