# 定制绘本制作手册

从「一句故事梗概」到「一个可翻页的网页绘本」的完整流程。
写给单机 Windows + NVIDIA 的环境（原来是 Mac 出图 + 拼装，现已全部合并）。

已用这套流程做出 8 本：森林里最大的花、蚂蚁要搬家了、恐龙没有走远、
海只来一点点、寄居蟹换了新房子、晚上地球转过去了、我住在一颗星星旁边、种子去旅行。

---

## 零、全流程

```
① 你给梗概        "他去海边，但他有点怕海"
        ↓
② 写脚本          story_sea.json —— 10 页中文旁白 + 英文画面词
        ↓
③ 试 1 页         换了画风必做，确认风格对了再跑全本
        ↓
④ 跑全本          10 张 1024×1024 PNG，约 16 分钟（8GB 笔记本实测）
        ↓
⑤ 审图            ★ 最容易被跳过、但最该做的一步，见第四章
        ↓
⑥ 重跑问题页      一般 1–3 页
        ↓
⑦ 合成网页        build_web.py → 自包含 HTML
        ↓
⑧ 发布            Artifact 拿链接，或直接本地打开
```

一本书的实际耗时：脚本 10 分钟，出图约 16 分钟（每页 80–120 秒，挂 LoRA 的页慢一些），
审图 10 分钟，重跑 5 分钟，合成 2 分钟。**约 45 分钟**，出图占三分之一，其余是审图和重跑。

---

## 一、环境

### 1.1 拉仓库

```bat
git clone https://github.com/PatrickSun93/imageGen
cd imageGen\storybook
```

