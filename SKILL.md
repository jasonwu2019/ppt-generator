---
name: ppt-generator
version: "3.16"
description: "HTML-based presentation slide generator using the Fluid Intelligence design system — glassmorphism, Electric Blue, immersive 16:9 with 12 content templates (Layout A-L). Generates full-screen HTML slides with keyboard/scroll navigation and pixel-perfect PPTX/PDF export via Playwright 16:9 FHD viewport. v3.16 optimizes export: headless Chromium viewport = true full-screen canvas (no browser chrome), waits for Tailwind + fonts to fully load before capturing."
agent_created: true
---

# PPT Generator Skill

Generate beautiful HTML-based presentation slides using the **Fluid Intelligence** design system,
with full-screen 16:9 display, keyboard/scroll navigation, and optional PPTX export.

## When to Use

Trigger this skill when the user says any of:
- "帮我生成一个关于 [主题] 的PPT"
- "做一个 [主题] 的演示文稿"
- "Generate a presentation about [topic]"
- "Create slides for [topic]"
- "制作 [主题] 幻灯片"
- Any request involving PPT/presentation/slides/幻灯片/演示文稿 generation

## Design System Overview

The Fluid Intelligence design system defines the visual language:

| Element | Specification |
|---------|--------------|
| **Primary Color** | Electric Blue `#0052D9` / `#0050cb` |
| **Surface** | `#faf8ff` (soft off-white) |
| **On-Surface** | `#131b2e` (deep slate) |
| **Glass Panels** | White 60-80% opacity + `backdrop-filter: blur(20-32px)` |
| **Aspect Ratio** | 16:9 (viewport-fit container) |
| **Layout Grid** | 12-column fluid grid, 8px base spacing unit |
| **Headline Font** | Hanken Grotesk or Noto Sans SC |
| **Body Font** | Inter or Noto Sans SC |
| **Label Font** | Geist |
| **Border Radius** | Default 0.5rem (8px), cards 1rem (16px) |

**Color Palette (Tailwind config):**
- `tencent-blue`: `#0052d9`
- `product-orange`: `#f37142`
- `business-blue`: `#308eef`
- `strategy-green`: `#2ba471`

Full design system details are in `references/design_system.md`. Load it when detailed specs are needed.

## Page Templates

Ten template types are available in `assets/templates/`:

| Template | File | Purpose |
|----------|------|---------|
| Cover | `cover.html` | Title slide with diagonal blue overlay + background image + hero image area (built-in SVG fallback) |
| TOC | `toc.html` | Table of contents with glassmorphism left panel + numbered list |
| Content (Text/Cards) | `content.html` | Multi-section content: 3-card grid, numbered list, 2x2 icon grid |
| Content (Text Grid) | `content-text-grid.html` | **CANONICAL** 4x2 glass card grid with icons — use for all text+icon card grids |
| Content (Text Industry) | `content-text-industry.html` | **v3.13** 4x2 industry/sector showcase grid — 8 gradient-icon glass cards for 行业应用/业务场景/产品能力 |
| Content (Text Intro) | `content-text-intro.html` | **v3.13** Product intro/positioning page — hero header + 3 positioning cards + split bottom (numbered list + 2x2 grid) |
| Content (Table) | `content-table.html` | Data table with glass container, primary header, hover rows |
| Content (Case Study) | `content-case.html` | Scenario case study: pain points, solution flow, business metrics |
| Content (Timeline) | `content-timeline.html` | Horizontal timeline with alternating milestone cards |
| Ending | `ending.html` | Thank-you slide with solid blue background |

Each template uses `{{PLACEHOLDER}}` markers for dynamic content. See each template file for
specific placeholders and their meanings.

## Workflow

Follow this ordered workflow when generating a PPT.

### Step 1: Understand the Request

Parse the user's request to determine:
- **Topic**: What is the presentation about?
- **Audience**: Who is it for? (if mentioned)
- **Format**: HTML only, or also PPTX export?
- **Content Provided?**: Did the user provide specific content (bullet points, text, outline),
  or only a topic name?

If the user provided an outline or bullet points, use them directly. Skip to Step 3 (planning).

### Step 2: Content Generation (when no content provided)

If the user only gave a topic name without specific content:

1. **Search the web** using WebSearch with the topic as query. Use Chinese and English keywords
   for better coverage. Search for:
   - Overview/introduction of the topic
   - Key concepts, features, or components
   - Latest developments or trends
   - Statistics or data points
   - Common use cases or applications

2. **Summarize findings** into a structured outline:
   - 1 cover slide: Title + subtitle + right-side hero image (fixed: 科技城市场景)
   - 1 TOC slide: 4-10 key sections
   - 3-N content slides: One per TOC section, with bullet points, cards, or data
   - 1 ending slide: Thank you / Q&A

3. **Verify completeness**: Ensure every TOC item has a corresponding content slide.

### Step 3: Plan Slide Structure

Create a slide-by-slide plan using only Fluid Intelligence templates:

```
Slide 1: Cover
  - Title: [title]
  - Subtitle: [subtitle]
  - Footer: [organization/author]
  - Cover Image: [if topic is visual, generate; otherwise omit]
  - Background: [if BG_IMAGE_URL is empty, fallback gradient auto-applied]

Slide 2: Table of Contents
  - Section title: [e.g., "目录" or custom]
  - Items: [numbered list of 4-10 items]

Slide 3-N: Content slides
  For each content slide, decide layout type:
  - "cards": 3-column glassmorphism cards with gradient headers (good for advantages, features, comparisons)
  - "list": Numbered list with icon circles (good for steps, key points, bullet content)
  - "grid": 4x2 or 3x2 grid of items with icons (good for categories, industries, product matrix, text+icon cards) → uses `content-text-grid.html`
  - "mixed": Left text + right 2x2 grid (good for overview + product forms)
  - "table": Data table with glass container + highlighted rows (good for scenario comparisons, specs)
  - "case": Case study: pain points → solution flow → business metrics (good for success stories, solutions)
  - "timeline": Horizontal milestone timeline with alternating up/down nodes (good for roadmap, history)
  - "growth": SVG growth curve with animated trend line + positioned milestones (good for growth story, evolution)
  - "architecture": Multi-tier layered architecture with vertical labels (good for product matrix, tech stack)
  - "expert": Center hub + surrounding character nodes with profile cards (good for team intro, expert network)

  **MANDATORY**: Every content slide plan entry MUST include template file annotation:
  ```
  Slide 4: [Title]
    Layout: cards (Layout A, file: content.html)
    Content: [bullet points]
  Slide 5: [Title]
    Layout: case (Layout F, file: content-case.html)
    Content: [case details]
  Slide 6: [Title]
    Layout: timeline (Layout G, file: content-timeline.html)
    Content: [milestone items]
  ```

Slide N+1: Ending
  - Main text: [e.g., "感谢倾听" or custom]
```

