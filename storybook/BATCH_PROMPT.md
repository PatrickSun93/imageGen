# 五本绘本 — 出图任务

给 Windows / NVIDIA 那台机器。跟《恐龙没有走远》同一套流程，参数不变，只是换脚本。

## 一、怎么跑

每本 10 页，1024×1024，出好后**按书分别打包**成 `sea.zip` / `crab.zip` / `night.zip` / `star.zip` / `seed.zip`，文件名 `page_01.png` … `page_10.png`。

下面每一页的提示词已经拼好了，**直接复制整段用，不要再拼 style**。

标了「带 LoRA」的页要挂 `son_ohwx_flux_v1`（strength 1.3）；没标的页**不要挂 LoRA、不要带 `ohwx boy`**。

## 二、通用负面提示词

```
character sheet, model sheet, multiple views, grid, collage, text, watermark, signature, blurry, deformed hands, extra fingers, photorealistic face
```
每本另有附加负面词，写在各书标题下面，**追加**到上面这段后面。

## 三、一条重要经验

恐龙那本的 `style` 里写了 `soft natural light`，结果「天空变黑了」那页出来是亮的。

**`style` 里的光照词会盖过 scene 的氛围描述。** 所以这五本我已经按整本的光线基调

把光照词写进 style 了（比如睡前那本是 `quiet glowing light`）。别再自己改 style。

如果某一页出来的明暗跟中文旁白不符，告诉我，我改 style 而不是改 scene。

---

## 《海只来一点点》 — `sea.zip`

> 浪来了，又回去了　·　画风：清透水彩　·　种子：4000 + 页码　·　带 LoRA 的页：1, 2, 3, 5, 10

**附加负面词**：`stormy, huge crashing waves, dark water, deep ocean, frightening, dramatic`

### page_01　seed 4001　带 LoRA

*旁白：我第一次来海边。 / 海好大好大，看不到边。 / 浪的声音轰隆隆的。 / 我抓紧了爸爸的手。*

```
ohwx boy, wearing a pale yellow t-shirt and orange shorts, bare feet, short black hair, children's picture book illustration, gentle watercolor painting, soft sea green and warm sand palette, loose wet washes, lots of white paper showing, calm soft daylight, A little boy stands high on a wide empty sandy beach, far back from the water, holding a grown-up's hand, looking out at a very large calm sea under a big pale sky. He is small in the frame, sea and sky fill most of the picture, wide open composition.
```

### page_02　seed 4002　带 LoRA

*旁白：爸爸说： / 「我们不下水， / 就坐在这里看。」 / 沙子是干的，暖暖的。*

```
ohwx boy, wearing a pale yellow t-shirt and orange shorts, bare feet, short black hair, children's picture book illustration, gentle watercolor painting, soft sea green and warm sand palette, loose wet washes, lots of white paper showing, calm soft daylight, A little boy and his father sitting together on warm dry sand near the top of a beach, seen from the side, the sea far away in the background, a folded towel beside them, calm and unhurried.
```

### page_03　seed 4003　带 LoRA

*旁白：浪跑过来了—— / 我往后缩了一下。 / 可是它没有过来。 / 它停住了，然后回去了。*

```
ohwx boy, wearing a pale yellow t-shirt and orange shorts, bare feet, short black hair, children's picture book illustration, gentle watercolor painting, soft sea green and warm sand palette, loose wet washes, lots of white paper showing, calm soft daylight, A thin sheet of seawater running up wet sand toward a little boy's bare feet and stopping short of them, the boy leaning back slightly, low viewpoint close along the sand, gentle foam edge.
```

### page_04　seed 4004　不挂 LoRA

*旁白：又来了一次。 / 还是停在那里。 / 再来一次。 / 每一次，都停在同一个地方。*

```
children's picture book illustration, gentle watercolor painting, soft sea green and warm sand palette, loose wet washes, lots of white paper showing, calm soft daylight, Three thin curved lines of foam left on wet sand at the same distance from the viewer, marking where each wave stopped, a gentle repeating pattern on an empty beach, soft daylight from above.
```

