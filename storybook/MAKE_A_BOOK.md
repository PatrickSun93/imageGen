# 做一本定制绘本 — 流程

## 一句话

你给故事梗概 → 我拆 10 页脚本 → 批量出图 → 合成网页发布。全程约 40 分钟。

## 步骤

1. **写脚本**：`story_<主题>.json`，字段见下
2. **先试 1 页**（换了画风必做）：只留一页跑一次，确认风格对了再跑全本
3. **跑全本**：Mac 上 `./storybook/render.sh storybook/story_xxx.json`，约 30 分钟；
   N 卡上 `venv\python.exe storybook\render_lora.py storybook\story_xxx.json`，约 15 分钟，
   后面加页码可以只重跑某几页（如 `... story_xxx.json 5 6 8`）
4. **合成网页**：压缩成 base64 内嵌，发布成 Artifact 拿链接

## story JSON 的字段

```json
{
  "title": "书名", "subtitle": "副标题", "slug": "输出目录名",
  "style": "画风词 —— 全书统一",
  "neg_extra": "这本额外要挡的东西",
  "pages": [{"n":1, "zh":"中文正文\n第二行", "scene":"英文画面描述"}]
}
```

`zh` 是念给孩子听的，`scene` 是给模型看的，两者不用对应得很死。

N 卡（Flux）出图还会读这几个字段：

- `has_boy`（每页）：有人物的页拼成 `ohwx boy, {character}, {style}, {scene}` 并挂 LoRA；
  没人物的页只拼 `{style}, {scene}`，不带触发词、不挂 LoRA，画面更干净
- `seed_base`：seed = `seed_base + 页码`（不写默认 2000），每本换一段，互不重复
- `colophon.strength`：LoRA 强度，出图和版权页用同一个值，两边不会对不上

## 画风配方（已验证）

| 风格 | style 词 | 注意 |
|---|---|---|
| **水彩绘本** | `children's picture book illustration, storybook art, soft watercolor painting, gentle rounded lineart, warm pastel colors, flat shading` | 最稳，先验强 |
| **蜡笔** | `children's book illustration drawn with wax crayons on textured paper, chunky crayon strokes, visible waxy grain, flat bright colors, naive childlike drawing, thick black outlines` | 必须写 **on textured paper**，给蜡笔一个物理载体，否则压不住 LoRA 的照片属性 |
| **复古水粉**（Flux） | `children's picture book illustration, warm vintage storybook art, soft gouache painting, earthy ochre and deep green palette, gentle textured brushwork, soft natural light` | 恐龙那本，Flux dev 上画风一次就对 |

蜡笔只在 SDXL 上成功过。Flux dev 天生画得太精细，压不出蜡笔颗粒，N 卡上优先选水彩 / 水粉。

## 三条踩过的坑

**画风词要指向成熟画种 + 物理载体。** `crayon drawing` 太抽象，出来是照片人物配蜡笔背景；
`drawn with wax crayons on textured paper` 才管用。水彩之所以一次就成，是因为
watercolor 本身是强先验画种。

**负面词千万别写 `real child` / `realistic skin` / `photo`。** LoRA 学的就是真实小孩，
这些词会把人物本身一起否掉——试过一次，画面里男孩直接变成一只绿色大虫子。
负面只挡**画种**（watercolor / oil / 3d / airbrush），不挡人。

**SDXL 画不好密集小物体。** 写 `a line of ants` 会糊成一团黑线。
要写成 `a neat row of five small black ants, each clearly drawn`——限定数量、
强调清晰、给形态描述。

**（Flux）别在提示词里描述五官。** 写 `narrow dark eyes`、`black eyes` 之类会覆盖 LoRA 学到的脸，
`character` 只写衣着和发型。

**（Flux）写清画面里"有什么"，别只写"没有什么"。** 恐龙那本第 6 页写 `Empty and quiet`，
远古荒原上冒出一个穿橙色卫衣的人；改成 `Nobody is there, only trees, rocks and falling ash` 才干净。
第 1 页 `dinosaur skeleton` 画成了有皮有眼睛的活恐龙，要写 `made only of pale bones, empty eye sockets, bare ribs`。
第 7 页没写羽毛的样子，出来是带刺的小恐龙；写明 `covered in soft orange and cream downy feathers` 才对上文字。

## 一致性怎么保证

全书固定三件事，翻页时人物才不会忽胖忽瘦：

- 同一套身份词 `ohwx boy, solo, 1boy, asian toddler, 3 years old`
- 同一套画风词（story JSON 的 `style`）
- LoRA 强度锁 **1.0**（画风优先）；想更像可以到 1.25，再高就照片化了

