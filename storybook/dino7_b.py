# -*- coding: utf-8 -*-
"""第七批恐龙书（2/5）：爪子、尾巴、手指、骨头里的空气。"""
from dino7_a import BOOKS, P, BG, EYES

BOOKS.append(dict(
    slug="claws", seed=93000, title="恐龙的爪子", subtitle="抓、挖、还是钩",
    keyword="爪子", style_label="彩色铅笔",
    style="children's picture book illustration, coloured pencil drawing with visible pencil "
          "strokes and layered hatching, brick red, warm grey and pale olive",
    character="wearing a brick red t-shirt, grey shorts and white sneakers, short black hair",
    palette=P(("#262620", "#6b6f7a", "#f3f1e9", "#fcfbf6", "#b5563a", "#8b7d64", "#dcd9cb"),
              ("#e9e6da", "#959aa6", "#131310", "#1e1e18", "#cd7057", "#8b7d64", "#34332a")),
    diagram=[2, 3, 5, 7, 9, 11],
    assets=[
        "One single therizinosaurus standing on two legs, seen from the side facing left, with "
        "three very long straight claws on each hand hanging down past its knees, its whole body "
        "inside the picture. " + BG,
        "One single large claw bone standing alone, wide and thick at its base and narrowing to "
        "one sharp point at the top. " + BG,
        "One single garden trowel seen from the side, a broad flat blade on a short straight "
        "handle. " + BG,
    ],
    pages=[
     ("柜子里放着一只爪子。\n又长又尖，\n比我的手还大。\n爸爸说，\n这只恐龙还不吃肉。",
      f"Waist-up view of the little boy in a museum leaning close to a glass case, his face large "
      f"in the frame and turned towards the viewer, {EYES}, his mouth open in surprise; inside "
      f"the case stands one very long pale claw as big as his hand.", 1),
     ("我们看见的爪子，\n其实只是骨头。\n真的爪子\n外面还套着一层壳，\n比骨头还长一截。", "", 0),
     ("这只恐龙叫镰刀龙。\n它的爪子\n有我的胳膊那么长，\n是所有恐龙里\n最长的一双手。", "", 0),
     ("这么长的爪子\n不是用来打架的。\n它把高处的树枝\n一根根钩下来，\n慢慢吃上面的叶子。",
      "One large long-armed dinosaur standing on two legs on a cream background, hooking a high "
      "branch down towards its mouth with the long claws of one hand. Nothing else in the "
      "picture.", 0),
     ("还有一种爪子\n长在脚上。\n第二个脚趾上\n挂着一只大钩子，\n走路的时候翘着。", "", 0),
     ("翘着是为了不磨坏。\n要用的时候\n才放下来。\n一下子扣进去，\n再也挣不开。",
      "One small feathered two-legged dinosaur standing on a cream background with one foot "
      "lifted, the big hooked claw on its second toe pointing down. Nothing else in the picture.",
      0),
     ("前面那三根手指\n也带着爪。\n三根能合到一起，\n像三把钩子\n一起抓住东西。", "", 0),
     ("另有一种恐龙，\n爪子又短又粗，\n像三把小铲子。\n它不抓东西，\n它专门挖。",
      "One small two-legged dinosaur on a cream background digging into a tall termite mound with "
      "its short thick front claws. Nothing else in the picture.", 0),
     ("挖土的爪子\n又宽又钝，\n像一把铲。\n抓肉的爪子\n又细又尖，像一把钩。", "", 0),
     ("最大的那些恐龙\n反而没什么爪。\n前脚粗得像柱子，\n只在里面那根趾头上\n留了一个。",
      "A close view of the thick round front foot of one huge long-necked dinosaur standing on a "
      "cream background, one single claw on its inner toe. Nothing else in the picture.", 0),
     ("钩的、抓的、挖的，\n还有干脆不用的。\n爪子长成什么形状，\n就等于告诉你\n它是干什么用的。", "", 0),
     ("我把手举到玻璃上，\n跟它比了一下。\n我的指甲\n也是那层壳做的，\n只是短得多。",
      f"Waist-up view of the little boy holding his open hand up against the glass of a museum "
      f"case, his face large in the frame and turned towards the viewer, {EYES}, comparing his "
      f"short fingernails with one huge pale claw behind the glass.", 1),
    ]))

