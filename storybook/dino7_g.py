# -*- coding: utf-8 -*-
"""第七批（7/10）：冰雹、龙卷风、天气预报、露水和霜。"""
from dino7_a import BOOKS, P, BG, EYES

BOOKS.append(dict(
    slug="hail", seed=113000, title="冰雹是怎么长大的", subtitle="在云里上上下下滚了好多趟",
    keyword="冰雹", style_label="彩色铅笔",
    style="children's picture book illustration, coloured pencil drawing with visible layered "
          "strokes and grainy hatching, slate blue, ice white and warm ochre",
    character="wearing a mustard yellow hoodie, dark blue jeans and grey sneakers, short black hair",
    palette=P(("#232a31", "#6b7d8c", "#eef2f4", "#f9fbfc", "#c2622f", "#7d8a93", "#d3dbe0"),
              ("#e6ecf0", "#8fa3b2", "#0d1218", "#141b22", "#d8834d", "#7d8a93", "#2a343d")),
    diagram=[2, 4, 5, 7, 9, 11],
    assets=[
        "One single round hailstone of white and clear ice, about as big as a walnut, lying on "
        "its own. " + BG,
        "One single hailstone sawn in half and seen face on, showing many rings of white and "
        "clear ice one inside the other, from a tiny core out to the rim. " + BG,
        "One single tall storm cloud seen from far away, dark and heavy along its base and spread "
        "flat and wide across its top. " + BG,
        "One single onion cut in half and seen face on, showing its many layers one inside the "
        "other. " + BG,
    ],
    pages=[
     ("屋顶忽然噼啪响。\n跑到窗边一看，\n草地上蹦着\n一粒一粒小白珠。\n爸爸说，那是冰雹。",
      f"A head-and-shoulders portrait of the little boy at a window with small white ice pellets bouncing on the "
      f"grass outside, only his head and shoulders inside the picture and everything below his chest outside the frame, his face turned straight towards the viewer, {EYES}, his "
      f"mouth open in surprise.", 1),
     ("冰雹不是雨冻的。\n它长在一朵\n又高又厚的云里。\n那种云叫积雨云，\n顶比飞机还高。", "", 0),
     ("那朵云的里面\n有一股很强的风，\n是竖着往上吹的。\n它能把水珠\n一直往上顶。",
      "One enormous storm cloud seen from far below, dark and flat along its base and piled up "
      "high into a wide flat top, the sky filling the whole picture right out to all four edges. "
      "Nothing else in the picture.", 0),
     ("云里面的风\n不只是往上。\n有的地方往上冲，\n旁边就往下沉，\n上上下下转个不停。", "", 0),
     ("越往上越冷。\n升过某一条线，\n水就冻住了。\n水珠一过那儿，\n立刻裹上一层冰。", "", 0),
     ("小冰粒变沉了，\n开始往下掉。\n还没落到地面，\n又被一股风\n托了回去。",
      "One small round pellet of ice deep inside a dark storm cloud, tilted as it is carried "
      "upward, the churning cloud filling the whole picture right out to all four edges. Nothing "
      "else in the picture.", 0),
     ("上去，结一层冰。\n掉下来，化一点。\n再上去，又结一层。\n这样来回好多趟，\n它就一点点变大。", "", 0),
     ("什么时候才掉下来？\n等它太重了，\n风托不住了，\n就一路砸下来，\n谁也拦不住。",
      "One hailstone falling fast out of the dark flat base of a storm cloud with a streak of "
      "motion behind it, the cloud and sky filling the whole picture right out to all four edges. "
      "Nothing else in the picture.", 0),
     ("把一颗冰雹切开，\n里面一圈套一圈，\n像切开的洋葱。\n数一数有几圈，\n就知道它上去过几趟。", "", 0),
     ("大多数冰雹\n只有豆子那么大。\n可也下过几回\n拳头那么大的，\n把车顶砸出坑。",
      "A close view of green grass with hailstones of several sizes resting on it, from tiny "
      "pellets to one as big as a fist, the grass filling the whole picture right out to all four "
      "edges. Nothing else in the picture.", 0),
     ("我们洛杉矶\n几乎不下冰雹。\n这儿的云不够高，\n也不够冷。\n别的地方年年都有。", "", 0),
     ("我捡起一粒，\n凉凉的，很快化了。\n它在那朵云里\n上上下下跑了那么久，\n才跑到我手上。",
      f"A head-and-shoulders portrait of the little boy holding one small white hailstone in his open palm and "
      f"looking down at it, only his head and shoulders inside the picture and everything below his chest outside the frame, his face turned straight towards the viewer, {EYES}, "
      f"quietly amazed.", 1),
    ]))