仓库里有：全部脚本（`story_*.json`）、合成工具（`build_web.py`）、
ComfyUI 工作流（`..\workflows\`）、以及本手册。
**模型权重和图片不在仓库里**，要自己下。

### 1.2 ComfyUI + Flux

详细步骤见 `..\FLUX_ON_8GB.md`。要点：

| 文件 | 放到 | 大小 |
|---|---|---|
| `flux1-dev-Q4_K_S.gguf` | `models\unet\` | 6.8 GB |
| `t5xxl_fp8_e4m3fn.safetensors` | `models\text_encoders\` | 4.9 GB |
| `clip_l.safetensors` | `models\text_encoders\` | 246 MB |
| `ae.safetensors` | `models\vae\` | 335 MB |

还要装 GGUF 节点：

```bat
cd ComfyUI\custom_nodes
git clone https://github.com/city96/ComfyUI-GGUF
..\..\venv\Scripts\pip install gguf
```

显存 8GB 够用（实测占 6.5–7.5 GB）。不够就：换 T5 的 GGUF 版 →
ComfyUI 加 `--lowvram` → 降到 768×768。

### 1.3 人物 LoRA

`son_ohwx_flux_v1`，触发词 `ohwx boy`，出图强度 **1.3**。

要重训见 `..\FLUX_ON_8GB.md` 第五章（用 kohya sd-scripts：`lora_training\train_flux_sdscripts.sh`，
1000 步约 1h20m；ai-toolkit 在 8GB 上约 30 秒/步，已放弃）和
`..\lora_training\RETRAIN.md`（素材筛选标准）。
**SDXL 的 LoRA 在 Flux 上用不了**，架构不同，必须用同一批照片重训。

素材照片不在仓库里（私人照片），但 `lora_training\raw\` 的标注写法
在 `RETRAIN.md` 里有说明和示例。

### 1.4 合成端

只要 Python + Pillow，用仓库根目录的 venv（这台机器的 venv 是 conda 结构，
`python.exe` 在 `venv\` 根目录，不在 `Scripts\` 里）。下面所有命令都在仓库根目录执行：

```bat
venv\python.exe -c "import PIL; print(PIL.__version__)"
```

---

## 二、写故事脚本

### 2.1 story JSON 的字段

```json
{
  "title":     "海只来一点点",
  "subtitle":  "浪来了，又回去了",
  "slug":      "sea",
  "character": "wearing a pale yellow t-shirt and orange shorts, bare feet, short black hair",
  "style":     "children's picture book illustration, gentle watercolor painting, ...",
  "neg_extra": "stormy, huge crashing waves, dark water",
  "keyword":   "潮池",
  "style_label": "清透水彩",
  "palette":   { "ink": "#1f3a42", ... },
  "pages": [
    { "n": 1, "zh": "我第一次来海边。\n海好大好大……", "scene": "A little boy stands …", "has_boy": true }
  ]
}
```

| 字段 | 作用 |
|---|---|
| `character` | **全书统一的穿着**。不写的话 LoRA 每页随机抽一件衣服，翻页时绿T黄衫轮着来 |
| `style` | **全书统一的画风**，见 2.3 的配方表 |
| `neg_extra` | 这本额外要挡的东西，追加在通用负面词后面 |
| `seed_base` | 书号 ×1000，每页 seed = `seed_base` + 页码（见 3.2）。不写就按 2000 算，会和蚂蚁那本撞号 |
| `keyword` | 正文里写成 `「潮池」` 的词会在网页上高亮，一本书用一个 |
| `palette` | 网页配色，14 个色值（7 个浅色 + 7 个 `_d` 深色） |
| `zh` | 念给孩子听的，`\n` 换行 |
| `scene` | 喂给模型的英文，**和 `zh` 不用一一对应** |
| `has_boy` | 这页要不要挂 LoRA、要不要带 `ohwx boy` |

### 2.2 故事怎么编

**10 页。** 少于 8 页讲不完，多于 12 页孩子坐不住。

**用「熟悉 → 绕远 → 揭示」的结构。** 这是最好用的一个：

```
第 1 页   一个他生活里见得到的东西      博物馆的恐龙骨架
第 2-8 页 绕开去讲一段他不知道的事      远古、灭绝、羽毛、幸存
第 9 页   揭示：那个东西就是这个        鸟就是恐龙
第 10 页  回到他身上，他做点什么        在院子里撒面包屑
```

《恐龙没有走远》《我住在一颗星星旁边》都是这个结构，效果最好。
最后一页一定要**让他有个动作**，不要只是感叹。

**旁白要长。** 四岁孩子的绘本每页 3–5 短句，不是一句。
早期做的几本旁白太短，实测念起来撑不住一页。

**一本书只教一个概念。** 寄生、演化、自转、潮汐、种子传播——一个就够。

**有情绪的题材要给出口。** 《海只来一点点》是给怕海的孩子写的，
逻辑不是「海不可怕」，而是让海变得**可预测**：浪每次都停在同一条线上 →
他数拍子 → 他能预测 → 恐惧降级。**结尾不给完成任务的压力**：
不是「他下水了」，是「明天我还来」。

### 2.3 画风配方（全部验证过）

| 画风 | `style` 值 |
|---|---|
| 水彩 | `children's picture book illustration, storybook art, soft watercolor painting, gentle rounded lineart, warm pastel colors, flat shading` |
| 清透水彩 | `children's picture book illustration, gentle watercolor painting, soft sea green and warm sand palette, loose wet washes, lots of white paper showing, calm soft daylight` |
| 蜡笔 | `children's book illustration drawn with wax crayons on textured paper, chunky crayon strokes, visible waxy grain, flat bright colors, naive childlike drawing, thick black outlines` |
| 复古水粉 | `children's picture book illustration, warm vintage storybook art, soft gouache painting, earthy ochre and deep green palette, gentle textured brushwork` |
| 彩铅 | `children's picture book illustration, colored pencil drawing, warm sandy palette with soft coral accents, visible pencil strokes and gentle cross-hatching, soft daylight` |
| 夜色粉彩 | `children's picture book illustration, soft chalk pastel painting, deep indigo night and warm cream palette, gentle grain, quiet glowing light` |
| 复古丝网印 | `children's picture book illustration, retro screenprint poster style, limited palette of deep navy teal and warm orange, flat simple shapes, subtle paper grain` |
| 剪纸拼贴 | `children's picture book illustration, cut paper collage, textured handmade paper, warm earth tones with fresh green, layered flat shapes` |
| 水墨淡彩（Qwen） | `children's picture book illustration, Chinese ink wash painting with soft watercolor tints on textured rice paper, gentle grey, blue and green washes, simple shapes, lots of empty paper` —— 右下角常出假印章，用 `clean_seal.py` 抹掉 |
| 木刻版画（Qwen） | `children's picture book illustration, linocut print on cream paper, bold carved shapes, limited palette of warm orange, sky blue and black ink, visible ink texture and paper grain` |
| 马克笔（Qwen） | `children's picture book illustration drawn with bright felt-tip markers on white paper, bold black outlines, flat vivid colors, simple cheerful shapes, visible marker strokes` |

**规律：画风词要指向一个成熟画种，并且给它一个物理载体。**
`crayon drawing` 太抽象，出来是照片人物配蜡笔背景；
`drawn with wax crayons on textured paper` 才压得住。

**每本换一个画风。** 排在一起才像一套书而不是一批插图。

### 2.4 镜头节奏

```
远景开场 → 推近 → 中景 → 特写（视觉高潮）→ 拉远收尾
```

控制比例**要用镜头术语**，不要写形容词。扩散模型不做尺寸推理，
写 `the size of a grain of rice` 它根本不理会：

| 想要 | 该写 | 别写 |
|---|---|---|
| 物体小、人全身 | `wide shot, full body` | `small ants` |
| 物体占满画面 | `extreme close up`, `macro` | `large ants` |
| 人物半身 | `medium shot, upper body` | — |

代价：镜头词会挤占内容描述的权重，次要物体更容易丢。是个取舍。

---

## 三、出图

### 3.1 Flux 参数（照抄）