BOOKS.append(dict(
    slug="tails", seed=94000, title="尾巴有什么用", subtitle="平衡、武器、还是撑着",
    keyword="尾巴", style_label="软色粉",
    style="children's picture book illustration, soft pastel drawing with powdery blended strokes "
          "and grainy texture, dusty plum, warm grey and pale sand",
    character="wearing a plum purple t-shirt, sand coloured shorts and white sneakers, short black hair",
    palette=P(("#272430", "#7d7a92", "#f4f1ec", "#fdfbf8", "#8a6096", "#8b7a70", "#ded9d6"),
              ("#ece8e4", "#a49fb4", "#14121a", "#201d27", "#a97fb4", "#8b7a70", "#38333f")),
    diagram=[2, 4, 6, 8, 11],
    assets=[
        "One single diplodocus standing on four legs, seen from the side facing left, with a long "
        "neck and a very long tail stretching far out behind it and thinning to a fine tip, its "
        "whole body inside the picture. " + BG,
        "One single tyrannosaurus standing on two legs, seen from the side facing left, its heavy "
        "tail held straight out behind it, its whole body inside the picture. " + BG,
        "One single long leather whip lying stretched out flat, thick at one end and thin at the "
        "other. " + BG,
    ],
    pages=[
     ("这条尾巴真长。\n从展台这一头\n一直伸到那一头。\n爸爸说，\n它比脖子还长。",
      f"Waist-up view of the little boy standing beside the long tail of a mounted dinosaur "
      f"skeleton in a museum, his face large in the frame and turned towards the viewer, {EYES}, "
      f"looking amazed.", 1),
     ("尾巴不是一根。\n是一节一节的骨头\n接起来的。\n梁龙的尾巴\n有八十多节。", "", 0),
     ("地上留下了脚印，\n尾巴的印子\n却一条也没有。\n所以它走路的时候，\n尾巴是抬着的。",
      "A line of large three-toed dinosaur tracks pressed into wet mud on a cream background, the "
      "ground between the tracks smooth and unmarked. Nothing else in the picture.", 0),
     ("为什么抬得起来？\n因为前后一样沉。\n头和脖子在前边，\n尾巴在后边，\n腿正好在中间。", "", 0),
     ("跑起来要拐弯，\n它就把尾巴\n甩到一边去。\n身子跟着一歪，\n就拐过去了。",
      "One two-legged dinosaur running on a cream background and turning, its long tail swung out "
      "to one side, with motion lines behind it. Nothing else in the picture.", 0),
     ("尾巴里面\n还藏着一大块肉。\n一头连着尾骨，\n一头连着大腿。\n一使劲，腿就往后蹬。", "", 0),
     ("梁龙的尾巴\n越往后越细。\n最后那几十节，\n细得像一根鞭子\n拖在地上。",
      "One very long-necked dinosaur standing in profile on a cream background, its tail "
      "stretching far out behind it and thinning to a fine whip-like tip. Nothing else in the "
      "picture.", 0),
     ("甩起来会不会响？\n有人算过。\n尖上甩得那么快，\n也许真会\n啪的一声。", "", 0),
     ("还有的把尾巴\n往地上一杵，\n后腿一使劲站起来，\n像搭了个三脚架，\n专去够树顶的叶子。",
      "One long-necked dinosaur rearing up on its two back legs on a cream background, the thick "
      "base of its tail pressed down onto the ground behind it like a third leg, reaching up "
      "towards high leaves. Nothing else in the picture.", 0),
     ("有的尾巴\n干脆做成了武器。\n尖上挂着骨锤，\n或者插着长刺。\n谁靠近就甩谁。",
      "One armoured dinosaur on a cream background swinging its tail sideways, a heavy round ball "
      "of bone at the tip. Nothing else in the picture.", 0),
     ("撑着的、甩响的、\n打人的、管平衡的。\n尾巴不是\n多长出来的一截，\n它一直在帮忙。", "", 0),
     ("回家的路上\n我学恐龙走了几步：\n身子往前一低，\n胳膊往后一伸——\n可惜我没有尾巴。",
      f"Waist-up view of the little boy outdoors leaning forward with both arms stretched back "
      f"behind him, his face large in the frame and turned towards the viewer, {EYES}, laughing.",
      1),
    ]))