BOOKS.append(dict(
    slug="tornado", seed=114000, title="龙卷风", subtitle="一根从云里垂下来的柱子",
    keyword="龙卷风", style_label="油画棒",
    style="children's picture book illustration, oil pastel drawing with thick waxy strokes and "
          "smudged blending, storm grey, olive green and warm ochre",
    character="wearing a red and white striped t-shirt, denim overalls and blue sneakers, short black hair",
    palette=P(("#26241c", "#6e7461", "#f0eee4", "#faf9f2", "#c06a34", "#857b63", "#d7d5c4"),
              ("#e9e6d9", "#98a088", "#121309", "#1d1e12", "#d78a54", "#857b63", "#343524")),
    diagram=[2, 4, 6, 8, 10],
    assets=[
        "One single tall twisting funnel of grey air, wide at the top and narrowing to a point at the bottom, its surface drawn as spiralling bands, floating alone with nothing around it and nothing under it. " + BG,
        "One single dark storm cloud with a low flat rotating base underneath it and a broad flat "
        "top. " + BG,
        "One single red wooden barn with a pitched roof, floating alone with nothing around it and nothing under it. " + BG,
        "One single wooden spinning top, upright and balanced on its point, floating alone with nothing around it and nothing under it. " + BG,
    ],
    pages=[
     ("叔叔在堪萨斯，\n发来一段视频。\n天边垂下一根柱子，\n慢慢扫过田地。\n那是龙卷风。",
      f"A head-and-shoulders portrait of the little boy holding a small tablet in both hands and looking up, his "
      f"face large in the frame and turned towards the viewer, {EYES}, wide-eyed.", 1),
     ("龙卷风这东西，\n是从云里长出来的。\n先得有一朵大雷云，\n云底下的空气\n开始慢慢打转。", "", 0),
     ("一开始转得很宽，\n也转得很慢，\n像一锅搅动的汤。\n从地上看上去，\n只是云压得很低。",
      "One huge dark storm cloud with a low flat base hanging over open fields, the sky filling "
      "the whole picture right out to all four edges. Nothing else in the picture.", 0),
     ("空气一边转，\n一边往中间挤。\n圈子越挤越小，\n转得就越来越快，\n像滑冰时收起胳膊。", "", 0),
     ("转得快了，\n云底垂下一个尖，\n像一根倒过来的\n细细的萝卜，\n越伸越长。",
      "One grey funnel of air hanging halfway down from the flat base of a dark storm cloud, "
      "narrowing towards its tip, the sky filling the whole picture right out to all four edges. "
      "Nothing else in the picture.", 0),
     ("尖一直往下伸。\n碰到地面那一下，\n它才算龙卷风。\n没碰到地的，\n只能叫漏斗云。", "", 0),
     ("一接到地，\n地上的土和草\n就被卷起来，\n跟着它一起转，\n柱子立刻变黑了。",
      "One tornado touching the ground with dust and bits of grass whirling up around its foot, "
      "the storm sky filling the whole picture right out to all four edges. Nothing else in the "
      "picture.", 0),
     ("柱子越细，\n转得越凶。\n最凶的龙卷风，\n比高速路上的车\n还要快上一倍。", "", 0),
     ("它走得并不快，\n开车都能追上。\n可它走过的地方，\n房顶、大树、汽车，\n全被抬起来扔出去。",
      "One narrow tornado crossing an empty flat field, its column leaning slightly, the storm sky "
      "filling the whole picture right out to all four edges. Nothing else in the picture.", 0),
     ("美国中部的平原，\n年年都有很多。\n那儿暖空气和冷空气\n老撞在一起。\n我们加州几乎没有。", "", 0),
     ("它也转不了多久。\n慢慢变细，\n细得像一根绳子，\n晃了两下，\n就缩回云里去了。",
      "One thin ropelike tornado bending and lifting away from the ground back towards the cloud "
      "base, the sky filling the whole picture right out to all four edges. Nothing else in the "
      "picture.", 0),
     ("我把那段视频\n又看了一遍。\n那根粗大的柱子，\n原来是空气\n自己转出来的。",
      f"A head-and-shoulders portrait of the little boy sitting and holding the small tablet on his knees, his "
      f"face large in the frame and turned towards the viewer, {EYES}, thoughtful.", 1),
    ]))

