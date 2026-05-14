"""
《血糖友好》家庭健康手册 - 杂志风格设计系统
- 尺寸：A5 (148×210mm) 竖向
- 字体：PingFang SC (苹方简体) 首选
- 配色：暖橙 + 温柔绿 + 米白（摆脱医院冰冷感）
- 字号：13pt 正文（老花眼友好）
"""
import re

COLORS = {
    'bg':          '#FAF7F2',
    'paper':       '#FFFFFF',
    'text':        '#2C2C2C',
    'text_soft':   '#5A5A5A',
    'text_mute':   '#8E8E8E',
    'line':        '#E6DFD3',
    'line_soft':   '#F0EAE0',

    'green':       '#2D8659',
    'green_bg':    '#E8F2EC',
    'orange':      '#E89B3C',
    'orange_bg':   '#FBEFDC',
    'sky':         '#4A90A4',
    'sky_bg':      '#E4EEF1',
    'purple':      '#8E6BAA',
    'purple_bg':   '#EDE6F4',
    'berry':       '#B85563',
    'berry_bg':    '#F5E3E6',
    'leaf':        '#6B8E3D',
    'leaf_bg':     '#EDF1E2',
    'pine':        '#1F6650',
    'pine_bg':     '#DCE9E3',
    'brick':       '#C84135',
    'brick_bg':    '#F5DDDB',

    'yellow_bg':   '#FBF3D9',
    'warn':        '#D97706',
    'danger':      '#C84135',
}

COLUMN_THEMES = {
    1: {'name': '认识血糖',      'color': COLORS['green'],  'bg': COLORS['green_bg'],  'icon': '🍃'},
    2: {'name': '餐桌',         'color': COLORS['orange'], 'bg': COLORS['orange_bg'], 'icon': '🍽'},
    3: {'name': '动一动',       'color': COLORS['leaf'],   'bg': COLORS['leaf_bg'],   'icon': '🚶'},
    4: {'name': '看懂数字',     'color': COLORS['sky'],    'bg': COLORS['sky_bg'],    'icon': '📊'},
    5: {'name': '药与针',       'color': COLORS['berry'],  'bg': COLORS['berry_bg'],  'icon': '💊'},
    6: {'name': '看不见的影响', 'color': COLORS['purple'], 'bg': COLORS['purple_bg'], 'icon': '🌙'},
    7: {'name': '守护未来',     'color': COLORS['pine'],   'bg': COLORS['pine_bg'],   'icon': '🛡'},
    8: {'name': '辟谣实验室',   'color': COLORS['brick'],  'bg': COLORS['brick_bg'],  'icon': '🔍'},
}

