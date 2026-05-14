---
name: course-creator
description: >
  创建结构化、多课时的课程材料。适用于用户想把某个知识领域（如提示词工程、产品管理、
  数据分析、销售技巧等）制作成系统化课程的场景。每节课约 1 小时学习量，包含课程导读、
  各课正文、练习题和独立的答案手册。默认输出 PDF，可选 HTML / Word / Markdown。
  触发词包括：制作课程、编写课程、设计课程、做成教程、写成教材、课程 PDF / HTML / Word 等。
---

# Course Creator Skill

## 概述

本 Skill 将一个知识领域制作成完整、专业、可下载的课程包。
核心技术栈：**Python + WeasyPrint（HTML→PDF）**，字体优先使用 **PingFang SC（苹方）**，
Linux/服务器渲染时自动降级到 Noto Sans CJK SC。

**默认输出格式：PDF**。可选同时生成 HTML / DOCX / Markdown（在需求确认阶段询问用户）。

---

## 第一阶段：需求确认（必须先做，不能跳过）

在写任何代码之前，先通过提问明确以下信息。可以用 `ask_user_input_v0` 工具集中收集：

```
必须确认的核心参数：
1. 目标学习者是谁？（零基础 / 有一定基础 / 职场特定人群 / 通用）
2. 课程语言？（中文 / 英文 / 双语）
3. 希望覆盖哪些核心主题？（让用户列举 3-5 个）
4. 课程深度定位？（入门科普 / 实战应用 / 进阶专业）
5. 课程量预期？（几节课 / 学习者能投入多少总时长）
   - 如果用户不确定，Claude 根据主题复杂度给出建议区间让用户选择
   - 例：「根据你的主题，我建议 6~9 课，你倾向于精简版（6课）还是完整版（9课）？」
   - 课时数直接影响学习者时间投入预期，属于用户决策权
6. 输出格式？（PDF 是默认，可多选）
   - ☑ PDF（默认，印刷/离线查看最佳）
   - ☐ HTML（可在线查看、分享链接、可嵌入网站）
   - ☐ DOCX（便于二次编辑、写批注）
   - ☐ Markdown（便于迁移到 Notion / GitHub / 飞书）
   - 用 ask_user_input_v0 的 multiSelect 模式询问
   - 不同格式会增加生成时间，建议只选真正需要的
```

### 关于输出格式的技术决策

| 格式 | 推荐度 | 适用场景 | 依赖 |
|------|--------|----------|------|
| PDF  | ★★★★★ | 默认；印刷、归档、离线查看 | `weasyprint` |
| HTML | ★★★★☆ | 在线课程、可嵌入 iframe、支持深链 | 无（生成独立单文件 HTML） |
| DOCX | ★★★☆☆ | 学员要改批注、打印带修订版 | `pandoc`（推荐）或 `html2docx` |
| MD   | ★★★☆☆ | 迁移到 Notion/GitHub/飞书妙记 | `pandoc`（推荐）或 `html2text` |

统一由 `course_design.py` 的 `write_course(..., formats=['pdf','html','docx','md'])` 入口分发。

**不需要确认的**（Claude 自行决定）：
- 设计风格（遵循本 Skill 的设计系统）
- 练习题数量（每课 4-5 道）

---

## 第二阶段：课程大纲设计（迭代讨论）

### 2.1 起草大纲

基于需求，起草课程大纲并**输出为 Markdown 表格**，格式如下：

```
## 《XXX》课程大纲

### 课程结构（共 N 课）

| 课程 | 阶段 | 主题 | 核心内容 |
|------|------|------|---------|
| 第一课 | 基础篇 | ... | ... |
...

### 每课详细大纲

#### 第一课：XXX
| 章节 | 内容 | 备注 |
|------|------|------|
| 1.1 | ... | 🆕新增 / 🔧加厚 |
...
```

### 2.2 大纲评估（主动提出）

给出大纲后，Claude 应主动评估并告知用户：

```
评估维度：
□ 覆盖度：是否有重要知识点缺失？
□ 深度：内容能否真正教会学习者，还是只是点到即止？
□ 时长：每课是否真的能填满 60 分钟？（阅读+练习+动手实验）
□ 结构：课程间的递进关系是否清晰？
□ 实用性：是否有足够的实战场景和可复用模板？
```

### 2.3 大纲确认

等用户确认大纲后再开始生成内容。**这一步是最关键的节约返工时间的步骤。**

---

## 第三阶段：技术环境准备

### 3.1 环境检查

```python
# 检查中文字体
import subprocess
result = subprocess.run(['fc-list', ':lang=zh'], capture_output=True, text=True)

# 检查 WeasyPrint
from weasyprint import HTML
# 如未安装：pip install weasyprint --break-system-packages -q

# 可选：检查 pandoc（DOCX / MD 输出需要）
pandoc_ok = subprocess.run(['pandoc', '--version'],
                           capture_output=True).returncode == 0
```

### 字体优先级（关键）

本 Skill 统一使用 **苹方字体（PingFang SC）** 作为首选：

```
1) PingFang SC / TC / HK   ← 首选（Apple 平台自带，最美观）
2) Noto Sans CJK SC        ← 兜底（Linux/服务器端 WeasyPrint 渲染用）
3) Source Han Sans SC      ← 开源备选（同思源黑体）
4) Microsoft YaHei         ← Windows 兜底
5) Hiragino Sans GB        ← Mac 老系统兜底
```

> **为什么 PingFang 放第一位？**
> macOS 用户本地查看 PDF/HTML 时会优先使用苹方，字形更优雅；
> 在 Linux 服务器渲染 PDF 的过程中会自动落到 Noto Sans CJK SC。
> 两种场景都得到最好的视觉效果。

