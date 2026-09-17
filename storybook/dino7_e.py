# -*- coding: utf-8 -*-
"""第七批恐龙书（5/5）：会爬树的、三个时代、那时候的地球、加州有没有恐龙。"""
from dino7_a import BOOKS, P, BG, EYES

BOOKS.append(dict(
    slug="climb", seed=105000, title="会爬树的恐龙", subtitle="小小的，抓着树干往上蹭",
    keyword="小盗龙", style_label="彩色铅笔",
    style="children's picture book illustration, coloured pencil drawing with visible hatching "
          "strokes and soft layered shading, moss green, warm brown and pale gold",
    character="wearing a mustard yellow t-shirt, dark blue shorts and grey sneakers, short black hair",
    palette=P(("#2b2a24", "#6b7a5a", "#f1f0e6", "#fbfaf4", "#b5703f", "#7d6a4f", "#d8d8c6"),
              ("#e9e7d9", "#93a382", "#12140d", "#1e2015", "#cb8558", "#7d6a4f", "#35382a")),
    diagram=[2, 4, 6, 8, 11],
    assets=[
        "One single small feathered dinosaur the size of a crow, seen from the side facing left, "
        "long feathers growing from both its arms and both its legs, its whole body inside the "
        "picture. " + BG,
        "One single crow standing on the ground, seen from the side facing left, its whole body "
        "inside the picture. " + BG,
        "One single tall straight tree trunk standing upright, with no leaves and no branches. "
        + BG,
        "One single bird foot with three long toes and sharp claws, seen from the side. " + BG,
    ],
    pages=[
     ("院子里有一棵大树，\n我怎么也爬不上去。\n爸爸说很久以前，\n有一种小恐龙，\n天天住在树上。",
      f"Waist-up view of the little boy standing under a tall tree in a backyard, one hand "
      f"resting on the trunk, his face large in the frame and turned towards the viewer, {EYES}, "
      f"a little frustrated.", 1),
     ("它的名字叫小盗龙。\n从头到尾巴尖，\n只有一只乌鸦那么长。\n它站在地上的时候，\n还没我的小腿高。",
      "", 0),
     ("它的爪子又细又尖，\n一钩就挂住树皮。\n后腿使劲一蹬，\n身子往上蹭一截，\n再往上钩一下。",
      "One small feathered dinosaur gripping the side of a tall tree trunk with its front claws, "
      "its body held upright against the bark. Nothing else in the picture.", 0),
     ("最奇怪的地方是，\n它四条腿上\n都长着长长的羽毛。\n前面一边一片，\n后面也是一边一片。", "", 0),
     ("它大概不会扇翅膀，\n只会一路往下滑。\n从这棵树上跳出去，\n在空中飘一段，\n落到那棵树上。",
      "One small feathered dinosaur gliding through the air between two tall trees with its arms "
      "and legs spread wide and its feathers fanned out. Nothing else in the picture.", 0),
     ("爱爬树的那些鸟，\n爪子弯得厉害；\n在地上跑的鸟，\n爪子就要直一些。\n小盗龙的爪子很弯。", "", 0),
     ("住在树上有什么好？\n树上没有大家伙。\n它睡在高高的枝上，\n地面上谁走过去，\n谁也够不着它。",
      "One small feathered dinosaur asleep on a high branch while a much larger dinosaur walks "
      "past on the ground far below. Nothing else in the picture.", 0),
     ("从十米高的树上跳下去，\n它能在空中飘出\n二三十米远。\n树要是再高一点，\n它就能飘得更远。",
      "", 0),
     ("它的化石压在石板里，\n羽毛一根一根，\n都留在石头上。\n过了一亿两千万年，\n还看得清清楚楚。",
      "A flat grey slab of rock holding a small dinosaur skeleton pressed flat, with the shapes "
      "of long feathers preserved in the stone around its arms and legs. Nothing else in the "
      "picture.", 0),
     ("有一块化石的肚子里，\n还留着半条小鱼。\n另外一块里，\n有一只小鸟的脚。\n它就吃这些东西。",
      "A fossil of a small dinosaur lying on grey stone with the bones of a small fish visible "
      "inside its ribcage. Nothing else in the picture.", 0),
     ("地上跑的恐龙\n个个又大又凶。\n它在地上谁也打不过，\n就搬到高处去，\n住在别人上不去的地方。",
      "", 0),
     ("我又去看院子里的树。\n树皮糙糙的。\n要是我也有\n那样一双尖爪子，\n是不是就爬上去了？",
      f"Waist-up view of the little boy pressing his hand flat against the rough bark of a tree "
      f"trunk, his face large in the frame and turned towards the viewer, {EYES}, thinking.", 1),
    ]))