BASE_CSS = f"""
@page {{
    size: 148mm 210mm;
    margin: 14mm 13mm 14mm 13mm;
    background: {COLORS['bg']};
    @bottom-center {{
        content: counter(page);
        font-family: 'PingFang SC', 'Hiragino Sans GB', sans-serif;
        font-size: 9pt;
        color: {COLORS['text_mute']};
        margin-bottom: 4mm;
    }}
}}
@page :first {{
    margin: 0;
    @bottom-center {{ content: none; }}
}}
@page cover {{ margin: 0; @bottom-center {{ content: none; }} }}
@page column-cover {{ margin: 0; @bottom-center {{ content: none; }} }}
@page plain {{ @bottom-center {{ content: none; }} }}

* {{ box-sizing: border-box; }}

html, body {{
    margin: 0;
    padding: 0;
    background: {COLORS['bg']};
    font-family: 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei',
                 'Noto Sans CJK SC', sans-serif;
    font-size: 13pt;
    line-height: 1.95;
    color: {COLORS['text']};
    text-rendering: optimizeLegibility;
    -webkit-font-smoothing: antialiased;
}}

p {{
    margin: 0 0 12pt 0;
    text-align: justify;
    word-break: break-word;
    hanging-punctuation: allow-end;
}}

h2, h3, h4 {{
    font-weight: 600;
    color: {COLORS['text']};
    line-height: 1.4;
}}
h2 {{ font-size: 22pt; margin: 18pt 0 14pt 0; }}
h3 {{ font-size: 16pt; margin: 16pt 0 8pt 0; }}
h4 {{ font-size: 13.5pt; margin: 12pt 0 6pt 0; }}

ul, ol {{ margin: 8pt 0 12pt 0; padding-left: 20pt; }}
li {{ margin: 4pt 0; line-height: 1.85; }}

strong {{ font-weight: 600; color: {COLORS['text']}; }}
em {{ font-style: italic; color: {COLORS['text_soft']}; }}

.page-break {{ page-break-before: always; }}
.no-break   {{ page-break-inside: avoid; }}
.cover-page    {{ page: cover; page-break-after: always; }}
.col-cover     {{ page: column-cover; page-break-after: always; }}
.plain-page    {{ page: plain; page-break-after: always; }}

.emoji {{
    font-family: 'Apple Color Emoji', 'Segoe UI Emoji', 'Noto Color Emoji',
                 'Twemoji Mozilla', 'PingFang SC', 'Hiragino Sans GB', sans-serif;
    font-size: 0.95em;
    font-style: normal;
    font-weight: 400;
    line-height: 1;
    vertical-align: -0.08em;
    display: inline-block;
    white-space: nowrap;
    word-break: keep-all;
}}

/* ===== 杂志封面 ===== */
.mag-cover {{
    width: 148mm; height: 210mm;
    background: linear-gradient(165deg, #2D8659 0%, #1F6650 60%, #154836 100%);
    color: white;
    padding: 18mm 14mm;
    position: relative;
    overflow: hidden;
}}
.mag-cover::before {{
    content: '';
    position: absolute;
    top: -40mm; right: -40mm;
    width: 110mm; height: 110mm;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(232,155,60,0.35) 0%, transparent 70%);
}}
.mag-cover::after {{
    content: '';
    position: absolute;
    bottom: -30mm; left: -30mm;
    width: 90mm; height: 90mm;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,255,255,0.10) 0%, transparent 70%);
}}
.mag-meta {{
    font-size: 9pt;
    letter-spacing: 4pt;
    opacity: 0.85;
    text-transform: uppercase;
    position: relative; z-index: 2;
}}
.mag-issue {{
    font-size: 8.5pt;
    letter-spacing: 2pt;
    opacity: 0.7;
    margin-top: 4mm;
    position: relative; z-index: 2;
}}
.mag-title {{
    font-size: 50pt;
    font-weight: 700;
    line-height: 1.05;
    margin-top: 18mm;
    letter-spacing: 2pt;
    position: relative; z-index: 2;
}}
.mag-sub {{
    font-size: 14pt;
    font-weight: 300;
    line-height: 1.6;
    margin-top: 8mm;
    opacity: 0.92;
    position: relative; z-index: 2;
}}
.mag-divider {{
    width: 30mm; height: 2pt;
    background: #E89B3C;
    margin: 14mm 0;
    position: relative; z-index: 2;
}}
.mag-features {{
    position: relative; z-index: 2;
}}
.mag-features-title {{
    font-size: 9pt;
    letter-spacing: 3pt;
    opacity: 0.7;
    margin-bottom: 4mm;
}}
.mag-features ul {{
    margin: 0; padding: 0; list-style: none;
}}
.mag-features li {{
    font-size: 11.5pt;
    line-height: 1.7;
    padding-left: 16pt;
    position: relative;
    margin: 3mm 0;
    color: rgba(255,255,255,0.95);
}}
.mag-features li::before {{
    content: '';
    position: absolute;
    left: 0; top: 9pt;
    width: 8pt; height: 1.5pt;
    background: #E89B3C;
}}
.mag-author {{
    position: absolute;
    bottom: 16mm; left: 14mm; right: 14mm;
    z-index: 2;
    font-size: 10pt;
    letter-spacing: 1pt;
    opacity: 0.88;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
}}
.mag-author-l {{ }}
.mag-author-r {{ text-align: right; font-size: 8.5pt; opacity: 0.75; }}

/* ===== 版权页 ===== */
.copyright-page {{
    padding-top: 70mm;
    text-align: center;
}}
.copyright-page .title {{
    font-size: 14pt; color: {COLORS['text_soft']};
    letter-spacing: 4pt; margin-bottom: 14mm;
}}
.copyright-page p {{
    text-align: center;
    font-size: 10.5pt;
    color: {COLORS['text_soft']};
    margin: 4pt 0;
}}
.copyright-page .line {{
    width: 18mm; height: 1pt; background: {COLORS['line']};
    margin: 10mm auto;
}}
.copyright-page .notice {{
    margin-top: 20mm;
    font-size: 9.5pt;
    color: {COLORS['text_mute']};
    line-height: 1.9;
    padding: 0 12mm;
}}

/* ===== 目录页 ===== */
.toc h2 {{
    font-size: 28pt;
    color: {COLORS['text']};
    margin: 0 0 2mm 0;
    letter-spacing: 1pt;
}}
.toc .sub {{
    font-size: 10pt;
    color: {COLORS['text_mute']};
    letter-spacing: 3pt;
    margin-bottom: 10mm;
    text-transform: uppercase;
}}
.toc-item {{
    display: flex;
    align-items: baseline;
    padding: 5mm 0;
    border-bottom: 1pt dotted {COLORS['line']};
}}
.toc-num {{
    font-size: 16pt;
    font-weight: 600;
    width: 14mm;
    color: {COLORS['orange']};
    font-family: Georgia, serif;
}}
.toc-text {{
    flex: 1;
    font-size: 12pt;
    color: {COLORS['text']};
}}
.toc-text .sub {{
    font-size: 9.5pt;
    color: {COLORS['text_mute']};
    margin-top: 1mm;
    letter-spacing: 0;
    text-transform: none;
}}
.toc-page {{
    font-size: 11pt;
    color: {COLORS['text_soft']};
    font-family: Georgia, serif;
}}

/* ===== 卷首语 ===== */
.editorial-tag {{
    font-size: 9pt;
    letter-spacing: 4pt;
    color: {COLORS['orange']};
    margin-bottom: 4mm;
    text-transform: uppercase;
}}
.editorial-title {{
    font-size: 26pt;
    line-height: 1.3;
    font-weight: 600;
    color: {COLORS['text']};
    margin: 0 0 8mm 0;
}}
.editorial-body p {{
    font-size: 12.5pt;
    line-height: 2.0;
    color: {COLORS['text']};
    text-indent: 2em;
}}
.editorial-body p.lead {{
    font-size: 14pt;
    line-height: 1.85;
    color: {COLORS['text']};
    font-weight: 500;
    text-indent: 0;
    border-left: 3pt solid {COLORS['orange']};
    padding-left: 10pt;
    margin: 8mm 0;
}}
.signature {{
    margin-top: 14mm;
    text-align: right;
    font-size: 12pt;
    color: {COLORS['text_soft']};
}}
.signature .name {{
    font-size: 14pt;
    color: {COLORS['text']};
    font-weight: 500;
    letter-spacing: 1pt;
}}
.signature .date {{
    font-size: 10pt;
    color: {COLORS['text_mute']};
    margin-top: 1mm;
}}

/* ===== 专栏封面页 ===== */
.col-cover-inner {{
    width: 148mm; height: 210mm;
    padding: 28mm 16mm;
    position: relative;
    color: white;
}}
.col-num {{
    font-family: Georgia, serif;
    font-size: 90pt;
    line-height: 1;
    opacity: 0.18;
    font-weight: 400;
}}
.col-tag {{
    font-size: 9.5pt;
    letter-spacing: 5pt;
    margin-top: 6mm;
    opacity: 0.85;
}}
.col-title {{
    font-size: 38pt;
    font-weight: 600;
    line-height: 1.2;
    margin-top: 6mm;
    letter-spacing: 1pt;
}}
.col-lead {{
    font-size: 13pt;
    line-height: 1.85;
    margin-top: 14mm;
    opacity: 0.92;
    max-width: 100mm;
}}
.col-icon {{
    position: absolute;
    right: 16mm; bottom: 22mm;
    font-size: 80pt;
    opacity: 0.35;
}}

/* ===== 内容页：专栏内 ===== */
.col-h-tag {{
    font-size: 9pt;
    letter-spacing: 4pt;
    color: var(--theme, {COLORS['green']});
    text-transform: uppercase;
    margin-bottom: 2mm;
}}
.col-h2 {{
    font-size: 21pt;
    font-weight: 600;
    line-height: 1.35;
    color: {COLORS['text']};
    margin: 0 0 8mm 0;
    padding-bottom: 3mm;
    border-bottom: 2pt solid var(--theme, {COLORS['green']});
}}
.col-h3 {{
    font-size: 15pt;
    font-weight: 600;
    color: var(--theme, {COLORS['green']});
    margin: 8mm 0 3mm 0;
}}

.lead-p {{
    font-size: 14pt;
    line-height: 1.85;
    color: {COLORS['text']};
    font-weight: 500;
    margin: 0 0 6mm 0;
    padding: 4mm 0;
    border-top: 1pt solid {COLORS['line']};
    border-bottom: 1pt solid {COLORS['line']};
    text-align: left;
    text-indent: 0;
}}

.pull-quote {{
    font-size: 19pt;
    line-height: 1.55;
    font-weight: 600;
    color: var(--theme, {COLORS['green']});
    text-align: center;
    margin: 10mm 4mm;
    padding: 5mm 0;
    position: relative;
}}
.pull-quote::before, .pull-quote::after {{
    content: '';
    display: block;
    width: 12mm; height: 1.5pt;
    background: var(--theme, {COLORS['green']});
    margin: 4mm auto;
    opacity: 0.6;
}}

.big-number {{
    text-align: center;
    margin: 8mm 0;
    padding: 6mm 4mm;
    background: var(--theme-bg, {COLORS['green_bg']});
    border-radius: 4pt;
}}
.big-number .num {{
    font-size: 56pt;
    font-weight: 700;
    line-height: 1;
    color: var(--theme, {COLORS['green']});
    font-family: Georgia, serif;
    letter-spacing: -2pt;
}}
.big-number .unit {{
    font-size: 14pt;
    color: var(--theme, {COLORS['green']});
    margin-left: 4pt;
}}
.big-number .label {{
    font-size: 11pt;
    color: {COLORS['text_soft']};
    margin-top: 3mm;
    line-height: 1.6;
}}

.info-card {{
    background: var(--theme-bg, {COLORS['green_bg']});
    border-radius: 6pt;
    padding: 5mm 6mm;
    margin: 5mm 0;
    page-break-inside: avoid;
}}
.info-card .ic-title {{
    font-size: 12pt;
    font-weight: 600;
    color: var(--theme, {COLORS['green']});
    margin-bottom: 3mm;
}}
.info-card p {{
    margin: 0 0 4pt 0;
    font-size: 12pt;
    line-height: 1.85;
    text-align: left;
}}
.info-card p:last-child {{ margin-bottom: 0; }}

.tip-box {{
    background: {COLORS['yellow_bg']};
    border-left: 3pt solid {COLORS['warn']};
    border-radius: 0 4pt 4pt 0;
    padding: 4mm 5mm;
    margin: 5mm 0;
    page-break-inside: avoid;
}}
.tip-box .tip-title {{
    font-size: 11pt;
    font-weight: 600;
    color: {COLORS['warn']};
    margin-bottom: 2mm;
}}
.tip-box p {{
    margin: 0;
    font-size: 11.5pt;
    line-height: 1.8;
    color: {COLORS['text']};
}}

.danger-box {{
    background: {COLORS['brick_bg']};
    border-left: 3pt solid {COLORS['danger']};
    border-radius: 0 4pt 4pt 0;
    padding: 4mm 5mm;
    margin: 5mm 0;
    page-break-inside: avoid;
}}
.danger-box .tip-title {{
    font-size: 11pt;
    font-weight: 600;
    color: {COLORS['danger']};
    margin-bottom: 2mm;
}}

.story-card {{
    background: {COLORS['paper']};
    border: 1pt solid {COLORS['line']};
    border-radius: 6pt;
    padding: 5mm 6mm;
    margin: 6mm 0;
    page-break-inside: avoid;
    position: relative;
}}
.story-card .story-tag {{
    display: inline-block;
    font-size: 9pt;
    letter-spacing: 2pt;
    color: var(--theme, {COLORS['green']});
    background: var(--theme-bg, {COLORS['green_bg']});
    padding: 1mm 3mm;
    border-radius: 2pt;
    margin-bottom: 3mm;
}}
.story-card p {{
    font-size: 11.5pt;
    line-height: 1.85;
    margin: 0 0 3pt 0;
    color: {COLORS['text']};
}}
.story-card p:last-child {{ margin-bottom: 0; }}

.compare-table {{
    display: flex;
    gap: 3mm;
    margin: 6mm 0;
    page-break-inside: avoid;
}}
.compare-col {{
    flex: 1;
    padding: 4mm 4mm;
    border-radius: 5pt;
    font-size: 11pt;
    line-height: 1.75;
}}
.compare-col.good {{
    background: {COLORS['green_bg']};
    border-left: 3pt solid {COLORS['green']};
}}
.compare-col.bad {{
    background: {COLORS['brick_bg']};
    border-left: 3pt solid {COLORS['danger']};
}}
.compare-head {{
    font-size: 11.5pt;
    font-weight: 600;
    margin-bottom: 2mm;
}}
.compare-col.good .compare-head {{ color: {COLORS['green']}; }}
.compare-col.bad  .compare-head {{ color: {COLORS['danger']}; }}

.data-row {{
    display: flex;
    padding: 3mm 0;
    border-bottom: 1pt solid {COLORS['line_soft']};
    font-size: 11.5pt;
}}
.data-row:last-child {{ border-bottom: none; }}
.data-label {{
    width: 38mm;
    color: {COLORS['text_soft']};
    font-weight: 500;
}}
.data-value {{
    flex: 1;
    color: {COLORS['text']};
}}
.data-value strong {{ color: var(--theme, {COLORS['green']}); }}

/* 自评题 */
.assess-intro {{
    background: {COLORS['orange_bg']};
    border-radius: 8pt;
    padding: 6mm 6mm;
    margin: 4mm 0 8mm 0;
}}
.assess-intro .label {{
    font-size: 9pt;
    letter-spacing: 4pt;
    color: {COLORS['orange']};
    margin-bottom: 2mm;
}}
.assess-intro h3 {{
    margin: 0 0 3mm 0;
    color: {COLORS['text']};
    font-size: 18pt;
}}
.assess-intro p {{
    margin: 0;
    font-size: 11.5pt;
    color: {COLORS['text_soft']};
    line-height: 1.75;
}}

.q-item {{
    margin: 6mm 0;
    padding: 4mm 5mm;
    background: {COLORS['paper']};
    border: 1pt solid {COLORS['line']};
    border-radius: 5pt;
    page-break-inside: avoid;
}}
.q-num {{
    display: inline-block;
    width: 8mm; height: 8mm;
    line-height: 8mm;
    text-align: center;
    background: {COLORS['orange']};
    color: white;
    border-radius: 50%;
    font-weight: 600;
    font-size: 11pt;
    margin-right: 3mm;
}}
.q-text {{
    font-size: 12.5pt;
    font-weight: 500;
    line-height: 1.6;
    color: {COLORS['text']};
    margin-bottom: 3mm;
    display: inline;
}}
.q-options {{
    margin-top: 3mm;
    padding-left: 11mm;
}}
.q-options .opt {{
    font-size: 11.5pt;
    line-height: 1.95;
    color: {COLORS['text']};
}}
.q-options .opt .box {{
    display: inline-block;
    width: 9pt; height: 9pt;
    border: 1pt solid {COLORS['text_soft']};
    border-radius: 1.5pt;
    margin-right: 4pt;
    vertical-align: -1pt;
}}
.q-options .opt .pts {{
    color: {COLORS['orange']};
    font-size: 10pt;
    margin-left: 4pt;
    font-weight: 500;
}}

.scoring {{
    margin-top: 8mm;
    background: {COLORS['green_bg']};
    border-radius: 6pt;
    padding: 5mm 6mm;
}}
.scoring h4 {{
    margin: 0 0 4mm 0;
    color: {COLORS['green']};
    font-size: 13pt;
}}
.score-row {{
    display: flex;
    padding: 2mm 0;
    font-size: 11pt;
    line-height: 1.7;
}}
.score-row .range {{
    width: 18mm;
    font-weight: 600;
    color: {COLORS['green']};
}}
.score-row .desc {{ flex: 1; color: {COLORS['text']}; }}

.divider-soft {{
    width: 24mm;
    height: 1pt;
    background: {COLORS['line']};
    margin: 8mm auto;
}}

/* 思考题 */
.thinking-box {{
    background: linear-gradient(135deg, {COLORS['orange_bg']} 0%, {COLORS['yellow_bg']} 100%);
    border-radius: 8pt;
    padding: 6mm 6mm;
    margin: 8mm 0 0 0;
    page-break-inside: avoid;
}}
.thinking-box .label {{
    font-size: 9pt;
    letter-spacing: 4pt;
    color: {COLORS['orange']};
    margin-bottom: 2mm;
}}
.thinking-box .q {{
    font-size: 13pt;
    line-height: 1.7;
    color: {COLORS['text']};
    font-weight: 500;
    margin: 0 0 3mm 0;
}}
.thinking-box .hint {{
    font-size: 11pt;
    color: {COLORS['text_soft']};
    line-height: 1.7;
    margin: 0;
    padding-top: 3mm;
    border-top: 1pt dotted {COLORS['line']};
    font-style: italic;
}}
"""


