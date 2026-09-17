# -*- coding: utf-8 -*-
"""第七批（9/10）：章鱼、企鹅、骆驼、蛇。"""
from dino7_a import BOOKS, P, BG, EYES

BOOKS.append(dict(
    slug="octopus", seed=121000, title="章鱼有三个心脏", subtitle="还有八条会自己想事的胳膊",
    keyword="章鱼", style_label="软色粉",
    style="children's picture book illustration, soft chalk pastel with velvety grain and "
          "smudged blended edges, deep sea blue, coral red and warm sand",
    character="wearing a deep blue hoodie, grey shorts and white sneakers, short black hair",
    palette=P(("#232a30", "#5f7d8c", "#eef2f2", "#f8fbfa", "#c2543f", "#7d7a66", "#cfd9d8"),
              ("#e6ecec", "#8ba7b3", "#0d1418", "#151d22", "#d97a62", "#7d7a66", "#2a3238")),
    diagram=[2, 4, 6, 9, 11],
    assets=[
        "One single octopus with a large rounded head and eight long arms trailing behind it, "
        "seen from the side facing left, its whole body inside the picture. " + BG,
        "One single small heart, a pale muscular lump with two short tubes leaving it, lying "
        "alone. " + BG,
        "One single gill of a sea animal, a soft feathery comb of many thin pale filaments, lying "
        "alone. " + BG,
        "One single small crab seen from above, its whole body inside the picture. " + BG,
    ],
    pages=[
     ("水族馆的玻璃后面，\n一团红红的东西\n正贴着石头慢慢挪。\n爸爸说那是章鱼，\n它有八条胳膊。",
      f"Waist-up view of the little boy at an aquarium window, his face large in the frame and "
      f"turned towards the viewer, {EYES}, his nose almost touching the glass; behind the glass a "
      f"red octopus rests against a rock.", 1),
     ("章鱼有三个心脏。\n两个小的挨着鳃，\n把血压进鳃里去。\n中间那个大的，\n再把血送到全身去。",
      "", 0),
     ("它的血不是红的，\n是淡淡的蓝色。\n因为里面带的是铜，\n不像我们带着铁。\n铜一遇上氧就发蓝。",
      "A close view of one octopus arm opened on a cream background, pale blue blood showing in "
      "the fine vessels inside it. Nothing else in the picture.", 0),
     ("它游起来的时候，\n中间那个大心脏\n会停下来不跳了。\n所以章鱼不爱游泳，\n更爱慢慢地爬。", "", 0),
     ("它的八条胳膊上\n排满了圆吸盘，\n一条腕排着两行，\n加起来好几百个。\n吸住了就不容易掉。",
      "Close view of one octopus arm lying across a cream background, two neat rows of round "
      "suckers along its underside. Nothing else in the picture.", 0),
     ("它的神经细胞\n并不全在脑袋里。\n有一大半都长在\n那八条胳膊上面，\n脑袋里反而少一些。", "", 0),
     ("所以它每条胳膊\n都能自己拿主意。\n一条去翻石头，\n另一条去摸石缝，\n谁也不用等谁。",
      "One octopus on a cream background with its eight arms reaching in different directions, "
      "one arm lifting a small stone and another arm feeling into a narrow gap between rocks. "
      "Nothing else in the picture.", 0),
     ("人们常说，章鱼\n像是有九个脑子：\n一个长在头顶上，\n八个长在胳膊里，\n各想各的事情。",
      "One single octopus arm lying alone on a cream background, its tip closing around a small "
      "crab. Nothing else in the picture.", 0),
     ("它全身上下，\n只有嘴是硬的。\n一个嘴那么大的洞，\n整只章鱼的身子\n都能挤着钻过去。", "", 0),
     ("它的皮肤里面\n藏着许多色素袋。\n肌肉一拉一松，\n颜色就跟着变，\n一眨眼就和石头一样。",
      "One octopus pressed against a rough grey rock on a cream background, half of its skin "
      "already the same grey as the rock and half still smooth and red. Nothing else in the "
      "picture.", 0),
     ("它的吸盘还能尝味。\n胳膊一贴上石头，\n就知道石头底下\n藏没藏着螃蟹，\n连眼睛都不用看。", "", 0),
     ("我隔着玻璃，\n一条一条数胳膊。\n数到第八条的时候，\n它身子里那三个心脏\n正一起跳着呢。",
      f"Waist-up view of the little boy counting on his fingers at the aquarium window, his face "
      f"large in the frame and turned towards the viewer, {EYES}, delighted; the red octopus "
      f"spreads its arms behind the glass.", 1),
    ]))

