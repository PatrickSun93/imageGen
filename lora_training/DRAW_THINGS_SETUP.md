# 用 Draw Things 训练「儿子」LoRA — 操作手册

素材已经备好：`lora_training/raw/` 里 11 张图 + 11 个同名 `.txt` 标注。
触发词是 **`ohwx boy`**，出图时提示词里必须带上它，模型才知道要画他。

---

## 一、准备底模

打开 Draw Things → 左侧模型下拉框 → **Manage Models** → 找到
**Stable Diffusion XL Base (v1.0)** 下载（App 内置，让它自己下最省事，
它需要的是自己的格式）。

> 我们在 `ComfyUI/models/checkpoints/sd_xl_base_1.0.safetensors` 下的那份
> 是给 ComfyUI 出图用的，两边各一份，别搞混。

## 二、导入训练素材

菜单 → **LoRA Training**（有的版本在 Settings 里叫 Fine-tuning）→
**Add Images**，选中 `lora_training/raw/` 里的 **11 张 jpg**。

导入后逐张确认标注是否跟着进来了。如果没有自动读取同名 `.txt`，
就手动把每张的标注粘进去——内容在 `raw/*.txt` 里，一张对一张。

**标注绝对不要改成描述长相**（不要写"圆脸""黑眼睛"）。
现在的写法是刻意的：`ohwx boy` 负责吸收长相，后面只写衣服、场景、动作、表情。
写了长相，身份特征就会被那些词分走，触发词学不到东西。

## 三、训练参数

| 参数 | 填什么 | 为什么 |
|---|---|---|
| Base Model | SDXL Base 1.0 | 通用性最好，练出的 LoRA 能配各种 SDXL 风格模型 |
| **Network Dim (Rank)** | **16** | 人物 LoRA 的常用值。8 也行但细节少，32 容易过拟合 |
| Network Alpha | 8（= Dim 的一半） | 配合 Dim 16 的稳妥搭配 |
| **Learning Rate** | **1e-4** | 官方推荐 1e-4 或 1e-3，人物用 1e-4 更稳 |
| **Training Steps** | **1200** | 11 张 × 约 100 步。官方说 500 步就能引入新概念，1200 更扎实 |
| Resolution | 768（内存紧就 512） | 越高越像，但吃内存。这台 32GB 可以试 1024 |
| Batch Size | 1 | 本地训练基本都是 1 |
| Optimizer | AdamW | Draw Things 默认，betas 0.9/0.999 |
| LR Scheduler | Cosine | 后期自动降速，避免烧坏 |
| Text Encoder 训练 | **关闭** | 只训 UNet，人物 LoRA 够用且更稳、更省内存 |
| Trigger Word | `ohwx boy` | 必须和标注里一致 |

**预计耗时**：官方实测 Mac Mini M2 跑 500 步约 20 分钟，M4 只快不慢。
1200 步估计 **40~60 分钟**。训练时别同时跑 ComfyUI，两个抢内存。

## 四、训练完导出

Draw Things 训完会把 LoRA 存在它自己的模型库里。导出成 `.safetensors`
（菜单里找 Export / Share LoRA），然后放到：

```
/Volumes/externalssd/devitems/learning/imageGen/ComfyUI/models/loras/
```

建议命名 `son_ohwx_v1.safetensors`，之后练了新版好区分。

## 五、在 ComfyUI 里用

底模选 `sd_xl_base_1.0.safetensors`，接 `LoraLoader`（这次要连 CLIP，
不是 ModelOnly——人物 LoRA 两边都要），强度先试 **0.8~1.0**。

提示词必须带触发词，例如：

```
ohwx boy, children's picture book illustration, soft watercolor,
gentle rounded lineart, warm pastel colors,
standing in a lush forest looking at a giant rafflesia flower,
wonder expression, sunlight through leaves
```

```
ohwx boy, storybook illustration, riding a friendly green dinosaur
through a jungle, happy, big smile, warm colors
```

**这次是纯文生图（denoise 1.0），不再是 img2img**——画面 100% 由提示词决定，
想画什么场景就画什么，而人物因为 LoRA 记得他，依然是他。
这正是 img2img 做不到、而你要的那个效果。

## 六、效果不对时怎么调

| 症状 | 怎么办 |
|---|---|
| 不像他 | LoRA 强度调到 1.0；还不行就加练到 1800~2000 步 |
| 像是像，但画风被带跑（出来像照片） | LoRA 强度降到 0.6~0.7；或训练时 Dim 降到 8 |
| 每张脸都一样、表情僵 | 过拟合了，减到 800 步重练，或强度降到 0.6 |
| 背景老是出现家里/乐高店 | 标注里场景描述写得不够，或素材背景不够杂 |
