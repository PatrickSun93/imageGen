# -*- coding: utf-8 -*-
"""给每本书生成一份素材清单 story_assets_<book>.json，供对比页拼合用。

画风和调色板直接从那本书自己的 story JSON 读，所以同一个东西在不同的书里
会按各自的画风画一遍（水粉的公交车和彩铅的公交车不是同一张）。

素材的提示词只说一件事：**一个物体、居中、占满画面、纯色背景**。
要点（踩过的坑）：
  · 不要写 curved —— curved cone 出来是月牙；
  · 不要在素材上强调锯齿之类的花纹 —— 会盖掉主体形状，那些交给对比页去标；
  · 背景写成 flat cream background of one single even colour，抠图才干净。

usage: make_assets.py            生成全部
       make_assets.py dinosize   只生成一本
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
SB = os.path.dirname(os.path.abspath(__file__))
BG = ("Centred and filling most of the picture on a flat cream background of one single "
      "even colour, nothing else in the picture.")

ASSETS = {
    "dinosize": [
        "One single long-necked plant-eating dinosaur standing on four legs, seen from the side "
        "facing left, its whole body from nose to tail tip inside the picture. " + BG,
        "One single small two-legged dinosaur standing upright, seen from the side facing left, "
        "about the size of a chicken, its whole body inside the picture. " + BG,
        "One single chicken standing on two legs, seen from the side facing right, its comb, "
        "beak and tail feathers clearly shaped. " + BG,
        "One single city bus seen from the side, a long box on wheels with a row of windows "
        "along it, its whole length inside the picture. " + BG,
        "One single elephant standing on four legs, seen from the side facing left, its trunk "
        "hanging down and one large ear showing. " + BG,
        "One single small car seen from the side, its whole length inside the picture. " + BG,
        "One single heap of green leaves piled into a tall mound, the pile wide at the bottom "
        "and pointed at the top. " + BG,
    ],
    "longneck": [
        "One single long-necked plant-eating dinosaur standing on four legs, seen from the side "
        "facing left, its neck stretched up high, its whole body inside the picture. " + BG,
        "One single three-storey house seen straight from the front, three rows of windows one "
        "above another, a flat roof on top. " + BG,
    ],
    "triceratops": [
        "One single horned plant-eating dinosaur standing on four legs, seen from the side facing "
        "left: one short horn on its nose, one long horn above its eye, and a wide bony shield "
        "fanning out behind its head. " + BG,
        "One single small car seen from the side, its whole length inside the picture. " + BG,
        "One single long pointed horn lying horizontally, thick and rounded at one end and "
        "tapering to a sharp point at the other, its surface smooth. " + BG,
    ],
    "dinoegg": [
        "One single chicken egg standing upright on its wider end, smooth and plain. " + BG,
        "One single large round dinosaur egg standing upright, its shell slightly pebbled. " + BG,
        "One single football standing on the ground, a round ball with dark pentagon patches "
        "over its surface. " + BG,
    ],
    "dinospeed": [
        "One single two-legged dinosaur running fast, seen from the side facing left, both feet "
        "off the ground and its tail streaming straight out behind it. " + BG,
        "One single bicycle seen from the side, two wheels, a frame and handlebars. " + BG,
    ],
    "extinct": [
        "One single rough round boulder of dark rock, its outline lumpy and uneven. " + BG,
        "One single mountain seen from a distance, a wide triangle of rock rising to one peak, "
        "its lower slopes darker. " + BG,
    ],
    "notdino": [
        "One single flying reptile gliding with both wings spread wide, seen from the side: each "
        "wing is a skin membrane held out by one very long finger bone, and it has a long pointed "
        "beak and a crest behind its head. " + BG,
        "One single sea reptile swimming, seen from the side: a smooth streamlined body with four "
        "paddle-shaped flippers, a long narrow snout and a large upright tail fin. " + BG,
        "One single small bird perched, seen from the side facing right, its beak, folded wing and "
        "tail feathers clearly shaped. " + BG,
        "One single woolly mammoth standing on four legs, seen from the side facing left, covered "
        "in long shaggy hair, with two long curved tusks and a raised domed head. " + BG,
        "One single two-legged meat-eating dinosaur standing, seen from the side facing left, its "
        "whole body from snout to tail tip inside the picture. " + BG,
    ],
}


def build(book):
    src = json.load(open(os.path.join(SB, f"story_{book}.json"), encoding="utf-8"))
    scenes = ASSETS[book]
    st = {
        "title": f"{src['title']} · 素材", "subtitle": "给对比页用的单体素材，不是一本书",
        "slug": f"assets_{book}", "seed_base": 90000, "character": "",
        "style": src["style"], "style_label": src["style_label"], "keyword": "素材",
        "diagram_pages": [], "palette": src["palette"], "neg_extra": "",
        "workflow": "workflows/qwen_image_2512.json",
        "colophon": {"model": "Qwen-Image-2512 (Q3)", "lora": "素材页，无人物", "strength": 1.3},
        "pages": [{"n": i, "zh": f"素材 {i}", "scene": s, "has_boy": False}
                  for i, s in enumerate(scenes, 1)],
    }
    path = os.path.join(SB, f"story_assets_{book}.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(st, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{book:12} {len(scenes)} 个素材 → story_assets_{book}.json")
    return len(scenes)


books = sys.argv[1:] or sorted(ASSETS)
print(f"合计 {sum(build(b) for b in books)} 个素材")
