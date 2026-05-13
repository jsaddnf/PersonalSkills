#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设计系统 — 课程生成器（通用版）
字体：PingFang SC 优先，Noto Sans CJK SC / Microsoft YaHei 兜底
渲染：WeasyPrint (HTML → PDF) / 可选 HTML / DOCX / Markdown

关键设计决策：
1. 字体优先级：PingFang SC > Noto Sans CJK SC > Microsoft YaHei
   在 macOS 用户本地打开时自动使用苹方（更美观），
   在服务器/Linux 渲染 PDF 时落到 Noto Sans CJK SC（兼容）。
2. Emoji 规范化：所有 emoji 需用 <span class="emoji"> 包裹
   用 normalize_emoji() 自动完成。避免 emoji 撑破行高、串字号。
3. 多格式输出：write_pdf / write_html / write_docx / write_markdown
   或用 write_course(..., formats=['pdf', 'html']) 统一分发。
"""

import os
import re
import subprocess

# ═══════════════════════════════════════════════════════════
#  全局设计 Token
# ═══════════════════════════════════════════════════════════
COLORS = {
    'primary':       '#1A3A5C',   # 深海蓝 — 品牌主色
    'accent':        '#2563EB',   # 电光蓝 — 强调/链接
    'accent_light':  '#EFF6FF',   # 极浅蓝 — 背景
    'accent_mid':    '#BFDBFE',   # 浅蓝   — 分隔线
    'success':       '#059669',   # 翠绿   — 好示例
    'success_bg':    '#F0FDF4',
    'success_bd':    '#BBF7D0',
    'danger':        '#DC2626',   # 红     — 坏示例
    'danger_bg':     '#FEF2F2',
    'danger_bd':     '#FECACA',
    'warn':          '#D97706',   # 琥珀   — 练习题
    'warn_bg':       '#FFFBEB',
    'warn_bd':       '#FDE68A',
    'purple':        '#7C3AED',   # 紫     — 进阶技巧
    'purple_bg':     '#F5F3FF',
    'purple_bd':     '#DDD6FE',
    'gray_100':      '#F8F9FA',
    'gray_200':      '#E9ECEF',
    'gray_400':      '#9CA3AF',
    'gray_600':      '#6B7280',
    'gray_800':      '#1F2937',
    'text':          '#111827',   # 正文
    'text_secondary':'#4B5563',   # 次要文字
    'white':         '#FFFFFF',
    'code_bg':       '#F1F5F9',
    'code_text':     '#1E40AF',
}

# ═══════════════════════════════════════════════════════════
#  全局 CSS
# ═══════════════════════════════════════════════════════════
BASE_CSS = """
/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

@page {
    size: A4;
    margin: 20mm 22mm 22mm 22mm;
    @top-center {
        content: element(header-area);
    }
    @bottom-center {
        content: element(footer-area);
    }
}

/* ── 字体设置（PingFang 优先） ── */
body {
    /* 字体优先级说明：
       1) PingFang SC/TC/HK — Apple 系统首选，本地查看 PDF/HTML 最美观
       2) Noto Sans CJK SC — Linux/服务器端 WeasyPrint 渲染兜底
       3) Microsoft YaHei / Source Han Sans — Windows/开源环境兜底
       4) 最后是 emoji 字体族，保证 emoji 不落到豆腐框 */
    font-family: 'PingFang SC', 'PingFang TC', 'PingFang HK',
                 'Noto Sans CJK SC', 'Source Han Sans SC',
                 'Microsoft YaHei', 'Hiragino Sans GB',
                 'Apple Color Emoji', 'Segoe UI Emoji', 'Noto Color Emoji',
                 sans-serif;
    font-size: 10.5pt;
    line-height: 1.85;
    color: %(text)s;
    font-weight: 400;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
}

/* ── Emoji 样式规范化（关键） ──
   所有 emoji 必须用 <span class="emoji"> 包裹，
   或用 normalize_emoji() 自动包裹。
   解决以下排版问题：
   a) emoji 原生字号比汉字大 → 锁定 1em（0.92em 视觉居中）
   b) emoji 字形带上下边距 → line-height: 1 + vertical-align 居中
   c) emoji 行高撑破段落 → inline-block 限制影响范围
   d) emoji 被斜体/加粗继承 → font-style/font-weight normal */
.emoji {
    font-family: 'Apple Color Emoji', 'Segoe UI Emoji',
                 'Noto Color Emoji', 'Twemoji Mozilla',
                 'Noto Emoji', sans-serif;
    font-size: 0.95em;
    font-style: normal;
    font-weight: 400;
    font-variant: normal;
    line-height: 1;
    vertical-align: -0.08em;
    display: inline-block;
    text-decoration: none;
    white-space: nowrap;
    /* 防止 emoji 触发断行 */
    word-break: keep-all;
}

/* ── 页眉 ── */
#page-header {
    position: running(header-area);
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 8pt;
    color: %(text_secondary)s;
    border-bottom: 1px solid %(gray_200)s;
    padding-bottom: 4px;
    margin-bottom: 0;
}
#page-header .brand { font-weight: 700; color: %(primary)s; }
#page-header .chapter { color: %(gray_600)s; }

/* ── 页脚 ── */
#page-footer {
    position: running(footer-area);
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 8pt;
    color: %(gray_400)s;
    border-top: 1px solid %(gray_200)s;
    padding-top: 4px;
}
#page-footer::after { content: counter(page); }

/* ── 版心容器 ── */
.page-body { padding: 0; }

