---
name: Fluid Intelligence
description: Complete design system specification for PPT generation
---

# Fluid Intelligence Design System

## Brand & Style

The brand personality is authoritative yet frictionless, designed for high-performance professionals.
The design style is a hybrid of **Corporate Modern** and **Glassmorphism**.

## Colors

### Primary Palette

| Token | Hex | Usage |
|-------|-----|-------|
| primary | `#0050cb` / `#0052D9` | Buttons, active states, brand indicators |
| on-primary | `#ffffff` | Text on primary backgrounds |
| primary-container | `#0066ff` | Prominent containers |
| primary-fixed | `#dae1ff` | Subtle primary backgrounds |

### Secondary & Tertiary

| Token | Hex | Usage |
|-------|-----|-------|
| secondary | `#00677f` | Data viz, secondary accents |
| secondary-container | `#00ccf9` | Cyan accent containers |
| tertiary | `#4345d1` | Deep indigo accent |
| tertiary-container | `#5d60eb` | Indigo containers |

### Accent Colors (for content cards)

| Name | Hex | Usage |
|------|-----|-------|
| product-orange | `#f37142` | Product/feature cards |
| business-blue | `#308eef` | Business/operation cards |
| strategy-green | `#2ba471` | Strategy/vision cards |

### Surface & Background

| Token | Hex | Usage |
|-------|-----|-------|
| background | `#faf8ff` | Page background (light mode) |
| surface | `#faf8ff` | Card/element backgrounds |
| surface-container | `#eaedff` | Layered container surfaces |
| surface-container-highest | `#dae2fd` | Highest elevation surfaces |
| on-surface | `#131b2e` | Primary text |
| on-surface-variant | `#424656` | Secondary text |
| outline | `#727687` | Borders, dividers |
| outline-variant | `#c2c6d8` | Subtle borders |

### Glass Layers

White at 60-80% opacity with backdrop blur:
```css
.glass-panel {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(32px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}
.glass-card {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.3);
}
```

## Typography

| Token | Font | Size | Weight | Line Height | Letter Spacing |
|-------|------|------|--------|-------------|----------------|
| display-lg | Hanken Grotesk | 56px | 700 | 64px | -0.02em |
| headline-lg | Hanken Grotesk | 32px | 600 | 40px | -0.01em |
| headline-md | Hanken Grotesk | 24px | 600 | 32px | - |
| body-lg | Inter | 18px | 400 | 28px | - |
| body-md | Inter | 16px | 400 | 24px | - |
| label-md | Geist | 14px | 500 | 20px | 0.02em |
| label-sm | Geist | 12px | 600 | 16px | 0.05em |

**Fallback for Chinese**: Noto Sans SC (used when Hanken Grotesk/Inter CJK support is limited)

## Layout & Spacing

### Grid System
- **Desktop**: 12-column fluid grid
- **Spacing Unit**: 8px (all spacing is a multiple of 8px)
- **Gutter Desktop**: 24px
- **Margin Desktop**: 40px
- **Container Max**: 1440px

### Immersive 16:9
```css
.aspect-16-9-container {
  aspect-ratio: 16 / 9;
  width: 100vw;
  max-height: 100vh;
  margin: auto;
  position: relative;
  overflow: hidden;
}
```

## Elevation & Depth

| Level | Description | CSS |
|-------|-------------|-----|
| L1 (Base) | Subtle gradients or solid neutral | `background: #faf8ff` |
| L2 (Cards) | White 70% + 32px blur + 1px border | `glass-card` class |
| L3 (Modals) | 90% opacity + 30px shadow | For overlays |
| Micro-depth | Inner shadows for inputs | `box-shadow: inset` |

## Shapes

- Default border-radius: `0.5rem` (8px) - buttons, small components
- Card border-radius: `1rem` (16px) - glass cards, containers
- Large border-radius: `1.5rem` (24px) - hero containers
- Pill shapes: `9999px` - status indicators, chips only

## Components

### Buttons
- **Primary**: Solid `#0066FF` fill, white text, 0.5rem radius
- **Secondary**: Ghost style, 1px border, glass hover effect

### Glass Cards
Signature component. Requirements:
1. Semi-transparent white background (60-80% opacity)
2. `backdrop-filter: blur(10px)` minimum
3. 1px semi-transparent white border
4. Rounded corners (1rem default)
5. Subtle shadow (`box-shadow: 0 10px 30px -10px rgba(0,0,0,0.05)`)

