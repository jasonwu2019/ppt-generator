---
name: ppt-generator
version: "3.1"
description: "HTML-based presentation slide generator using the Fluid Intelligence design system (16:9 immersive layout, glassmorphism, Electric Blue theme). Generates beautiful full-screen HTML slides with keyboard/scroll navigation and optional PPTX export. Supports cover page, table of contents, content pages, and ending page templates. When user has not provided specific slide content, this skill searches the web to gather information, summarizes with AI, and then builds the slides. This skill should be used when the user asks to generate/create/make a PPT, presentation, slides about any topic."
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

Create a slide-by-slide plan before writing any code:

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
  - "cards": 2-3 glassmorphism cards (good for features, comparisons)
  - "list": Numbered/icon list (good for steps, key points)
  - "grid": 2x2 or 3x2 grid of items (good for categories)
  - "mixed": Left text + right cards (good for overview + detail)
  - "table": Data table with glass container (good for comparisons, industry data, specifications)
  - "case": Case study with pain points + solution + metrics (good for success stories, solutions)
  - "timeline": Diagonal timeline with milestones (good for history, roadmap, evolution)

Slide N+1: Ending
  - Main text: [e.g., "感谢倾听" or custom]
```

### Step 4: Generate HTML

Create a single self-contained HTML file that includes all slides.

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
       <!-- Slide 1: Cover (from assets/templates/cover.html with placeholders replaced) -->
       <!-- Slide 2: TOC (from assets/templates/toc.html with placeholders replaced) -->
       <!-- Slide 3-N: Content pages -->
       <!-- Slide N+1: Ending (from assets/templates/ending.html with placeholders replaced) -->
     </div>
     <!-- Navigation indicators -->
     <!-- Slide engine JS (from assets/slide-engine.js, JS section) -->
   </body>
   </html>
   ```

4. **Each slide** must be wrapped in a `<section class="slide">` element with 16:9 container.
5. Replace all `{{PLACEHOLDER}}` markers with actual content.
6. Apply design system colors and typography consistently across all slides.
7. **Cover image handling**:
   - If a cover image was generated (Step 2.3): set `{{COVER_IMAGE_URL}}` = `cover-hero.png`, `{{COVER_IMAGE_ALT}}` = topic description.
   - If NO cover image was generated: copy `assets/cover-default-hero.jpg` (腾讯滨海大厦) to workspace alongside the HTML as `cover-hero.png`, then set `{{COVER_IMAGE_URL}}` = `cover-hero.png`, `{{COVER_IMAGE_ALT}}` = `"封面装饰图"`.
   - **The cover page MUST always have an image on the right side — never leave it blank.**
8. **Content density rules** (CRITICAL — prevents layout overflow):
   - Each content slide max 4 items (cards, list items, grid cells)
   - Each list item text max 2 lines (~60 Chinese characters)
   - Reduce padding from `p-10 lg:p-16` to `p-8 lg:p-12` when content is dense
   - Always add `overflow-hidden` and `flex-shrink-0` on headers, `min-h-0` on scrollable areas
   - Numbered list items MUST use `flex items-start` (NOT `items-center`) to handle multiline text

**Critical CSS rules for the container:**
```css
.slides-container { width: 100vw; height: 100vh; overflow: hidden; position: relative; }
.slide { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
         transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1); }
.slide.active { transform: translateY(0); }
.slide.above { transform: translateY(-100vh); }
.slide.below { transform: translateY(100vh); }
```

**Content page template usage:**
- For "cards" layout: use the 3-column glassmorphism card grid from `content.html`
- For "list" layout: use the numbered list pattern from the "核心3句话" section in `content.html`
- For "grid" layout: use the 2x2 product-form grid with icons in `content.html`
- For headers: use the left-side blue accent bar + title pattern
- For "table" layout: use `content-table.html` template
- For "case" layout: use `content-case.html` template
- For "timeline" layout: use `content-timeline.html` template

**Critical CSS rules for the container:**
```css
.slides-container { width: 100vw; height: 100vh; overflow: hidden; position: relative; }
.slide { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center;
         transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1); }
.slide.active { transform: translateY(0); }
.slide.above { transform: translateY(-100vh); }
.slide.below { transform: translateY(100vh); }
```

