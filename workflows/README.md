# 出图速查

服务跑在 **8188**。启动：

```bash
cd /Volumes/externalssd/devitems/learning/imageGen && nohup ./start.sh >/dev/null 2>&1 &
```

浏览器：本机 <http://127.0.0.1:8188> ·
Tailscale <http://<你的-tailscale-ip>:8188> · 局域网 <http://<局域网-ip>:8188>

## 网页界面怎么用

1. 浏览器打开 <http://127.0.0.1:8188>
2. 左上角菜单 **Workflow → Open**（或直接把 JSON 拖进画布），
   选 `workflows/ui/` 里的 **`*_ui.json`**
3. 找到 **CLIPTextEncode** 节点（两个：上面接 positive 的是正面提示词，
   接 negative 的是负面），直接在框里改文字
4. 想换随机种子：**KSampler** 节点的 `seed` 改数字，
   或把它下面的 `fixed` 点成 `randomize`
5. 点右下角 **Queue Prompt** 出图，右侧队列能看进度

> **注意目录区别**：
> `workflows/*.json` 是 **API 格式**，只能给 `run_workflow.py` 用，网页打不开；
> `workflows/ui/*_ui.json` 是 **UI 格式**，网页专用。
> 两者内容等价。改了 API 版想同步到网页版：
> `ComfyUI/venv/bin/python bench/api2ui.py workflows/xxx.json workflows/ui/xxx_ui.json`

常用操作：拖画布空白处平移，滚轮缩放，双击空白搜索节点，
选中节点按 `Ctrl+C/V` 复制，连线拖动圆点到另一个圆点。

## 命令行出图

```bash
cd /Volumes/externalssd/devitems/learning/imageGen
ComfyUI/venv/bin/python workflows/run_workflow.py workflows/<工作流>.json [--seed N]
```

出图落在 `ComfyUI/output/`。提示词直接改工作流 JSON 里的 `CLIPTextEncode.text`。

---

## 日常用哪个

全部 1024×1024，耗时为热加载实测（模型已在内存），冷加载再加 10~20 秒。

| 想干什么 | 用这个 | 每张 | s/it |
|---|---|---|---|
| **试提示词、快速迭代** | `pony_v6_dmd2.json` | **18 秒** | 1.91 |
| **动漫图，日常首选** | `anima_turbo.json` | **62 秒** | 5.97 |
| Pony 风格出成品 | `pony_v6_xl.json` | 104 秒 | 4.02 |
| 动漫图要最好质量 | `anima_aesthetic.json` | 352 秒 | 11.59 |
| V7 试试看（慢，768） | `pony_v7_768.json` | 454 秒 | 21.17 |
| V7 完整质量（很慢） | `pony_v7_s20.json` | 834 秒 | 40.34 |

**先用快的定构图和提示词，满意了再换慢的出成品。** 换工作流不必重启服务。

## 用自己的照片改图（img2img）

1. 把照片复制到 **`ComfyUI/input/`**
2. 改工作流里 `LoadImage` 的 `image` 字段为你的文件名（网页里就是节点上的下拉框）
3. 改正面提示词，描述**你想要的结果**（不是描述原图）
4. 出图

```bash
cp ~/Desktop/我的照片.jpg ComfyUI/input/
# 编辑 workflows/pony_v6_img2img.json 里的 "image": "我的照片.jpg"
ComfyUI/venv/bin/python workflows/run_workflow.py workflows/pony_v6_img2img_fast.json
```

| 工作流 | 每张 | 用途 |
|---|---|---|
| `pony_v6_img2img_fast.json` | **22 秒** | 反复试提示词和 denoise |
| `pony_v6_img2img.json` | 100 秒 | 定下来了出成品 |

### `denoise` 是最关键的旋钮

它控制"改多少"，在 `KSampler` 节点上：

