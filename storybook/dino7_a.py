# -*- coding: utf-8 -*-
"""第七批恐龙书（1/5）：剑龙的板、甲龙的锤、爪子、尾巴。

这批从一开始就按前六批的教训写：
· 画风只用留得住笔触的（水彩、彩铅、色粉、油画棒、水粉），不用平涂线条那类
  把脸压成色块的 —— 人物不像他的根子在那儿（手册 4.2h）；
· 他出镜的 p1/p12 直接写成半身、正脸、眼白加虹膜高光；
· 对比页按「模型画单体素材 + 程序拼合」设计，assets 里就是素材的提示词，
  不再画几何剪影；
· 素材提示词不写 curved、不强调花纹、背景写成铺满四边的单一奶油色。
"""
import os

K = "ink soft ground paper accent bark line".split()
BG = ("The background is one flat cream colour of a single even tone that fills the whole "
      "picture right out to all four edges. The object floats on this flat colour: it casts "
      "no shadow and rests on no ground, and there is no darker patch, wash, puddle, base, "
      "line or platform of any kind underneath it.")
EYES = "both eyes clearly drawn with white, a dark round iris and a small bright highlight"


def P(light, dark):
    r = dict(zip(K, light))
    r.update(dict(zip([x + "_d" for x in K], dark)))
    return r


BOOKS = []

BOOKS.append(dict(
    slug="stego", seed=91000, title="剑龙背上的板", subtitle="散热，还是吓唬人",
    keyword="剑龙", style_label="水彩铅笔",
    style="children's picture book illustration, soft watercolour washes with fine pencil "
          "outlines and visible paper grain, sage green, warm ochre and dusty rose",
    character="wearing a sage green t-shirt, brown shorts and white sneakers, short black hair",
    palette=P(("#2c2b23", "#6f7360", "#f2f1e7", "#fbfbf5", "#b06a4e", "#8a7f66", "#dbd9c9"),
              ("#eae8da", "#9ba08a", "#14140c", "#201f15", "#c8836a", "#8a7f66", "#383626")),
    diagram=[2, 3, 5, 6, 9, 11],
    assets=[
        "One single stegosaurus standing on four legs, seen from the side facing left, a double "
        "row of tall flat plates running along its back and four long spikes at the tip of its "
        "tail, its whole body inside the picture. " + BG,
        "One single tall flat bony plate standing upright, shaped like a rounded triangle, its "
        "surface covered in fine branching grooves. " + BG,
        "One single car radiator seen from the front, a flat rectangular grid of thin metal fins. "
        + BG,
    ],
    pages=[
     ("博物馆里有一只恐龙，\n背上竖着一排板，\n像一把一把\n插在背上的扇子。\n爸爸说，它叫剑龙。",
      f"Waist-up view of the little boy in a museum, his face large in the frame and turned "
      f"towards the viewer, {EYES}, his mouth open in surprise; behind him rises the back of a "
      f"stegosaurus skeleton with a row of tall flat plates.", 1),
     ("最大的一块板，\n比我的脸还大。\n一共十七块，\n沿着背脊\n一路排到尾巴根。", "", 0),
     ("奇怪的是，\n这些板\n并不长在脊椎上。\n它们埋在皮里，\n像插在土里的牌子。", "", 0),
     ("把板切开看，\n里面全是细细的管子。\n血从管子里流过。\n这说明那些板\n是活的，会流血。",
      "One tall bony plate cut open on a cream background, showing many fine branching channels "
      "running through it. Nothing else in the picture.", 0),
     ("有人说，\n板是用来散热的。\n热血流进板里，\n风一吹就凉下来，\n像汽车前面的水箱。", "", 0),
     ("也有人说，\n板是用来吓唬人的。\n血一涌上去，\n板就变得通红，\n看着大了一圈。", "", 0),
     ("到底是哪一种呢？\n也许两样都是。\n一样东西\n本来就可以\n有好几个用处。",
      "One stegosaurus standing in profile on a cream background with its plates flushed a warm "
      "red, one other dinosaur backing away from it. Nothing else in the picture.", 0),
     ("它的尾巴尖上\n还有四根长刺，\n每根都有大人的胳膊那么长。\n甩起来呼呼响，\n谁都得躲开。",
      "Close view of a stegosaurus tail tip on a cream background, four long sharp spikes "
      "spreading out from it, swinging, with motion lines behind. Nothing else in the picture.", 0),
     ("剑龙的头很小，\n脑子只有核桃那么大。\n可它在地球上\n活了好几千万年，\n看来脑子小也不耽误事。",
      "", 0),
     ("它的脖子不长，\n嘴巴几乎贴着地。\n它吃的是矮矮的蕨叶，\n不跟长脖子的\n抢树顶那一层。",
      "One stegosaurus lowering its head to eat low ferns on a cream background. Nothing else in "
      "the picture.", 0),
     ("那排板\n不是两边对齐的。\n是左一块、右一块\n错开着排，\n看上去更宽更唬人。", "", 0),
     ("我伸手\n摸了摸那块板。\n薄薄的，边上还有点糙。\n它当年\n真的会变红吗？",
      f"Waist-up view of the little boy reaching out to touch one tall bony plate on a museum "
      f"mount, his face large in the frame and turned towards the viewer, {EYES}, thoughtful.", 1),
    ]))

