# -*- coding: utf-8 -*-
"""第七批（6/10）：谁第一个发现恐龙、名字怎么来的、云、雾。"""
from dino7_a import BOOKS, P, BG, EYES

BOOKS.append(dict(
    slug="firstfind", seed=109000, title="谁第一个发现恐龙", subtitle="一颗牙引出来的事",
    keyword="禽龙", style_label="彩色铅笔",
    style="children's picture book illustration, coloured pencil drawing with visible hatching "
          "strokes and grainy layered colour, warm ochre, moss green and brick red",
    character="wearing a mustard yellow t-shirt, dark blue shorts and white sneakers, "
              "short black hair",
    palette=P(("#2b2820", "#6e6b55", "#f3f0e5", "#fcfaf3", "#9a5b3e", "#857a5f", "#dcd8c6"),
              ("#ece9db", "#9a9782", "#151209", "#221f13", "#bd7a56", "#857a5f", "#37341f")),
    diagram=[4, 6, 7, 9, 10, 11],
    assets=[
        "One single fossil tooth lying flat, seen from the side, wide and flat like a leaf with a "
        "row of small points along one edge, its whole shape inside the picture. " + BG,
        "One single green iguana lizard standing on four legs, seen from the side facing left, "
        "its whole body inside the picture. " + BG,
        "One single iguanodon standing on four legs, seen from the side facing left, a pointed "
        "spike on each thumb, its whole body inside the picture. " + BG,
        "One single grey lump of broken road stone lying on the ground, seen from the side, its "
        "whole shape inside the picture. " + BG,
    ],
    pages=[
     ("博物馆的柜子里，\n躺着一颗小黄牙。\n只有拇指那么大。\n爸爸说，恐龙这件事，\n就是从它开始的。",
      f"A head-and-shoulders portrait of the little boy in a museum leaning close to a glass case, his face large "
      f"in the frame and turned towards the viewer, {EYES}, curious; inside the case rests one "
      f"small fossil tooth.", 1),
     ("两百年前的英国，\n乡下有条小路。\n路边堆着碎石头，\n是留着修路用的。\n故事就从这儿起头。",
      "A narrow country road in the English countryside with hedges on both sides and a heap of "
      "broken grey stones at the roadside. Nothing else in the picture.", 0),
     ("有位医生叫曼特尔。\n他出诊的时候，\n妻子在路边等着，\n随手翻了翻碎石，\n翻出一块亮的。",
      "Close view of a heap of broken grey road stones on the ground, one of them split open with "
      "a pale shape showing inside. Nothing else in the picture.", 0),
     ("亮的是一颗牙。\n扁扁的像片叶子，\n边上一排小锯齿，\n一看就知道\n它的主人吃草。", "", 0),
     ("他拿去问人。\n有人说是鱼牙，\n有人说是犀牛的，\n还有人劝他：\n别折腾了，回家吧。",
      "One fossil tooth lying on a dark wooden table beside an old brass magnifying glass. "
      "Nothing else in the picture.", 0),
     ("过了三年，\n他见到一只鬣蜥，\n嘴里的牙\n跟那颗一模一样，\n只是小得多得多。", "", 0),
     ("他量了一量：\n那一颗牙，\n是鬣蜥牙的二十倍。\n二十倍的牙，\n得配多大一只？", "", 0),
     ("他给它起名叫禽龙，\n意思是「鬣蜥的牙」。\n一颗牙换来一个名字，\n两百年过去，\n这名字还在用。",
      "One iguanodon standing on four legs among low ferns, seen from the side. Nothing else in "
      "the picture.", 0),
     ("可谁也没见过它。\n曼特尔只能猜。\n有根尖尖的骨头，\n他不知道该搁哪儿，\n就插在了鼻子上。",
      "", 0),
     ("后来挖出整副骨架，\n大家才看清：\n那根尖骨头\n不长在鼻子上，\n长在大拇指上。", "", 0),
     ("再后来，欧文\n把这些大家伙归成一类，\n造了一个新词，\n叫 dinosaur，\n意思是可怕的大蜥蜴。",
      "", 0),
     ("我把大拇指竖起来。\n它的刺就长在这儿。\n一颗小小的牙，\n居然牵出了\n整整一个世界。",
      f"A head-and-shoulders portrait of the little boy holding one hand up with the thumb raised and looking at "
      f"it, only his head and shoulders inside the picture and everything below his chest outside the frame, his face turned straight towards the viewer, {EYES}, delighted.", 1),
    ]))