seed 用 `2000 + 页码` 连号，既有变化又可复现。

N 卡 Flux 版：身份词只用 `ohwx boy, {character}`；LoRA 用 `son_ohwx_flux_v1` 的 1000 步存档，
强度 **1.3**（A/B 试过 0.5 / 1.0 / 1.3 / 1.6 后选定）；seed 用 `seed_base + 页码`。


## 选题：什么题材这台 Mac 画得出来

SDXL 有个硬限制：**一张图里只能可靠地画好一个主体**。
提示词里的次要物体经常整个丢掉——这不是配置问题，去掉 LoRA 一样丢，是模型能力上限。

### ✅ 适合（主体大、和人同框不冲突）

大王花、大树、瀑布、月亮、星空、彩虹、云、雪、影子、篝火、大石头、
海浪、恐龙、大型动物（熊、鹿、鲸）、房子、船、桥

判断标准：**那个东西画出来能有孩子的半身那么大**，就抢得过。
「森林里最大的花」之所以一次成功，正因为大王花是个大主体。

### ❌ 不适合（等 Flux）

蚂蚁、蜜蜂、蝴蝶群、鱼群、鸟群、种子、雨滴、沙粒、
任何"很多只小东西"的题材

「蚂蚁要搬家了」踩的就是这个坑：10 页里蚂蚁稳定出现的不到一半。
（后来换到 N 卡用 Flux 出图，蚂蚁和人同框直接就对，见 `PIPELINE.md`。）

### 🔶 折中办法

真要写小生物，把它写成**画面唯一主体**，人物那页干脆不出现：

```
第 3 页  一只蚂蚁扛着饼干屑的特写，画面里没有人
第 4 页  男孩蹲在地上看的中景，蚂蚁交给文字交代
```

绘本本来就是图文互相补位，不必每页都图解文字。

## 试过但不推荐的两条路

**分层生成（主图不带 LoRA + FaceDetailer 换脸）**——想着 LoRA 抢注意力，
去掉就好了。实测无效：SDXL base 照样画不出男孩和蚂蚁同框。归因错了。

**区域提示词（ConditioningSetAreaPercentage）**——把画面分区，
上半部分画男孩、下半部分画蚂蚁。**确实能让两者同框**，是 Mac 上唯一做到的方法，
但要同时平衡区域的位置、大小、强度、和全局条件的配比四个变量，
每次验证 3–5 分钟，而且换个场景就得重调（特写页和远景页的分区完全不同）。
调试成本远超收益。工作流留在 `workflows/son_regional_fd.json`，想折腾可以接着调。

## 角色一致性：两个必填字段

story JSON 里这两个字段是全书统一的关键，别省：

```json
"character": "wearing a green short sleeve t-shirt and dark blue shorts, white socks and grey sneakers, short black hair",
"scale": "consistent character proportions across all pages, a small three year old toddler"
```

**不写 character 的后果**：LoRA 见过他 15 件衣服，每页随机抽一件，
翻页时绿T、黄衫、蓝背带裤轮着来。加上之后 10 页完全统一。

**scale 字段作用有限**。扩散模型不做尺寸推理，写 `the size of a grain of rice`
它根本不理会。控制比例要用**镜头术语**，因为那直接对应训练数据里的图片类型：

| 想要 | 该写 | 别写 |
|---|---|---|
| 物体小、人全身 | `wide shot, full body` | `small ants` |
| 物体大、占满画面 | `extreme close up`, `macro` | `large ants` |
| 人物半身 | `medium shot, upper body` | — |

代价是：**镜头词会挤占内容描述的权重**。用了 wide/close/medium 之后，
次要物体更容易丢。这是个此消彼长的取舍。

## 镜头节奏（让它像本书而不是十张插图）

```
远景开场 → 推近 → 中景 → 特写（视觉高潮）→ 拉远收尾
```

参考「蚂蚁」那本的排布：1、7、10 远景 ｜ 2、3 近景 ｜ 4、6、9 中景 ｜ 5 特写。

## 已完成

| 书 | 画风 | 链接 |
|---|---|---|
| 森林里最大的花（大王花 / 寄生） | 水彩 | （私有链接，未公开） |
| 蚂蚁要搬家了（蚂蚁 / 下雨） | 蜡笔 | （私有链接，未公开） |
| 恐龙没有走远（恐龙 / 鸟） | 复古水粉（N 卡 / Flux） | 出图完成，待排版 |
