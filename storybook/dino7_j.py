# -*- coding: utf-8 -*-
"""第七批（10/10）：蝌蚪变青蛙、海龟找家、猫头鹰的眼睛、鲸鱼呼吸。"""
from dino7_a import BOOKS, P, BG, EYES

BOOKS.append(dict(
    slug="tadpole", seed=125000, title="小蝌蚪怎么变成青蛙", subtitle="先长后腿，再长前腿，尾巴自己没了",
    keyword="蝌蚪", style_label="彩色铅笔",
    style="children's picture book illustration, coloured pencil drawing with visible hatching "
          "strokes and grainy layered colour, pond green, warm yellow and soft brown",
    character="wearing a grass green t-shirt, khaki shorts and blue rubber boots, short black hair",
    palette=P(("#242a20", "#5f7a55", "#eef2e7", "#f9fbf4", "#7fa23c", "#7a7a52", "#d3ddc7"),
              ("#e6eddd", "#8fa87f", "#0f1408", "#181d10", "#9dbf5a", "#7a7a52", "#2d3524")),
    diagram=[3, 4, 5, 7, 8, 11],
    assets=[
        "One single tadpole seen from the side facing left, a round head and a long flat tail, "
        "its whole body inside the picture. " + BG,
        "One single frog sitting on four legs, seen from the side facing left, its long back legs "
        "folded and no tail at all, its whole body inside the picture. " + BG,
        "One single clear jelly mass of frog eggs with many small dark dots set inside it. " + BG,
        "One single green lily pad lying flat, seen from above, with one narrow notch cut into "
        "its edge. " + BG,
    ],
    pages=[
     ("春天，池塘边，\n水里有一群黑点。\n它们摆着尾巴游，\n爸爸说那不是鱼，\n是小蝌蚪。",
      f"Waist-up view of the little boy crouching at the edge of a pond, his face large in the "
      f"frame and turned towards the viewer, {EYES}, looking down into the water with delight.", 1),
     ("它们从卵里孵出来。\n一团透明的果冻，\n里面点着黑芝麻。\n每一粒黑芝麻，\n将来都是一只青蛙。",
      "One clear jelly mass of frog eggs floating in still water on a cream background, many "
      "small dark dots set inside it. Nothing else in the picture.", 0),
     ("刚出来的蝌蚪\n没有腿，也没有肺。\n它的脖子两边\n长着一丛鳃，\n像鱼一样在水里呼吸。", "", 0),
     ("过了几个星期，\n它的屁股后面\n先鼓出两个小包。\n小包慢慢伸长，\n变成两条后腿。", "", 0),
     ("后腿长好了，\n前腿才开始长。\n前腿先藏在皮里，\n有一天早上，\n忽然从两边顶出来。", "", 0),
     ("这时候尾巴\n开始一天天变短。\n它不是断掉的，\n也不是被谁咬掉的。\n是身体把它吃回去了。",
      "One tadpole with four legs and only a very short stub of tail left on a cream background, "
      "seen from the side. Nothing else in the picture.", 0),
     ("鳃也在慢慢不见。\n身体里长出了肺。\n从今往后，\n它得浮到水面上，\n用鼻孔吸一口空气。", "", 0),
     ("肚子里也在变。\n蝌蚪吃水草，\n肠子盘得又细又长。\n青蛙要吃虫子，\n肠子就变短变粗。", "", 0),
     ("从吃素改成吃肉，\n嘴也跟着变宽了。\n还多了一条长舌头，\n卷住一只虫子\n只要一眨眼。",
      "One frog on a cream background shooting out its long tongue to catch a small flying "
      "insect. Nothing else in the picture.", 0),
     ("尾巴剩最后一点点，\n它就爬上了荷叶。\n四条腿一蹬，\n扑通一声跳进水里，\n这回是青蛙了。",
      "One frog sitting on a flat lily pad on a cream background, seen from the side, crouched "
      "and about to jump. Nothing else in the picture.", 0),
     ("卵、蝌蚪、\n长腿蝌蚪、青蛙，\n四个模样，\n是同一只小东西。\n它把自己改了一遍。", "", 0),
     ("我蹲在池塘边看，\n找那只尾巴最短的。\n尾巴不是丢了，\n是变成了它自己\n身上的一部分。",
      f"Waist-up view of the little boy at the pond holding a clear jar with one tadpole in it, "
      f"his face large in the frame and turned towards the viewer, {EYES}, thoughtful.", 1),
    ]))

