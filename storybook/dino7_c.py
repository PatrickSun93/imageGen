# -*- coding: utf-8 -*-
"""第七批恐龙书（3/5）：照顾宝宝、成群走、怎么睡觉、打架。"""
from dino7_a import BOOKS, P, BG, EYES

BOOKS.append(dict(
    slug="mother", seed=97000, title="恐龙会照顾宝宝吗", subtitle="有的守着窝，有的下完就走",
    keyword="窝", style_label="彩色铅笔",
    style="children's picture book illustration, coloured pencil drawing with visible layered "
          "strokes and soft grain, warm mustard, leaf green and soft brown",
    character="wearing a mustard yellow t-shirt, green shorts and white sneakers, short black hair",
    palette=P(("#2b2a24", "#7a8a6e", "#f3f1e8", "#fcfbf6", "#c98a3e", "#8b7d63", "#dedbcb"),
              ("#eae7d9", "#a3b193", "#131509", "#1e2013", "#dda25a", "#8b7d63", "#35381f")),
    diagram=[2, 3, 5, 6, 8, 11],
    assets=[
        "One single duck-billed dinosaur standing on four legs, seen from the side facing left, a "
        "low flat crest in front of its eyes and a wide flat beak, its whole body inside the "
        "picture. " + BG,
        "One single bowl-shaped nest of packed mud seen from the side, hollow in the middle and "
        "heaped up all around the rim. " + BG,
        "One single oval egg standing upright on its narrower end, pale and smooth, entirely "
        "alone: there is no animal, no hatchling and no nest anywhere in the picture. " + BG,
        "One single newly hatched dinosaur with scaly skin, a beaked snout and a stubby tail, "
        "standing on four legs, seen from the side facing left. " + BG,
    ],
    pages=[
     ("博物馆里摆着一窝蛋，\n十几个挨在一起，\n围成一个圈。\n爸爸说这是恐龙的窝。",
      f"Waist-up view of the little boy in a museum beside a mounted nest of fossil eggs, his "
      f"face large in the frame and turned towards the viewer, {EYES}, his mouth open in "
      f"surprise.", 1),
     ("窝是一个泥坑，\n边上堆起一圈土。\n有澡盆那么大，\n蛋就一个挨一个\n一个个竖在坑里。", "", 0),
     ("蛋并不大，\n和柚子差不多。\n那么大的恐龙，\n下出来的蛋\n只有这么一点。", "", 0),
     ("壳碎了以后，\n小恐龙爬出来，\n只有猫那么大，\n腿软软的，\n站都站不稳。",
      "Several newly hatched dinosaurs with scaly skin, beaked snouts and stubby tails sitting in "
      "a bowl-shaped mud nest on a cream background. Nothing else in the picture.", 0),
     ("看它们的腿骨，\n两头还软软的，\n没有长结实。\n这样的腿脚\n走不了远路。", "", 0),
     ("可它们的小牙\n已经磨平了一点。\n牙被磨平，\n就是吃过东西。\n没出窝也有得吃。", "", 0),
     ("窝里还留着\n嚼碎的叶子。\n小恐龙嚼不动，\n是大恐龙嚼好了，\n叼回来喂它们。",
      "One adult duck-billed dinosaur lowering its head over a bowl-shaped mud nest and dropping "
      "chewed leaves to several hatchlings with scaly skin, beaked snouts and stubby tails, on a "
      "cream background. Nothing else in the picture.", 0),
     ("这样的窝不止一个，\n一大片排在一起。\n窝和窝隔开的距离，\n正好是一只\n大恐龙的长度。", "", 0),
     ("另一种恐龙\n干脆趴在窝上，\n前肢张得开开的，\n把整整一圈蛋\n都盖在身子底下。",
      "One feathered dinosaur crouching low on top of a ring of oval eggs on a cream background, "
      "its arms spread wide out over them. Nothing else in the picture.", 0),
     ("也有的恐龙\n根本不守窝。\n找一块暖沙地，\n把蛋埋进去，\n扭头就走了。",
      "One long-necked dinosaur walking away from a patch of sandy ground where oval eggs lie "
      "half buried, on a cream background. Nothing else in the picture.", 0),
     ("不守窝的那种\n一次下几十个蛋，\n能活几个算几个。\n守窝的下得少，\n可是一个个看得住。", "", 0),
     ("我数了数那窝蛋，\n一共十七个。\n真有大恐龙\n嚼碎了叶子\n回来喂它们吗？",
      f"Waist-up view of the little boy leaning over a low glass case of fossil eggs and counting "
      f"them with one raised finger, his face large in the frame and turned towards the viewer, "
      f"{EYES}, curious.", 1),
    ]))

