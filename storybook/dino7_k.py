# -*- coding: utf-8 -*-
"""第七批补两本：蜘蛛织网、长颈鹿的脖子。"""
from dino7_a import BOOKS, P, BG, EYES

BOOKS.append(dict(
    slug="spider", seed=129000, title="蜘蛛网是怎么织出来的", subtitle="先搭桥，再拉辐条，最后绕圈",
    keyword="蜘蛛", style_label="钢笔淡彩",
    style="children's picture book illustration, fine ink pen lines with light transparent "
          "watercolour washes, dewy blue grey, pale leaf green and warm amber",
    character="wearing a light blue t-shirt, grey shorts and white sneakers, short black hair",
    palette=P(("#23282b", "#6b7c80", "#eef2f1", "#f9fbfa", "#c2793f", "#7d8a6e", "#d5dcd9"),
              ("#e6ecea", "#8c9d9f", "#0e1416", "#161d1f", "#d68f56", "#7d8a6e", "#2e3a38")),
    diagram=[2, 4, 5, 6, 7, 8],
    assets=[
        "One single garden spider seen from above, eight legs spread evenly around its round "
        "body, its whole body inside the picture. " + BG,
        "One single complete orb web seen flat from the front, straight silk lines running out "
        "from the centre and a long spiral of silk winding around them, its whole shape inside "
        "the picture. " + BG,
        "One single small fly with two thin wings, seen from the side facing left. " + BG,
    ],
    pages=[
     ("早上的窗角上，\n挂着一张新网。\n太阳一照丝都亮了，\n一圈一圈地绕着。\n蜘蛛蹲在正中间。",
      f"Waist-up view of the little boy at a window in the morning light, his face large in the "
      f"frame and turned towards the viewer, {EYES}, delighted; behind him a round orb web hangs "
      f"in the corner of the window with a spider at its centre.", 1),
     ("织一张网的第一步\n是放出一根丝。\n风一吹，丝飘过去，\n粘在对面的树枝上。\n一座桥就搭好了。", "", 0),
     ("它顺着这根丝\n爬到对面的枝头，\n又放一根丝回来。\n来回走了好几趟，\n这座桥才够结实。",
      "One single spider walking along a straight silk thread stretched between two twigs on a "
      "cream background, its eight legs gripping the thread. Nothing else in the picture.", 0),
     ("它走到桥中间，\n往下坠一根丝，\n拉住下面的叶子。\n三根丝聚在一起，\n网的中心就定了。", "", 0),
     ("接着开始拉辐条。\n从中心到边上，\n一根，又一根，\n像车轮上的条。\n数一数，三十多根。", "", 0),
     ("辐条拉完了，\n它从中心往外绕，\n绕出一圈松松的丝。\n这圈是临时的，\n只是给自己当脚手架。", "", 0),
     ("然后它掉过头来，\n从最外圈往里绕。\n这一回的丝是粘的，\n一圈比一圈密，\n一直绕到中心。", "", 0),
     ("有意思的地方在这儿：\n辐条的丝不粘，\n绕圈的丝才粘。\n蜘蛛只踩辐条走，\n所以从不粘住自己。", "", 0),
     ("一只小虫撞上来，\n翅膀就粘住了。\n它一挣，网就抖，\n这一抖顺着丝，\n传到蜘蛛的脚上。",
      "One small fly caught in the outer rings of an orb web on a cream background, its thin "
      "wings stuck fast to the silk. Nothing else in the picture.", 0),
     ("网破了怎么办？\n它把旧丝吃回去，\n再吐出新的来。\n一点丝也没浪费，\n又变成了一张网。",
      "One single spider on a torn orb web on a cream background, half the web gone, the spider "
      "taking an old loose thread into its mouth. Nothing else in the picture.", 0),
     ("织好一整张网，\n只要半个钟头。\n先搭桥，再拉辐条，\n最后一圈一圈绕，\n从来不会弄乱。",
      "One complete orb web strung between two branches at dawn on a cream background, tiny dew "
      "drops hanging along its threads. Nothing else in the picture.", 0),
     ("我凑近看那张网，\n丝细得几乎看不见。\n这么长的一根线，\n是它从自己身上\n一点一点抽出来的。",
      f"Waist-up view of the little boy leaning in close to a spider web on a garden fence, his "
      f"face large in the frame and turned towards the viewer, {EYES}, looking hard at the fine "
      f"threads.", 1),
    ]))