BOOKS.append(dict(
    slug="seaturtle", seed=126000, title="海龟怎么找回出生的那片海滩", subtitle="它记得沙子的味道",
    keyword="海龟", style_label="软色粉",
    style="children's picture book illustration, soft pastel drawing with powdery blended strokes "
          "and visible tooth of the surface, sea blue, warm sand and coral orange",
    character="wearing a light blue t-shirt, sand coloured shorts and bare feet, short black hair",
    palette=P(("#22282e", "#5a7684", "#ecf0f1", "#f8fafa", "#d99a52", "#8a7b63", "#cdd8dc"),
              ("#e4ebee", "#84a0ad", "#0a1016", "#12181f", "#e0a866", "#8a7b63", "#26333b")),
    diagram=[3, 4, 7, 8, 10],
    assets=[
        "One single sea turtle swimming, seen from the side facing left, four long flippers spread "
        "out and a broad shell, its whole body inside the picture. " + BG,
        "One single baby sea turtle seen from above, its four small flippers spread out, its whole "
        "body inside the picture. " + BG,
        "One single white round turtle egg, about the size of a ping pong ball. " + BG,
        "One single bar magnet lying flat on its side, a short straight metal bar. " + BG,
    ],
    pages=[
     ("海边的沙子很烫。\n退潮的地方\n有一道浅浅的印子，\n从水里一直爬上来。\n爸爸说是海龟爬的。",
      f"Waist-up view of the little boy standing on a beach at low tide, his face large in the "
      f"frame and turned towards the viewer, {EYES}, pointing down at a track in the sand.", 1),
     ("夏天的半夜，\n一只母海龟上了岸。\n它在水里很轻快，\n到了沙滩上\n只能一点一点往前挪。",
      "One large sea turtle hauling itself slowly up a beach at night on a cream background, seen "
      "from the side. Nothing else in the picture.", 0),
     ("它用后脚挖坑，\n挖得比自己还深。\n然后把蛋下进去，\n一百多个，\n再把沙子盖回来。", "", 0),
     ("蛋埋在沙子里，\n靠太阳的热气孵。\n沙子凉的时候，\n孵出来多是男孩；\n热的时候多是女孩。", "", 0),
     ("两个月以后，\n蛋壳里传出响动。\n小海龟用嘴上的\n一个小尖，\n把壳顶开一道缝。",
      "One baby sea turtle breaking out of a white egg on a cream background, a crack opening "
      "along the shell. Nothing else in the picture.", 0),
     ("它们等到天黑才出来。\n一窝几十只，\n一起往海的方向爬。\n谁也不回头，\n谁也不停下。",
      "Many baby sea turtles on a cream background seen from above, all crawling in the same "
      "direction. Nothing else in the picture.", 0),
     ("就在爬这几分钟里，\n它们把这片沙滩\n记了下来。\n记的不是样子，\n是地下磁力的方向。", "", 0),
     ("地球本身是块大磁铁。\n每一段海岸，\n磁力的劲儿都不一样。\n小海龟记住的，\n就是这里的那一份。",
      "", 0),
     ("然后它们游走了。\n游进大洋，\n一游就是好多年，\n绕着地球转半圈，\n谁也不知道它在哪。",
      "One sea turtle swimming alone in open water on a cream background, seen from the side. "
      "Nothing else in the picture.", 0),
     ("有的海龟游过的路，\n加起来上万公里，\n比从我们家\n走到南极还要远。\n它一路都没有地图。", "", 0),
     ("二十年后，\n它长成了大海龟，\n又回到这片沙滩。\n不是旁边那一片，\n就是它出生的这一片。",
      "One large sea turtle coming out of the water onto sand on a cream background, seen from "
      "the side. Nothing else in the picture.", 0),
     ("我在沙滩上走，\n沙子是一样的沙子。\n可海龟分得出来。\n它记住的不是路，\n是这一片沙的味道。",
      f"Waist-up view of the little boy sitting on the sand with a handful of it running through "
      f"his fingers, his face large in the frame and turned towards the viewer, {EYES}, quiet.", 1),
    ]))

