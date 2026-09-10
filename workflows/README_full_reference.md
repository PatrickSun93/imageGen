# 三个文生图模型的提示词 / 采样参数速查

本文件内容摘自各模型官方发布页（Civitai 模型页、HuggingFace README），
配套的 API 格式工作流 JSON 在同目录下。

- `pony_v6_xl.json` —— Pony Diffusion V6 XL（SDXL 架构）
- `pony_v7.json` —— Pony V7（AuraFlow 架构）
- `anima_aesthetic.json` —— Anima Aesthetic v1.0（Cosmos-Predict2 2B 微调）
- `run_workflow.py` —— 提交工作流到 `http://127.0.0.1:8188/prompt` 并等待完成的小脚本

跑一张图：

```bash
cd /Volumes/externalssd/devitems/learning/imageGen
ComfyUI/venv/bin/python workflows/run_workflow.py workflows/pony_v6_xl.json
ComfyUI/venv/bin/python workflows/run_workflow.py workflows/anima_aesthetic.json --seed 12345
```

出图落在 `ComfyUI/output/`。

---

## 1. Pony Diffusion V6 XL

- 来源：<https://civitai.com/models/257749>
- 采用版本：**V6 (start with this one)**，versionId `290640`，2026-04-29 更新（页面上另有 V6 Turbo DPO merge 和 V6-1.5，均为 2024 年的旧版本）
- 架构：SDXL
- 文件：`ComfyUI/models/checkpoints/ponyDiffusionV6XL_v6.safetensors`（6 938 041 050 字节 / 6.46 GiB，fp16 pruned，自带 VAE）

### 官方推荐采样参数

| 项目 | 值 |
|---|---|
| 采样器 | Euler a（ComfyUI 里是 `euler_ancestral`） |
| 步数 | 25 |
| 分辨率 | 1024px 及其它 SDXL 标准分辨率 |
| **Clip Skip** | **2**（官方标注 critical for quality，工作流里用 `CLIPSetLastLayer = -2`） |
| VAE | checkpoint 自带，无需另配 |

### 提示词格式

官方模板：

```
score_9, score_8_up, score_7_up, score_6_up, score_5_up, score_4_up, [描述], [标签]
```

其它特殊标签：

- 来源：`source_pony` / `source_furry` / `source_cartoon` / `source_anime`
- 分级：`rating_safe` / `rating_questionable` / `rating_explicit`

官方原话：本模型「is designed to not need negative prompts in most cases」，
也不需要额外堆质量词。

---

## 2. Pony V7

- 来源：<https://huggingface.co/purplesmartai/pony-v7-base>（官方仓库，2025-10-26 更新）
- 架构：AuraFlow（fal.ai），ComfyUI 原生支持，**不需要装额外节点**
- 文件（三个，缺一不可 —— 单文件 checkpoint 里只有 transformer，text encoder 和 VAE 要单独下）：

| 用途 | HF 路径 | 本地位置 | 大小 |
|---|---|---|---|
| transformer | `safetensor/pony-v7-base.safetensors` | `models/checkpoints/pony-v7-base.safetensors` | 13 717 249 520 字节 / 12.77 GiB |
| text encoder (Pile-T5-XL) | `text_encoder/model.fp16.safetensors` | `models/text_encoders/pony_v7_pile_t5_xl_fp16.safetensors` | 2 950 448 704 字节 / 2.75 GiB |
| VAE | `vae/diffusion_pytorch_model.fp16.safetensors` | `models/vae/pony_v7_auraflow_vae_fp16.safetensors` | 167 335 342 字节 / 160 MiB |

> `CheckpointLoaderSimple` 加载 `pony-v7-base.safetensors` 时只取 MODEL 输出，
> CLIP 走 `CLIPLoader`（type 填什么都行，ComfyUI 会按 state_dict 自动识别成 T5_XL → aura_t5），
> VAE 走 `VAELoader`。这是官方 `workflows/pony-v7-simple.png` 里的接法。

### 官方推荐采样参数

官方 README 只写了范围，具体数值取自官方工作流 `pony-v7-simple.png`：

