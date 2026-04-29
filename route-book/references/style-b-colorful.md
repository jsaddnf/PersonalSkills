# Style B — Colorful Infographic (Dark Canvas)

> Vibrant cards floating on a single immersive dark canvas. Scannable, attention-grabbing, modern. The kind of route book that survives the chaos of a 100-person 微信群 and feels like a proper design piece.

## Tone
- 鲜艳卡片 on 沉浸暗底
- 整页一块连续深色画布——header / 地图 / 卡片间隙都是同一个底色，没有"图区""tips 区"这种分块感
- 色块说话，分类靠色彩
- 卡片是画布上唯一鲜艳的元素，更跳

## Color palette

### 系统色 — 深色画布
| Role | Hex | Use |
|---|---|---|
| Page bg | `#1a1816` | 整页一块连续暖深灰 — 不是纯黑 `#000`（太硬）也不是冷灰（不够暖）|
| Header — title | `#fefcf6` | 主标题白字 |
| Header — meta | `#9a8d75` | 副标题、灰字 |
| Header — accent | `#d97a3a` | 总里程/海拔的橙红强调（暗底上自然跳出）|
| Map — route | `#9a8d75` | 主路线（暖灰，融入画布而非喧宾夺主）|
| Map — train return | `#5a5045` | 虚线返程（更暗，次级视觉）|
| Map — city name | `#fefcf6` | 城市名白字 |
| Map — caption | `#7a6f60` | 海拔、距离、火车返程 label 等暖灰 |
| Map — stop stroke | `#1a1816` (= page bg) | **关键技巧** — 站点圆点用页面底色描边，让色块"嵌"入画布而不是"贴"上去 |

### 七天主色
| Day | 主色 | 暗色（水印 + chip）| 浅色（脚注）|
|---|---|---|---|
| D1 钴蓝 | `#5b8cb5` | `#4a7aa0` | `#dde8f1` |
| D2 金黄 | `#e6a13a` | `#c88a25` | `#fef0d8` |
| D3 砖红 | `#c44d3e` | `#a83a2c` | `#f7d7d2` |
| D4 青绿 | `#3d8b85` | `#2d716c` | `#c5e1de` |
| D5 橄榄 | `#5a7a3a` | `#4a6628` | `#d2dec0` |
| D6 葡萄紫 | `#6b4f7a` | `#563d62` | `#d8c8de` |
| D7 落日橙 | `#d97a3a` | `#b86028` | `#f7dcc4` |

如果行程超过 7 天，可循环或扩展色板（建议不超过 9 天）。

## Layout — viewBox 720 × N

7 天行程参考高度 ≈ **2360**。每多一天约 +250。

```
y 0 — 180    Header (text on page bg, no separate rect)
y 180 — 560  Map area (no bg, fully merged with page)
y 580 — 2333  Day cards (each ~232 tall, with chips + bullets + footer note)
```

**没有底部出行提示 section，没有页脚版本号** — 终点是最后一张 day card。精简优先。

### Header (180 tall, on page bg)
- 整段文本直接落在页面 `#1a1816` 上，**没有单独的 header rect**
- y=56: 主标题，font 30, weight 700, white
- y=82: 副标题，font 12, color `#9a8d75`，格式：`节气 · 天数自驾 · 主要国道`
- y=50 right: 总里程 `1,750 km` font 22, weight 700, color `#d97a3a`
- y=80 right: 总海拔 `▲ 3,820 m` font 18, weight 700, color `#d97a3a`
- y=148: 路线流向 `城市A  ·  城市B  ·  城市C  ·  ...` font 13 color `#7a6f60` — 直接落在页面，**没有底色条**

### Map (380 tall, no bg, fully transparent on page)
- **不画地图区背景 rect** — 路线、站点、标签都直接落在页面 `#1a1816` 上
- 左上 (50, 220) 小指南针：`fill="none"` 圆 + 暖灰指针 `#a89e8c` + 暖灰 N 字
- 右上 (680, 210) `ROUTE MAP` eyebrow color `#5a5045`
- 路线 `path stroke 2 color #9a8d75 linecap round` —— 暖灰，不要纯白也不要彩色，目的是融入画布
- 火车返程 `path stroke 1.2 color #5a5045 dasharray "6 5"` — 比主路线更暗
- 距离标签 italic 10pt color `#7a6f60`
- 城市名 font 13-14 weight 700 white，海拔 font 9 color `#7a6f60`
- 主驻留点：圆 fill 当日色 + **stroke `#1a1816` (页面底色) width 3**
  - 起 / 终点（西宁 1·7）r=11 + 圆心白色文字 D# 数字
  - 普通驻留点 r=10