### Input Fields
- Semi-transparent background
- Distinct bottom-border focus state in primary blue

### Chips
- Highly rounded (pill)
- Low-contrast background tints matching category color

## Tailwind CSS Configuration

```javascript
tailwind.config = {
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        'tencent-blue': '#0052d9',
        'product-orange': '#f37142',
        'business-blue': '#308eef',
        'strategy-green': '#2ba471',
        'primary': '#0050cb',
        'on-primary': '#ffffff',
        'surface': '#faf8ff',
        'on-surface': '#131b2e',
        'outline': '#727687',
        'secondary-container': '#00ccf9',
        'tertiary-container': '#5d60eb',
      },
      borderRadius: {
        DEFAULT: '0.25rem',
        lg: '0.5rem',
        xl: '0.75rem',
        full: '9999px',
      },
      fontFamily: {
        'headline-lg': ['Hanken Grotesk', 'Noto Sans SC'],
        'headline-md': ['Hanken Grotesk', 'Noto Sans SC'],
        'body-md': ['Inter', 'Noto Sans SC'],
        'body-lg': ['Inter', 'Noto Sans SC'],
        'label-md': ['Geist'],
      },
      fontSize: {
        'headline-lg': ['32px', { lineHeight: '40px', letterSpacing: '-0.01em', fontWeight: '600' }],
        'headline-md': ['24px', { lineHeight: '32px', fontWeight: '600' }],
        'body-md': ['16px', { lineHeight: '24px', fontWeight: '400' }],
        'body-lg': ['18px', { lineHeight: '28px', fontWeight: '400' }],
        'label-md': ['14px', { lineHeight: '20px', letterSpacing: '0.02em', fontWeight: '500' }],
      },
    },
  },
}
```

## Cover Slide Specifics

- **Diagonal overlay**: 78% width, clip-path polygon for blue area
- **Background image**: Right side, object-cover, object-right
- **Title font**: 5.5vw, bold, line-height 1.2
- **Subtitle font**: 2.2vw, medium, 90% opacity
- **Footer font**: 1.8vw, medium, letter-spacing 0.05em
- **Blue color**: `#0052D9`

## Ending Slide Specifics

### Fluid Intelligence Ending

- **Background**: Solid `#005eff` (slightly brighter than primary)
- **Main text**: 11vw, white, bold italic, Noto Sans SC
- **Decorative squares**: White at 10% and 30% opacity, positioned absolutely
- **Text shadow**: `2px 2px 4px rgba(0,0,0,0.1)`

## Common SVG Icons

Available for use in content slides:

**Monitor/Desktop**: `<path d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>`

**Lightning/Bolt**: `<path d="M13 10V3L4 14h7v7l9-11h-7z"/>`

**Star**: `<path d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z"/>`

**Document**: `<path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/>`

**Grid/Apps**: `<path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>`

**Mobile**: `<path d="M12 18h.01M8 21h8a2 2 0 002-2V5a2 2 0 00-2-2H8a2 2 0 00-2 2v14a2 2 0 002 2z"/>`

**Server/Backend**: `<path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"/>`

**Box/Cube**: `<path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>`

**Book**: `<path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/>`

## Data Table Component (Layout E)

Used for industry data, comparisons, specification tables. Requirements:

1. **Container**: `.glass-container` with `backdrop-filter: blur(32px)`, rounded-xl, border
2. **Header row**: `bg-primary text-on-primary`, rounded top, font-headline
3. **Body rows**: `divide-y divide-outline-variant/20`, hover state `bg-primary/5`
4. **Category highlights**: Use `text-primary font-semibold` for category column
5. **Metric highlights**: Use `text-primary font-bold italic` for key metric column
6. **Star icons**: `.material-symbols-outlined text-[18px] text-orange-400` with `FILL: 1`

```css
.bg-mesh {
  background-color: #faf8ff;
  background-image:
    radial-gradient(at 0% 0%, rgba(0,80,203,0.05) 0px, transparent 50%),
    radial-gradient(at 100% 0%, rgba(0,204,249,0.08) 0px, transparent 50%),
    radial-gradient(at 50% 100%, rgba(67,69,209,0.05) 0px, transparent 50%);
}
.parallelogram { clip-path: polygon(25% 0%, 100% 0%, 75% 100%, 0% 100%); }
```

## Case Study Component (Layout F)