BOOKS.append(dict(
    slug="herd", seed=98000, title="它们为什么一起走", subtitle="一串脚印看出来的事",
    keyword="脚印", style_label="软色粉",
    style="children's picture book illustration, soft pastel drawing with powdery blended strokes "
          "and visible grain, dusty blue, warm clay and pale sand",
    character="wearing a dusty blue t-shirt, sand coloured shorts and white sneakers, short black hair",
    palette=P(("#262a2e", "#7d8b95", "#f1f0ea", "#fbfaf6", "#b2593f", "#7f7566", "#d8d6cc"),
              ("#e9e6dc", "#9fb0ba", "#0f1316", "#1a1e22", "#cb7358", "#7f7566", "#313739")),
    diagram=[2, 3, 5, 6, 8, 10],
    assets=[
        "One single long-necked dinosaur standing on four thick legs, seen from the side facing "
        "left, its whole body inside the picture. " + BG,
        "One single young long-necked dinosaur standing on four legs, seen from the side facing "
        "left, small with a short neck, its whole body inside the picture. " + BG,
        "One single large round dinosaur track seen from straight above, a wide deep hollow "
        "pressed into flat ground. " + BG,
        "One single round metal washtub seen from straight above, wide and shallow. " + BG,
    ],
    pages=[
     ("博物馆的地上\n铺着一块大石板，\n上面一个个坑。\n爸爸说那是脚印，\n恐龙踩出来的。",
      f"Waist-up view of the little boy standing on a big flat slab of rock covered in large "
      f"dinosaur tracks, his face large in the frame and turned towards the viewer, {EYES}, "
      f"surprised.", 1),
     ("最大的那个脚印\n比脸盆还大，\n我整个人坐进去\n还空出一圈。\n那是后脚踩的。", "", 0),
     ("脚印有两种，\n一大一小。\n大的是后脚，\n小的是前脚。\n它是四条腿走路的。", "", 0),
     ("这样的脚印不止一串。\n二十几串排在一起，\n一串挨着一串，\n而且全都朝着\n同一个方向去。",
      "Many rows of large round dinosaur tracks pressed into flat rock on a cream background, all "
      "the rows running in the same direction. Nothing else in the picture.", 0),
     ("没有哪一串\n压在另一串上面，\n谁也没踩着谁。\n这说明它们\n是同时走过去的。", "", 0),
     ("再看得仔细些：\n大脚印走在两边，\n小脚印夹在中间。\n大的在外面，\n小的在里面。", "", 0),
     ("外面才有危险。\n大的走在外圈，\n小的走在当中，\n这样就不容易\n被谁叼走。",
      "A group of long-necked dinosaurs walking together across open ground on a cream "
      "background, the largest ones on the outside and the smaller ones in the middle. Nothing "
      "else in the picture.", 0),
     ("量一量两个脚印\n中间隔多远，\n就能算出来，\n它当时走得多快。\n答案是：不快。", "", 0),
     ("这一串脚印\n是踩在湿泥上的。\n太阳晒了几天，\n泥就变硬，\n后来变成了石头。",
      "One large round dinosaur track pressed deep into wet mud on a cream background, water "
      "gathering in the bottom of it. Nothing else in the picture.", 0),
     ("它们一起走，\n是要换个地方。\n一片树叶吃光了，\n就往前挪一挪，\n再找一片。", "", 0),
     ("也不是都这样。\n有的石头上\n从头到尾只有一串，\n孤零零的，\n那是自己走的。",
      "One single line of large round dinosaur tracks crossing flat rock on a cream background, "
      "with no other tracks anywhere. Nothing else in the picture.", 0),
     ("我踩在脚印里，\n一步一步往前走。\n一亿年前，\n这里真的走过\n一大群恐龙。",
      f"Waist-up view of the little boy standing with one foot inside a huge dinosaur track "
      f"in the rock, his face large in the frame and turned towards the viewer, {EYES}, smiling.",
      1),
    ]))

