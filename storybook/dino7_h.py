# -*- coding: utf-8 -*-
"""第七批（8/10）：猫的胡须、狗的鼻子、松鼠埋果子、蝙蝠的回声。"""
from dino7_a import BOOKS, P, BG, EYES

BOOKS.append(dict(
    slug="whisker", seed=117000, title="猫的胡须有什么用", subtitle="量一量这个洞钻不钻得过去",
    keyword="猫胡须", style_label="彩色铅笔",
    style="children's picture book illustration, coloured pencil drawing with visible strokes and "
          "layered hatching on textured paper, warm grey, mustard yellow and soft orange",
    character="wearing a mustard yellow t-shirt, grey shorts and white sneakers, short black hair",
    palette=P(("#2b2a26", "#7a7468", "#f3f1ea", "#fbfaf5", "#c17a45", "#8d8272", "#dcd8cc"),
              ("#eae7dd", "#a09889", "#14130e", "#201e16", "#d9925b", "#8d8272", "#383428")),
    diagram=[2, 3, 5, 6, 9, 11],
    assets=[
        "One single short-haired cat sitting upright, seen from the side facing left, its long "
        "straight whiskers spreading out to both sides of its face, its whole body inside the "
        "picture. " + BG,
        "One single long white cat whisker lying straight and alone, thicker at one end and fine "
        "at the other. " + BG,
        "One single cardboard box standing on the floor, seen straight from the front, with a "
        "square hole cut in its side. " + BG,
    ],
    pages=[
     ("邻居家的猫\n蹲在台阶上晒太阳。\n它嘴边那几根白毛\n直直地向两边翘着，\n比我的手指还长。",
      f"A head-and-shoulders portrait of the little boy crouching on a doorstep beside one cat, his face large in "
      f"the frame and turned towards the viewer, {EYES}, smiling a little; the cat sits close to "
      f"him with its long whiskers spread wide. No other person in the picture.", 1),
     ("胡须不只长在嘴边。\n眼睛上面有几根，\n下巴上也有几根，\n两条前腿的后面\n还各藏着一小把。", "", 0),
     ("别的毛只浅浅地\n插在皮肤里面。\n胡须扎得要深得多，\n根上连着神经，\n一动就有信号传进去。", "", 0),
     ("它能感觉到\n很轻很轻的一股风。\n墙就挡在前面，\n风从墙边绕过来，\n它立刻就知道有东西。",
      "One single cat sitting close beside a wall on a cream background, its whiskers spread wide, "
      "thin lines of moving air drifting around the edge of the wall towards its face. Nothing "
      "else in the picture.", 0),
     ("最要紧的是那个宽度。\n胡须向左右张开，\n正好等于它身子上\n最宽的那一处，\n不多也不少。", "", 0),
     ("所以要钻洞以前，\n它先把脸探进去。\n胡须碰不到两边，\n身子就一定过得去；\n碰到了，就退回来。", "", 0),
     ("这个洞看着太窄了。\n胡须两边都蹭到了，\n它立刻停下来，\n掉头就走开了，\n另找一条路进去。",
      "One single cat with its head pushed into a narrow gap between two stacked wooden crates on "
      "a cream background, its whiskers pressed against both sides of the gap, its body pulling "
      "back. Nothing else in the picture.", 0),
     ("夜里屋子里全黑了，\n它照样走得很稳。\n桌子腿在哪儿，\n椅子腿在哪儿，\n胡须一路替它先探。",
      "One single cat walking between table legs and chair legs in a dark unlit room on a cream "
      "background, its whiskers brushing past the wood. Nothing else in the picture.", 0),
     ("所以胡须剪不得。\n要是给它剪短一截，\n它一下就量不准了，\n走路会撞上东西，\n跳也跳不稳当。", "", 0),
     ("胡须还会说话呢。\n它舒服的时候，\n软软地垂向两边；\n一紧张害怕起来，\n立刻全部朝前面张开。",
      "Two cats drawn side by side on a cream background: the left one relaxed with its whiskers "
      "lying softly out to the sides, the right one tense with its whiskers pushed forward in a "
      "wide fan. Nothing else in the picture.", 0),
     ("胡须也会掉下来。\n偶尔掉了一根，\n过些天又长出来，\n长到该有的长短，\n就自己停住不长了。", "", 0),
     ("我慢慢蹲下来，\n跟它脸对着脸。\n它那几根白胡须\n朝我这边抖了一下——\n它这是在量我呢。",
      f"A head-and-shoulders portrait of the little boy crouching face to face with one cat, his face large in the "
      f"frame and turned towards the viewer, {EYES}, wide eyed; the cat's white whiskers almost "
      f"touch his cheek. No other person in the picture.", 1),
    ]))

