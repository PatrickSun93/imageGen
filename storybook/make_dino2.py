# -*- coding: utf-8 -*-
"""第六批的后两本，外加把十本一起落盘。

单独放一个文件，是因为 heredoc 里的撇号（children's）会被外层 shell 的引号包装截断。
"""
import json, os
from make_dino import BOOKS, P, SB

BOOKS.append(dict(
    slug="dinospeed", seed=79000, title="恐龙跑得有多快", subtitle="看脚印隔多远就知道",
    keyword="速度", style_label="麻布拼色",
    style="children's picture book illustration, flat shapes with soft woven texture and clean "
          "edges, dusty teal, sand and burnt orange",
    character="wearing a burnt orange t-shirt, teal shorts and white sneakers, short black hair",
    palette=P(("#262a29", "#5f7472", "#f2f0ea", "#fbfaf6", "#bd6533", "#877a63", "#d9d6cc"),
              ("#e8e6dd", "#8fa29f", "#121514", "#1d211f", "#d17e4e", "#877a63", "#353a38")),
    diagram=[2, 4, 6, 8, 10],
    pages=[
     ("我和爸爸在院子里赛跑。\n我跑得很快，\n可还是爸爸先到。\n我问他，\n恐龙跑得过爸爸吗？",
      "The little boy runs across a garden lawn beside his father, both mid-stride, the boy looking up at him.", 1),
     ("有的恐龙\n比人跑得快多了。\n有的连走路\n都慢吞吞的。\n差得很远。",
      "A simple clear diagram, drawn flat and plain: three horizontal bars on a cream background all starting from the same left edge, the top one medium, the middle one the longest, the bottom one very short. Nothing else in the picture.", 0),
     ("跑得快不快，\n先看腿。\n腿长的一步\n就迈出去好远，\n步子不多也跑得远。",
      "One long-legged dinosaur taking a big stride on a cream background, its legs stretched far apart. Nothing else in the picture.", 0),
     ("还要看小腿。\n跑得快的恐龙，\n小腿比大腿长。\n跑得慢的\n正好相反。",
      "A simple clear diagram, drawn flat and plain: two leg outlines side by side on a cream background, each split into an upper and a lower part, the left one with a longer lower part and the right one with a longer upper part. Nothing else in the picture.", 0),
     ("用两条腿跑的\n一般都快。\n四条腿的身体太重，\n跑不了几步\n就得停下来歇。",
      "One two-legged dinosaur running past one heavy four-legged dinosaur standing still, on a cream background. Nothing else in the picture.", 0),
     ("怎么知道它跑多快呢？\n看脚印。\n脚印隔得远，\n说明它在跑；\n隔得近，那是在散步。",
      "A simple clear diagram, drawn flat and plain: two rows of footprints running across a cream background, the top row widely spaced and the bottom row closely spaced. Nothing else in the picture.", 0),
     ("这些脚印\n后来也变成了石头。\n一串一串，\n留在河边的泥地上，\n一直留到今天。",
      "One long line of fossil footprints preserved in dried mud on a cream background. Nothing else in the picture.", 0),
     ("跑起来的时候\n尾巴要翘起来。\n头往前伸，\n尾巴往后伸，\n这样才不会栽跟头。",
      "A simple clear diagram, drawn flat and plain: one running dinosaur seen from the side on a cream background with its head stretched forward, its tail lifted straight back, and a small triangle marking the balance point over its hips. Nothing else in the picture.", 0),
     ("最大的那几种\n其实跑不动。\n身体太重了，\n真跑起来\n腿骨会受不住。",
      "One enormous heavy dinosaur walking slowly with its feet planted on a cream background. Nothing else in the picture.", 0),
     ("跑得最快的恐龙\n有多快呢？\n差不多\n和骑自行车一样，\n追得上骑车的大人。",
      "A simple clear diagram, drawn flat and plain: one running dinosaur silhouette and one bicycle shape side by side on a cream background, each with an arrow of exactly the same length in front of it. Nothing else in the picture.", 0),
     ("它们有时候一起跑。\n地面咚咚地响，\n灰尘扬得老高，\n好远好远\n都看得见。",
      "A group of dinosaurs running together across open ground with dust rising behind them, on a cream background. Nothing else in the picture.", 0),
     ("我又跑了一次。\n这回我把两只手\n往后甩，\n像一条尾巴。\n好像真的快了一点。",
      "The little boy runs across the lawn again with both arms stretched straight back behind him like a tail, laughing.", 1),
    ]))