| 值 | 效果 |
|---|---|
| 0.3~0.4 | 轻微润色，基本还是原图 |
| **0.5~0.6** | 明显转成动漫/插画风，构图和姿势保留（**默认 0.6，从这里开始试**） |
| 0.7~0.8 | 大幅重画，只留个大致轮廓 |
| 0.9~1.0 | 基本等于无视原图 |

**先用 fast 版把 denoise 试出来，再用标准版出成品。**

### 注意

- 照片会被 `ImageScale` 缩放裁剪到 1024×1024（`crop: center` 居中裁剪）。
  想保留原始比例就改成 SDXL 支持的尺寸，比如竖图 832×1216、横图 1216×832
- 提示词写**你想要的结果**，不是描述原图。开头照旧要有 `score_9, score_8_up, score_7_up`
- **img2img 不保证脸像本人**——它是按提示词重画，denoise 越高越不像。
  想要"凭空生成你在别的场景"，那要另做 IPAdapter 或训练专属 LoRA，是另一套东西

## 各工作流的参数

| 工作流 | 模型 | 步数 | CFG | 采样器 / 调度器 | 备注 |
|---|---|---|---|---|---|
| `pony_v6_dmd2.json` | Pony V6 + DMD2 LoRA | 8 | 1.0 | lcm / sgm_uniform | clip skip 2；画风偏 CG |
| `anima_turbo.json` | Anima Turbo v1.0 | 10 | 1.0 | er_sde / simple | 蒸馏版，画风更平涂 |
| `pony_v6_xl.json` | Pony V6 XL | 25 | 7.0 | euler_ancestral / normal | clip skip 2 |
| `anima_aesthetic.json` | Anima Aesthetic v1.0 | 30 | 4.0 | er_sde / simple | |
| `pony_v7_s20.json` | Pony V7 | 20 | 3.48 | euler / simple | 加载要 13.7 GB |
| `pony_v7_768.json` | Pony V7 | 20 | 3.48 | euler / simple | 768×768 |

## 提示词开头怎么写

**Pony V6（含 DMD2）**——分数标签必须打头：

```
score_9, score_8_up, score_7_up, source_anime, rating_safe, 然后写内容
```

**Pony V7**——同样支持 score 标签，但官方承认 V7 的提示词响应不稳定：

```
score_9, score_8_up, score_7_up, rating_safe, 一句话概括画面, 再展开细节
```

**Anima（Danbooru 标签，小写、空格代替下划线）**：

- Aesthetic：`masterpiece, best quality, safe, 1girl, ...` —— 官方建议**不要**用 `score_*`
- Turbo：同上
- 画师标签必须加 `@`，例如 `@某画师`，不加几乎没效果
- 负面：`worst quality, low quality, artist name, blurry, jpeg artifacts, chromatic aberration`

> CFG=1 的两个工作流（DMD2 / Turbo）**负面提示词不生效**——CFG 1 时不跑负面分支。
> 这正是它们快一倍的原因。

## 几个要知道的坑

- **Pony V7 例外**：`start.sh` 开的 `--use-pytorch-cross-attention` 对 V7 是负优化（慢 9.6%）。
  认真跑 V7 时去掉该参数重启，可快约 10%。
- **V7 加载时会挤掉 8.4 GB 内存**（13.7 GB 权重），别在跑 V7 时干别的重活。
  采样期间不 swap，加载完就稳了。
- **不要指望调参数提速**：这台 M4 的 GPU 只有 3.8 TFLOPS，三个模型都跑在硬件峰值的
  73~79%。想快只有减少计算量（少步数 / CFG=1 / 降分辨率）。
  `--force-fp16` 实测让 Anima **慢 27%**。详见 `bench/FINDINGS.md`。

---

完整的模型来源、文件大小、官方参数说明和提示词规则在
[`README_full_reference.md`](README_full_reference.md)；
性能排查的完整数据和方法在 [`../bench/FINDINGS.md`](../bench/FINDINGS.md)。