BOOKS.append(dict(
    slug="penguin", seed=122000, title="企鹅站在冰上为什么不冷", subtitle="三层保暖，外加挤在一起",
    keyword="企鹅", style_label="彩色铅笔",
    style="children's picture book illustration, coloured pencil with visible hatching strokes "
          "and layered shading, ice blue, slate grey and pale gold",
    character="wearing a red puffer jacket, dark blue jeans and grey boots, short black hair",
    palette=P(("#24272e", "#6a7a8c", "#f0f2f4", "#fafbfc", "#d09a3c", "#7b7668", "#d5dade"),
              ("#e8eaee", "#93a3b2", "#0e1216", "#171b20", "#e0b05c", "#7b7668", "#2d3238")),
    diagram=[2, 4, 6, 8, 10],
    assets=[
        "One single emperor penguin standing upright on both feet, seen from the side facing "
        "left, its whole body inside the picture. " + BG,
        "One single penguin feather lying alone, short and stiff with a tuft of soft down at its "
        "base. " + BG,
        "One single thick woollen blanket folded into a neat rectangle, lying alone. " + BG,
    ],
    pages=[
     ("玻璃后面是一块冰，\n几只企鹅站在上面。\n冰凉得直冒白气，\n它们光着两只脚，\n却一点也不缩。",
      f"Waist-up view of the little boy in a warm jacket at a zoo window, his face large in the "
      f"frame and turned towards the viewer, {EYES}, wondering; behind the glass two penguins "
      f"stand on a slab of ice.", 1),
     ("企鹅身上有三层。\n最外面是羽毛，\n羽毛底下压着空气，\n皮底下还藏着\n厚厚的一层脂肪。", "", 0),
     ("它的羽毛又短又硬，\n一根压着一根，\n密得像鱼鳞一样。\n巴掌那么大一块皮，\n能长出上千根来。",
      "Close view of a patch of penguin skin on a cream background, short stiff feathers "
      "overlapping each other like tiles. Nothing else in the picture.", 0),
     ("羽毛根上还带着绒。\n绒把空气兜住了，\n空气不爱传热，\n就成了一层被子，\n盖在它的皮上面。", "", 0),
     ("它的尾巴根上\n有一个小油腺。\n它用嘴蘸一点油，\n从头到脚抹一遍，\n水就沾不上身了。",
      "One penguin turning its head back to touch the base of its tail with its beak on a cream "
      "background. Nothing else in the picture.", 0),
     ("腿里的血管很怪，\n往下的和往上的\n紧紧贴在一块儿。\n热还没走到脚上，\n就被带回去了。", "", 0),
     ("所以它的两只脚\n只比冰暖一点点。\n脚上没有多少热，\n底下的冰就化不了，\n它也站得稳稳的。",
      "Close view of two penguin feet standing on a slab of ice on a cream background, the ice "
      "under them still dry and unmelted. Nothing else in the picture.", 0),
     ("天最冷的时候，\n几千只挤成一团。\n外面一圈顶着风，\n里面的暖烘烘的，\n挨着挨着就热了。", "", 0),
     ("挤久了怎么办呢？\n外圈的往里钻，\n里圈的被挤到外面，\n一圈一圈慢慢转，\n轮流站在最外面。",
      "A huddle of many penguins packed tightly together in blowing snow on a cream background, "
      "the ones on the outside leaning into the wind. Nothing else in the picture.", 0),
     ("团里面有多暖和？\n比外面高出好多。\n挤在中间的企鹅\n有时候还嫌热，\n自己挪到边上去。", "", 0),
     ("公企鹅更辛苦。\n蛋放在脚背上，\n肚皮垂下来盖住，\n一站就是两个月，\n风再大也不挪窝。",
      "One male emperor penguin standing still in the snow on a cream background, a single egg "
      "resting on top of his feet and a fold of belly skin hanging over it. Nothing else in the "
      "picture.", 0),
     ("我哈了一口气，\n玻璃上起了白雾。\n擦干净再看过去，\n它还光着两只脚，\n稳稳地站在冰上。",
      f"Waist-up view of the little boy wiping a patch of fog off the zoo window with his mitten, "
      f"his face large in the frame and turned towards the viewer, {EYES}, smiling; a penguin "
      f"stands on ice beyond the glass.", 1),
    ]))