/* ── 标题层级 ── */
h1.lesson-title {
    font-size: 22pt;
    font-weight: 700;
    color: %(white)s;
    line-height: 1.3;
    letter-spacing: -0.02em;
}
h2 {
    font-size: 13pt;
    font-weight: 700;
    color: %(primary)s;
    line-height: 1.4;
    margin-top: 24pt;
    margin-bottom: 8pt;
    padding-left: 10pt;
    border-left: 3.5px solid %(accent)s;
}
h3 {
    font-size: 11pt;
    font-weight: 700;
    color: %(gray_800)s;
    line-height: 1.5;
    margin-top: 14pt;
    margin-bottom: 5pt;
}

/* ── 正文段落 ── */
p {
    font-size: 10.5pt;
    line-height: 1.85;
    color: %(text)s;
    margin-bottom: 8pt;
    text-align: justify;
    word-break: break-all;
}

/* ── 列表 ── */
ul, ol {
    margin: 6pt 0 10pt 18pt;
    padding: 0;
}
ul { list-style: none; }
ul li { position: relative; padding-left: 14pt; margin-bottom: 5pt; line-height: 1.7; font-size: 10.5pt; }
ul li::before {
    content: '';
    position: absolute;
    left: 0; top: 8pt;
    width: 5px; height: 5px;
    border-radius: 50%%;
    background: %(accent)s;
}
ol { list-style: none; counter-reset: ol-counter; }
ol li {
    counter-increment: ol-counter;
    position: relative;
    padding-left: 20pt;
    margin-bottom: 6pt;
    line-height: 1.7;
    font-size: 10.5pt;
}
ol li::before {
    content: counter(ol-counter);
    position: absolute;
    left: 0; top: 0;
    width: 16px; height: 16px;
    background: %(accent)s;
    color: white;
    border-radius: 50%%;
    font-size: 8pt;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 16px;
    text-align: center;
}