BOOKS.append(dict(
    slug="eras", seed=106000, title="恐龙住了一亿六千万年", subtitle="三个时代，长得都不一样",
    keyword="恐龙时代", style_label="软色粉",
    style="children's picture book illustration, soft chalk pastel with grainy blended strokes "
          "and a visible grain in the surface, dusty violet, slate blue and warm rose",
    character="wearing a dusty purple hoodie, grey trousers and white sneakers, short black hair",
    palette=P(("#2a2733", "#7a7490", "#f2f0f0", "#fbf9f8", "#b4677a", "#8a7a72", "#dcd7dd"),
              ("#e9e5ea", "#a09ab4", "#141020", "#201c28", "#cc8095", "#8a7a72", "#383044")),
    diagram=[2, 4, 6, 8, 9, 10],
    assets=[
        "One single small early dinosaur standing on two legs, waist high, seen "
        "from the side facing left, with a long tail held straight out behind it, its whole body "
        "inside the picture. " + BG,
        "One single very large long-necked dinosaur standing on four legs, seen from the side "
        "facing left, its neck reaching high up, its whole body inside the picture. " + BG,
        "One single tyrannosaurus standing on two legs, seen from the side facing left, its big "
        "head low and its mouth open, its whole body inside the picture. " + BG,
        "One single stegosaurus standing on four legs, seen from the side facing left, a row of "
        "tall flat plates along its back, its whole body inside the picture. " + BG,
    ],
    pages=[
     ("我问爸爸一个问题：\n恐龙在地球上住了多久？\n他说了一个数，\n一亿六千万年。\n这个数我数不完。",
      f"Waist-up view of the little boy holding up five fingers in front of him, his face large "
      f"in the frame and turned towards the viewer, {EYES}, puzzled.", 1),
     ("这么长的日子，\n人们把它分成三段：\n三叠纪、侏罗纪，\n最后是白垩纪。\n一段比一段更长。", "", 0),
     ("最早的那批恐龙不大。\n它们用两条腿跑，\n尾巴伸得直直的，\n站起来大概\n跟一只大狗一样高。",
      "One small early dinosaur running on two legs, waist high, with its long "
      "tail held straight out behind it. Nothing else in the picture.", 0),
     ("那时候它们还不厉害。\n地上有别的爬行动物，\n个头比它们大，\n数量比它们多。\n恐龙只是小小一群。",
      "", 0),
     ("到了侏罗纪，\n恐龙一下子长大了。\n脖子一直伸到树顶，\n一步迈出去，\n比我们一间屋子还长。",
      "One huge long-necked dinosaur standing among tall conifer trees with its head up in the "
      "treetops. Nothing else in the picture.", 0),
     ("最早的那种小恐龙，\n站在它的脚边，\n只够到它的膝盖。\n这中间隔了\n整整五千多万年。", "", 0),
     ("再往后是白垩纪。\n霸王龙来了，\n三角龙也来了。\n地上开始开出花，\n以前的恐龙没见过。",
      "One tyrannosaurus and one horned dinosaur standing apart on open ground with small "
      "flowering plants growing between them. Nothing else in the picture.", 0),
     ("剑龙和霸王龙\n其实没有见过面。\n剑龙先走的，\n又过了八千万年，\n霸王龙才出来。", "", 0),
     ("换一句话说，\n霸王龙离我们，\n比离剑龙还要近。\n我们跟它中间，\n才隔六千六百万年。", "", 0),
     ("从三个时代里\n各挑一只排好：\n一只像一条大狗，\n一只高得像楼房，\n一只满嘴都是牙。", "", 0),
     ("它们自己当然不知道\n住了多少年。\n对它们来说，\n就是一天一天地过，\n过了一亿多年。",
      "One long-necked dinosaur walking slowly across open ground under a low evening sun. "
      "Nothing else in the picture.", 0),
     ("我今年五岁。\n一亿六千万年，\n是我三千多万个五岁。\n我把两只手张开，\n还是想不出来。",
      f"Waist-up view of the little boy holding both hands open in front of him as if measuring "
      f"something far too big, his face large in the frame and turned towards the viewer, "
      f"{EYES}, amazed.", 1),
    ]))