BOOKS.append(dict(
    slug="forecast", seed=115000, title="明天会下雨吗", subtitle="天气预报是怎么做出来的",
    keyword="天气预报", style_label="钢笔淡彩",
    style="children's picture book illustration, fine pen lines with light transparent watercolour "
          "washes, teal blue, pale grey and warm sand",
    character="wearing a teal blue t-shirt, khaki shorts and orange sneakers, short black hair",
    palette=P(("#1f2a2e", "#5f7f85", "#eef2f2", "#fafcfb", "#c87a35", "#7c8c8b", "#d2dedd"),
              ("#e4edec", "#86a4a8", "#0b1315", "#121c1e", "#dd964f", "#7c8c8b", "#26363a")),
    diagram=[2, 5, 7, 9, 10, 11],
    assets=[
        "One single white louvred weather station box standing on four thin legs on short grass. "
        + BG,
        "One single large white weather balloon in flight with a small white instrument box "
        "hanging below it on a thin line. " + BG,
        "One single white radar dome shaped like a ball, sitting on top of a short square tower. "
        + BG,
        "One single weather satellite with two long flat solar wings and a small dish on its body. "
        + BG,
    ],
    pages=[
     ("明天要去海边。\n我问爸爸，\n明天会下雨吗？\n他看看手机说，\n下雨的可能是一成。",
      f"A head-and-shoulders portrait of the little boy looking up and asking a question, his face large in the "
      f"frame and turned towards the viewer, {EYES}, eyebrows raised.", 1),
     ("要算明天，\n先得量今天。\n量温度，量气压，\n量风往哪儿吹，\n量空气有多潮。", "", 0),
     ("地上到处是气象站。\n一个白白的小箱子，\n立在草地当中。\n箱子上有小百叶窗，\n风能吹进去。",
      "One white louvred weather station box on four legs standing in a wide grass field under an "
      "open sky, the field and sky filling the whole picture right out to all four edges. Nothing "
      "else in the picture.", 0),
     ("天上也得量。\n每天两次，\n一只大气球\n带着小盒子往上飘，\n一边飘一边发数字。",
      "One large white weather balloon rising high with a small instrument box swinging below it, "
      "the open sky filling the whole picture right out to all four edges. Nothing else in the "
      "picture.", 0),
     ("气球一路往上，\n越高越冷。\n飘到最高的地方，\n盒子外头的空气，\n比冰箱里冷得多。", "", 0),
     ("还有雷达。\n那是一个大白球，\n蹲在山顶上。\n球里面的天线\n一圈一圈地转。",
      "One white ball-shaped radar dome on a short tower standing on a bare hilltop under a wide "
      "open sky, the hill and sky filling the whole picture right out to all four edges. Nothing "
      "else in the picture.", 0),
     ("雷达往外发一下，\n碰到雨点，\n就弹回来一点点。\n弹回来得越强，\n那边的雨就越大。", "", 0),
     ("更高的地方\n还有卫星。\n它从上往下看，\n一眼就看得见\n整片云往哪儿走。",
      "One weather satellite with two long solar wings floating high above the curved edge of the "
      "Earth, dark space and the bright edge of the planet filling the whole picture right out to "
      "all four edges. Nothing else in the picture.", 0),
     ("量到的数字\n都填进一张大格子。\n把空气切成\n一个一个小方块，\n每块都有自己的数。", "", 0),
     ("再交给计算机。\n它算这块空气\n一小时后到哪儿，\n三小时后变成什么样，\n一步一步往前推。", "", 0),
     ("所以算明天很准。\n算下个星期，\n就没那么准了。\n空气的事，\n差一点就跑偏。", "", 0),
     ("第二天早上，\n天真的没下雨。\n那句话不是猜的，\n是一格一格\n算出来的。",
      f"A head-and-shoulders portrait of the little boy standing on a sunny beach with a bucket in one hand, his "
      f"face large in the frame and turned towards the viewer, {EYES}, grinning.", 1),
    ]))