_EMOJI_CHARS = (
    '\U0001F300-\U0001F5FF'
    '\U0001F600-\U0001F64F'
    '\U0001F680-\U0001F6FF'
    '\U0001F900-\U0001F9FF'
    '\U0001FA00-\U0001FAFF'
    '\U0001F100-\U0001F1FF'
    '\U00002600-\U000026FF'
    '\U00002700-\U000027BF'
)
_EMOJI_PATTERN = re.compile(
    rf'(?<!class="emoji">)([{_EMOJI_CHARS}]+[\uFE0F\u200D\u20E3]*)+',
    re.UNICODE,
)

def normalize_emoji(html: str) -> str:
    """将裸 emoji 包裹为 <span class='emoji'>，只匹配真正的 emoji 码点，
    不包括通用标点(——……""等)、几何形状、箭头等会被误判的区段。"""
    return _EMOJI_PATTERN.sub(lambda m: f'<span class="emoji">{m.group(0)}</span>', html)


def html_doc(body: str, extra_css: str = '') -> str:
    """组装完整 HTML 文档。"""
    body = normalize_emoji(body)
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>血糖友好</title>
<style>{BASE_CSS}
{extra_css}
</style>
</head>
<body>
{body}
</body>
</html>"""


# =========== 组件 ===========

def mag_cover(title: str, sub: str, features: list, author: str, publisher: str,
              issue: str = '创刊号 · 2026') -> str:
    feat_html = '\n'.join(f'<li>{f}</li>' for f in features)
    return f"""
