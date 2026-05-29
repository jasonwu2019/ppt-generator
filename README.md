# PPT Generator

基于 Fluid Intelligence 设计系统的 HTML 演示文稿生成器：玻璃拟态、Electric Blue 主色、12 种页面布局（Layout A-L）。

> 🎯 为 WorkBuddy 定制的 ppt-generator Skill | 版本 v3.18

## ✨ 特性

- **Fluid Intelligence 设计系统**：玻璃拟态 + Electric Blue 主色 + 16:9 沉浸式全屏
- **12 种 Layout（A-L）**：覆盖封面/目录/卡片网格/表格/案例/时间轴/行业网格/产品介绍等全部场景
- **全屏 16:9**：基于 vh/vw 响应式布局，禁止滚动，键盘/滚轮翻页
- **AI 内容生成**：无内容时自动 WebSearch + AI 总结生成幻灯片
- **封面图自动兜底**：AI 生图失败时使用默认装饰图（硅谷科技楼），绝不空白
- **📸 真实浏览器全屏截图导出**：Playwright **headed** Chromium（可见窗口）+ `--start-fullscreen`（F11），通过实际 Windows GPU 管线渲染，导出效果与浏览器全屏完全一致
- **Glassmorphism 设计**：毛玻璃卡片 + 渐变叠加 + 微阴影层次
- **视觉多样性规则**：禁止连续 3 张同布局，图文并茂比例 ≥ 40%，稀疏内容自动合并

## 🎨 设计系统

| 要素 | 规格 |
|------|------|
| **主色** | Electric Blue `#0050cb` |
| **辅色** | Product Orange `#ff6b35` / Business Blue `#308EEF` / Strategy Green `#2BA471` |
| **渐变** | `#0050cb → #00ccf9`（标题渐变）/ `#0066ff → #0040a4`（图标渐变） |
| **表面色** | 柔和灰白 `#FAF8FF` |
| **玻璃面板** | 白色 60%-85% 透明度 + `backdrop-filter: blur(20-32px)` |
| **宽高比** | 16:9（1920×1080 基准） |
| **网格** | 12 列流式布局，8px 基础间距 |
| **标题字体** | Hanken Grotesk / Noto Sans SC |
| **正文字体** | Inter / Noto Sans SC |
| **圆角** | 默认 8px，卡片 16px，大卡片 20px |

## 📄 页面模板（10 种文件 / 12 种 Layout）

| 模板文件 | Layout | 用途 |
|----------|--------|------|
| `cover.html` | — | 封面页：蓝色斜切面叠加 + 背景图 + 右侧 Hero 图 |
| `toc.html` | — | 目录页：左侧玻璃面板 + 右侧编号列表 |
| `content.html` | A/B/C/D/H/I/J | 多功能内容：3卡片网格(A) / 编号列表(B) / 2×2图标网格(C) / 通用卡片(D) / 增长曲线(H) / 架构层级(I) / 专家网络(J) |
| `content-text-grid.html` | D | **标准 4×2 卡片网格**：图标+标题+描述 |
| `content-text-industry.html` | **K** | **行业网格**（v3.13）：4×2 渐变图标玻璃卡片，用于行业应用/业务场景 |
| `content-text-intro.html` | **L** | **产品介绍**（v3.13）：Hero头部+3定位卡片+底部分栏 |
| `content-table.html` | E | 数据表格：玻璃容器 + 蓝色表头 + 悬停高亮行 |
| `content-case.html` | F | 场景案例：痛点 → 方案流程 → 业务指标 |
| `content-timeline.html` | G | 时间轴：中轴线 + 交替里程碑卡片 + 渐变连接线 |
| `ending.html` | — | 结束页：纯蓝背景感谢页 |

## 📁 项目结构

```
ppt-generator/
├── SKILL.md                          # Skill 定义与完整工作流程（v3.14）
├── README.md                         # 本文件
├── assets/
│   ├── templates/                    # 10 个 HTML 模板
│   │   ├── cover.html                # 封面页
│   │   ├── toc.html                  # 目录页
│   │   ├── content.html              # 多功能内容（Layout A/B/C/D/H/I/J）
│   │   ├── content-text-grid.html    # 标准卡片网格（Layout D）
│   │   ├── content-text-industry.html # 行业网格（Layout K）
│   │   ├── content-text-intro.html   # 产品介绍（Layout L）
│   │   ├── content-table.html        # 数据表格（Layout E）
│   │   ├── content-case.html         # 场景案例（Layout F）
│   │   ├── content-timeline.html     # 时间轴（Layout G）
│   │   └── ending.html               # 结束页
│   ├── slide-engine.js               # 翻页导航引擎
│   └── cover-default-hero.jpg        # 默认封面装饰图（硅谷科技楼）
├── scripts/
│   └── export_pptx.py                # PPTX/PDF 导出（Playwright 截图驱动 v4.0）
└── references/
    └── design_system.md              # 完整设计规范
```

