# Style A — Minimal Editorial

> Calm, magazine-like, type-led. The kind of route book you'd want to print and tape into a notebook.

## Tone
- 安静、克制、留白
- 像 Cereal magazine / Kinfolk / Apple 产品页 的极简编辑风
- 字体撑场子，不靠装饰元素
- 单一暖色调，灰阶分层

## Color palette

| Role | Hex | Use |
|---|---|---|
| Background | `#fbfaf7` | 暖白主背景 |
| Text — primary | `#1c1916` | 标题、卡片标题 |
| Text — body | `#3c3530` | bullet 正文 |
| Text — muted | `#6b6258` | 副标题、脚注 |
| Text — caption | `#8a8175` | 距离/时长等元数据 |
| Text — tertiary | `#a59e93` | eyebrow（MAP / DAILY / DAY 1 等）|
| Divider — light | `#e8e3d8` | 全部 hairline 分割线 |
| Map — water | `#cbd6dc` (低透明) | 湖水提示 |
| Map — route | `#2c2925` | 主路线（暖炭色，不用纯黑）|
| Map — train return | `#a59e93` (虚线) | 火车返程 |

**No accent color.** 简约风的"高级感"靠完全克制的灰阶达成。任何彩色元素（红色 / 蓝色 chip）都会破坏整体气质。

## Layout — viewBox 720 × N

7 天行程参考高度 ≈ **2050**。每多一天约加 +170。

```
y 0 — 200    Title block
y 200 — 720  Map area
y 720 — 800  DAILY section break
y 800+ — N   Day cards (each ~150 tall, varies)
y last       Optional bottom indicator
```

### Title block
- y=86: eyebrow `ROAD TRIP · OCT 2026` font 11, weight 700, letter-spacing 4, color `#a59e93`
- y=146: 主标题，font 44, weight 700, letter-spacing -0.5
- y=180: 副标题，font 14，color `#6b6258`，格式：`日期 · 总里程 · 副标语`
- y=208: 全宽 hairline 分割线 (`#e8e3d8`, stroke-width 0.8)

### Map area
- y=252: eyebrow "MAP" 同 eyebrow 样式
- 路线 path stroke 2.2, line-cap round
- 火车返程 path 1.2 stroke + dasharray "5 4" + opacity 0.7
- 主驻留点：填充圆 r=6 + 外圈 r=11 stroke="#2c2925" opacity 0.35
- 普通经停点：填充圆 r=5
- 路过点：r=3.5 空心
- 高海拔垭口：填充三角形 + 海拔数字（仅 >3500m 标注）
- 城市标签 font 13-14 weight 600-700
- 距离标签 italic font 10 color `#8a8175`，沿路径放但不压字

### Day cards
每张卡片 600 宽（x=60-660）：
- y=0: eyebrow `DAY N` font 11, weight 700, letter-spacing 2, color `#2c2925`
- y=0 right: 日期文字 font 12, color `#6b6258`
- y=14: hairline 分割线 (stroke-width 0.6)
- y=46: 标题 font 22, weight 700, color `#1c1916`
- y=46 right: 元数据（距离 · 时长）font 13, color `#8a8175`
- y=80, 104, 128, 152: bullet 行（每行 24px 间距），font 14, color `#3c3530`
- emoji 占 x=0 起，文字从 x=32 起（这样多 bullet 横向对齐）

每两个 day card 之间留 ~25px 空隙（不画分隔线，靠空白即可）。

## Principles
- **Hierarchy through size**：标题 44 → section 22 → body 14 → caption 11。字号差距大，不靠粗细。
- **Hairlines, not boxes**：要分块就用 0.6-0.8 stroke，不用 rect 或 border。
- **Eyebrows为锚**：每个 section 都有一个 11pt 大写英文小标，作为视觉锚点。
- **每行 1 个 emoji**：作为 bullet 视觉锚，不要堆叠。
- **不要 chip / badge / pill**：所有数据都是纯文字，靠位置和颜色分层。

## Use cases
- 朋友间分享，对方愿意细读
- 长期保存（家里一份、电子一份）
- 情绪型 / 慢节奏旅行
- 单一目的地深度游

## Anti-pattern (避免)
- 加边框、加纸纹、加 watermark
- 用任何彩色 accent
- 标题写得过长（保持在 8 个汉字以内）
- 给每天加复杂的结构化框（破坏留白感）