BOOKS.append(dict(
    slug="ankylo", seed=92000, title="甲龙的尾巴锤", subtitle="一身盔甲，外加一把锤",
    keyword="甲龙", style_label="厚涂水粉",
    style="children's picture book illustration, thick opaque gouache with bold brush marks and "
          "visible texture, olive green, rust brown and bone cream",
    character="wearing an olive green t-shirt, rust brown shorts and white sneakers, short black hair",
    palette=P(("#2a271f", "#6d6b52", "#f2f0e6", "#fbfaf4", "#a65f3c", "#847a5e", "#d9d6c5"),
              ("#eae7d8", "#9c9a80", "#151208", "#211e12", "#c07a54", "#847a5e", "#37341f")),
    diagram=[2, 4, 6, 8, 10],
    assets=[
        "One single ankylosaurus standing low on four short legs, seen from the side facing left, "
        "its whole back covered in rows of bony plates and knobs, and a large round bony club at "
        "the tip of its tail. " + BG,
        "One single large round bony tail club, two heavy knobs of bone fused together at the end "
        "of a short length of tail. " + BG,
        "One single large meat-eating dinosaur standing on two legs, seen from the side facing "
        "right, its mouth open. " + BG,
    ],
    pages=[
     ("这只恐龙矮矮的，\n背上全是疙瘩，\n尾巴尖上\n还挂着一个大球。\n爸爸说，那是一把锤子。",
      f"Waist-up view of the little boy in a museum beside a low armoured dinosaur model, his "
      f"face large in the frame and turned towards the viewer, {EYES}, curious.", 1),
     ("它从头到尾\n都盖着骨头板。\n背上、脖子上，\n连眼皮上\n都长着一小块骨头。", "", 0),
     ("这身盔甲\n不是披上去的，\n是从皮里长出来的。\n一块一块嵌在皮里，\n脱都脱不下来。",
      "A cut-away view of a piece of thick skin on a cream background, several solid bony plates "
      "embedded inside it. Nothing else in the picture.", 0),
     ("尾巴尖上那个锤，\n是两块骨头\n长在一起长成的。\n有西瓜那么大，\n也有西瓜那么沉。", "", 0),
     ("锤子\n不是天生就有的。\n小甲龙的尾巴是光的，\n长大了\n骨头才慢慢长成一团。",
      "Two ankylosaurus tails side by side on a cream background: a short plain young tail and a "
      "long tail with a big round club at the end. Nothing else in the picture.", 0),
     ("挥起来有多重呢？\n一下能把\n追它的那只\n小腿骨打断。\n所以没人敢从后面来。", "", 0),
     ("它打不过就趴下。\n四条腿一收，\n整个身子贴住地，\n只剩一身骨板朝上，\n谁也咬不动。",
      "One armoured dinosaur crouched flat on the ground on a cream background, its legs tucked "
      "under and only its armoured back showing. Nothing else in the picture.", 0),
     ("它的肚子\n是软的。\n所以它从不翻身，\n也很少跑，\n就那样稳稳地趴着走。", "", 0),
     ("它吃的是\n地上的矮草和蕨。\n嘴前面有一片喙，\n剪断，\n再用后面的小牙磨。",
      "One armoured dinosaur lowering its beak to crop low plants on a cream background. Nothing "
      "else in the picture.", 0),
     ("一身盔甲加一把锤，\n这样的搭配\n在恐龙里也不多见。\n它不追谁，\n谁也别想追它。", "", 0),
     ("甲龙一直活到最后。\n那块石头砸下来那天，\n它还在地上慢慢走。\n盔甲挡得住牙，\n挡不住那一下。",
      "One armoured dinosaur walking slowly across bare ground under a dim grey sky on a cream "
      "background. Nothing else in the picture.", 0),
     ("我绕着它走了一圈，\n从头看到尾。\n锤子就挂在那儿，\n沉甸甸的，\n像是随时会甩起来。",
      f"Waist-up view of the little boy standing beside the tail end of an armoured dinosaur "
      f"model, looking at the big round bony club, his face large in the frame and turned "
      f"towards the viewer, {EYES}, impressed.", 1),
    ]))
