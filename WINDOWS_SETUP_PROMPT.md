# 在 Windows 上装 ComfyUI + Pony V6 / Pony V7 / Anima（可直接粘贴给 Claude Code 的任务 prompt）

> 这份 prompt 是从一次 macOS(M4) 实际安装中提炼的，所有 URL、文件字节数、
> 节点接法、推荐参数都经过实测验证，已按 Windows + NVIDIA 调整。
> 把下面 `---` 之间的全部内容复制粘贴给 Claude Code 即可，
> 显卡相关的判断留给它自己做。

---

目标：在这台 Windows 机器上装好 ComfyUI，配置三个文生图模型（Pony Diffusion V6 XL、
Pony V7、Anima），并能从局域网/Tailscale 里的另一台机器用浏览器访问。

**根目录**：所有东西放在 `D:\imageGen` 下（下称 `$ROOT`，如果 D 盘不存在或空间不足就换一个
数据盘，先告诉我用了哪个）。ComfyUI 装到 `$ROOT\ComfyUI`，venv 建在 `$ROOT\ComfyUI\venv`，
模型、工作流、输出、日志全部在这个目录里，不要往 `C:\Users\<我>` 下面放任何文件。

## 1. 先检查环境，有问题先停下来告诉我

- **显卡型号和 VRAM**（`nvidia-smi`）。这一步最关键，直接决定 Pony V7 用哪个版本。
  **你自己根据实测的 VRAM 判断**，然后告诉我你选了什么、为什么：
  - Pony V7 的 fp16 单文件是 **13.7 GB**，显存装不下就会不断卸载重载，慢到没法用
  - 装不下就改用官方 GGUF 量化版（见第 5 节），别硬上 fp16
  - Pony V6（6.5 GB）和 Anima（4.2 GB）显存要求低得多，基本都能跑
- **CUDA 驱动版本**（`nvidia-smi` 右上角）。太旧的话你判断要不要让我升级驱动，
  并挑一个和驱动匹配的 PyTorch CUDA 轮子版本（cu121 / cu124 / cu126 / cu128 等）
- **Python 版本**：需要 3.11 或 3.12。**不要用 3.13/3.14**（PyTorch 轮子跟不上）。
  没有就用 `winget install Python.Python.3.12` 装，装完确认
  `py -3.12 --version` 能用
- **git**：`git --version`，没有就 `winget install Git.Git`
- **aria2**：`winget install aria2.aria2`（断点续传，30 GB 下载必备）。
  实在装不上就用 `curl.exe -L -C -`
- **目标盘剩余空间**：三个模型加起来约 **32 GB**，加上 venv 和 PyTorch 约 **40 GB**。
  不够先停下来告诉我
- **系统内存**：Pony V7 加载时会吃 14 GB 左右，内存小于 16 GB 要提前说
- 确认 **8188 端口没被占用**（`netstat -ano | findstr :8188`）

## 2. 装 ComfyUI

```
git clone https://github.com/comfyanonymous/ComfyUI.git $ROOT\ComfyUI
```

用 `py -3.12 -m venv venv` 建独立环境（**必须用 3.11/3.12**）。

装 PyTorch **CUDA 版**（不要装成 CPU 版，装完必须验证）：