## 🚀 使用方式

### 在 WorkBuddy 中使用

1. 将 `ppt-generator` 安装为 WorkBuddy Skill
2. 对话中直接说：
   - 「帮我生成一个关于新能源汽车的 PPT」
   - 「做一个 AI 大模型发展史的演示文稿」
   - 「Generate a presentation about quantum computing」

Skill 会自动：搜索资料 → AI 总结 → 选择模板 → 生成 HTML → 导出 PPTX

### 手动使用模板

1. 选择模板 HTML 文件
2. 替换 `{{PLACEHOLDER}}` 变量
3. 用浏览器打开 HTML 文件
4. 使用方向键翻页

### 导出 PPTX

```bash
python scripts/export_pptx.py your-presentation.html
```

## 📋 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|----------|
| v3.18 | 2026-05-29 | **真实浏览器全屏截图**：从 headless 模拟改为 **headed（可见）Chromium + --start-fullscreen（F11）**；渲染通过实际 Windows GPU 管线，字体/玻璃态/色彩与真实 Chrome 完全一致 |
| v3.17 | 2026-05-29 | **GPU渲染导出**：`--use-gl=angle --use-angle=swiftshader` 软件GPU确保backdrop-filter/玻璃态正确渲染；强制sRGB色彩；过渡等待2×CSS时长(1.2s)；导出与真实浏览器F11全屏视觉一致 |
| v3.16 | 2026-05-29 | **16:9 全屏视口截图优化**：移除无用的 --start-fullscreen；headless Chromium 原生无 chrome = 全屏画布；新增 `document.fonts.ready` 等待 + Tailwind 编译缓冲，确保截图与浏览器显示完全一致 |
| v3.15 | 2026-05-29 | **全屏浏览器截图**：导出引擎添加 `--start-fullscreen`（F11 等效），确保截图与浏览器全屏访问完全一致 |
| v3.14 | 2026-05-29 | **导出引擎重写**: Playwright 截图驱动替代文本提取，PPTX/PDF 与 HTML 像素一致；3840x2160 视网膜质量 |
| v3.13 | 2026-05-29 | 新增 2 个文本模板：行业网格（Layout K）+ 产品介绍（Layout L）；升级到 12 种 Layout |
| v3.12 | 2026-05-29 | 修复时间轴连接线消失：calc() 运算符两侧添加空格（CSS 规范要求） |
| v3.11 | 2026-05-29 | 时间轴连接线双锚点定位：top+bottom 动态拉伸替代固定高度；marker 偏移 ±3px |
| v3.10 | 2026-05-29 | 修复时间轴 DOWN 卡片连接线渐变方向（0deg） |
| v3.9 | 2026-05-29 | 新增稀疏内容合并规则：相邻内容过少页面自动合并 |
| v3.8 | 2026-05-29 | 修复时间轴连接线方向；TOC/封面图改用固定目录图片；新增视觉多样性规则 |
| v3.7 | 2026-05-29 | 修复内容页溢出、表格换行问题；新增 Layout A-J 选择指引 |
| v3.5 | 2026-05-29 | 简化为单主题 Fluid Intelligence |
| v3.2 | 2026-05-29 | 新增腾讯云企业模板主题（3 个模板）；双主题设计系统 |
| v3.1 | 2026-05-29 | 默认封面图兜底（腾讯滨海大厦）；SKILL.md 新增 version 字段 |
| v3.0 | 2026-05-29 | 修复封面缺图问题；修复内容页溢出；新增内容密度约束规则 |
| v2.0 | 2026-05-29 | 新增 3 个内容模板（表格 / 案例 / 时间轴），总计 7 个模板 |
| v1.0 | 2026-05-29 | 初始版本，4 个模板（封面 / 目录 / 内容 / 结束） |

## 📄 许可证

本仓库仅供查看和下载。未经作者许可，禁止修改和再分发。

---

**作者**: jasonwu2019 | **仓库**: [github.com/jasonwu2019/ppt-generator](https://github.com/jasonwu2019/ppt-generator)