**不要自己在批次脚本里重新定义字体栈**，必须引用 `course_design.py` 中的 `BASE_CSS`。

### 字体踩坑备忘

```
❌ ReportLab TTFont + Noto CJK TTC 文件   （PostScript 格式，不兼容）
❌ 在脚本里覆盖 font-family                （会打破统一性）
❌ 混用 PingFang 和 思源黑体               （字重体系不同，标题不对齐）
✅ 只用 course_design.py 的 BASE_CSS      （已经按优先级配好）
```

### 3.2 关键技术决策

| 方案 | 推荐 | 原因 |
|------|------|------|
| WeasyPrint + HTML/CSS | ✅ 强烈推荐 | 中文排版完美，CSS 全功能，字体兼容性好 |
| ReportLab | ⚠️ 不推荐用于中文 | Noto CJK TTC 是 CFF/PostScript 格式，TTFont 不支持 |
| pdfplumber | 仅用于读取/验证 | 不用于生成 |

---

## 第四阶段：设计系统（核心模块，复用于所有课程）

### 4.1 文件结构

```
/home/claude/
├── course_design.py      # 设计系统（颜色/样式/组件），所有课程复用
├── gen_guide.py          # 课程导读生成
├── gen_batch1.py         # 第1-3课 + 答案
├── gen_batch2.py         # 第4-6课
├── gen_batch3.py         # 第7-9课 + 完整答案手册
└── {课程名}/             # 输出目录
    └── final/            # 最终输出目录（干净文件名）
```

### 4.2 设计 Token（颜色系统）

```python
# 语义化颜色定义
COLORS = {
    # 品牌色
    'primary':      '#1A3A5C',  # 深蓝 - 主色/标题
    'accent':       '#2563EB',  # 电光蓝 - 强调/链接
    'accent_light': '#EFF6FF',  # 极浅蓝 - 背景

    # 语义色（卡片系统）
    'success':      '#059669',  'success_bg': '#F0FDF4',  # 好示例
    'danger':       '#DC2626',  'danger_bg':  '#FEF2F2',  # 坏示例
    'warn':         '#D97706',  'warn_bg':    '#FFFBEB',  # 练习题
    'purple':       '#7C3AED',  'purple_bg':  '#F5F3FF',  # 进阶技巧

    # 中性色
    'gray_100': '#F8F9FA',
    'gray_200': '#E9ECEF',
    'text':     '#111827',
    'white':    '#FFFFFF',
}
```

### 4.3 卡片组件系统

每种卡片对应特定的信息类型，全课程统一：

| 卡片类型 | 颜色 | 用途 | 函数 |
|---------|------|------|------|
| `card_key` | 蓝色 | 核心概念、知识点 | `card_key(title, body)` |
| `card_good` | 绿色 | 好示例 ✅ | `card_good(label, body)` |
| `card_bad` | 红色 | 坏示例 ❌ | `card_bad(label, body)` |
| `card_tip` | 灰色 | 提示、注意事项 💡 | `card_tip(title, body)` |
| `card_exercise` | 琥珀 | 练习题 ✏️ | `card_exercise(num, question)` |
| `card_advanced` | 紫色 | 进阶内容 ⚡ | `card_advanced(title, body)` |
| `card_answer` | 深绿 | 答案手册答案 ✅ | `card_answer(num, answer)` |

### 4.4 核心 CSS 规则

```css
/* 字体 */
body {
    font-family: 'Noto Sans CJK SC', 'PingFang SC', 'Microsoft YaHei', sans-serif;
    font-size: 10.5pt;
    line-height: 1.85;
    text-rendering: optimizeLegibility;
}

/* 分页控制 */
@page { size: A4; margin: 20mm 22mm 22mm 22mm; }
.page-break { page-break-before: always; }
.no-break   { page-break-inside: avoid; }

/* 标题层级 */
h2 {
    border-left: 3.5px solid #2563EB;  /* 左侧蓝色标识线 */
    padding-left: 10pt;
    color: #1A3A5C;
}

/* 段落 */
p { text-align: justify; word-break: break-all; }

/* 列表 */
ul li::before { content: ''; border-radius: 50%; background: #2563EB; }
ol { counter-reset: ol-counter; }
ol li::before { content: counter(ol-counter); background: #2563EB; color: white; }
```

### 4.5 为什么 HTML 不能直接复用 PDF 样式

PDF 是给印刷/A4 阅读设计的，HTML 是给屏幕滚动阅读设计的。两者根本不同：

| 维度 | PDF | HTML |
|------|-----|------|
| 容器宽度 | `@page margin` 给版心 | 没有版心约束，文字撑满 viewport |
| 单位系统 | `pt`（印刷单位） | `px` / `rem`（屏幕单位） |
| 字体大小 | 10.5pt（印刷阅读距离） | 16px（屏幕阅读距离） |
| 对齐 | `justify` 配合连字符 | 浏览器无连字符算法，justify 出大空隙 |
| 断字 | `word-break: break-all` 节省空间 | 会切断英文单词，可读性差 |
| 留白 | 印刷工艺要求的页边距 | 需要主动设计阅读容器 |
| 响应式 | 不需要 | 必须支持手机/平板/PC |

### 4.6 HTML 阅读容器规范

- **最大宽度**：760px（≈ 60-75 CJK 字符/行，最舒适阅读宽度）
- **页面背景**：`#F5F6F8`（暖灰，护眼）
- **容器背景**：`#FFFFFF` + 微阴影
- **圆角**：16px（PC）/ 12px（平板）/ 0px（手机）
- **内边距**：56px 64px（PC）→ 36px 28px（平板）→ 28px 20px（手机）

### 4.7 字号体系（屏幕）