BOOKS.append(dict(
    slug="owl", seed=127000, title="猫头鹰的眼睛不会转", subtitle="所以它把整个头转过来",
    keyword="猫头鹰", style_label="钢笔淡彩",
    style="children's picture book illustration, fine pen lines with thin transparent watercolour "
          "washes laid loosely over them, warm brown, indigo and pale gold",
    character="wearing a mustard yellow hoodie, dark blue jeans and grey sneakers, short black hair",
    palette=P(("#251f1a", "#6b5f4e", "#f3efe6", "#fcfaf3", "#c08a3e", "#7d6a4f", "#dcd5c4"),
              ("#ece7da", "#9b8d78", "#120e08", "#1c1710", "#d7a458", "#7d6a4f", "#342c1f")),
    diagram=[3, 4, 6, 7, 8],
    assets=[
        "One single owl perched upright on a bare branch, seen from the front, two large round "
        "eyes facing forward, its whole body inside the picture. " + BG,
        "One single short bare tree branch with no leaves on it, lying level. " + BG,
        "One single field mouse standing on all four feet, seen from the side facing left, its "
        "whole body inside the picture. " + BG,
        "One single neck bone, a small block of bone with a hole through the middle, seen from "
        "the side. " + BG,
    ],
    pages=[
     ("动物园的笼子里，\n一只猫头鹰\n一直在看着我。\n我走到哪一边，\n它的头就转到哪边。",
      f"Waist-up view of the little boy standing in front of a large aviary, his face large in "
      f"the frame and turned towards the viewer, {EYES}, wide-eyed; an owl sits on a branch "
      f"behind him.", 1),
     ("它的眼睛又大又圆，\n两只都朝着前面，\n像两盏小灯。\n我看了很久，\n它一次也没转眼珠。",
      "One owl perched on a bare branch on a cream background, seen from the front, its two large "
      "round eyes facing forward. Nothing else in the picture.", 0),
     ("因为它的眼睛\n根本不是球。\n是两根小管子，\n前面粗，后面细，\n一直插进脑袋里。", "", 0),
     ("管子太长了，\n被骨头卡在眼窝里，\n一动也动不了。\n我们能斜着眼看人，\n它一点也不能。", "", 0),
     ("想看左边的东西，\n它只有一个办法，\n把整个头转过去。\n身子站得稳稳的，\n一动都不动。",
      "One owl on a bare branch on a cream background, its body facing the viewer and its head "
      "turned far round to one side. Nothing else in the picture.", 0),
     ("它的脖子里面\n藏着十四节骨头。\n我们的脖子\n只有七节。\n它的零件多一倍。", "", 0),
     ("所以它的头\n能转到身子后面，\n差不多两百七十度。\n一圈里的四分之三，\n再多就不行了。", "", 0),
     ("脖子转这么狠，\n血管不会拧断吗？\n它的血管比骨头洞细，\n旁边还有小口袋，\n存着血备用。", "", 0),
     ("夜里，它的瞳孔\n张得特别特别大。\n一点点星光\n就够它看清楚\n草丛里的动静。",
      "Close view of one owl face at night on a cream background, its two round eyes wide open "
      "with very large dark pupils. Nothing else in the picture.", 0),
     ("它的两只耳朵\n一只高一只低。\n声音先到哪一只，\n它就能听出来\n老鼠在哪个方向。",
      "One owl head seen from the front on a cream background, one ear opening set higher than "
      "the other under the feathers. Nothing else in the picture.", 0),
     ("它飞起来没有声音。\n翅膀边上的羽毛\n长着一排细齿，\n把风梳散了，\n呼呼声就没有了。",
      "One owl flying low with both wings spread wide on a cream background, seen from the side. "
      "Nothing else in the picture.", 0),
     ("我也试着不转眼珠，\n只用脖子看东西。\n转到一半就酸了。\n眼睛转不动的，\n就把整个头转过来。",
      f"Waist-up view of the little boy turning his head as far round as he can while keeping his "
      f"shoulders still, his face large in the frame and turned towards the viewer, {EYES}, "
      f"trying hard.", 1),
    ]))