| 项目 | 值 |
|---|---|
| 采样器 | `euler` |
| 调度器 | `simple` |
| 步数 | 官方 README：**至少 30 步**；官方工作流里给的是 20 |
| CFG | 3.48 |
| 分辨率 | 768px ~ 1536px，官方建议往高了走（官方工作流用 1280×1536） |
| T5TokenizerOptions | `min_padding = 768`，`min_length = 768`（官方工作流里有这个节点，别省） |

本仓库的 `pony_v7.json` 取 30 步（跟随 README 的下限建议）+ CFG 3.48 + 1024×1024。

### 提示词格式

官方模板：

```
special tags, factual description of image, stylistic description of image, additional content tags
```

- **special tags**：`score_X`、`style_cluster_x`、`source_X`
  官方警告：「V7 prompting may be inconsistent」，他们在做 V7.1 修这个问题。
- **factual description**：先用一句话概括画面，再展开细节；
  提到角色时用 `<species> <gender> <name> from <source>` 的写法，
  例如 `Anthro bunny female Lola Bunny from Space Jam`。
- **stylistic description**：媒介、镜头、光线等。
- **tags**：V7 同时吃自然语言和标签，可以在主提示词后面追加标签来加权。

相比 V6 的改进（官方列举）：提示词理解（尤其空间关系和多角色）、背景生成、
开箱即用的写实度、极暗/极亮画面、最高 1536×1536。

---

## 3. Anima（Aesthetic v1.0）

- 来源：<https://huggingface.co/circlestone-labs/Anima>（CircleStone Labs × Comfy Org，2026-08-24 更新）
- 架构：`nvidia/Cosmos-Predict2-2B-Text2Image` 微调，2B 参数，ComfyUI **原生支持**（需要较新版本，本机 v0.35.0 已带 `comfy/ldm/anima/`）
- 文件：

| 用途 | HF 路径 | 本地位置 | 大小 |
|---|---|---|---|
| diffusion model | `split_files/diffusion_models/anima-aesthetic-v1.0.safetensors` | `models/diffusion_models/` | 4 182 230 656 字节 / 3.90 GiB |
| text encoder (Qwen3 0.6B) | `split_files/text_encoders/qwen_3_06b_base.safetensors` | `models/text_encoders/` | 1 192 135 096 字节 / 1.11 GiB |
| VAE (Qwen-Image VAE) | `split_files/vae/qwen_image_vae.safetensors` | `models/vae/` | 253 806 246 字节 / 242 MiB |

> text encoder 用 `CLIPLoader` 加载，type 选 `stable_diffusion` 即可 —— 官方工作流就是这么填的，
> ComfyUI 会自动把 Qwen3-0.6B 识别成 Anima 的 text encoder。

### 版本说明（官方原文摘要）

- **Anima-Base**：未精调的底模，风格自由度和多样性最高，训练 LoRA 用这个。
- **Anima-Aesthetic**：为一致性和默认画风质量做过微调。`v1.0b` 是纯美学微调版，
  `v1.0` 额外并入了风格调整和稳定化 LoRA —— 作者本人说「I personally think 1.0 is better」。
- **Anima-Turbo**：蒸馏版，CFG 1 + 8~12 步。作者推荐先用 Turbo 快速试提示词。

### 官方推荐采样参数

| 项目 | 值 |
|---|---|
| 分辨率 | 512² ~ 1536² |
| 步数 | 30 ~ 50 |
| CFG | 4 ~ 5 |
| 采样器 | `er_sde`（作者的默认选择：中性画风、平涂、线条锐利） |

其它采样器（官方点评）：

- `euler_a`：线条更柔更细，偶尔偏 2.5D；CFG 可以比别的采样器推得更高而不糊。
- `dpmpp_2m_sde_gpu`：风格接近 er_sde，但更"有创意"，有时会跑野。
- `euler`：比 er_sde 更放得开，适合本身就稳的 Turbo 和 Aesthetic 版本。
- 想要写实/绘画质感，可以上 RES4LYF 节点包的 `beta57` 调度器。

### 提示词格式（Danbooru 风格标签）

- 标签用**小写**，用**空格**代替下划线；只有 score 标签保留下划线。
- 推荐正面前缀：`masterpiece, best quality, score_7, safe, `
- 推荐负面：`worst quality, low quality, score_1, score_2, score_3, artist name, blurry, jpeg artifacts, chromatic aberration`
- Danbooru 和 Gelbooru 标签不一致时，**优先用 Gelbooru 的写法**。
- 提示词加权有效，但权重要比 SDXL 惯用的高，例如 `(chibi:2)`。

