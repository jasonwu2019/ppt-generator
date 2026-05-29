#!/usr/bin/env python3
"""
PPTX & PDF Export Script — Native-Resolution Browser Capture (v9.0)
====================================================================
THE FUNDAMENTAL FIX (what makes this version different):
  Previous versions forced a 1920×1080 viewport regardless of the
  actual monitor resolution. When the monitor is 1280×720 (HD), the
  browser renders at 1920×1080 in a virtual canvas, then the OS
  downscales it to 1280×720 — introducing scaling artifacts.
  v9.0 detects the ACTUAL monitor resolution and sets the viewport
  to match. This makes the rendering pipeline PIXEL-PERFECT at the
  native resolution — identical to opening Chrome and pressing F11.

Other improvements:
  - Hides UI overlays (nav-dots, counter, hint) before capture
    → clean presentation slides, no navigation chrome
  - Captures only the slide element (not the full viewport)
    → no body background, no gaps, pure slide content
  - 3× device scale factor → high-density screenshots
  - Headed Chromium → real GPU pipeline (glassmorphism works)

Usage:
    python export_pptx.py <input_html> <output_file>
    .pptx  → PowerPoint,  .pdf  → PDF

Dependencies:
    playwright, python-pptx, Pillow
"""

import sys
import os
import ctypes
from pathlib import Path

PYTHON = sys.executable


def get_monitor_resolution() -> tuple[int, int]:
    """Detect the primary monitor's native resolution via Windows API."""
    try:
        user32 = ctypes.windll.user32
        width = user32.GetSystemMetrics(0)   # SM_CXSCREEN
        height = user32.GetSystemMetrics(1)  # SM_CYSCREEN
        if width > 0 and height > 0:
            return width, height
    except Exception:
        pass
    # Fallback: assume 1920×1080
    return 1920, 1080


# ── Browser screenshot capture ────────────────────────────────

def capture_slides(html_path: str) -> list[bytes]:
    """
    Open HTML in a real Chromium browser window, match viewport to
    the actual monitor resolution, hide UI overlays, and screenshot
    each slide element at 3× retina quality.
    """
    from playwright.sync_api import sync_playwright

    abs_html = Path(html_path).resolve()
    if not abs_html.exists():
        print(f"ERROR: HTML file not found: {html_path}")
        sys.exit(1)

    file_url = abs_html.as_uri()

    # Detect native monitor resolution
    screen_w, screen_h = get_monitor_resolution()
    print(f"\n  Monitor native resolution: {screen_w}×{screen_h}")

    # Calculate 16:9 viewport that fits within the monitor
    # (maintain 16:9 aspect ratio, constrained by monitor height)
    vp_w = screen_w
    vp_h = screen_h
    # Ensure exactly 16:9 for PPT compatibility
    expected_h = int(vp_w * 9 / 16)
    if expected_h > vp_h:
        # Monitor is wider than 16:9, constrain by height
        vp_h = screen_h
        vp_w = int(vp_h * 16 / 9)
    else:
        vp_h = expected_h

    print(f"  Viewport: {vp_w}×{vp_h} (16:9)")
    print(f"  Scale: 3× → {vp_w * 3}×{vp_h * 3} PNG")

    with sync_playwright() as p:
        # Headed Chromium → real GPU pipeline
        # Window sized to exactly match viewport (plus minimal chrome)
        browser = p.chromium.launch(
            headless=False,
            args=[
                f"--window-size={vp_w + 16},{vp_h + 80}",
                "--window-position=0,0",
                "--disable-infobars",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-extensions",
                "--force-color-profile=srgb",
                "--enable-font-antialiasing",
            ],
        )
        context = browser.new_context(
            viewport={"width": vp_w, "height": vp_h},
            device_scale_factor=3,   # 3× retina
        )
        page = context.new_page()

        print(f"\n{'='*60}")
        print(f"  Opening in Chrome (viewport = monitor = {vp_w}×{vp_h})")
        print(f"{'='*60}\n")

        page.goto(file_url, wait_until="domcontentloaded", timeout=60000)

        # Wait for fonts
        print("Waiting for fonts...")
        page.wait_for_function(
            """
            () => {
                const ready = document.fonts ? document.fonts.ready : Promise.resolve();
                return ready.then(() => true);
            }
            """,
            timeout=30000,
        )
        page.wait_for_timeout(3000)
        print("Fonts loaded.\n")

        # ── Hide UI overlays ──
        page.evaluate("""
            (() => {
                const hide = sel => {
                    const el = document.querySelector(sel);
                    if (el) { el.style.display = 'none'; }
                };
                hide('.nav-dots');
                hide('.slide-counter');
                hide('.instruction-hint');
            })()
        """)

        # Count slides
        slide_count = page.evaluate(
            "() => document.querySelectorAll('.slide').length"
        )
        print(f"Found {slide_count} slides\n")

        screenshots: list[bytes] = []
        for i in range(slide_count):
            # Activate this slide (others above/below)
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

            # Wait for CSS transition (0.6s) × 2.5 + reflow margin
            page.wait_for_timeout(1500)

            # Force layout reflow to ensure all CSS has been applied
            page.evaluate("() => document.body.offsetHeight")

            # Screenshot the active slide element
            # (not the viewport — cleaner, no body background or gaps)
            slide_el = page.locator(".slide.active")
            png_bytes = slide_el.screenshot(type="png")
            screenshots.append(png_bytes)
            print(f"  ✓ Slide {i + 1}/{slide_count} captured "
                  f"({len(png_bytes) / 1024:.0f} KB)")

        browser.close()
        print(f"\nBrowser closed. {len(screenshots)} slides captured.\n")

    return screenshots


# ── PDF export ───────────────────────────────────────────────

def export_pdf(screenshots: list[bytes], output_path: str):
    """Create a PDF from slide screenshots — one image per page, 16:9."""
    from PIL import Image
    from io import BytesIO

    images: list[Image.Image] = []
    for i, png in enumerate(screenshots):
        img = Image.open(BytesIO(png))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        images.append(img)
        print(f"  Slide {i + 1}/{len(screenshots)} → PDF page "
              f"({img.width}×{img.height})")

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
        pic = slide.shapes.add_picture(
            img_stream,
            left=0, top=0,
            width=slide_w, height=slide_h,
        )
        # Disable PPTX compression — keep PNG quality
        try:
            pic.image.auto_compress = False
        except Exception:
            pass
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
        deps_ok = False

    try:
        from pptx import Presentation  # noqa: F401
    except ImportError:
        print("ERROR: python-pptx is not installed.")
        deps_ok = False

    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        print("ERROR: Pillow is not installed.")
        deps_ok = False

    if not deps_ok:
        sys.exit(1)

    screenshots = capture_slides(input_html)

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