### Step 4: Generate HTML

Create a single self-contained HTML file that includes all slides.

**BEFORE generating any content slide HTML, complete this pre-check:**

1. **Read the plan from Step 3** — identify which layout was assigned to each slide
2. **Load the correct template file** for each unique layout used:
   - Layout A/B/C → read `assets/templates/content.html`
   - Layout D → read `assets/templates/content-text-grid.html`
   - Layout E → read `assets/templates/content-table.html`
   - Layout F → read `assets/templates/content-case.html`
   - Layout G → read `assets/templates/content-timeline.html`
   - Layout H/I/J → read `assets/templates/content.html` (use Layout reference patterns)
   - Layout K → read `assets/templates/content-text-industry.html`
   - Layout L → read `assets/templates/content-text-intro.html`
3. **Apply the layout-specific CSS and HTML patterns** from the Layout Reference section below
4. **NEVER** generate a content slide from scratch — always use the layout's canonical structure

**Assembly rules:**
1. Read `assets/slide-engine.js` for the navigation system CSS and JS.
2. Read templates from `assets/templates/` as needed.
3. Combine all slides into one HTML document:
   ```html
   <!DOCTYPE html>
   <html lang="zh-CN">
   <head>
     <meta charset="utf-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title>[Presentation Title]</title>
     <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
     <!-- Tailwind config from design system -->
     <!-- Slide engine CSS (from assets/slide-engine.js, CSS section) -->
   </head>
   <body>
     <div class="slides-container">
       <!-- All slide <section> elements -->
     </div>
     <!-- Navigation indicators -->
     <!-- Slide engine JS (from assets/slide-engine.js, JS section) -->
   </body>
   </html>
   ```

4. **Each slide** must be wrapped in a `<section class="slide">` element with 16:9 container.
5. Replace all `{{PLACEHOLDER}}` markers with actual content.
6. Apply design system colors and typography consistently across all slides.

**Template assembly:**
- Use: `cover.html`, `toc.html`, `content.html` (Layout A/B/C/D H/I/J), `content-text-grid.html` (D), `content-text-industry.html` (K), `content-text-intro.html` (L), `content-table.html` (E), `content-case.html` (F), `content-timeline.html` (G), `ending.html`
- Include all glassmorphism CSS, Google Fonts, and Material Symbols
- Cover image generation applies (see Cover Image Generation section)

**Content page template usage (MANDATORY — every content slide MUST match a layout):**

Before generating ANY content slide HTML, classify the page content type and explicitly select the correct layout. This is NOT optional — failure results in broken layouts.

| Content Type | Layout | Template File | Key Visual Pattern |
|-------------|--------|---------------|-------------------|
| Advantages, features, value props | **Layout A (Cards)** | `content.html` | 3-column gradient header cards with icon + description |
| Steps, key points, bullet content | **Layout B (List)** | `content.html` | Numbered circles (`bg-product-orange`) + flex items-start |
| Overview + detail split | **Layout C (Mixed)** | `content.html` | 12-col grid: left col-span-7 text + right col-span-5 2x2 grid |
| Industries, categories, product matrix, text+icon grids | **Layout D (Grid)** | `content-text-grid.html` | 4x2 or 3x2 icon-driven grid with glass cards, `industry-icon-bg` gradient circles, header gradient text |
| Comparisons, specs, scenario data | **Layout E (Table)** | `content-table.html` | `glass-container` table, primary header, hover rows |
| Success stories, solution demos | **Layout F (Case)** | `content-case.html` | 3-zone: pain points → solution flow → business metrics |
| Roadmap, milestones, history | **Layout G (Timeline)** | `content-timeline.html` | Horizontal line, alternating up/down nodes, dot+connect-line |
| Growth story, evolution, trend | **Layout H (Growth)** | `content.html` | SVG growth curve + absolute-positioned milestones |
| Product matrix, tech stack, hierarchy | **Layout I (Architecture)** | `content.html` | Layered tiers, vertical-text labels, color-coded blocks |
| Team intro, expert network | **Layout J (Expert)** | `content.html` | Center hub + radiating profile cards + bottom metrics |
| Industry showcase, sector comparison, business scenarios (8 items) | **Layout K (Industry Grid)** | `content-text-industry.html` | 4x2 glass card grid, gradient icon circles side-by-side with titles + descriptions |
| Product intro, positioning page, value proposition overview | **Layout L (Product Intro)** | `content-text-intro.html` | Hero header + 3 positioning cards (colored left borders) + split bottom: numbered list + 2x2 form grid |

**For headers on ALL layouts**: use parallelogram blue accent bar + page title pattern.

**Enforcement rules**:
- Each content slide in Step 3 plan MUST include `Layout: X (file: Y.html)` annotation
- When generating HTML in Step 4, read the template file specified for that layout
- NEVER default all content slides to `content.html` or any single template
- If a content type doesn't clearly match any layout, default to Layout B (List) — safest fallback

**Content density rules** (CRITICAL — prevents layout overflow):
- Each content slide max 4 items (cards, list items, grid cells)
- Each list item text max 2 lines (~60 Chinese characters)
- Reduce padding from `p-10 lg:p-16` to `p-8 lg:p-12` when content is dense
- Always add `overflow-hidden` and `flex-shrink-0` on headers, `min-h-0` on scrollable areas
- Numbered list items MUST use `flex items-start` (NOT `items-center`) to handle multiline text