BOOKS.append(dict(
    slug="dognose", seed=118000, title="狗为什么一路闻过去", subtitle="它用鼻子看世界",
    keyword="狗鼻子", style_label="软色粉",
    style="children's picture book illustration, soft pastel drawing with powdery blended strokes "
          "and grainy texture, dusty blue, warm sand and soft green",
    character="wearing a sky blue t-shirt, sand coloured shorts and white sneakers, short black hair",
    palette=P(("#2a2823", "#6e7a72", "#f1f2ec", "#fafbf6", "#b9834a", "#86806c", "#d8dccd"),
              ("#e9eadc", "#96a094", "#10130d", "#1c1f15", "#cf9a63", "#86806c", "#343827")),
    diagram=[2, 4, 6, 8, 10],
    assets=[
        "One single dog standing on four legs, seen from the side facing left, its head lowered "
        "and its nose touching the grass, its whole body inside the picture. " + BG,
        "One single dog's head seen straight from the front, its black nose in the middle of the "
        "picture, its mouth closed and its ears hanging down. " + BG,
        "One single wooden lamp post standing upright on a small patch of grass, seen straight "
        "from the front. " + BG,
    ],
    pages=[
     ("我牵着狗去散步。\n它一路都低着头，\n这儿停下闻一闻，\n那儿又停下闻闻，\n走得比我还要慢。",
      f"A head-and-shoulders portrait of the little boy standing on a grass path holding a dog's lead, his face "
      f"large in the frame and turned towards the viewer, {EYES}, patient; beside him one dog has "
      f"its nose down in the grass. No other person in the picture.", 1),
     ("我们鼻子里\n有五百万个闻味的细胞。\n狗有整整两亿多个。\n一个一个数过去，\n差了好几十倍。", "", 0),
     ("它的鼻子里面\n并不是空空的，\n是一层层薄薄的皱褶。\n要是摊平铺开来，\n比一张手帕还大。",
      "A cut-away side view of a dog's head on a cream background, showing many thin folded layers "
      "of tissue filling the whole space inside its nose. Nothing else in the picture.", 0),
     ("它还有一个本事：\n左边鼻孔和右边鼻孔，\n是分开来闻的。\n两边闻到的浓淡\n常常不一样。", "", 0),
     ("哪边先闻到，\n哪边的味道更浓，\n它就往哪边转过去。\n气味是从哪里来的，\n它一下就找准了。",
      "One single dog standing in grass on a cream background with its head turned to one side and "
      "its nose lifted, thin drifting lines of scent coming towards it from the left. Nothing else "
      "in the picture.", 0),
     ("吸气从鼻孔前面进，\n呼气从两边缝里出。\n这样吹出去的风\n不会把眼前的味道\n吹散掉一点。", "", 0),
     ("它低头闻的地方，\n刚才有别的狗来过。\n是大狗还是小狗，\n心情好还是不好，\n味里全写着呢。",
      "One single dog with its nose pressed to the ground beside a wooden lamp post on a cream "
      "background, sniffing hard. Nothing else in the picture.", 0),
     ("一根电线杆上面，\n常留着好几只狗\n写下来的消息。\n一只压着一只，\n像一面贴满纸条的墙。", "", 0),
     ("它的鼻头总是湿的。\n湿了才粘得住\n飘在空气里的味道。\n刚睡醒的时候\n才会干上一会儿。",
      "Close view of one single dog's nose on a cream background, the black nose tip shiny and wet. "
      "Nothing else in the picture.", 0),
     ("昨天有只野猫\n从这儿走过去。\n味道已经淡了，\n可它还闻得出来，\n还知道猫是往哪边走的。", "", 0),
     ("有的狗在机场上班，\n有的跟着人进山里，\n去找走丢的孩子。\n我们看不见的东西，\n它能闻得见。",
      "One single dog wearing a working harness walking through tall grass on a cream background, "
      "its nose down and its tail straight out behind it. Nothing else in the picture.", 0),
     ("我也蹲下去闻了闻，\n草就是草的味儿。\n它抬起头来看看我，\n好像在说一句：\n你什么都没读到吧。",
      f"A head-and-shoulders portrait of the little boy crouching down with his own nose close to the grass, his "
      f"face large in the frame and turned towards the viewer, {EYES}, puzzled; one dog sits "
      f"beside him watching. No other person in the picture.", 1),
    ]))