- 路过点（如水上雅丹）：r=6 fill `#1a1816` + stroke 当日色 width 2
- 水体提示（青海湖）：`#3a6a8a` opacity 0.4 椭圆，作为非常 subtle 的地理锚点

### Day cards (~232 tall, x=60-660)
- 全卡填充：`rect rx=10` 当日主色
- **大数字水印**：`text x=570 y=195 text-anchor=end font-size=160 weight=800 opacity=0.55` 当日暗色
- y=40: `D{N}` font 16 weight 700 white
- y=40 next to D#: 日期 font 12 color 当日浅色
- y=78: 标题 font 22 weight 700 white
- y=96-120: 胶囊 chip 横排（每个高 24, rx=12, fill 当日暗色, white text）
  - chip 内容：`📍 280 km` / `▲ 3,820 m` / `⏱ 5-6 h` 等
- y=148, 170, 192, 214: bullet 行 font 13 white
- y=240/218 视高度: 卡片底部脚注 font 11 当日浅色（避坑提醒 / 加油提醒 / 额外信息）

每两张卡之间留 18px 空隙。空隙处露出页面 `#1a1816` 深底，自然分块。

## Principles

1. **整页一块深色画布** — 页面 / 地图 / 卡片间隙都是同一个 `#1a1816`，没有独立的"图区""tips 区"。这是这一风格的核心识别点。

2. **站点描边用底色** — 站点圆点的 stroke 必须是页面底色 `#1a1816`，不是白色。这是让色块嵌入暗底的关键技巧。如果用白色描边，站点会有"贴上去"的感觉；用底色描边，站点像挖空的洞，融合度高得多。

3. **路线非纯白** — 暖灰 `#9a8d75` 比白色 `#fefcf6` 更融入暗底。如果路线用亮白，会喧宾夺主，把视线从卡片上拉走，破坏整体的"卡片才是主角"的层次。

4. **大数字水印是核心视觉** — 每张卡右下角浮一个 160pt 半透明大数字，是这一风格的视觉签名。必须 `opacity 0.55` 才不会喧宾夺主。

5. **Chip 强化数据** — 所有量化信息（km, m, h）都包成胶囊。chip fill 必须用当日暗色 + 白字，保持对比。**绝不**用浅色 chip + 深色文字，那会显廉价。

6. **分类化 emoji** — emoji 不只是装饰，而是分类信号（食物 🍜 / 山 ⛰️ / 床 🏨 / 车 🚗 等）。每个 bullet 一个，卡片底部脚注不带 emoji。

7. **白字 on 色块** — 卡片正文全部白字，脚注用当日浅色（不是灰色——浅色保持卡片色相统一）。

## Use cases
- 微信群 / 朋友圈分发，需要一眼吸睛
- 攻略型旅行，重信息密度
- 多日高强度，颜色区分天数有用
- 多人同行，每个人在群里只看自己关心的那一天
- 想要"专业感""设计感"的最终交付

## Anti-patterns（避免）

- 给地图加单独的背景 rect / 加 header 单独的 rect — 破坏沉浸感
- 站点描边用白色 — 破坏融入感（站点像贴纸而非画布的一部分）
- 路线用纯白 `#fefcf6` 或彩色 — 喧宾夺主，让卡片失去焦点地位
- 用纯黑 `#000` 而不是 `#1a1816` — 太硬太冷，缺暖度
- 卡片颜色饱和度过高 — 这套色板已是降饱和过的色，更加饱和会显廉价
- 大数字水印不透明 / opacity 太低 — 必须 0.5–0.6 区间才不喧宾夺主
- chip 用浅色背景 — 必须深 chip + 白字
- 加阴影 / 渐变 — 这一风格是 flat design，没有 3D 元素
- 加底部出行提示 / 加版本水印 / 加底部 footer — 精简优先，止于最后一张 day card
- 加边框 / 装饰花边 — 整套设计靠色块和留白说话