**CSS calc() spacing rule** (CRITICAL — per CSS spec §8.1.1):
- `calc()` expressions MUST have whitespace on both sides of `+` and `-` operators
- ❌ WRONG: `calc(6rem+110px)`, `calc(50%-10px)`, `calc(50%+3px)`
- ✅ RIGHT: `calc(6rem + 110px)`, `calc(50% - 10px)`, `calc(50% + 3px)`
- Without whitespace, browsers reject the value as invalid, causing layout breakage (elements collapse to zero size)
- This applies to ALL inline styles, attributes, and CSS blocks — no exceptions

**Required fonts** (include in `<head>`):
```html
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700;800&family=Inter:wght@400;500&family=Geist:wght@400;500;600&family=Noto+Sans+SC:wght@300;400;500;700&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
```

When using **Layout E (Table)**, also include:
```css
.bg-mesh{background-color:#faf8ff;background-image:radial-gradient(at 0% 0%,rgba(0,80,203,.05) 0px,transparent 50%),radial-gradient(at 100% 0%,rgba(0,204,249,.08) 0px,transparent 50%),radial-gradient(at 50% 100%,rgba(67,69,209,.05) 0px,transparent 50%)}
.parallelogram{clip-path:polygon(25% 0%,100% 0%,75% 100%,0% 100%)}
.glass-container{background:rgba(255,255,255,.7);backdrop-filter:blur(32px);border:1px solid rgba(255,255,255,.3)}
```
Additional CSS for Layout F/G — see each template's Layout reference section for required styles.

**Critical CSS rules for the container:**
```css
.slides-container { width: 100vw; height: 100vh; overflow: hidden; position: relative; }
.slide { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
         transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1); }
.slide.active { transform: translateY(0); }
.slide.above { transform: translateY(-100vh); }
.slide.below { transform: translateY(100vh); }
```

## Cover & TOC Images

封面右侧和TOC左侧始终使用默认图片，不进行 AI 图片生成。

在 Step 4 生成 HTML 之前：
1. 将 `assets/cover-default-hero.jpg`（科技城市场景）复制到 workspace
2. 封面：`{{COVER_IMAGE_URL}}` 设为复制后的图片文件名，`{{COVER_IMAGE_ALT}}` 设为 "科技城市场景"
3. TOC：`{{DECORATION_IMG_URL}}` 也设为同一个图片文件名，`onerror` fallback 保持不变

### Step 5: Deliver the HTML

1. **Save** the generated HTML to the workspace as `[topic]-presentation.html`
2. **Preview** using `preview_url` with the absolute file path
3. Tell the user: arrow keys or scroll to navigate, or click the nav dots

### Step 6: PPTX / PDF Export (only if user requests .pptx or .pdf)

**Architecture (v3.16)**: Playwright 16:9 FHD viewport screenshot export. Opens the HTML in headless Chromium at 1920×1080 (16:9 Full HD), waits for Tailwind CSS CDN + all Google Fonts to fully load (`document.fonts.ready`), then captures each `<section class="slide">` as a retina-quality (3840×2160) viewport screenshot. **Headless Chromium has NO browser chrome** — no title bar, no tabs, no address bar, no OS window decorations. The 1920×1080 viewport IS the entire visible area, identical to pressing F11 in a real browser at 1920×1080 resolution. This guarantees the exported PPTX/PDF is **pixel-identical** to the browser full-screen view.

**Prerequisites** (install once per environment):

1. Ensure `playwright` + `python-pptx` + `Pillow` are installed:
   ```bash
   "C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/pip.exe" install playwright python-pptx Pillow
   "C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe" -m playwright install chromium
   ```
   If already installed, skip this step.

2. Run the export script:
   ```bash
   "C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe" "<SKILL_DIR>/scripts/export_pptx.py" "<generated_html>" "<output>"
   ```
   - `<output>` extension determines format: `.pptx` → PowerPoint, `.pdf` → PDF

3. Deliver the file to the user via `deliver_attachments`.

**How it works**:
- Launches headless Chromium — NO browser chrome = viewport is the full visible canvas
- Viewport = 1920×1080 (16:9 FHD) — the standard presentation full-screen resolution
- Waits for `document.fonts.ready` to ensure all Google Fonts are rendered
- Extra 2s buffer for Tailwind CDN to finish compiling all utility classes
- Cycles through slides via JS (sets `.active` class, others `.above`/`.below`)
- `full_page=False` captures the 1920×1080 viewport — this IS the full-screen view (each slide fills 100vh/100vw)
- Screenshots at @2x retina → 3840×2160 PNG per slide
- PPTX: 16:9 (13.333"×7.5"), each slide = one screenshot filling the entire slide
- PDF: multi-page, each page = one screenshot, 150dpi

## Content Page Layouts Reference

Based on Fluid Intelligence design system, 10 content page layouts. Each layout is based on verified HTML template patterns.

### Layout A: 优势卡片 (3-Column Cards — for advantages, features, comparisons)

Three-column side-by-side cards, each containing: icon circle + title + glass-card (gradient blue header + white content area + bottom English decorative text).

```html
<section class="slide">
  <main class="presentation-canvas relative z-10 flex flex-col px-margin-desktop py-12">
    <header class="flex justify-between items-center w-full mb-16">
      <div class="flex items-center gap-4">
        <div class="w-10 h-10 bg-primary-container parallelogram"></div>
        <h1 class="font-headline-lg text-headline-lg italic text-gradient">优势分析</h1>
      </div>
      <img src="{{LOGO_URL}}" class="h-10" alt="logo"/>
    </header>
    <div class="grid grid-cols-3 gap-12 flex-grow items-start px-8">
      <!-- Each column: icon circle + title + glass-card(gradient header + white content + English sub) -->
    </div>
  </main>
</section>
```