BOOKS.append(dict(
    slug="squirrel", seed=119000, title="松鼠记得埋在哪儿吗", subtitle="忘掉的那些长成了树",
    keyword="松鼠", style_label="油画棒",
    style="children's picture book illustration, oil pastel drawing with thick waxy strokes and "
          "softly blended edges, burnt orange, moss green and warm cream",
    character="wearing a rust orange hoodie, dark green trousers and white sneakers, short black hair",
    palette=P(("#2d2720", "#7d7050", "#f4f0e4", "#fcfaf2", "#c26a34", "#8b7550", "#ded7c0"),
              ("#ece6d4", "#a1926e", "#17120a", "#221c11", "#d68449", "#8b7550", "#3a3220")),
    diagram=[2, 4, 6, 9, 11],
    assets=[
        "One single squirrel sitting upright on its back legs, seen from the side facing left, "
        "holding one nut in its front paws, its bushy tail raised behind it, its whole body inside "
        "the picture. " + BG,
        "One single acorn with its cap still on, standing upright. " + BG,
        "One single young oak tree with a thin straight trunk and a small crown of leaves, "
        "standing alone. " + BG,
    ],
    pages=[
     ("公园的草地上面，\n一只松鼠在刨土。\n刨两下，停一停，\n左看一看，右看一看，\n再低下头接着刨。",
      f"A head-and-shoulders portrait of the little boy kneeling on park grass, his face large in the frame and "
      f"turned towards the viewer, {EYES}, watching quietly; one squirrel digs in the earth just "
      f"in front of him. No other person in the picture.", 1),
     ("一整个秋天下来，\n它能埋下几千个果子。\n不是几十个，\n是整整好几千个，\n一个一个埋下去。", "", 0),
     ("它从不把果子\n都堆在同一个窝里。\n这儿埋下一个，\n那儿埋下一个，\n分开藏在好多个地方。",
      "One single squirrel on grass on a cream background pressing one nut into a small hole, with "
      "several other patches of freshly turned earth scattered far apart around it. Nothing else "
      "in the picture.", 0),
     ("往土里埋以前，\n它先把那个果子\n在自己脸上蹭一蹭。\n蹭上一点自己的味，\n以后就好认了。", "", 0),
     ("它还记得地方。\n这棵树，那块大石头，\n谁跟谁隔着多远，\n它都记在心里头，\n像记住一张地图。",
      "One single squirrel sitting upright on the ground on a cream background between a large "
      "stone and a thick tree root, looking around. Nothing else in the picture.", 0),
     ("到了冬天雪下来，\n它一个一个挖回来。\n要是埋下十个，\n大概能找回七八个。\n剩下的那些，忘了。", "", 0),
     ("雪盖住了地面，\n它照样能找得到。\n鼻子贴着雪闻一闻，\n闻准了地方以后，\n两只前爪一起刨。",
      "One single squirrel digging down into deep snow with both front paws on a cream background, "
      "its nose pushed into the hole. Nothing else in the picture.", 0),
     ("有时候它还会装样子。\n明明没放东西，\n也假装埋下一个，\n再把土盖盖好，\n骗那些偷看的鸟。",
      "One single squirrel patting loose earth flat over an empty hole with its front paws on a "
      "cream background, one bird watching from a branch above. Nothing else in the picture.", 0),
     ("被忘掉的那几个\n就一直留在土里头。\n外面下着大雪，\n里面一动不动，\n慢慢地等着春天来。", "", 0),
     ("春天一暖起来，\n果子裂开一道缝，\n伸出一根细细的芽，\n顶开上面的泥土，\n往有光的地方长。",
      "One single acorn lying in dark earth on a cream background, split open along one side with "
      "a thin pale shoot rising out of it towards the light. Nothing else in the picture.", 0),
     ("所以一片林子里，\n总有好些棵树\n是松鼠种下来的。\n它当初只是想\n留着自己冬天慢慢吃。", "", 0),
     ("我看着那只小松鼠\n又埋下了一个。\n它忘掉的那几个，\n后来都变成了树。\n忘一点，也挺好的。",
      f"A head-and-shoulders portrait of the little boy sitting on the grass holding one acorn in his open hand, "
      f"only his head and shoulders inside the picture and everything below his chest outside the frame, his face turned straight towards the viewer, {EYES}, thoughtful; one squirrel "
      f"sits a little way off on the grass. No other person in the picture.", 1),
    ]))