### page_05　seed 4005　带 LoRA

*旁白：我数：一、二、三…… / 浪就来了。 / 一、二、三…… / 浪就回去了。 / 原来它是有拍子的。*

```
ohwx boy, wearing a pale yellow t-shirt and orange shorts, bare feet, short black hair, children's picture book illustration, gentle watercolor painting, soft sea green and warm sand palette, loose wet washes, lots of white paper showing, calm soft daylight, A little boy sitting on the sand counting on his fingers, mouth open counting, a small wave rolling in gently behind him, bright and calm.
```

### page_06　seed 4006　不挂 LoRA

*旁白：浪回去以后， / 沙子上留下了东西： / 一个白色的贝壳， / 一根海草， / 还有一个小小的洞。*

```
children's picture book illustration, gentle watercolor painting, soft sea green and warm sand palette, loose wet washes, lots of white paper showing, calm soft daylight, Close up of wet sand after a wave has gone, a single white spiral shell, one strand of dark seaweed, and a small round hole in the sand with tiny bubbles, seen from above.
```

### page_07　seed 4007　不挂 LoRA

*旁白：岩石中间有小水坑。 / 那是浪走的时候， / 忘记带走的一点点海。 / 这种小水坑叫「潮池」。*

```
children's picture book illustration, gentle watercolor painting, soft sea green and warm sand palette, loose wet washes, lots of white paper showing, calm soft daylight, A shallow rock pool between grey rocks, clear still water, seaweed around the rim, sunlight on the surface, small movement in the water, quiet and inviting.
```

### page_08　seed 4008　不挂 LoRA

*旁白：里面住着好多小东西： / 一只小螃蟹，横着走。 / 一条小鱼，比我的手指还短。 / 还有一颗海星， / 慢慢地、慢慢地爬。*

```
children's picture book illustration, gentle watercolor painting, soft sea green and warm sand palette, loose wet washes, lots of white paper showing, calm soft daylight, Inside a clear rock pool seen from above: a small crab walking sideways, a tiny fish shorter than a finger, and an orange starfish moving slowly across the bottom, pebbles and green seaweed, bright clear water.
```

### page_09　seed 4009　不挂 LoRA

*旁白：它们一点也不怕。 / 它们在等下一次浪来， / 接它们回家。*

```
children's picture book illustration, gentle watercolor painting, soft sea green and warm sand palette, loose wet washes, lots of white paper showing, calm soft daylight, A rock pool with small sea creatures resting quietly among the rocks, and beyond the rocks the sea further out with one gentle wave approaching in the distance, warm afternoon light.
```

### page_10　seed 4010　带 LoRA

*旁白：我站起来，慢慢走过去。 / 浪来了，碰到我的脚。 / 凉凉的，痒痒的。 / 然后它就回去了。 / 我说：「明天我还来。」*

```
ohwx boy, wearing a pale yellow t-shirt and orange shorts, bare feet, short black hair, children's picture book illustration, gentle watercolor painting, soft sea green and warm sand palette, loose wet washes, lots of white paper showing, calm soft daylight, A little boy standing at the very edge of the water, a thin sheet of foam just touching his bare feet, looking down at his own feet and smiling, calm sea behind, gentle low sunlight.
```

---

## 《寄居蟹换了新房子》 — `crab.zip`

> 长大了，就要换一个大一点的　·　画风：彩铅　·　种子：5000 + 页码　·　带 LoRA 的页：1, 2, 3, 10

**附加负面词**：`scary, pincers threatening, dark, realistic photo`

### page_01　seed 5001　带 LoRA

*旁白：还是那片海滩。 / 今天我敢走近一点了。 / 我蹲下来找贝壳。*

