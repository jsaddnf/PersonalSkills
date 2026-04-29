---
name: route-book
description: Create polished trip route books (路书) for self-driving and multi-day trips — with daily itinerary cards, distance & elevation data, scenic spot bullets, and a stylized route map. Two visual styles bundled — minimal editorial (clean, calm, cohesive) and colorful infographic (vibrant, high-density, scannable). Use this skill whenever the user asks to plan a road trip, design an itinerary graphic, build a 路书/攻略图/行程总览, summarize travel plans visually, or prepare a trip overview to share with traveling companions. Especially trigger on mentions of specific Chinese self-drive routes (青甘小环线, 滇藏线, 川西环线, 新疆独库, etc.) or generic phrases like 自驾, 路书, 行程, 攻略, road trip, itinerary.
---

# Route Book Generator

A skill for generating polished trip route books as paired SVG + PNG deliverables, covering daily itinerary, stylized route map, distance & elevation, scenic highlights, and trip-prep tips.

## What "good" looks like

A route book that:
- A traveling companion can read on their phone in 30 seconds and understand the whole trip
- Shows the geography clearly enough that they can mentally place themselves on the route
- Lists each day's main attractions/passes/lodging without overwhelming detail
- Calls out anything time-sensitive (high-altitude days, ticket booking deadlines, longest driving day)
- Looks tasteful — not a copy-paste template

## Workflow

### 1. Gather trip info (one batch, use AskUserQuestion if available)

Ask in one round:
- 出发日期 + 天数
- 每天的主要城市/驻留点
- 人数 + 车型（如果是自驾）
- 风格偏好 — A 简约 / B 彩色 / 让 Claude 推荐

If the user has already provided enough info above (e.g. they pasted a full itinerary), don't re-ask — just confirm the gaps.

### 2. Pick a style

Two styles ship with this skill — see `references/style-a-minimal.md` and `references/style-b-colorful.md` for full specs. Quick guide:

| Use case | Recommend |
|---|---|
| Microsoft 群里发出去给同行人看 | B 彩色（信息密度高，扫读性强）|
| 自己收藏 / 长期保存 / 慢节奏旅行 | A 简约（编辑感，安静）|
| 高强度多日自驾，颜色区分天数有用 | B 彩色 |
| 情绪型 / 沉浸型 / 单一目的地 | A 简约 |

If the user is undecided, recommend B for sharing scenarios, A for personal use.

### 3. Build the SVG

Read the relevant style spec from `references/`, and use the matching sample in `assets/` as a structural reference. The samples are the actual qinggan-loop-7day route book — they're real, working SVGs you can study line by line.

**Critical layout rules across both styles:**
- ViewBox width 720, height variable based on # of days (rough budget: header + map + cards × N + tips ≈ 2050 for 7 days minimal / 2580 for 7 days colorful)
- Font stack: `'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif`
- Map should preserve approximate real-world geography — east cities right, west cities left, north cities up
- Distance labels in italic small font; place along the route segments without overlapping city labels
- Mark only high-altitude passes (>3500m) with small triangle markers
- Don't over-decorate the map with province boundaries, terrain, etc. — they tend to clash with route labels

### 4. Render to PNG

Use `scripts/render_png.py` (depends on `resvg-py`, install with `pip install resvg-py --break-system-packages`):

```bash
python3 scripts/render_png.py input.svg output.png --width 1440
```

1440px width is a good balance for WeChat/微信 sharing. For higher quality, use 2160.

If `resvg-py` isn't available and you can't install it, the SVG is still the deliverable — tell the user to open it directly on their Mac (Safari, Preview, or Quick Look will render it perfectly with PingFang and Apple Color Emoji).

### 5. Deliver

Provide both files via computer:// links:
- `.svg` — master file (renders perfectly on macOS with PingFang + Apple emojis)
- `.png` — universally viewable, ready to share

In your reply, briefly note the rendering trade-off if relevant (e.g. "Linux 渲染的 PNG 里 emoji 显示成空方框，刚好当 bullet marker 用，不影响阅读；要正版 emoji 直接打开 SVG").

## Iteration etiquette

Trip-book design is opinionated work. Expect 3-5 revision rounds. After each delivery, ask the user concretely:
- 颜色 / 字号 / 间距 — 哪里别扭？
- 内容 — 漏了什么 / 多了什么？
- 排版 — 想加 / 删 哪个 section？

Don't ship without preview. Before saving the final SVG file, render via show_widget so the user sees and approves first.

## Common pitfalls to avoid

- **不要凭空编造数据** — 海拔、距离、餐厅名等如果用户没给，要么省掉要么明说"待补"。瞎编可信度极低、还可能误导。
- **不要时间敏感的硬约束** — 比如"9/6 8:00 抢莫高窟票"——这只在写图的时刻成立，过段时间再用就过期了。这类信息留给单独的行前清单文档。
- **不要堆 emoji** — 简约风每条 bullet 1 个，彩色风每行最多 1 个。不要 🔥💯⭐️🎉 这种装饰性堆叠。
- **不要让地图太挤** — 省名/边界/地形 容易和路线、距离、地标 冲撞。地图区只放：路线 + 节点 + 距离 + 高海拔垭口 + 必要的水体提示（如青海湖）。
- **不要忘记给用户最终成品** — 计算路线、写完文案后，必须真正把 SVG 文件写到工作目录、转 PNG、提供 computer:// 链接。

## File map

```
route-book/
├── SKILL.md (this file)
├── references/
│   ├── style-a-minimal.md     # 简约风格完整规范
│   └── style-b-colorful.md    # 彩色风格完整规范
├── assets/
│   ├── sample-minimal.svg     # 完整工作样例（青甘小环线 简约版）
│   └── sample-colorful.svg    # 完整工作样例（青甘小环线 彩色版）
└── scripts/
    └── render_png.py          # SVG → PNG 转换脚本
```