<div class="mag-cover cover-page">
  <div class="mag-meta">FAMILY HEALTH HANDBOOK</div>
  <div class="mag-issue">{issue}</div>
  <div class="mag-title">{title}</div>
  <div class="mag-sub">{sub}</div>
  <div class="mag-divider"></div>
  <div class="mag-features">
    <div class="mag-features-title">本期看点 · IN THIS ISSUE</div>
    <ul>{feat_html}</ul>
  </div>
  <div class="mag-author">
    <div class="mag-author-l">作者　{author}</div>
    <div class="mag-author-r">出品<br>{publisher}</div>
  </div>
</div>
"""


def copyright_page(title: str, author: str, publisher: str,
                   year: str = '2026', notice: str = '') -> str:
    return f"""
<div class="plain-page">
  <div class="copyright-page">
    <div class="title">版　权　声　明</div>
    <p><strong>《{title}》</strong></p>
    <div class="line"></div>
    <p>作者　{author}</p>
    <p>出品　{publisher}</p>
    <p>版本　{year} · 创刊号</p>
    <div class="line"></div>
    <p>© {year} {author}　保留所有权利</p>
    <p>未经授权，禁止以任何形式复制、改编或商用</p>
    <div class="notice">{notice}</div>
  </div>
</div>
"""


def toc_page(items: list) -> str:
    """items: [(num, title, sub, page)]"""
    rows = []
    for num, title, sub, page in items:
        sub_html = f'<div class="sub">{sub}</div>' if sub else ''
        rows.append(f"""
        <div class="toc-item">
          <div class="toc-num">{num}</div>
          <div class="toc-text">{title}{sub_html}</div>
          <div class="toc-page">{page}</div>
        </div>""")
    return f"""