```
模型      flux1-dev-Q4_K_S.gguf          UnetLoaderGGUF
CLIP      t5xxl_fp8_e4m3fn + clip_l      DualCLIPLoader, type=flux
VAE       ae.safetensors
LoRA      son_ohwx_flux_v1   strength 1.3
latent    EmptySD3LatentImage 1024×1024   ← 不是 EmptyLatentImage
采样      20 步 / CFG 1.0 / euler / simple
引导      FluxGuidance 3.5
负面      见 3.3
```

**四个和 SDXL 不一样的地方**：latent 节点不同（Flux 是 16 通道）；
CFG 固定 1.0，强度改用 FluxGuidance；步数 20；提示词吃自然语言长句不吃标签堆砌。

### 3.2 提示词怎么拼

```
有人物的页（has_boy: true）：  ohwx boy, {character}, {style}, {scene}     挂 LoRA
没人物的页（has_boy: false）： {style}, {scene}                            不挂 LoRA
```

**绝对不要在提示词里描述五官。** 写 `black eyes` `round face` 之类
会覆盖 LoRA 学到的脸——这是最容易犯的错，早期几本人物不像就是因为这个。

**seed 用「书号 ×1000 + 页码」。** 已用：蚂蚁 2000、恐龙 3000、
海边 4000、寄居蟹 5000、夜晚 6000、星星 7000、种子 8000、雨 9000、影子 10000、
毛毛虫 11000、交通 12000、挖掘机 13000、走丢 14000、身体 15000、生气 16000。新书往后排。
重跑某页时用 **原种子 +100**，避免复现同样的构图。

### 3.3 负面提示词

Flux dev 是蒸馏模型，CFG 固定 1.0。**CFG 为 1 时 ComfyUI 根本不计算负面分支，负面词完全不起作用**
——2026-09-10 那批五本书写了 `signature`，crab 第 2 页、night 第 2/5 页照样出了签名。
负面词只作记录；要改画面，写正面描述（「画面里有什么」），见 4.3。
真要负面词生效，只能换能跑真 CFG 的模型（例如 Qwen-Image 的完整模式，CFG 4）。

通用：
```
character sheet, model sheet, multiple views, grid, collage, text, watermark,
signature, blurry, deformed hands, extra fingers, photorealistic face
```

**千万别写 `real child` / `realistic skin` / `photo`。** LoRA 学的就是真实小孩，
这些词会把人物本身一起否掉——试过一次，画面里男孩直接变成一只绿色大虫子。
负面只挡**画种**（watercolor / oil / 3d / airbrush），不挡人。

### 3.4 先试 1 页

**换了画风必做。** 挑一页有人物的跑一次，确认：画风对不对、人像不像、
衣服对不对。对了再跑全本，否则 10 页白跑。

### 3.5 输出

