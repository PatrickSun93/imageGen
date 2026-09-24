import sys
from PIL import Image
# args: out path, then items "folder/page:x0,y0,x1,y1" in fractions
out=sys.argv[1]; base='C:/FlowDev/githubdevitems/comfyUIItems/storybook/out/'
ims=[]
for a in sys.argv[2:]:
  p,b=a.split(':'); x0,y0,x1,y1=map(float,b.split(','))
  im=Image.open(base+p); W,H=im.size
  c=im.crop((int(x0*W),int(y0*H),int(x1*W),int(y1*H)))
  c=c.resize((1200,int(c.height*1200/c.width)),Image.LANCZOS); ims.append(c)
H=sum(i.height for i in ims)+10*len(ims)
o=Image.new('RGB',(1200,H),'white'); y=0
for i in ims: o.paste(i,(0,y)); y+=i.height+10
o.save(out,quality=88)
