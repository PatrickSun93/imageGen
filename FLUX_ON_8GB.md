# 在 8GB 显存的 N 卡上装 Flux + 训练人物 LoRA

写给：Windows 笔记本 / NVIDIA 8GB 显存 / 已经装好 ComfyUI 的情况。
目标：解决 SDXL 画不出"人物 + 次要物体同框"的问题（蚂蚁总是丢失、比例失控）。

> **为什么换 Flux**：SDXL 只能锁定一个主体，提示词里的次要物体经常被整个丢掉。
> 实测过——去掉 LoRA 也一样丢，是模型能力上限，不是配置问题。
> Flux 是 12B 参数的 DiT，多主体提示词遵循能力强一个档次。

---

## 一、选哪个版本

8GB 显存必须用 GGUF 量化版，fp16 原版 23.8 GB 完全装不下。

| 文件 | 大小 | 说明 |
|---|---|---|
| **flux1-dev-Q4_K_S.gguf** | 6.8 GB | **推荐**，质量和显存的平衡点 |
| flux1-dev-Q5_K_S.gguf | 8.3 GB | 更好但 8GB 卡会溢出到内存，变慢 |
| flux1-schnell-Q4_K_S.gguf | 6.8 GB | 只要 4 步，快 5 倍，质量略低。**先拿它试水** |

下载（HuggingFace，仓库 `city96/FLUX.1-dev-gguf` 和 `city96/FLUX.1-schnell-gguf`）：

```
放到 ComfyUI\models\unet\
  flux1-dev-Q4_K_S.gguf
```

### 配套文件（三个，缺一不可）

| 文件 | 放到 | 大小 | 来源 |
|---|---|---|---|
| `t5xxl_fp8_e4m3fn.safetensors` | `models\text_encoders\` | 4.9 GB | comfyanonymous/flux_text_encoders |
| `clip_l.safetensors` | `models\text_encoders\` | 246 MB | 同上 |
| `ae.safetensors` | `models\vae\` | 335 MB | black-forest-labs/FLUX.1-dev（需登录同意许可） |

T5 也有 GGUF 版（`t5-v1_1-xxl-encoder-Q4_K_M.gguf`，约 3 GB），显存实在紧张就用它。

## 二、装 GGUF 节点

```bat
cd ComfyUI\custom_nodes
git clone https://github.com/city96/ComfyUI-GGUF
..\..\venv\Scripts\pip install gguf
```

重启 ComfyUI，节点列表里应该出现 `UnetLoaderGGUF` 和 `DualCLIPLoaderGGUF`。

## 三、工作流怎么接

跟 SDXL 完全不同，注意这几点：

```
UnetLoaderGGUF(flux1-dev-Q4_K_S.gguf) ──────────┐
DualCLIPLoader(t5xxl_fp8, clip_l, type=flux) ──┤
VAELoader(ae.safetensors) ─────────────────────┤
                                                │
CLIPTextEncode(正面) → FluxGuidance(3.5) → KSampler
EmptySD3LatentImage(1024x1024)  ← 不是 EmptyLatentImage
```

**四个和 SDXL 不一样的地方**：

1. **用 `EmptySD3LatentImage`**，不是 `EmptyLatentImage`（Flux 是 16 通道 latent）
2. **CFG 设 1.0**，改用 `FluxGuidance` 节点控制强度（dev 用 3.5，schnell 用 1.0）
3. **负面提示词无效**——Flux dev 是蒸馏模型，不跑负面分支。别在负面里花力气
4. **步数**：dev 20 步，schnell 4 步

### 提示词写法也不同

SDXL 吃标签堆砌，Flux 吃**自然语言长句**：

```
❌ SDXL 风格： a boy, ants, crayon, storybook, grass, 5 ants
✅ Flux 风格： A little boy in a green t-shirt crouches on a garden path,
              watching a line of five black ants carry crumbs across the dirt
              in front of him. Children's book illustration drawn with wax crayons.
