---
name: ppt-generator
version: "3.4"
description: "HTML-based presentation slide generator supporting TWO design themes: (1) Fluid Intelligence — glassmorphism, Electric Blue, immersive 16:9 with 10 Layout A-J templates; (2) Tencent Cloud Corporate — clean white, blue accent bar, all content via content-corp.html with corp-* CSS patterns. Generates full-screen HTML slides with keyboard/scroll navigation and optional PPTX export. v3.4 fixes Corporate/Layout A-J scope conflict."
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

## Design Themes

This skill supports TWO design themes. Choose based on context:

### Theme 1: Fluid Intelligence (default)
Modern, creative, glassmorphism-heavy. Best for: product launches, tech demos, creative pitches, design-forward presentations.

### Theme 2: Tencent Cloud Corporate (腾讯云企业模板)
Clean, professional, minimal. Best for: business reports, enterprise sales, investor decks, internal presentations, 腾讯对外正式文档.

**How to choose:**
- If the user mentions 腾讯/腾讯云/Tencent, 公司/企业/商务, or 正式汇报 → use **Theme 2 (Corporate)**
- If the user mentions 创意/科技感/炫酷, or no preference → use **Theme 1 (Fluid Intelligence)**
- Corporate theme is the default for Chinese enterprise/company scenarios

**Theme selection in the workflow:** See Step 4 (Generate HTML) for template file mappings.

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

### Corporate Theme Design Specs
From 腾讯云介绍_浅色.pptx company template (1440x811px, 16:9):

| Element | Specification |
|---------|--------------|
| **Primary / Accent Bar** | `#006DFF` — 17px left-side vertical bar, full slide height |
| **Title Accent** | `#1365E2` — decorative first-letter color |
| **Background** | `#FFFFFF` — solid white, clean and minimal |
| **Title Text** | `#1a1a2e` — deep dark, near-black |
| **Body Text** | `#333`~`#555` — readable dark gray |
| **Subtle Text** | `#888`~`#999` — footer, page numbers, tags |
| **Title Font** | TTTGB Medium → Noto Sans SC (fallback), bold, 3-6vw |
| **Body Font** | 微软雅黑 → Noto Sans SC (fallback), 400 weight |
| **Label Font** | Inter, uppercase, tracking-wider |
| **Border Radius** | None (sharp corners, corporate style) |
| **Glass Effects** | None (solid colors only) |
| **Layout Type** | Minimal: bar + content, no decorative elements |

**Corporate layout structure (every slide):**
```
┌──────────────────────────────────────────────┐
│ ▐   Logo (top-right)                         │
│ ▌                                            │
│ ▌  Title (top-left, below logo-level)        │
│ ▌                                            │
│ ▌  ┌──────────────────────────────────┐      │
│ ▌  │  Content Area                    │      │
│ ▌  │  (flexible: cards, list, grid,   │      │
│ ▌  │   text, table — max 4 items)     │      │
│ ▌  └──────────────────────────────────┘      │
│ ▌                   Page N / Footer          │
└──────────────────────────────────────────────┘
```

## Page Templates

Seven template types are available in `assets/templates/`:

| Template | File | Purpose |
|----------|------|---------|
| Cover | `cover.html` | Title slide with diagonal blue overlay + background image + hero image area (built-in SVG fallback) |
| TOC | `toc.html` | Table of contents with glassmorphism left panel + numbered list |
| Content (Text/Cards) | `content.html` | Multi-section content: 3-card grid, numbered list, 2x2 icon grid |
| Content (Table) | `content-table.html` | Data table with glass container, primary header, hover rows |
| Content (Case Study) | `content-case.html` | Scenario case study: pain points, solution flow, business metrics |
| Content (Timeline) | `content-timeline.html` | Diagonal timeline with alternating milestone cards |
| Ending | `ending.html` | Thank-you slide with solid blue background |

### Corporate Theme Templates

Three corporate-style templates based on 腾讯云 company design:

| Template | File | Purpose |
|----------|------|---------|
| Cover (Corp) | `cover-corp.html` | Title slide: 17px left blue bar + large title with first-letter accent + subtitle |
| Content (Corp) | `content-corp.html` | Content slide: blue bar + section title + flexible content area (cards, text, list) |
| Ending (Corp) | `ending-corp.html` | Thank-you slide: blue bar + centered thank-you text + subtitle |

Corporate templates use these key placeholders:
- `{{CORP_ACCENT_COLOR}}` — Left bar color (default `#006DFF`)
- `{{CORP_TITLE}}` — Page title
- `{{CORP_CONTENT}}` — Main HTML content (for content slides)
- `{{CORP_BG_COLOR}}` — Background (default `#FFFFFF`)
- `{{CORP_PAGE_NUM}}` — Page number in bottom-right
- Cover-specific: `{{CORP_TITLE_ACCENT_CHAR}}`, `{{CORP_TITLE_REST}}`, `{{CORP_SUBTITLE}}`, `{{CORP_TAGLINE}}`
- Ending-specific: `{{CORP_ENDING_TITLE_ACCENT}}`, `{{CORP_ENDING_TITLE_REST}}`, `{{CORP_ENDING_SUB}}`

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