```
body          16px  / 1.85 / letter-spacing 0.02em
h2            22px  / 1.45 / margin-top 48px
h3            18px  / 1.55 / margin-top 32px
p             16px  / 1.85 / margin-bottom 18px
ul/ol li      16px  / 1.75 / item gap 8px
table cell    14-15px
卡片正文       15.5px
封面标题       30px
```

### 4.8 间距节奏（8px 栅格）

```
xs   = 4px    小元素内
sm   = 8px    段落内、列表项
md   = 16px  段落间、卡片标题-正文
lg   = 24px  卡片外边距
xl   = 40px  大区块间
2xl  = 56px  h2 章节切换
```

### 4.9 响应式断点

| 屏幕 | 容器宽度 | 容器内边距 | 容器圆角 |
|------|---------|----------|---------|
| ≥ 1024px | 760px | 56px 64px | 16px |
| 768-1024px | calc(100% - 64px) | 48px 48px | 16px |
| 480-768px | calc(100% - 32px) | 36px 28px | 12px |
| < 480px | 100% | 28px 20px | 0 |

### 4.10 HTML 必须改的 PDF 默认（关键修复）

- `text-align: justify` → `text-align: left`（HTML 无连字符算法）
- `word-break: break-all` → `overflow-wrap: anywhere`（CJK 自然换行 + 长 URL 兜底）
- `pt` → `px`（屏幕单位）
- 不依赖 `@page` 约束（屏幕无效）

### 4.11 PDF/HTML 兼容策略（关键）

所有 HTML 屏幕优化包在 `@media screen { ... }` 里：
- WeasyPrint 渲染 PDF 时只读 `@media print`，会自动忽略 screen 规则
- 浏览器渲染 HTML 时读 `@media screen`，覆盖 PDF 默认值

**一份 CSS，两种渲染。**具体实现见 `course_design.py` 中的 `HTML_SCREEN_CSS` 常量，自 v2 起 `make_html()` 会同时注入 `BASE_CSS + HTML_SCREEN_CSS`。

---

## 第五阶段：内容生成规范

### 5.1 每节课的标准结构

```
1. lesson_cover()     - 封面（课程编号、标题、描述、时长、主题标签）
2. h2() × N          - 章节内容（通常 5-7 个章节）
3. 各种卡片/表格/对比 - 核心知识点
4. prompt_block()    - 提示词示例（如适用）
5. h2('本课练习题')  - 练习题区域
6. card_exercise() ×4-5  - 练习题（带难度标签）
```

### 5.2 练习题设计规范

```python
# 难度标签（每课必须有梯度）
'1.1  🌱'   # 基础：直接应用本课知识
'1.2  🌱'   # 基础：识别/判断类
'1.3  🌿'   # 进阶：综合运用
'1.4  🌿'   # 进阶：设计/创作类
'1.5  🌳'   # 挑战：综合题、开放题

# 练习题必须包含：
# - 明确的任务描述
# - 必要的场景背景
# - 💡 提示（指向关键知识点）
# - 建议在 AI 工具中实际运行
```

### 5.3 对比表格规范

```python
# 所有好坏示例必须使用 compare() 函数，不要用文字描述
compare(
    '❌ 差提示词',  '模糊的描述',
    '✅ 好提示词',  '具体清晰的描述，包含...'
)
# 两列等宽，左红右绿，视觉对比强烈
```

### 5.4 提示词块规范

```python
# 所有提示词示例必须放在 prompt_block() 中
# 使用多行文本，占位符用【】标注
prompt_block(
    '请帮我写一封【邮件类型】邮件。\n\n'
    '收件人：【身份】\n'
    '核心目的：【目的】\n'
    '【更多参数】'
)
# 样式：深蓝标题栏 + 浅蓝背景，等宽字体
```

---

## 第六阶段：答案手册设计规范（重要）

### 6.1 核心原则

**每课答案必须从新页开始（page-break-before: always）**
即使上一课答案只占了半页，也必须强制翻页。原因：学习者查看某课答案时，不会意外看到下一课答案。

### 6.2 答案手册结构

```
封面页
使用说明页
─────────────────── [强制新页] ───────────────────
LESSON 01 第一课答案
  警告横幅：请确认完成第一课全部练习题后再查阅
  1.1 答案（题目回顾 → 分析 → 参考答案 → 评分要点）
  1.2 答案
  ...
─────────────────── [强制新页] ───────────────────
LESSON 02 第二课答案
  ...
```

### 6.3 每道答案的内部结构

```python
card_answer('1.1  🌱  题目简短描述',
    '<p><strong>问题分析：</strong>指出原始版本的具体问题</p>'
    '<p><strong>参考答案：</strong>完整的参考内容</p>'
    '<p><strong>评分要点：</strong>判断答案是否正确的标准</p>'
    # 进阶题额外加：
    '<p><strong>进一步思考：</strong>引导超越标准答案的思考</p>'
)
```

### 6.4 答案手册标题样式

```python
def lesson_ans_header(num_cn, num_en, title):
    return (
        page_break() +  # ← 强制新页，这是关键
        f'<div style="background:linear-gradient(135deg,#1A3A5C,#2563EB);...">'
        f'  <div>LESSON {num_en}</div>'
        f'  <div>第{num_cn}课答案</div>'
        f'  <div>{title}</div>'
        f'</div>'
        f'<div style="background:#FFFBEB;border-left:3.5px solid #D97706;...">'
        f'  ✏️ 请确认已完成第{num_cn}课全部练习题后，再查阅以下答案。'
        f'</div>'
    )
```

---

## 第七阶段：文件输出规范

### 7.1 文件命名规则（关键）

