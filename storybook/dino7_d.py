# -*- coding: utf-8 -*-
"""第七批恐龙书（4/5）：会不会游泳、最小的、长羽毛的、背上长帆的。"""
from dino7_a import BOOKS, P, BG, EYES

BOOKS.append(dict(
    slug="dinoswim", seed=101000, title="恐龙会游泳吗", subtitle="河底留下的划痕",
    keyword="划痕", style_label="彩色铅笔",
    style="children's picture book illustration, coloured pencil drawing with visible strokes "
          "and layered hatching, river blue, silt grey and warm sand",
    character="wearing a river blue t-shirt, sand beige shorts and white sneakers, short black hair",
    palette=P(("#23292c", "#61808a", "#f1f0e8", "#fbfaf5", "#c46a3e", "#7d7460", "#d8d5c7"),
              ("#e9e6d9", "#93aab2", "#0f1417", "#1a2023", "#d68554", "#7d7460", "#343a3d")),
    diagram=[2, 4, 6, 8, 11],
    assets=[
        "One single large two-legged dinosaur standing on its hind legs, seen from the side "
        "facing left, its whole body inside the picture. " + BG,
        "One single three-toed dinosaur track pressed deep into flat mud, seen from directly "
        "above, the whole print inside the picture. " + BG,
        "One single set of three straight parallel scratch grooves cut into flat mud, seen from "
        "directly above. " + BG,
    ],
    pages=[
     ("河边这块大石头上，\n有一道一道的痕。\n不是脚印，\n是三条一组的划痕。\n爸爸说，恐龙留的。",
      f"Waist-up view of the little boy beside a large flat rock covered in rows of three long "
      f"scratch marks, his face large in the frame and turned towards the viewer, {EYES}, his "
      f"mouth open in surprise.", 1),
     ("脚印是整只脚踩的，\n又深又清楚。\n这些划痕却很浅，\n只有爪尖那么宽，\n像用叉子刮过。", "", 0),
     ("先看看真正的脚印。\n三个脚趾，\n一个脚跟，\n稳稳踩在软泥里，\n边上还堆起一圈泥。",
      "One deep three-toed dinosaur track pressed into soft mud on a cream background with a "
      "low ridge of mud pushed up all around its edge. Nothing else in the picture.", 0),
     ("河底的划痕不一样。\n每一组三条，\n又细又直，\n一组接着一组，\n排出长长的一串。", "", 0),
     ("原来它是浮着的。\n水把身子托起来，\n只有爪尖\n够得着河底，\n一蹬一蹬往前走。",
      "One large two-legged dinosaur floating in a river with most of its body under the water "
      "and only the tips of its toes touching the river bottom, seen from the side. Nothing else "
      "in the picture.", 0),
     ("水有多深呢？\n比它的腿还深，\n一直没到肚子。\n脚踩不实，\n只能用爪尖点着走。", "", 0),
     ("有意思的是，\n这一串划痕\n并不是笔直的。\n它一点点偏向一边，\n是水把它推歪了。",
      "One long line of toe-tip scratch marks on a river bottom running forwards but sloping "
      "towards one side, seen from directly above. Nothing else in the picture.", 0),
     ("在岸上走，\n一步就是一步。\n在水里蹬一下，\n身子能滑出去好远，\n两组划痕隔得很开。", "", 0),
     ("现在的大象也这样。\n过河的时候\n身子沉在水里，\n鼻子伸出水面，\n脚在底下点着走。",
      "One elephant wading across a deep river with only its head and back above the water, seen "
      "from the side. Nothing else in the picture.", 0),
     ("这样的划痕\n一共有好多道，\n方向全都一样。\n那天大概是一群恐龙，\n一起过的河。",
      "Many lines of toe-tip scratch marks on a river bottom all running the same way, seen from "
      "directly above. Nothing else in the picture.", 0),
     ("河底的泥后来干了，\n又埋上一层沙，\n一层一层压成石头。\n那几道爪印\n就这样留到今天。", "", 0),
     ("我把手指\n放进那道浅沟里。\n它不是走过去的，\n是浮着蹬过去的。\n一千万年前的一步。",
      f"Waist-up view of the little boy crouching beside a slab of rock with three long scratch "
      f"grooves in it, one finger resting inside a groove, his face large in the frame and turned "
      f"towards the viewer, {EYES}, thoughtful.", 1),
    ]))