**Card structure per column**:
```html
<div class="flex flex-col items-center group">
  <div class="mb-8 p-6 bg-surface-container-low rounded-full border border-primary/10">
    <span class="material-symbols-outlined text-[64px] text-primary">icon_name</span>
  </div>
  <h2 class="font-headline-md text-headline-md mb-8">优势标题</h2>
  <div class="w-full flex flex-col rounded-xl overflow-hidden glass-card">
    <div class="card-header-gradient py-4 px-6 text-center">
      <h3 class="font-headline-md text-white text-lg">子标题</h3>
    </div>
    <div class="bg-white p-8 flex flex-col justify-between min-h-[160px]">
      <p class="font-body-md text-on-surface-variant text-center">描述内容</p>
    </div>
  </div>
</div>
```

**Key CSS**:
```css
.glass-card { background: rgba(255,255,255,0.7); backdrop-filter: blur(32px);
              border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 4px 30px rgba(0,0,0,0.05); }
.card-header-gradient { background: linear-gradient(180deg, #0066ff 0%, #0050cb 100%); }
```

### Layout B: 编号列表 (Numbered List — for steps, key points, bullet content)

Numbered circles + text vertical list, each entry with colored number circle.

```html
<!-- "核心3句话" pattern -->
<div class="space-y-4">
  <div class="flex items-center bg-white/60 p-4 rounded-xl border border-slate-100 shadow-sm">
    <div class="w-10 h-10 rounded-full bg-product-orange text-white flex items-center justify-center font-bold text-xl mr-6 shrink-0">1</div>
    <p class="text-xl text-slate-700 font-medium">Content text, key info with <span class="text-tencent-blue font-bold italic">highlight</span></p>
  </div>
  <!-- Max 4 items -->
</div>
```

**Rules**: Each item max 2 lines (~60 chars), use `flex items-start` (NOT `items-center`) for multiline.

### Layout C: 左右分栏 (Two-Column — for overview + detail)

Left text list + right 2x2 icon grid, clear visual contrast.

```html
<section class="grid grid-cols-12 gap-12 flex-grow">
  <div class="col-span-7 flex flex-col">
    <h4 class="text-2xl font-bold mb-6">核心要点</h4>
    <div class="space-y-4"><!-- Layout B numbered list --></div>
  </div>
  <div class="col-span-5 flex flex-col">
    <h4 class="text-2xl font-bold mb-6">产品形态</h4>
    <div class="grid grid-cols-2 gap-4 flex-grow">
      <!-- 4 icon+label cards -->
    </div>
  </div>
</section>
```

### Layout D: 内容条目网格 (Item Grid — for categories, industries, product matrix, text+icon pages)

**CANONICAL template**: `assets/templates/content-text-grid.html` — this is the authoritative source for ALL text+icon grid slides. The template provides a 4x2 glass card grid with header (parallelogram icon + gradient title + logo) and footer.

Card structure per item (use inside `{{GRID_ITEMS}}`):
```html
<article class="glass-card rounded-xl p-6 flex flex-col">
  <div class="flex items-center gap-4 mb-4">
    <div class="industry-icon-bg w-14 h-14 rounded-full flex items-center justify-center shadow-lg shadow-primary/20 shrink-0">
      <span class="material-symbols-outlined text-white text-3xl">ICON_NAME</span>
    </div>
    <h2 class="font-headline-md text-headline-md text-on-surface">ITEM_TITLE</h2>
  </div>
  <p class="font-body-md text-body-md text-on-surface-variant leading-relaxed">ITEM_DESC</p>
</article>
```

Grid sizing rules:
- 8 items: `grid-cols-4 grid-rows-2`
- 6 items: `grid-cols-3 grid-rows-2`
- 4 items: `grid-cols-2 grid-rows-2`
- 3 items: `grid-cols-3 grid-rows-1`
- 2 items: `grid-cols-2 grid-rows-1`

**Key CSS** (must be included in main `<style>`):
```css
.glass-card { background: rgba(255,255,255,.65); backdrop-filter: blur(24px);
              border: 1px solid rgba(255,255,255,.4);
              transition: all .3s cubic-bezier(.4,0,.2,1); }
.glass-card:hover { background: rgba(255,255,255,.85); transform: translateY(-4px);
                    box-shadow: 0 12px 32px -8px rgba(0,80,203,.12); }
.industry-icon-bg { background: linear-gradient(135deg, #0066ff 0%, #0040a4 100%); }
.header-gradient-text { background: linear-gradient(90deg, #0050cb 0%, #00ccf9 100%);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.aspect-16-9 { aspect-ratio: 16/9; max-height: 100vh; width: 100%; }
```

### Layout E: 数据表格 (Data Table — for comparisons, specs, scenario data)

Glass-container-wrapped table, primary header, hover row highlight.

```html
<div class="w-full glass-container rounded-xl overflow-hidden shadow-sm">
  <table class="w-full text-left border-collapse">
    <thead>
      <tr class="bg-primary text-on-primary">
        <th class="py-4 px-6 font-headline text-body-lg font-semibold">Col1</th>
        <th class="py-4 px-6 font-headline text-body-lg font-semibold">Col2</th>
        <th class="py-4 px-6 font-headline text-body-lg font-semibold">Col3</th>
        <th class="py-4 px-6 font-headline text-body-lg font-semibold">Col4</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-outline-variant/20">
      <tr class="hover:bg-primary/5 transition-colors">
        <td class="py-3 px-6 font-semibold text-primary">Industry Name</td>
        <td class="py-3 px-6 text-body-md text-on-surface-variant">Scene Description</td>
        <td class="py-3 px-6 text-body-md text-on-surface-variant">Core Value</td>
        <td class="py-3 px-6 text-body-md font-bold text-primary italic">Efficiency Data</td>
      </tr>
      <!-- 5-10 rows -->
    </tbody>
  </table>
</div>
```

