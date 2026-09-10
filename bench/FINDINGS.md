# M4 上 ComfyUI 出图速度排查结论

排查日期 2026-09-09。机器：Mac mini M4（10 核 GPU）/ 32 GB 统一内存 / macOS 26.3，
ComfyUI v0.35.0 + torch 2.14.0 (MPS)。

## 一句话结论

**不是配置问题，是这台机器的 GPU 只有 3.8 TFLOPS。**
三个模型都跑在硬件峰值的 73~79%，参数调优的总空间不到 6%。
唯一有数量级效果的手段是**减少计算量**——Anima Turbo 快 5.7 倍。

## 硬件天花板实测

`torch` 直接跑 4096³ matmul：

| dtype | 耗时 | 算力 |
|---|---|---|
| fp16 | 36.22 ms | **3.79 TFLOPS** |
| bf16 | 36.21 ms | **3.80 TFLOPS** |
| fp32 | 40.30 ms | 3.41 TFLOPS |

**fp16 和 bf16 算力完全相同**——这直接决定了 `--force-fp16` / `--bf16-unet` 不可能带来提升。
（对比：M4 Pro 约 9 TFLOPS，M4 Max 约 18，RTX 4090 约 165。）

## 计算量与实测对照

两个模型都是 DiT，`patch_size=2`，1024×1024 → latent 128² → **4096 token**。
每步 FLOPs = 2 × 参数量 × token 数 × 2（CFG 正负两条）。

| 模型 | 参数 | 每步 FLOPs | 理论下限 | 实测 | 硬件效率 |
|---|---|---|---|---|---|
| Anima Aesthetic | 2.09B | 34.2 TFLOPs | 9.0 s/step | 11.59 | **78%** |
| Pony V7 | 6.86B | 112.4 TFLOPs | 29.6 s/step | 37.3 | **79%** |

78~79% 是很健康的数字，没有优化余量。

**分辨率缩放验证**（Pony V7）：

| 分辨率 | token | s/it | 比值 |
|---|---|---|---|
| 1024² | 4096 | 40.47 | 1.00 |
| 768² | 2304 | 21.17 | **0.523**（token 比值 0.5625） |

几乎完全线性，说明没有固定开销，纯算力决定。

## 为什么 2B 的 Anima 比 SDXL 慢

架构差异，不是实现问题：

- **SDXL 是 UNet**：注意力在下采样后的低分辨率层做，高分辨率层只有卷积
- **Anima / Pony V7 是 DiT**：全程 4096 token 的全分辨率 transformer

同参数量下，DiT 在高分辨率就是比 UNet 贵得多。Pony V6 (SDXL 3.47B) 只要 5.06 s/it，
Anima (DiT 2.09B) 要 11.59 s/it，这是正常的。

## 内存 / swap

Anima（4 GB 权重）：整轮测试 **swapouts 增量恒为 0**，完全不碰内存墙。

Pony V7（13.7 GB 权重）：

| 阶段 | 时长 | swapouts | swapins |
|---|---|---|---|
| 加载期 | 36 秒 | **+8.4 GB** | +1.6 GB |
| 采样期 | 27 分钟 | +194 MB | +1.2 GB |

**是"加载时 swap"不是"采样时 swap"**。装载 13.7 GB 权重会把别的进程挤出去 8.4 GB
（swap 池从 7 GB 自动扩到 10 GB）；模型常驻后采样期只有 0.7 MB/s 的轻微颠簸，
对速度影响可以忽略。

**GGUF 量化的定位**：省的是内存不是算力（推理时要反量化回 fp16，FLOPs 一分没少，
还多了反量化开销）。所以它只在"跑图时还要用这台 Mac 做别的事"时才值得装——
能少挤 7 GB；纯挂机出图的话装了反而更慢。
另外 ComfyUI-GGUF 在 macOS 上有已知的 `M1 buffer is not large enough`
问题（city96/ComfyUI-GGUF#107）。

## MPS 算子回落

去掉 `PYTORCH_ENABLE_MPS_FALLBACK=1` 跑 Anima：**353.6 秒 / 11.59 s/it，与保留时完全一致，
零报错**。日志里 MPS 相关只有 `Device: mps` 和 `VAE load device: mps` 两行正常信息，
没有任何 `not implemented` / `aten::` / `NotImplementedError`。

**这三个模型没有任何算子需要回落 CPU**，那个环境变量是多余的（留着无害，只在需要时生效）。

## 唯一有效的优化：减少计算量

Anima Turbo v1.0（官方蒸馏版，10 步 / CFG 1）：