<div class="plain-page toc">
  <h2>目　录</h2>
  <div class="sub">CONTENTS</div>
  {''.join(rows)}
</div>
"""


def editorial_page(tag: str, title: str, paragraphs: list,
                   lead: str = '', signature: str = '', date: str = '') -> str:
    lead_html = f'<p class="lead">{lead}</p>' if lead else ''
    paras_html = '\n'.join(f'<p>{p}</p>' for p in paragraphs)
    sig_html = ''
    if signature:
        date_html = f'<div class="date">{date}</div>' if date else ''
        sig_html = f"""
    <div class="signature">
      ——<span class="name">{signature}</span>
      {date_html}
    </div>"""
    return f"""
<div class="plain-page">
  <div class="editorial-tag">{tag}</div>
  <h2 class="editorial-title">{title}</h2>
  <div class="editorial-body">
    {lead_html}
    {paras_html}
    {sig_html}
  </div>
</div>
"""


def column_cover(num: int, title: str, lead: str) -> str:
    theme = COLUMN_THEMES[num]
    color = theme['color']
    icon = theme['icon']
    return f"""
<div class="col-cover" style="background:{color}">
  <div class="col-cover-inner">
    <div class="col-num">0{num}</div>
    <div class="col-tag">COLUMN · {theme['name'].upper()}</div>
    <div class="col-title">{title}</div>
    <div class="col-lead">{lead}</div>
    <div class="col-icon">{icon}</div>
  </div>