**Aesthetic 版专门说明（重要）**：Aesthetic 只在高质量图上微调，训练时把质量标签全部剥掉了。
正面完全不用质量标签也行，留 `masterpiece, best quality, ` 是安全的。
官方**建议正负两边都不要用 `score_*` 标签** —— 模型质量已经足够高，score 标签会把它推过头。
本仓库的 `anima_aesthetic.json` 因此没有用 score 标签。

#### 标签顺序

```
[质量/meta/年份/分级标签] [1girl/1boy/1other 等] [角色] [作品] [画师] [通用标签]
```

每一段内部顺序随意。

- 质量标签（人评分体系）：`masterpiece, best quality, good quality, normal quality, low quality, worst quality`
- 质量标签（PonyV7 美学模型体系）：`score_9` ~ `score_1`，两套可以混用也可以都不用
- 年份：`year 2025` / 时期：`newest, recent, mid, early, old`
- meta：`highres, absurdres, anime screenshot, jpeg artifacts, official art` 等
- 分级：`safe, sensitive, nsfw, explicit`
- **画师标签必须加 `@` 前缀**，例如 `@big chungus`；不加的话效果会非常弱

模型训练时做了随机标签 dropout，不需要把所有相关标签都写全。

#### 自然语言提示

- 角色名和作品名遵循英文大小写规范。
- 纯自然语言时越详细越好，至少两句；极短的提示词结果会不可控。
- 标签和自然语言可以任意混排，质量/画师标签可以放在自然语言提示词开头。
- 多角色时，先点名角色再描述外观，否则模型容易混。

---

## 已知环境细节

- 后端是 Apple Silicon 的 MPS。`start.sh` 里设了 `PYTORCH_ENABLE_MPS_FALLBACK=1`，
  遇到 MPS 没实现的算子会回落 CPU 而不是直接报错。
- 服务端口 **8188**（8502 被别的服务占用）。

---

## 本机实测（M4 / 32GB 统一内存 / MPS，1024×1024，首次冷加载模型）

| 模型 | 步数 | 采样速度 | 端到端耗时 | 输出 |
|---|---|---|---|---|
| Pony Diffusion V6 XL | 25 | 5.1 s/it | **139.2 秒** | `pony_v6_00001_.png` |
| Anima Aesthetic v1.0 | 30 | 12.6 s/it | **391.4 秒** | `anima_00001_.png` |
| Pony V7 | 30 | 37.3 s/it | **1139.1 秒**（约 19 分钟） | `pony_v7_00001_.png` |

耗时差异基本就是模型规模：V6 是 SDXL UNet（约 2.6B），Anima 是 2B DiT，
V7 是 6.8B 的 AuraFlow —— 权重加载就有 13 GB（日志里 `loaded completely; 13027.71 MB`）。
以上都包含首次加载模型的时间，模型常驻内存后重复出图会快一些。

想在 V7 上跑得快些，可以考虑官方的 GGUF 量化版（`gguf/base-v7-Q8_0.gguf`，7.3 GB），
需要额外装 [City96 的 GGUF 节点](https://github.com/city96/ComfyUI-GGUF)。

## 启动 / 停止 / 看日志

不做开机自启，手动管理：

```bash
cd /Volumes/externalssd/devitems/learning/imageGen

# 启动（后台常驻）
nohup ./start.sh >/dev/null 2>&1 &

# 确认起来了
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:8188/system_stats   # 期望 200

# 停止
kill $(lsof -t -nP -iTCP:8188 -sTCP:LISTEN)

# 看日志
tail -f logs/comfyui.err     # 运行日志、采样进度、报错都在这里
tail -f logs/comfyui.log     # 只有启动横幅
```

访问地址（`--listen 0.0.0.0`，三种都通）：

| 场景 | 地址 |
|---|---|
| 本机 | <http://127.0.0.1:8188> |
| Tailscale 内的其它机器 | <http://<你的-tailscale-ip>:8188> 或 <http://<你的机器>.<你的tailnet>.ts.net:8188> |
| 同一局域网 | <http://<局域网-ip>:8188> |