```
ohwx boy, wearing a pale yellow t-shirt and orange shorts, bare feet, short black hair, children's picture book illustration, colored pencil drawing, warm sandy palette with soft coral accents, visible pencil strokes and gentle cross-hatching, soft daylight, A little boy crouching on wet sand close to the water's edge, looking down at the sand for shells, a small bucket beside him, bright open beach, calm sea behind.
```

### page_02　seed 5002　带 LoRA

*旁白：我捡到一个漂亮的贝壳。 / 咦—— / 它在动！ / 它长出脚来，跑起来了。*

```
ohwx boy, wearing a pale yellow t-shirt and orange shorts, bare feet, short black hair, children's picture book illustration, colored pencil drawing, warm sandy palette with soft coral accents, visible pencil strokes and gentle cross-hatching, soft daylight, Close up of a little boy's open palm holding a pretty spiral shell, small crab legs poking out of the shell opening, the boy's surprised face behind slightly out of focus.
```

### page_03　seed 5003　带 LoRA

*旁白：爸爸说： / 「这不是贝壳。 / 这是「寄居蟹」。 / 它住在别人的空壳里。」*

```
ohwx boy, wearing a pale yellow t-shirt and orange shorts, bare feet, short black hair, children's picture book illustration, colored pencil drawing, warm sandy palette with soft coral accents, visible pencil strokes and gentle cross-hatching, soft daylight, A father crouching beside a little boy on the sand, both looking closely at a hermit crab sitting in a spiral shell on the boy's palm, warm and gentle.
```

### page_04　seed 5004　不挂 LoRA

*旁白：寄居蟹自己没有硬壳。 / 它前面是硬的， / 后面软软的、卷卷的。 / 所以它要找一个空壳， / 钻进去，背着走。*

```
children's picture book illustration, colored pencil drawing, warm sandy palette with soft coral accents, visible pencil strokes and gentle cross-hatching, soft daylight, A clear friendly picture book diagram of a hermit crab half out of its shell on plain sand, showing hard front claws and a soft curled belly, gentle and cute, not scary, plenty of empty space around it.
```

### page_05　seed 5005　不挂 LoRA

*旁白：我把它放回沙子上。 / 它伸出脚，慢慢走了。 / 壳在背上，一晃一晃。*

```
children's picture book illustration, colored pencil drawing, warm sandy palette with soft coral accents, visible pencil strokes and gentle cross-hatching, soft daylight, A hermit crab walking away across wet sand carrying its spiral shell tilted on its back, small tracks left behind it, low close viewpoint.
```

### page_06　seed 5006　不挂 LoRA

*旁白：可是它一直在长大。 / 壳不会跟着长大。 / 有一天， / 壳就太小了。*

```
children's picture book illustration, colored pencil drawing, warm sandy palette with soft coral accents, visible pencil strokes and gentle cross-hatching, soft daylight, A hermit crab whose body has grown too big for its shell, part of it squeezed out, sitting on the sand with a slightly worried face, gentle and sympathetic, soft light.
```

### page_07　seed 5007　不挂 LoRA

*旁白：于是它要搬家。 / 它在沙滩上找啊找。 / 试一个——太小。 / 再试一个——太大。*

```
children's picture book illustration, colored pencil drawing, warm sandy palette with soft coral accents, visible pencil strokes and gentle cross-hatching, soft daylight, A hermit crab beside three empty spiral shells of different sizes on the sand, reaching toward one to compare, busy and small, lots of sand around.
```

### page_08　seed 5008　不挂 LoRA

*旁白：找到合适的了！ / 它飞快地钻出来， / 一下子钻进新壳。 / 这一下， / 是它最紧张的时候。*

```
children's picture book illustration, colored pencil drawing, warm sandy palette with soft coral accents, visible pencil strokes and gentle cross-hatching, soft daylight, A hermit crab in mid movement between an old shell and a new bigger shell on the sand, a quick hurried moment, soft motion lines, warm sand background.
```

### page_09　seed 5009　不挂 LoRA