If the user provided an outline or bullet points, use them directly. Skip to Step 2 (planning).

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
   - 1 cover slide: Title + subtitle + right-side hero image (generate if topic is visual)
   - 1 TOC slide: 4-10 key sections
   - 3-N content slides: One per TOC section, with bullet points, cards, or data
   - 1 ending slide: Thank you / Q&A

3. **Generate cover image** (when the topic is visual/has a physical subject):
   - Use ImageGen to generate a relevant transparent-background hero image
   - Then use rembg to remove background + PIL to crop watermarks
   - Save as `cover-hero.png` in workspace, reference as `{{COVER_IMAGE_URL}}`
   - If topic is abstract or ImageGen fails: skip, use the default building image (see Step 4)

4. **Verify completeness**: Ensure every TOC item has a corresponding content slide.

### Step 3: Plan Slide Structure

Create a slide-by-slide plan. First, **decide the theme** based on the Design Themes section above.

**For Fluid Intelligence theme:**
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
  - "grid": 4x2 or 3x2 grid of items with icons (good for categories, industries, product matrix)
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

**For Corporate theme (腾讯云企业模板):**
```
Slide 1: Cover (cover-corp.html)
  - CORP_TITLE_ACCENT_CHAR: First character of title (accent color #1365E2, 1.4x size)
  - CORP_TITLE_REST: Rest of title text
  - CORP_SUBTITLE: Subtitle below title
  - CORP_TAGLINE: Bottom-left tagline (e.g., company slogan)
  - CORP_FOOTER: Bottom-right info (presenter, date)
  - CORP_LOGO_URL: Company logo img tag (optional)

Slide 2: Table of Contents (use content-corp.html with CORP_CONTENT=list)
  - CORP_TITLE: "目录"
  - CORP_CONTENT: Numbered list of sections

Slide 3-N: Content slides (content-corp.html)
  - CORP_TITLE: Section title
  - CORP_CONTENT: HTML content — text paragraphs, bullet lists, cards, or simple tables
  - CORP_PAGE_NUM: Slide number (bottom-right)
  - **For each content slide, classify content type and use the matching Corporate pattern:**
    ```
    Slide 4: [Title]
      Content: cards (2-col .corp-card grid)
    Slide 5: [Title]
      Content: table (.corp-table + intro .corp-card)
    Slide 6: [Title]
      Content: split (.grid grid-cols-2 left text + right cards)
    Slide 7: [Title]
      Content: Q&A (.grid grid-cols-2 .corp-card with colored border-left)
    Slide 8: [Title]
      Content: code (.folder-tree block)
    ```

Slide N+1: Ending (ending-corp.html)
  - CORP_ENDING_TITLE_ACCENT: First character of "感谢倾听" (#006DFF)
  - CORP_ENDING_TITLE_REST: "谢倾听"
  - CORP_ENDING_SUB: "Q & A" or custom subtitle
```

Corporate content slides are simpler — no glassmorphism or diagonal layouts. Use:
- Text paragraphs with clear hierarchy
- Simple icon+text cards (max 4 per slide)
- Numbered/bullet lists (max 5 items, 2 lines each)
- Clean tables (simple borders, no glass container)

### Step 4: Generate HTML

Create a single self-contained HTML file that includes all slides.

**BEFORE generating any content slide HTML, complete this pre-check:**

1. **Check which theme was selected** in Step 3:
   - **Fluid Intelligence** → follow the Layout A-J template loading below
   - **Corporate** → skip template loading, use `content-corp.html` pattern with inline `{{CORP_CONTENT}}` HTML

**For Fluid Intelligence theme only — template loading pre-check:**
1. **Read the plan from Step 3** — identify which layout was assigned to each slide
2. **Load the correct template file** for each unique layout used:
   - Layout A/B/C/D → read `assets/templates/content.html`
   - Layout E → read `assets/templates/content-table.html`
   - Layout F → read `assets/templates/content-case.html`
   - Layout G → read `assets/templates/content-timeline.html`
   - Layout H/I/J → read `assets/templates/content.html` (use Layout reference patterns)
3. **Apply the layout-specific CSS and HTML patterns** from the Fluid Intelligence Layout Reference section below
4. **NEVER** generate a Fluid Intelligence content slide from scratch — always use the layout's canonical structure

