# PPT Generator

基于 **Fluid Intelligence** 设计系统的 HTML 演示文稿生成器。全屏 16:9 沉浸式布局，玻璃拟态风格，Electric Blue 主题配色。

> 🎯 为 WorkBuddy 定制的 ppt-generator Skill | 版本 v3.1

## ✨ 特性

- **7 种页面模板**：封面、目录、内容页（4 种布局）、结束页
- **全屏 16:9**：基于 vh/vw 响应式布局，完美适配各类屏幕
- **键盘翻页**：方向键 / 空格键 / 滚轮导航，流畅切换
- **AI 内容生成**：无内容时自动 WebSearch + AI 总结生成幻灯片
- **封面图自动兜底**：AI 生图失败时使用默认装饰图，绝不空白
- **PPTX 导出**：通过 Python 脚本一键导出为 PowerPoint 文件
- **Glassmorphism 设计**：毛玻璃卡片 + 渐变叠加 + 微阴影层次

## 🎨 设计系统

| 要素 | 规格 |
|------|------|
| **主色** | Electric Blue `#0052D9` |
| **辅色** | Product Orange `#F37142` / Business Blue `#308EEF` / Strategy Green `#2BA471` |
| **表面色** | 柔和灰白 `#FAF8FF` |
| **玻璃面板** | 白色 60%-80% 透明度 + `backdrop-filter: blur(20-32px)` |
| **宽高比** | 16:9 |
| **网格** | 12 列流式布局，8px 基础间距 |
| **标题字体** | Hanken Grotesk / Noto Sans SC |
| **正文字体** | Inter / Noto Sans SC |
| **圆角** | 默认 8px，卡片 16px |

## 📄 页面模板

| 模板 | 文件 | 用途 |
|------|------|------|
| **封面** | `cover.html` | 蓝色斜切面叠加 + 背景图 + 右侧 Hero 图 |
| **目录** | `toc.html` | 左侧玻璃面板 + 右侧编号列表 |
| **内容页 A** | `content.html` | 3 卡片网格 / 编号列表 / 2×2 图标网格 |
| **内容页 B** | `content-table.html` | 数据表格，蓝色表头 + 悬停高亮行 |
| **内容页 C** | `content-case.html` | 场景案例：痛点 → 方案流程 → 业务指标 |
| **内容页 D** | `content-timeline.html` | 对角时间轴 + 交替里程碑卡片 |
| **结束页** | `ending.html` | 纯蓝背景感谢页 |

## 📁 项目结构

```
ppt-generator/
├── SKILL.md                       # Skill 定义与工作流程
├── README.md                      # 本文件
├── assets/
│   ├── templates/                 # 7 个 HTML 模板
│   │   ├── cover.html
│   │   ├── toc.html
│   │   ├── content.html
│   │   ├── content-table.html
│   │   ├── content-case.html
│   │   ├── content-timeline.html
│   │   └── ending.html
│   ├── slide-engine.js            # 翻页导航引擎
│   └── cover-default-hero.jpg     # 默认封面装饰图（腾讯滨海大厦）
├── scripts/
│   └── export_pptx.py             # PPTX 导出脚本
└── references/
    └── design_system.md           # 完整设计规范
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
| v3.1 | 2026-05-29 | 默认封面图兜底（腾讯滨海大厦）；SKILL.md 新增 version 字段 |
| v3.0 | 2026-05-29 | 修复封面缺图问题；修复内容页溢出（overflow-hidden / min-h-0 / flex-shrink-0）；新增内容密度约束规则 |
| v2.0 | 2026-05-29 | 新增 3 个内容模板（表格 / 案例 / 时间轴），总计 7 个模板 |
| v1.0 | 2026-05-29 | 初始版本，4 个模板（封面 / 目录 / 内容 / 结束） |

## 📄 许可证

本仓库仅供查看和下载。未经作者许可，禁止修改和再分发。

---

**作者**: jasonwu2019 | **仓库**: [github.com/jasonwu2019/ppt-generator](https://github.com/jasonwu2019/ppt-generator)
