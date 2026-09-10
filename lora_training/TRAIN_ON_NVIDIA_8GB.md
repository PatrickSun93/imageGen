# 把这套流程搬到 8GB 显存的 N 卡笔记本

Mac 上这套配置是为 MPS 特调的，直接照搬到 CUDA 会又慢又占显存。
下面只列**需要改的地方**，其余照原样。

> **这是 SDXL 的旧方案，留作记录。** 现在绘本用的是 Flux，人物 LoRA 实际是用
> kohya sd-scripts 训的（`lora_training/train_flux_sdscripts.sh`），见 `FLUX_ON_8GB.md` 第五节。
> 这台机器上也没有 SDXL 底模 `sd_xl_base_1.0.safetensors`。

## 一、出图（不用改，直接能跑）

SDXL fp16 的 UNet 约 5.1 GB，加 VAE 和激活约 6–7 GB，8 GB 够用，
ComfyUI 还会自动卸载暂时不用的部分。

**启动参数要去掉两个 Mac 专用项**：

```bat
:: 不要 PYTORCH_ENABLE_MPS_FALLBACK（那是 macOS 的）
:: 不要 --use-pytorch-cross-attention（NVIDIA 上 ComfyUI 自动开 SDPA，加了多余）
:: 在 ComfyUI 目录里跑；这台机器的 venv 是 conda 结构，python.exe 在 venv 根目录
..\venv\python.exe main.py --listen 127.0.0.1 --port 8188
```

显存实在紧张就加 `--lowvram`，会慢一些但稳。

**预期速度**：1024×1024 一张约 15–30 秒（Mac M4 要 195 秒）。
整本 10 页从 33 分钟压到 5 分钟内。

## 二、训练（要改 4 个参数）

| 参数 | Mac (MPS) | **N 卡 8GB** | 为什么 |
|---|---|---|---|
| `--mixed_precision` | `no` | **`fp16`** | MPS 上 fp16 会 NaN 才用的 fp32；CUDA 没这问题，省一半显存 |
| `--optimizer_type` | `AdamW` | **`AdamW8bit`** | 需要 bitsandbytes，只有 CUDA 有 |
| `resolution`（dataset_config.toml） | 768 | **640** | 保险值，跑稳了再试 768 |
| 额外加 | — | **`--cache_text_encoder_outputs`** | 文本编码器算完就卸载，省 1–2 GB |

`--gradient_checkpointing`、`--network_train_unet_only`、`--cache_latents`
这三个原样保留，它们本来就是省显存的。

**bitsandbytes 要装回来**——Mac 上我从 requirements 里删掉了：

```bat
venv\Scripts\pip install bitsandbytes
```

### 改好的完整命令

```bat
set ROOT=C:\FlowDev\githubdevitems\comfyUIItems
venv\Scripts\python sdxl_train_network.py ^
  --pretrained_model_name_or_path="%ROOT%\ComfyUI\models\checkpoints\sd_xl_base_1.0.safetensors" ^
  --dataset_config="%ROOT%\lora_training\dataset_config.toml" ^
  --output_dir="%ROOT%\lora_training\output" ^
  --output_name="son_ohwx_v1" ^
  --save_model_as=safetensors ^
  --network_module=networks.lora ^
  --network_dim=16 --network_alpha=8 ^
  --learning_rate=1e-4 --unet_lr=1e-4 --text_encoder_lr=0 ^
  --network_train_unet_only ^
  --lr_scheduler=cosine --lr_warmup_steps=50 ^
  --optimizer_type=AdamW8bit ^
  --max_train_steps=1800 --save_every_n_steps=400 ^
  --mixed_precision=fp16 --save_precision=fp16 ^
  --gradient_checkpointing --cache_latents --cache_text_encoder_outputs ^
  --max_data_loader_n_workers=2 ^
  --seed=42
```

显存占用约 6–7 GB。**1800 步约 20–30 分钟**（Mac 上要 2 小时 55 分）。

`--max_data_loader_n_workers` 在 Windows 上可以给 2，Mac 上必须 0（多进程会卡死）。

## 三、显存不够时的降级顺序

按这个顺序退，每退一步再试：

1. `resolution` 640 → 512
2. 加 `--network_dim=8`（细节略少，但显存和体积都降）
3. 加 `--vae_batch_size=1`
4. 实在不行，`--full_fp16`（更省但可能不稳）

## 四、一个别忘的检查

装完先跑这句，**必须是 True**：

```bat
venv\python.exe -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

出图慢得跟 Mac 差不多，就是装成 CPU 版 PyTorch 了，回去重装 CUDA 轮子。