`page_01.png` … `page_10.png`，1024×1024，由 `render_lora.py` 放进 `storybook\out\<slug>_lora\`：

```bat
venv\python.exe storybook\render_lora.py storybook\story_sea.json         :: 全本
venv\python.exe storybook\render_lora.py storybook\story_sea.json 1 4     :: 只重跑这几页
```

需要 ComfyUI 先跑在 `127.0.0.1:8188`。页里写了 `seed` 就用页里的（重跑 +100 时这样写），
否则用 `seed_base` + 页码。长时间出图要用独立进程启动，否则内存吃紧时会被系统停掉。

### 3.6 另一个选择：Qwen-Image（《海只来一点点》用的就是它）

2026-09-10 做过同页对比，Qwen-Image-2512 在这几件事上明显强过 Flux：
画面里只写了什么就只画什么（太阳页不再冒出月亮）、光照跟着 scene 走而不是被 style 压暗
（白天的天空是真蓝）、排队和数数更准、能画出真正的蜡笔颗粒。

| 页 | 用什么 | 每页耗时 |
|---|---|---|
| 没有他 | Qwen-Image-2512 Q4 + Lightning 8 步 LoRA，CFG 1 | 约 80 秒 |
| 有他 | Qwen-Image-Edit-2511 **Q3_K_M** + Edit Lightning 8 步，拿**两张他的照片**当参考图，不用 LoRA | 约 3 分钟 |

```bat
venv\python.exe storybook\bakeoff_qwen.py lightning8 storybook\story_sea.json:4
:: 两张他的照片先放进 ComfyUI\input\（照片不进仓库），文件名换成你自己的
venv\python.exe storybook\edit_qwen.py --v2 照片1.png 照片2.png storybook\story_sea.json:1
```

几条要记住的：

- **Edit 的提示词要直接点名参考图**：`Picture 1 and Picture 2 show the same little boy. Draw exactly this boy…`
  （`--v2`）。写成 Flux 那种长串关键词，画出来是棕发、年纪大的油画男孩。
- **两个 Qwen 模型不能同时加载**（合起来约 36 GB）。先出完所有有他的页，`/free` 清内存，再出其余页。
- **Edit 用 Q3_K_M（9.9 GB），别用 Q4_K_M（13 GB）**：Q4 + 文本编码器 9.4 GB 会把 32 GB 内存用满，
  只要再开一个占 6.7 GB 的程序（比如 sonictype），每页就从 3 分钟掉到 20 多分钟（一直在从硬盘读模型）。
  2026-09-11 实测 Q3 在同样条件下每页 192 秒，画质看不出差别。工作流默认已经是 Q3。
- **印刷类画风（孔版印刷、复古网点）的没人物页会画成「加了滤镜的照片」**，机器、红绿灯这类题材尤其明显；
  水墨、木刻、马克笔这类有实物画材的画风没这个问题。解决办法是 `restyle_ref`：在 story JSON 里写
  `"restyle_ref": 4`（一页已经画好的有他的页），`render_qwen_books.py` 会先出文生图底稿，再用 Edit 模型
  「按 Picture 2 的画风重画 Picture 1」（`edit_qwen.py --restyle`），构图来自底稿，画风来自样板页。
  提示词里一定要带上本书的 style 描述，只写画面内容会变成光滑的电脑插画。每页多花约 3 分钟。
  **别直接拿样板页当参考图画新页**（`--style`）：Edit 模型会把样板页的整个构图照搬过去，
  挖掘机页出来的是那页的游乐场，只是把男孩换成了挖掘机。
- **缺点**：颜色比 Flux 浓，不太「清透」；「一张图里画一个过程」会切成三格连环画；
  对「浪停在他脚前」这种否定式的动作不太听话（海边第 3 页他坐进了水里）。

---

## 四、审图 ★

**这一步不能跳。** 8 本书的经验：平均每本有 1–3 页需要重跑，
而且问题往往不是「画得丑」，是**画的内容和旁白对不上**——
出图时看着挺好，拼成书念给孩子听才发现逻辑断了。

### 4.1 做一张联系表一次看全

```bat
venv\python.exe storybook\contact_sheet.py storybook\out\sea_lora
```

### 4.2 逐页对着旁白核六件事

- [ ] **文图相符** —— 旁白说「壳太小了」，画出来是不是真的小？
      旁白说「我抓紧了爸爸的手」，爸爸在不在画面里？
- [ ] **没有多余人物** —— 不挂 LoRA 的页经常凭空冒出小孩剪影
- [ ] **没有假签名** —— 模型会模仿画作在右下角签个花体名字
- [ ] **构图不空** —— 极简场景 + 「大量留白」的画风词会让画面空掉一大半，
      看起来像没画完
- [ ] **角色一致** —— 衣服、脸、年龄；配角（爸爸）要明确是成年人
- [ ] **概念画对了** —— 科普页最容易出错，见下表

### 4.2b 分工原则：示意图交给程序，场景交给模型 ★

2026-09-13 全库重审 48 本约 560 页，**165 页画的和旁白对不上**，而且压倒性地集中在
**示意图页**——箭头方向、对比两格、边数、数目、局部结构；场景页（人物、动物、风景）
出错少得多。示意图的价值恰恰在于精确，而这是这个模型系统性做不到的。

证据：`tens` 和 `minus` 的示意图页改用 `draw_math.py` 程序画之后，复审全部通过；
同样这些页交给模型画了四轮都不对（十根画成十一二根、八个画成六个）。

所以：

- **需要精确数目、方向、边数、刻度、对比的页 → 用程序画**，别和模型缠斗。
  基线做法：整数栅格；尺寸放不下就**抛异常**而不是挤压（挤压会让十根糊成条形码）；
  每页打印「3 捆 ×10 根 + 4 根散」这样的构造清单，**核对数字而不是数图**。
- **人物、动物、风景、情绪 → 交给模型**，这是它的长处。

审图时也照这条分：示意图页核对数字和方向，场景页核对主体身份和安全信息是否画反。

### 4.2c 画「场」和「流向」：必须有出入点和走向箭头 ★

磁力线、水流、气流、电流这类图，**光把几何画对没用**：任何首尾相接的曲线都会被
读成「环」。地球磁场那页连错三次才收口——

1. 模型画成**土星环**（给球套了一圈赤道环）
2. 改用程序画，画成三个**同心椭圆** → 还是环
3. 再改成两端收拢到南北极的弧 → `sin(πt)` 在两端归零、端点重合，左右一对称就成了
   **眼睛形的闭环** → 仍然是环

真正管用的做法：

- 弧线的**起点和终点分处不同位置**（北半球某纬度出发 → 南半球对应纬度回来），
  绝不让两端收拢到同一点；
- 每条弧上**加一个走向箭头**；
- 需要的话再标出出入点（两极各点一个记号）。

同理，「水从嘴进、从鳃出」「电从插座出、绕一圈回插座」这类页，**方向必须由箭头
说清楚**，否则画出来就是一团管子。

### 4.2d 扁平几何画不出「立体结构」——该退就退 ★

程序画对「数目、方向、边数、比例」是碾压式的，但对**立体结构**无能为力。
2026-09-13 有三页都是同一个剧本：参数怎么调都不对，最后退成简化画法才收口。

| 页 | 想画的立体结构 | 反复画成 | 最后怎么收 |
|---|---|---|---|
| magnet p9 | 地球磁场的三维弧线 | 土星环 / 同心椭圆 / 眼睛形闭环 / 尖角橄榄（四版） | 退成「地球 + 地轴 + 指南针」，磁力线交给旁白 |
| hiccup p2 | 胸腔里的膈肌 | 一张脸（两只眼一张嘴）/ 歪斜的方盒子（三版） | 退成「躯干轮廓 + 一片肺 + 一条横线」 |
| bee p11 | 一把勺子 | 棒棒糖 / 团扇（三版） | 接受现状——「十二格只填一格」这个信息已经成立 |

**判断法则：信息到位就收手。** 一页图只需要承载旁白里的那一条信息；
「像不像实物」是额外的，不值得第三次返工。具体做法：

- 第一次不对 → 改参数；第二次不对 → **换构图**（正面对称 → 侧视、整体 → 局部）；
  第三次不对 → **退成最朴素能表意的画法**，或直接接受。
- 正面对称构图（方框 + 两个圆 + 一道横弧）几乎必然读成人脸，从一开始就别用。
- 任何首尾相接的曲线都会被读成「环」，画场和流向必须有出入点和走向箭头（见 4.2c）。

### 4.2e 程序画的页要「正文 + 构造清单」并排核对 ★

程序画保证了数目和方向，但保证不了**这页画的是不是这页要讲的事**。
《一封信怎么寄到》整本的示意图错位了一页：p3 画了 p2 的内容、p4 画了 p3 的、
p6 画了 p5 的。根因是写 `@page(slug, n)` 时顺着正文往下编号，**漏算了中间的场景页**。

这种错位有两个特点，都让人查不出来：

- **页码集合是一致的** —— story JSON 的 `diagram_pages` 和代码注册的页号完全相同，
  比集合查不出任何问题；
- **每页单独看都是对的** —— 每张图本身画得没错，只是挂在了错误的页上。

唯一管用的查法是把两样东西**并排打出来**：

```python
# 抓每个 @page 后面那句 docstring，和 story JSON 里同一页的 zh 并排显示
for p in story["pages"]:
    if doc := docs.get((slug, p["n"])):
        print(f'p{p["n"]:02d} 正文: {p["zh"][:34]}')
        print(f'     画的: {doc}')