Used for success stories, solution scenarios. Structure:

1. **Top grid (12-col)**:
   - Left 4 cols: "典型需求来源" — 3 icon cards with category labels
   - Right 8 cols: "业务痛点" — 2 pain point cards with orange accents
2. **Main grid (12-col)**:
   - Left 8 cols: "核心解法" — 3-node flow diagram (Source → Core → Knowledge Base)
   - Right 4 cols: "业务效果" — Metric cards with green accent
3. **Footer**: Reference tags + action button

**Accent borders**:
```css
.section-accent-left { border-left: 4px solid #0066ff; }
.section-accent-orange { border-left: 4px solid #ff6b35; }
.section-accent-green { border-left: 4px solid #34a853; }
```

**Flow diagram**: 3 nodes connected by `arrow_forward` Material Symbols, center node highlighted with gradient glow effect.

## Diagonal Timeline Component (Layout G)

Used for history, roadmaps, evolution timelines. Key specs:

- **Canvas**: 16:9 `canvas-16-9` container, `overflow: hidden`
- **Timeline line**: Diagonally rotated (-25°) from bottom-left to top-right
  - Positioned at `bottom: 25%; left: 5%; width: 90%`
  - Color: `#00ccf9` (secondary-container), 4px height
  - Start dot: 30px circle at `#4A6CF7`
  - Arrow: CSS triangle at the end
- **Milestones**: Positioned along the diagonal at % intervals (8%, 24%, 34%, 44%, 54%, 66%, 78%, 88%, 98%)
- **Alternating pattern**: Milestones alternate between above (UP) and below (DOWN) the line to prevent overlap
- **Connector**: Dashed vertical line connecting marker to card
- **Info cards**: 260px wide, centered on marker, with date + title + description

**Standard spacing pattern**:
| Milestone | Position | Left % | Connector Height | Card Offset |
|-----------|----------|--------|-----------------|-------------|
| 1 | UP | 8% | h-24 | bottom-28 |
| 2 | UP | 24% | h-32 | bottom-36 |
| 3 | DOWN | 34% | h-20 | top-24 |
| 4 | UP | 44% | h-28 | bottom-32 |
| 5 | DOWN | 54% | h-24 | top-28 |
| 6 | UP | 66% | h-32 | bottom-36 |
| 7 | DOWN | 78% | h-20 | top-24 |
| 8 | UP | 88% | h-28 | bottom-32 |
| 9 | DOWN | 98% | h-24 | top-28 |

## Font Loading

All content templates require these Google Fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600;700;800&family=Inter:wght@400;500&family=Geist:wght@400;500;600&family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
```

Material Symbols Outlined usage:
```css
.material-symbols-outlined { font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24; }
.fill-icon { font-variation-settings: 'FILL' 1; }
```

---

# Tencent Cloud Corporate Design System

Extracted from 腾讯云介绍_浅色.pptx company template (1440×811px, 16:9).

## Design Philosophy

Clean, professional, minimal. No glassmorphism, no decorative overlays, no background images. 
The design communicates authority and trust through simplicity — a single blue accent bar + solid white space.

## Colors

### Corporate Palette

| Token | Hex | Usage |
|-------|-----|-------|
| `corp-accent` | `#006DFF` | Left vertical accent bar (17px, full height) |
| `corp-title-accent` | `#1365E2` | Decorative first-letter color in titles |
| `corp-bg` | `#FFFFFF` | Background (solid white) |
| `corp-title` | `#1A1A2E` | Title text (deep dark, near-black) |
| `corp-body` | `#333333` ~ `#555555` | Body text |
| `corp-subtle` | `#888888` ~ `#999999` | Footer, page numbers, secondary text |
| `corp-dk1` | `#000000` | System windowText |
| `corp-lt1` | `#FFFFFF` | System window |
| `corp-dk2` | `#1F497D` | Dark 2 theme color |
| `corp-lt2` | `#EEECE1` | Light 2 theme color |

### Accent Colors (theme XML)
| Name | Hex | Usage |
|------|-----|-------|
| `accent1` | `#4F81BD` | Theme accent 1 |
| `accent2` | `#C0504D` | Theme accent 2 |
| `accent3` | `#9BBB59` | Theme accent 3 |
| `accent4` | `#8064A2` | Theme accent 4 |
| `accent5` | `#4BACC6` | Theme accent 5 |
| `accent6` | `#F79646` | Theme accent 6 |