BOOKS.append(dict(
    slug="fingers", seed=95000, title="恐龙有几根手指", subtitle="有的五根，有的只剩两根",
    keyword="手指", style_label="油画棒",
    style="children's picture book illustration, oil pastel drawing with thick waxy strokes and "
          "visible smudges, deep blue, mustard yellow and warm cream",
    character="wearing a deep blue t-shirt, mustard yellow shorts and white sneakers, short black hair",
    palette=P(("#1f2430", "#5f7188", "#f3f0e4", "#fbf9f0", "#35618f", "#9a7d52", "#dcd7c4"),
              ("#eae6d8", "#8f9fb4", "#0f131a", "#1b202a", "#5a87b6", "#9a7d52", "#32363f")),
    diagram=[2, 3, 5, 7, 9, 11],
    assets=[
        "One single tyrannosaurus rex standing on two legs, seen from the side facing left, one "
        "very short arm held against its chest ending in two short fingers, its whole body inside "
        "the picture. " + BG,
        "One single dinosaur front hand seen from the front, five separate bony fingers spread "
        "wide apart. " + BG,
        "One single iguanodon standing on four legs, seen from the side facing left, one sharp "
        "cone-shaped spike standing up from the thumb of each front hand, its whole body inside "
        "the picture. " + BG,
    ],
    pages=[
     ("我把手贴在玻璃上，\n一根、两根、三根……\n一共五根。\n柜子里那只恐龙的手，\n只有两根。",
      f"Waist-up view of the little boy pressing his open hand flat against the glass of a museum "
      f"case, his face large in the frame and turned towards the viewer, {EYES}, counting; behind "
      f"the glass is the small two-fingered hand of a dinosaur skeleton.", 1),
     ("最早的恐龙\n也是五根手指。\n后来变成了三根，\n再往后\n就只剩下两根了。", "", 0),
     ("先没的是\n最外边那两根。\n它们本来就又细又短，\n真要抓东西，\n一点忙也帮不上。", "", 0),
     ("异特龙还有三根。\n每根上头\n都套着一只钩爪。\n三根一合，\n正好扣住。",
      "One large two-legged dinosaur on a cream background holding out one front hand with three "
      "long clawed fingers closing together. Nothing else in the picture.", 0),
     ("霸王龙只剩两根，\n还都长在\n一条很短的胳膊上。\n跟它的大脑袋比，\n小得不像话。", "", 0),
     ("这么短的手\n够不到自己的嘴，\n也挠不到脸。\n有人说，\n是趴着起身时撑地用的。",
      "One large two-legged dinosaur lying on the ground on a cream background, pushing itself up "
      "with its two small front hands. Nothing else in the picture.", 0),
     ("那第三根呢？\n也没有全没。\n它的肉里面\n还埋着一小截骨头，\n从外面看不出来。", "", 0),
     ("禽龙的手最怪。\n它的大拇指\n变成了一根尖钉，\n硬邦邦地立着，\n收都收不回去。",
      "One plant-eating dinosaur on a cream background holding up one front hand, one sharp "
      "cone-shaped spike standing out where its thumb should be. Nothing else in the picture.", 0),
     ("一只手上\n摆着三样东西：\n一根钉、三个蹄，\n最外边那根\n还能弯过来夹住树枝。", "", 0),
     ("最大的那些恐龙\n把手指并成一圈，\n变成一根柱子。\n它不用手抓东西，\n它只要站得稳。",
      "A close view of the thick round front foot of one huge long-necked dinosaur standing on a "
      "cream background, its toes packed together into a ring like a pillar. Nothing else in the "
      "picture.", 0),
     ("今天的鸟\n翅膀里面\n还藏着三根手指。\n那是恐龙的手\n剩下的最后一点。", "", 0),
     ("我张开五根手指，\n一根一根数过去。\n用得着的留下来，\n用不着的\n慢慢就没有了。",
      f"Waist-up view of the little boy holding up his open hand and counting his fingers with "
      f"the other hand, his face large in the frame and turned towards the viewer, {EYES}, "
      f"thoughtful.", 1),
    ]))