```

这样一眼就看出「正文讲地址从大到小、画的却是信封三块区域」。

### 4.2f 模型返工的止损线：同一页第二次还错，就别再让它画 ★

2026-09-13 第五批 9 本共 **22 页返工页**（第一轮复审判错、换了场景词重画），
第二轮复审 **17 页仍然错，命中率 23%**。更要紧的是：这 17 页的错法和第一轮**一模一样**，
换措辞、换构图都没动摇它——说明这不是提示词没写好，是这类页超出了模型的能力。

| 错法 | 这轮的例子 | 根因 |
|---|---|---|
| 画面自带纸底纹 | wind p8 撕边纸、sleepwin p7 卷边旧纸、doctor p7 浮在纸卡上 | 画风词里的 paper / collage / pastel on paper 会被当成**画面内容**而不是画法 |
| 乱码假字 | post p4 告示牌、post p9 信箱铭牌、paper p9 假手写 | 画面里只要有可写字的平面，模型就要往上写 |
| 主体变成「摊开的书」 | paper p6 / paper p9 / doctor p5 | 主体本身就是纸、信、圆片时尤其严重；**换画风词救不回来**（paper 这本换过一轮仍然出书） |
| 确数画错 | thunder p7 竖三根手指画了五根、share p1 六块饼干三个人画成四块四人 | 数目一直是模型的系统性短板（见 4.2b） |
| 年龄比例 | doctor p2 成年医生画成穿白大褂的小孩 | 童书画风会把所有人画成孩子 |

所以定一条止损线：

- **同一页让模型画第二次还错，就不要第三次。** 按页的性质改判：
  示意图页 → 交给程序（这轮 12 页这么处理）；他本人出镜的页 → 只能留给模型，
  但必须改写场景词（下面三条）。
- **程序画的人物靠比例说明年龄，不靠画风。** doctor p2 按 6.8 个头画（小孩只有 4~5 个），
  再加眼镜和听诊器；构造清单里直接把头身比打出来，核对数字而不是核对「像不像大人」。
- 程序画一个由多块拼成的东西（手、动物），**整体用一条闭合轮廓画完**，
  别拼圆角矩形——拼出来内部全是接缝，深色底上会散成几块（thunder p7 第一版就是这样）。

他出镜的页改场景词，这轮验证有效的三条：

1. **不想要的东西一个字都别提。** 「太阳在他背后」写成 no sun 只会招来太阳；
   改成写他脚下**朝着彩虹伸出去的长影子**——影子蕴含了太阳的位置，而画面里没有太阳可画错。
2. **别要求确数。** 「桌上六块饼干、三个人」改成「一盘饼干 + 两个同伴」，
   确数交给同一本里程序画的那几页去承载。
3. **别要求手部确数。** 「竖三根手指」改成「一只手五指张开」（五指是手的自然形态，
   模型画得出），或者整页改判给程序。
所以每个页面函数都要写一句 docstring 说明这页画什么——它不是注释，是校验用的。

### 4.3 常见失败模式（都真实发生过）

表里「负面加 …」对 Flux（CFG 1.0）是无效的，只作记录（见 3.3）；真正起作用的是正面描述那一半。

| 现象 | 原因 | 怎么改 |
|---|---|---|
| 太阳画成月亮 | scene 里写了 `dark starry background` + `not fiery` | 强调 `radiating light rays`、`no craters`，去掉夜空 |
| 地球长出行星环 | scene 里写了 `a curved arrow around it` | 删掉箭头；负面加 `rings, saturn, ribbon, band` |
| 月亮长出卡通脸 | 模型对 moon 的先验里有「人脸月亮」 | 负面加 `face, eyes, eyelashes, man in the moon` |
| 右下角有手写签名 | 模仿画作签名 | 负面加 `signature, handwriting`；或事后本地抹掉 |
| 空景页冒出人影 | 画面太空，模型自己补主体 | 场景写满一点；负面加 `person, figure, silhouette` |
| 画面七成是空白 | 极简 scene + `lots of white paper showing` | scene 里明确要求把地平线/海面放进画面，负面加 `blank page, unfinished` |
| 「爸爸」画成少年 | `a grown-up` 强度不够 | 写 `a grown adult man with an adult face and adult build, much larger than the child`，并给他**不同的衣服** |
| 大小画反了 | `too big for its shell` 被理解成「壳很大」 | 正面说清楚 `the shell is clearly too small and the body bulges out`；负面加 `large shell, roomy shell` |
| 情绪转折页不够暗 | `style` 里的光照词盖过了 scene | **整段替换 style 的光照词**，在 scene 里写 dark 压不住 |
| 人物每页不一样 | 没写 `character` 字段 | 补上全书统一的穿着 |
| 人不像他 | 提示词里描述了五官 | 删掉所有五官描述 |
| 出成了角色设定图 | `white background` + `full body` 触发了角色表模式 | 正面加 `only one child, single character`，负面加 `character sheet, multiple views` |
| 水墨页右下角盖了红印章（Qwen） | 画风写了 `Chinese ink wash` / `rice paper`，模型模仿国画落款 | `clean_seal.py` 事后抹掉（`render_qwen_books.py` 对水墨书自动做）；章可能很淡（比纸色 r−g 只高 10–25），有时左右两个下角各一个，工具都能处理 |
| 一整本的主体全画成了同一个东西（八颗行星全是土星） | 模型对某个词有强先验：说 `planet` 就画土星，说 `moon` 就画环形山。画风越装饰（彩色玻璃、版画），先验越压得住描述 | **逐页写死「不是什么」**：`one plain round planet with no rings at all`，月亮类再加 `no craters`。审图时**必须逐页核对画面主体是不是这一页文字说的那个东西**——只看画风统一和有没有缺页会漏掉整本级别的错误（这本 12 页里错了 4 页才被用户发现） |
| 有他的页画成了「另一个孩子」，画风也跑掉（Qwen Edit） | 场景太满：一整座积木房子、四分之三侧身、一堆道具。画面里要交代的东西太多，模型顾不上两张参考照片，干脆自己编一个扁平矢量的通用小孩 | 把场景削到只剩「他 + 一件道具」，正面近景、背景留白（`stands facing us, close up, holding one large paper triangle, plain background`）。这样能救回肤色、发型、衣着，但**脸未必救得回来**——`shapes` p12 连试三次都不像本人。**三次为止**：再试是烧 GPU，要么接受，要么把这一页改写成没有他的页 |
| 爸爸的脸和手被涂成绿色、像少年（Qwen） | 画风写了 `limited palette of bright red, green, yellow and navy`，模型连皮肤也只用这几种颜色 | style 里去掉「只用这几色」的说法，加 `every person has natural skin tones`；爸爸写成 `a tall grown adult man with short black hair and natural skin, in a grey jacket and dark trousers` |
| 工程车画成写实机械图（Qwen 文生图） | 机器题材的先验是照片；画风词写 `toy-like` 也压不住 | scene 里写 `a big simple cartoon excavator with chunky rounded shapes`——「cartoon」这个词才起作用 |
| 卡通工程车的玻璃上长笑脸、驾驶座里坐个小孩 | 写了 `cartoon`/`friendly`，模型给车拟人化或补一个主角 | 每辆车写上 `a grown-up driver with a bushy mustache in a yellow hard hat sitting inside its cab`；只写 grown-up 画出来仍像大孩子 |
| 卡通车的车头长出一张笑脸 | 写了 cartoon，模型把车拟人化；只写 grown-up 司机，脸就挪到保险杠上 | 每辆车加一句 `The front of the vehicle is plain painted metal with two small round headlights.`（挖掘机 p4/p5 实测没脸了） |
| 车里的司机、路上的工人都画成小孩 | 卡通画法下人物都偏幼；「一群人」尤其明显 | 车窗写 `dark tinted windows`（看不见车里就不会画错）；人群写 `tall grown-up construction workers, men with bushy mustaches and beards` |
| 画面里凭空多出一排带脸的小车 | scene 里写了泛泛的 `simple cartoon machines behind them` | 背景里的东西写具体：`a yellow excavator and a dump truck with dark tinted cab windows`，或者干脆写空地、砖堆 |
| 整页基本对，只多了一个小东西（多一对触角、车头一张小笑脸） | 模型随手加的细节 | 别整页重画：`storybook/fix_edit.py <图> "Remove the ..."` 用 Edit 模型只改那一处，约 3 分钟（毛毛虫 p5 实测） |
| 两个大人合成了一个人（医生穿着妈妈的开衫） | 同一页两个配角都没写清长相，模型合并了 | 让两人一眼能分开：性别、年纪、发型、衣服都写不同，并写 `two different grown-ups beside him: on one side …, on the other side …`（身体 p6 实测） |
| 妈妈、爸爸每页换一身衣服 | 只有第一页写了衣着 | 大人出场的**每一页**都写同一句衣着，例如 `his mother, a grown adult woman with short black hair in a blue coat` |
| 比喻被画成了实物（「像吹生日蜡烛一样吐气」→ 下巴上贴了一个带蜡烛的小蛋糕） | scene 里写了 `as if blowing out birthday candles`，Edit 模型把比喻当成画面内容 | 比喻只写在中文旁白里；scene 只写动作本身：`puffs out his cheeks, lips in a small O, soft curved lines of air flowing out`。已画坏的用 `fix_edit.py` 去掉那个东西 |
| 示意图页画成了写实场景（地壳示意图→乱石堆、地面裂开的大深沟） | scene 写得像"描述一个场景"，模型就按写实场景画 | 开头写死 `A simple clear side-view diagram, drawn flat and plain:`；物体给形状和排列（`three wide flat stone tiles laid horizontally edge to edge`）；箭头写明数量和方向（`one black horizontal arrow points right … so the two arrows face each other`）；结尾加 `Nothing else in the picture.` |
| 安全类的书画出了灾难场面（房子悬在崖边、碎石掉落） | scene 里出现 `crack/hole/chasm` 这类词 | 只画"轻微"：`the two tiles have just slipped a little`、`a few short wavy vibration lines`、`one short curved motion line on each side of the house`，并明确 `The ground is not broken open and there is no hole or cliff.` 基调是「我知道该怎么做」，不吓孩子 |
| 加了「画面铺满整幅、不是书的照片」还是画成摊开的书（消防员，两稿都中招） | 只要 style 里留着 `printed with rubber stamps` / `risograph` 这类印刷词，模型就会把承载它的纸一起画出来 | **换掉画风词本身**：改成不含纸和印刷概念的说法，例如 `bold flat graphic art with thick hand-inked black outlines and slightly grainy flat fills in warm red, yellow and deep blue`。一次就好了 |
| 整页被画成「桌上摊开的一本书」，看得见书页边和木桌（毛毛虫、消防员先后中招） | style 里写了纸张或印刷载体（`on white paper`、`printed with rubber stamps`），模型把载体当成了要画的实物 | 载体照写，但后面补一句把画面钉死：`the picture fills the whole frame edge to edge, not a photo of a book or a page on a table` |
| 画风跑成写实照片（刮画写成了写实月球摄影） | style 只说了画种名字，没说「不是照片」 | style 末尾加 `flat and graphic, not a photograph and not a realistic rendering`；月亮这本的 8 张示意图内容全对，说明问题只在画风词，示意图模板本身是可靠的 |
| 只有大人的那一页画成了写实素描肖像（脸部细节多、还上了口红），和全书简笔淡彩不搭 | 文生图画"一个成年人"时默认往写实人像走，画风词压不住 | 这类页在 scene 末尾加一句：`drawn in the same plain simple style as the rest of the book: few lines, simple flat face with small dot eyes and no makeup, not a detailed realistic portrait`。有他的页不受影响（走 Edit 模型，照片参考会带住画风） |
| 同一处毛病改了三次描述还是照旧（地震页的墙和土，三稿都有裂纹） | 模型对"怎么表现这个概念"有很顽固的偏好，正面描述压不住 | **改两次不成就别再重画**：留下构图最好的那张，用 `fix_edit.py` 把多余的东西抹掉（"Remove every crack …, keep the tiles and motion lines exactly as they are"）。重画一次约 3 分钟且结果随机，修图一次也是 3 分钟但只动那一处 |
| 安全类的书背景自己加上了破损（墙上一片裂纹、天花板掉灰） | 模型用"破损"来表现灾害，光写「不裂开的地面」挡不住墙 | 把每个背景元素逐项写成完好：`the walls are smooth, clean and completely undamaged, with no cracks and no marks on them`；要表现摇晃，只用会动的小物件（书滑落、杯子翻落、吊灯摇摆）加 motion lines |
| 画风词被当成画面内容（写了"包装上不写字"，桌上就多出一堆空包装袋） | 约束性的词写进了全书 style，模型把名词当成要画的物件 | 这类约束只写进真正有该物件的那一两页 scene，别放进 style |
| 红绿灯红灯、绿灯同时亮 | 模型对红绿灯的先验是三灯都亮 | 按位置写 `its bottom green light glowing and the red and yellow lights above it dark`；还有残留就本地把红灯压暗（红色像素乘 0.4），不必重画 |
| 「中午影子最短」画成长影子（Qwen） | `the sun high overhead` 不够具体 | 按位置写：`a bright round sun sits at the very top center of the picture, straight above his head`，影子写成 `a tiny dark oval directly beneath his sneakers, about the size of his feet` |

### 4.4 重跑

把要改的页写成一个清单（参考仓库里的 `REDO.md`），每页给：
**问题描述 + 整段替换的提示词 + 附加负面词 + 新种子**。
不要只说「这页重跑一下」——说清楚为什么，否则容易换个种子出同样的毛病。

---

## 五、合成网页

### 5.1 压成 base64

图片要内嵌进 HTML（这样是单文件，发给谁都能看）：

```bat
venv\python.exe storybook\pack_images.py storybook\out\sea_lora storybook\out\web_sea
```

10 张 1024×1024 压成 JPEG q82 约 1.4 MB，base64 后约 1.9 MB。
**上限 16 MB**，远远够用。

### 5.2 生成 HTML

```bat
venv\python.exe storybook\build_web.py storybook\story_sea.json storybook\out\web_sea > storybook\out\web_sea\index.html
```

出来的是自包含单文件：内嵌全部图片、Noto Serif SC 字体、
键盘左右键翻页、深浅色自适应、配色取自 story JSON 的 `palette`。

**改文字不用重新出图**，改完 `story_*.json` 重跑这一条命令就行。

### 5.3 发布

双击 `index.html` 就能看。要拿个链接分享，让 Claude 用 Artifact 工具发布。
**注意**：发布出来的页面含孩子的形象，默认是私有的，
要给家里人看从页面右上角分享，别公开。

---

## 六、选题：什么画得出来

Flux 之后限制小多了，但还是有几条：

**✅ 好画**：大主体（大王花、恐龙、大树、月亮、海浪、船）、
有明确前后景关系的场景、少量可数的小动物（`five black ants, each clearly drawn`）。

**⚠️ 要小心**：抽象概念（自转、轨道、时间流逝）——
必须找到一个**具体可画的画面**来承载，别指望模型画示意图。
「地球一半亮一半暗、两个小镇」就比「地球在自转」好画得多。

**❌ 避开**：需要精确数量的密集小物体（鸟群、鱼群、沙粒）、
文字和数字（模型写不对）、需要严格解剖正确的图解。

---

## 七、仓库里的东西

```
storybook/
  HANDBOOK.md          ← 本文件
  story_*.json         8 本书的脚本
  build_web.py         合成网页
  pack_images.py       图片压 base64
  contact_sheet.py     生成联系表（审图用）
  compose.py           图层合成（SDXL 时代的遗产，Flux 用不上）
  BATCH_PROMPT.md      批量出图任务书的样例
  REDO.md              重跑清单的样例
workflows/             ComfyUI 工作流
FLUX_ON_8GB.md         Flux 部署 + LoRA 训练
lora_training/
  RETRAIN.md           素材筛选标准、标注写法
```

## 八、命令速查

```bat
:: 出图（全本 / 只重跑几页）
venv\python.exe storybook\render_lora.py storybook\story_sea.json
venv\python.exe storybook\render_lora.py storybook\story_sea.json 1 4

:: 看一本书的全部页
venv\python.exe storybook\contact_sheet.py storybook\out\sea_lora

:: 压图 + 出网页
venv\python.exe storybook\pack_images.py storybook\out\sea_lora storybook\out\web_sea
venv\python.exe storybook\build_web.py storybook\story_sea.json storybook\out\web_sea > storybook\out\web_sea\index.html

:: 只改了文字，重出网页
venv\python.exe storybook\build_web.py storybook\story_sea.json storybook\out\web_sea > storybook\out\web_sea\index.html
```
