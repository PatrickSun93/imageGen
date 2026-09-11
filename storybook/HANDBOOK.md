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
④ 跑全本          10 张 1024×1024 PNG，约 5–8 分钟
        ↓
⑤ 审图            ★ 最容易被跳过、但最该做的一步，见第四章
        ↓
⑥ 重跑问题页      一般 1–3 页
        ↓
⑦ 合成网页        build_web.py → 自包含 HTML
        ↓
⑧ 发布            Artifact 拿链接，或直接本地打开
```

一本书的实际耗时：脚本 10 分钟，出图 8 分钟，审图 10 分钟，
重跑 5 分钟，合成 2 分钟。**约 35 分钟**，瓶颈在审图和重跑，不在出图。

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

要重训见 `..\FLUX_ON_8GB.md` 第五章（用 ai-toolkit）和
`..\lora_training\RETRAIN.md`（素材筛选标准）。
**SDXL 的 LoRA 在 Flux 上用不了**，架构不同，必须用同一批照片重训。

素材照片不在仓库里（私人照片），但 `lora_training\raw\` 的标注写法
在 `RETRAIN.md` 里有说明和示例。

### 1.4 合成端

只要 Python + Pillow，直接借 ComfyUI 的 venv：

```bat
ComfyUI\venv\Scripts\python -c "import PIL; print(PIL.__version__)"
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
海边 4000、寄居蟹 5000、夜晚 6000、星星 7000、种子 8000。新书往后排。
重跑某页时用 **原种子 +100**，避免复现同样的构图。

### 3.3 负面提示词

Flux dev 是蒸馏模型，**不跑负面分支，负面词作用有限**，但还是要写——
实测能减少假签名和角色表的出现频率。

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

`page_01.png` … `page_10.png`，1024×1024，放进 `storybook\<slug>_win\`。

---

## 四、审图 ★

**这一步不能跳。** 8 本书的经验：平均每本有 1–3 页需要重跑，
而且问题往往不是「画得丑」，是**画的内容和旁白对不上**——
出图时看着挺好，拼成书念给孩子听才发现逻辑断了。

### 4.1 做一张联系表一次看全

```bat
ComfyUI\venv\Scripts\python storybook\contact_sheet.py sea_win
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

### 4.3 常见失败模式（都真实发生过）

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

### 4.4 重跑

把要改的页写成一个清单（参考仓库里的 `REDO.md`），每页给：
**问题描述 + 整段替换的提示词 + 附加负面词 + 新种子**。
不要只说「这页重跑一下」——说清楚为什么，否则容易换个种子出同样的毛病。

---

## 五、合成网页

### 5.1 压成 base64

图片要内嵌进 HTML（这样是单文件，发给谁都能看）：

```bat
ComfyUI\venv\Scripts\python storybook\pack_images.py sea_win web_sea
```

10 张 1024×1024 压成 JPEG q82 约 1.4 MB，base64 后约 1.9 MB。
**上限 16 MB**，远远够用。

### 5.2 生成 HTML

```bat
ComfyUI\venv\Scripts\python storybook\build_web.py story_sea.json web_sea > web_sea\index.html
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
:: 看一本书的全部页
ComfyUI\venv\Scripts\python storybook\contact_sheet.py sea_win

:: 压图 + 出网页
ComfyUI\venv\Scripts\python storybook\pack_images.py sea_win web_sea
ComfyUI\venv\Scripts\python storybook\build_web.py story_sea.json web_sea > web_sea\index.html

:: 只改了文字，重出网页
ComfyUI\venv\Scripts\python storybook\build_web.py story_sea.json web_sea > web_sea\index.html
```