**Required fonts** (include in `<head>` when using any content template):
```html
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700;800&family=Inter:wght@400;500&family=Geist:wght@400;500;600&family=Noto+Sans+SC:wght@300;400;500;700&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet">
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

## Content Page Layouts Reference

When generating content pages, use these layout patterns:

### Layout A: Three Cards (for features, positioning, comparisons)
```html
<section class="slide">
  <main class="w-full h-screen flex flex-col p-10 lg:p-16 max-w-[1920px] mx-auto">
    <header><!-- Title with blue accent bar --></header>
    <section class="grid grid-cols-3 gap-8">
      <!-- Card 1: glass-card, border-l-product-orange -->
      <!-- Card 2: glass-card, border-l-business-blue -->
      <!-- Card 3: glass-card, border-l-strategy-green -->
    </section>
  </main>
</section>
```

### Layout B: Numbered List (for steps, key points)
```html
<!-- IMPORTANT: Use flex items-start for multiline text, NOT items-center -->
<section class="slide">
  <main class="w-full h-screen flex flex-col p-8 lg:p-12 overflow-hidden">
    <header class="mb-6 flex-shrink-0"><!-- Title --></header>
    <div class="space-y-3 flex-grow min-h-0 overflow-y-auto">
      <!-- Each item: flex items-start with numbered circle + text -->
      <!-- Max 4 items per slide, each text max 2 lines -->
    </div>
  </main>
</section>
```

### Layout C: Two-Column (for overview + detail)
```html
<section class="slide">
  <main class="w-full h-screen flex flex-col p-10 lg:p-16">
    <header><!-- Title --></header>
    <section class="grid grid-cols-12 gap-12 flex-grow">
      <div class="col-span-7"><!-- Left: main content --></div>
      <div class="col-span-5"><!-- Right: cards/grid --></div>
    </section>
  </main>
</section>
```

### Layout D: 2x2 Grid (for categories, product types)
```html
<section class="slide">
  <main class="w-full h-screen flex flex-col p-10 lg:p-16">
    <header><!-- Title --></header>
    <div class="grid grid-cols-2 gap-4 flex-grow">
      <!-- 4 items: icon circle + label -->
    </div>
  </main>
</section>
```

### Layout E: Data Table (for comparisons, industry data, specifications)

Use `content-table.html` template with these placeholders:
- `{{TABLE_TITLE}}`: Table section title (gradient text)
- `{{TABLE_SUBTITLE}}`: Subtitle below title
- `{{TABLE_HEADERS}}`: `<th>` elements inside `<tr>` in `<thead>` with `bg-primary text-on-primary`
- `{{TABLE_ROWS}}`: `<tr>` elements with `<td>` cells, use `hover:bg-primary/5` for interactivity
- `{{TABLE_FOOTER}}`: Footer attribution text
- `{{LOGO_URL}}`: Logo image URL

**Required CSS** (include in `<style>`):
```css
.bg-mesh { background-color: #faf8ff;
  background-image: radial-gradient(at 0% 0%, rgba(0,80,203,0.05) 0px, transparent 50%),
                    radial-gradient(at 100% 0%, rgba(0,204,249,0.08) 0px, transparent 50%),
                    radial-gradient(at 50% 100%, rgba(67,69,209,0.05) 0px, transparent 50%); }
.parallelogram { clip-path: polygon(25% 0%, 100% 0%, 75% 100%, 0% 100%); }
.glass-container { background: rgba(255,255,255,0.7); backdrop-filter: blur(32px);
                   border: 1px solid rgba(255,255,255,0.3); }
```

**Fonts required**: Inter, Hanken Grotesk, Geist, Material Symbols Outlined

### Layout F: Case Study (for success stories, solution demos)

Use `content-case.html` template with these placeholders:
- `{{CASE_TITLE}}`: Case study title (italic, primary color)
- `{{CASE_SOURCES}}`: 3 category icon cards (物流/跨境/零售 style)
- `{{CASE_PAIN_POINTS}}`: 2 pain point cards with icon + title + description
- `{{CASE_SOLUTION_TITLE}}`: Solution section title (e.g., "WorkBuddy 核心解法")
- `{{CASE_SOLUTION_FLOW}}`: 3-node flow diagram (Source→Core→Knowledge Base)
- `{{CASE_METRICS}}`: 2 metric cards (e.g., "x2", "-50%")
- `{{CASE_REFERENCES}}`: Reference tags (e.g., "某金融服务平台")
- `{{CASE_FOOTER_BUTTON}}`: Footer button text (e.g., "演示视频")
- `{{LOGO_URL}}`: Logo image URL

**Required CSS** (include in `<style>`):
```css
.glass-card { background: rgba(255,255,255,0.7); backdrop-filter: blur(32px);
              border: 1px solid rgba(255,255,255,0.2);
              box-shadow: 0 4px 20px rgba(0,80,203,0.05); }
