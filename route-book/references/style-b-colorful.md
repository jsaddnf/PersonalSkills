# Style B — Colorful Infographic

> Vibrant, scannable, attention-grabbing. The kind of route book that survives the chaos of a 100-person 微信群.

## Tone
- 鲜艳、信息密度高、扫读性强
- 像旅行海报 / 攻略图 / Notion 模板
- 色块说话，分类靠色彩
- 高对比，白字 on 彩色卡片

## Color palette

### 系统色
| Role | Hex | Use |
|---|---|---|
| Header bg | `#1a1a1a` | 顶部深炭灰头部 |
| Header strip | `#252321` | 路线流向条（略浅）|
| Header — title | `#fefcf6` | 白字标题 |
| Header — meta | `#9a8d75` | 副标题、灰字 |
| Header — accent | `#d97a3a` | 总里程/海拔的橙红强调 |
| Map bg | `#ead5b0` | 沙黄米色地图底 |
| Map — route | `#3a2d1a` | 深棕路线 |
| Map — text | `#1a1a1a` / `#5a4a35` | 标签 |
| Tips bg | `#fefcf6` | 底部白卡 |

### 七天主色（每张卡一色）
| Day | 主色 | 暗色（水印 + chip）|
|---|---|---|
| D1 钴蓝 | `#5b8cb5` | `#4a7aa0` |
| D2 金黄 | `#e6a13a` | `#c88a25` |
| D3 砖红 | `#c44d3e` | `#a83a2c` |
| D4 青绿 | `#3d8b85` | `#2d716c` |
| D5 橄榄 | `#5a7a3a` | `#4a6628` |
| D6 葡萄紫 | `#6b4f7a` | `#563d62` |
| D7 落日橙 | `#d97a3a` | `#b86028` |

如果行程超过 7 天，可循环使用 D1 蓝 → D8 蓝（更深 `#3a6a95`），但建议一天一色不超过 9 天。

## Layout — viewBox 720 × N

7 天行程参考高度 ≈ **2580**。每多一天约 +250。

```
y 0 — 180     Header (dark)
y 180 — 560   Map (sand beige)
y 580 — 2330  Day cards (each ~232 tall, with chips + bullets + footer)
y 2360 — 2540 Tips section (white card)
y 2570        Bottom indicator
```

### Header (180 tall)
- 全宽 `#1a1a1a` 背景
- y=56: 主标题，font 30, weight 700, white
- y=82: 副标题，font 12, color `#9a8d75`，格式：`节气 · 天数自驾 · 主要国道`
- y=50 right: 总里程 `1,750 km` font 22, weight 700, color `#d97a3a`
- y=80 right: 总海拔 `▲ 3,820 m` font 18, weight 700, color `#d97a3a`
- y=118-168: `#252321` 横条，y=148 放完整流向 `城市A → 城市B → 城市C → ...` font 13 color `#9a8d75`

### Map (380 tall)
- 全宽 `#ead5b0` 沙黄底
- 左上小指南针：圆 r=14 + N 标 + 三角箭头
- 右上 `ROUTE MAP` eyebrow（小灰字）
- 路线 path stroke 2.5 color `#3a2d1a`
- 火车返程 dashed stroke 1.5 color `#5a4a35` opacity 0.55
- **关键**：每个 stop 用对应当日色 + 白色 stroke 2.5，圆心填白色 D# 数字（如 "3"）
- 起 / 终点（如 "西宁 1·7"）用稍大圆 r=11
- 路过点（如 水上雅丹）用 r=6 空心
- 距离标签 italic 10pt color `#5a4a35`
- 城市名 font 13-14 weight 700，海拔 font 9 color `#5a4a35`

### Day cards (~232 tall each, x=60-660)
- 全卡填充：`rect rx=10` 当日主色
- **大数字水印**：`text x=570 y=195 text-anchor=end font-size=160 weight=800 opacity=0.55` 当日暗色 — 这是该风格最显著的视觉符号
- y=40: `D{N}` font 16 weight 700 white
- y=40 right of D: 日期 font 12 color 当日浅色
- y=78: 标题 font 22 weight 700 white
- y=96-120: 胶囊 chip 横排（每个高 24, rx=12, 当日暗色）
  - chip 内容：`📍 280 km` / `▲ 3,820 m` / `⏱ 5-6 h` 等
- y=148, 170, 192, 214: bullet 行 font 13 white
- y=240/218: 卡片底部脚注 font 11 当日浅色（用于：避坑提醒 / 加油提醒 / 额外信息）

每两张卡之间留 18px 空隙。

### Tips (180-220 tall)
- 全宽白卡 `#fefcf6` + `#e8e0cf` 1px 边框
- y=34: 大标题 "出行提示" font 16 weight 700
- y=48: 分割线
- 4 列分类（每列宽 280）：
  - 📋 证件 / ⛽ 燃油 / 🏔️ 高原 / 🎫 抢票（或其他）
  - 每个分类标题用对应当日色（D1蓝 / D4绿 / D3红 / D7橙等）font 12 weight 700
  - 每分类下 2 条小提示 font 11 color `#3c3530`

## Principles
- **色块替代分割线**：整张卡都是色块，section 自然分开
- **大数字水印是核心视觉**：每张卡右下角浮一个 160pt 半透明大数字
- **Chip 强化数据**：所有量化信息（km, m, h）都包成胶囊
- **分类化 emoji**：emoji 不只是装饰，而是分类信号（食物 / 山 / 床 / 车 等）
- **白字 on 色块**：所有正文白字 + 当日色脚注 + 当日暗色 chip

## Use cases
- 微信群/朋友圈分发，需要一眼吸睛
- 攻略型旅行，重信息密度
- 多日高强度，颜色区分天数有用
- 多人同行，每个人在群里只看自己关心的那一天

## Anti-pattern (避免)
- 用纯黑而不是 #1a1a1a（太硬）
- 卡片用饱和度过高的色（建议色板里的色都是经过降饱和的）
- 大数字水印不透明（必须 opacity 0.55 才不会喧宾夺主）
- chip 用浅色背景配深色文字（必须深 chip + 白字保持对比）
- 加阴影 / 渐变 — 这一风格是 flat design，没有 3D 元素