BOOKS.append(dict(
    slug="oldworld", seed=107000, title="那时候的地球长什么样", subtitle="没有草，也没有花",
    keyword="蕨类", style_label="油画棒",
    style="children's picture book illustration, oil pastel with thick waxy strokes and rich "
          "layered colour, deep fern green, warm ochre and burnt orange",
    character="wearing a burnt orange t-shirt, khaki shorts and brown sandals, short black hair",
    palette=P(("#26281f", "#6a7b4a", "#f1efe3", "#faf8ef", "#c07a2e", "#7c6a4a", "#d7d5c0"),
              ("#e8e6d5", "#91a472", "#101208", "#1c1e12", "#d4913f", "#7c6a4a", "#343722")),
    diagram=[3, 5, 7, 9, 11],
    assets=[
        "One single clump of ferns growing from the ground, its long leaves spreading outwards, "
        "the whole clump inside the picture. " + BG,
        "One single tall conifer tree with a straight trunk, its whole shape inside the picture. "
        + BG,
        "One single very large long-necked dinosaur standing on four legs, seen from the side "
        "facing left, its whole body inside the picture. " + BG,
        "One single small flower with a few open petals on a short stem. " + BG,
    ],
    pages=[
     ("我们家门口的地上，\n有草，也有花，\n还有一棵大树。\n爸爸说恐龙那时候，\n这些大多还没有。",
      f"Waist-up view of the little boy standing on a front lawn with small flowers around his "
      f"feet, his face large in the frame and turned towards the viewer, {EYES}, curious.", 1),
     ("那时候的地面上，\n长的都是蕨。\n一丛紧挨着一丛，\n叶子像大羽毛，\n踩上去软软的一片。",
      "A stretch of ground covered in low clumps of ferns growing close together with their long "
      "leaves spreading out. Nothing else in the picture.", 0),
     ("草是很晚很晚才来的。\n等它铺满整个地面，\n恐龙差不多\n已经全走光了。\n它们谁也没吃过草。",
      "", 0),
     ("有一种树叫苏铁，\n长得矮矮胖胖，\n顶上顶着一圈叶子，\n像一把撑开的伞。\n那时候到处都是它。",
      "One short thick cycad tree with a ring of stiff leaves spreading out from the top of its "
      "trunk. Nothing else in the picture.", 0),
     ("针叶树长得最高。\n笔直地往上长，\n能长到二三十米。\n长脖子的恐龙，\n就吃它们的树顶。", "", 0),
     ("还有一种银杏树。\n叶子像一把小扇子。\n我们这条街上，\n现在也种着银杏，\n跟那时候一个样。",
      "One ginkgo tree with small fan-shaped leaves on its spreading branches. Nothing else in "
      "the picture.", 0),
     ("花出现得也很晚。\n恐龙都住了一亿年，\n地上才开出\n头一批小花来。\n花很小，不起眼。", "", 0),
     ("花一开出来，\n虫子就飞来了。\n钻进去找吃的，\n身上沾了一层花粉，\n再带到别的花上。",
      "One small insect flying towards one small open flower on a short stem. Nothing else in "
      "the picture.", 0),
     ("那时候的陆地，\n也不是现在这个样子。\n最早的时候，\n所有的陆地\n都连成一大块。", "", 0),
     ("地球比现在暖。\n南边北边两头，\n都没有厚厚的冰。\n恐龙一直走，\n能走到很南很北。",
      "One dinosaur walking across a wide green plain under a warm low sun near the horizon. "
      "Nothing else in the picture.", 0),
     ("还有一件怪事：\n那时候地球转得快，\n一天比现在短一点，\n一年有三百七十多天，\n比现在多好几天。",
      "", 0),
     ("我跑到院子里，\n拔了一根草，\n又摘了一朵小花。\n就这两样东西，\n恐龙谁也没见过。",
      f"Waist-up view of the little boy holding one blade of grass in one hand and one small "
      f"flower in the other, his face large in the frame and turned towards the viewer, {EYES}, "
      f"pleased with himself.", 1),
    ]))

