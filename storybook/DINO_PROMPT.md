# 给出图机器的任务 prompt —— 第二本《恐龙没有走远》

> 复制 `---` 之间的全部内容，粘贴给那台 Windows 机器上的 Claude Code。
> 它自包含：故事脚本、要改的代码、出图参数、回传格式都在里面。

---

做第二本绘本《恐龙没有走远》，10 页，用现有的 Flux + `ohwx boy` LoRA 出图。

## 一、先修三个会挡路的硬编码

上一本是一次性脚本，第二本跑之前必须先通用化，否则标题会错：

**1. `storybook/build_web.py`** —— 页面标题「蚂蚁要搬家了」、画风标签「watercolor」、
版权信息（18 张照片 / strength 1.3 / 耗时）都是写死的模板文本。
改成从 story JSON 读：`title` / `subtitle` / `style_label` / `colophon` 字段。

**2. `storybook/render_lora.py`** —— 故事文件路径、`BOY_PAGES`（哪几页有人物）、
LoRA 参数都写死在代码里。改成从命令行接收 story JSON 路径，
`BOY_PAGES` 改成读每页的 `has_boy` 字段。
另外第 35–37 行有个残留表达式 `... if False else TRIGGER + scene`，直接简化掉。

**3. 文档和实际不符**，顺手更正：
实际用的是 sd-scripts 不是 ai-toolkit、1000 步不是 2000 步、
路径是 `C:\FlowDev\...` 不是 `D:\imageGen`、水彩不是蜡笔、`render.py` 不是 `render.sh`。
`MAKE_A_BOOK.md` 里蚂蚁那本还标着「制作中」，改成已完成。

改完先用蚂蚁那本跑一次 `build_web.py` 回归验证，确认没跑偏。

## 二、故事脚本

存成 `storybook/story_dino.json`：

```json
{
  "title": "恐龙没有走远",
  "subtitle": "院子里的麻雀，是它们的孩子",
  "slug": "dino",
  "workflow": "workflows/flux_dev_lora.json",
  "character": "wearing a green short sleeve t-shirt and dark blue shorts, white socks and grey sneakers, short black hair",
  "style": "children's picture book illustration, warm vintage storybook art, soft gouache painting, earthy ochre and deep green palette, gentle textured brushwork, soft natural light",
  "neg_extra": "",
  "keyword": "鸟",
  "palette": {
    "ink": "#2f2a1e",
    "soft": "#6d6350",
    "ground": "#efe9dc",
    "paper": "#fcfaf4",
    "accent": "#9c6b3f",
    "bark": "#8a7a5e",
    "line": "#ddd4c0",
    "ink_d": "#ece4d4",
    "soft_d": "#a89a80",
    "ground_d": "#17140f",
    "paper_d": "#221e17",
    "accent_d": "#d29a63",
    "bark_d": "#a3947a",
    "line_d": "#393225"
  },
  "pages": [
    {
      "n": 1,
      "zh": "博物馆里，站着一只好大好大的恐龙。\n它只剩下骨头了。\n我要仰起头，才能看见它的脑袋。",
      "scene": "A little boy stands in a dinosaur museum hall, tilting his head all the way back to look up at an enormous mounted dinosaur skeleton that towers over him. Warm light comes through tall windows. The boy is small at the bottom of the frame, the skeleton fills the upper space.",
      "has_boy": true
    },
    {
      "n": 2,
      "zh": "很久很久以前，\n地球上到处都是恐龙。\n那时候还没有人，也没有房子。",
      "scene": "A wide prehistoric landscape with several large dinosaurs walking among giant ferns and tall conifer trees, a volcano smoking far away on the horizon. Misty morning light. No people, no buildings.",
      "has_boy": false
    },
    {
      "n": 3,
      "zh": "有的恐龙比房子还高，\n脖子长得能够到树顶。\n有的恐龙却和一只鸡差不多大。",
      "scene": "A very tall long necked dinosaur reaching the top of a tree on the left, and on the right a small chicken sized dinosaur standing on the ground looking up at it. The size difference between them is dramatic. Green prehistoric forest.",
      "has_boy": false
    },
    {
      "n": 4,
      "zh": "咦？这只小恐龙身上，\n好像长着羽毛。\n毛茸茸的，像小鸡一样。",
      "scene": "Close up of a small fluffy feathered dinosaur the size of a chicken, standing among ferns. Its body is covered in soft downy feathers, but it has a long tail and clawed feet like a dinosaur. Curious and gentle expression.",
      "has_boy": false
    },
    {
      "n": 5,
      "zh": "有一天，天上掉下来一颗大石头。\n它比一座山还大。",
      "scene": "A huge glowing meteor falling through a darkening sky above the prehistoric landscape, leaving a bright trail of fire. Dinosaurs below look up. Dramatic orange and dark blue sky.",
      "has_boy": false
    },
    {
      "n": 6,
      "zh": "轰——\n天空变黑了，太阳被灰尘挡住了。\n好冷，好黑。",
      "scene": "A dark ash covered prehistoric landscape under a black sky, bare broken trees, grey dust falling like snow, cold and silent. Faint dim light. Empty and quiet.",
      "has_boy": false
    },
    {
      "n": 7,
      "zh": "大恐龙们，一个一个都不见了。\n可是有一些小小的、有羽毛的恐龙，\n躲在洞里，活了下来。",
      "scene": "Inside a small burrow under a tree root, two little feathered dinosaurs huddle together in the dark, keeping warm. Outside the burrow opening the world is grey and ashy. Warm soft light inside the hole.",
      "has_boy": false
    },
    {
      "n": 8,
      "zh": "太阳又出来了。\n小恐龙的孩子，孩子的孩子，\n羽毛越长越长，\n有一天，它们飞了起来。",
      "scene": "A sequence in one picture: a small feathered dinosaur on the ground on the left, a similar creature spreading longer feathered arms in the middle, and on the right it lifts off the ground into the air. Green landscape returning to life, sunlight breaking through.",
      "has_boy": false
    },
    {
      "n": 9,
      "zh": "那就是——鸟！\n原来鸟是恐龙的孩子。\n它们一直都在。",
      "scene": "A small brown sparrow perched on a branch in bright daylight, seen close up, with a faint soft silhouette of a feathered dinosaur behind it in the background like a memory. Warm sunny sky.",
      "has_boy": false
    },
    {
      "n": 10,
      "zh": "我在院子里放了一些面包屑。\n麻雀飞下来吃。\n我小声说：\n「你好呀，小恐龙。」",
      "scene": "A little boy crouching in his backyard holding out a hand with breadcrumbs, several sparrows landing on the ground in front of him to eat. Warm afternoon light, green grass, the boy is smiling gently.",
      "has_boy": true
    }
  ],
  "style_label": "复古水粉",
  "colophon": {
    "model": "FLUX.1-dev Q4_K_S GGUF",
    "lora": "son_ohwx_flux_v1 (1000 steps, 18 photos)",
    "strength": 1.3
  }
}
```