BOOKS.append(dict(
    slug="camel", seed=123000, title="驼峰里装的是什么", subtitle="不是水，是脂肪",
    keyword="骆驼", style_label="油画棒",
    style="children's picture book illustration, oil pastel with thick waxy strokes and blended "
          "edges, sand ochre, terracotta and dusty sky blue",
    character="wearing a pale yellow shirt, khaki shorts and brown sandals, short black hair",
    palette=P(("#2e2820", "#8a7a5a", "#f4f0e6", "#fdfaf2", "#b8603a", "#8a7150", "#e0d8c4"),
              ("#efe9da", "#a99a78", "#171208", "#221c10", "#cf7d50", "#8a7150", "#3a3220")),
    diagram=[2, 4, 6, 8, 10],
    assets=[
        "One single camel standing on four legs, seen from the side facing left, two humps on its "
        "back, its whole body inside the picture. " + BG,
        "One single metal water bucket standing upright with a handle across the top. " + BG,
        "One single thick block of pale yellow butter lying on its side. " + BG,
        "One single thorny desert branch lying alone. " + BG,
    ],
    pages=[
     ("动物园里那只骆驼，\n背上鼓着两个大包。\n我仰着头问爸爸，\n那两个包里装的\n是不是一包水。",
      f"Waist-up view of the little boy at a zoo rail looking up, his face large in the frame and "
      f"turned towards the viewer, {EYES}, asking a question; behind him stands a camel with two "
      f"humps.", 1),
     ("爸爸说不是水。\n驼峰里装的是脂肪，\n像一大块黄油。\n两个包加在一起，\n有三十多公斤重。", "", 0),
     ("脂肪一天天用掉，\n驼峰就瘪下去了，\n软软地歪到一边。\n等它吃饱睡足几天，\n驼峰又鼓起来了。",
      "Two camels standing side by side on a cream background, one with two full upright humps "
      "and one with two empty humps flopping over. Nothing else in the picture.", 0),
     ("脂肪化开的时候，\n一边放出力气，\n一边还出一点水。\n所以不喝水的日子，\n它也能撑很久。", "", 0),
     ("可它一见到水，\n就没完没了地喝。\n十分钟能灌下去\n一百多升水，\n差不多顶一大缸。",
      "One camel lowering its head to drink from a long stone trough on a cream background. "
      "Nothing else in the picture.", 0),
     ("一百升是多少呢？\n够装满十个水桶。\n我一天喝的水，\n连一小桶都不到，\n它一口气就喝完。", "", 0),
     ("沙子刮起来的时候，\n它把两个鼻孔一闭，\n睫毛又长又密，\n像两排小帘子，\n沙子就进不去了。",
      "Close view of a camel's head facing the viewer in blowing sand on a cream background, its "
      "nostrils squeezed shut and its long lashes lowered. Nothing else in the picture.", 0),
     ("它还有个省水的法子：\n白天让身子变热，\n热得受不了才出汗。\n少出一点汗，\n就少丢一点水。",
      "", 0),
     ("它连带刺的枝子\n也能嚼着吃下去。\n嘴唇又厚又灵活，\n刺扎不进去，\n照样能咽下肚。",
      "One camel biting a thorny branch on a cream background, its thick lips folded around the "
      "spines. Nothing else in the picture.", 0),
     ("它的血也不一样。\n里面的红细胞\n是长长的椭圆形，\n缺水变稠的时候\n也能挤着往前走。", "", 0),
     ("它的脚掌很宽，\n踩下去铺开一大片，\n像四块软垫子，\n所以走在软沙上\n也不会往下陷。",
      "Close view of one camel foot pressed onto sand on a cream background, the broad pad spread "
      "out wide and leaving a shallow dent. Nothing else in the picture.", 0),
     ("我算是记住了：\n驼峰里装的不是水，\n是一大块脂肪。\n它不是背着一壶水，\n是背着一袋干粮。",
      f"Waist-up view of the little boy at the zoo rail nodding to himself, his face large in the "
      f"frame and turned towards the viewer, {EYES}, pleased; the two-humped camel stands behind "
      f"him.", 1),
    ]))