| 版本 | 步数 | CFG | s/it | 每张耗时 |
|---|---|---|---|---|
| Aesthetic v1.0 | 30 | 4.0 | 11.59 | 351.6 秒 |
| **Turbo v1.0** | 10 | 1.0 | **5.97** | **62.3 秒** |

**快 5.7 倍**，两个因子相乘：

- 步数 30 → 10：3×
- CFG 4 → 1：**免掉负面提示词那条前向**，每步计算量减半，2×

注意 s/it 本身从 11.59 掉到 5.97，正好一半，就是 CFG=1 省掉的那条前向。
画质代价很小（线条更平涂锐利，多样性略降），日常迭代提示词应该默认用 Turbo。

## attention 后端：两个模型的最优选择是相反的

ComfyUI 的 `ENABLE_PYTORCH_ATTENTION` 只对 nvidia / intel-xpu / 部分 AMD 自动开启
（`comfy/model_management.py:466-474`），**MPS 不在列表里**，所以 Mac 默认走
sub-quadratic 回退路径。想用 PyTorch SDPA 必须显式传 `--use-pytorch-cross-attention`。

实测两个模型的结论**相反**：

| 模型 | sub-quadratic | PyTorch SDPA | 最优 |
|---|---|---|---|
| Anima Aesthetic (2.09B, 30 步) | 12.28 / 12.30 | **11.61 / 11.59** | SDPA 快 **5.8%** |
| Pony V7 (6.86B, 20 步) | **36.56 / 36.61** | 40.20 / 40.47 | sub-quad 快 **9.6%** |

每个组合都跑了两张，数字稳定在 ±0.3% 以内，不是噪声。
推测原因：SDPA 在 6.8B / 4096 token 这个规模上的内存访问模式不占优；
V7 那两次还叠加了更满的 swap 池（8.9 GB vs 6.1 GB），所以真实差距只会更大。

**决定**：`start.sh` 采用 `--use-pytorch-cross-attention`，因为日常主力是
Anima Turbo 和 Pony V6。要认真跑 Pony V7 时，手动用不带该参数的方式启动可再快约 10%：

```bash
kill $(lsof -t -nP -iTCP:8188 -sTCP:LISTEN)
cd /Volumes/externalssd/devitems/learning/imageGen/ComfyUI
PYTORCH_ENABLE_MPS_FALLBACK=1 ./venv/bin/python main.py --listen 0.0.0.0 --port 8188
```

## Pony V6 + DMD2 LoRA

`tianweiy/DMD2` 官方的 `dmd2_sdxl_4step_lora_fp16.safetensors`（393 854 592 字节，
标准 `lora_unet_` 格式，2364 个张量），走 `LoraLoaderModelOnly` 只作用于 UNet，
CLIP 仍走 `CLIPSetLastLayer(-2)` 保留 Pony 需要的 clip skip 2。

同为 SDPA 后端的公平对照：

| 配置 | 步数 | CFG | 采样器 | s/it | 每张 |
|---|---|---|---|---|---|
| 25 步基线 | 25 | 7.0 | euler_ancestral / normal | 3.96 / 4.02 | 106.4 / 104.5 秒 |
| **+ DMD2 LoRA** | 8 | 1.0 | lcm / sgm_uniform | **1.96 / 1.91** | **28.1 / 18.2 秒** |

**快 5.8 倍**。s/it 减半同样来自 CFG=1 免掉负面分支。

画质代价比 Anima Turbo 明显：结构、光影、构图都保住了，但风格从绘画感偏向
3D/CG 渲染感，对比度拉高，背景细节有丢失（提示词里的 flower field 退化成草坡）。
适合试提示词和定构图，出成品建议切回 25 步。

## 各参数实测汇总（Anima，1024×1024 / 30 步）

| 参数 | s/it | 相对基线 |
|---|---|---|
| 基线（sub-quadratic, bf16） | 12.28 / 12.30 | — |
| `--use-pytorch-cross-attention` | **11.61 / 11.59** | **−5.8%** |
| `--force-fp16` | 15.60 / 15.67 | **+27%（负优化）** |
| 去掉 `PYTORCH_ENABLE_MPS_FALLBACK` | 11.59 | 无差异，零报错 |

`--bf16-unet` / `--fp16-vae` 中途停测——Anima 权重本就是 BF16，
且 M4 的 fp16/bf16 算力完全相同，不可能有提升（`--bf16-unet` 第一张实测 12.42，
与基线一致，已足够佐证）。

## 最终采用的配置

`start.sh` 加了 `--use-pytorch-cross-attention`（Pony V6 −22%，Anima −5.8%）。
Pony V7 是唯一例外，跑它时手动去掉该参数可再快约 10%。