```
❌ 禁止使用全角括号：练习题答案手册（全9课）.pdf  → 导致系统无法识别，无法下载
❌ 禁止使用特殊符号：[]{}|<>  等

✅ 正确格式：
00_课程导读.pdf
01_第一课_认识AI与提示词基础.pdf
10_练习题答案手册.pdf

规则：只允许 数字 + 下划线 + 中文 + 英文字母 + 点号
```

### 7.2 目录结构

```
/mnt/user-data/outputs/{课程名}/
├── {中间产物，各批次生成的文件}
└── final/                    ← 最终交付目录，只放干净版本
    ├── 00_课程导读.pdf
    ├── 01_第一课_XXX.pdf
    ├── ...
    └── 10_练习题答案手册.pdf

/mnt/user-data/outputs/{课程名}_完整版.zip  ← 打包交付
```

### 7.3 多格式统一输出（write_course）

`course_design.py` 已内置多格式分发器，batch 脚本直接调用即可：

```python
from course_design import write_course

# 单格式（PDF，默认）
write_course(
    out_dir='/mnt/user-data/outputs/提示词工程课/final',
    basename='01_第一课_认识AI',      # 无扩展名，会自动清理特殊字符
    chapter='第一课',                 # 页眉章节名
    body=lesson1_body_html,           # 已组装好的 body
    formats=['pdf'],                   # 只输 PDF
    brand='提示词工程实战课',           # 页眉左侧品牌
)

# 多格式（用户选了 PDF + HTML + DOCX）
write_course(
    out_dir=out_dir,
    basename='01_第一课_认识AI',
    chapter='第一课',
    body=lesson1_body_html,
    formats=['pdf', 'html', 'docx'],
)
```

单独调用各格式：
- `write_pdf(out_dir, basename, chapter, body, brand)`
- `write_html(out_dir, basename, chapter, body, brand)`
- `write_docx(out_dir, basename, chapter, body, brand)` — 需 pandoc
- `write_markdown(out_dir, basename, chapter, body, brand)` — 需 pandoc

所有函数**自动调用 normalize_emoji()**，无需手动处理 emoji 包裹。

---

## 第八阶段：验证（生成后必须执行）

### 8.1 自动化验证脚本

生成完成后，**必须运行以下验证**，确保内容完整：

```python
import pdfplumber, os

def validate_course(final_dir, lesson_count, exercises_per_lesson):
    issues = []
    
    # 1. 检查所有课程文件存在
    expected_files = (
        ['00_课程导读.pdf'] +
        [f'0{i}_第{cn}课_XXX.pdf' for i, cn in enumerate('一二三四五六七八九', 1)] +
        ['10_练习题答案手册.pdf']
    )
    
    # 2. 检查每课练习题编号完整（如 1.1, 1.2...）
    for lesson_num in range(1, lesson_count + 1):
        q_count = exercises_per_lesson.get(lesson_num, 5)
        fname = f'对应课程文件.pdf'
        with pdfplumber.open(os.path.join(final_dir, fname)) as pdf:
            text = '\n'.join(p.extract_text() or '' for p in pdf.pages)
        for q_num in range(1, q_count + 1):
            if f'{lesson_num}.{q_num}' not in text:
                issues.append(f'第{lesson_num}课: 练习题 {lesson_num}.{q_num} 缺失')
    
    # 3. 检查答案手册每课分页标记
    with pdfplumber.open(os.path.join(final_dir, '10_练习题答案手册.pdf')) as pdf:
        ans_text = '\n'.join(p.extract_text() or '' for p in pdf.pages)
    for n in range(1, lesson_count + 1):
        n_str = f'{n:02d}'
        if f'LESSON {n_str}' not in ans_text:
            issues.append(f'答案手册: LESSON {n_str} 分页标记缺失')
    
    # 4. 检查关键内容关键词
    # （根据具体课程定制）
    
    if issues:
        print(f'❌ 发现 {len(issues)} 个问题:')
        for issue in issues:
            print(f'  · {issue}')
    else:
        print('✅ 验证通过')
    
    return len(issues) == 0
```

### 8.2 文件系统验证

```python
# 检查所有文件可正常访问（确认无全角字符文件名问题）
import os
final_dir = '/mnt/user-data/outputs/xxx/final'
for fname in os.listdir(final_dir):
    path = os.path.join(final_dir, fname)
    size = os.path.getsize(path)
    print(f'{fname}: {size//1024}KB')
    assert size > 100 * 1024, f'{fname} 文件太小，可能生成失败'
```

---

## 第九阶段：打包交付

```bash
# 打包时注意：
# 1. 只打包 final/ 目录中的文件，不包含中间产物
# 2. ZIP 文件名不含全角字符

cd /mnt/user-data/outputs/{课程名}/final
zip -j /mnt/user-data/outputs/{课程名}_完整版.zip *.pdf

# 验证 ZIP 内容
unzip -l /mnt/user-data/outputs/{课程名}_完整版.zip
```

---

## 第十阶段：Emoji 与特殊字符处理规范（重要）

### 10.1 为什么要特殊处理 emoji？

emoji 在课程 PDF 中大量使用（🌱🌿🌳 表难度、✅❌表对错、📌💡⚡表类别），
但直接裸写会导致以下排版问题：

```
问题         具体表现                            原因
────────────────────────────────────────────────────────
撑破行高     一行里有 emoji 的比其它行更高      emoji 原生字形比汉字高
上下错位     emoji 浮在基线上或沉到下方         baseline 不对齐
字号变形     emoji 比同段文字看着大一号         emoji 字体默认字号不同
粗体溢出     加粗段里的 emoji 变形              emoji 继承了 bold
豆腐框       部分环境显示成 □                   字体栈没配 emoji fallback
行首断行     emoji 触发奇怪的换行点             word-break 不当
```

