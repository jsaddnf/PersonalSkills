---
name: course-creator
description: >
  创建结构化、多课时的 PDF 课程材料。适用于用户想把某个知识领域（如提示词工程、产品管理、
  数据分析、销售技巧等）制作成系统化课程的场景。每节课约 1 小时学习量，包含课程导读、
  各课正文、练习题和独立的答案手册，均以 PDF 格式输出并打包为 ZIP 提供下载。
  触发词包括：制作课程、编写课程、设计课程、做成教程、写成教材、课程 PDF 等。
---

# Course Creator Skill

## 概述

本 Skill 将一个知识领域制作成完整、专业、可下载的 PDF 课程包。
核心技术栈：**Python + WeasyPrint（HTML→PDF）**，利用 Noto Sans CJK SC 系统字体处理中文。

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
6. 输出格式偏好？（PDF 是默认推荐）
```

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
# 确认 Noto Sans CJK SC 可用

# 检查 WeasyPrint
from weasyprint import HTML
# 如未安装：pip install weasyprint --break-system-packages -q

# 字体确认清单（按优先级）：
# ✅ Noto Sans CJK SC（最佳，系统自带）
# ✅ WenQuanYi Zen Hei（备选）
# ❌ ReportLab TTFont + Noto CJK TTC 文件（PostScript 格式，不兼容）
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

### 7.3 write_pdf 标准函数

```python
def write_pdf(filename, chapter, body):
    """
    filename: 文件名（无路径），不含全角字符
    chapter:  页眉显示的章节名
    body:     HTML body 内容
    """
    path = os.path.join(OUT, filename)
    HTML(string=make_html(chapter, body)).write_pdf(path)
    size_kb = os.path.getsize(path) // 1024
    print(f'  ✅ {filename}  ({size_kb} KB)')
```

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

## 常见问题与解决方案

### ❌ 问题1：中文 PDF 生成乱码或字体显示异常
**原因**：ReportLab TTFont 不支持 Noto CJK TTC 文件（CFF/PostScript 格式）
**解决**：改用 WeasyPrint，CSS 直接声明 `font-family: 'Noto Sans CJK SC'`

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
□ 阶段一：需求确认（ask_user_input_v0 收集关键参数）
□ 阶段二：起草大纲 → 展示给用户 → 讨论覆盖度和深度 → 用户确认
□ 阶段三：检查技术环境（字体、WeasyPrint）
□ 阶段四：创建 course_design.py（设计系统，一次性创建，后续复用）
□ 阶段五：创建内容生成脚本（分 batch，每批 2-3 课）
□ 阶段六：生成第一批（导读 + 第1课）→ 用户预览确认排版
□ 阶段七：生成剩余各课
□ 阶段八：生成完整答案手册（每课强制分页）
□ 阶段九：运行验证脚本（内容完整性 + 文件名检查）
□ 阶段十：整理 final 目录（统一命名，无全角字符）
□ 阶段十一：打包 ZIP → present_files 提供下载
```
