# 第七批 40 本：停在哪儿，下次从哪儿接

停于 2026-09-17 11:10。ComfyUI 已停，出图进程已停，代码全部提交（本地领先 origin 68 个提交，**未推送**）。

## 一句话状态

**图全出齐了（481/481），40 本网页全部打包好了，但只发布了 11 本。**
审图查出约 190 页图文对不上，用户定的方针是**只修硬伤、先发布**；硬伤已经修完一轮，
剩下发布和一轮收尾没做。

## 下次接着做的四件事

```bat
REM 0. 先把 ComfyUI 起回来（只有第 1 步需要 GPU）
cd C:\FlowDev\githubdevitems\comfyUIItems
venv\python.exe main.py --listen 127.0.0.1 --port 8188
```

1. **补出 4 张图**（约 10 分钟 GPU）。清单已经写好在 scratchpad：
   - `fix_boy.txt` —— giraffe p1 / owl p1 / whale p12。前者是「竖幅图被补成正方形，
     左右各贴一条模糊放大的自身填充带」，后两者右上角有灰色乱码水印。**这 3 张我已经
     把旧图放回去了**（所以现在不缺页），重出后会覆盖。
     `venv\python.exe storybook\edit_qwen.py --v2 --unet=qwen-image-edit-2511-Q3_K_M.gguf <照片1> <照片2> storybook/story_giraffe.json:1 storybook/story_owl.json:1 storybook/story_whale.json:12`
   - `fix_assets2.txt` —— cloud 素材 8（雨滴）。提示已改好（原来的
     "falling raindrop" 把整片雨天招来了，抠图抠不掉）。
     `venv\python.exe storybook\bakeoff_qwen.py lightning8 storybook/story_assets_cloud.json:8`

2. **重画 217 页 + 重打包**（不用 GPU，两三分钟）：
   ```
   cd storybook
   ..\venv\python.exe draw_diagrams.py stego ankylo claws tails fingers aircell mother herd dinosleep fight dinoswim tiny feather sail climb eras oldworld california firstfind dinonames cloud fog hail tornado forecast dew whisker dognose squirrel bat octopus penguin camel snake tadpole seaturtle owl whale spider giraffe
   ```
   然后每本跑 `pack_images.py out/<slug>_qwen out/web_<slug>`，再
   `build_web.py story_<slug>.json out/web_<slug> > out/web_<slug>/index.html`。
   **注意工作目录必须是 storybook**——这两个脚本的相对路径是相对它的，
   在仓库根目录跑会打出 320 字节的空壳（踩过一次）。

3. **发布剩下 29 本**，并把 11 本已发的重新发布一遍（修过的页要更新，链接不变）。
   已发的 11 个链接记在记忆的 `book-artifact-links.md` 里。

4. **书架更新到 119 本**：`scratchpad/shelf7.py` 已经写好（40 本分九组），
   把发布拿到的链接填进它的 `LINKS` 再跑一遍，然后发布 `scratchpad/workshop.html`
   到书架那个 artifact（18d50822）。

## 已经修掉的（这一轮）

- **11 个坏素材**重出。杠杆最大的一类：一张坏图连累好几页（长颈鹿那块颈椎骨画坏了，
  p4 和 p5 十四块骨头全长着鹿头）。
- **9 张画错的模型场景页**重出：爱心里坐着狮子的「心脏」、长出人拳头的冰雹、
  长着青蛙脸的卵块、被画成「一本摊开的书的照片」的三页、正好画成海豚的鱼龙
  （而旁白说「它不是海豚」）。
- **9 页程序画的硬伤**改代码：猫胡须那两页（一页两根尺量的是同一个外框、一页叉号反了）、
  冷暖上下画反的冰雹页、整页跑题的雾页、漏斗悬空的龙卷风页、画错内容的章鱼页、
  蜘蛛踩在粘丝上的那页。

## 还没修的（用户说先留着，等他翻过书再定）

约 130 页，集中在两类：
- **旁白点名的对比物没画**：「和柚子差不多大」没画柚子、「像汽车前面的水箱」没画汽车、
  「有我的胳膊那么长」没画胳膊。同一条管线是支持画对比物的（西瓜、核桃、脸盆都画出来了），
  只是漏了一半。
- **动作不到位**：「跳下来」画成还站着、「把翅膀盖下去」画成翅膀收在背上、
  「趴在窝上」画成直着腿站在蛋上。

四份逐页审图报告在会话记录里，没有单独存文件。

## 这一批最值得记的一条

**提示里的每个名词都会被画出来。** 一晚上栽了五次，每次是同一个毛病的不同面孔：

| 写了什么 | 画出来什么 |
|---|---|
| `belly scale **of a snake**`（部件） | 一整条盘起来的蛇 |
| `neck bone **of a giraffe**`（所属） | 骨头右端长出一个长颈鹿的头 |
| `wide and flat **like a leaf**`（比喻） | 一片叶子 |
| `about the size of a **big dog**`（比喻） | 一条狗 |
| `as big as a **fist**`（比喻） | 冰雹里长出一只人的拳头 |
| `a tall **sail**`（一词多义） | 带桅杆缆绳的船帆 |
| `resting **on the ground**`（位置） | 一整片地面（抠图抠不掉） |

想要一个孤零零的物体，就一个多余的名词都不能提；不想要的东西要**正面否掉**
（not a ship / not a leaf / no animal in the picture），写 "no X" 比不提 X 更管用。

另外两条：
- **「脸要大」是形容词，模型不当回事；「身子在画面外」是构图指令，它照办。**
  人物页 80 张就是这么从「脸占不到一成」提到「占两成半」的。
- **画不下的时候要改取景，不是把东西缩小到看不清。** 蜘蛛那页整张网的尺度下
  相邻粘丝只隔 39px，塞不进 205px 的蜘蛛，硬塞的结果是蜘蛛骑在粘丝上——
  正好打脸那页旁白。改成画网的一小块放大就成立了。