## Typography

| Token | Font | Size | Weight | Usage |
|-------|------|------|--------|-------|
| `corp-display` | TTTGB Medium → Noto Sans SC | 5-6vw (clamp: 40-80px) | 700 | Main title on cover |
| `corp-display-accent` | Same | 1.4× display size | 700 | First character (accent color) |
| `corp-headline` | Noto Sans SC | 2.5-3vw (clamp: 24-40px) | 700 | Section titles |
| `corp-subtitle` | Noto Sans SC / 微软雅黑 | 1.5-2.5vw (clamp: 18-36px) | 400 | Subtitles |
| `corp-body` | Noto Sans SC / 微软雅黑 | 1.2-1.8vw (clamp: 16-24px) | 400 | Body text |
| `corp-caption` | Inter | 0.8-1vw (clamp: 11-14px) | 400 | Page numbers, footer |
| `corp-label` | Inter | 0.9-1.2vw (clamp: 10-16px) | 400 | Tags, section labels |

**Font fallback chain**: `'Noto Sans SC', 'Microsoft YaHei', system-ui, sans-serif`

## Layout & Spacing

### Slide Frame
```
┌──────────────────────────────────────────────────────────┐
│▐ 17px                                                    │
│▌ #006DFF                                                 │
│▌                                                          │
│▌    Content area (flex-1, px-[6%])                       │
│▌    Title at ~9% from top                                │
│▌    Body starts ~3% below title                          │
│▌    Footer at ~3% from bottom                            │
│▌                                                          │
│▌                         Page N ── bottom-right, ~3%      │
└──────────────────────────────────────────────────────────┘
```

### Positioning Reference (from PPTX template)
| Element | Left | Top | Width | Height | Notes |
|---------|------|-----|-------|--------|-------|
| Accent Bar | 0 | 44px | 17px | full | `#006DFF` |
| Logo | 1120px | 53px | 265px | 25px | Top-right |
| Title | 49px | 37px | ~1089px | 68px | Top-left area |
| Content | ~55px | ~120px+ | var | var | Below title |

### Spacing Rules
- No glassmorphism — solid backgrounds only
- No border-radius (sharp corners)
- No drop-shadows on content
- Minimal padding: percentage-based (4-8%) for responsive scaling
- Content max-width: none (fills the available space)

## Corporate Cover Slide

- **Background**: Solid white (`#FFFFFF`)
- **Accent bar**: Left side, 17px, `#006DFF`, full height
- **Title**: Centered in the remaining space
  - First character: accent color `#1365E2`, 1.4× larger
  - Rest: `#1A1A2E`, bold, 5-6vw
- **Subtitle**: Below title, `#555`, 2.5vw
- **Tagline**: Bottom-left, `#999`, small caps, uppercase
- **Footer**: Bottom-right, presenter/date info
- **No images**, no decorative elements

## Corporate Content Slide

- **Background**: Solid white
- **Title area**: Bold, 24-40px, positioned ~9% from top
- **Content area**: Flexible — supports:
  - Text paragraphs (16-24px, `#333`)
  - Simple cards (2-4 columns, thin border or background tint)
  - Numbered/bullet lists (clean, minimal markers)
  - Tables (simple borders, no glass container)
- **Page number**: Bottom-right, `#999`, small

## Corporate Ending Slide

- **Background**: Solid white
- **Centered text**: Large "感谢倾听" with accent first character
- **Subtitle**: "Q & A" or custom, below the main text
- **Footer**: Contact/date info centered at bottom

## Corporate CSS Baseline

```css
/* Corporate theme — NO glassmorphism, NO gradients, NO decorative shadows */
.corp-slide {
  background: #FFFFFF;
  font-family: 'Noto Sans SC', 'Microsoft YaHei', system-ui, sans-serif;
}
.corp-accent-bar {
  width: 17px;
  height: 100%;
  background: #006DFF;
  flex-shrink: 0;
}
.corp-title {
  color: #1A1A2E;
  font-weight: 700;
}
.corp-title-accent {
  color: #1365E2;
  font-size: 1.4em;
  display: inline-block;
  line-height: 0.8;
  vertical-align: middle;
}
.corp-body {
  color: #333;
  line-height: 1.6;
}
.corp-card {
  background: #F8F9FC;
  border: 1px solid #E8ECF2;
  border-left: 3px solid #006DFF;
  padding: 5%;
  border-radius: 0;
}
```