### 10.2 解决方案：强制样式规范化

在 `course_design.py` 中已内置完整方案：

```css
/* CSS 端：锁定 emoji 外观 */
.emoji {
    font-family: 'Apple Color Emoji', 'Segoe UI Emoji',
                 'Noto Color Emoji', 'Twemoji Mozilla',
                 'Noto Emoji', sans-serif;
    font-size: 0.95em;         /* 锁定大小 */
    font-style: normal;        /* 防斜体继承 */
    font-weight: 400;          /* 防加粗继承 */
    line-height: 1;            /* 不撑破行高 */
    vertical-align: -0.08em;   /* 基线微调对齐 */
    display: inline-block;     /* 限制影响范围 */
    white-space: nowrap;
    word-break: keep-all;      /* 防奇怪换行 */
}
```

```python
# Python 端：自动包裹工具
from course_design import normalize_emoji, emoji, strip_emoji

# 1) 自动包裹（推荐）——make_html 默认开启，无需手动调用
make_html(chapter, body_html)   # auto_normalize_emoji=True

# 2) 手动在组件里精确控制
f'<h3>{emoji("🌱")} 基础题</h3>'

# 3) emoji-free 模式（特殊场景：老旧打印机、OCR 前处理）
plain_title = strip_emoji('🌱 基础题')   # → " 基础题"
```

### 10.3 规范：emoji 编辑七要素

```
1. 只从"推荐 emoji 集"中选用，不要用生僻 emoji（见 10.4）
2. 单个元素至多 1 个 emoji，不要连续堆砌（如 ✨🎉🌟🎊）
3. 不要在标题的末尾用 emoji（容易触发断行）
4. 同一类型信息用同一个 emoji，全课程统一
   （如"小贴士"永远用 💡、"练习题"永远用 ✏️）
5. 永远不要把 emoji 放进 <strong>/<em>/<code> 内部
6. 永远不要直接在 HTML 属性里用 emoji（如 title="⭐"）
7. 生成完 body_html 后，必须经过 make_html() 或手动 normalize_emoji()
```

### 10.4 推荐 emoji 集（全课程统一使用）

```
类别              emoji   用途                   对应函数
─────────────────────────────────────────────────────────
核心知识点        📌      标注重点              card_key
小贴士            💡      额外提示              card_tip
好示例            ✅      正确做法              card_good
坏示例            ❌      反面教材              card_bad
练习题            ✏️      题目区                card_exercise
进阶技巧          ⚡      高阶内容              card_advanced
参考答案          ✅      答案手册              card_answer
提示词示例        ✦       prompt 块             prompt_block
时长              ⏱       封面 meta             lesson_cover
主题数            📚      封面 meta             lesson_cover
基础难度          🌱      题目标签              手动
进阶难度          🌿      题目标签              手动
挑战难度          🌳      题目标签              手动
新增内容          🆕      大纲备注              手动
加厚内容          🔧      大纲备注              手动
```

> 这 15 个 emoji 已经足够覆盖全部课程需求。**不要自己创造新的**。

### 10.5 验证 emoji 未撑破排版

生成 PDF 后用 pdfplumber 抽样检查行高：

```python
import pdfplumber
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages[:3]:
        # 检查同一行内字符高度是否一致
        chars = page.chars
        by_row = {}
        for c in chars:
            row_key = round(c['top'], 0)
            by_row.setdefault(row_key, []).append(c['height'])
        # 同一行字号方差应该很小（< 2pt）
        for row, heights in by_row.items():
            if max(heights) - min(heights) > 3:
                print(f'⚠️ 行 {row} 字号差异异常: '
                      f'{min(heights):.1f} ~ {max(heights):.1f}')
```

如果出现字号差异警告，检查该行是否有裸 emoji（未被 span class="emoji" 包裹）。

---

## 常见问题与解决方案

### ❌ 问题1：中文 PDF 生成乱码或字体显示异常
**原因**：ReportLab TTFont 不支持 Noto CJK TTC 文件（CFF/PostScript 格式）
**解决**：改用 WeasyPrint，字体栈优先使用 PingFang SC，兜底 Noto Sans CJK SC

### ❌ 问题2：文件无法预览/下载
**原因**：文件名包含全角括号 `（）` 等特殊字符
**解决**：文件名只用 ASCII + 中文汉字，无括号、无方括号

### ❌ 问题3：答案手册查阅时能看到下一课答案
**原因**：答案间没有强制分页
**解决**：每课答案块开头必须有 `page-break-before: always` 的 div

### ❌ 问题4：课程内容感觉"点到即止"，不够深
**原因**：只覆盖了"是什么"，没有覆盖"为什么失败"和"怎么诊断"
**解决**：主动补充：反模式（错误写法）、失败诊断框架、可复用模板

### ❌ 问题5：练习题没有反馈机制，学习者不知道答得对不对
**原因**：练习题设计为开放式，答案模糊
**解决**：每道答案必须包含"评分要点"——明确说明正确答案的判断标准

### ❌ 问题6：PDF 里 emoji 撑破行高 / 字号变形 / 显示成豆腐框
**原因**：emoji 原生字形比汉字大，基线不对齐；字体栈未包含 emoji fallback
**解决**：
1. 所有 emoji 必须用 `<span class="emoji">` 包裹（或依赖 `make_html()` 自动规范化）
2. CSS 端 `.emoji` 类锁定 font-size / line-height / vertical-align
3. 只使用第 10.4 节的"推荐 emoji 集"，不要用生僻 emoji

### ❌ 问题7：DOCX / Markdown 输出失败
**原因**：未安装 pandoc 或 html2docx / html2text
**解决**：
```bash
brew install pandoc                                # macOS 推荐
apt install pandoc                                 # Linux
pip install html2docx html2text --break-system-packages  # Python 兜底
```