</div>
"""


def col_page_open(num: int, h2: str, tag: str = '') -> str:
    """开始一个专栏内的章节页"""
    theme = COLUMN_THEMES[num]
    style = f'--theme:{theme["color"]};--theme-bg:{theme["bg"]}'
    tag_html = f'<div class="col-h-tag">{tag}</div>' if tag else ''
    return f"""
<div class="page-break" style="{style}">
  {tag_html}
  <h2 class="col-h2">{h2}</h2>
"""


def col_page_continue(num: int) -> str:
    """专栏内续页（不分页）"""
    theme = COLUMN_THEMES[num]
    style = f'--theme:{theme["color"]};--theme-bg:{theme["bg"]}'
    return f'<div style="{style}">'


def col_page_close() -> str:
    return "</div>"


def col_h3(text: str) -> str:
    return f'<h3 class="col-h3">{text}</h3>'


def lead_p(text: str) -> str:
    return f'<p class="lead-p">{text}</p>'


def pull_quote(text: str) -> str:
    return f'<div class="pull-quote">{text}</div>'


def big_number(num: str, unit: str, label: str) -> str:
    return f"""
<div class="big-number">
  <div><span class="num">{num}</span><span class="unit">{unit}</span></div>
  <div class="label">{label}</div>
</div>
"""


def info_card(title: str, body: str) -> str:
    return f"""