BOOKS.append(dict(
    slug="aircell", seed=96000, title="骨头里为什么有空气", subtitle="又轻又结实的秘密",
    keyword="骨头", style_label="钢笔淡彩",
    style="children's picture book illustration, fine pen and ink lines with light watercolour "
          "washes, teal green, pale grey blue and warm cream",
    character="wearing a teal green t-shirt, light grey shorts and white sneakers, short black hair",
    palette=P(("#232a2a", "#6d8580", "#f5f4ee", "#fdfdf8", "#2e7f74", "#877f6a", "#dedcd0"),
              ("#ebeae0", "#9ab0ab", "#101514", "#1a201f", "#4fa196", "#877f6a", "#333a38")),
    diagram=[2, 4, 6, 8, 10],
    assets=[
        "One single length of metal bicycle frame tube standing upright, cut straight across at "
        "the top so that the thin wall and the empty middle show. " + BG,
        "One single large pale bone standing alone, one deep round opening in its side. " + BG,
        "One single pigeon standing on two feet, seen from the side facing left, its whole body "
        "inside the picture. " + BG,
    ],
    pages=[
     ("老师递给我\n一块恐龙骨头的模子。\n那么大一块，\n我以为很沉，\n一拿——轻得吓一跳。",
      f"Waist-up view of the little boy holding a large pale bone model in both hands, his face "
      f"large in the frame and turned towards the viewer, {EYES}, surprised at how light it is.",
      1),
     ("把它锯开看看。\n里面几乎是空的。\n只有薄薄的骨片，\n横一道竖一道\n撑在当中。", "", 0),
     ("骨头外面\n还开着几个洞。\n不是摔坏的。\n左边一个右边一个，\n长得一模一样。",
      "One large pale bone lying alone on a cream background, two deep round openings in its "
      "side. Nothing else in the picture.", 0),
     ("空的会不会不结实？\n一点也不会。\n自行车的车架\n就是一根空管子，\n照样压不弯。", "", 0),
     ("一样粗的两根，\n实心的沉，\n空心的轻。\n可你要把它们掰弯，\n费的劲差不多。",
      "Two metal rods of the same thickness lying side by side on a cream background, one cut "
      "open at the end showing solid metal and the other cut open showing an empty middle. "
      "Nothing else in the picture.", 0),
     ("梁龙的脖子里\n有十几节这样的骨头，\n一节一节都是空的。\n要不是空的，\n它根本抬不起来。", "", 0),
     ("所以它才能\n把脑袋举那么高。\n脖子那么长一条，\n真要称一称，\n也没有多少分量。",
      "One very long-necked dinosaur on a cream background raising its head high above the tree "
      "tops. Nothing else in the picture.", 0),
     ("这些空腔是谁挖的？\n是气挖的。\n肺后面连着一串气袋，\n气袋一点一点\n钻进骨头里去。", "", 0),
     ("今天的鸟\n身体里就有这些气袋。\n它吸一口气，\n那口气要走两趟\n才从身上出去。",
      "One pigeon standing in profile on a cream background, its chest puffed out. Nothing else "
      "in the picture.", 0),
     ("鳄鱼的骨头\n是实心的。\n鸟的骨头\n是空心的。\n恐龙的，跟鸟一样。", "", 0),
     ("所以我们才敢说，\n这些大家伙\n身体里也有气袋。\n骨头上那些洞，\n就是气袋按出来的。",
      "One huge long-necked dinosaur standing in profile on a cream background, one large pale "
      "bone with round openings in its side lying on the ground in front of it. Nothing else in "
      "the picture.", 0),
     ("我又掂了掂\n手里这块骨头。\n中间掏空了，\n一样结实，\n还轻得多。",
      f"Waist-up view of the little boy weighing the large pale bone model in one hand, his face "
      f"large in the frame and turned towards the viewer, {EYES}, smiling.", 1),
    ]))