.parallelogram { clip-path: polygon(25% 0%, 100% 0%, 75% 100%, 0% 100%); }
.section-accent-left { border-left: 4px solid #0066ff; }
.section-accent-orange { border-left: 4px solid #ff6b35; }
.section-accent-green { border-left: 4px solid #34a853; }
.fill-icon { font-variation-settings: 'FILL' 1; }
```

### Layout G: Diagonal Timeline (for history, roadmap, evolution)

Use `content-timeline.html` template with these placeholders:
- `{{TIMELINE_TITLE}}`: Page title (36px, gradient text)
- `{{TIMELINE_MILESTONES}}`: Multiple milestone blocks, alternating up/down positions
- `{{TIMELINE_SUMMARY}}`: Footer summary text
- `{{LOGO_URL}}`: Logo image URL

Each milestone block uses:
- `{{M_DATE}}`, `{{M_TITLE}}`, `{{M_DESC}}`, `{{M_COLOR}}`, `{{M_STAR}}`,
  `{{M_LEFT}}`, `{{M_HEIGHT}}`, `{{M_OFFSET}}`, `{{M_POS}}` (detail in template comments)

**Required CSS** (include in `<style>`):
```css
.canvas-16-9 { aspect-ratio: 16/9; width: 100vw; max-height: 100vh; margin: auto;
               position: relative; overflow: hidden; }
.timeline-line { position: absolute; bottom: 25%; left: 5%; width: 90%; height: 4px;
                 background: #00ccf9; transform: rotate(-25deg);
                 transform-origin: left bottom; z-index: 1; }
.milestone-marker { position: absolute; width: 12px; height: 12px;
                    background: #00ccf9; border-radius: 50%;
                    transform: translate(-50%,-50%); z-index: 2; }
.connector-line { position: absolute; width: 1px;
                  border-left: 1px dashed #727687; z-index: 1; }
.info-card { position: absolute; width: 260px; transform: translateX(-50%); z-index: 3; }
```

**Milestone positioning pattern** (alternate to avoid overlap):
- Milestone 1: UP, left:8%, height:h-24, offset:bottom-28
- Milestone 2: UP, left:24%, height:h-32, offset:bottom-36
- Milestone 3: DOWN, left:34%, height:h-20, offset:top-24
- Continue alternating, ~10-12% spacing between markers
- UP milestones use `bottom-[6px]` for connector; DOWN use `top:[6px]`

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
| Features, benefits, value props | Layout A (Cards) | Cards emphasize distinct items visually |
| Step-by-step, ordered items | Layout B (Numbered List) | Numbers convey sequence |
| Overview + detail split | Layout C (Two-Column) | Asymmetric balance for depth |
| Categories, product types | Layout D (2x2 Grid) | Equal visual weight, icon-driven |
| Comparisons, specs, industry data | Layout E (Table) | Rows allow scanning across dimensions |
| Success stories, solutions, scenarios | Layout F (Case Study) | Pain→Solution→Impact narrative arc |
| History, roadmap, milestones, evolution | Layout G (Timeline) | Time progression, forward momentum |

## Quality Checklist

Before delivering, verify:
- [ ] All slides have 16:9 aspect ratio containers
- [ ] Colors match the design system (Electric Blue primary)
- [ ] Glassmorphism effects applied correctly (backdrop-filter, semi-transparent borders)
- [ ] Navigation works: keyboard arrows, scroll, nav dots
- [ ] No horizontal scrollbar or overflow
- [ ] Text is readable with proper contrast
- [ ] All `{{PLACEHOLDER}}` markers replaced with actual content
- [ ] Cover has diagonal blue overlay; right-side has image (AI-generated or default 腾讯滨海大厦)
- [ ] No content overflow (each slide has `overflow:hidden`, max 4 items per slide)
- [ ] Numbered list items use `flex items-start` (NOT `items-center`) for multiline text
- [ ] Ending has solid blue background
- [ ] TOC items have corresponding content slides
- [ ] For Layout E (Table): required CSS (.bg-mesh, .parallelogram, .glass-container) is included
- [ ] For Layout F (Case Study): .section-accent-* CSS, Material Symbols font loaded
- [ ] For Layout G (Timeline): .canvas-16-9, .timeline-* CSS all present; milestones alternate up/down
