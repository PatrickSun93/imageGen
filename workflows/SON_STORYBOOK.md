# 给儿子画绘本 — 速查

**一句话**：改 `son_forest_fd.json` 或 `son_dino_fd.json` 里节点 `3` 的提示词，
只改最后那段场景描述，其他别动。

```bash
cd /Volumes/externalssd/devitems/learning/imageGen
ComfyUI/venv/bin/python workflows/run_workflow.py workflows/son_dino_fd.json --seed 123
```

出图在 `ComfyUI/output/`，每次存两张：`xxx_before` 是原始图，`xxx` 是修过脸的。

## 提示词结构

节点 `3` 的 text 是四段拼起来的，**前三段固定不要动**：

| 段 | 内容 | 作用 |
|---|---|---|
| 身份 | `ohwx boy, solo, 1boy, asian toddler, 3 years old, round chubby face, chubby cheeks, short black hair, black eyes` | `ohwx boy` 是 LoRA 触发词，**必须有** |
| 画风 | `children's picture book illustration, storybook art, soft watercolor painting, gentle rounded lineart, warm pastel colors, flat shading` | 绘本水彩 |
| 构图 | `full body shot, standing, whole figure visible` | 想要特写就改 `close-up portrait` |
| **场景** | **← 只改这段** | 想画什么写什么 |

场景写法举例：

```
sitting on the back of a friendly green dinosaur, laughing happily, jungle with palm trees, blue sky
crouching in a lush green forest, looking at a giant red flower with white speckles, ferns and tall trees
sitting in a small wooden boat on a calm lake, holding a fishing rod, mountains and sunset behind
standing on the moon in a spacesuit, looking at earth in the starry sky
riding a big fluffy white cat through a field of sunflowers
```

**注意**：SDXL 不认识生僻词。写 `rafflesia` 它会画成蘑菇，得直接描述长相
（`giant red flower with white speckles and thick petals`）。

## 为什么是这套参数

| 参数 | 值 | 原因 |
|---|---|---|
| LoRA strength | **1.25** | 1.0 不够像，1.3 以上开始伤画风 |
| FaceDetailer guide_size | **1024** | 脸抠出来放大到 1024 再重绘 —— 这是全身构图也能像的关键 |
| FaceDetailer denoise | **0.5** | 够改脸，又不脱离原构图 |
| KSampler | 25 步 / CFG 7 / dpmpp_2m / karras | SDXL 常规配置 |

**最重要的一条经验**：LoRA 需要脸占足够多像素才使得上劲。
远景直接出图，脸只有几十像素，怎么调都不像；
FaceDetailer 把脸单独放大重绘，等于让每张图的脸都享受特写级像素。

## 训练素材和 LoRA

- 素材：`lora_training/raw/` 11 张图 + 标注，触发词 `ohwx boy`
- 训练脚本：`lora_training/train.sh`（sd-scripts + MPS，1200 步约 2 小时）
- 存档：`lora_training/output/` 有 400/800/1200 三个版本，当前用的是 1200
- 想练更像：补 5~10 张**正脸特写**再跑一遍 `train.sh`，正脸特写是现在素材里最缺的

## 每张耗时

约 110 秒（出图 25 步 + 脸部重绘 25 步）。