**Key CSS**:
```css
.bg-mesh { background: radial-gradient(at 0% 0%, rgba(0,80,203,.05) 0px, transparent 50%),
                   radial-gradient(at 100% 0%, rgba(0,204,249,.08) 0px, transparent 50%); }
.glass-container { background: rgba(255,255,255,0.7); backdrop-filter: blur(32px);
                   border: 1px solid rgba(255,255,255,0.3); }
```

Table row hover micro-animation: `transform: translateX(8px)`.

### Layout F: 场景案例 (Case Study — for success stories, solutions)

Three-zone layout: top (3 demand source icons + 2 pain point cards), middle (solution flow: Source → WorkBuddy → Knowledge Base), right (2 business metrics).

```html
<!-- Top: Demand + Pain Points -->
<div class="grid grid-cols-12 gap-6 mb-6 h-[22%]">
  <section class="col-span-4 glass-card rounded-xl p-4 section-accent-left">
    <!-- 3 icon+label source cards -->
  </section>
  <section class="col-span-8 glass-card rounded-xl p-4 section-accent-orange">
    <!-- 2 pain point cards: circle icon + title + description -->
  </section>
</div>
<!-- Middle: Solution Flow + Business Metrics -->
<div class="grid grid-cols-12 gap-6 flex-grow">
  <section class="col-span-8 glass-card rounded-xl p-6 section-accent-left">
    <!-- 3-node flow: WeCom → WorkBuddy → Knowledge Base -->
  </section>
  <section class="col-span-4 glass-card rounded-xl p-6 section-accent-green">
    <!-- 2 metric cards: x2, -50% -->
  </section>
</div>
```

**Key CSS**:
```css
.section-accent-left { border-left: 4px solid #0066ff; }
.section-accent-orange { border-left: 4px solid #ff6b35; }
.section-accent-green { border-left: 4px solid #34a853; }
```

### Layout G: 水平路线图 (Horizontal Timeline — for roadmap, history, milestones)

Horizontal timeline with alternating up/down nodes, connected by dots and connect-lines.

```html
<main class="flex-grow flex items-center relative w-full px-12">
  <div class="timeline-line"></div>
  <div class="flex justify-between w-full relative z-10">
    <!-- Upper node -->
    <div class="relative flex flex-col items-center">
      <div class="absolute bottom-12 w-64 mb-8">
        <h3 class="font-headline-md text-headline-md text-primary">Year</h3>
        <p class="font-body-md text-on-surface-variant">Description</p>
      </div>
      <div class="connect-line-top"></div>
      <div class="dot"></div>
    </div>
    <!-- spacer dots -->
    <!-- Lower node -->
    <div class="relative flex flex-col items-center">
      <div class="dot"></div>
      <div class="connect-line-bottom"></div>
      <div class="absolute top-12 w-64 mt-8">
        <h3 class="font-headline-md text-headline-md text-primary">Year</h3>
        <p class="font-body-md text-on-surface-variant">Description</p>
      </div>
    </div>
  </div>
</main>
```

**Key CSS**:
```css
.timeline-line { height: 1px; background: #00ccf9; width: 100%; position: absolute; top: 50%; }
.dot { width: 24px; height: 24px; background: #0050cb; border-radius: 50%; z-index: 10; }
.connect-line-top { width: 1px; height: 120px; background: #00ccf9; position: absolute; bottom: 24px; left: 50%; }
.connect-line-bottom { width: 1px; height: 120px; background: #00ccf9; position: absolute; top: 24px; left: 50%; }
```

**Rules**: Nodes alternate up/down, first node on top, insert spacer dots between every 2-3 nodes. Max 8-10 milestones per page.

**CRITICAL — Timeline connector + marker positioning (v3.12 fix)**:

The connector MUST dynamically stretch from card to marker using `top` + `bottom` dual-anchor (NOT fixed `h-*`). Fixed heights (h-20/h-24) cannot reach the marker at container 50% on most viewports, leaving visible gaps. The marker MUST also be offset 3px toward its card (NOT all identically on center at `top:50%`).

**UP = card ABOVE the line (marker offset below line toward card, connector stretches DOWN):**
```html
<div class="absolute left-[8%] top-0 bottom-0 w-0">
  <div class="milestone-marker" style="top:calc(50% + 3px);"></div>
  <!-- dual-anchor stretch: from just below card to just above marker -->
  <div class="connector-line" style="left:0; top:calc(6rem + 110px); bottom:calc(50% - 10px); background:linear-gradient(180deg,#0050cb,#00ccf9);"></div>
  <div class="info-card top-24" style="left:0">
    ...content...
  </div>
</div>
```

**DOWN = card BELOW the line (marker offset above line toward card, connector stretches UP):**
```html
<div class="absolute left-[34%] top-0 bottom-0 w-0">
  <div class="milestone-marker" style="top:calc(50% - 3px);"></div>
  <!-- dual-anchor stretch: from just above card to just below marker -->
  <!-- gradient 0deg = dark at card (bottom) → light at marker (top) -->
  <div class="connector-line" style="left:0; bottom:calc(6rem + 110px); top:calc(50% + 10px); background:linear-gradient(0deg,#0050cb,#00ccf9);"></div>
  <div class="info-card bottom-24" style="left:0">
    ...content...
  </div>
</div>
```

**Why v3.11**: v3.8 fixed UP/DOWN swap. v3.10 fixed DOWN gradient direction. But both used fixed `h-20`/`h-24` heights that only reach ~80-96px from the card — typical gap from card to marker is ~120-180px on 1080p. Result: connector visually "floats" near card, never reaching the marker. Dual-anchor `top`+`bottom` eliminates the gap entirely. The 3px marker offset visually distinguishes card ownership.

**Why v3.12 (calc-spacing)**: ALL `calc()` expressions MUST have whitespace on both sides of `+` and `-` operators per CSS spec. `calc(6rem+110px)` is INVALID — browsers reject it and fall back to `auto`, causing connectors to have zero height. Always use `calc(6rem + 110px)`, `calc(50% - 10px)`, `calc(50% + 3px)`.

### Layout H: 增长曲线 (Growth Timeline — for growth stories, evolution, trend)

SVG trend line + absolute-positioned milestone nodes for growth visualization.