BOOKS.append(dict(
    slug="dinosleep", seed=99000, title="恐龙怎么睡觉", subtitle="蜷成一团，把头埋进胳膊里",
    keyword="睡觉", style_label="油画棒",
    style="children's picture book illustration, oil pastel drawing with thick waxy strokes and "
          "rich blended colour, deep indigo, warm amber and dusty cream",
    character="wearing a dark blue t-shirt, grey shorts and white sneakers, short black hair",
    palette=P(("#232433", "#5f6486", "#f2f0ea", "#fcfaf5", "#c97b52", "#7c7260", "#dbd8cc"),
              ("#ebe8dc", "#8d93b5", "#0d0e18", "#171a26", "#dd9066", "#7c7260", "#33354a")),
    diagram=[2, 3, 5, 7, 8, 10],
    assets=[
        "One single small feathered dinosaur curled up asleep on the ground, seen from the side, "
        "its legs folded under its body, its tail wrapped around it and its snout tucked under "
        "one forelimb. " + BG,
        "One single duck standing on two legs, seen from the side facing left, its whole body "
        "inside the picture. " + BG,
        "One single small bird asleep, seen from the side, its neck turned back and its beak "
        "tucked under one wing. " + BG,
    ],
    pages=[
     ("石头上有一只恐龙，\n缩成小小一团，\n头埋在胳膊底下。\n爸爸说它是睡着的。",
      f"Waist-up view of the little boy in a museum in front of one small curled-up dinosaur "
      f"fossil in a slab of rock, his face large in the frame and turned towards the viewer, "
      f"{EYES}, curious.", 1),
     ("这只恐龙不大，\n和一只鸭子差不多。\n名字叫寐龙，\n寐就是睡觉的意思。", "", 0),
     ("它是这样睡的：\n四条腿收在身子下，\n尾巴绕过来\n圈住自己，\n头掖进前肢里。", "", 0),
     ("鸟睡觉也这样。\n站在树枝上，\n脖子往后一弯，\n把嘴埋进翅膀里，\n一动不动。",
      "One small bird asleep on a branch on a cream background, its neck turned back and its beak "
      "tucked under one wing. Nothing else in the picture.", 0),
     ("为什么要埋起头？\n为了暖和。\n嘴巴一埋进去，\n呼出来的气\n就不会白白跑掉。", "", 0),
     ("石头里全是火山灰。\n那天夜里火山喷了，\n灰一层一层落下来，\n盖住了它，\n它就没再醒。",
      "One small curled-up dinosaur lying asleep on the ground on a cream background with grey "
      "volcanic ash falling thickly over it. Nothing else in the picture.", 0),
     ("这样的化石\n前后找到了两只，\n睡觉的姿势\n一模一样，\n可见不是碰巧摆的。", "", 0),
     ("大恐龙蜷不起来。\n它们太沉了，\n只能就地趴下，\n把肚子贴住地，\n头搁在前面。", "", 0),
     ("长脖子的那种\n睡觉更麻烦。\n那么长一条脖子，\n只好放下来，\n盘在身子边上。",
      "One long-necked dinosaur lying asleep on the ground on a cream background, its long neck "
      "laid down and resting beside its body. Nothing else in the picture.", 0),
     ("怎么知道谁夜里醒着？\n看眼睛周围\n那一圈小骨头。\n这圈骨头大的，\n夜里也看得见。", "", 0),
     ("睡着了最危险。\n所以它们睡得浅，\n一点点动静\n就睁开眼睛。\n有的还轮着睡。",
      "One dinosaur lying curled asleep on open ground on a cream background with one eye open. "
      "Nothing else in the picture.", 0),
     ("晚上我也蜷着睡，\n手塞在脸底下。\n一亿年前的那只，\n睡的姿势\n和我差不多。",
      f"Waist-up view of the little boy curled up in bed at night with both hands tucked under "
      f"his cheek, his face large in the frame and turned towards the viewer, {EYES}, sleepy.", 1),
    ]))