### ⚠️ 注意：生成脚本分批运行
**原因**：课程内容量大，单个脚本超过 context 限制容易截断
**解决**：拆分为 gen_batch1.py / gen_batch2.py / gen_batch3.py，每批 2-3 课

---

## 快速参考：课程结构模板

### 适合大多数知识课程的 8 课结构

```
基础篇（第1-2课）
  第1课：认识 XXX / 为什么重要 / 核心原则
  第2课：基础框架 / 核心方法论

实战应用篇（第3-5课）
  第3课：场景一实战（最高频的应用场景）
  第4课：场景二实战
  第5课：场景三实战（可以是通用/生活场景）

技能进阶篇（第6-7课）
  第6课：工具/系统/流程深化
  第7课：进阶技巧 / 高级方法

综合实践篇（第8课）
  第8课：最佳实践 / 常见误区 / 持续学习 / 资源汇总
```

### 课程总量参考

| 知识领域 | 推荐课数 | 原因 |
|---------|---------|------|
| 入门科普类 | 4-6 课 | 内容不需要太深，重在建立认知 |
| 实战技能类 | 6-9 课 | 需要多个场景覆盖，含进阶内容 |
| 专业领域类 | 8-12 课 | 内容复杂，需要循序渐进 |

---

## 执行流程总结（Checklist）

```
□ 阶段一：需求确认
    · 学习者/语言/主题/深度/课时数
    · 输出格式（PDF 默认，可多选 HTML / DOCX / MD）
□ 阶段二：起草大纲 → 展示给用户 → 讨论覆盖度和深度 → 用户确认
□ 阶段三：检查技术环境
    · 字体：fc-list | grep -i "PingFang\|Noto CJK" 至少有一个
    · WeasyPrint 已安装
    · 如需 DOCX/MD：pandoc 已安装（优先）或 html2docx/html2text
□ 阶段四：创建 course_design.py（设计系统，从本 Skill 拷贝，不要修改）
□ 阶段五：创建内容生成脚本（分 batch，每批 2-3 课）
    · 所有 emoji 只用第 10.4 节的"推荐集合"
    · 生成的 body_html 由 make_html() 自动 normalize_emoji()
□ 阶段六：生成第一批（导读 + 第1课）→ 用户预览确认排版
    · 重点检查：emoji 是否撑破行高、字体是否是苹方
□ 阶段七：生成剩余各课
□ 阶段八：生成完整答案手册（每课强制分页）
□ 阶段九：运行验证脚本
    · 内容完整性 + 文件名检查
    · emoji 排版验证（pdfplumber 检查字符高度一致）
□ 阶段十：按需多格式输出
    · write_course(out_dir, basename, chapter, body, formats=[...])
□ 阶段十一：整理 final 目录（统一命名，无全角字符）
□ 阶段十二：打包 ZIP → present_files 提供下载
```

---

# 附录 A：杂志模式（Magazine Mode）

> 课程模式之外的另一种形态。读者不是"学员"而是"读者"，没有学习路径，可以从任何一页翻开。
> 适合：家庭科普读物、行业内参、年度报告、生活方式手册。

## A.1 何时用杂志模式

| 维度 | 课程模式 | 杂志模式 |
|------|---------|---------|
| 受众 | 学员（要学会某项技能） | 读者（想了解某个话题） |
| 阅读路径 | 必须从头到尾 | 可任意翻读 |
| 文件结构 | 多个 PDF（每课一个 + 答案手册） | **单个 PDF**（一本完整杂志） |
| 章节命名 | "第一课"、"第二课" | "专栏 01"、"专栏 02" |
| 章节开头 | 学习目标、时长、概述 | **没有**——直接进入故事/引言 |
| 章节结尾 | 练习题 + 答案 | 思考题（开放式，无标准答案） |
| 文风 | 教师讲解 | 编辑讲故事 |
| 视觉密度 | 文字为主 | 文字 + 信息图 + 大数字 + 卡片 |
| 页面尺寸 | A4 | **A5（148×210mm）**——手机阅读友好 |
| 正文字号 | 10.5pt | **13pt**——大字号、老花眼友好 |

**决策提示**：
- 用户说"做成杂志"、"轻松阅读"、"不要每章前面啰嗦"、"放在一个文件里" → 杂志模式
- 用户说"让爸妈/老人/中老年人看" → 强制杂志模式 + 大字号
- 内容偏"知识科普 + 生活方式" → 倾向杂志
- 内容偏"技能训练 + 操作步骤" → 倾向课程

## A.2 设计系统：`magazine_design.py`

本 Skill 目录下提供 `magazine_design.py`，是杂志模式的完整设计系统，**和 `course_design.py` 并行存在**。
- 不要把杂志组件塞进 `course_design.py`
- 不要在杂志项目里 import `course_design.py`

### 杂志专用颜色系统

```python
# 暖色调，摆脱"医院蓝"的冰冷感
COLORS = {
    'bg':       '#FAF7F2',  # 米白背景（不用纯白，护眼）
    'text':     '#2C2C2C',  # 深墨（比纯黑柔和）
    'green':    '#2D8659',  # 温柔绿（主色）
    'orange':   '#E89B3C',  # 暖橙（点缀色）
    'sky':      '#4A90A4',  # 天空蓝（数据类）
    'purple':   '#8E6BAA',  # 暖紫（情绪类）
    'berry':    '#B85563',  # 莓红
    'leaf':     '#6B8E3D',  # 草青
    'pine':     '#1F6650',  # 深绿
    'brick':    '#C84135',  # 砖红（仅警示用）
    'warn':     '#D97706',  # 警示橙
}
```