**注意 `has_boy` 字段**：只有第 1、10 页有他出镜，中间八页是恐龙和远古场景。
没有人物的页面**不要加 LoRA**，直接用 Flux 原生跑，画面会更干净。

## 三、出图参数

照抄蚂蚁那本已验证的配方：

```
模型      flux1-dev-Q4_K_S.gguf
LoRA      son_ohwx_flux_v1-step00001000.safetensors   strength 1.3（仅 has_boy 的页）
CLIP      t5xxl_fp8_e4m3fn + clip_l,  type=flux
VAE       ae.safetensors
latent    EmptySD3LatentImage 1024×1024
采样      20 步 / CFG 1.0 / euler / simple
引导      FluxGuidance 3.5
负面      留空
seed      3000 + 页码          ← 换一套编号，和蚂蚁那本区分开
```

提示词拼法：

- 有人物的页：`ohwx boy, {character}, {style}, {scene}`
- 无人物的页：`{style}, {scene}`（不带触发词，不挂 LoRA）

**别在提示词里描述五官**，写 "black eyes" 之类会覆盖 LoRA 学到的脸。

## 四、这本的难点

第 5、6 页是灭绝场景（陨石、黑暗、火山灰），情绪比前一本重。
如果出来太吓人（4 岁孩子看的），把 `scene` 里的 `dramatic` 换成 `gentle`，
`dark` 换成 `dim`，保留叙事但降低压迫感。

第 8 页是「一张图里画出演化过程」（地上 → 张开翅膀 → 飞起来），
Flux 对这种序列构图不一定听话。跑出来不对的话，
改成只画「一只长着长羽毛的小恐龙正要跳起来」，演化过程交给文字。

## 五、回传

出完打包成 zip 发回来，里面 `page_01.png` … `page_10.png` 即可，尺寸随意。
我这边负责压缩、排版、合成可翻页网页并发布。

如果哪几页反复出不对，也告诉我是哪几页、什么问题，我改脚本文案来适配画面
——绘本图文本来互相补位，不必图解文字。

---