*旁白：有时候， / 好几只寄居蟹排成一队。 / 大的换了新壳， / 旧壳就留给小的。 / 一个传一个，谁都有房子。*

```
children's picture book illustration, colored pencil drawing, warm sandy palette with soft coral accents, visible pencil strokes and gentle cross-hatching, soft daylight, Several hermit crabs of different sizes lined up in a neat row on the sand from biggest to smallest, each next to a shell, shells being passed along the line, sunny and orderly, charming.
```

### page_10　seed 5010　带 LoRA

*旁白：我把捡到的空壳， / 又放回沙滩上。 / 说不定有一只寄居蟹， / 正在到处找房子呢。*

```
ohwx boy, wearing a pale yellow t-shirt and orange shorts, bare feet, short black hair, children's picture book illustration, colored pencil drawing, warm sandy palette with soft coral accents, visible pencil strokes and gentle cross-hatching, soft daylight, A little boy crouching on the sand carefully placing an empty spiral shell back down on the beach, sea in the background, warm afternoon light.
```

---

## 《晚上，地球转过去了》 — `night.zip`

> 太阳没有走，是我们转过去了　·　画风：夜色粉彩　·　种子：6000 + 页码　·　带 LoRA 的页：1, 7, 9, 10

**附加负面词**：`harsh light, daytime, bright saturated colors, scary darkness`

### page_01　seed 6001　带 LoRA

*旁白：天黑了，该睡觉了。 / 我趴在窗台上问： / 「太阳去哪里了？」*

```
ohwx boy, wearing light blue pajamas with a small star pattern, bare feet, short black hair, children's picture book illustration, soft chalk pastel painting, deep indigo night and warm cream palette, gentle grain, quiet glowing light, A little boy in pajamas kneeling at a bedroom window at night looking out at a deep blue sky, a small bedside lamp glowing warm behind him, cozy quiet room.
```

### page_02　seed 6002　不挂 LoRA

*旁白：太阳没有去哪里。 / 它一直在那儿， / 一直亮着， / 从来没有关过。*

```
children's picture book illustration, soft chalk pastel painting, deep indigo night and warm cream palette, gentle grain, quiet glowing light, The sun shining steadily and calmly in deep space against a dark starry background, warm and quiet, gentle glow, not fiery or frightening.
```

### page_03　seed 6003　不挂 LoRA

*旁白：是我们—— / 慢慢地， / 转过去了。*

```
children's picture book illustration, soft chalk pastel painting, deep indigo night and warm cream palette, gentle grain, quiet glowing light, The Earth as a blue and green ball floating in dark space, one half lit by warm sunlight from the side, the other half in soft shadow, calm and gentle.
```

### page_04　seed 6004　不挂 LoRA

*旁白：我们住的地球， / 是一个很大很大的球。 / 它一直在「转」。 / 转一圈，就是一天。*

```
children's picture book illustration, soft chalk pastel painting, deep indigo night and warm cream palette, gentle grain, quiet glowing light, The Earth turning slowly in dark space with a soft curved arrow drawn around it showing the spin, stars behind, calm night colours, picture book style.
```

### page_05　seed 6005　不挂 LoRA

*旁白：转到有太阳的那一面—— / 就是白天。 / 转到背着太阳的那一面—— / 就是晚上。*

```
children's picture book illustration, soft chalk pastel painting, deep indigo night and warm cream palette, gentle grain, quiet glowing light, One round Earth in space: on the sunlit side a small town in daylight, on the shadowed side a similar town at night with warm lit windows, the line between them soft and gradual.
```

### page_06　seed 6006　不挂 LoRA

*旁白：现在我们这边是晚上。 / 地球的另外一边， / 有小朋友正在吃早饭呢。*

```
children's picture book illustration, soft chalk pastel painting, deep indigo night and warm cream palette, gentle grain, quiet glowing light, Two children drawn small on the curve of the round Earth on opposite sides: one asleep in bed on the night side, one eating breakfast at a sunlit table on the day side, stars around the planet.
```