**For Corporate theme only — content pattern pre-check:**
1. Classify each content slide by its content type (cards, list, table, Q&A, etc.) using the Corporate content patterns table above
2. Generate clean HTML inside `{{CORP_CONTENT}}` using ONLY the predefined `.corp-*` CSS classes (corp-card, corp-table, corp-num, corp-warn, folder-tree, etc.)
3. Do NOT use any Fluid Intelligence classes (glass-card, glass-container, bg-mesh, industry-icon-bg, etc.)
4. Do NOT load separate template files per slide — `content-corp.html` is the ONLY template for all corporate content slides
5. The full set of corporate CSS classes MUST be included once in `<style>` (see Corporate CSS reference below)

**Assembly rules (common to both themes):**
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

**Fluid Intelligence theme assembly:**
- Use: `cover.html`, `toc.html`, `content.html` (A/B/C/D), `content-table.html` (E), `content-case.html` (F), `content-timeline.html` (G), `ending.html`
- Include all glassmorphism CSS, Google Fonts, and Material Symbols
- Cover image generation applies (see Cover Image Generation section)

**Corporate theme assembly:**
- Use: `cover-corp.html`, `content-corp.html`, `ending-corp.html`
- Corporate theme uses ONLY `data-theme="corp"` on slides
- Simpler CSS: NO glassmorphism, NO Google Fonts required (Noto Sans SC from CDN)
- NO cover image generation needed (corporate templates use text-only titles)
- Replace placeholders with actual content per the corporate template comments
- Corporate content slides: generate clean HTML inside `{{CORP_CONTENT}}` (text, simple cards, lists)
- Font fallback chain: `'Noto Sans SC', 'Microsoft YaHei', system-ui, sans-serif`

**MANDATORY Corporate CSS classes** (must be included in `<style>` for ANY corporate theme PPT):
```css
/* Corporate content styles */
.corp-card {
  background: #F8FAFD; border: 1px solid #E8EDF4; border-radius: 8px;
  padding: 20px 24px; transition: all 0.2s;
}
.corp-card:hover { border-color: #006DFF; box-shadow: 0 2px 12px rgba(0,109,255,0.08); }
.corp-card-sm {
  background: #F8FAFD; border: 1px solid #E8EDF4; border-radius: 6px;
  padding: 14px 18px;
}
.corp-icon-circle {
  width: 44px; height: 44px; border-radius: 50%;
  background: linear-gradient(135deg, #006DFF, #0052CC);
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 20px; font-weight: 600; flex-shrink: 0;
}
.corp-tag {
  display: inline-block; background: rgba(0,109,255,0.08); color: #006DFF;
  padding: 3px 10px; border-radius: 4px; font-size: 13px; font-weight: 500;
}
.corp-tag-orange {
  display: inline-block; background: rgba(243,113,66,0.08); color: #E55C2E;
  padding: 3px 10px; border-radius: 4px; font-size: 13px; font-weight: 500;
}
.corp-table {
  width: 100%; border-collapse: collapse; font-size: 14px;
}
.corp-table th {
  background: #F0F4FA; color: #1a1a2e; font-weight: 600;
  padding: 10px 14px; text-align: left; border-bottom: 2px solid #006DFF;
}
.corp-table td {
  padding: 9px 14px; border-bottom: 1px solid #E8EDF4; color: #444;
}
.corp-table tr:hover td { background: #F8FAFD; }
.corp-num {
  display: inline-flex; align-items: center; justify-content: center;
  width: 28px; height: 28px; border-radius: 50%;
  background: #006DFF; color: #fff; font-size: 14px; font-weight: 600;
  flex-shrink: 0;
}
.corp-check-list { list-style: none; padding: 0; margin: 0; }
.corp-check-list li {
  display: flex; align-items: flex-start; gap: 10px;
  padding: 6px 0; font-size: 14px; color: #444; line-height: 1.6;
}
.corp-check-list li::before {
  content: "✓"; color: #2ba471; font-weight: 700; flex-shrink: 0; margin-top: 1px;
}
.corp-warn {
  background: #FFF8F0; border-left: 3px solid #E55C2E;
  padding: 12px 16px; border-radius: 0 6px 6px 0; font-size: 13px; color: #8B4513;
}
.folder-tree {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 13px; line-height: 1.8; color: #444;
  background: #F5F7FA; border-radius: 6px; padding: 14px 18px;
  border: 1px solid #E8EDF4;
}
.folder-tree .dir { color: #006DFF; font-weight: 600; }
.folder-tree .file { color: #555; }
.folder-tree .comment { color: #999; }
```

**Critical CSS rules for the container:**
```css
.slides-container { width: 100vw; height: 100vh; overflow: hidden; position: relative; }
.slide { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
         transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1); }
.slide.active { transform: translateY(0); }
.slide.above { transform: translateY(-100vh); }
.slide.below { transform: translateY(100vh); }
```

**Fluid Intelligence content page template usage (MANDATORY — every Fluid Intelligence content slide MUST match a layout):**