每个专栏一个主题色（`COLUMN_THEMES`），封面色块、章节标题边框、信息卡背景全用该专栏的主题色，视觉一致性强。

### 字号体系（杂志专用，比课程大一档）

```
封面主标题      48-50pt
专栏封面标题    38pt
章节标题 h2     21-22pt
小节标题 h3     15-16pt
正文段落        13pt    line-height 1.95
引言段落 lead   14pt    顶下加横线
拉出引语 quote  19pt    上下加短装饰线
大数字 number   56pt    Georgia 衬线体
卡片标题        12pt
卡片正文        11.5-12pt
```

### 杂志专用组件

```python
mag_cover(title, sub, features, author, publisher, issue)
    # 满版渐变色封面 + 期刊号 + 本期看点 + 作者署名

toc_page(items)
    # 目录，左侧专栏号(Georgia 衬线大号字) + 右侧页码

column_cover(num, title, lead)
    # 整页满版色块封面，专栏号 + 标题 + 一句话引言 + 大图标

col_page_open(num, h2, tag='COLUMN 0X · 第 X 节')
    # 专栏内章节页开始(自动应用主题色 CSS 变量)

lead_p(text)                  # 加横线的引言段落
pull_quote(text)              # 拉出引语(带装饰线)
big_number(num, unit, label)  # 大数字 + 单位 + 说明
info_card(title, body)        # 主题色背景信息卡
tip_box(title, body)          # 黄色提示
danger_box(title, body)       # 红色警示
story_card(tag, body)         # 案例卡片
compare(good, good_b, bad, bad_b)  # 左绿右红对比
data_row(label, value)        # 速查表行
thinking_box(question, hint)  # 专栏末尾思考题(无答案)
```

**版权页建议自定义**：默认的 `copyright_page()` 偏严肃。家庭科普读物建议写自定义内联 HTML"读前须知"，用三个色块：黄色（仅供科普参考）+ 绿色（怎么读这本书）+ 粉色（免责声明）。

### 杂志 ≠ 课程，不能复用课程组件

| 课程组件 | 杂志替代 | 为什么 |
|---------|---------|--------|
| `lesson_cover()` | `column_cover()` | 杂志不叫"第一课" |
| `card_exercise()` | `thinking_box()` | 杂志没有作业，只有思考题 |
| 答案手册 | **没有** | 杂志没有标准答案 |
| 课末复习 | **没有** | 直接结尾 |

## A.3 渲染管线 ⚠️ 关键

### 字体陷阱（实战踩过的坑）

**❌ 错误流程**：weasyprint → PDF
- weasyprint 子集化 macOS 系统中文字体（PingFang / Hiragino，都是 **OpenType-CFF** 格式）时
- **ToUnicode CMap 会写入错误的字形→Unicode 映射**
- 结果：
  - poppler / Chrome / Firefox 渲染：✅ 正常（不严格依赖 ToUnicode）
  - **macOS Preview / qlmanage / Quick Look：❌ 全屏乱码**（"HCO KN CN C F D M"）
- 这个 bug 在 weasyprint 68 仍存在

**✅ 正确流程**：weasyprint → HTML → **Chrome headless → PDF**
- weasyprint 只负责把 HTML 排版好（保留它的 CSS 排版能力）
- Chrome 用 Skia 渲染字体，嵌入为 **Type 3 字体 + Custom encoding**
- Type 3 = 字形画成 PDF 内部子例程，独立于原字体格式
- 任何 PDF 阅读器（包括 macOS Preview / 微信内置 / WPS）都能正确渲染

```python
# 杂志项目的 PDF 生成（最关键的一段代码）
import subprocess

# 1. weasyprint 只生成 HTML
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(HTML_DOC)

# 2. Chrome 把 HTML 转 PDF
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
subprocess.run([
    CHROME,
    '--headless=new',
    '--disable-gpu',
    '--no-sandbox',
    '--no-pdf-header-footer',
    '--virtual-time-budget=8000',
    '--run-all-compositor-stages-before-draw',
    f'--print-to-pdf={pdf_path}',
    f'file://{html_path}',
], capture_output=True, text=True, timeout=300)
```

**注意**：内容多时（50+ 页 A5），Chrome 渲染可能需要 30-60 秒。subprocess `timeout` 设到 **300 秒** 起步。

### 如何验证 PDF 没有乱码 ⚠️ 必须用对工具

| 工具 | 引擎 | 是否反映 Preview 实际效果 |
|------|------|------|
| `pdftoppm` | poppler | ❌ **不反映**——poppler 不严格按 ToUnicode |
| `qlmanage -t -s 1500 -o /tmp file.pdf` | **CoreGraphics（同 Preview）** | ✅ **必须用这个验证** |
| 直接 `open file.pdf` | macOS Preview | ✅ 最终用户体验 |

**血泪教训**：之前用 `pdftoppm` 转 PNG 自我验证一直显示正常，但用户在 Preview 看到的是全屏乱码。后来换 `qlmanage` 才复现问题。

**强制规范**：杂志模式 PDF 生成后，**必须**用 `qlmanage` 渲染至少 3 页转 PNG，确认无乱码再交付。

### 如果用户系统没有 Chrome

退而求其次的方案（按优先级）：
1. 让用户用 Chrome / Edge / Brave 任一 Chromium 浏览器手动打印 HTML
2. 装 `brew install --cask chromium`（征得用户同意）
3. Playwright / Puppeteer（需要 Node.js）

**不要建议换字体**——用户对 PingFang 美感有要求，换思源黑体或 Noto Sans 是降级。

## A.4 emoji 正则的"通用标点陷阱"