### page_07　seed 6007　带 LoRA

*旁白：你睡觉的时候， / 地球也在转。 / 轻轻地，稳稳地， / 一点声音都没有。*

```
ohwx boy, wearing light blue pajamas with a small star pattern, bare feet, short black hair, children's picture book illustration, soft chalk pastel painting, deep indigo night and warm cream palette, gentle grain, quiet glowing light, A little boy asleep in bed seen from above, moonlight falling across the blanket, everything very still and quiet, deep blue and cream tones.
```

### page_08　seed 6008　不挂 LoRA

*旁白：转啊转， / 天边慢慢变亮了。 / 那不是太阳升起来， / 是我们转回来了。*

```
children's picture book illustration, soft chalk pastel painting, deep indigo night and warm cream palette, gentle grain, quiet glowing light, The curved horizon of the Earth seen from a little way above, the dark side slowly coming into light, a thin warm band of dawn along the curve, stars fading softly.
```

### page_09　seed 6009　带 LoRA

*旁白：早上， / 第一缕光照在窗帘上。 / 我们又转到太阳这边了。*

```
ohwx boy, wearing light blue pajamas with a small star pattern, bare feet, short black hair, children's picture book illustration, soft chalk pastel painting, deep indigo night and warm cream palette, gentle grain, quiet glowing light, Warm morning light falling across a curtain in a child's bedroom, a little boy in pajamas just waking up, one bare foot out from under the blanket, soft and quiet.
```

### page_10　seed 6010　带 LoRA

*旁白：所以「晚安」的意思是： / 我们转过去一会儿， / 明天， / 再转回来。*

```
ohwx boy, wearing light blue pajamas with a small star pattern, bare feet, short black hair, children's picture book illustration, soft chalk pastel painting, deep indigo night and warm cream palette, gentle grain, quiet glowing light, A little boy in pajamas lying in bed with his eyes closed and a small smile, the window behind him showing a night sky with a few stars, very peaceful, warm lamp light.
```

---

## 《我住在一颗星星旁边》 — `star.zip`

> 太阳也是一颗星星　·　画风：复古丝网印　·　种子：7000 + 页码　·　带 LoRA 的页：1, 2, 9, 10

**附加负面词**：`photorealistic, busy detail, harsh contrast`

### page_01　seed 7001　带 LoRA

*旁白：晚上，我躺在草地上看天。 / 星星好多好多， / 小小的，一闪一闪。*

```
ohwx boy, wearing a dark blue long sleeve shirt and grey trousers, short black hair, children's picture book illustration, retro screenprint poster style, limited palette of deep navy teal and warm orange, flat simple shapes, subtle paper grain, A little boy lying on his back on grass at night looking up, seen from above, the whole sky above him filled with small stars, deep navy tones, flat graphic style.
```

### page_02　seed 7002　带 LoRA

*旁白：我说：「星星好小。」 / 爸爸说： / 「不是小。 / 是远。」*

```
ohwx boy, wearing a dark blue long sleeve shirt and grey trousers, short black hair, children's picture book illustration, retro screenprint poster style, limited palette of deep navy teal and warm orange, flat simple shapes, subtle paper grain, A little boy and his father lying side by side on grass at night, both pointing up at the stars, drawn small inside a large starry frame.
```

### page_03　seed 7003　不挂 LoRA

*旁白：星星其实很大很大。 / 大得像太阳一样。 / 因为太远太远了， / 看起来才只有一点点。*

```
children's picture book illustration, retro screenprint poster style, limited palette of deep navy teal and warm orange, flat simple shapes, subtle paper grain, A comparison picture: an enormous glowing star filling the left half of the frame, and the same star shown as a tiny dot far away on the right, dark sky between them, flat screenprint shapes.
```

### page_04　seed 7004　不挂 LoRA

*旁白：那太阳呢？ / 太阳也是一颗「星星」。 / 只是它离我们最近， / 所以又大又亮。*