BOOKS.append(dict(
    slug="tiny", seed=102000, title="最小的恐龙有多小", subtitle="比一只鸽子还轻",
    keyword="小", style_label="软色粉",
    style="children's picture book illustration, soft pastel drawing with powdery grain and "
          "gently blended edges, pale moss green, dove grey and apricot",
    character="wearing a pale moss green t-shirt, dove grey shorts and white sneakers, short black hair",
    palette=P(("#2b2a26", "#74786a", "#f3f1ea", "#fcfbf6", "#d08a5c", "#867d68", "#dcd9cb"),
              ("#ebe8dc", "#a1a493", "#12130e", "#1e1f18", "#e09a6f", "#867d68", "#383629")),
    diagram=[2, 3, 5, 7, 10],
    assets=[
        "One single small feathered dinosaur standing on two legs, seen from the side facing "
        "left, its whole body inside the picture. " + BG,
        "One single pigeon standing on two feet, seen from the side facing left, its whole body "
        "inside the picture. " + BG,
        "One single chicken egg standing upright with the narrow end at the top. " + BG,
        "One single walnut in its shell, seen from the side. " + BG,
    ],
    pages=[
     ("这个柜子特别小。\n里面那只恐龙，\n从头到尾\n还没有我的胳膊长。\n爸爸说它早就长大了。",
      f"Waist-up view of the little boy leaning close to a small glass case holding a tiny "
      f"dinosaur skeleton, his face large in the frame and turned towards the viewer, {EYES}, "
      f"curious.", 1),
     ("它到底有多大呢？\n跟一只鸽子差不多。\n两个并排站着，\n鸽子看着还要\n胖出一圈来。", "", 0),
     ("它又有多重呢？\n只有几十克，\n和一只麻雀一样。\n放在秤上，\n还没有一个鸡蛋沉。", "", 0),
     ("它就住在树上。\n爪子细细的，\n正好勾住小树枝。\n风一吹过来，\n它跟着枝子一起晃。",
      "One small feathered dinosaur perched on a thin tree branch with its claws gripping the "
      "branch, seen from the side. Nothing else in the picture.", 0),
     ("它的脑袋很小，\n比一颗核桃大不了多少。\n嘴里那些牙\n细得像针尖，\n一根一根排得很密。", "", 0),
     ("它专吃小虫子。\n嘴往前一啄，\n把爬过去的甲虫\n一口叼起来，\n仰着脖子吞下去。",
      "One small feathered dinosaur bending down to catch a beetle on the ground, seen from the "
      "side. Nothing else in the picture.", 0),
     ("最大的恐龙\n有三十米那么长。\n这一只有多长呢？\n站起来连半米都不到，\n差了六十多倍。", "", 0),
     ("它身上长着羽毛。\n天一冷下来，\n羽毛就蓬起来，\n把自己裹成\n圆圆的一个小绒球。",
      "One small feathered dinosaur asleep with its head tucked under one wing and its feathers "
      "fluffed up, seen from the side. Nothing else in the picture.", 0),
     ("它的骨头是空心的。\n里面有细细的格子，\n又轻又结实。\n捧在手里，\n轻得像一团棉花。",
      "One thin dinosaur leg bone cut open on a cream background showing the hollow space and the "
      "fine struts inside it. Nothing else in the picture.", 0),
     ("它下的蛋\n比鹌鹑蛋还小。\n一窝好几个，\n挨着围成一圈，\n刚好放满一只手心。", "", 0),
     ("它的化石压扁了，\n嵌在一块石板里。\n骨头细得像线，\n连羽毛的印子\n也印在旁边。",
      "One flat slab of stone on a cream background with the fine skeleton of a small dinosaur "
      "pressed into it and faint feather marks all around it. Nothing else in the picture.", 0),
     ("我把两只手\n合成一个小窝。\n最小的恐龙，\n一只手就能捧住。\n它也是恐龙呀。",
      f"Waist-up view of the little boy holding both hands cupped together in front of him as if "
      f"holding something very small, his face large in the frame and turned towards the viewer, "
      f"{EYES}, smiling.", 1),
    ]))