When using the Fluid Intelligence theme, before generating ANY content slide HTML, classify the page content type and explicitly select the correct layout. This is NOT optional — failure results in broken layouts.

| Content Type | Layout | Template File | Key Visual Pattern |
|-------------|--------|---------------|-------------------|
| Advantages, features, value props | **Layout A (Cards)** | `content.html` | 3-column gradient header cards with icon + description |
| Steps, key points, bullet content | **Layout B (List)** | `content.html` | Numbered circles (`bg-product-orange`) + flex items-start |
| Overview + detail split | **Layout C (Mixed)** | `content.html` | 12-col grid: left col-span-7 text + right col-span-5 2x2 grid |
| Industries, categories, product matrix | **Layout D (Grid)** | `content.html` | icon-grid 2x4 or 3x2 with `industry-icon-bg` gradient circles |
| Comparisons, specs, scenario data | **Layout E (Table)** | `content-table.html` | `glass-container` table, primary header, hover rows |
| Success stories, solution demos | **Layout F (Case)** | `content-case.html` | 3-zone: pain points → solution flow → business metrics |
| Roadmap, milestones, history | **Layout G (Timeline)** | `content-timeline.html` | Horizontal line, alternating up/down nodes, dot+connect-line |
| Growth story, evolution, trend | **Layout H (Growth)** | `content.html` | SVG growth curve + absolute-positioned milestones |
| Product matrix, tech stack, hierarchy | **Layout I (Architecture)** | `content.html` | Layered tiers, vertical-text labels, color-coded blocks |
| Team intro, expert network | **Layout J (Expert)** | `content.html` | Center hub + radiating profile cards + bottom metrics |

**For headers on ALL Fluid Intelligence layouts**: use parallelogram blue accent bar + page title pattern.

**Fluid Intelligence enforcement rules**:
- Each content slide in Step 3 plan MUST include `Layout: X (file: Y.html)` annotation
- When generating HTML in Step 4, read the template file specified for that layout
- NEVER default all content slides to `content.html` or any single template
- If a content type doesn't clearly match any layout, default to Layout B (List) — safest fallback

**Corporate content page rules (separate — do NOT mix with Layout A-J above):**

Corporate theme uses ONE template (`content-corp.html`) for ALL content slides. Classification is only needed for choosing the right HTML pattern to put inside `{{CORP_CONTENT}}`:

| Content Type | What to put in {{CORP_CONTENT}} |
|-------------|--------------------------------|
| Cards / features / comparisons | `.corp-card` grid (2-3 columns) with `.corp-icon-circle` + text |
| Steps / key points / bullets | `.corp-card` cards running list or numbered `.corp-num` circles |
| Overview + detail split | `.grid grid-cols-2` with left text + right cards/table |
| Categories / industries | `.grid grid-cols-2/3/4` of `.corp-card-sm` tag+label items |
| Data tables / comparisons | `.corp-table` with `.corp-card mb-4` intro paragraph |
| Code / folder structures | `.folder-tree` monospace blocks |
| Warnings / constraints | `.corp-warn` orange alert cards |
| Q&A / FAQ | `.grid grid-cols-2` of `.corp-card` with colored left border |
| Checklists | `ul.corp-check-list` with ✓ markers |

**Corporate theme uses these already-defined CSS classes** (defined in Step 4 assembly): `.corp-card`, `.corp-card-sm`, `.corp-icon-circle`, `.corp-tag`, `.corp-tag-orange`, `.corp-table`, `.corp-num`, `.corp-check-list`, `.corp-warn`, `.folder-tree`, `.diagram-box`.

**Corporate rules**:
- ALL content slides share the `content-corp.html` structure (17px left bar + section tag + title + content area + page number)
- Content diversity comes from the `{{CORP_CONTENT}}` HTML patterns — NOT from switching template files
- Max 4 major content blocks per slide; overflow content goes to next slide
- Corporate slides use plain HTML/CSS — NO glassmorphism, NO Material Symbols, NO TailwindCDN

**Content density rules** (CRITICAL — prevents layout overflow):
  - Each content slide max 4 items (cards, list items, grid cells)
  - Each list item text max 2 lines (~60 Chinese characters)
  - Reduce padding from `p-10 lg:p-16` to `p-8 lg:p-12` when content is dense
  - Always add `overflow-hidden` and `flex-shrink-0` on headers, `min-h-0` on scrollable areas
  - Numbered list items MUST use `flex items-start` (NOT `items-center`) to handle multiline text
  - Corporate theme: padding is managed by `px-[6%]` and `pt-[9%]` — do NOT add extra padding

**Required fonts** (include in `<head>` when using any content template):
```html
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700;800&family=Inter:wght@400;500&family=Geist:wght@400;500;600&family=Noto+Sans+SC:wght@300;400;500;700&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
```