BOOKS.append(dict(
    slug="fight", seed=100000, title="打到一半被埋住了", subtitle="一块化石里的两只恐龙",
    keyword="搏斗化石", style_label="钢笔淡彩",
    style="children's picture book illustration, fine pen line work with light watercolour "
          "washes, sand ochre, brick red and warm grey",
    character="wearing a brick red t-shirt, khaki shorts and white sneakers, short black hair",
    palette=P(("#1f1e1a", "#6b6a58", "#f2efe4", "#fcfaf3", "#a8503a", "#8a7a5c", "#dcd8c7"),
              ("#ece8d9", "#9d9c86", "#121108", "#1e1c10", "#c56a4e", "#8a7a5c", "#37341e")),
    diagram=[2, 3, 4, 6, 8, 10],
    assets=[
        "One single small two-legged dinosaur covered in feathers, seen from the side facing "
        "left, a long stiff tail behind it and one large sharp claw held up off the ground on "
        "each back foot, its whole body inside the picture. " + BG,
        "One single four-legged dinosaur with a parrot-like beak and a short bony frill behind "
        "its head, seen from the side facing left, its whole body inside the picture. " + BG,
        "One single turkey standing on two legs, seen from the side facing left. " + BG,
        "One single large sharp claw of bone, thick and heavy at its base and narrowing to one "
        "fine point. " + BG,
    ],
    pages=[
     ("一块石头里\n卡着两只恐龙，\n一只咬住对方的胳膊，\n另一只的爪子\n钩在它脖子上。",
      f"Waist-up view of the little boy in a museum beside one slab of rock holding two dinosaur "
      f"skeletons locked together, his face large in the frame and turned towards the viewer, "
      f"{EYES}, his mouth open in surprise.", 1),
     ("一只是伶盗龙，\n两条腿，尖爪子。\n一只是原角龙，\n四条腿走路，\n嘴巴像鹦鹉。", "", 0),
     ("伶盗龙后脚上\n有一根大爪子，\n平时翘着不落地，\n要用的时候\n才扳下来。", "", 0),
     ("那根大爪子\n就卡在原角龙\n脖子那块地方。\n那儿有大血管。\n它知道往哪儿下手。", "", 0),
     ("原角龙也没闲着。\n它的嘴像一把钳子，\n死死咬住了\n伶盗龙的右胳膊，\n骨头都咬断了。",
      "Close view of one parrot-beaked dinosaur's beak clamped tightly on the forearm of a "
      "smaller two-legged dinosaur on a cream background. Nothing else in the picture.", 0),
     ("谁也不松开。\n一个钩着脖子，\n一个咬着胳膊，\n就这样僵在那儿，\n动不了了。", "", 0),
     ("就在这时候，\n旁边的沙丘塌了。\n几吨重的沙子\n一下子压下来，\n把它们盖住。",
      "A steep sand dune collapsing and pouring down over two dinosaurs locked together on the "
      "ground on a cream background. Nothing else in the picture.", 0),
     ("沙子埋得太快，\n它们来不及倒下，\n也没被别人拖走。\n所以打架的样子\n原封不动留到今天。", "", 0),
     ("八千万年以后，\n有人在蒙古的沙漠里\n挖到了这块石头。\n一挖出来\n就看呆了。",
      "Two dinosaur skeletons still locked together, lying half uncovered in desert sand on a "
      "cream background. Nothing else in the picture.", 0),
     ("伶盗龙其实不大，\n只有火鸡那么高，\n身上还长着羽毛，\n站直了身子\n才到我胸口。", "", 0),
     ("那谁赢了呢？\n谁也没赢。\n两只一起被埋，\n一起变成石头，\n到现在还没分开。",
      "Close view of one large sharp claw on the back foot of a small two-legged dinosaur, still "
      "hooked into the neck of a larger four-legged dinosaur, on a cream background. Nothing else "
      "in the picture.", 0),
     ("我趴在玻璃上看。\n它们打到一半，\n沙子就下来了。\n八千万年过去，\n还是那个姿势。",
      f"Waist-up view of the little boy with both hands pressed flat on a glass case, two "
      f"dinosaur skeletons locked together inside it, his face large in the frame and turned "
      f"towards the viewer, {EYES}, thoughtful.", 1),
    ]))