BOOKS.append(dict(
    slug="dinonames", seed=110000, title="恐龙的名字是怎么来的", subtitle="名字里藏着它长什么样",
    keyword="恐龙名字", style_label="钢笔淡彩",
    style="children's picture book illustration, fine pen lines with light watercolour washes "
          "laid over them, ink blue, warm sand and terracotta",
    character="wearing a navy blue striped t-shirt, grey shorts and white sneakers, "
              "short black hair",
    palette=P(("#22262e", "#5f6b78", "#eef1f2", "#fafcfb", "#b0653f", "#7d7566", "#d3d9dc"),
              ("#e6ebee", "#8e9aa6", "#0e1116", "#191d23", "#c88359", "#7d7566", "#2e343c")),
    diagram=[2, 4, 6, 8, 10, 11],
    assets=[
        "One single triceratops standing on four legs, seen from the side facing left, three "
        "horns on its face and a broad bony frill behind its head, its whole body inside the "
        "picture. " + BG,
        "One single tyrannosaurus rex standing on two legs, seen from the side facing left, a "
        "very large head and two short arms, its whole body inside the picture. " + BG,
        "One single velociraptor standing on two legs, seen from the side facing left, a slim "
        "feathered body and a long stiff tail, its whole body inside the picture. " + BG,
        "One single brachiosaurus standing on four legs, seen from the side facing left, its "
        "front legs longer than its back legs and its long neck held high, its whole body inside "
        "the picture. " + BG,
    ],
    pages=[
     ("恐龙的名字\n一个比一个长。\n三角龙、霸王龙、\n迅猛龙……\n为什么都这么叫？",
      f"A head-and-shoulders portrait of the little boy standing in front of a large dinosaur skull in a museum, "
      f"only his head and shoulders inside the picture and everything below his chest outside the frame, his face turned straight towards the viewer, {EYES}, puzzled.", 1),
     ("名字大多是拼出来的。\n前面一半说它的样子，\n后面那个「龙」，\n原本的意思\n是蜥蜴。", "", 0),
     ("这只脸上有三只角，\n两只在眼睛上方，\n一只在鼻子上，\n后面还撑着\n一圈大骨头领子。",
      "One triceratops standing in profile on a cream background, three horns on its face and a "
      "broad bony frill behind its head, its head turned so the face is clearly seen. Nothing "
      "else in the picture.", 0),
     ("它的名字拆开来：\n三，角，脸。\n连起来就是\n「长着三只角的脸」。\n名字就是一句描述。", "", 0),
     ("这只头特别大，\n牙像香蕉那么粗，\n前面两只小手\n短得够不着嘴。\n谁见了都得让路。",
      "One tyrannosaurus standing in profile on a cream background, its huge head open in a roar, "
      "its two short arms held close to its chest. Nothing else in the picture.", 0),
     ("它的名字拆开来：\n暴君，蜥蜴，王。\n合起来是\n「暴君蜥蜴之王」。\n听着就不好惹。", "", 0),
     ("这只个头不大，\n身上长着羽毛，\n腿细，跑得飞快，\n专挑别人不留神的时候\n扑上去。",
      "One feathered velociraptor running fast in profile on a cream background, its long stiff "
      "tail held straight out behind it. Nothing else in the picture.", 0),
     ("它的名字拆开来：\n快，加上贼。\n「跑得快的贼」——\n给它起名的人\n一定见过它的本事。", "", 0),
     ("这只守着一窝蛋。\n蛋孵出来以后，\n它还接着喂。\n所以人给它起名叫\n「好妈妈蜥蜴」。",
      "One maiasaura crouching over a round nest of eggs on a cream background, lowering its head "
      "towards them. Nothing else in the picture.", 0),
     ("还有些名字里\n藏着地名。\n禄丰龙在云南禄丰，\n青岛龙在青岛——\n在哪儿挖出来的。", "", 0),
     ("也有些名字里\n藏着人名，\n记着是谁\n第一个把它\n从石头里挖出来。", "", 0),
     ("原来每个名字\n都是一句短短的话。\n它长什么样，\n有什么本事，\n名字里全写着呢。",
      f"A head-and-shoulders portrait of the little boy standing beside a triceratops skull in a museum, his face "
      f"large in the frame and turned towards the viewer, {EYES}, smiling as if he has just "
      f"understood something.", 1),
    ]))

