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

## Windows / N 卡（出图端）

那台 8GB N 卡的 Windows 笔记本布局和 Mac 不同：`ComfyUI/`、`sd-scripts/`、`ai-toolkit/`、`venv/`
都直接放在仓库根目录（均已 gitignore）。

```bat
venv\python.exe storybook\render_lora.py storybook\story_xxx.json [页码…]      :: Flux dev + 人物 LoRA 出图
venv\python.exe storybook\build_preview.py storybook\story_xxx.json out.html   :: 本地预览（正式成书用 Mac 的 build_web.py）
sh lora_training/train_flux_sdscripts.sh                                       :: 训练 Flux 人物 LoRA
```

配方和 8GB 的注意事项见 `FLUX_ON_8GB.md`，整条出书流程见 `storybook/HANDBOOK.md`。

## 关键文档（按需要读）

- `bench/FINDINGS.md` —— 为什么慢、能不能更快。结论：不是配置问题，模型已跑到 M4 硬件峰值的 73–79%，唯一的提速手段是减少计算量（DMD2 / Turbo，CFG=1）。
- **`storybook/HANDBOOK.md` —— 绘本制作完全手册。**从故事梗概到发布的整条流程：
  环境搭建、脚本字段、8 种验证过的画风配方、审图清单、13 种常见失败模式及改法。
  换机器、接手这个项目，看这一份就够。
- `lora_training/RETRAIN.md` —— 重新训练角色 LoRA 的流程与素材标准。
- `FLUX_ON_8GB.md` / `WINDOWS_SETUP_PROMPT.md` / `lora_training/TRAIN_ON_NVIDIA_8GB.md` —— 移植到 Windows/NVIDIA 的说明。

## 不在版本库里的东西

`ComfyUI/`（含 venv 与模型，约 19G）、`lora_training/sd-scripts/`（上游仓库）、
所有模型权重（`*.safetensors`）、训练输出、生成的图片，以及**训练素材照片**。
`.txt` 标注保留在 `lora_training/raw/`，重新准备素材时可对照使用。

克隆到新机器后需要自行安装 ComfyUI 与下载模型，参见 `WINDOWS_SETUP_PROMPT.md`。
