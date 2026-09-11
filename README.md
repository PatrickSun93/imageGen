# imageGen —— 本地文生图 / 定制绘本工坊

Mac mini M4 (32GB) 上的本地图像生成环境，以及在此之上搭的「儿童定制绘本」流水线。
**所有素材、模型、训练、出图全程本地，没有任何数据离开这台机器。**

## 目录

| 路径 | 内容 |
|---|---|
| `start.sh` | 启动 ComfyUI（端口 8188，手动启动，无 launchd） |
| `workflows/` | ComfyUI 工作流（API 格式 + `ui/` 下的 UI 格式）与提交脚本 |
| `bench/` | 性能测试脚本与结论 → **`bench/FINDINGS.md`** |
| `lora_training/` | kohya sd-scripts 训练配置与文档（素材图片不入库） |
| `storybook/` | 绘本脚本（`story_*.json`）、批量渲染、合成、网页生成 |

## 快速上手

```bash
./start.sh                                   # 启动 ComfyUI → http://127.0.0.1:8188
python workflows/run_workflow.py <api.json>  # 命令行提交单个工作流
./storybook/render.sh storybook/story_xxx.json   # 批量渲染一本书
python storybook/build_web.py <slug>             # 生成可翻页网页
```

## 关键文档（按需要读）

- `bench/FINDINGS.md` —— 为什么慢、能不能更快。结论：不是配置问题，模型已跑到 M4 硬件峰值的 73–79%，唯一的提速手段是减少计算量（DMD2 / Turbo，CFG=1）。
- **`storybook/HANDBOOK.md` —— 绘本制作完全手册。**从故事梗概到发布的整条流程：
  环境搭建、脚本字段、8 种验证过的画风配方、审图清单、13 种常见失败模式及改法。
  换机器、接手这个项目，看这一份就够。
- `lora_training/RETRAIN.md` —— 重新训练角色 LoRA 的流程与素材标准。
- `FLUX_ON_8GB.md` / `WINDOWS_SETUP_PROMPT.md` / `lora_training/TRAIN_ON_NVIDIA_8GB.md` —— 移植到 Windows/NVIDIA 的说明。

## 模型（不在版本库里，需自行下载）

装在 `ComfyUI/models/` 下，当前这台 Mac 上保留的：

| 模型 | 文件 | 大小 | 来源 |
|---|---|---|---|
| Pony Diffusion V6 XL | `checkpoints/ponyDiffusionV6XL_v6.safetensors` | 6 938 041 050 B | Civitai `api/download/models/290640?fileId=228616`（**匿名可下**，307 跳 R2；遇 401 用 `?token=<CIVITAI_API_KEY>`） |
| Anima Aesthetic | `diffusion_models/anima-aesthetic-v1.0.safetensors` | 3.9 G | HuggingFace |
| Anima Turbo | `diffusion_models/anima-turbo-v1.0.safetensors` | 3.9 G | HuggingFace |
| Anima 的 text encoder | `text_encoders/qwen_3_06b_base.safetensors` | 1.1 G | 同上 |
| Anima 的 VAE | `vae/qwen_image_vae.safetensors` | 242 M | 同上 |

**Anima 不自带 text encoder 和 VAE**，那两个 qwen 文件看着像无关模型，实际是必需件，
删了四个 anima 工作流全跑不起来。

已删除（SDXL 时代的东西，绘本已转 Flux）：`sd_xl_base_1.0`、`dmd2_sdxl_4step_lora`、
`ultralytics/bbox`。因此 `workflows/son_*.json` 那 9 个工作流现在缺文件跑不了，
保留作记录。Pony V7 也没装（单文件 checkpoint 只含 transformer，
还要单独下 Pile-T5-XL 和 VAE，见 `WINDOWS_SETUP_PROMPT.md`）。

下载用 `aria2c -c -x8 -s8`，断点续传，下完**务必核对字节数**。

## 不在版本库里的东西

`ComfyUI/`（含 venv 与模型，约 19G）、`lora_training/sd-scripts/`（上游仓库）、
所有模型权重（`*.safetensors`）、训练输出、生成的图片，以及**训练素材照片**。
`.txt` 标注保留在 `lora_training/raw/`，重新准备素材时可对照使用。

克隆到新机器后需要自行安装 ComfyUI 与下载模型，参见 `WINDOWS_SETUP_PROMPT.md`。