BOOKS.append(dict(
    slug="bat", seed=120000, title="蝙蝠在黑里怎么飞", subtitle="喊一声，听回声",
    keyword="蝙蝠", style_label="钢笔淡彩",
    style="children's picture book illustration, fine pen lines with light transparent watercolour "
          "washes and visible grain, dusk blue, soft violet and warm cream",
    character="wearing a navy blue jacket, grey trousers and white sneakers, short black hair",
    palette=P(("#262633", "#6b6f85", "#f0f0ee", "#fafaf7", "#a86a7a", "#7c7a70", "#d6d7d4"),
              ("#e7e7e2", "#949ab0", "#101018", "#1b1b22", "#c4838f", "#7c7a70", "#33333c")),
    diagram=[2, 4, 5, 6, 8, 11],
    assets=[
        "One single bat in flight seen from below, its wings stretched out flat to both sides and "
        "its thin finger bones showing through the thin skin, its whole body inside the picture. "
        + BG,
        "One single wooden door standing upright and closed, seen straight from the front. " + BG,
        "One single small moth with its wings open, seen from above. " + BG,
        "One single red rubber ball resting on the ground. " + BG,
    ],
    pages=[
     ("天快要黑下来了，\n院子上空有个东西\n一晃就过去了。\n不像鸟那样滑，\n一忽儿高一忽儿低。",
      f"A head-and-shoulders portrait of the little boy standing in a yard at dusk looking up, his face large in "
      f"the frame and turned towards the viewer, {EYES}, surprised; one small bat flies across the "
      f"sky behind him. No other person in the picture.", 1),
     ("爸爸说那是只蝙蝠。\n它其实不是鸟。\n它那对大翅膀，\n是手指撑开的一层皮，\n薄得能透过光。", "", 0),
     ("天完全黑下来了，\n什么都看不见了。\n它那双小眼睛\n也帮不上多少忙。\n可它照样飞得很稳。",
      "One single bat flying with its wings spread wide and its small eyes almost shut, seen from "
      "the front on a cream background. Nothing else in the picture.", 0),
     ("秘密就在它的嘴里。\n它一边往前飞，\n一边不停地叫。\n那叫声高得吓人，\n我们的耳朵听不见。", "", 0),
     ("喊出去的那一声，\n一直往前头跑，\n撞到东西就弹回来，\n像皮球扔到墙上，\n又弹回自己手里。", "", 0),
     ("回声弹回来得快，\n东西就在近处。\n回声弹回来得慢，\n东西就还远着呢。\n它听一听就明白了。", "", 0),
     ("屋里拉一根细细的线，\n再把灯全关上，\n它也能贴着飞过去，\n一根线都不碰到。\n它是听出来的。",
      "One single bat flying past a thin string stretched across a dark room on a cream background, "
      "tilting its body to slip by without touching it. Nothing else in the picture.", 0),
     ("发现一只小虫的时候，\n它叫得越来越密。\n离得远就慢慢叫，\n眼看快抓住了，\n就叫成一长串。", "", 0),
     ("就这么一个晚上，\n一只小小的蝙蝠\n能吃掉上千只蚊子。\n夏天坐在院子里，\n能少挨好几个包。",
      "One single bat catching one small moth in mid air on a cream background, its mouth open and "
      "its wings swept forward. Nothing else in the picture.", 0),
     ("天一亮起来，\n它就钻进屋檐底下，\n倒挂着整个身子，\n翅膀裹得严严的，\n一睡就是一整个白天。",
      "One single bat hanging upside down from the underside of a roof eave on a cream background, "
      "its wings folded around its body, asleep. Nothing else in the picture.", 0),
     ("这个本事有名字，\n就叫回声定位。\n海里的船也这么干：\n往水底喊上一声，\n听回声算出有多深。", "", 0),
     ("我站在院子里，\n学着它喊了一声。\n回声真的就回来了。\n蝙蝠就是这样——\n喊一声，看见一片黑。",
      f"A head-and-shoulders portrait of the little boy in the yard at night with his hands cupped around his mouth "
      f"calling out, only his head and shoulders inside the picture and everything below his chest outside the frame, his face turned straight towards the viewer, {EYES}, listening; "
      f"one bat flies high above him. No other person in the picture.", 1),
    ]))