之前的 emoji 正则范围太宽，把 General Punctuation (`U+2000-U+206F`) 圈进去，导致 `——`、`……`、`""` 这些 CJK 标点被当成 emoji 包裹，进而被 emoji 字体栈接管——emoji 字体不含这些字符 → 显示 `[?][?]`（豆腐框）。

**正确的 emoji 正则范围**（只匹配真 emoji 码点）：

```python
_EMOJI_CHARS = (
    '\U0001F300-\U0001F5FF'   # Symbols & Pictographs
    '\U0001F600-\U0001F64F'   # Emoticons
    '\U0001F680-\U0001F6FF'   # Transport
    '\U0001F900-\U0001F9FF'   # Supplemental Symbols
    '\U0001FA00-\U0001FAFF'   # Symbols Extended
    '\U0001F100-\U0001F1FF'   # Enclosed Chars
    '\U00002600-\U000026FF'   # Misc Symbols
    '\U00002700-\U000027BF'   # Dingbats
)
# 注意：U+2000-U+206F (General Punctuation) **不要包含**
# 注意：U+2300-U+23FF (Misc Technical)      **不要包含**
# 注意：U+25A0-U+25FF (Geometric Shapes)    **不要包含**
```

**双保险**：emoji CSS 字体栈末尾加 PingFang 兜底，即使误判也不会出豆腐框。

## A.5 info-card 文本对齐陷阱

`info-card` 是杂志最常用的容器。如果继承全局 `text-align: justify`，多行内容里的全角空格会被 justify 拉伸成大空白，特别是"① 嘴里　米饭..."、"② 胃里　..."这种"序号 + 标题 + 全角空格 + 正文"的场景下，③④⑤ 会有夸张的首字缩进。

**修复**：`.info-card p { text-align: left; }`

## A.6 内容严谨性原则（科普类必看）⚠️

杂志模式经常承载医学、健康、法律、金融等科普类内容。**错误信息影响很坏**。

### 强制流程

1. **数值标准必须按权威指南**
   - 医学：以最新版国内指南为准（如《中国 2 型糖尿病防治指南 2020》）
   - 不要混用国际标准（如 WHO 腰围 vs 中国指南腰围）
   - 不确定就标注"具体由医生 / 专业人士判断"

2. **同一数值在不同处出现，必须一致**
   - 案例：腰围标准在"风险清单"和"自评题"出现，必须用同一个数字（中国指南：男 ≥90cm，女 ≥85cm）
   - 一旦不一致，立即修复——这是诱导用户错误判断的硬伤

3. **生成完所有内容后，必须做一次内部 review**
   - 主动告诉用户："我自己审查了一遍，发现 X 处不严谨，已修正为 Y"
   - 不要等用户发现

4. **每节涉及医学决策的地方加免责声明**
   - "具体诊断须由医生确认"
   - "请遵主治医生指导"
   - "不构成医疗建议"

5. **辟谣类章节必须有正面证据**
   - 不要只说"这是谣言"
   - 要解释"为什么是谣言" + "正确做法是什么"

## A.7 用户措辞稳定性原则

杂志类项目用户对措辞会反复推敲。一旦用户定下某段文字（"读前须知"、"封面看点"、"卷首语"），**绝对不要在后续修改其他部分时偷偷动它**。

**血泪教训**：用户定了"这是一本家庭科普杂志，帮助家人。"，我在下一版里"优化"成"这是一本小小的家庭科普手册"，被用户严厉指出。

**规范**：
- 重大文案变更必须提示用户确认
- 同样的话不要"再润色一次"
- 用户的原话尽量原样保留，不要"觉得太短/太朴素"就加修饰

## A.8 杂志模式执行流程 Checklist

```
□ 阶段一：形态判断
    · 用户要求是课程还是杂志？(A.1 决策表)
    · 如果是杂志：单文件 PDF / A5 / 大字号 / 不要练习题
□ 阶段二：需求确认
    · 杂志名 / 期号 / 作者 / 出品方
    · 专栏(栏目)数量、每个专栏的核心内容点
    · 工具页(急救卡 / 打卡 / 参考资料 / 寄语 / 封底)
□ 阶段三：技术环境
    · weasyprint 已装
    · Chrome 已装（/Applications/Google Chrome.app）
    · pdftoppm(poppler) + qlmanage 可用
□ 阶段四：拷贝 magazine_design.py，**不修改**
□ 阶段五：写 gen_magazine.py，组装所有专栏内容
    · 每个专栏：column_cover() + 数个 col_page_open(...) + col_page_close()
    · 末尾思考题用 thinking_box()
□ 阶段六：weasyprint 渲染 HTML → Chrome headless → PDF
    · subprocess.run(timeout=300) 起步
□ 阶段七：⚠️ 用 qlmanage 验证(不是 pdftoppm！)
    · 抽样 3-5 页(封面、读前须知、专栏内页、表格页、急救页)
    · 确认 macOS CoreGraphics 渲染无乱码
□ 阶段八：内部内容 review
    · 数值与权威指南一致
    · 同一指标多处一致
    · 主动告知用户审查结果和修正点
□ 阶段九：交付 PDF + HTML 双份
    · PDF：~/Downloads/{杂志名}.pdf
    · HTML：~/Downloads/{杂志名}.html(兜底，浏览器可看)
□ 阶段十：用户验收，回填目录页码(如果用户在意精确度)
```

## A.9 已知未解决问题

- **Chrome headless 启动慢**：50+ 页 A5 单次渲染需要 30-60 秒。subprocess 超时设到 300 秒
- **目录页码估算**：内容生成前无法精确知道每节多少页。当前做法是估算 → 生成 → 用 `pdfinfo` 检查实际位置 → 改目录数字 → 再生成一次。如果用户接受目录页码"大致对"，可以省第二次生成