BOOKS.append(dict(
    slug="feather", seed=103000, title="长羽毛的恐龙", subtitle="先是绒毛，后来才会飞",
    keyword="羽毛", style_label="油画棒",
    style="children's picture book illustration, oil pastel drawing with thick waxy strokes and "
          "grainy overlaps, rust red, warm cream and deep forest green",
    character="wearing a rust red t-shirt, forest green shorts and white sneakers, short black hair",
    palette=P(("#2a2422", "#6b7a63", "#f2efe6", "#fbf9f3", "#b5533a", "#8a7457", "#dad5c6"),
              ("#eae5d7", "#9aa88f", "#14110c", "#201c15", "#cd6d4f", "#8a7457", "#37332a")),
    diagram=[2, 4, 5, 7, 10],
    assets=[
        "One single thin straight hair-like strand standing upright. " + BG,
        "One single tuft of several thin straight strands joined together at one root. " + BG,
        "One single flat bird feather with a straight central shaft and fine barbs along both "
        "sides. " + BG,
        "One single small feathered dinosaur standing on two legs, seen from the side facing "
        "left, its whole body inside the picture. " + BG,
    ],
    pages=[
     ("石头上有一只恐龙，\n骨头旁边\n还留着一圈毛。\n爸爸说，\n那是羽毛的印子。",
      f"Waist-up view of the little boy leaning close to a stone slab with a small dinosaur "
      f"skeleton and faint feather marks pressed into it, his face large in the frame and turned "
      f"towards the viewer, {EYES}, curious.", 1),
     ("最早的羽毛\n不是一片，\n是一根。\n细细的一根丝，\n像小狗身上的绒毛。", "", 0),
     ("它满身都是这种丝。\n一根一根立着，\n把身子裹起来。\n风吹不透，\n身上就一直是暖的。",
      "One small dinosaur standing on two legs covered all over in short fine fuzz, seen from the "
      "side. Nothing else in the picture.", 0),
     ("后来这根丝\n从根上分了叉。\n一根变成好几根，\n聚成一小簇，\n蓬蓬的更暖和。", "", 0),
     ("再后来，\n中间长出一根梗，\n两边排开细丝，\n合成平平的一片。\n这才叫一根羽毛。", "", 0),
     ("羽毛还有颜色。\n有的漆黑，\n有的会发亮。\n它把脖子一伸，\n远远的就看得见。",
      "One small feathered dinosaur standing tall with its neck stretched up and its dark glossy "
      "neck feathers raised, seen from the side. Nothing else in the picture.", 0),
     ("它胳膊上的羽毛\n长得最长。\n越靠外越长，\n一排排开，\n合起来像一把扇子。", "", 0),
     ("有一天它跳了下来。\n胳膊往两边一张，\n羽毛兜住风，\n身子慢慢往下飘，\n一点也没摔疼。",
      "One small feathered dinosaur leaping off a tree branch with both feathered arms spread "
      "wide and gliding down through the air, seen from the side. Nothing else in the picture.", 0),
     ("羽毛还有一个用处。\n它蹲在窝上，\n把翅膀盖下去，\n底下的那些蛋\n就一直是暖的。",
      "One feathered dinosaur crouching on a nest of eggs with its feathered arms spread over "
      "them, seen from the side. Nothing else in the picture.", 0),
     ("今天的鸟\n身上也是这个。\n把两根羽毛\n并在一起比一比，\n几乎分不出来。", "", 0),
     ("羽毛那么软，\n本来留不下来。\n可它落进细泥里，\n泥慢慢变成石头，\n印子就留住了。",
      "One flat stone with the clear mark of a single feather pressed into it, seen from "
      "directly above on a cream background. Nothing else in the picture.", 0),
     ("楼下捡到一根羽毛。\n羽毛不是为了飞\n才长出来的，\n是先长出来，\n后来才用来飞。",
      f"Waist-up view of the little boy holding up one small feather between two fingers, his "
      f"face large in the frame and turned towards the viewer, {EYES}, smiling.", 1),
    ]))