```html
<main class="flex-grow relative px-margin-desktop">
  <svg class="absolute inset-0 w-full h-full pointer-events-none" viewBox="0 0 1600 800">
    <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#0066ff"/>
      <stop offset="100%" stop-color="#00ccf9"/>
    </linearGradient>
    <path class="timeline-path" d="M 50,600 L ... L 1500,100" fill="none"
          stroke="url(#lineGrad)" stroke-width="4" stroke-linecap="round"/>
  </svg>
  <div class="absolute inset-0 w-full h-full">
    <!-- Absolute-positioned milestones: date + description + dot -->
    <div class="absolute" style="left: 5%; top: 58%;">
      <span class="text-primary mb-1">1998.11</span>
      <p class="font-semibold">Milestone Event</p>
      <div class="w-3 h-3 bg-primary rounded-full milestone-node"></div>
    </div>
    <!-- 8-12 milestones along SVG path -->
  </div>
</main>
```

**Key CSS**: milestone-node hover scale (`transform: scale(1.4)`), SVG path animation (`stroke-dasharray/dashoffset`).

### Layout I: 架构图 (Architecture — for product matrix, tech stack, layered structure)

Layered architecture display, left vertical labels + right multi-level color-coded blocks.

```html
<main class="flex-1 flex gap-2 px-8 pb-8 min-h-0">
  <div class="w-12 flex flex-col gap-2 shrink-0">
    <div class="flex-1 bg-blue-50 border border-blue-200 rounded flex items-center justify-center">
      <span class="vertical-text text-primary font-bold text-sm">Solutions</span>
    </div>
    <div class="h-[45%] bg-blue-50 border border-blue-200 rounded flex items-center justify-center">
      <span class="vertical-text text-primary font-bold text-sm">Products</span>
    </div>
  </div>
  <div class="flex-1 flex flex-col gap-3 min-h-0">
    <!-- Each layer: colored header + sub-item grid -->
    <div class="flex-1 border-2 border-tier-solutions flex flex-col rounded-sm overflow-hidden">
      <div class="bg-tier-solutions text-white text-center py-1.5 text-lg font-bold">Layer Name</div>
      <div class="flex-1 grid grid-cols-3 divide-x bg-white p-4"><!-- Sub-items --></div>
    </div>
  </div>
</main>
```

**Color variables** (use exact tailwind classes):
- 2 tiers: tier-solutions `#00b5d1` (cyan), tier-platform `#0066ff` (blue)
- 3 tiers: add tier-infra `#0052cc` (indigo)
- 4 tiers: add tier-data `#7c3aed` (violet)
- 5 tiers: add tier-deploy `#64748b` (slate)

**Tier sizing by layer count**:
| Layers | Sizing formula | Example |
|--------|---------------|---------|
| 2 | `flex-[3]` + `flex-[2]` | large top, smaller bottom |
| 3 | `flex-[2]` + `flex-[2]` + `flex-[2]` | equal 3-way split |
| 4 | `flex-[3]` + `flex-[1.5]` + `flex-[1.5]` + `flex-[1.5]` | large top + 3 small |
| 5 | `flex-[2]` + `flex-[1]` + `flex-[1]` + `flex-[1]` + `flex-[1]` | proportional, all readable |

**CRITICAL**: When using 5 layers, NEVER use `h-[20%]` — it's too cramped. Use `flex-[2]` for the primary layer and `flex-[1]` for the rest. Font size must remain >= 14px (text-sm) in all tiers.

**Layer label naming** — use descriptive Chinese labels, one of these sets:
- 业务层 / 产品层 / 平台层 / 数据层 / 基础设施层
- 表现层 / 业务逻辑层 / 数据访问层 / 服务层 / 存储层
- Or topic-specific layered names

**Key CSS**:
```css
.vertical-text { writing-mode: vertical-rl; text-orientation: mixed; }
```

### Layout J: 图文并茂 (Hub & Spokes — for team intros, expert networks, capability showcase)

Center shield icon + ring keywords + 3 left/right "avatar+text" nodes, bottom achievement showcase.

```html
<div class="flex-grow relative flex items-center justify-center">
  <!-- Center shield + dashed circle -->
  <div class="relative w-48 h-48 flex flex-col items-center justify-center z-10">
    <div class="central-circle-dashed"></div>
    <div class="bg-white rounded-full p-6 shadow-lg border border-blue-100">
      <svg><!-- Shield icon --></svg>
    </div>
    <span class="absolute -top-6 text-[11px] text-gray-500">Connect</span>
    <span class="absolute -bottom-24 text-center">
      <p class="text-2xl font-bold">3500+ Security Experts</p>
    </span>
  </div>
  <!-- Left/Right person nodes -->
  <div class="absolute left-0 w-1/3 h-full"><!-- 3 right-aligned avatar+description --></div>
  <div class="absolute right-0 w-1/3 h-full"><!-- 3 left-aligned avatar+description --></div>
</div>
<!-- Bottom achievement grid: 3 columns -->
<footer class="grid grid-cols-3 gap-0 border-t">
  <div class="pr-8 border-r"><!-- Milestone --></div>
  <div class="px-8 border-r"><!-- Awards --></div>
  <div class="pl-8"><!-- Vulnerabilities --></div>
</footer>
```

**Key CSS**: skew-banner (`transform: skewX(-20deg)`), expert-photo (`w-16 h-16 rounded-full`), central-circle-dashed (`border: 1px dashed #0066ff; border-radius: 50%`).

### Layout K: 行业网格 (Industry Grid — for sector showcase, business scenarios, 8-item category pages)

**v3.13 NEW** — Dedicated 4x2 glass card grid for industry/sector/category showcase pages. Each card features a blue-gradient circular icon + title side-by-side with description below.

