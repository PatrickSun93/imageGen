# 绘本生产线（分工版）

**那台 N 卡机器出图，这台 Mac 做脚本和成书。**

## 分工

| 环节 | 谁做 | 产出 |
|---|---|---|
| 1. 故事梗概 | 你 | 一句话就行，比如"他在森林里找会发光的蘑菇" |
| 2. 拆脚本 | 我 | `story_xxx.json`：10 页中文旁白 + 英文画面词 |
| 3. 出图 | N 卡机器 | `page_01.png` … `page_10.png` |
| 4. 合成发布 | 我 | 可翻页网页 + 链接 |

## 交接格式

**我给你的**：`story_xxx.json`，每页有 `zh`（念给孩子的中文）和 `scene`（喂给模型的英文）。
另外全书统一的 `character`（服装）和 `style`（画风）也在里面。

**你给我的**：一个 zip，里面 `page_01.png` ~ `page_10.png`。尺寸随意，我会统一压到 860px。
文件名只要能看出页码就行。

## 出图端的配方（已验证）

从 Flux 版图片的元数据里读出来的，照抄即可：

```
模型      flux1-dev-Q4_K_S.gguf
LoRA      son_ohwx_flux_v1（1000 步存档）  strength 1.3
CLIP      t5xxl_fp8_e4m3fn + clip_l,  type=flux
VAE       ae.safetensors
latent    EmptySD3LatentImage 1024×1024   ← 不是 EmptyLatentImage
采样      20 步 / CFG 1.0 / euler / simple
引导      FluxGuidance 3.5
负面      留空                            ← Flux dev 不跑负面分支
seed      seed_base + 页码               ← story JSON 里给，蚂蚁 2000，恐龙 3000
```

提示词拼法：`ohwx boy, {character}, {style}, {scene}`
没有人物的页（`has_boy: false`）：`{style}, {scene}`，不带触发词、不挂 LoRA。
**别在提示词里描述五官**——写 "black eyes" 之类会覆盖 LoRA 学到的脸。

## 我这边的命令

```bash
cd /Volumes/externalssd/devitems/learning/imageGen/storybook
# 1. 把 zip 里的图放进 ComfyUI/output/<slug>/，命名 p01.png ~ p10.png
# 2. 压缩成内嵌用的 base64
#    （脚本在 build_web.py 同目录，读 story JSON + images_b64.json）
# 3. 合成网页
python3 build_web.py story_xxx.json web_xxx > web_xxx/index.html
# 4. 我用 Artifact 工具发布，拿链接
```

## N 卡这边的命令

```bat
:: 在仓库根目录；ComfyUI 先跑在 127.0.0.1:8188
venv\python.exe storybook\render_lora.py storybook\story_xxx.json          :: 全本
venv\python.exe storybook\render_lora.py storybook\story_xxx.json 1 6 7    :: 只重跑这几页
:: 图在 storybook\out\<slug>_lora\page_01.png …，打成 zip 交回
venv\python.exe storybook\build_preview.py storybook\story_xxx.json out.html   :: 可选：本地预览
```

## 为什么这么分工

同样的素材、同样的 LoRA 思路、同样的脚本，SDXL 和 Flux 的差距是代差级的：

| | SDXL（这台 M4） | Flux（N 卡） |
|---|---|---|
| 人物与小物体同框 | 试了 6 种方案都不稳 | 直接就对 |
| 画风跨页一致 | 翻两页就变 | 十页一致 |
| 每页耗时 | 200 秒 | 80–120 秒（8GB 笔记本实测，挂 LoRA 的页慢一些） |
| 提示词 | 正负上百词还在打架 | 一句自然语言，负面留空 |

这台 Mac 在 SDXL 上做的那些补丁（图层合成、区域提示词、双强度 LoRA、换头术），
本质都是在填模型的能力缺口。Flux 不需要这些。

Mac 这边保留的价值：写脚本、排版成书、以及训练 LoRA（慢但能跑通）。

## 已完成

| 书 | 画风 | 出图 | 链接 |
|---|---|---|---|
| 森林里最大的花 | 水彩 | Mac / SDXL | （私有链接，未公开） |
| 蚂蚁要搬家了 | 数字水彩 | N 卡 / Flux | （私有链接，未公开） |
| 恐龙没有走远 | 复古水粉 | N 卡 / Flux | 出图完成，待排版 |