BOOKS.append(dict(
    slug="giraffe", seed=130000, title="长颈鹿的脖子", subtitle="和我们一样只有七块骨头",
    keyword="长颈鹿", style_label="彩色铅笔",
    style="children's picture book illustration, coloured pencil drawing with visible pencil "
          "strokes and layered hatching, warm ochre, savanna gold and dusty brown",
    character="wearing a mustard yellow t-shirt, navy blue shorts and white sneakers, short black hair",
    palette=P(("#2e2820", "#7a6b4e", "#f4efe2", "#fcf9f0", "#c07a2c", "#8a7348", "#ded6c2"),
              ("#efe8d6", "#a39270", "#15120a", "#211c10", "#d69a4e", "#8a7348", "#3a3323")),
    diagram=[2, 4, 5, 7, 9],
    assets=[
        "One single giraffe standing on four legs, seen from the side facing left, its long neck "
        "held upright and its head high, its whole body inside the picture. " + BG,
        "One single neck bone of a giraffe lying on its side, a long heavy block of bone with a "
        "knob at each end, its whole shape inside the picture. " + BG,
        "One single tall thorn tree with a wide flat top, its whole shape inside the picture. "
        + BG,
    ],
    pages=[
     ("长颈鹿走过来了。\n我把头仰到最后，\n才看见它的脸。\n它就站在那儿，\n比一层楼还高。",
      f"Waist-up view of the little boy at a zoo tilting his head far back, his face large in the "
      f"frame and turned towards the viewer, {EYES}, amazed; behind him the long neck and small "
      f"head of a giraffe rise high above him.", 1),
     ("它光是一个脖子，\n就有两米多长。\n比爸爸站着还高，\n比我高出两个头。\n身子还在下面呢。", "", 0),
     ("这么长的脖子，\n是用来吃饭的。\n高树顶上的叶子，\n别的动物够不着，\n它一伸头就咬到。",
      "One single giraffe stretching its head up into the top of a tall thorn tree on a cream "
      "background, its long tongue reaching out for the leaves. Nothing else in the picture.", 0),
     ("最奇怪的是骨头。\n你摸摸自己的脖子，\n里面有七块骨头。\n长颈鹿的脖子里，\n也正好是七块。", "", 0),
     ("它不是多长了骨头，\n是每一块都被拉长了。\n它的一块颈椎骨，\n差不多有我的\n一条胳膊那么长。", "", 0),
     ("头举得那么高，\n血怎么送上去呢？\n它的心脏特别有力，\n有二十多斤重，\n墙一样厚的肌肉。",
      "One single animal heart with very thick muscular walls, cut open on a cream background to "
      "show the deep chamber inside. Nothing else in the picture.", 0),
     ("心脏一下一下地跳，\n把血往上顶两米高。\n这股劲比我们的\n要大上两三倍，\n不然血就上不去。", "", 0),
     ("喝水的时候才麻烦。\n它得把两条前腿\n向两边劈得很开，\n脖子一路低下去，\n嘴才够得着水。",
      "One single giraffe drinking at a water hole on a cream background, its two front legs "
      "splayed wide apart and its head lowered right down to the water. Nothing else in the "
      "picture.", 0),
     ("头一下子低到地上，\n血不会冲坏脑子吗？\n脖子里有一道道瓣膜，\n像一扇扇小门，\n把血挡住慢慢放。", "", 0),
     ("等它抬起头来，\n小门再打开，\n血慢慢流回去。\n所以它喝完水，\n站起来也不会晕。",
      "One single giraffe lifting its head up from the water on a cream background, drops of "
      "water falling from its mouth. Nothing else in the picture.", 0),
     ("两只公长颈鹿打架，\n不用嘴也不用腿，\n就甩起长脖子，\n互相撞过去，\n咚的一声，很响。",
      "Two male giraffes standing side by side on a cream background, swinging their long necks "
      "to strike each other. Nothing else in the picture.", 0),
     ("回家的路上我想，\n它的脖子那么长，\n骨头却和我一样多，\n只有七块，\n只是每一块都长。",
      f"Waist-up view of the little boy walking home with one hand resting on the back of his own "
      f"neck, his face large in the frame and turned towards the viewer, {EYES}, thoughtful.", 1),
    ]))