```html
<main class="aspect-16-9 w-full flex flex-col px-margin-desktop py-8 relative overflow-hidden">
  <!-- Background Atmosphere -->
  <div class="absolute -top-[20%] -right-[10%] w-[60%] h-[60%] bg-primary-container/5 blur-[120px] rounded-full pointer-events-none"></div>
  <div class="absolute -bottom-[20%] -left-[10%] w-[50%] h-[50%] bg-secondary-container/5 blur-[100px] rounded-full pointer-events-none"></div>

  <header class="flex justify-between items-end w-full mb-12 z-10">
    <div class="flex items-center gap-4">
      <div class="w-12 h-12 bg-primary-container flex items-center justify-center transform -skew-x-12">
        <span class="material-symbols-outlined text-white text-3xl skew-x-12" style="font-variation-settings:'FILL' 1;">ICON</span>
      </div>
      <h1 class="font-headline-lg text-headline-lg italic header-gradient-text tracking-tight">TITLE</h1>
    </div>
  </header>

  <div class="grid grid-cols-4 grid-rows-2 gap-gutter-desktop flex-grow z-10 pb-8">
    <!-- 8 cards, each: glass-card with industry-icon-bg circle + title + description -->
    <article class="glass-card rounded-xl p-6 flex flex-col">
      <div class="flex items-center gap-4 mb-4">
        <div class="industry-icon-bg w-14 h-14 rounded-full flex items-center justify-center shadow-lg shadow-primary/20 shrink-0">
          <span class="material-symbols-outlined text-white text-3xl">ICON_NAME</span>
        </div>
        <h2 class="font-headline-md text-headline-md text-on-surface">ITEM_TITLE</h2>
      </div>
      <p class="font-body-md text-body-md text-on-surface-variant leading-relaxed">ITEM_DESC</p>
    </article>
  </div>
</main>
```

**When to use Layout K instead of Layout D (Grid)**:
- Layout K: 8 items ALWAYS (4x2 grid), bigger icon circles (w-14 h-14 gradient), icon+title in same row — better for industry/sector names with short descriptions
- Layout D: flexible item count (4/6/8), icon above title, `{{GRID_ICON}}` placeholder — better for general-purpose card grids
- For "行业应用" / "业务场景" / "解决方案" with exactly 8 items → prefer Layout K

**Key CSS**:
```css
.glass-card { background: rgba(255,255,255,.65); backdrop-filter: blur(24px);
              border: 1px solid rgba(255,255,255,.4);
              transition: all .3s cubic-bezier(.4,0,.2,1); }
.glass-card:hover { background: rgba(255,255,255,.85); transform: translateY(-4px);
                    box-shadow: 0 12px 32px -8px rgba(0,80,203,.12); }
.industry-icon-bg { background: linear-gradient(135deg, #0066ff 0%, #0040a4 100%); }
.header-gradient-text { background: linear-gradient(90deg, #0050cb 0%, #00ccf9 100%);
                        -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
```

### Layout L: 产品介绍 (Product Intro — for product positioning, value proposition pages)

**v3.13 NEW** — Hero header + 3 positioning cards (colored left borders) + split bottom (numbered list + 2x2 form grid). Best for "产品介绍" / "产品定位" / "核心价值" pages.

```html
<main class="w-full h-screen flex flex-col p-10 lg:p-16 max-w-[1920px] mx-auto">
  <!-- Hero Header -->
  <header class="flex justify-between items-start mb-12">
    <div>
      <div class="flex items-center gap-3 mb-2">
        <div class="w-4 h-10 bg-tencent-blue rounded-sm -skew-x-12"></div>
        <h1 class="text-4xl font-bold italic text-tencent-blue tracking-tight">PAGE_TITLE</h1>
      </div>
      <h2 class="text-5xl font-extrabold text-tencent-blue mt-4">SUBTITLE</h2>
    </div>
    <!-- Logo + action buttons area -->
  </header>

  <!-- 3 Positioning Cards -->
  <section class="grid grid-cols-3 gap-8 mb-16">
    <!-- Each card: glass-card, left colored border, icon, title, description -->
    <div class="relative glass-card rounded-2xl p-8 border-l-8 border-l-product-orange card-shadow">
      <div class="w-12 h-12 bg-white border rounded-lg flex items-center justify-center mb-6">
        <svg class="w-6 h-6 text-tencent-blue">...</svg>
      </div>
      <h3 class="text-2xl font-bold mb-4">产品定位</h3>
      <p class="text-lg font-medium">DESCRIPTION</p>
    </div>
  </section>

  <!-- Bottom Split: Left numbered list + Right 2x2 form grid -->
  <section class="grid grid-cols-12 gap-12 flex-grow">
    <div class="col-span-7">
      <!-- 3 numbered items: orange circle number + text -->
    </div>
    <div class="col-span-5">
      <!-- 2x2 grid: icon circle + form name -->
    </div>
  </section>
</main>
```

**When to use Layout L**:
- Product introduction / overview pages with a hero title + subtitle
- Pages needing 3 "positioning" or "value proposition" cards with colored accents
- Pages with a bottom dual-section: core highlights (numbered list) + product forms/features (icon grid)
- Distinctive visual: skewed blue decorator block on title, colored left border cards (orange/blue/green)

**Card colors**: card1=`border-l-product-orange`, card2=`border-l-business-blue`, card3=`border-l-strategy-green`

**Key CSS**:
```css
.glass-card { background: rgba(255,255,255,.7); backdrop-filter: blur(10px);
              border: 1px solid rgba(255,255,255,.3); }
.card-shadow { box-shadow: 0 10px 30px -10px rgba(0,0,0,.05); }
.header-italic { font-style: italic; }
```

## Content Searching Best Practices

When searching for content (Step 2):

- Use **2-3 parallel WebSearch calls** with different keyword angles (Chinese + English)
- For technology topics: search for overview, features, latest trends
- For business topics: search for market analysis, use cases, statistics
- For academic topics: search for concepts, history, key figures
- Combine search results, deduplicate, and synthesize into coherent slides
- Each content slide should have 3-5 key points (not walls of text)
- Use the user's preferred language (Chinese by default) for slide text

### Layout Selection Guide

Choose the right content layout based on the information type:

| Information Type | Recommended Layout | Why |
|-----------------|-------------------|-----|
| Advantages, features, value props | Layout A (Cards) | 3-col gradient cards with icon+description |
| Steps, key points, bullet points | Layout B (List) | Numbered circles convey sequence |
| Overview + detail split | Layout C (Two-Column) | Asymmetric left text + right grid |
| Industries, categories, product matrix, icon+text cards | Layout D (Grid) | 4x2 or 3x2 icon-driven equal-weight grid with glass cards (`content-text-grid.html`) |
| Scenario data, industry comparisons | Layout E (Table) | Rows scan across dimensions, metrics highlight |
| Success stories, solution demos | Layout F (Case) | Pain→Solution→Impact narrative arc |
| Roadmap, milestones, process history | Layout G (Timeline) | Alternating up/down nodes, clear time axis |
| Growth stories, evolution, trend data | Layout H (Growth) | SVG curve + positioned milestones, dramatic arc |
| Product matrix, tech stack, hierarchy | Layout I (Architecture) | Layered tiers with vertical labels, color-coded |
| Team intro, expert network, capability showcase | Layout J (Expert) | Center hub + radiating nodes, profile cards |
| Industry showcase, sector comparison, 8-item category pages | Layout K (Industry Grid) | 4x2 gradient-icon glass cards, icon inline with title |
| Product intro, positioning page, value proposition with dual-section | Layout L (Product Intro) | Hero header + 3 accent cards + split bottom (list + grid) |

**Visual Diversity Rules (v3.8 — prevents monotonous slides):**

1. **No more than 2 consecutive content slides may use the same layout.** If you have 3+ consecutive slides of the same type, reclassify content to use a different layout.

2. **"图文并茂" (image+text rich) ratio**: At least 40% of content slides should use visually rich layouts: Layout C (Mixed), D (Grid), F (Case), G (Timeline), H (Growth), I (Architecture), J (Expert), K (Industry Grid), or L (Product Intro). These layouts use icons, grids, flow diagrams, or imagery — not just text lists.

3. **Layout B (List) usage limit**: Layout B should be used for at most 25% of content slides. For detailed explanation slides, prefer enriching content with icons/categories and using Layout D (Grid with icons) instead. Only use Layout B when content truly is a pure sequential list without visual elements.

4. **Common conversion strategies**:
   - "4 key points" as Layout B → convert to Layout D (2x2 grid with icons) if each point has a distinct theme
   - "Feature explanation" as Layout B → convert to Layout A (3 cards) if features are comparable
   - "Module overview" as Layout B → convert to Layout C (left text + right grid) or Layout D (grid)
   - "Data/metrics" as Layout B → convert to Layout E (Table) for side-by-side comparison

5. **Step 3 plan review**: After creating the slide plan, count layout usage. If any layout appears 3+ times, adjust the plan to redistribute layouts before proceeding to Step 4.

6. **Sparse content merge rule (v3.9)**: If two adjacent content slides each have sparse content (e.g., ≤5 table rows, ≤3 bullet points, ≤2 cards) and related topics, merge them into a single slide instead of having two nearly-empty pages. Signs a slide is too sparse:
   - Table with ≤5 rows and short cell text → likely <40% of available vertical space used
   - List with ≤3 items and short descriptions → likely <30% of vertical space
   - Single chart/minimal content with large `flex-grow` area → blank space >50%
   - **Merge strategy**: Stack both sets of content vertically in one slide (e.g., two tables with a small gap, or table + summary list). Reduce cell padding and font size slightly (e.g., `text-sm`→`text-xs`, `py-3`→`py-1.5`) to fit comfortably. Place the more important content on top.
   - **TOC update**: When merging slides, update the TOC entry to reflect the merged topic (e.g., "竞品对比分析" + "生态运营与数据" → "竞品对比与生态数据") and renumber subsequent items.
   - **Before proceeding to Step 4**: Scan the plan for sparse slides that neighbor each other, and merge where possible.

## Quality Checklist

Before delivering, verify:
- [ ] All slides have 16:9 aspect ratio containers
- [ ] Navigation works: keyboard arrows, scroll, nav dots
- [ ] No horizontal scrollbar or overflow
- [ ] Text is readable with proper contrast
- [ ] All `{{PLACEHOLDER}}` markers replaced with actual content
- [ ] TOC items have corresponding content slides

**Design system checks:**
- [ ] Colors match the design system (Electric Blue primary)
- [ ] Glassmorphism effects applied correctly (backdrop-filter, semi-transparent borders)
- [ ] Cover has diagonal blue overlay; right-side has default hero image
- [ ] Ending has solid blue background
- [ ] No content overflow (each slide has `overflow:hidden`, max 4 items per slide)
- [ ] Numbered list items use `flex items-start` (NOT `items-center`) for multiline text
- [ ] Every content slide uses correct Layout A-L template (see Layout Selection Guide)

**Layout-specific checks:**
- [ ] Layout A (Cards): 3 columns, `.card-header-gradient` CSS present, `.glass-card` defined
- [ ] Layout B (List): Numbered circles with `.bg-product-orange`, max 4 items, text max 2 lines
- [ ] Layout C (Two-Column): 12-col grid, left `.col-span-7` + right `.col-span-5`
- [ ] Layout D (Grid): `.industry-icon-bg` gradient CSS present, max 8 items (2x4)
- [ ] Layout E (Table): `.bg-mesh`, `.glass-container` CSS present; table has 4-5 columns, 5-10 rows
- [ ] Layout F (Case): `.section-accent-*` CSS present; 3-zone layout (sources/pain → flow → metrics)
- [ ] Layout G (Timeline): `.timeline-line`, `.dot`, `.connect-line-*` CSS present; nodes alternate up/down
- [ ] Layout H (Growth): SVG viewBox `0 0 1600 800`, `linearGradient` defined, `.milestone-node` hover style
- [ ] Layout I (Architecture): `.vertical-text` CSS present, 2-3 tier colors defined, left labels + right tier blocks
- [ ] Layout J (Expert): `.central-circle-dashed`, `.expert-photo` CSS present; nodes on both sides of center
