# -*- coding: utf-8 -*-
"""把第七批各个 dino7_*.py 里的 BOOKS 落盘成正式的 story JSON + 素材 JSON。

每本出两个文件：
  story_<slug>.json          正文、画面描述、diagram_pages、调色板
  story_assets_<slug>.json   这本对比页要用的单体素材

顺带做四项自检（都是前六批踩出来的）：
  · 12 页，他只在 p1/p12；
  · diagram_pages 标的页 scene 必须为空（那些页由代码画，不过模型）；
    没标的页 scene 必须非空 —— 手册 4.2e 那条「页码集合一致但内容错位」就是这么漏掉的；
  · 他出镜的页必须写了半身、正脸、眼睛结构（手册 4.2h）；
  · 场景页不许出现 paper / collage / print / page / book / babies，
    素材不许出现 curved（手册 4.2f 的招词表）。

usage: dino7_build.py
"""
import glob, importlib, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
SB = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SB)

import dino7_a                                            # noqa: E402  先建起 BOOKS
for f in sorted(glob.glob(os.path.join(SB, "dino7_[b-z].py"))):
    importlib.import_module(os.path.basename(f)[:-3])
from dino7_a import BOOKS                                 # noqa: E402

BAD_SCENE = ("paper", "collage", "print", " page", "book", "babies")
FACE = ("A head-and-shoulders portrait of the little boy", "turned towards the viewer", "iris")
from dino7_extra import EXTRA

ASSET_NEG = ("shadow, cast shadow, drop shadow, ground, floor, base, pedestal, platform, "
             "dirt patch, grass patch, reflection, sky, blue sky, horizon, landscape, "
             "scenery, sunset, clouds in the background")

COMMON = {"workflow": "workflows/qwen_image_2512.json",
          "colophon": {"model": "Qwen-Image-2512 + Qwen-Image-Edit-2511 (Q3)",
                       "lora": "照片参考，不用 LoRA", "strength": 1.3}}


def FACE_FIX(sc):
    """把「脸要大」从形容词换成构图指令。

    2026-09-16 那批 80 张实测：写 "Waist-up view ... his face large in the frame"，
    模型画的是整个人站着、脑袋占不到画面一成——形容词它不当回事。换成明确的
    构图指令（身子在画面外）以后，脸占到两成半，正好落在手册 4.2h 要的 12~30%。

    放在落地这一步做，不在源码里替换：那句话在 f-string 里被折行拆成了两段，
    字面匹配不到。
    """
    return sc.replace(
        "his face large in the frame and turned towards the viewer",
        "only his head and shoulders inside the picture and everything below his chest "
        "outside the frame, his face turned straight towards the viewer")


warn = 0
for b in BOOKS:
    slug, diag = b["slug"], b["diagram"]
    pages = [{"n": i, "zh": zh, "scene": FACE_FIX(sc) if hb else sc,
              "has_boy": bool(hb)}
             for i, (zh, sc, hb) in enumerate(b["pages"], 1)]
    for p in pages:
        n, sc = p["n"], p["scene"]
        if len(pages) != 12:
            print(f"  !! {slug}: {len(pages)} 页，不是 12 页")
        if (n in diag) != (not sc.strip()):
            print(f"  !! {slug} p{n:02d}: diagram_pages={n in diag} 但 scene "
                  f"{'空' if not sc.strip() else '非空'}")
            warn += 1
        if p["has_boy"] and not all(k in sc for k in FACE):
            print(f"  !! {slug} p{n:02d}: 他出镜的页缺少半身/正脸/眼睛结构的描述")
            warn += 1
        if p["has_boy"] and n in diag:
            print(f"  !! {slug} p{n:02d}: 他出镜的页不能交给程序画")
            warn += 1
        for w in BAD_SCENE:
            if w in sc.lower():
                print(f"  !! {slug} p{n:02d}: scene 里出现了招词「{w.strip()}」")
                warn += 1
    for i, a in enumerate(b.get("assets", []), 1):
        if "curved" in a.lower():
            print(f"  !! {slug} 素材{i}: 出现了招词「curved」（会画成月牙）")
            warn += 1

    st = dict(COMMON, title=b["title"], subtitle=b["subtitle"], slug=slug,
              seed_base=b["seed"], character=b["character"], style=b["style"],
              style_label=b["style_label"], keyword=b["keyword"],
              diagram_pages=sorted(diag), palette=b["palette"], neg_extra="", pages=pages)
    with open(os.path.join(SB, f"story_{slug}.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(st, f, ensure_ascii=False, indent=2)
        f.write("\n")

    # 补渲的素材接在原有素材后面，原来的下标一个都不动（见 dino7_extra.py）
    assets = b.get("assets", []) + EXTRA.get(slug, [])
    if assets:
        at = dict(COMMON, title=f"{b['title']} · 素材", subtitle="给对比页用的单体素材",
                  slug=f"assets_{slug}", seed_base=90000, character="", style=b["style"],
                  style_label=b["style_label"], keyword="素材", diagram_pages=[],
                  palette=b["palette"], neg_extra="",
                  pages=[{"n": i, "zh": f"素材 {i}", "scene": s, "has_boy": False,
                          # bakeoff_qwen 只认 negative_extra 这个键
                          "negative_extra": ASSET_NEG}
                         for i, s in enumerate(assets, 1)])
        at["colophon"] = {"model": "Qwen-Image-2512 (Q3)", "lora": "素材页，无人物",
                          "strength": 1.3}
        with open(os.path.join(SB, f"story_assets_{slug}.json"), "w",
                  encoding="utf-8", newline="\n") as f:
            json.dump(at, f, ensure_ascii=False, indent=2)
            f.write("\n")

    words = sum(len(re.sub(r"\s", "", p["zh"])) for p in pages)
    print(f"{slug:12} {b['title']:14} {len(pages)} 页 {words} 字 "
          f"程序画 {len(diag)} 页 素材 {len(assets)} 个 [{b['style_label']}]")

t2i = sum(len([p for p in b["pages"] if not p[2]]) - len(b["diagram"]) for b in BOOKS)
edit = sum(len([p for p in b["pages"] if p[2]]) for b in BOOKS)
ast = sum(len(b.get("assets", [])) for b in BOOKS)
print(f"\n{len(BOOKS)} 本，自检告警 {warn} 条")
print(f"要出的图：场景页 {t2i} 张 + 素材 {ast} 张（各约 78 秒）+ 他出镜 {edit} 张（约 165 秒）")
print(f"程序画 {sum(len(b['diagram']) for b in BOOKS)} 页（瞬时）")
print(f"预计 GPU 时间 {((t2i + ast) * 78 + edit * 165) / 3600:.1f} 小时")
