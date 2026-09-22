# -*- coding: utf-8 -*-
"""五本「一本正经讲荒唐事」的书，每本 32 页。

学的是那种手法，不是那两本书的内容：讲故事的人一直对「你」说话；用很正经的口气
讲一件荒唐的事；前面警告一件小事，后面这件小事一定发生；中间一场大乱；最后落回
他自己的生活。故事、句子、角色都是自己写的。

写提示时守的几条（第七批栽过的）：
  · 每个名词都会被画出来——不提不想要的东西，要否掉的就正面写 no X；
  · 画面里不要字：模型会写一堆乱码，所以象声词只在旁白里，画面里不出现；
  · 他出镜的页用「正常比例」那句，不写「只画头和肩」（那句让模型把头画大）；
  · 行为那几本里犯错的是恐龙，不是他——他是帮忙的那个。
"""
import json, os

SB = os.path.dirname(os.path.abspath(__file__))
BOY = ("A medium shot of the little boy seen from his knees up, {what}, his face turned towards "
       "the viewer, drawn with the natural body proportions of a real five-year-old child, his head "
       "in proportion to his body and about one fifth of his height, not a big-headed cartoon, "
       "his eyes calm and natural")
STYLE = ("children's picture book illustration, loose sketchy pencil lines with soft transparent "
         "watercolour washes, lots of plain white paper around the figures, muted faded colours, "
         "simple rounded characters with small dot eyes and calm deadpan expressions, "
         "no words, no letters and no writing anywhere in the picture, {palette}")
PAL = {"ink": "#2a2419", "soft": "#7a6e5a", "ground": "#f5f2ea", "paper": "#fffdf8",
       "accent": "#c0603a", "bark": "#8a7f66", "line": "#e2dccd", "ink_d": "#ece5d8",
       "soft_d": "#a99b83", "ground_d": "#16130e", "paper_d": "#211d16",
       "accent_d": "#e0805a", "bark_d": "#8a7f66", "line_d": "#37301f"}

# 斑点纸画风。画风里不描述龙——写进画风的龙会出现在每一页（第一版每页都挤满了龙）；
# 龙写进每页的画面，并写清楚几只。画面上面三分之一留空，印书时字放那儿。
ODD = ("flat hand-drawn illustration on speckled cream paper with tiny grey flecks, "
       "the speckled paper fills the whole square picture edge to edge with no border, "
       "simple flat colour shapes with thin wobbly outlines, muted faded colours: rusty red, soft pink, "
       "pale yellow, soft green and grey-blue, ordinary objects drawn plain, "
       "without eyes or faces, the upper third of the picture left as empty speckled paper, "
       "no words, no letters and no writing anywhere in the picture")

SEEDS = {("dragonsocks", 23): 130923}   # 这几页换过种子：原种子的构图总在前景塞一排东西