BOOKS.append(dict(
    slug="cloud", seed=111000, title="云是怎么来的", subtitle="水变成小水珠挂在天上",
    keyword="云", style_label="软色粉",
    style="children's picture book illustration, soft pastel with powdery blended strokes and "
          "visible chalk texture, sky blue, cloud white and warm apricot",
    character="wearing a pale blue hoodie, white shorts and white sneakers, short black hair",
    palette=P(("#26303a", "#6b7f92", "#eef4f8", "#fbfdfe", "#d98b5f", "#7f8b96", "#d2dee6"),
              ("#e8eff5", "#94a6b6", "#0d1319", "#171f26", "#e0a077", "#7f8b96", "#2c3a45")),
    diagram=[2, 4, 6, 7, 8, 11],
    assets=[
        "One single tall white cumulus cloud floating alone, its whole shape inside the picture. "
        + BG,
        "One single small round drop of water, seen from the side, its whole shape inside the "
        "picture. " + BG,
        "One single tiny grey grain of dust, its whole shape inside the picture. " + BG,
        "One single yellow sun with straight rays reaching out from it, its whole shape inside "
        "the picture. " + BG,
    ],
    pages=[
     ("天上飘着一团白的，\n软软的，像棉花糖。\n我问爸爸：\n能拿下来\n咬一口吗？",
      f"A head-and-shoulders portrait of the little boy lying back on grass and looking up, his face large in the "
      f"frame and turned towards the viewer, {EYES}, wondering, with big white clouds in a blue "
      f"sky filling the whole picture behind him right out to all four edges.", 1),
     ("爸爸说那不能吃。\n天上那团白，\n既不是棉花，\n也不是烟，\n它是水变出来的。", "", 0),
     ("太阳晒着地上的水，\n水洼、河，还有海。\n水被晒得暖了，\n就悄悄变成气，\n偷偷往上跑。",
      "Warm sunlight falling on a wide shallow puddle on bare ground, faint wisps of vapour "
      "rising from it, and a bright blue sky filling the whole picture right out to all four "
      "edges. Nothing else in the picture.", 0),
     ("变成气的水\n我们看不见。\n它就在身边，\n在你吸进去的\n每一口空气里。", "", 0),
     ("越往上越冷。\n升到高处的水汽\n冷得受不了，\n只好又变回水，\n变成小水珠。",
      "A tall column of open sky filling the whole picture right out to all four edges, warm and "
      "hazy near the bottom and cold pale blue near the top. Nothing else in the picture.", 0),
     ("变的时候\n它得先找个芯。\n空气里飘着灰尘，\n一粒灰尘\n就够一颗水珠抱住。", "", 0),
     ("一颗水珠有多小？\n比一根头发\n还要细得多。\n几百颗排起来，\n才有头发那么宽。", "", 0),
     ("一颗看不见，\n十颗也看不见。\n可等到几千亿颗\n挤在一块儿，\n我们就看见白了。", "", 0),
     ("那就是云。\n它不是一整块，\n是数不清的小水珠，\n各自飘着，\n凑成了一团。",
      "Great white cumulus clouds piled high in a blue sky that fills the whole picture right out "
      "to all four edges, seen from below. Nothing else in the picture.", 0),
     ("所以云摸不着。\n飞机从里面穿过去，\n窗外只是一片灰白，\n再没有别的——\n就像穿过一阵湿气。",
      "A great white cloud filling the whole picture right out to all four edges, one small "
      "aeroplane flying into it and everything around it pale grey white. Nothing else in the "
      "picture.", 0),
     ("水珠碰上水珠，\n越碰越大，\n大到托不住了，\n就往下掉。\n掉下来的，就是雨。", "", 0),
     ("我又抬头看了看。\n那不是棉花糖，\n那是好多好多\n小得看不见的水珠，\n挤在一起在天上走。",
      f"A head-and-shoulders portrait of the little boy standing in a field at dusk and pointing up, his face "
      f"large in the frame and turned towards the viewer, {EYES}, happy, with the evening sky "
      f"filling the whole picture behind him right out to all four edges.", 1),
    ]))