BOOKS.append(dict(
    slug="whale", seed=128000, title="鲸鱼在水里怎么呼吸", subtitle="头顶上有个喷气孔",
    keyword="鲸", style_label="油画棒",
    style="children's picture book illustration, oil pastel drawing with thick waxy strokes and "
          "blunt smudged edges, deep sea blue, pale grey and bright teal",
    character="wearing a navy blue windbreaker, grey trousers and a red life vest, short black hair",
    palette=P(("#1e2430", "#4d6b86", "#eaeff4", "#f7fafc", "#2f7fa8", "#6d7787", "#ccd8e2"),
              ("#e5ecf3", "#7d9ab3", "#070d16", "#10161f", "#4ea6cc", "#6d7787", "#212c3a")),
    diagram=[3, 4, 6, 8, 10],
    assets=[
        "One single sperm whale swimming, seen from the side facing left, a huge blunt square head "
        "and one flipper, its whole body inside the picture. " + BG,
        "One single pair of lungs, two soft pink bags joined at the top by a short windpipe. " + BG,
        "One single small wooden boat floating level, seen from the side. " + BG,
        "One single giant squid seen from the side, a long body and many long arms trailing "
        "behind it. " + BG,
    ],
    pages=[
     ("我们坐船去看鲸。\n海面上先冒出\n一根白白的柱子，\n又高又直。\n爸爸说，它在那儿。",
      f"Waist-up view of the little boy at the rail of a small boat at sea, his face large in the "
      f"frame and turned towards the viewer, {EYES}, excited, wind in his hair.", 1),
     ("白柱子底下，\n浮起一道黑背，\n又长又滑，\n慢慢从水里升上来，\n又慢慢沉下去。",
      "One long dark whale back rising above the sea surface on a cream background, seen from the "
      "side. Nothing else in the picture.", 0),
     ("鲸长得像鱼，\n可它不是鱼。\n它和我们一样用肺，\n生下来就是小宝宝，\n还要喝妈妈的奶。", "", 0),
     ("鱼长着鳃，\n泡在水里就能呼吸。\n鲸没有鳃。\n它的鼻孔搬了家，\n搬到了头顶上。", "", 0),
     ("所以它换气的时候，\n不用把整个头抬起来。\n只要把头顶\n露出水面一点点，\n就够用了。",
      "One whale at the sea surface on a cream background with only the top of its head showing "
      "above the water. Nothing else in the picture.", 0),
     ("换气分两步。\n先噗的一声，\n把憋久的废气喷出去，\n再张开那个孔，\n吸一大口新的。", "", 0),
     ("喷出来的那根柱子，\n不是海里的水。\n是肚子里的热气\n一碰到冷空气，\n变成的白雾。",
      "Close view of a whale blowhole on a cream background with a tall column of white mist "
      "bursting upward out of it. Nothing else in the picture.", 0),
     ("我憋气能憋多久？\n数到六十就难受了。\n海豚能憋十分钟。\n抹香鲸下去一趟，\n一个多小时才上来。",
      "", 0),
     ("它为什么憋这么久？\n因为它要一直潜到\n很深很黑的地方，\n去抓住在那里的\n大鱿鱼吃。",
      "One sperm whale swimming downward in deep dark water on a cream background, seen from the "
      "side. Nothing else in the picture.", 0),
     ("它睡觉也不能全睡。\n睡死了会忘记上浮。\n所以它一次\n只睡半边脑子，\n另外半边替它守着。",
      "", 0),
     ("小鲸刚生下来，\n第一件事不是吃奶。\n是妈妈用头托着它，\n送到水面上，\n吸进第一口气。",
      "One whale mother nudging a small newborn whale up towards the water surface on a cream "
      "background, seen from the side. Nothing else in the picture.", 0),
     ("我趴在船边等。\n又一根白柱子。\n它一辈子住在海里，\n可每一口气，\n都得到水面上来拿。",
      f"Waist-up view of the little boy leaning on the boat rail watching the sea, his face large "
      f"in the frame and turned towards the viewer, {EYES}, calm and happy.", 1),
    ]))