```
children's picture book illustration, retro screenprint poster style, limited palette of deep navy teal and warm orange, flat simple shapes, subtle paper grain, The sun drawn as one star among many: a large warm glowing sun on one side and many smaller stars of the same kind scattered across the dark sky, simple flat shapes.
```

### page_05　seed 7005　不挂 LoRA

*旁白：白天的时候， / 星星还在天上吗？ / 在的。 / 只是太阳太亮了， / 把它们盖住了。*

```
children's picture book illustration, retro screenprint poster style, limited palette of deep navy teal and warm orange, flat simple shapes, subtle paper grain, A bright daytime sky over a simple field, with faint pale stars drawn very softly behind the daylight to show they are still there, limited flat palette.
```

### page_06　seed 7006　不挂 LoRA

*旁白：月亮不一样。 / 月亮自己不发光。 / 是太阳照亮了它， / 像照亮一面镜子。*

```
children's picture book illustration, retro screenprint poster style, limited palette of deep navy teal and warm orange, flat simple shapes, subtle paper grain, The moon in a dark sky with sunlight coming from one side lighting its face, the lit half bright warm orange and the other half soft shadow, flat graphic shapes.
```

### page_07　seed 7007　不挂 LoRA

*旁白：那我们呢？ / 我们住的地球， / 也在天上飞。 / 绕着太阳， / 一圈，又一圈。*

```
children's picture book illustration, retro screenprint poster style, limited palette of deep navy teal and warm orange, flat simple shapes, subtle paper grain, The Earth as a small blue ball travelling along a wide curved path around a warm glowing sun, dark space and scattered stars, simple poster composition.
```

### page_08　seed 7008　不挂 LoRA

*旁白：如果从很远的地方看， / 地球也只是一个小亮点。 / 小小的， / 蓝蓝的。*

```
children's picture book illustration, retro screenprint poster style, limited palette of deep navy teal and warm orange, flat simple shapes, subtle paper grain, The Earth seen from very far away as one small pale blue dot in dark empty space, tiny and quiet, a great deal of empty space around it.
```

### page_09　seed 7009　带 LoRA

*旁白：所以我不用坐火箭去太空。 / 我已经在太空里了。 / 我一直都在。*

```
ohwx boy, wearing a dark blue long sleeve shirt and grey trousers, short black hair, children's picture book illustration, retro screenprint poster style, limited palette of deep navy teal and warm orange, flat simple shapes, subtle paper grain, A little boy standing on grass at night with his arms out, the ground beneath him curving away like the surface of a planet, stars all around him, flat graphic style.
```

### page_10　seed 7010　带 LoRA

*旁白：我躺在草地上， / 抱着这颗会飞的大球， / 和满天的星星一起， / 转啊，转啊。*

```
ohwx boy, wearing a dark blue long sleeve shirt and grey trousers, short black hair, children's picture book illustration, retro screenprint poster style, limited palette of deep navy teal and warm orange, flat simple shapes, subtle paper grain, A little boy lying on grass at night seen from directly above with arms spread, boy and grass small at the centre of a huge sky full of stars, calm and wide.
```

---

## 《种子去旅行》 — `seed.zip`

> 它们不会走路，可是哪儿都去过　·　画风：剪纸拼贴　·　种子：8000 + 页码　·　带 LoRA 的页：10

**附加负面词**：`photorealistic, glossy, harsh outlines`

### page_01　seed 8001　不挂 LoRA

*旁白：大树站在那里， / 一辈子都不动。*

```
children's picture book illustration, cut paper collage, textured handmade paper, warm earth tones with fresh green, layered flat shapes, soft daylight, A single very large old tree standing alone in a wide open field, deep roots, completely still, soft daylight, plenty of empty space around it, cut paper collage style.
```

### page_02　seed 8002　不挂 LoRA

*旁白：可是它的小树， / 长到了很远很远的地方。 / 它们是怎么去的呢？*

