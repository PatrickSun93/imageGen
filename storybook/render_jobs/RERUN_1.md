# 重跑清单（8 页）— 等用户说「开始」再跑

四本书整体都能用，下面这 8 页有硬问题。**每段提示词整段复制替换**，
不要再拼 style。种子建议换成原种子 +100（避免复现同样的构图）。

通用负面词照旧，另外**每页有附加负面词**，追加在后面。
（Windows 端备注：CFG 1.0 下 Flux dev 不跑负面分支，负面词只作记录，靠正面描述修。）

---

## 《晚上，地球转过去了》night

### page_02　不挂 LoRA　seed 6102
**问题**：太阳画对了，但左下角山坡上多了一个扎马尾的小孩剪影。这页不该有人。

```
children's picture book illustration, soft chalk pastel painting, deep indigo night and warm cream palette, gentle grain, quiet glowing light, An enormous warm golden sun filling most of the frame, radiating soft light rays outward in all directions, smooth even glowing surface with no craters and no dark spots, seen close up in open space, nothing else in the picture
```
附加负面：`person, child, figure, silhouette, hill, ground, grass, horizon, landscape, moon, crater, signature, handwriting`

（Windows 端备注：已发过的 night_ALT_page_02_sun_only.png 已经没有人影，只剩底部很淡的山影，可能不必重跑。）

---

## 《海只来一点点》sea

### page_01　带 LoRA　seed 4101
**问题**：旁白是「我抓紧了爸爸的手」，但画面里他一个人站着，爸爸没出现。

```
ohwx boy, wearing a pale yellow t-shirt and orange shorts, bare feet, short black hair, children's picture book illustration, gentle watercolor painting, soft sea green and warm sand palette, loose wet washes, lots of white paper showing, calm soft daylight, the little boy standing on dry sand high up the beach beside his grown adult father, seen from behind, the boy holding his father's hand tightly, both facing a very wide calm sea, the two figures small in the lower part of the frame, wide open sky and sea above them
```
附加负面：`child alone, single figure, only one person, empty beach`

### page_04　不挂 LoRA　seed 4104
**问题**：画面七成是空白，底部三条浪痕是直线，看起来像没画完，不像沙滩。

```
children's picture book illustration, gentle watercolor painting, soft sea green and warm sand palette, loose wet washes, calm soft daylight, A stretch of wet sandy beach seen at a low angle, three soft curved lines of white foam left behind on the sand at the same distance from the viewer, the calm sea and a low horizon in the upper third of the picture, a few small pebbles, complete and balanced composition
```
附加负面：`empty white space, blank page, unfinished, straight lines, geometric shapes, steps`

---

## 《我住在一颗星星旁边》star

### page_05　不挂 LoRA　seed 7105
**问题**：旁白是「白天的时候，星星还在天上吗？在的」，画面却是傍晚的橘色地平线，一颗星星都没有，右边还多了个人影。

```
children's picture book illustration, retro screenprint poster style, limited palette of deep navy teal and warm orange, flat simple shapes, subtle paper grain, A bright blue daytime sky in full midday daylight above a simple green field, the sun high and warm, and a scattering of very faint pale stars still drawn softly across the blue daytime sky to show that they are still there
```
附加负面：`sunset, dusk, twilight, evening, night, dark sky, orange horizon, silhouette, person, figure`

### page_06　不挂 LoRA　seed 7106
**问题**：月亮画了一张卡通脸。这页讲「月亮不发光，是被太阳照亮的」，是物理解释。

```
children's picture book illustration, retro screenprint poster style, limited palette of deep navy teal and warm orange, flat simple shapes, subtle paper grain, The moon alone in a dark night sky, sunlight arriving from one side so that half of its surface is bright and the other half falls into soft shadow, a plain round moon with a few simple craters, several small stars around it
```
附加负面：`face, eyes, eyelashes, mouth, nose, smiling moon, man in the moon, cartoon character, anthropomorphic`

### page_07　不挂 LoRA　seed 7107
**问题**：地球又长出了行星环，轨道被画成实心缎带，地球和太阳之间还连了一根棍子。

```
children's picture book illustration, retro screenprint poster style, limited palette of deep navy teal and warm orange, flat simple shapes, subtle paper grain, A warm orange sun at the centre of the picture and a small blue Earth further out to one side, with a simple thin dotted oval line drawn around the sun to show the path the Earth travels along, dark space and a few small stars
```
附加负面：`rings around planet, ringed planet, saturn, ribbon, road, band, thick solid curve, stick, connecting rod, straight line between objects`

---

## 《寄居蟹换了新房子》crab

### page_03　带 LoRA　seed 5103
**问题**：「爸爸」画成了少年，穿着和他一模一样；旁边的小孩反而穿白上衣，像两兄弟。

```
ohwx boy, wearing a pale yellow t-shirt and orange shorts, bare feet, short black hair, children's picture book illustration, colored pencil drawing, warm sandy palette with soft coral accents, visible pencil strokes and gentle cross-hatching, soft daylight, the little boy crouching on the sand beside a grown adult man who is clearly his father, the man has an adult face and adult build and is much larger than the child, wearing a light blue shirt and khaki shorts, both looking down at a hermit crab in a spiral shell resting on the boy's small palm
```
附加负面：`two children, two boys, teenager, older brother, twins, same clothes on both figures, identical characters`

### page_06　不挂 LoRA　seed 5106
**问题**：旁白是「壳太小了」，画面里的壳却明显偏大。

```
children's picture book illustration, colored pencil drawing, warm sandy palette with soft coral accents, visible pencil strokes and gentle cross-hatching, soft daylight, A hermit crab that has grown much too big for its shell, the shell is clearly too small and the crab's body bulges out of the opening and cannot fit back inside, the crab looks uncomfortable and a little worried, sitting on plain sand
```
附加负面：`large shell, big shell, roomy shell, crab hidden inside shell, shell bigger than crab`

---

## 可改可不改（Windows 端定）

- sea page_09：左上角有一块比较大的空白，能接受。
- star page_04：小星星画成卡通五角星，太阳是圆盘，类比稍弱。
- crab page_04：壳画成扇贝帽子，跟其余各页的螺旋壳不一致。
- night page_06：两个小孩是棕发西方小孩。（已试过黑发替代版，构图变差，建议保留原版。）

## Mac 端本地处理，不用重跑

crab/page_02 和 night/page_05 右下角的手写签名。

## 还没开始的书

seed（种子去旅行）一页都没跑，也等用户说启动。