```
venv\Scripts\python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
venv\Scripts\python -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

`torch.cuda.is_available()` 必须是 `True`，否则停下来告诉我。
然后装 `requirements.txt`，再把 ComfyUI-Manager clone 到 `custom_nodes\`：

```
git clone https://github.com/Comfy-Org/ComfyUI-Manager.git $ROOT\ComfyUI\custom_nodes\ComfyUI-Manager
```

## 3. 下载模型（用 aria2c -c 断点续传，下完逐个核对字节数）

**Pony Diffusion V6 XL** → `models\checkpoints\ponyDiffusionV6XL_v6.safetensors`

```
https://civitai.com/api/download/models/290640?fileId=228616
```
- 6 938 041 050 字节。Civitai 这个链接**匿名可下**（307 跳转到 R2），不需要 API token。
  如果遇到 401 或跳登录页，停下来告诉我，我会给你 `CIVITAI_API_KEY`，
  用 `?token=<key>` 追加到 URL
- 这是 `civitai.com/models/257749` 的 versionId **290640**（页面上叫 "V6 (start with this one)"）。
  页面上另有 V6 Turbo DPO 和 V6-1.5，都是 2024 年的旧版，**不要下错**

**Pony V7** → 三个文件，**缺一不可**。单文件 checkpoint 里**只有 transformer**，
text encoder 和 VAE 必须单独下（这是最容易踩的坑）：

| HuggingFace 路径（仓库 `purplesmartai/pony-v7-base`） | 放到 | 字节数 |
|---|---|---|
| `safetensor/pony-v7-base.safetensors` | `models\checkpoints\pony-v7-base.safetensors` | 13 717 249 520 |
| `text_encoder/model.fp16.safetensors` | `models\text_encoders\pony_v7_pile_t5_xl_fp16.safetensors` | 2 950 448 704 |
| `vae/diffusion_pytorch_model.fp16.safetensors` | `models\vae\pony_v7_auraflow_vae_fp16.safetensors` | 167 335 342 |

下载 URL 形如 `https://huggingface.co/purplesmartai/pony-v7-base/resolve/main/<路径>`。
注意 HF 的 API 元数据里 text encoder 大小写的是 2 949 811 976，**那个值不准**，
以 HTTP `Content-Range` 的总长度 2 950 448 704 为准。

**Anima** → 仓库 `circlestone-labs/Anima`，下 **Aesthetic v1.0** 和 **Turbo v1.0** 两个：

| 路径 | 放到 | 字节数 |
|---|---|---|
| `split_files/diffusion_models/anima-aesthetic-v1.0.safetensors` | `models\diffusion_models\` | 4 182 230 656 |
| `split_files/diffusion_models/anima-turbo-v1.0.safetensors` | `models\diffusion_models\` | 4 182 230 656 |
| `split_files/text_encoders/qwen_3_06b_base.safetensors` | `models\text_encoders\` | 1 192 135 096 |
| `split_files/vae/qwen_image_vae.safetensors` | `models\vae\` | 253 806 246 |

**DMD2 LoRA**（给 Pony V6 提速 5.8 倍，强烈建议装）→ `models\loras\`

```
https://huggingface.co/tianweiy/DMD2/resolve/main/dmd2_sdxl_4step_lora_fp16.safetensors
```
393 854 592 字节。

## 4. 建工作流（API 格式，放 `$ROOT\workflows\`）

给每个模型写一个最简 API 格式工作流 JSON，通过 `http://127.0.0.1:8188/prompt` 提交测试。
下面的节点接法都是从**官方 workflow 里解出来的**，不要自己猜：

**Pony V6 XL**（SDXL）：`CheckpointLoaderSimple` → `CLIPSetLastLayer(-2)` → `CLIPTextEncode`
→ `KSampler` → `VAEDecode`(用 checkpoint 自带 VAE) → `SaveImage`
- **`CLIPSetLastLayer = -2` 必须有**（clip skip 2），官方标注 critical for quality
- 25 步 / CFG 7 / `euler_ancestral` / `normal`

**Pony V6 + DMD2**（日常试提示词用这个）：在上面基础上插入
`LoraLoaderModelOnly`（strength 1.0，只作用于 UNet，CLIP 仍走 CLIPSetLastLayer）
- 8 步 / **CFG 1.0** / `lcm` / `sgm_uniform`

**Pony V7**（AuraFlow，ComfyUI 原生支持，不需要额外节点）：
- `CheckpointLoaderSimple` 加载 `pony-v7-base.safetensors`，**只取 MODEL 输出**
- CLIP 走 `CLIPLoader` 加载 `pony_v7_pile_t5_xl_fp16.safetensors`，
  type 填什么都行（ComfyUI 会按 state_dict 自动识别成 T5_XL → aura_t5）
- 再接 `T5TokenizerOptions`（`min_padding=768`, `min_length=768`），**这个节点别省**
- VAE 走 `VAELoader` 加载 `pony_v7_auraflow_vae_fp16.safetensors`
- 20~30 步 / CFG 3.48 / `euler` / `simple`，分辨率 768~1536

**Anima**（Cosmos-Predict2 架构，需要较新版 ComfyUI）：
- `UNETLoader` 加载 `anima-aesthetic-v1.0.safetensors`（或 turbo）
- `CLIPLoader` 加载 `qwen_3_06b_base.safetensors`，**type 选 `stable_diffusion`**
  （官方 workflow 就这么填，ComfyUI 会自动识别成 Anima 的 text encoder）