# 每页：(旁白, 画面, 他在不在)。画面里的 {c} 换成这本书的主角描述。
BOOKS = [
 dict(slug="dragonsocks", title="龙最爱收袜子", subtitle="你少的那只袜子去哪儿了",
      seed=130000, style_label="斑点纸平涂", palette="",
      character="",
      style_full=ODD,
      cast={"A": "one long flat brick-red dragon shaped like a stretched pillow, with branching antler-like horns, droopy whiskers and tiny stubby legs, small dot eyes and a plain deadpan face",
            "B": "one round dusty-pink dragon shaped like a potato, with two small round bumps on its head and tiny stubby legs",
            "C": "one tall thin sage-green dragon with a long neck, no horns and tiny wings, small dot eyes and a plain deadpan face",
            "D": "one small grey-blue dragon with a curly tail, one short horn and droopy whiskers, small dot eyes and a plain deadpan face",
            "E": "one very long sandy-yellow dragon, small dot eyes and a plain deadpan face",
            "G": "four dragons of different shapes and colours: a long flat brick-red one with antler-like horns, a round dusty-pink one, a tall thin sage-green one and a small grey-blue one"},
      pages=[
  ("嘿，小朋友。\n你的袜子，\n是不是总是少一只？", "One single striped sock lying alone on a wooden floor, and at the very edge of the picture the tip of one brick-red dragon tail slipping out of view, no other dragons", 0),
  ("大人会说，\n是洗衣机吃掉了。", "A washing machine with its round door open and nothing inside, standing alone, no dragons and no animals in the picture", 0),
  ("洗衣机才不吃袜子。\n洗衣机连饭都不吃。", "The same washing machine standing alone with its round door shut, no dragons and no animals in the picture", 0),
  ("是龙拿走的。", "{A} sneaking along a hallway floor on tiptoe with a striped sock in its mouth, only one dragon in the picture", 0),
  ("龙最爱收袜子。", "{B} lying on its back hugging a sock to its chest with a blissful face, only one dragon in the picture", 0),
  ("条纹的，圆点的，\n毛茸茸的。\n有个小洞的，也要。", "{C} holding up a sock with a small hole and peering through the hole with one eye, a few socks lying beside it, only one dragon in the picture", 0),
  ("只有爸爸的袜子，龙不要。\n太大了，\n还有点味儿。", "{D} holding a huge grey sock as far away from its body as it can with both arms stretched straight out, head turned away in disgust, eyes squeezed shut, only one dragon in the picture", 0),
  ("龙都很有礼貌。\n拿走袜子之前，\n一定会先问一声。", "A small simple cartoon child fast asleep in bed at night with eyes closed, and beside the bed {A} with its mouth stuffed full of many socks, more socks dangling from its lips, only one dragon in the picture", 0),
  ("大概问了吧。", "{A} with its cheeks puffed out enormously round like two balloons because its mouth is stuffed full, the tip of a sock poking out between its lips, looking straight at the viewer innocently, only one dragon in the picture", 0),
  ("龙从来不承认\n是它拿的。", "{B} with a sock hanging out of its mouth, looking away to the side, only one dragon in the picture", 0),
  ("它们把袜子带回山洞，\n堆成一座袜子山。", "A cave with an enormous mountain of colourful socks inside, {G} climbing up it", 0),
  ("晚上，就钻进去睡觉。\n又软，又暖，\n还有一点点脚丫的味道。", "{G} asleep inside a big heap of socks, only their heads and tails poking out", 0),
  ("大龙喜欢长袜子。", "{E} with eight tiny stubby legs, each leg wearing a different long sock, only one dragon in the picture", 0),
  ("小龙喜欢短袜子。", "{B} wearing little ankle socks on its feet, only one dragon in the picture", 0),
  ("最小的龙只要一只，\n戴在尾巴尖上。\n它觉得这样最帅。", "{D} proudly looking back at a single small sock on the tip of its curly tail, only one dragon in the picture", 0),
  ("龙不分左脚右脚。\n一只蓝的配一只红的。\n它们说，这叫时髦。", "{C} posing proudly in one red sock and one blue sock, only one dragon in the picture", 0),
  ("所以，你要是想请龙来家里玩，\n就把袜子挂出来。", "A backyard with clotheslines full of socks of every colour, no people and no dragons in the picture", 0),
  ("越多越好。", "A small simple cartoon child adding one more sock to clotheslines crammed with dozens and dozens of socks, the lines sagging so low under the weight that they almost touch the ground, no dragons in the picture", 0),
  ("不过，有一件事，\n你一定、一定要记住。", "Close-up of one grey sock lying alone on a plain wooden floor, nothing else in the picture", 0),
  ("千万不能给龙\n臭袜子。", "One grey sock with wavy smell lines rising from it in the front, and far away in the distance {D} pinching its nose shut", 0),
  ("龙一闻到臭袜子，\n就会马上睡着。\n站着的，就站着睡。\n趴着的，就趴着睡。", "Three dragons fast asleep in silly positions: {C} asleep standing up, {B} asleep upside down, and {A} asleep flat on its belly", 0),
  ("睡着的龙会打呼噜，\n打得整座城都在晃。", "{A} asleep on a hill with its eyes shut and its mouth wide open, and in the town below every little house is tilted at a crazy angle, roofs hopping up off the houses, chimneys tipping over, wobbly motion lines around everything", 0),
  ("所以，臭袜子，放远一点。\n再远一点。\n……好，就放那儿。", "A wide empty grassy landscape under a pale sky, the grass in the front completely empty with nothing lying on it, and far away on top of a distant hill one tiny grey sock next to a tiny flag, nothing else in the picture", 0),
  ("星期六，\n你办了一个袜子派对。", "A small simple cartoon child standing in a backyard full of hanging socks, waving, while {G} climb over the garden fence", 0),
  ("龙都来了。\n长的，圆的，扁的，\n还有一只一直在说「不是我」的。", "{G} standing in a backyard, one of them with a sock hanging out of its mouth looking away", 0),
  ("大家穿着袜子跳舞，\n跳得正高兴——", "A small simple cartoon child dancing in a backyard with {G} who wear socks on their feet and tails", 0),
  ("可是谁也没看见，\n小狗叼来了一只袜子。\n一只踢了一整天足球的袜子。", "A small scruffy white dog trotting into a backyard with a muddy grey sock in its mouth, wavy smell lines rising from the sock, no dragons in the picture", 0),
  ("吸——", "{D} leaning its nose towards a muddy grey sock, its eyes slowly closing, only one dragon in the picture", 0),
  ("呼噜！呼噜！呼噜！\n窗户在抖，屋顶在晃，\n小狗跳进了篮子里。", "{G} all fast asleep in a heap in a backyard, every one with its eyes shut tight and its mouth wide open snoring, the house behind them with its roof lifting up off the walls and its windows rattling with wobbly motion lines, a small white dog hiding in a laundry basket with only its eyes showing", 0),
  ("怎么叫都叫不醒。\n你把那只袜子拿去洗了。\n洗了三遍。", "A small simple cartoon child scrubbing a grey sock in a bucket full of soap bubbles, a few sleeping dragons small in the background", 0),
  ("袜子香了。\n龙一只一只醒过来，\n打个哈欠，接着跳。", "{G} waking up, yawning and stretching in a backyard full of hanging socks", 0),
  ("现在你知道了。\n下次再少一只袜子，\n别怪洗衣机。\n去看看龙的尾巴。\n它会说：不是我。", "{A} walking away across the speckled paper with a striped sock on the tip of its tail, looking back over its shoulder at the viewer, only one dragon in the picture", 0),
      ]),
 dict(slug="dinobubbles", title="恐龙爱泡泡浴", subtitle="千万别放会叫的小黄鸭",
      seed=131000, style_label="铅笔淡彩", palette="soft aqua, lilac and warm orange",
      character="wearing light blue pyjamas with short sleeves, short black hair",
      c="soft rounded friendly cartoon dinosaurs with small dot eyes",
      pages=[
  ("嘿，小朋友。\n你知道恐龙最爱干什么吗？", "holding a toy dinosaur, looking curious", 1),
  ("不是吼。\n也不是跑。", "one of the {c} standing with a bored face, arms hanging, on white paper", 0),
  ("是泡泡浴。", "one of the {c} sitting in an old bathtub full of bubbles, eyes half closed, blissful", 0),
  ("大泡泡。", "one of the {c} blowing one enormous bubble", 0),
  ("小泡泡。", "a small one of the {c} surrounded by hundreds of tiny bubbles", 0),
  ("能把一整只恐龙装进去的\n超级大泡泡。", "one of the {c} floating calmly inside a giant clear bubble", 0),
  ("它们用泡泡做胡子。", "one of the {c} with a big white beard made of foam", 0),
  ("做帽子，做皇冠。", "three of the {c} wearing tall hats and crowns made of foam", 0),
  ("三角龙喜欢把泡泡\n堆在三只角上。", "a triceratops in a bathtub with foam piled up on its three horns", 0),
  ("长脖子恐龙喜欢泡到\n只剩一个脑袋。", "a long-necked dinosaur in a very deep tub, only its head above the foam", 0),
  ("霸王龙的手太短了，\n搓不到背。", "a T. rex in a bathtub stretching its tiny arms and failing to reach its back", 0),
  ("所以它每次泡澡，\n都要请朋友帮忙。", "a triceratops scrubbing a T. rex's back with a long brush in the bath", 0),
  ("要是你想请恐龙来家里，\n就放一大缸泡泡水。", "pouring bubble liquid into a big bathtub, sleeves pushed up", 1),
  ("越满越好。", "a bathtub overflowing with foam spilling onto the floor, nobody in the picture", 0),
  ("不过，你一定要记住一件事。", "one small yellow rubber duck alone on white paper", 0),
  ("千万不能放\n会叫的小黄鸭。", "one of the {c} peeking nervously from far away at a small yellow rubber duck", 0),
  ("恐龙什么都不怕。\n不怕打雷，也不怕黑。", "one of the {c} sitting calmly under a dark stormy sky, unbothered", 0),
  ("就怕那一声吱。", "a small yellow rubber duck in the middle, the {c} around it frozen with wide eyes", 0),
  ("它们一听见，\n就会吓得跳起来，\n到处乱跑。", "the {c} leaping and running off in every direction", 0),
  ("所以，小黄鸭，\n放到别的地方去。", "reaching up to put a yellow rubber duck on a high shelf", 1),
  ("星期六晚上，他决定\n办一个泡泡浴派对。", "standing in a bathroom beside a big old bathtub, towels over his arm", 1),
  ("他放了满满一缸水，\n倒了一整瓶泡泡液。", "pouring a big bottle into the bath while foam rises high", 1),
  ("恐龙一只一只挤进来。", "the {c} squeezing through a bathroom doorway one after another", 0),
  ("它们泡得眯起了眼睛。\n舒服极了。", "sitting on the edge of the bathtub while the {c} soak packed together in the foam, eyes closed", 1),
  ("可是，谁也没有发现，\n泡泡底下，\n漂着一只小黄鸭。", "a close view of foam with a small yellow rubber duck half hidden underneath", 0),
  ("一只恐龙坐了下去——", "a large one of the {c} lowering itself slowly into the foam", 0),
  ("吱！", "a flattened yellow rubber duck under a dinosaur's bottom, the dinosaur's eyes huge", 0),
  ("恐龙全跳起来了！", "the {c} leaping out of the bathtub, foam flying everywhere", 0),
  ("泡泡飞出窗户，飞满客厅，\n一直涨到天花板。", "a living room filled with foam up to the ceiling, dinosaur tails poking out of it", 0),
  ("他在泡泡里摸呀摸，\n摸到了那只小黄鸭。\n他把它捏住，不让它叫了。", "standing waist-deep in foam holding a yellow rubber duck tightly in both hands", 1),
  ("大家把泡泡搬到后院，\n吹出一个比房子还大的泡泡。", "in the backyard with the {c} beside a giant bubble bigger than the house", 1),
  ("现在你知道了：\n恐龙爱泡泡浴，不爱会叫的鸭子。\n今天晚上洗澡的时候，你也看看，\n泡泡里有没有一只小恐龙。", "kneeling beside a bathtub with one hand in the foam, a tiny dinosaur peeking out of the bubbles", 1),
      ]),
 dict(slug="dinowantsplay", title="恐龙想跟你玩", subtitle="千万别对恐龙说「不行」",
      seed=132000, style_label="铅笔淡彩", palette="leaf green, sand and soft brick red",
      character="wearing a green t-shirt, khaki shorts and white sneakers, short black hair",
      c="soft rounded friendly cartoon dinosaurs with small dot eyes",
      pages=[
  ("嘿，小朋友。\n你知道恐龙最想干什么吗？", "standing in a backyard, looking curious", 1),
  ("找人玩。", "a small triceratops peeking around a tree trunk, looking for someone", 0),
  ("恐龙交朋友的办法\n很奇怪。", "two of the {c} standing nose to nose, studying each other", 0),
  ("先闻一闻你。", "one of the {c} sniffing the top of another one's head", 0),
  ("再甩一甩尾巴。", "one of the {c} wagging its tail happily", 0),
  ("最后，把它最喜欢的\n那块石头送给你。", "one of the {c} holding out a smooth round stone", 0),
  ("收到石头，就是说：\n我们是朋友了。", "two of the {c} sitting side by side, a round stone between them", 0),
  ("霸王龙问「我可以一起玩吗」\n的时候，嗓门太大了。", "a T. rex with its mouth wide open, leaves blowing off a tree in front of it", 0),
  ("树叶全被吹掉了。", "a completely bare tree, leaves piled on the ground, a T. rex looking sheepish", 0),
  ("三角龙玩滑梯，\n角会卡住。", "a triceratops stuck halfway down a playground slide by its horns", 0),
  ("所以它最会排队，\n从来不挤。", "the {c} waiting in a neat line at a slide, a triceratops at the back", 0),
  ("长脖子恐龙最会轮流：\n让大家一个一个，\n从它的脖子上滑下来。", "a long-necked dinosaur bending its neck like a slide while small dinosaurs slide down one at a time", 0),
  ("不过，你一定要记住一件事。", "one small triceratops sitting alone in the middle of white paper, looking at the viewer", 0),
  ("千万别对恐龙说「不行！」\n然后扭头就走。", "one of the {c} with drooping head looking at a trail of footprints walking away", 0),
  ("恐龙一听见「不行」，\n就会把尾巴一盘，\n脑袋一缩——", "one of the {c} curling up tight, tucking in its head and tail", 0),
  ("变成一块大石头。\n谁也搬不动。", "a large round grey boulder shaped like a curled-up dinosaur, the tip of a tail peeking out", 0),
  ("星期天，他在院子里\n用积木搭恐龙城堡。", "building a castle of wooden blocks on the grass in the backyard", 1),
  ("他搭到最要紧的一层，\n一块一块，小心又小心。", "carefully placing one block on top of a tall block castle", 1),
  ("一只小三角龙走过来，\n捧着一块圆石头。\n「我也想玩。」", "busy with his block castle while a small triceratops walks up holding a round stone", 1),
  ("他一着急，\n张嘴就说——", "turning towards a small triceratops, his mouth opening, one hand up", 1),
  ("「不行！」", "holding one arm out in front of his block castle, a small triceratops startled in front of him", 1),
  ("小三角龙一缩——", "a small triceratops curling up tight, tucking in its head", 0),
  ("变成了一块大石头，\n正好堵住城堡的门。", "staring at a big round boulder sitting in front of the door of his block castle", 1),
  ("别的恐龙来了，一看——\n也都缩成了石头。", "more of the {c} arriving in the backyard and curling up into boulders", 0),
  ("一块、两块、十块……\n院子里全是石头。", "standing in the middle of a backyard full of big round boulders", 1),
  ("他推也推不动。", "pushing a big round boulder with all his strength, cheeks puffed", 1),
  ("叫也叫不醒。", "calling out to a big round boulder with his hands around his mouth", 1),
  ("他想起来了：\n恐龙听不得「不行」，\n可是听得懂「等一下」。", "sitting on the grass beside a boulder with his chin in his hand, thinking", 1),
  ("他蹲下来，小声说：\n「对不起，我刚才正在搭。\n等我搭完这一块，\n你来搭屋顶，好吗？」", "crouching beside a big round boulder, speaking to it softly", 1),
  ("咔嚓！\n石头裂开了，\n小三角龙跳了出来。", "a boulder cracking open and a small triceratops popping out of it happily", 0),
  ("大家一起搭。\n城堡比原来大了三倍。", "building an enormous block castle together with the {c}", 1),
  ("现在你知道了：\n有人想跟你玩的时候，别说「不行」。\n说「等一下」，再给他一件事做。\n下次有小朋友来找你，你也试试。", "sitting on top of a big block castle next to a small triceratops at sunset", 1),
      ]),
 dict(slug="trexwontstop", title="霸王龙不想停", subtitle="小鼓手敲门了吗",
      seed=133000, style_label="铅笔淡彩", palette="moss green, warm yellow and soft sky blue",
      character="wearing a yellow t-shirt, navy shorts and white sneakers, short black hair",
      c="a big friendly green T. rex with tiny arms, a soft rounded body and small dot eyes",
      pages=[
  ("嘿，小朋友。\n你知道霸王龙最讨厌什么吗？", "standing in a park, looking curious", 1),
  ("不是下雨。", "{c} standing in the rain, completely unbothered", 0),
  ("不是蚊子。", "{c} with a tiny mosquito sitting on its nose, completely unbothered", 0),
  ("是——\n停下来。", "{c} frozen in the middle of running, looking very annoyed", 0),
  ("它一玩起来，\n就停不下来。", "{c} bouncing around happily in a meadow", 0),
  ("跑步。", "{c} running fast across the grass", 0),
  ("捉迷藏。", "{c} hiding badly behind a very thin tree, most of its body showing", 0),
  ("搭石头城堡，\n一玩就是一整天。", "{c} stacking stones into a little castle as the sun goes down", 0),
  ("可是，有一件事，\n它不停也得停。", "{c} stopping suddenly, looking down at its own round belly", 0),
  ("每只恐龙的肚子里，\n都住着一个小鼓手。", "a round dinosaur looking down in surprise at its own belly, a small drum drawn faintly on the belly", 0),
  ("咚咚咚。", "one small drum with two drumsticks on white paper, little motion marks around it", 0),
  ("这是在说：\n该去厕所了。", "a small wooden outhouse standing behind a big tree in a green jungle", 0),
  ("三角龙一听见，马上就去。\n从来不磨蹭。", "a triceratops walking briskly towards a wooden outhouse behind a tree", 0),
  ("长脖子恐龙的鼓手在很下面，\n声音要走好久，\n才传到脑袋。", "a long-necked dinosaur with small wavy motion marks travelling up its long neck", 0),
  ("所以，它总是很早很早\n就出发。", "a long-necked dinosaur setting off at dawn towards a wooden outhouse", 0),
  ("不过，你一定要记住一件事。", "one small drum alone in the middle of white paper", 0),
  ("千万别让小鼓手等。", "a small drum shaking with motion marks while a dinosaur turns its back on it", 0),
  ("你不理它，\n它就越敲越响——", "a small drum shaking hard, leaves trembling on nearby bushes", 0),
  ("最后，它干脆不敲了。", "a silent small drum, a dinosaur beside it with very wide eyes", 0),
  ("那天，他和霸王龙\n在比赛搭石头塔。", "stacking stones into a tower on the grass next to {c}", 1),
  ("谁搭得高，谁就赢。", "concentrating on his stone tower while {c} builds its own beside him", 1),
  ("咚咚咚。\n霸王龙说：「等一下，\n我再玩一会儿。」", "watching {c} wave a tiny arm dismissively and keep stacking stones", 1),
  ("咚咚咚咚！\n「再等一下，我快赢了！」", "looking worried at {c}, who is stacking stones with its knees pressed together", 1),
  ("轰！轰！轰！", "{c} leaping straight up in the air with huge eyes", 0),
  ("霸王龙夹着腿，\n就跑。", "{c} running with its knees pressed together, looking desperate", 0),
  ("厕所在山那边！", "a green hill, a tiny wooden outhouse far away on the other side, {c} small in the front", 0),
  ("要过小河。", "{c} leaping over a small stream", 0),
  ("跳过三块石头。", "running ahead and pointing the way while {c} hops across three stepping stones", 1),
  ("钻过一个山洞。\n他在前面帮它开路。", "holding branches aside at the mouth of a cave while {c} hurries through", 1),
  ("差一点点……差一点点……\n扑通！坐上去了。\n霸王龙长长地松了一口气。", "{c} hidden behind tall bushes next to a wooden outhouse, only its relieved face showing above them", 0),
  ("回来一看，石头塔还在，\n一块都没倒。\n「原来一听见就去，\n一点都不耽误玩。」", "standing beside two stone towers with {c}, both smiling", 1),
  ("现在你知道了：\n小鼓手一敲，马上就去，\n游戏会等你。\n你的小鼓手，现在敲门了吗？", "walking towards a bathroom door holding a toy dinosaur, looking back over his shoulder", 1),
      ]),
 dict(slug="dinojoin", title="恐龙想加入", subtitle="想加入的时候，要说暗号",
      seed=134000, style_label="铅笔淡彩", palette="grass green, warm grey and soft coral",
      character="wearing a coral t-shirt, grey shorts and white sneakers, short black hair",
      c="soft rounded friendly cartoon dinosaurs with small dot eyes",
      pages=[
  ("嘿，小朋友。\n你知道吗？", "standing on a grassy hill, looking curious", 1),
  ("恐龙玩游戏的时候，\n有一句暗号。", "the {c} huddled close in a circle, whispering", 0),
  ("不知道暗号的，\n谁也进不去。", "the {c} in a closed circle with their backs out, one small dinosaur outside peeking in", 0),
  ("今天，我偷偷告诉你。", "leaning in with one hand cupped behind his ear", 1),
  ("不过，你得先听我讲完。", "sitting cross-legged on the grass, listening", 1),
  ("恐龙最爱玩的游戏，\n叫「滚大蛋」。", "a huge round stone egg sitting on top of a grassy hill", 0),
  ("一颗比房子还大的石头蛋。", "a giant round stone egg next to a small cottage, taller than the cottage", 0),
  ("从山坡上滚下来，\n大家一起追。", "the {c} chasing a giant rolling stone egg down a hill", 0),
  ("三角龙管推。", "a triceratops pushing a giant stone egg with its horns", 0),
  ("长脖子恐龙管在前面看路。", "a long-necked dinosaur at the front looking far ahead", 0),
  ("最小的恐龙管喊\n「一、二、三」。", "a tiny dinosaur standing on a rock with its mouth wide open", 0),
  ("每只恐龙都有一件事做。\n所以想加入，\n光说「我要玩」不够。", "the {c} around a giant stone egg, each busy with a different job", 0),
  ("暗号是两句话。", "one small dinosaur whispering into the ear of another", 0),
  ("第一句：\n「我可以一起玩吗？」", "asking a triceratops a question politely, hands together", 1),
  ("第二句：\n「我可以帮你们……」\n后面，说你会做的事。", "pointing at himself while a triceratops listens", 1),
  ("不过，你一定要记住一件事：\n千万别不说暗号，\n就冲进去抢那颗蛋。", "a giant stone egg on a hilltop, the {c} standing guard around it", 0),
  ("恐龙会以为你是来抢东西的。\n呼——全跑光，\n只剩一地脚印。", "an empty hillside covered with dinosaur footprints leading away into bushes", 0),
  ("那天，他在山坡下面，\n看见恐龙们在滚大蛋。", "at the bottom of a hill looking up at the {c} gathered around a giant stone egg", 1),
  ("他太想玩了。", "with both fists clenched in excitement, eyes wide", 1),
  ("暗号？\n忘了。", "running up the hill as fast as he can", 1),
  ("他一下冲过去，\n一把抱住那颗蛋。", "hugging a giant stone egg with both arms", 1),
  ("呼——\n恐龙全跑光了。", "still hugging a giant stone egg while the {c} flee into the bushes", 1),
  ("地上只剩一圈脚印，\n和他。", "standing alone next to a giant stone egg on a hilltop, footprints all around him", 1),
  ("没人扶，\n大石头蛋开始往下滚。", "reaching out as a giant stone egg starts to roll away down the hill", 1),
  ("越滚越快！", "a giant stone egg rolling fast down a grassy slope", 0),
  ("他一个人在后面追。\n追不上！", "running down the hill after a giant rolling stone egg", 1),
  ("蛋滚过小河，滚过草地，\n眼看就要滚进泥坑。", "a giant stone egg rolling towards a big brown mud puddle", 0),
  ("他停下来。\n他想起来了。", "stopping on the hillside, thinking hard", 1),
  ("他转身对着树丛，大声说：\n「我可以一起玩吗？\n我可以帮你们挡住蛋！」", "facing a row of bushes with his hands cupped around his mouth, calling out", 1),
  ("树丛里探出一个个脑袋。\n恐龙们冲出来了！", "dinosaur heads popping out of the bushes, then the {c} running out", 0),
  ("三角龙推，长脖子看路，\n他站在泥坑前面，\n一伸手——挡住了！", "stopping a giant stone egg at the edge of a mud puddle with both hands while the {c} help", 1),
  ("现在你知道暗号了：\n走过去，问一句，\n再说你能帮什么。\n要是他们说「等一下」，\n那是游戏正玩到一半。\n等一等，他们会叫你的。", "sitting on top of a giant stone egg with the {c}, all laughing", 1),
      ]),
]