**For Corporate theme, use a lighter font set** (no Google Fonts required for basic slides):
```html
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
```

When using **Layout E (Table)**, also include:
```css
.bg-mesh{background-color:#faf8ff;background-image:radial-gradient(at 0% 0%,rgba(0,80,203,.05) 0px,transparent 50%),radial-gradient(at 100% 0%,rgba(0,204,249,.08) 0px,transparent 50%),radial-gradient(at 50% 100%,rgba(67,69,209,.05) 0px,transparent 50%)}
.parallelogram{clip-path:polygon(25% 0%,100% 0%,75% 100%,0% 100%)}
.glass-container{background:rgba(255,255,255,.7);backdrop-filter:blur(32px);border:1px solid rgba(255,255,255,.3)}
```
Additional CSS for Layout F/G — see each template's Layout reference section above for required styles.

## Cover Image Generation

When the PPT topic is visual (product, technology, vehicle, building, device etc.), generate a cover hero image for the right-side white area:

1. **Use ImageGen** to generate a topic-relevant image (e.g., "a futuristic AI agent dashboard, clean minimalist style")
2. **Remove background** with rembg:
   ```python
   from rembg import remove
   from PIL import Image
   img = Image.open('cover-raw.png')
   result = remove(img)
   result.save('cover-hero.png', 'PNG')
   ```
3. **Crop watermark**: If the generated image has "图片由AI生成" text at bottom, crop bottom 6% with PIL.
4. **Set in cover template**: `{{COVER_IMAGE_URL}}` = `cover-hero.png`, `{{COVER_IMAGE_ALT}}` = topic description.
5. If no image is generated, set both to empty string `""`.

**Skip cover image generation when**: topic is abstract (theory, methodology, software architecture, management concepts), ImageGen fails, or user explicitly says no images. When skipped, copy `assets/cover-default-hero.jpg` (腾讯滨海大厦) to the workspace as `cover-hero.png` — the cover always has a real image, never blank.

### Step 5: Deliver the HTML

1. **Save** the generated HTML to the workspace as `[topic]-presentation.html`
2. **Preview** using `preview_url` with the absolute file path
3. Tell the user: arrow keys or scroll to navigate, or click the nav dots

### Step 6: PPTX Export (optional, only if user requests .pptx)

If the user explicitly asks for PPTX format or says "生成PPT文件":

1. Ensure `python-pptx` is installed in the managed Python environment:
   ```bash
   C:\Users\Administrator\.workbuddy\binaries\python\envs\default\bin\pip install python-pptx Pillow
   ```

2. Read and run `scripts/export_pptx.py`, passing:
   - The generated HTML file path
   - The output PPTX file path

3. The script converts each slide section into a PPTX slide, preserving text content
   and basic layout structure.

4. Deliver the PPTX file to the user.

## Content Page Layouts Reference (Fluid Intelligence ONLY)

基于 Fluid Intelligence 设计系统，提供 10 种内容页布局。每种布局基于已验证的 HTML 模板模式。

### Layout A: 优势卡片 (3-Column Cards — for advantages, features, comparisons)

三列并排卡片，每列包含：图标圆 + 标题 + glass-card（渐变蓝头部 + 白色内容区 + 底部英文装饰字）。

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
      <!-- 每列: 图标圆 + 标题 + glass-card(渐变头部 + 白色内容 + 英文底字) -->
    </div>
  </main>
</section>
```

**每个卡片结构**:
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

**关键CSS**:
```css
.glass-card { background: rgba(255,255,255,0.7); backdrop-filter: blur(32px);
              border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 4px 30px rgba(0,0,0,0.05); }
