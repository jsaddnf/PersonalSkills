#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设计系统 — 提示词工程实战课
字体：Noto Sans CJK SC（苹方同级无衬线字体）
渲染：WeasyPrint (HTML → PDF)
"""

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

/* ── 字体设置 ── */
body {
    font-family: 'Noto Sans CJK SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    font-size: 10.5pt;
    line-height: 1.85;
    color: %(text)s;
    font-weight: 400;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
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
    font-family: 'Noto Sans CJK SC', 'PingFang SC', sans-serif;
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
    font-family: 'Noto Sans Mono CJK SC', monospace;
    font-size: 9.5pt;
    background: %(code_bg)s;
    color: %(code_text)s;
    padding: 1pt 4pt;
    border-radius: 3px;
}
""" % COLORS


def make_html(chapter_title: str, body_html: str) -> str:
    """Wrap body content in full HTML document."""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
{BASE_CSS}
</style>
</head>
<body>
<div id="page-header">
  <span class="brand">提示词工程实战课</span>
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
      <span class="value">⏱ {duration}</span>
    </div>
    <div class="lesson-meta-item">
      <span class="label">本课主题数</span>
      <span class="value">📚 {len(topics)} 个主题</span>
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
    icon_html = f'<span>{icon}</span>' if icon else ''
    return f"""
<div class="card card-{kind} no-break">
  <div class="card-title">{icon_html}{title}</div>
  <div class="card-body">{body}</div>
</div>"""

def card_key(title: str, body: str)      -> str: return card('key',      title, body, '📌')
def card_tip(title: str, body: str)      -> str: return card('tip',      title, body, '💡')
def card_good(label: str, body: str)     -> str: return card('good',     f'✅ {label}', body)
def card_bad(label: str, body: str)      -> str: return card('bad',      f'❌ {label}', body)
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
      <th class="bad-col">❌ {bad_title}</th>
      <th class="good-col">✅ {good_title}</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td class="bad-cell">{bad_html}</td>
      <td class="good-cell">{good_html}</td>
    </tr>
  </tbody>
</table>"""

def prompt_block(body: str) -> str:
    body_safe = body.replace('<', '&lt;').replace('>', '&gt;')
    return f"""
<div class="prompt-block no-break">
  <div class="prompt-header">✦ 提示词示例</div>
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