for b in BOOKS:
    assert len(b["pages"]) == 32, (b["slug"], len(b["pages"]))
    pages = []
    for i, (zh, scene, boy) in enumerate(b["pages"], 1):
        scene = scene.replace("{c}", b.get("c", ""))
        for k, v in b.get("cast", {}).items():
            scene = scene.replace("{" + k + "}", v)
        extra = {"seed": SEEDS[(b["slug"], i)]} if (b["slug"], i) in SEEDS else {}
        pages.append({"n": i, "zh": zh, "has_boy": bool(boy), **extra,
                      "scene": BOY.format(what=scene) if boy else scene[0].upper() + scene[1:]})
    doc = {"workflow": "workflows/qwen_image_2512.json",
           "colophon": {"model": "Qwen-Image-2512 + Qwen-Image-Edit-2511 (Q3)",
                        "lora": "照片参考，不用 LoRA", "strength": 1.3},
           "title": b["title"], "subtitle": b["subtitle"], "slug": b["slug"],
           "seed_base": b["seed"], "character": b["character"],
           "style": b.get("style_full") or STYLE.format(palette=b["palette"]), "style_label": b["style_label"],
           "keyword": "", "diagram_pages": [], "palette": PAL, "neg_extra": "", "pages": pages}
    json.dump(doc, open(os.path.join(SB, f"story_{b['slug']}.json"), "w", encoding="utf-8",
                        newline="\n"), ensure_ascii=False, indent=2)
    boys = sum(p["has_boy"] for p in pages)
    words = sum(len(p["zh"].replace("\n", "")) for p in pages)
    print(f"{b['slug']:14} {b['title']:10} 32 页，他出镜 {boys} 页，旁白 {words} 字")