.card-header-gradient { background: linear-gradient(180deg, #0066ff 0%, #0050cb 100%); }
```

### Layout B: 编号列表 (Numbered List — for steps, key points, bullet content)

编号圆 + 文本的垂直列表，每个条目带彩色编号圆。

```html
<!-- 核心3句话 模式 -->
<div class="space-y-4">
  <div class="flex items-center bg-white/60 p-4 rounded-xl border border-slate-100 shadow-sm">
    <div class="w-10 h-10 rounded-full bg-product-orange text-white flex items-center justify-center font-bold text-xl mr-6 shrink-0">1</div>
    <p class="text-xl text-slate-700 font-medium">内容文本，关键信息用 <span class="text-tencent-blue font-bold italic">高亮</span></p>
  </div>
  <!-- 最多4条 -->
</div>
```

**规则**: 每条最多2行文本（~60字），使用 `flex items-start`（不是 `items-center`）处理多行。

### Layout C: 左右分栏 (Two-Column — for overview + detail)

左侧文本列表 + 右侧 2x2 图标网格，清晰的视觉对比。

```html
<section class="grid grid-cols-12 gap-12 flex-grow">
  <div class="col-span-7 flex flex-col">
    <h4 class="text-2xl font-bold mb-6">核心要点</h4>
    <div class="space-y-4"><!-- Layout B numbered list --></div>
  </div>
  <div class="col-span-5 flex flex-col">
    <h4 class="text-2xl font-bold mb-6">产品形态</h4>
    <div class="grid grid-cols-2 gap-4 flex-grow">
      <!-- 4个图标+标签卡片 -->
    </div>
  </div>
</section>
```

### Layout D: 内容条目网格 (Item Grid — for categories, industries, product matrix)

2x4 或 3x2 等间距网格，每个条目 = 圆形渐变图标 + 标题 + 描述。

```html
<div class="grid grid-cols-4 grid-rows-2 gap-gutter-desktop flex-grow">
  <article class="glass-card rounded-xl p-6 flex flex-col">
    <div class="flex items-center gap-4 mb-4">
      <div class="industry-icon-bg w-14 h-14 rounded-full flex items-center justify-center shadow-lg shadow-primary/20 shrink-0">
        <span class="material-symbols-outlined text-white text-3xl">icon_name</span>
      </div>
      <h2 class="font-headline-md text-headline-md">条目标题</h2>
    </div>
    <p class="font-body-md text-body-md text-on-surface-variant">描述文本，最多2行。</p>
  </article>
  <!-- 最多8个条目 (2x4) 或 6个 (3x2) -->
</div>
```

**关键CSS**:
```css
.industry-icon-bg { background: linear-gradient(135deg, #0066ff 0%, #0040a4 100%); }
```

### Layout E: 数据表格 (Data Table — for comparisons, specs, scenario data)

Glass-container 包裹的表格，primary 色表头，hover 行高亮。

```html
<div class="w-full glass-container rounded-xl overflow-hidden shadow-sm">
  <table class="w-full text-left border-collapse">
    <thead>
      <tr class="bg-primary text-on-primary">
        <th class="py-4 px-6 font-headline text-body-lg font-semibold">列1</th>
        <th class="py-4 px-6 font-headline text-body-lg font-semibold">列2</th>
        <th class="py-4 px-6 font-headline text-body-lg font-semibold">列3</th>
        <th class="py-4 px-6 font-headline text-body-lg font-semibold">列4</th>
      </tr>
    </thead>
    <tbody class="divide-y divide-outline-variant/20">
      <tr class="hover:bg-primary/5 transition-colors">
        <td class="py-3 px-6 font-semibold text-primary">行业名</td>
        <td class="py-3 px-6 text-body-md text-on-surface-variant">场景描述</td>
        <td class="py-3 px-6 text-body-md text-on-surface-variant">核心价值</td>
        <td class="py-3 px-6 text-body-md font-bold text-primary italic">提效数据</td>
      </tr>
      <!-- 5-10行 -->
    </tbody>
  </table>
</div>
```

**关键CSS**:
```css
.bg-mesh { background: radial-gradient(at 0% 0%, rgba(0,80,203,.05) 0px, transparent 50%),
                   radial-gradient(at 100% 0%, rgba(0,204,249,.08) 0px, transparent 50%); }
.glass-container { background: rgba(255,255,255,0.7); backdrop-filter: blur(32px);
                   border: 1px solid rgba(255,255,255,0.3); }
```

表格行 hover 微动效: `transform: translateX(8px)`。

### Layout F: 场景案例 (Case Study — for success stories, solutions)

三区布局：顶部（需求来源3图标 + 痛点2卡片）、中部（解法流程：来源→WorkBuddy→知识库）、右侧（业务效果2指标）。

```html
<!-- 顶部: 需求+痛点 -->
<div class="grid grid-cols-12 gap-6 mb-6 h-[22%]">
  <section class="col-span-4 glass-card rounded-xl p-4 section-accent-left">
    <!-- 3个 icon+label 来源卡片 -->
  </section>
  <section class="col-span-8 glass-card rounded-xl p-4 section-accent-orange">
    <!-- 2个痛点卡片: 圆形图标+标题+描述 -->
  </section>
</div>
<!-- 中部: 解法流程 + 业务效果 -->
<div class="grid grid-cols-12 gap-6 flex-grow">
  <section class="col-span-8 glass-card rounded-xl p-6 section-accent-left">
    <!-- 3节点流程: 企业微信 → WorkBuddy → 知识库 -->
  </section>
  <section class="col-span-4 glass-card rounded-xl p-6 section-accent-green">
    <!-- 2个指标卡片: x2, -50% -->
  </section>
</div>
```

**关键CSS**:
```css
.section-accent-left { border-left: 4px solid #0066ff; }
.section-accent-orange { border-left: 4px solid #ff6b35; }
.section-accent-green { border-left: 4px solid #34a853; }
```

### Layout G: 水平路线图 (Horizontal Timeline — for roadmap, history, milestones)

水平时间线，节点上下交替排列，dot + connect-line 连接。

```html
<main class="flex-grow flex items-center relative w-full px-12">
  <div class="timeline-line"></div>
  <div class="flex justify-between w-full relative z-10">
    <!-- 上方节点 -->
    <div class="relative flex flex-col items-center">
      <div class="absolute bottom-12 w-64 mb-8">
        <h3 class="font-headline-md text-headline-md text-primary">年份</h3>
        <p class="font-body-md text-on-surface-variant">描述</p>
      </div>
      <div class="connect-line-top"></div>
      <div class="dot"></div>
    </div>
    <!-- spacer dots -->
    <!-- 下方节点 -->
    <div class="relative flex flex-col items-center">
      <div class="dot"></div>
      <div class="connect-line-bottom"></div>
      <div class="absolute top-12 w-64 mt-8">
        <h3 class="font-headline-md text-headline-md text-primary">年份</h3>
        <p class="font-body-md text-on-surface-variant">描述</p>
      </div>
    </div>
  </div>
</main>
```

**关键CSS**:
```css
.timeline-line { height: 1px; background: #00ccf9; width: 100%; position: absolute; top: 50%; }
.dot { width: 24px; height: 24px; background: #0050cb; border-radius: 50%; z-index: 10; }
.connect-line-top { width: 1px; height: 120px; background: #00ccf9; position: absolute; bottom: 24px; left: 50%; }
.connect-line-bottom { width: 1px; height: 120px; background: #00ccf9; position: absolute; top: 24px; left: 50%; }
```

**规则**: 节点上下交替，首节点在上方，每2-3个节点间插入 spacer dots。每页最多8-10个里程碑。

### Layout H: 增长曲线 (Growth Timeline — for growth stories, evolution, trend)

SVG 趋势线 + 绝对定位里程碑节点的增长可视化。

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
    <!-- 绝对定位里程碑: 日期 + 描述 + dot -->
    <div class="absolute" style="left: 5%; top: 58%;">
      <span class="text-primary mb-1">1998.11</span>
      <p class="font-semibold">里程碑事件</p>
      <div class="w-3 h-3 bg-primary rounded-full milestone-node"></div>
    </div>
    <!-- 8-12个里程碑沿SVG路径分布 -->
  </div>
</main>
```

**关键CSS**: milestone-node hover 放大 (`transform: scale(1.4)`), SVG 路径动画 (`stroke-dasharray/dashoffset`)。

### Layout I: 架构图 (Architecture — for product matrix, tech stack, layered structure)

分层架构展示，左侧竖排标签 + 右侧多层颜色区分区块。

```html
<main class="flex-1 flex gap-2 px-8 pb-8 min-h-0">
  <div class="w-12 flex flex-col gap-2 shrink-0">
    <div class="flex-1 bg-blue-50 border border-blue-200 rounded flex items-center justify-center">
      <span class="vertical-text text-primary font-bold text-sm">解决方案</span>
    </div>
    <div class="h-[45%] bg-blue-50 border border-blue-200 rounded flex items-center justify-center">
      <span class="vertical-text text-primary font-bold text-sm">通用产品</span>
    </div>
  </div>
  <div class="flex-1 flex flex-col gap-3 min-h-0">
    <!-- 每层: 颜色头部 + 网格子项 -->
    <div class="flex-1 border-2 border-tier-solutions flex flex-col rounded-sm overflow-hidden">
      <div class="bg-tier-solutions text-white text-center py-1.5 text-lg font-bold">层名称</div>
      <div class="flex-1 grid grid-cols-3 divide-x bg-white p-4"><!-- 子项 --></div>
    </div>
  </div>
</main>
```

**颜色变量**: tier-solutions `#00b5d1`, tier-paas `#0066ff`, tier-iaas `#0052cc`。

**关键CSS**:
```css
.vertical-text { writing-mode: vertical-rl; text-orientation: mixed; }
```

### Layout J: 图文并茂 (Hub & Spokes — for team intros, expert networks, capability showcase)

中心盾牌图标 + 环形关键词 + 左右各3个"头像+文字"节点，底部成果展示。

```html
<div class="flex-grow relative flex items-center justify-center">
  <!-- 中心盾牌 + 虚线圆 -->
  <div class="relative w-48 h-48 flex flex-col items-center justify-center z-10">
    <div class="central-circle-dashed"></div>
    <div class="bg-white rounded-full p-6 shadow-lg border border-blue-100">
      <svg><!-- 盾牌图标 --></svg>
    </div>
    <span class="absolute -top-6 text-[11px] text-gray-500">连接</span>
    <span class="absolute -bottom-24 text-center">
      <p class="text-2xl font-bold">3500+安全专家</p>
    </span>
  </div>
  <!-- 左/右两侧人物节点 -->
  <div class="absolute left-0 w-1/3 h-full"><!-- 3个右对齐头像+描述 --></div>
  <div class="absolute right-0 w-1/3 h-full"><!-- 3个左对齐头像+描述 --></div>
</div>
<!-- 底部成果网格: 3列 -->
<footer class="grid grid-cols-3 gap-0 border-t">
  <div class="pr-8 border-r"><!-- 里程碑 --></div>
  <div class="px-8 border-r"><!-- 奖项 --></div>
  <div class="pl-8"><!-- 漏洞 --></div>
</footer>
```

**关键CSS**: skew-banner (`transform: skewX(-20deg)`), expert-photo (`w-16 h-16 rounded-full`), central-circle-dashed (`border: 1px dashed #0066ff; border-radius: 50%`)。

## Content Searching Best Practices

When searching for content (Step 2):

- Use **2-3 parallel WebSearch calls** with different keyword angles (Chinese + English)
- For technology topics: search for overview, features, latest trends
- For business topics: search for market analysis, use cases, statistics
- For academic topics: search for concepts, history, key figures
- Combine search results, deduplicate, and synthesize into coherent slides
- Each content slide should have 3-5 key points (not walls of text)
- Use the user's preferred language (Chinese by default) for slide text

### Layout Selection Guide (Fluid Intelligence)

Choose the right content layout based on the information type:

| Information Type | Recommended Layout | Why |
|-----------------|-------------------|-----|
| Advantages, features, value props | Layout A (Cards) | 3-col gradient cards with icon+description |
| Steps, key points, bullet points | Layout B (List) | Numbered circles convey sequence |
| Overview + detail split | Layout C (Two-Column) | Asymmetric left text + right grid |
| Industries, categories, product matrix | Layout D (Grid) | 2x4 or 3x2 icon-driven equal-weight grid |
| Scenario data, industry comparisons | Layout E (Table) | Rows scan across dimensions, metrics highlight |
| Success stories, solution demos | Layout F (Case) | Pain→Solution→Impact narrative arc |
| Roadmap, milestones, process history | Layout G (Timeline) | Alternating up/down nodes, clear time axis |
| Growth stories, evolution, trend data | Layout H (Growth) | SVG curve + positioned milestones, dramatic arc |
| Product matrix, tech stack, hierarchy | Layout I (Architecture) | Layered tiers with vertical labels, color-coded |
| Team intro, expert network, capability showcase | Layout J (Expert) | Center hub + radiating nodes, profile cards |

## Quality Checklist

Before delivering, verify:
- [ ] All slides have 16:9 aspect ratio containers
- [ ] Navigation works: keyboard arrows, scroll, nav dots
- [ ] No horizontal scrollbar or overflow
- [ ] Text is readable with proper contrast
- [ ] All `{{PLACEHOLDER}}` markers replaced with actual content
- [ ] TOC items have corresponding content slides

**Fluid Intelligence theme checks:**
- [ ] Colors match the design system (Electric Blue primary)
- [ ] Glassmorphism effects applied correctly (backdrop-filter, semi-transparent borders)
- [ ] Cover has diagonal blue overlay; right-side has image (AI-generated or default 腾讯滨海大厦)
- [ ] Ending has solid blue background

**Corporate theme checks:**
- [ ] Left blue bar: 17px, `#006DFF`, full height on every slide
- [ ] Background is solid white (`#FFFFFF`) on all slides
- [ ] NO glassmorphism, NO backdrop-filter, NO diagonal overlays
- [ ] NO TailwindCDN — all styling is plain CSS
- [ ] Title first character uses accent color (`#1365E2`) at 1.4x size
- [ ] Cover uses `cover-corp.html` template with text-only title
- [ ] ALL content slides use `content-corp.html` with inline `{{CORP_CONTENT}}` HTML
- [ ] ALL `.corp-*` CSS classes (corp-card, corp-table, corp-num, corp-warn, folder-tree, etc.) are included in `<style>`
- [ ] Page numbers shown in bottom-right on content slides
- [ ] Ending uses `ending-corp.html` with centered thank-you text
- [ ] NO Fluid Intelligence classes used (no glass-card, glass-container, bg-mesh, industry-icon-bg, etc.)

**Both themes:**
- [ ] No content overflow (each slide has `overflow:hidden`, max 4 items per slide)
- [ ] Numbered list items use `flex items-start` (NOT `items-center`) for multiline text
- [ ] **Fluid Intelligence: every content slide uses correct Layout A-J template** (see Layout Selection Guide)
- [ ] **Corporate: ALL content slides use ONLY `content-corp.html` template** — content diversity comes from `{{CORP_CONTENT}}` patterns, not different template files

**Layout-specific checks (Fluid Intelligence only):**
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