BOOKS.append(dict(
    slug="snake", seed=124000, title="蛇没有腿怎么走", subtitle="靠鳞片和肌肉一推一推",
    keyword="蛇", style_label="钢笔淡彩",
    style="children's picture book illustration, fine pen lines with light transparent "
          "watercolour washes, moss green, warm grey and soft amber",
    character="wearing a moss green sweatshirt, dark grey trousers and white sneakers, short "
              "black hair",
    palette=P(("#26291f", "#6f7f5c", "#f1f2ea", "#fbfcf6", "#b5713a", "#7f7a5e", "#d8dcc9"),
              ("#e9ecdd", "#9aa987", "#0f1309", "#1a1e11", "#cb8b55", "#7f7a5e", "#2f3423")),
    diagram=[2, 4, 6, 8, 10],
    assets=[
        # 「蛇」这个词压过了所有限定语：第一版出的是一条盘起来的眼镜蛇，
        # 外框近乎正方，按宽度缩放就是一坨压住整页。所以把「直」写死。
        "One single snake lying stretched out in one perfectly straight line from its head to "
        "the tip of its tail, seen from directly above, its body straight along its whole "
        "length and not coiled, looped or curled at any point. " + BG,
        # 这一片鳞更麻烦：写 belly scale of a snake，模型画的是整条蛇。
        # 索性一个动物词都不提，只描述那块东西本身。
        "One single wide flat horny plate lying alone on flat ground, seen from the side, shaped "
        "like a shallow rectangle much wider than it is tall with a gently rounded front edge, "
        "its front edge resting flat on the ground and its back edge tilted up a little. " + BG,
        "One single length of snake backbone, many small bones joined end to end, each with a "
        "pair of thin ribs. " + BG,
        "One single smooth polished stone lying alone. " + BG,
    ],
    pages=[
     ("玻璃箱里那条蛇\n一动起来就往前溜。\n它一条腿也没有，\n我盯着看了半天，\n还是没看出门道。",
      f"Waist-up view of the little boy crouching in front of a glass tank, his face large in the "
      f"frame and turned towards the viewer, {EYES}, puzzled; a green snake glides across the "
      f"sand behind the glass.", 1),
     ("爸爸让我看它肚子。\n肚皮上有一排鳞，\n一片挨着一片，\n横着排过去，\n从脖子排到尾巴。",
      "", 0),
     ("这排鳞又宽又扁，\n每一片的后边\n都翘起来一点点。\n往前推的时候不费劲，\n往后就勾住地面。",
      "Close view of a snake's underside on a cream background, one row of wide flat belly scales "
      "running along it, each scale's back edge lifted a little. Nothing else in the picture.",
      0),
     ("所以它一使劲，\n鳞片就勾住地面，\n身子被推着往前。\n勾一下，走一点，\n一推一推地往前走。", "", 0),
     ("最常见的走法\n是把身子弯成波浪，\n一边一边地弯。\n每个弯的外边\n都在使劲蹬着地。",
      "One snake moving through short grass on a cream background, its body bent into a wave, "
      "pressing against small stones on the outside of each bend. Nothing else in the picture.",
      0),
     ("身子弯不是白弯的。\n一个弯推一下，\n一个弯又推一下，\n像一道浪从头上\n一直传到尾巴尖。", "", 0),
     ("它还会直着往前走。\n身子一点也不弯，\n肚皮底下的鳞片\n一片一片往后拨，\n像许多只小脚。",
      "One snake moving straight forward along a fallen log on a cream background, its body held "
      "in a straight line. Nothing else in the picture.", 0),
     ("它的骨头也多。\n我们只有二十四根肋骨，\n它有好几百根，\n一根连着一根，\n所以怎么弯都行。",
      "", 0),
     ("可它怕光溜的地方。\n把它放到玻璃上，\n鳞片勾不住东西，\n使多大的劲\n也挪不了几步。",
      "One snake lying on a wide sheet of smooth polished stone on a cream background, its body "
      "bent but going nowhere. Nothing else in the picture.", 0),
     ("沙漠里的蛇\n还有另一种走法：\n身子斜着甩出去，\n一段一段落下，\n沙上留下一排斜道。",
      "", 0),
     ("爬树的时候呢，\n它先绕住树干，\n一圈一圈地箍紧，\n再一节一节地\n把自己一点点往上挪。",
      "One snake wound around a rough tree trunk on a cream background, gripping it tightly as it "
      "works its way upward. Nothing else in the picture.", 0),
     ("我趴在玻璃跟前\n看它肚皮底下。\n那排鳞真的在动，\n一片接着一片，\n把它推着往前走。",
      f"Waist-up view of the little boy lying on the floor with his chin near the glass tank, his "
      f"face large in the frame and turned towards the viewer, {EYES}, absorbed; the green snake "
      f"moves past on the other side.", 1),
    ]))