/* ── 课程封面卡片 ── */
.lesson-cover {
    background: linear-gradient(135deg, %(primary)s 0%%, #1e4d7b 60%%, #2563eb 100%%);
    border-radius: 10px;
    padding: 32pt 28pt;
    margin-bottom: 24pt;
    color: %(white)s;
}
.lesson-cover .lesson-num {
    font-size: 9pt;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: %(accent_mid)s;
    margin-bottom: 8pt;
}
.lesson-cover h1.lesson-title { margin-bottom: 12pt; }
.lesson-cover .lesson-desc {
    font-size: 10pt;
    line-height: 1.7;
    color: rgba(255,255,255,0.82);
    margin-bottom: 20pt;
    max-width: 90%%;
}
.lesson-meta {
    display: flex;
    gap: 0;
    flex-wrap: wrap;
    margin-top: 16pt;
    border-top: 1px solid rgba(255,255,255,0.2);
    padding-top: 14pt;
}
.lesson-meta-item {
    flex: 1;
    min-width: 120pt;
}
.lesson-meta-item .label {
    font-size: 7.5pt;
    font-weight: 500;
    letter-spacing: 0.08em;
    color: %(accent_mid)s;
    text-transform: uppercase;
    display: block;
    margin-bottom: 3pt;
}
.lesson-meta-item .value {
    font-size: 9pt;
    font-weight: 500;
    color: white;
}

/* ── 信息卡片系统 ── */
.card {
    border-radius: 8px;
    padding: 13pt 15pt;
    margin: 10pt 0;
    page-break-inside: avoid;
}
.card-title {
    font-size: 10pt;
    font-weight: 700;
    margin-bottom: 6pt;
    line-height: 1.4;
    display: flex;
    align-items: center;
    gap: 6pt;
}
.card-body {
    font-size: 10pt;
    line-height: 1.8;
    color: %(text)s;
}
.card-body p { margin-bottom: 5pt; font-size: 10pt; }
.card-body p:last-child { margin-bottom: 0; }

/* 知识点卡 — 蓝色 */
.card-key {
    background: %(accent_light)s;
    border-left: 3.5px solid %(accent)s;
    border: 1px solid %(accent_mid)s;
    border-left: 3.5px solid %(accent)s;
}
.card-key .card-title { color: %(primary)s; }

/* 好示例卡 — 绿色 */
.card-good {
    background: %(success_bg)s;
    border: 1px solid %(success_bd)s;
    border-left: 3.5px solid %(success)s;
}
.card-good .card-title { color: %(success)s; }

/* 坏示例卡 — 红色 */
.card-bad {
    background: %(danger_bg)s;
    border: 1px solid %(danger_bd)s;
    border-left: 3.5px solid %(danger)s;
}
.card-bad .card-title { color: %(danger)s; }

/* 提示/Tip 卡 — 灰色 */
.card-tip {
    background: %(gray_100)s;
    border: 1px solid %(gray_200)s;
    border-left: 3.5px solid %(gray_400)s;
}
.card-tip .card-title { color: %(gray_800)s; }

/* 练习题卡 — 琥珀色 */
.card-exercise {
    background: %(warn_bg)s;
    border: 1px solid %(warn_bd)s;
    border-left: 3.5px solid %(warn)s;
}
.card-exercise .card-title { color: %(warn)s; }

/* 进阶技巧卡 — 紫色 */
.card-advanced {
    background: %(purple_bg)s;
    border: 1px solid %(purple_bd)s;
    border-left: 3.5px solid %(purple)s;
}
.card-advanced .card-title { color: %(purple)s; }

/* 答案卡 — 绿色深 */
.card-answer {
    background: %(success_bg)s;
    border: 1px solid %(success_bd)s;
    border-left: 3.5px solid %(success)s;
}
.card-answer .card-title { color: %(success)s; }

/* ── 对比表格 ── */
.compare-table {
    width: 100%%;
    border-collapse: collapse;
    margin: 10pt 0;
    font-size: 10pt;
    page-break-inside: avoid;
}
.compare-table th {
    padding: 8pt 12pt;
    font-size: 9.5pt;
    font-weight: 700;
    text-align: left;
    line-height: 1.4;
}
.compare-table th.bad-col {
    background: %(danger)s;
    color: white;
    border-radius: 6px 0 0 0;
    width: 50%%;
}
.compare-table th.good-col {
    background: %(success)s;
    color: white;
    border-radius: 0 6px 0 0;
    width: 50%%;
}
.compare-table td {
    padding: 10pt 12pt;
    vertical-align: top;
    line-height: 1.75;
}
.compare-table td.bad-cell {
    background: %(danger_bg)s;
    border: 1px solid %(danger_bd)s;
    border-top: none;
    border-radius: 0 0 0 6px;
}
.compare-table td.good-cell {
    background: %(success_bg)s;
    border: 1px solid %(success_bd)s;
    border-top: none;
    border-radius: 0 0 6px 0;
}

/* ── 提示词展示块 ── */
.prompt-block {
    margin: 10pt 0;
    border-radius: 8px;
    overflow: hidden;
    page-break-inside: avoid;
    border: 1px solid %(accent_mid)s;
}
.prompt-header {
    background: %(primary)s;
    color: white;
    padding: 6pt 12pt;
    font-size: 8.5pt;
    font-weight: 700;
    letter-spacing: 0.06em;
    display: flex;
    align-items: center;
    gap: 5pt;
}
.prompt-body {
    background: %(accent_light)s;
    padding: 12pt 14pt;
    font-size: 10pt;
    line-height: 1.85;
    color: %(primary)s;
    font-family: 'PingFang SC', 'Noto Sans CJK SC',
                 'Source Han Sans SC', 'Microsoft YaHei', sans-serif;
    white-space: pre-wrap;
    word-break: break-all;
}

/* ── 框架表格（RTCF等） ── */
.data-table {
    width: 100%%;
    border-collapse: collapse;
    margin: 10pt 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
}
.data-table thead tr {
    background: %(primary)s;
    color: white;
}
.data-table thead th {
    padding: 8pt 10pt;
    text-align: left;
    font-weight: 700;
    font-size: 9.5pt;
    line-height: 1.4;
}
.data-table thead th:first-child { border-radius: 6px 0 0 0; }
.data-table thead th:last-child  { border-radius: 0 6px 0 0; }
.data-table tbody tr:nth-child(odd)  { background: %(white)s; }
.data-table tbody tr:nth-child(even) { background: %(gray_100)s; }
.data-table tbody td {
    padding: 7pt 10pt;
    border-bottom: 1px solid %(gray_200)s;
    vertical-align: top;
    line-height: 1.7;
}
.data-table tbody tr:last-child td:first-child { border-radius: 0 0 0 6px; }
.data-table tbody tr:last-child td:last-child  { border-radius: 0 0 6px 0; }

/* ── 工具/目录表格 ── */
.toc-table {
    width: 100%%;
    border-collapse: collapse;
    margin: 10pt 0;
    font-size: 10pt;
}
.toc-table thead tr { background: %(accent)s; color: white; }
.toc-table thead th {
    padding: 9pt 12pt;
    text-align: left;
    font-weight: 700;
    line-height: 1.4;
    font-size: 9.5pt;
}
.toc-table tbody tr:nth-child(odd)  { background: %(white)s; }
.toc-table tbody tr:nth-child(even) { background: %(gray_100)s; }
.toc-table tbody td {
    padding: 8pt 12pt;
    border-bottom: 1px solid %(gray_200)s;
    line-height: 1.65;
    vertical-align: top;
}
.toc-table .lesson-no {
    font-weight: 700;
    color: %(primary)s;
    white-space: nowrap;
}
.toc-table .lesson-name { font-weight: 500; }
.toc-table .lesson-topics { color: %(text_secondary)s; font-size: 9pt; }

/* ── 分隔线 ── */
hr.section-divider {
    border: none;
    border-top: 1px solid %(gray_200)s;
    margin: 20pt 0 16pt;
}
hr.accent-divider {
    border: none;
    border-top: 2px solid %(accent)s;
    margin: 20pt 0;
    width: 40pt;
}

/* ── 标签/Tag ── */
.tag {
    display: inline-block;
    padding: 2pt 7pt;
    border-radius: 4px;
    font-size: 8.5pt;
    font-weight: 600;
    margin-right: 5pt;
    margin-bottom: 3pt;
    line-height: 1.5;
}
.tag-blue   { background: %(accent_light)s; color: %(accent)s; border: 1px solid %(accent_mid)s; }
.tag-green  { background: %(success_bg)s;  color: %(success)s; border: 1px solid %(success_bd)s; }
.tag-purple { background: %(purple_bg)s;   color: %(purple)s;  border: 1px solid %(purple_bd)s; }

/* ── 课程导读封面 ── */
.course-cover {
    background: linear-gradient(150deg, %(primary)s 0%%, #0f2a47 40%%, %(accent)s 100%%);
    border-radius: 12px;
    padding: 44pt 36pt;
    color: white;
    text-align: center;
    margin-bottom: 28pt;
}
.course-cover .course-label {
    font-size: 8.5pt;
    font-weight: 600;
    letter-spacing: 0.15em;
    color: %(accent_mid)s;
    margin-bottom: 10pt;
    text-transform: uppercase;
}
.course-cover .course-title {
    font-size: 28pt;
    font-weight: 700;
    line-height: 1.25;
    letter-spacing: -0.02em;
    margin-bottom: 10pt;
    color: white;
}
.course-cover .course-subtitle {
    font-size: 12pt;
    line-height: 1.6;
    color: rgba(255,255,255,0.80);
    margin-bottom: 24pt;
}
.course-stats {
    display: flex;
    justify-content: center;
    gap: 0;
    border-top: 1px solid rgba(255,255,255,0.2);
    padding-top: 18pt;
    margin-top: 4pt;
}
.course-stat {
    flex: 1;
    text-align: center;
    padding: 0 10pt;
}
.course-stat + .course-stat {
    border-left: 1px solid rgba(255,255,255,0.2);
}
.course-stat .stat-num {
    font-size: 20pt;
    font-weight: 700;
    color: white;
    display: block;
    line-height: 1.2;
}
.course-stat .stat-label {
    font-size: 8.5pt;
    color: rgba(255,255,255,0.65);
    display: block;
    margin-top: 3pt;
}

/* ── 答案手册封面 ── */
.answer-cover {
    background: linear-gradient(135deg, %(success)s 0%%, #047857 100%%);
    border-radius: 12px;
    padding: 44pt 36pt;
    color: white;
    text-align: center;
    margin-bottom: 24pt;
}
.answer-cover .cover-icon { font-size: 28pt; margin-bottom: 10pt; }
.answer-cover h1 {
    font-size: 24pt;
    font-weight: 700;
    color: white;
    margin-bottom: 10pt;
}
.answer-cover p {
    color: rgba(255,255,255,0.82);
    font-size: 10.5pt;
    text-align: center;
}

/* ── 练习题编号 ── */
.exercise-num {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 20pt;
    height: 20pt;
    background: %(warn)s;
    color: white;
    border-radius: 50%%;
    font-size: 9pt;
    font-weight: 700;
    margin-right: 6pt;
    flex-shrink: 0;
    vertical-align: middle;
}

/* ── 工具推荐徽章 ── */
.stars { color: #F59E0B; font-size: 9pt; }

/* ── 小字说明 ── */
.footnote {
    font-size: 8.5pt;
    color: %(text_secondary)s;
    margin-top: 4pt;
}

/* ── 页面间断控制 ── */
.page-break { page-break-before: always; }
.no-break   { page-break-inside: avoid; }

/* ── Strong / Em ── */
strong { font-weight: 700; color: %(gray_800)s; }
em { font-style: normal; font-weight: 500; color: %(accent)s; }
code {
    font-family: 'SF Mono', 'PingFang SC', 'Noto Sans Mono CJK SC',
                 'Source Han Sans HW', Menlo, Consolas, monospace;
    font-size: 9.5pt;
    background: %(code_bg)s;
    color: %(code_text)s;
    padding: 1pt 4pt;
    border-radius: 3px;
}
""" % COLORS


# ═══════════════════════════════════════════════════════════
#  HTML 屏幕阅读专属 CSS（包在 @media screen 内，PDF 不受影响）
#  设计规范 v1：见 ~/Downloads/courses/ai-pm-transition/DESIGN_SPEC.md
# ═══════════════════════════════════════════════════════════
HTML_SCREEN_CSS = """
@media screen {
    /* ── 1. 页面外层：暖灰背景 + 平滑滚动 ── */
    html { background: #F5F6F8; scroll-behavior: smooth; }
    body {
        background: transparent;
        font-size: 16px;
        line-height: 1.85;
        letter-spacing: 0.02em;
        color: #1F2937;
        padding: 0;
        margin: 0;
    }

    /* ── 2. 阅读容器：760px max + 居中卡片 ── */
    .page-body {
        max-width: 760px;
        margin: 24px auto 80px;
        background: #FFFFFF;
        padding: 56px 64px;
        border-radius: 16px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.05),
                    0 1px 3px rgba(0,0,0,0.03);
    }

    /* ── 3. 顶部品牌条（替代 PDF running header） ── */
    #page-header {
        max-width: 760px;
        margin: 24px auto 0;
        padding: 12px 24px;
        background: #FFFFFF;
        border-radius: 12px;
        border-bottom: none;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        font-size: 13px;
    }
    #page-header .brand { font-size: 13px; }
    #page-header .chapter { font-size: 13px; }
    #page-footer { display: none; }

    /* ── 4. 标题层级 ── */
    h2 {
        font-size: 22px;
        line-height: 1.45;
        margin-top: 48px;
        margin-bottom: 16px;
        padding-left: 14px;
        border-left-width: 4px;
    }
    h2:first-child { margin-top: 0; }
    h3 {
        font-size: 18px;
        line-height: 1.55;
        margin-top: 32px;
        margin-bottom: 8px;
    }

    /* ── 5. 正文段落（关键修复） ── */
    p {
        font-size: 16px;
        line-height: 1.85;
        margin-bottom: 18px;
        text-align: left;            /* 不用 justify，HTML 没连字符算法 */
        word-break: normal;          /* 不切英文单词 */
        overflow-wrap: anywhere;     /* 长 URL/代码自然换行 */
        letter-spacing: 0.02em;
    }

    /* ── 6. 列表 ── */
    ul, ol { margin: 8px 0 18px 0; }
    ul li, ol li {
        font-size: 16px;
        line-height: 1.75;
        margin-bottom: 8px;
        padding-left: 22px;
    }
    ul li::before { top: 11px; width: 5px; height: 5px; }
    ol li { padding-left: 30px; }
    ol li::before {
        width: 20px; height: 20px;
        font-size: 11px;
        line-height: 20px;
        top: 2px;
    }

    /* ── 7. 卡片系统 ── */
    .card {
        border-radius: 12px;
        padding: 20px 24px;
        margin: 24px 0;
        border-left-width: 4px;
    }
    .card-title {
        font-size: 16px;
        margin-bottom: 12px;
        gap: 8px;
    }
    .card-body { font-size: 15.5px; line-height: 1.8; }
    .card-body p { font-size: 15.5px; margin-bottom: 10px; }
    .card-body ul, .card-body ol { margin-top: 8px; margin-bottom: 0; }
    .card-body ul li, .card-body ol li { font-size: 15.5px; margin-bottom: 6px; }

    /* ── 8. 课程封面 ── */
    .lesson-cover {
        padding: 44px 40px;
        border-radius: 16px;
        margin-bottom: 36px;
    }
    .lesson-cover .lesson-num { font-size: 12px; margin-bottom: 12px; }
    .lesson-cover h1.lesson-title {
        font-size: 30px;
        line-height: 1.25;
        margin-bottom: 16px;
    }
    .lesson-cover .lesson-desc {
        font-size: 15px;
        line-height: 1.75;
        margin-bottom: 24px;
    }
    .lesson-meta { margin-top: 20px; padding-top: 18px; }
    .lesson-meta-item .label { font-size: 11px; }
    .lesson-meta-item .value { font-size: 14px; }

    /* ── 9. 课程导读封面 ── */
    .course-cover {
        padding: 56px 40px;
        border-radius: 16px;
        margin-bottom: 40px;
    }
    .course-cover .course-title { font-size: 32px; }
    .course-cover .course-subtitle { font-size: 16px; line-height: 1.7; }

    /* ── 10. 表格统一升级 ── */
    .compare-table, .data-table, .toc-table {
        font-size: 15px;
        margin: 24px 0;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
    .compare-table th { padding: 12px 18px; font-size: 14px; }
    .compare-table td { padding: 14px 18px; font-size: 15px; line-height: 1.75; }
    .data-table thead th, .toc-table thead th {
        padding: 12px 16px;
        font-size: 14px;
    }
    .data-table tbody td, .toc-table tbody td {
        padding: 12px 16px;
        font-size: 14.5px;
        line-height: 1.7;
    }

    /* ── 11. Prompt 展示块 ── */
    .prompt-block { border-radius: 10px; margin: 24px 0; }
    .prompt-header { padding: 10px 16px; font-size: 13px; }
    .prompt-body {
        padding: 16px 18px;
        font-size: 15px;
        line-height: 1.8;
        word-break: normal;
        overflow-wrap: anywhere;
    }

    /* ── 12. 标签/Tag ── */
    .tag {
        padding: 4px 10px;
        font-size: 12px;
        border-radius: 6px;
        margin-right: 6px;
        margin-bottom: 4px;
    }

    /* ── 13. 行内样式 ── */
    strong { color: #0F172A; }
    em { color: #2563EB; font-weight: 500; }
    code { font-size: 14px; padding: 2px 6px; border-radius: 4px; }

    /* ── 14. 选中高亮 ── */
    ::selection { background: #DBEAFE; color: #0F172A; }

    /* ── 15. 分隔线 ── */
    hr.section-divider { margin: 32px 0 24px; }
    hr.accent-divider { margin: 32px 0; width: 56px; border-top-width: 2px; }

    /* ── 16. 响应式：1024px 以下 ── */
    @media (max-width: 1024px) {
        .page-body, #page-header {
            max-width: calc(100% - 64px);
        }
        .page-body { padding: 48px 48px; }
    }

    /* ── 17. 响应式：平板 768px 以下 ── */
    @media (max-width: 768px) {
        body { font-size: 15.5px; }
        .page-body, #page-header { max-width: calc(100% - 32px); }
        .page-body {
            padding: 36px 28px;
            border-radius: 12px;
            margin-top: 16px;
            margin-bottom: 48px;
        }
        #page-header { margin-top: 16px; padding: 10px 16px; }
        h2 { font-size: 20px; margin-top: 36px; }
        h3 { font-size: 17px; }
        .card { padding: 18px 20px; margin: 20px 0; }
        .lesson-cover { padding: 36px 28px; border-radius: 14px; }
        .lesson-cover h1.lesson-title { font-size: 24px; }
        .compare-table th, .compare-table td,
        .data-table thead th, .data-table tbody td {
            padding: 10px 12px;
            font-size: 14px;
        }
    }

    /* ── 18. 响应式：手机 480px 以下 ── */
    @media (max-width: 480px) {
        body { font-size: 15px; }
        .page-body, #page-header { max-width: 100%; }
        .page-body {
            padding: 28px 20px;
            border-radius: 0;
            margin: 0 0 32px 0;
            box-shadow: none;
        }
        #page-header {
            border-radius: 0;
            margin: 0;
            padding: 12px 20px;
            box-shadow: none;
            border-bottom: 1px solid #E5E7EB;
        }
        h2 { font-size: 19px; padding-left: 10px; }
        .lesson-cover { padding: 28px 20px; border-radius: 10px; }
        .lesson-cover h1.lesson-title { font-size: 22px; }
        .card { padding: 16px 18px; }
    }
}
"""


# ═══════════════════════════════════════════════════════════
#  Emoji 规范化工具（关键模块）
# ═══════════════════════════════════════════════════════════
# 问题背景：
#   emoji 在 PDF/HTML 渲染中会因为字号、基线、字体族不同，
#   导致 a) 撑破行高；b) 行内错位；c) 和加粗/斜体叠加出错；
#   d) 部分环境显示成 □（豆腐块）。
# 解决方案：
#   所有 emoji 必须用 <span class="emoji">…</span> 包裹，
#   由 CSS 强制锁定 font-family、font-size、line-height、
#   vertical-align。只要统一走这个包装，排版就稳定。

# ─── Unicode emoji 范围（覆盖 99% 常用场景） ──────────────
_EMOJI_PATTERN = re.compile(
    r"(?:"
    r"[\U0001F300-\U0001F5FF]"    # Misc Symbols & Pictographs
    r"|[\U0001F600-\U0001F64F]"   # Emoticons 😀
    r"|[\U0001F680-\U0001F6FF]"   # Transport & Map 🚀
    r"|[\U0001F700-\U0001F77F]"   # Alchemical
    r"|[\U0001F780-\U0001F7FF]"   # Geometric Shapes Ext
    r"|[\U0001F800-\U0001F8FF]"   # Supplemental Arrows-C
    r"|[\U0001F900-\U0001F9FF]"   # Supplemental Symbols 🧠
    r"|[\U0001FA00-\U0001FAFF]"   # Symbols Ext-A 🪐
    r"|[\U0001F1E6-\U0001F1FF]"   # Regional Indicators 🇨🇳
    r"|[\u2600-\u26FF]"           # Misc Symbols ☀ ✅ ⚠ ⚡
    r"|[\u2700-\u27BF]"           # Dingbats ✏ ✂ ✔ ✖
    r"|[\u2300-\u23FF]"           # Misc Technical ⏱ ⏰ ⌚
    r"|[\u2B00-\u2BFF]"           # Misc Symbols & Arrows
    r"|[\u3030\u303D\u3297\u3299]"  # 部分 CJK emoji
    r")"
    r"(?:\uFE0F)?"                # 变体选择符
    r"(?:"                        # 可选 ZWJ 序列（组合 emoji）
    r"\u200D"
    r"(?:[\U0001F300-\U0001F9FF]|[\u2600-\u27BF])"
    r"(?:\uFE0F)?"
    r")*"
)


def emoji(char: str) -> str:
    """把单个 emoji 包进规范化 span，用于组件内精确控制位置。"""
    return f'<span class="emoji">{char}</span>'


def normalize_emoji(html: str) -> str:
    """自动把 HTML 字符串中所有裸 emoji 包装进 <span class="emoji">。

    特性：
    - 自动跳过已包裹的 emoji，避免重复嵌套
    - 自动跳过 HTML 标签属性里的 emoji（如 title="⭐"）
    - 支持 ZWJ 组合 emoji（如 👨‍💻、🏳️‍🌈）

    推荐用法：
        body_html = assemble_body(...)
        body_html = normalize_emoji(body_html)
        HTML(string=make_html(ch, body_html)).write_pdf(path)
    或直接让 make_html(auto_normalize_emoji=True) 自动处理（默认开启）。
    """
    if not html:
        return html

    # 先把已经 wrap 过的部分占位，避免二次嵌套
    _marker_map = {}

    def _out(m):
        key = f'\x00EMOJI_SPAN_{len(_marker_map)}\x00'
        _marker_map[key] = m.group(0)
        return key

    wrapped_re = re.compile(
        r'<span\s+class="emoji"[^>]*>.*?</span>', re.DOTALL
    )
    working = wrapped_re.sub(_out, html)

    # 交替遍历 HTML 标签 / 文本节点，只在文本节点里包 emoji
    def _wrap_seg(match):
        seg = match.group(0)
        if seg.startswith('<'):
            return seg  # HTML 标签，不碰
        return _EMOJI_PATTERN.sub(
            lambda em: f'<span class="emoji">{em.group(0)}</span>',
            seg
        )

    result = re.sub(r'<[^>]+>|[^<]+', _wrap_seg, working)

    # 还原占位符
    for key, orig in _marker_map.items():
        result = result.replace(key, orig)
    return result


def strip_emoji(text: str) -> str:
    """删除字符串中所有 emoji（emoji-free 模式，用于打印机/OCR）。"""
    return _EMOJI_PATTERN.sub('', text)


# ═══════════════════════════════════════════════════════════
#  HTML 装配
# ═══════════════════════════════════════════════════════════
def make_html(chapter_title: str,
              body_html: str,
              brand: str = '课程材料',
              auto_normalize_emoji: bool = True) -> str:
    """Wrap body content in full HTML document.

    参数：
      chapter_title:          页眉显示的章节名
      body_html:              正文 HTML
      brand:                  页眉左侧品牌名（默认为"课程材料"）
      auto_normalize_emoji:   是否自动包装 emoji（默认开启，建议保持）
    """
    if auto_normalize_emoji:
        body_html = normalize_emoji(body_html)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{chapter_title} · {brand}</title>
<style>
{BASE_CSS}
{HTML_SCREEN_CSS}
</style>
</head>
<body>
<div id="page-header">
  <span class="brand">{brand}</span>
  <span class="chapter">{chapter_title}</span>
</div>
<div id="page-footer">第 </div>
<div class="page-body">
{body_html}
</div>
</body>
</html>"""


# ─── 组件构建函数 ────────────────────────────────────────────

def lesson_cover(num_cn: str, title: str, desc: str, duration: str, topics: list) -> str:
    topics_html = '  '.join(
        f'<span class="tag tag-blue">{t}</span>' for t in topics
    )
    return f"""
<div class="lesson-cover no-break">
  <div class="lesson-num">第{num_cn}课</div>
  <h1 class="lesson-title">{title}</h1>
  <p class="lesson-desc">{desc}</p>
  <div>{topics_html}</div>
  <div class="lesson-meta">
    <div class="lesson-meta-item">
      <span class="label">学习时长</span>
      <span class="value"><span class="emoji">⏱</span> {duration}</span>
    </div>
    <div class="lesson-meta-item">
      <span class="label">本课主题数</span>
      <span class="value"><span class="emoji">📚</span> {len(topics)} 个主题</span>
    </div>
  </div>
</div>"""


def h2(text: str) -> str:
    return f'<h2>{text}</h2>\n'

def h3(text: str) -> str:
    return f'<h3>{text}</h3>\n'

def p(text: str) -> str:
    return f'<p>{text}</p>\n'

def ul(items: list) -> str:
    li = ''.join(f'<li>{i}</li>' for i in items)
    return f'<ul>{li}</ul>\n'

def ol(items: list) -> str:
    li = ''.join(f'<li>{i}</li>' for i in items)
    return f'<ol>{li}</ol>\n'

def card(kind: str, title: str, body: str, icon: str = '') -> str:
    # icon 走 class="emoji" 通道，保证行高一致、不撑破标题
    icon_html = f'<span class="emoji">{icon}</span>' if icon else ''
    return f"""
<div class="card card-{kind} no-break">
  <div class="card-title">{icon_html}{title}</div>
  <div class="card-body">{body}</div>
</div>"""

def card_key(title: str, body: str)      -> str: return card('key',      title, body, '📌')
def card_tip(title: str, body: str)      -> str: return card('tip',      title, body, '💡')
def card_good(label: str, body: str)     -> str: return card('good',     label, body, '✅')
def card_bad(label: str, body: str)      -> str: return card('bad',      label, body, '❌')
def card_exercise(num, question: str)    -> str: return card('exercise', f'练习题 {num}', question, '✏️')
def card_answer(num, answer: str)        -> str: return card('answer',   f'练习题 {num} — 参考答案', answer, '✅')
def card_advanced(title: str, body: str) -> str: return card('advanced', title, body, '⚡')

def compare(bad_title: str, bad_body: str, good_title: str, good_body: str) -> str:
    bad_html  = bad_body.replace('\n', '<br>')
    good_html = good_body.replace('\n', '<br>')
    return f"""
<table class="compare-table no-break">
  <thead>
    <tr>
      <th class="bad-col"><span class="emoji">❌</span> {bad_title}</th>
      <th class="good-col"><span class="emoji">✅</span> {good_title}</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="bad-cell">{bad_html}</td>
      <td class="good-cell">{good_html}</td>
    </tr>
  </tbody>
</table>"""

def prompt_block(body: str, label: str = '提示词示例') -> str:
    body_safe = body.replace('<', '&lt;').replace('>', '&gt;')
    return f"""
<div class="prompt-block no-break">
  <div class="prompt-header"><span class="emoji">✦</span> {label}</div>
  <div class="prompt-body">{body_safe}</div>
</div>"""

def data_table(headers: list, rows: list, col_widths: list = None) -> str:
    width_attrs = ''
    if col_widths:
        colgroup = '<colgroup>' + ''.join(
            f'<col style="width:{w}">' for w in col_widths
        ) + '</colgroup>'
    else:
        colgroup = ''
    th_html = ''.join(f'<th>{h}</th>' for h in headers)
    rows_html = ''
    for row in rows:
        td_html = ''.join(f'<td>{c}</td>' for c in row)
        rows_html += f'<tr>{td_html}</tr>'
    return f"""
<table class="data-table no-break">
  {colgroup}
  <thead><tr>{th_html}</tr></thead>
  <tbody>{rows_html}</tbody>
</table>"""

def hr_section() -> str:
    return '<hr class="section-divider">\n'

def page_break() -> str:
    return '<div class="page-break"></div>\n'


# ═══════════════════════════════════════════════════════════
#  多格式输出（PDF 默认；HTML / DOCX / Markdown 可选）
# ═══════════════════════════════════════════════════════════
# 约定：
# - basename = 无扩展名的文件名（如 "01_第一课_认识AI"）
# - out_dir  = 输出目录
# - chapter  = 页眉/标题用的章节名
# - body     = HTML 主体
#
# 推荐入口 write_course(out_dir, basename, chapter, body, formats=['pdf'])
# 按 formats 选项分发到对应的 write_* 函数。

SUPPORTED_FORMATS = ('pdf', 'html', 'docx', 'md')


def _safe_basename(name: str) -> str:
    """清理文件名中会导致系统无法识别的字符（全角括号、特殊符号）。"""
    # 只保留：数字/字母/下划线/点号/中文汉字/减号
    return re.sub(r'[^0-9A-Za-z_\-.\u4e00-\u9fff]', '_', name)


def write_pdf(out_dir: str, basename: str, chapter: str, body: str,
              brand: str = '课程材料') -> str:
    """生成 PDF（使用 WeasyPrint）。"""
    from weasyprint import HTML  # 延迟 import，其他输出格式下无需安装
    basename = _safe_basename(basename)
    path = os.path.join(out_dir, f'{basename}.pdf')
    html_str = make_html(chapter, body, brand=brand)
    HTML(string=html_str).write_pdf(path)
    size_kb = os.path.getsize(path) // 1024
    print(f'  ✅ PDF    {basename}.pdf  ({size_kb} KB)')
    return path


def write_html(out_dir: str, basename: str, chapter: str, body: str,
               brand: str = '课程材料') -> str:
    """生成独立 HTML 文件（单文件、内联 CSS，可直接在浏览器打开）。"""
    basename = _safe_basename(basename)
    path = os.path.join(out_dir, f'{basename}.html')
    html_str = make_html(chapter, body, brand=brand)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html_str)
    size_kb = os.path.getsize(path) // 1024
    print(f'  ✅ HTML   {basename}.html  ({size_kb} KB)')
    return path


def write_docx(out_dir: str, basename: str, chapter: str, body: str,
               brand: str = '课程材料') -> str:
    """生成 Word DOCX。

    优先使用 pandoc（最稳定，保留丰富格式）；
    如果 pandoc 不可用，回退到 python-docx 的简化版（仅保留文字层级）。
    """
    basename = _safe_basename(basename)
    path = os.path.join(out_dir, f'{basename}.docx')
    html_str = make_html(chapter, body, brand=brand)

    # 优先 pandoc
    if _has_pandoc():
        tmp_html = os.path.join(out_dir, f'.{basename}.tmp.html')
        with open(tmp_html, 'w', encoding='utf-8') as f:
            f.write(html_str)
        try:
            subprocess.run(
                ['pandoc', tmp_html, '-f', 'html', '-t', 'docx',
                 '-o', path, '--standalone'],
                check=True, capture_output=True
            )
        finally:
            if os.path.exists(tmp_html):
                os.remove(tmp_html)
    else:
        # 回退：html2docx（若可用）/ 简化转换
        try:
            from html2docx import html2docx  # type: ignore
            buf = html2docx(html_str, title=chapter)
            with open(path, 'wb') as f:
                f.write(buf.getvalue())
        except ImportError:
            raise RuntimeError(
                'DOCX 输出需要 pandoc（推荐）或 html2docx 库。\n'
                '安装方式：\n'
                '  brew install pandoc                # macOS\n'
                '  apt install pandoc                 # Linux\n'
                '  pip install html2docx --break-system-packages'
            )
    size_kb = os.path.getsize(path) // 1024
    print(f'  ✅ DOCX   {basename}.docx  ({size_kb} KB)')
    return path


def write_markdown(out_dir: str, basename: str, chapter: str, body: str,
                   brand: str = '课程材料') -> str:
    """生成 Markdown。

    优先用 pandoc（保留标题层级/表格）；否则用 html2text 库；
    都不可用时做简化正则转换（仅保留文本和一级标题）。
    """
    basename = _safe_basename(basename)
    path = os.path.join(out_dir, f'{basename}.md')
    html_str = make_html(chapter, body, brand=brand,
                         auto_normalize_emoji=False)

    md_text = None
    if _has_pandoc():
        tmp_html = os.path.join(out_dir, f'.{basename}.tmp.html')
        with open(tmp_html, 'w', encoding='utf-8') as f:
            f.write(html_str)
        try:
            result = subprocess.run(
                ['pandoc', tmp_html, '-f', 'html', '-t',
                 'gfm',  # GitHub-flavored Markdown
                 '--wrap=none'],
                check=True, capture_output=True, text=True
            )
            md_text = result.stdout
        finally:
            if os.path.exists(tmp_html):
                os.remove(tmp_html)
    else:
        try:
            import html2text  # type: ignore
            h = html2text.HTML2Text()
            h.body_width = 0  # 不自动换行
            h.ignore_images = False
            md_text = h.handle(html_str)
        except ImportError:
            md_text = _html_to_markdown_fallback(html_str)

    # 在顶部补一个 h1 标题（pandoc 版本常丢失）
    if md_text and not md_text.lstrip().startswith('#'):
        md_text = f'# {chapter}\n\n{md_text}'

    with open(path, 'w', encoding='utf-8') as f:
        f.write(md_text)
    size_kb = max(1, os.path.getsize(path) // 1024)
    print(f'  ✅ MD     {basename}.md  ({size_kb} KB)')
    return path


def write_course(out_dir: str, basename: str, chapter: str, body: str,
                 formats=('pdf',), brand: str = '课程材料') -> dict:
    """多格式统一入口。

    示例：
      write_course(
          out_dir='./out',
          basename='01_第一课_认识AI',
          chapter='第一课',
          body=my_body_html,
          formats=['pdf', 'html'],
      )

    返回：{'pdf': path, 'html': path, ...}
    """
    os.makedirs(out_dir, exist_ok=True)
    dispatch = {
        'pdf':  write_pdf,
        'html': write_html,
        'docx': write_docx,
        'md':   write_markdown,
    }
    results = {}
    for fmt in formats:
        fmt = fmt.lower().lstrip('.')
        if fmt not in dispatch:
            raise ValueError(
                f'不支持的输出格式: {fmt}。支持: {SUPPORTED_FORMATS}'
            )
        results[fmt] = dispatch[fmt](out_dir, basename, chapter, body, brand)
    return results


# ─── 内部工具 ────────────────────────────────────────────
def _has_pandoc() -> bool:
    """检测 pandoc 是否可用。"""
    try:
        subprocess.run(['pandoc', '--version'],
                       capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def _html_to_markdown_fallback(html: str) -> str:
    """极简 HTML→MD 转换（pandoc 和 html2text 都不可用时的兜底）。

    只处理最基本的标签，保证文本层级可读。复杂表格/卡片降级为普通段落。
    """
    text = html
    # 删除 style/script
    text = re.sub(r'<style[^>]*>.*?</style>', '', text,
                  flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<script[^>]*>.*?</script>', '', text,
                  flags=re.DOTALL | re.IGNORECASE)
    # 标题
    text = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n# \1\n', text,
                  flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', text,
                  flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', text,
                  flags=re.DOTALL | re.IGNORECASE)
    # 强调
    text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', text,
                  flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', text,
                  flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', text,
                  flags=re.DOTALL | re.IGNORECASE)
    # 段落和换行
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</p>', '\n\n', text, flags=re.IGNORECASE)
    # 列表
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'- \1\n', text,
                  flags=re.DOTALL | re.IGNORECASE)
    # 删掉所有剩余的 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)
    # 压缩空白
    text = re.sub(r'\n{3,}', '\n\n', text)
    # HTML 实体
    text = text.replace('&lt;', '<').replace('&gt;', '>')
    text = text.replace('&amp;', '&').replace('&nbsp;', ' ')
    return text.strip()
