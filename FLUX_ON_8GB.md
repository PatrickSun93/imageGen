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
| 出图 1024×1024 / 20 步 | 实测：不挂 LoRA 约 80 秒，挂 LoRA 约 100–120 秒（原先估的 25–45 秒太乐观） |
| schnell 4 步 | 8–15 秒 |
| 显存占用 | 6.5–7.5 GB |

比 SDXL 慢一倍，但比这台 M4 快 10 倍以上（M4 跑 Flux 要 8–12 分钟一张）。

**显存不够的降级顺序**：换 T5 的 GGUF 版 → ComfyUI 加 `--lowvram` → 降到 768×768。

## 五、训练 Flux 人物 LoRA

**SDXL 的 LoRA 在 Flux 上用不了**，架构完全不同，必须用同一批照片重训。

素材：原图在 `lora_training/raw/`，筛过之后 18 张图 + 标注放在 `lora_training/dataset/`，
触发词 `ohwx boy`。标注不用改，Flux 训练一样吃这种写法。

### 实际用的是 kohya sd-scripts（ai-toolkit 试过，放弃了）

ai-toolkit 在 8GB 上只能用 `uint4` 量化，而它的 4-bit 反量化没有融合内核，
实测约 30 秒 / 步，1000 步要 8 小时以上。它的配置留在 `lora_training/flux_lora_ohwx.yaml`，仅作记录。

改用 sd-scripts 的 8GB 方案（fp8 底模 + 块交换），脚本是 `lora_training/train_flux_sdscripts.sh`，关键参数：

```
flux_train_network.py
  --pretrained_model_name_or_path ComfyUI/models/unet/flux1-dev.safetensors   # 23 GB 原版，训练要用它，不能用 GGUF
  --clip_l / --t5xxl / --ae       复用 ComfyUI/models 里的 clip_l、t5xxl_fp8、ae
  --network_module networks.lora_flux --network_dim 16 --network_alpha 16
  --network_train_unet_only
  --optimizer_type AdamW8bit --learning_rate 1e-4 --lr_scheduler constant
  --max_train_steps 1000 --save_every_n_steps 250
  --mixed_precision bf16 --fp8_base      # ← 8GB 必须
  --blocks_to_swap 28                    # ← 8GB 必须，一部分 DiT 块换到内存里
  --gradient_checkpointing --sdpa
  --cache_latents_to_disk --cache_text_encoder_outputs_to_disk
  --max_data_loader_n_workers 0          # Windows 上多进程会卡死
  --guidance_scale 1.0 --timestep_sampling flux_shift --model_prediction_type raw
```

分辨率在 `lora_training/dataset_config_flux_win.toml`：512，开 bucket（256–1024）。
（`lora_training/dataset_config.toml` 是 Mac 上 SDXL 训练用的，别混用。）

**实测**：1000 步约 1h20m。每 250 步存一个档，共 4 个（step 250 / 500 / 750 / 1000），
已复制到 `ComfyUI/models/loras/`。

### 训练时的注意

- **多存几个档**（`--save_every_n_steps`）。我们在 SDXL 上吃过亏：
  1800 步跑满，结果最好的是 800 步那个存档，后面全过拟合成照片风了
- 训完在 ComfyUI 里做**同种子 A/B**，别默认最后一个存档最好。
  这次的对比图在 `storybook/out/ab*`，强度试过 0.5 / 1.0 / 1.3 / 1.6，
  最终选的是 **1000 步存档 + 强度 1.3**（比 SDXL 时的 1.0 高）

## 六、出书流程

1. `storybook/story_xxx.json` 写脚本（`scene` 用 Flux 的自然语言长句，每页标 `has_boy`）
2. `venv\python.exe storybook\render_lora.py storybook\story_xxx.json` 出图（工作流 `workflows/flux_dev_lora.json`）
3. 审图、压图、合成网页、发布，按 `storybook/HANDBOOK.md` 第四、五章做——整条流程现在都在这台机器上。
   只想快速看一眼：`venv\python.exe storybook\build_preview.py storybook\story_xxx.json out.html`

参考现有文件：
- `storybook/HANDBOOK.md` — **绘本制作完全手册**（流程、画风配方、审图清单、失败模式）
- `lora_training/RETRAIN.md` — 素材筛选标准（这套规则对 Flux 一样适用）
- `lora_training/TRAIN_ON_NVIDIA_8GB.md` — SDXL 版的 8GB 训练参数（旧方案）

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
