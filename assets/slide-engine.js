/**
 * Slide Engine - Fluid Intelligence PPT Navigation System
 * Full-screen 16:9 presentation navigation with keyboard, scroll, touch, and nav dots.
 *
 * CSS section: Include in <style> block of the HTML document.
 * JS section:  Include in <script> block at end of <body>.
 */

/* ============================================================
   CSS SECTION - Copy this into your <style> block
   ============================================================ */
const SLIDE_ENGINE_CSS = `
/* ---- Reset & Base ---- */
html, body {
  margin: 0; padding: 0;
  width: 100%; height: 100%;
  overflow: hidden;
  font-family: 'Noto Sans SC', 'Inter', sans-serif;
  background: #000;
}

/* ---- Slides Container ---- */
.slides-container {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  position: relative;
  background: #faf8ff;
}

/* ---- Individual Slide ---- */
.slide {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100vw;
  height: 100vh;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: transform;
}
.slide.active   { transform: translateY(0); }
.slide.above    { transform: translateY(-100vh); }
.slide.below    { transform: translateY(100vh); }

/* ---- Navigation Dots ---- */
.nav-dots {
  position: fixed;
  right: 24px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 12px;
  z-index: 1000;
}
.nav-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(0, 82, 217, 0.25);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}
.nav-dot:hover {
  background: rgba(0, 82, 217, 0.5);
  transform: scale(1.3);
}
.nav-dot.active {
  background: #0052D9;
  border-color: rgba(255,255,255,0.8);
  box-shadow: 0 0 8px rgba(0, 82, 217, 0.4);
}

/* ---- Slide Counter ---- */
.slide-counter {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255,255,255,0.8);
  backdrop-filter: blur(8px);
  border-radius: 20px;
  padding: 6px 20px;
  font-size: 13px;
  color: #0052D9;
  font-weight: 600;
  z-index: 1000;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  letter-spacing: 0.05em;
}

/* ---- Instruction Hint (fades out) ---- */
.instruction-hint {
  position: fixed;
  bottom: 60px;
  left: 50%;
  transform: translateX(-50%);
  color: rgba(0,82,217,0.5);
  font-size: 13px;
  z-index: 1000;
  pointer-events: none;
  transition: opacity 0.8s ease;
}
.instruction-hint.fade { opacity: 0; }

/* ---- Keyboard shortcut overlay (optional) ---- */
.shortcut-bar {
  position: fixed;
  top: 16px;
  right: 24px;
  display: flex;
  gap: 8px;
  z-index: 1000;
  opacity: 0.4;
}
.shortcut-key {
  background: rgba(255,255,255,0.8);
  backdrop-filter: blur(4px);
  border-radius: 6px;
  padding: 4px 10px;
  font-size: 11px;
  color: #0052D9;
  font-weight: 600;
  border: 1px solid rgba(0,82,217,0.15);
}
`;

/* ============================================================
   JS SECTION - Copy this into your <script> block
   ============================================================ */
const SLIDE_ENGINE_JS = `
(function() {
  'use strict';

  let currentSlide = 0;
  const slides = document.querySelectorAll('.slide');
  const totalSlides = slides.length;
  let isTransitioning = false;

  // ---- Show all slides reference ----
  console.log('Slide Engine initialized: ' + totalSlides + ' slides ready');

  // ---- Build nav dots ----
  const navDotsContainer = document.querySelector('.nav-dots');
  if (navDotsContainer && totalSlides > 1) {
    slides.forEach((_, i) => {
      const dot = document.createElement('div');
      dot.className = 'nav-dot' + (i === 0 ? ' active' : '');
      dot.addEventListener('click', () => goToSlide(i));
      navDotsContainer.appendChild(dot);
    });
  }

  // ---- Go to specific slide ----
  function goToSlide(index) {
    if (isTransitioning || index === currentSlide) return;
    if (index < 0 || index >= totalSlides) return;

    isTransitioning = true;
    const direction = index > currentSlide ? 'down' : 'up';

    // Update slide positions
    slides.forEach((slide, i) => {
      slide.classList.remove('active', 'above', 'below');
      if (i === index) {
        slide.classList.add('active');
      } else if (i < index) {
        slide.classList.add('above');
      } else {
        slide.classList.add('below');
      }
    });

    // Update nav dots
    const dots = document.querySelectorAll('.nav-dot');
    dots.forEach((d, i) => d.classList.toggle('active', i === index));

    // Update counter
    const counter = document.querySelector('.slide-counter');
    if (counter) {
      counter.textContent = (index + 1) + ' / ' + totalSlides;
    }

    currentSlide = index;

    // Fade instruction hint
    const hint = document.querySelector('.instruction-hint');
    if (hint) hint.classList.add('fade');

    setTimeout(() => { isTransitioning = false; }, 650);
  }

  // ---- Next / Previous ----
  function nextSlide() { goToSlide(currentSlide + 1); }
  function prevSlide() { goToSlide(currentSlide - 1); }

  // ---- Keyboard Navigation ----
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {
      e.preventDefault();
      nextSlide();
    } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft' || e.key === 'PageUp') {
      e.preventDefault();
      prevSlide();
    } else if (e.key === 'Home') {
      e.preventDefault();
      goToSlide(0);
    } else if (e.key === 'End') {
      e.preventDefault();
      goToSlide(totalSlides - 1);
    }
  });

  // ---- Mouse Wheel ----
  let wheelTimeout;
  document.addEventListener('wheel', (e) => {
    e.preventDefault();
    if (wheelTimeout) return;
    wheelTimeout = setTimeout(() => { wheelTimeout = null; }, 800);

    if (e.deltaY > 20) {
      nextSlide();
    } else if (e.deltaY < -20) {
      prevSlide();
    }
  }, { passive: false });

  // ---- Touch Swipe ----
  let touchStartY = 0;
  document.addEventListener('touchstart', (e) => {
    touchStartY = e.touches[0].clientY;
  }, { passive: true });

  document.addEventListener('touchend', (e) => {
    const deltaY = e.changedTouches[0].clientY - touchStartY;
    if (Math.abs(deltaY) > 50) {
      if (deltaY > 0) {
        prevSlide();
      } else {
        nextSlide();
      }
    }
  });

  // ---- Click navigation (top/bottom zones on ending/cover slides) ----
  document.addEventListener('click', (e) => {
    const rect = document.body.getBoundingClientRect();
    const clickY = e.clientY;
    const threshold = rect.height * 0.15;

    // Only trigger zone click if not clicking on interactive elements
    const tag = e.target.tagName.toLowerCase();
    if (tag === 'a' || tag === 'button' || tag === 'input' || e.target.closest('.nav-dot')) return;

    if (clickY < threshold) {
      prevSlide();
    } else if (clickY > rect.height - threshold) {
      nextSlide();
    }
  });

})();
`;

// Export for Node.js usage
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { SLIDE_ENGINE_CSS, SLIDE_ENGINE_JS };
}
