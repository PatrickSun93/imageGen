#!/usr/bin/env python3
"""图层合成：把抠好的人物贴进场景图，再交给 ComfyUI 低 denoise 融合。

用法:
  python3 compose.py cutout          # 把 actors/*.png 抠成透明底
  python3 compose.py place <场景图> <姿势> <x%> <y%> <高度%> <输出>
"""
import sys, os, glob
from PIL import Image

ROOT = "/Volumes/externalssd/devitems/learning/imageGen"
ACT  = f"{ROOT}/storybook/actors"

def cutout():
    from rembg import remove, new_session
    os.makedirs(f"{ACT}/cut", exist_ok=True)
    sess = new_session("isnet-general-use")   # 对插画比默认 u2net 干净
    for p in sorted(glob.glob(f"{ROOT}/ComfyUI/output/actors2/*.png")):
        name = os.path.basename(p).split("_")[0]
        im = Image.open(p).convert("RGBA")
        out = remove(im, session=sess, post_process_mask=True)
        # 裁掉全透明的边，只留人物外接框
        bbox = out.getbbox()
        if bbox: out = out.crop(bbox)
        dst = f"{ACT}/cut/{name}.png"
        out.save(dst)
        print(f"  {name:6s} {out.size[0]}x{out.size[1]}  → {dst}")

def place(scene, pose, xp, yp, hp, dst):
    """xp/yp = 人物中心在画面的百分比位置, hp = 人物高度占画面百分比"""
    bg = Image.open(scene).convert("RGBA")
    fg = Image.open(f"{ACT}/cut/{pose}.png").convert("RGBA")
    W, H = bg.size
    th = int(H * float(hp) / 100)
    tw = int(fg.size[0] * th / fg.size[1])
    fg = fg.resize((tw, th), Image.LANCZOS)
    x = int(W * float(xp) / 100) - tw // 2
    y = int(H * float(yp) / 100) - th // 2
    # 脚下加一团柔和阴影，避免"漂浮贴纸"感
    sh = Image.new("RGBA", bg.size, (0,0,0,0))
    from PIL import ImageDraw, ImageFilter
    d = ImageDraw.Draw(sh)
    d.ellipse([x + tw*0.12, y + th*0.94, x + tw*0.88, y + th*1.04], fill=(40,30,20,90))
    sh = sh.filter(ImageFilter.GaussianBlur(th*0.02))
    bg = Image.alpha_composite(bg, sh)
    bg.paste(fg, (x, y), fg)
    bg.convert("RGB").save(dst)
    print(f"  合成 → {dst}  人物 {tw}x{th} @ ({x},{y})")

if __name__ == "__main__":
    if sys.argv[1] == "cutout": cutout()
    elif sys.argv[1] == "place": place(*sys.argv[2:])

def swap_head(pose):
    """把高清头部贴回立绘：检测两边的脸框，按比例对齐替换。"""
    from ultralytics import YOLO
    from PIL import ImageFilter
    ROOT="/Volumes/externalssd/devitems/learning/imageGen"
    det=YOLO(f"{ROOT}/ComfyUI/models/ultralytics/bbox/face_yolov8m.pt")
    def facebox(im):
        r=det(im, verbose=False)[0]
        if len(r.boxes)==0: return None
        b=max(r.boxes,key=lambda b:(b.xyxy[0][2]-b.xyxy[0][0])*(b.xyxy[0][3]-b.xyxy[0][1]))
        return [float(v) for v in b.xyxy[0]]

    body=Image.open(f"{ACT}/cut/{pose}.png").convert("RGBA")
    head=Image.open(sorted(glob.glob(f"{ROOT}/ComfyUI/output/heads/{pose}_*.png"))[-1]).convert("RGB")
    bb, hb = facebox(body.convert("RGB")), facebox(head)
    if not bb or not hb:
        print(f"  {pose}: 没检测到脸，跳过"); return
    # 高清头按立绘脸的大小缩放，多留 60% 边把头发和下巴带上
    bw,bh = bb[2]-bb[0], bb[3]-bb[1]
    hw,hh = hb[2]-hb[0], hb[3]-hb[1]
    m=0.6
    crop=(max(0,hb[0]-hw*m), max(0,hb[1]-hh*m*1.2),
          min(head.width,hb[2]+hw*m), min(head.height,hb[3]+hh*m))
    piece=head.crop(crop)
    scale=bw/hw
    nw,nh=int(piece.width*scale), int(piece.height*scale)
    piece=piece.resize((nw,nh), Image.LANCZOS).convert("RGBA")
    # 椭圆羽化遮罩，避免硬边
    mask=Image.new("L",(nw,nh),0)
    ImageDraw.Draw(mask).ellipse([nw*0.06,nh*0.04,nw*0.94,nh*0.96],fill=255)
    mask=mask.filter(ImageFilter.GaussianBlur(nw*0.05))
    px=int(bb[0]-(hb[0]-crop[0])*scale); py=int(bb[1]-(hb[1]-crop[1])*scale)
    out=body.copy(); out.paste(piece,(px,py),mask)
    out.save(f"{ACT}/cut/{pose}.png")
    print(f"  {pose:6s} 脸 {int(bw)}px → {int(hw*scale)}px（源 {int(hw)}px）")