BOOKS.append(dict(
    slug="dew", seed=116000, title="早上草叶上的水珠", subtitle="露水和霜是从哪儿来的",
    keyword="露水", style_label="软色粉",
    style="children's picture book illustration, soft pastel drawing with velvety blended tones "
          "and a gentle grain, dawn lilac, misty green and pale gold",
    character="wearing a lavender purple hoodie, grey sweatpants and green rubber boots, short black hair",
    palette=P(("#2b2a33", "#7c8a86", "#f1f3ef", "#fbfcf9", "#8f7bb5", "#8a8577", "#dadfd8"),
              ("#e9eae4", "#9aa8a2", "#0f1116", "#191b21", "#a892cf", "#8a8577", "#2e3239")),
    diagram=[2, 4, 6, 8, 10],
    assets=[
        "One single blade of green grass standing upright with several round clear water drops "
        "resting along it. " + BG,
        "One single green leaf lying flat and seen from above, covered all over with tiny round "
        "water drops. " + BG,
        "One single sprig of grass stiff with white frost, its edges fringed with small white ice "
        "needles. " + BG,
    ],
    pages=[
     ("早上去上学，\n草叶上全是水珠。\n昨天晚上没下雨呀。\n这些水珠到底\n是从哪儿来的？",
      f"A head-and-shoulders portrait of the little boy crouching beside a dewy lawn in the early morning, his "
      f"face large in the frame and turned towards the viewer, {EYES}, puzzled.", 1),
     ("空气里一直有水，\n只是看不见。\n它散成极小的粒，\n小得看不出来，\n混在空气中间。", "", 0),
     ("草叶是凉的。\n凉东西旁边的空气，\n也跟着凉下来。\n一凉下来，\n它就装不下那么多水。",
      "A close view of green grass blades in the early morning with round clear water drops "
      "resting on them, the grass filling the whole picture right out to all four edges. Nothing "
      "else in the picture.", 0),
     ("空气像个口袋。\n热的时候口袋大，\n装得下很多水；\n凉下来口袋就小了，\n装不下的只好出来。", "", 0),
     ("夜里为什么会凉？\n因为地面这一晚，\n一直在往天上放热。\n天上没云的夜，\n放得最痛快。",
      "A wide grass lawn at night under a clear sky full of small stars, the sky filling the whole "
      "picture right out to all four edges. Nothing else in the picture.", 0),
     ("有云的夜就不同。\n热往上走，\n被云挡回来一半。\n所以阴天的早上，\n草叶常常是干的。", "", 0),
     ("水汽碰到凉叶子，\n就停在上面，\n一粒一粒并起来，\n变成一颗水珠。\n这就是露水。",
      "A very close view of one green blade of grass holding a single large round clear water "
      "drop, soft green blur filling the whole picture right out to all four edges. Nothing else "
      "in the picture.", 0),
     ("露水不是天上掉的，\n也不是草根里冒的。\n它本来就在\n叶子旁边的空气里，\n只是现出了形。", "", 0),
     ("要是更冷呢？\n冷过结冰那条线，\n水汽就不停成水珠，\n直接变成冰，\n贴在叶子上。",
      "A wide field of grass stiff and white with frost in the first light of morning, the field "
      "and the pale sky filling the whole picture right out to all four edges. Nothing else in "
      "the picture.", 0),
     ("那就是霜。\n霜不是冻住的露，\n是水汽一步跨过去，\n直接长成的冰。", "", 0),
     ("太阳一出来，\n草叶就暖了。\n水珠一颗颗变小，\n又回到空气里，\n像从来没有过。",
      "A low morning sun just above a grass field with the last water drops shining on the "
      "blades, the field and the glowing sky filling the whole picture right out to all four "
      "edges. Nothing else in the picture.", 0),
     ("我伸手在草叶上\n抹了一下，\n手心凉凉地湿了。\n这一小片水，\n昨晚一直在我旁边。",
      f"A head-and-shoulders portrait of the little boy holding up one open palm wet with dew, his face large in "
      f"the frame and turned towards the viewer, {EYES}, smiling a little.", 1),
    ]))