BOOKS.append(dict(
    slug="sail", seed=104000, title="背上长帆的恐龙", subtitle="棘龙和它的大帆",
    keyword="帆", style_label="钢笔淡彩",
    style="children's picture book illustration, fine pen line work with light transparent "
          "watercolour washes, sandstone ochre, dusty teal and warm grey",
    character="wearing a sandstone ochre t-shirt, dusty teal shorts and white sneakers, short black hair",
    palette=P(("#24262a", "#5f7b7c", "#f2f0e8", "#fcfaf5", "#c07a3a", "#7f7561", "#d7d4c6"),
              ("#e9e6da", "#90a8a8", "#101315", "#1c1f22", "#d18f58", "#7f7561", "#34383b")),
    diagram=[2, 3, 4, 7, 10],
    assets=[
        "One single spinosaurus standing on two legs, seen from the side facing left, a tall sail "
        "rising along its back and a long narrow snout, its whole body inside the picture. " + BG,
        "One single tall straight bony rod standing upright, thick at the bottom and tapering "
        "towards the top. " + BG,
        "One single wooden door standing upright and closed inside a plain frame. " + BG,
    ],
    pages=[
     ("这只恐龙背上\n竖着一面帆。\n比展厅的门还高，\n从脖子后面\n一直排到屁股。",
      f"Waist-up view of the little boy standing in front of a huge dinosaur skeleton with a tall "
      f"sail of bone rising along its back, his face large in the frame and turned towards the "
      f"viewer, {EYES}, his mouth open in surprise.", 1),
     ("帆最高的地方\n有两米。\n比一扇门还高。\n人站在下面，\n连帆顶都够不着。", "", 0),
     ("帆不是皮长出来的。\n它是骨头撑起来的。\n每一节脊椎骨\n往上长出一根长棒，\n一根挨着一根。", "", 0),
     ("别的恐龙也有这根棒，\n可只有短短一截。\n棘龙的这一根\n长得吓人，\n有我这么高。", "", 0),
     ("从正面看过去，\n这面帆薄薄的，\n只有手掌那么厚。\n它一侧过身，\n帆就几乎不见了。",
      "One spinosaurus seen from directly in front, the tall sail on its back showing only as a "
      "thin upright edge. Nothing else in the picture.", 0),
     ("帆是干什么用的呢？\n也许是拿来显摆的。\n两只碰上了，\n谁的帆更大，\n谁就不用动手打。",
      "Two spinosaurus standing facing each other with their tall back sails raised high, seen "
      "from the side. Nothing else in the picture.", 0),
     ("血一涌上帆，\n帆就慢慢变红。\n远远看过去，\n那个身子\n好像又大了一圈。", "", 0),
     ("它的嘴又长又窄。\n牙是圆锥形的，\n不是刀片。\n这样的牙\n最适合叼鱼。",
      "One spinosaurus lowering its long narrow snout into a river and catching a large fish, "
      "seen from the side. Nothing else in the picture.", 0),
     ("它的骨头很实，\n沉甸甸的。\n沉一点\n就不容易被水托起，\n站在河里更稳当。",
      "One spinosaurus standing in a river with its legs under the water, seen from the side. "
      "Nothing else in the picture.", 0),
     ("它比霸王龙还长。\n从鼻子到尾巴尖，\n足足十五米。\n两辆小汽车\n接起来还不够。", "", 0),
     ("这些长棒\n埋在沙漠的石头里。\n一根一根挖出来，\n再拼到一起，\n才知道是一面帆。",
      "Several long bony rods lying half buried in dry desert rock, seen from the side. Nothing "
      "else in the picture.", 0),
     ("我站在帆底下\n抬头看。\n那面帆不是皮长的，\n是骨头\n一根一根撑起来的。",
      f"Waist-up view of the little boy standing below the tall bony back sail of a huge dinosaur "
      f"skeleton and looking up at it, his face large in the frame and turned towards the viewer, "
      f"{EYES}, amazed.", 1),
    ]))