BOOKS.append(dict(
    slug="california", seed=108000, title="加州有没有恐龙", subtitle="我们脚底下埋着什么",
    keyword="加州化石", style_label="钢笔淡彩",
    style="children's picture book illustration, fine pen lines with light transparent watercolour "
          "washes, sea blue, warm sand and soft ink grey",
    character="wearing a light blue t-shirt, navy shorts and white sneakers, short black hair",
    palette=P(("#21262c", "#5d7f8c", "#eef1f0", "#f9fbfa", "#c26a4a", "#7b6f5e", "#d2d9d8"),
              ("#e4ebea", "#86a7b3", "#0d1216", "#171d20", "#d4825f", "#7b6f5e", "#2c3538")),
    diagram=[2, 5, 7, 9, 11],
    assets=[
        "One single ammonite shell coiled into a flat round spiral, seen from the side, its whole "
        "shape inside the picture. " + BG,
        "One single large sea reptile with a long body, four flippers and a long tail, seen from "
        "the side facing left, its whole body inside the picture. " + BG,
        "One single duck-billed dinosaur standing on four legs, seen from the side facing left, "
        "its flat wide snout lowered, its whole body inside the picture. " + BG,
        "One single sabre-toothed cat standing on four legs, seen from the side facing left, two "
        "long teeth hanging down from its upper jaw, its whole body inside the picture. " + BG,
    ],
    pages=[
     ("博物馆里的这些恐龙，\n是从别的州运来的。\n我就问爸爸，\n加州有没有恐龙。\n他说，很少很少。",
      f"Waist-up view of the little boy standing in a museum hall beside a large dinosaur leg "
      f"bone, his face large in the frame and turned towards the viewer, {EYES}, asking a "
      f"question.", 1),
     ("蒙大拿、犹他那边，\n恐龙骨头一堆一堆。\n加州挖出来的，\n数得过来的，\n一只手都用不完。", "", 0),
     ("为什么这么少呢？\n因为恐龙住着的时候，\n加州这块地方，\n大半都在水底下，\n是一片大海。",
      "A wide open sea with low waves stretching all the way to the horizon under an empty sky. "
      "Nothing else in the picture.", 0),
     ("海里不缺大家伙。\n有一种叫沧龙，\n身子像大蜥蜴，\n尾巴左右一摆，\n在水里追着鱼群跑。",
      "One large sea reptile with a long body and four flippers swimming underwater after a "
      "small fish. Nothing else in the picture.", 0),
     ("还有一种菊石。\n壳一圈一圈盘起来，\n小的像颗纽扣，\n最大的那种，\n比饭桌上的盘子还宽。", "", 0),
     ("鱼龙长得很像海豚，\n可它不是鱼，\n也不是海豚。\n它得浮上水面，\n换一口气再下去。",
      "One ichthyosaur with a smooth dolphin-shaped body breaking the surface of the sea to take "
      "a breath. Nothing else in the picture.", 0),
     ("沧龙、鱼龙、菊石，\n一个都不算恐龙。\n恐龙住在陆地上，\n它们住在水里头。\n这是两回事。", "", 0),
     ("加州也挖到过一只。\n鸭子一样的扁嘴巴，\n在中部的山里找到的。\n现在它就是\n加州的州恐龙。",
      "One duck-billed dinosaur with a flat wide snout standing on a low hillside of dry bare "
      "ground. Nothing else in the picture.", 0),
     ("洛杉矶有个沥青坑。\n里面挖出好多骨头，\n可都不是恐龙的。\n恐龙走了六千多万年，\n那些骨头才四万年。",
      "", 0),
     ("沥青是黑色的，\n黏糊糊的一大片。\n猛犸一脚踩进去，\n就拔不出来了，\n一直陷在那里面。",
      "One woolly mammoth standing stuck in a pool of black sticky tar with its legs sunk in up "
      "to the knees. Nothing else in the picture.", 0),
     ("坑里数量最多的\n是一种大狼，\n挖出来好几千只。\n还有剑齿虎，\n两颗牙有香蕉那么长。", "", 0),
     ("我们脚底下埋的，\n不是恐龙的骨头。\n是海里的大蜥蜴，\n是陷进沥青的猛犸。\n一样很了不起。",
      f"Waist-up view of the little boy standing at a railing beside a black tar pool, his face "
      f"large in the frame and turned towards the viewer, {EYES}, serious and proud.", 1),
    ]))