BOOKS.append(dict(
    slug="fog", seed=112000, title="雾就是落在地上的云", subtitle="走进云里是什么感觉",
    keyword="雾", style_label="油画棒",
    style="children's picture book illustration, oil pastel with thick waxy strokes and visible "
          "smudging, misty grey green, dull gold and deep pine",
    character="wearing a red raincoat over a grey t-shirt, dark green trousers and yellow rain "
              "boots, short black hair",
    palette=P(("#292d2b", "#6d7a74", "#f0f2ef", "#fafbf8", "#c07a52", "#7b7a68", "#d6dbd5"),
              ("#e9ece8", "#95a19a", "#101413", "#1c211e", "#d18f66", "#7b7a68", "#333936")),
    diagram=[2, 4, 6, 8, 10],
    assets=[
        "One single bare tree standing alone, seen from the side, its whole shape inside the "
        "picture. " + BG,
        "One single small round drop of water, seen from the side, its whole shape inside the "
        "picture. " + BG,
        "One single low green hill with a few dark pine trees on top, its whole shape inside the "
        "picture. " + BG,
        "One single yellow sun with straight rays reaching out from it, its whole shape inside "
        "the picture. " + BG,
    ],
    pages=[
     ("早上我推开门，\n外面白茫茫的。\n对面的楼不见了，\n路口那棵树\n也只剩一个影子。",
      f"A head-and-shoulders portrait of the little boy standing in an open doorway early in the morning, his "
      f"face large in the frame and turned towards the viewer, {EYES}, wondering, with thick "
      f"white fog filling the whole picture behind him right out to all four edges.", 1),
     ("爸爸说，这是雾。\n雾其实就是云，\n只不过这一朵\n没有飘在天上，\n而是贴着地面。", "", 0),
     ("夜里地面凉得快。\n太阳一落，\n热就一点点跑掉，\n贴着地的那层空气\n跟着冷下来。",
      "A cold dark meadow at night with thin mist just beginning to settle over it, the misty air "
      "filling the whole picture right out to all four edges. Nothing else in the picture.", 0),
     ("空气一冷，\n里头的水汽\n就待不住了，\n变成小水珠，\n悬在半空中。", "", 0),
     ("我走进雾里。\n脸上凉凉的，\n还有一点点湿。\n那是小水珠\n落在了我脸上。",
      "Thick white fog filling the whole picture right out to all four edges, with a narrow path "
      "just visible fading away into it. Nothing else in the picture.", 0),
     ("低头一看，\n袖子上、头发上，\n全挂着细细的水珠，\n一颗一颗，\n像撒了一层糖霜。", "", 0),
     ("雾里看不远。\n前面才五步，\n就只剩灰影子。\n是水珠把光\n弹得到处都是。",
      "Thick white fog filling the whole picture right out to all four edges, with one dark tree "
      "showing only as a soft grey shape inside it. Nothing else in the picture.", 0),
     ("所以雾天走路\n要慢一点。\n车看不见人，\n人也看不见车，\n手要牵好大人的手。", "", 0),
     ("山上常常有雾。\n我们在山里走，\n觉得是雾；\n山下的人抬头看，\n说那是一朵云。",
      "A green hill with a band of white cloud lying across its middle, the cloudy sky filling "
      "the whole picture right out to all four edges. Nothing else in the picture.", 0),
     ("太阳一出来，\n地面暖起来，\n小水珠一颗一颗\n又变回看不见的气，\n雾就散了。", "", 0),
     ("雾散完了，\n草叶上还挂着水珠，\n一碰就滚下来。\n那是雾留下来的，\n一点点痕迹。",
      "Low morning sunlight over wet grass, the last thin fog clearing away and still filling the "
      "whole picture right out to all four edges. Nothing else in the picture.", 0),
     ("原来今天早上，\n我走进过一朵云。\n云不在天上的时候，\n就在我脸上，\n凉凉的，湿湿的。",
      f"A head-and-shoulders portrait of the little boy walking in the fog with his arms stretched out, his face "
      f"large in the frame and turned towards the viewer, {EYES}, laughing, with the fog filling "
      f"the whole picture behind him right out to all four edges.", 1),
    ]))