```

**写成完整句子，说清楚谁在哪里做什么**——这正是 Flux 强过 SDXL 的地方，
也是解决"蚂蚁丢失"的关键。

## 四、预期性能（8GB 卡）

| 项 | 数值 |
|---|---|
| 首次加载模型 | 40–60 秒 |
| 出图 1024×1024 / 20 步 | 25–45 秒 |
| schnell 4 步 | 8–15 秒 |
| 显存占用 | 6.5–7.5 GB |

比 SDXL 慢一倍，但比这台 M4 快 10 倍以上（M4 跑 Flux 要 8–12 分钟一张）。

**显存不够的降级顺序**：换 T5 的 GGUF 版 → ComfyUI 加 `--lowvram` → 降到 768×768。

## 五、训练 Flux 人物 LoRA

**SDXL 的 LoRA 在 Flux 上用不了**，架构完全不同，必须用同一批照片重训。

素材直接用现成的：`lora_training/raw/` 里 29 张图 + 标注，触发词 `ohwx boy`。
标注不用改，Flux 训练一样吃这种写法。

### 用 ai-toolkit（比 sd-scripts 更适合 Flux）

```bat
git clone https://github.com/ostris/ai-toolkit
cd ai-toolkit
git submodule update --init --recursive
python -m venv venv
venv\Scripts\pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
venv\Scripts\pip install -r requirements.txt
```

配置文件的关键项（8GB 显存）：

```yaml
model:
  name_or_path: "black-forest-labs/FLUX.1-dev"
  is_flux: true
  quantize: true          # ← 必须开，否则 8GB 装不下
network:
  type: "lora"
  linear: 16              # rank，和我们 SDXL 那版一致
  linear_alpha: 16
train:
  batch_size: 1
  steps: 2000
  gradient_accumulation_steps: 1
  gradient_checkpointing: true    # ← 必须开
  noise_scheduler: "flowmatch"
  optimizer: "adamw8bit"          # ← 必须，省显存
  lr: 1e-4
  dtype: bf16
datasets:
  - folder_path: "D:/imageGen/lora_training/raw"
    caption_ext: "txt"
    resolution: [ 512, 768 ]      # 8GB 建议从 512 起
sample:
  every_n_steps: 250              # 中途出样图，方便挑存档
```

**预期**：显存 7–7.5 GB，2000 步约 1.5–2.5 小时。

### 训练时的注意

- **一定要开中途采样**（`sample.every_n_steps`）。我们在 SDXL 上吃过亏：
  1800 步跑满，结果最好的是 800 步那个存档，后面全过拟合成照片风了
- Flux LoRA 的强度通常比 SDXL 低，出图时从 **0.8** 开始试，别一上来 1.25
- 训完同样要做**同种子 A/B**，别默认最后一个存档最好

## 六、迁移过来之后的流程

绘本生产的其余部分不用改，`storybook/` 那套照搬：

1. `story_xxx.json` 写脚本（`scene` 字段改成 Flux 的自然语言长句）
2. `render.sh` 里换成 Flux 工作流
3. `build_web.py` 合成网页，完全不用动

参考现有文件：
- `storybook/MAKE_A_BOOK.md` — 绘本流程和画风配方
- `lora_training/RETRAIN.md` — 素材筛选标准（这套规则对 Flux 一样适用）
- `lora_training/TRAIN_ON_NVIDIA_8GB.md` — SDXL 版的 8GB 训练参数

## 七、先验证再投入

别一上来就训 LoRA。**先花 20 分钟验证 Flux 能不能解决蚂蚁问题**：

1. 只装 schnell GGUF（4 步，最快）
2. 不带任何 LoRA，跑这句：

```
A little boy in a green t-shirt and dark blue shorts crouches on a sunny garden path.
In front of him, five black ants walk in a neat line across the dirt, each carrying
a small crumb. Children's book illustration drawn with wax crayons on textured paper.
```

3. 看蚂蚁在不在、数量对不对、比例合不合理

**这一步就能判断 Flux 值不值得投入**。SDXL 在这句话上稳定失败——蚂蚁要么消失，
要么糊成黑线团，要么变成巨大怪物。Flux 应该能画对。