<div class="info-card">
  <div class="ic-title">{title}</div>
  {body}
</div>
"""


def tip_box(title: str, body: str) -> str:
    return f"""
<div class="tip-box">
  <div class="tip-title">💡 {title}</div>
  <p>{body}</p>
</div>
"""


def danger_box(title: str, body: str) -> str:
    return f"""
<div class="danger-box">
  <div class="tip-title">⚠️ {title}</div>
  <p>{body}</p>
</div>
"""


def story_card(tag: str, body: str) -> str:
    return f"""
<div class="story-card">
  <div class="story-tag">{tag}</div>
  {body}
</div>
"""


def compare(good_title: str, good_body: str, bad_title: str, bad_body: str) -> str:
    return f"""
<div class="compare-table">
  <div class="compare-col good">
    <div class="compare-head">✅ {good_title}</div>
    {good_body}
  </div>
  <div class="compare-col bad">
    <div class="compare-head">❌ {bad_title}</div>
    {bad_body}
  </div>
</div>
"""


def data_row(label: str, value: str) -> str:
    return f"""
<div class="data-row">
  <div class="data-label">{label}</div>
  <div class="data-value">{value}</div>
</div>
"""


def assess_intro(label: str, title: str, body: str) -> str:
    return f"""
<div class="assess-intro">
  <div class="label">{label}</div>
  <h3>{title}</h3>
  <p>{body}</p>
</div>
"""


def assess_q(num: int, question: str, options: list) -> str:
    """options: [(text, points)]"""
    opts_html = '\n'.join(
        f'<div class="opt"><span class="box"></span>{opt}<span class="pts">+{pts}分</span></div>'
        for opt, pts in options
    )
    return f"""
<div class="q-item">
  <span class="q-num">{num}</span><span class="q-text">{question}</span>
  <div class="q-options">{opts_html}</div>
</div>
"""


def scoring_table(title: str, rows: list) -> str:
    """rows: [(range, desc)]"""
    rows_html = '\n'.join(
        f'<div class="score-row"><div class="range">{r}</div><div class="desc">{d}</div></div>'
        for r, d in rows
    )
    return f"""
<div class="scoring">
  <h4>📊 {title}</h4>
  {rows_html}
</div>
"""


def thinking_box(question: str, hint: str) -> str:
    return f"""
<div class="thinking-box">
  <div class="label">💭 想 一 想</div>
  <p class="q">{question}</p>
  <p class="hint">{hint}</p>
</div>
"""