```
children's picture book illustration, cut paper collage, textured handmade paper, warm earth tones with fresh green, layered flat shapes, soft daylight, The same wide field with several small young trees growing far away from the big old tree, showing the long distance between them, layered paper shapes.
```

### page_03　seed 8003　不挂 LoRA

*旁白：蒲公英的「种子」 / 有一把小伞。 / 风一吹—— / 呼，飞走了。*

```
children's picture book illustration, cut paper collage, textured handmade paper, warm earth tones with fresh green, layered flat shapes, soft daylight, A dandelion seed head with several seeds lifting off in the wind, each seed carrying a small white parachute, floating across a pale sky, cut paper collage.
```

### page_04　seed 8004　不挂 LoRA

*旁白：枫树的种子 / 有两片翅膀。 / 掉下来的时候， / 转啊转， / 像小螺旋桨。*

```
children's picture book illustration, cut paper collage, textured handmade paper, warm earth tones with fresh green, layered flat shapes, soft daylight, Two winged maple seeds spinning down through the air like little propellers, motion shown with soft curved paper lines, warm autumn colours.
```

### page_05　seed 8005　不挂 LoRA

*旁白：苍耳的种子 / 全身都是小钩子。 / 它钩住小狗的毛， / 搭了一段顺风车。*

```
children's picture book illustration, cut paper collage, textured handmade paper, warm earth tones with fresh green, layered flat shapes, soft daylight, Close up of a dog's furry leg with several small hooked burr seeds stuck in the hair, the dog walking through tall grass, collage textures.
```

### page_06　seed 8006　不挂 LoRA

*旁白：还有的种子藏在果子里。 / 小鸟把果子吃掉， / 飞到很远的地方， / 种子就跟着搬了家。*

```
children's picture book illustration, cut paper collage, textured handmade paper, warm earth tones with fresh green, layered flat shapes, soft daylight, A small bird holding a red berry in its beak on a branch, and further away in the distance the same bird flying over a wide field, layered paper landscape.
```

### page_07　seed 8007　不挂 LoRA

*旁白：椰子最厉害。 / 它掉进海里， / 漂啊漂，漂过一整片大海， / 在另一个岛上发芽。*

```
children's picture book illustration, cut paper collage, textured handmade paper, warm earth tones with fresh green, layered flat shapes, soft daylight, A coconut floating on the surface of a calm sea, drifting along, a small green island in the distance, flat collage waves.
```

### page_08　seed 8008　不挂 LoRA

*旁白：有的种子会自己弹。 / 果荚晒干了， / 啪的一声裂开， / 把种子弹得远远的。*

```
children's picture book illustration, cut paper collage, textured handmade paper, warm earth tones with fresh green, layered flat shapes, soft daylight, A dry seed pod splitting open with a snap, small seeds flying outward in several directions, short motion lines, warm paper textures.
```

### page_09　seed 8009　不挂 LoRA

*旁白：种子不会走路。 / 可是风会带它， / 水会送它， / 小鸟和小狗 / 会捎上它。*

```
children's picture book illustration, cut paper collage, textured handmade paper, warm earth tones with fresh green, layered flat shapes, soft daylight, One small seed at the centre of the picture with the wind, a stream of water, a bird and a dog arranged gently around it in a ring, all helping it travel, symmetrical collage composition.
```

### page_10　seed 8010　带 LoRA

*旁白：我口袋里有一颗种子， / 是刚才在路上捡的。 / 我把它种在院子里。 / 这一次—— / 是我帮它。*

```
ohwx boy, wearing a mustard yellow t-shirt and brown corduroy overalls, red sneakers, short black hair, children's picture book illustration, cut paper collage, textured handmade paper, warm earth tones with fresh green, layered flat shapes, soft daylight, A little boy crouching in a garden pressing a single seed into the soil with one finger, a small watering can beside him, warm afternoon light, cut paper collage.
```

---