- `VAELoader` 加载 `qwen_image_vae.safetensors`
- 用普通的 `EmptyLatentImage`（不是 EmptySD3LatentImage）
- Aesthetic：30 步 / CFG 4 / `er_sde` / `simple`
- **Turbo：10 步 / CFG 1**（快 5.7 倍，日常用这个）

提示词：
- Pony 系开头必须是 `score_9, score_8_up, score_7_up`，
  再加 `source_anime` / `rating_safe` 之类
- Anima 用 Danbooru 标签（小写、空格代替下划线），画师标签**必须加 `@` 前缀**。
  Aesthetic 版官方建议**不要**用 `score_*` 标签
- **CFG=1 的工作流（DMD2 / Turbo）负面提示词不生效**，这正是它们快一倍的原因

**同时生成网页可加载的 UI 格式**：API 格式的 JSON 网页界面**打不开**。
写一个转换脚本读 `/object_info` 拿节点的输入输出顺序，把 API 格式转成 UI 格式
（要有 `nodes`/`links`/`widget_idx_map` 等字段），另存到 `$ROOT\workflows\ui\`。
不然我只能用命令行出图。

## 5. Pony V7 的 GGUF 备选（显存装不下 13.7 GB 时用）

改用官方 GGUF 量化版：
- `purplesmartai/pony-v7-base` 仓库里的 `gguf/base-v7-Q8_0.gguf`（6.84 GiB）
  或 `gguf/base-v7-Q4_0.gguf`（3.68 GiB）
- 需要装 [City96 的 GGUF 节点](https://github.com/city96/ComfyUI-GGUF) 到 `custom_nodes\`
- 注意：**GGUF 省的是显存不是算力**，推理时要反量化回 fp16，速度只会更慢不会更快

## 6. 启动和验证

写一个 `$ROOT\start.bat`：激活 venv，用
`python main.py --listen 0.0.0.0 --port 8188` 启动，日志写到 `$ROOT\logs\`。

**Windows 特别注意**：
- `--listen 0.0.0.0` 需要在**防火墙**放行，第一次启动会弹窗，选"允许"；
  或者提前 `netsh advfirewall firewall add rule name="ComfyUI" dir=in action=allow protocol=TCP localport=8188`
- 不需要 `PYTORCH_ENABLE_MPS_FALLBACK`（那是 macOS 的）
- **不要加 `--use-pytorch-cross-attention`**：ComfyUI 在 NVIDIA 上会自动开启 SDPA，
  手动加是多余的
- 可选提速：装 `xformers` 或 SageAttention，装完对比一下 s/it 再决定留不留

验证：每个模型各跑一张 1024×1024，确认 `$ROOT\ComfyUI\output\` 里图都出来了，
**告诉我每张的 s/it 和总耗时**，以及 `nvidia-smi` 看到的显存占用峰值。

最后把"日常用哪个工作流、各自多少秒一张"写成一页 `workflows\README.md`。

## 7. 约束

- 只在 `$ROOT` 里操作，不动系统 Python，不改系统环境变量
- 任何一步出问题**先告诉我再决定**，不要自己换成别的模型
- 下载完必须核对字节数，不对就重下

---

## 附：macOS 那次的实测数据（供 Windows 对照）

Mac mini M4（10 核 GPU，3.8 TFLOPS）/ 32 GB，1024×1024：

| 工作流 | 步数 / CFG | s/it | 每张 |
|---|---|---|---|
| Pony V6 + DMD2 | 8 / 1.0 | 1.91 | 18 秒 |
| Anima Turbo | 10 / 1.0 | 5.97 | 62 秒 |
| Pony V6 XL | 25 / 7.0 | 4.02 | 104 秒 |
| Anima Aesthetic | 30 / 4.0 | 11.59 | 352 秒 |
| Pony V7 | 20 / 3.48 | 36.58 | 743 秒 |

M4 只有 3.8 TFLOPS，任何一块中端以上的独显都会快一个数量级以上。
**如果 Windows 上跑出来的数字没有明显好过上表，八成是装成 CPU 版 PyTorch 了**，
回去检查 `torch.cuda.is_available()`。