BOOKS.append(dict(
    slug="dinoskin", seed=80000, title="恐龙的皮是什么样的", subtitle="鳞片、羽毛，还有颜色",
    keyword="皮肤", style_label="厚涂水粉",
    style="children's picture book illustration, thick opaque gouache with bold brush marks, "
          "chestnut brown, moss green and warm cream",
    character="wearing a chestnut brown t-shirt, moss green shorts and white sneakers, short black hair",
    palette=P(("#2b2620", "#6f6a54", "#f3f0e7", "#fcfaf5", "#a4623a", "#7f7357", "#dcd7c7"),
              ("#eae5d8", "#a09a80", "#161108", "#221c12", "#c07a4e", "#7f7357", "#383225")),
    diagram=[2, 4, 6, 8, 10],
    pages=[
     ("墙上挂着一块皮，\n上面全是小格子，\n摸起来像我的篮球。\n爸爸说，\n那是恐龙的皮印。",
      "The little boy reaches up to touch a large fossil skin impression mounted on a museum wall, feeling its pebbled surface.", 1),
     ("大恐龙身上\n是一块一块的鳞。\n不是鱼身上那种会翘的，\n是平平地铺着，\n像地砖一样。",
      "A simple clear diagram, drawn flat and plain: one patch of skin shown greatly magnified on a cream background, covered with many small flat scales fitted edge to edge with no gaps. Nothing else in the picture.", 0),
     ("皮本来是软的，\n烂得最快。\n可要是刚好\n被很细的泥盖住，\n就能印下一个印子。",
      "One piece of dinosaur skin pressed into fine mud on a cream background, leaving a pebbled imprint. Nothing else in the picture.", 0),
     ("有的恐龙有羽毛。\n先是细细的一根根，\n像绒毛；\n后来才慢慢长成\n一片一片的。",
      "A simple clear diagram, drawn flat and plain: three feather shapes in a row on a cream background, the first a single thin filament, the second a tuft of several filaments, the third a full flat feather with a central shaft. Nothing else in the picture.", 0),
     ("最早的羽毛\n不是用来飞的。\n是用来保暖，\n也用来让自己\n看起来更好看。",
      "One small fluffy feathered dinosaur puffing out its plumage on a cream background. Nothing else in the picture.", 0),
     ("颜色怎么知道呢？\n羽毛里有很小的颗粒，\n形状不一样，\n颜色就不一样。\n显微镜下看得见。",
      "A simple clear diagram, drawn flat and plain: two magnified grain shapes on a cream background, one round and one long and rod-like, each with a colour swatch beside it. Nothing else in the picture.", 0),
     ("有一种小恐龙，\n身上是栗红色的，\n尾巴上还有\n一圈一圈的白环，\n像浣熊的尾巴。",
      "One small chestnut red feathered dinosaur with white rings banding its long tail, on a cream background. Nothing else in the picture.", 0),
     ("还有的恐龙\n背上颜色深，\n肚子颜色浅。\n这样在太阳底下\n看起来平平的，不容易被发现。",
      "A simple clear diagram, drawn flat and plain: one dinosaur seen from the side on a cream background with its back shaded dark and its belly shaded pale, and one sun above it. Nothing else in the picture.", 0),
     ("个子越大的\n越用不着毛。\n身体大，热气散得慢，\n毛要是太多，\n反而会热坏。",
      "One enormous bare-skinned dinosaur standing in strong sunlight on a cream background. Nothing else in the picture.", 0),
     ("有的恐龙\n皮里还长着骨头，\n一块一块嵌在背上，\n像穿了一件\n脱不下来的盔甲。",
      "A simple clear diagram, drawn flat and plain: one piece of skin cut through on a cream background showing several solid bony plates embedded inside it. Nothing else in the picture.", 0),
     ("甲龙的尾巴尖上\n有一个骨头做的锤子。\n甩起来呼呼响，\n能把追它的那只\n打得转身就走。",
      "One armoured dinosaur swinging its heavy bony tail club, motion lines behind it, on a cream background. Nothing else in the picture.", 0),
     ("我把手\n按在那块皮印上。\n一格一格的，\n硌手。\n原来恐龙摸上去是这样。",
      "The little boy presses his palm flat against the fossil skin impression on the museum wall, feeling the texture, absorbed.", 1),
    ]))

for b in BOOKS:
    slug, diag, title = b["slug"], b["diagram"], b["title"]
    st = {
        "title": title, "subtitle": b["subtitle"], "slug": slug,
        "seed_base": b["seed"], "character": b["character"], "style": b["style"],
        "style_label": b["style_label"], "keyword": b["keyword"],
        "diagram_pages": diag, "palette": b["palette"], "neg_extra": "",
        "workflow": "workflows/qwen_image_2512.json",
        "colophon": {"model": "Qwen-Image-2512 + Qwen-Image-Edit-2511 (Q3)",
                     "lora": "照片参考，不用 LoRA", "strength": 1.3},
        "pages": [{"n": i, "zh": zh, "scene": sc, "has_boy": bool(hb)}
                  for i, (zh, sc, hb) in enumerate(b["pages"], 1)],
    }
    # 手册 4.2e：diagram_pages 和写成示意图的 scene 必须一一对上，写的时候就查出来
    for p in st["pages"]:
        n = p["n"]
        marked = n in diag
        looks = p["scene"].startswith("A simple clear diagram")
        if marked != looks:
            print(f"  !! {slug} p{n:02d}: diagram_pages={marked}，scene 写法={looks}")
        if p["has_boy"] and marked:
            print(f"  !! {slug} p{n:02d}: 他出镜的页不能交给程序画")
    with open(os.path.join(SB, f"story_{slug}.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(st, f, ensure_ascii=False, indent=2)
        f.write("\n")
    words = sum(len(p["zh"].replace("\n", "")) for p in st["pages"])
    boy = [p["n"] for p in st["pages"] if p["has_boy"]]
    print(f"{slug:11} {title:11} {len(st['pages'])} 页 {words} 字 他在 {boy} 程序画 {diag}")
