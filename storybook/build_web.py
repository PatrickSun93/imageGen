#!/usr/bin/env python3
"""把 story JSON + 压好的 base64 图合成一个可翻页的绘本网页。
用法: python3 build_web.py story_ants.json web_ants "蜡笔" > web_ants/index.html
"""
import json, sys

sys.stdout.reconfigure(encoding="utf-8")   # Windows would write the redirected HTML as cp1252
story_path, webdir = sys.argv[1], sys.argv[2]
story = json.load(open(story_path, encoding="utf-8"))
imgs  = json.load(open(f"{webdir}/images_b64.json"))
PAL   = story.get("palette", {})

# 每本书一套配色，从故事本身取
ink   = PAL.get("ink","#22392e");   ink_d  = PAL.get("ink_d","#e6ece2")
soft  = PAL.get("soft","#5c6f62");  soft_d = PAL.get("soft_d","#a4b3a6")
grd   = PAL.get("ground","#eef1e7");grd_d  = PAL.get("ground_d","#141a16")
ppr   = PAL.get("paper","#fbfaf5"); ppr_d  = PAL.get("paper_d","#1d2620")
acc   = PAL.get("accent","#c1503a");acc_d  = PAL.get("accent_d","#e07a63")
bark  = PAL.get("bark","#8a7860");  bark_d = PAL.get("bark_d","#9d8c74")
line  = PAL.get("line","#d5dbcd");  line_d = PAL.get("line_d","#2f3b33")
KEY   = story.get("keyword")

pages=[]
for p in story["pages"]:
    body = "".join(f"<p>{l}</p>" for l in p["zh"].split("\n"))
    if KEY: body = body.replace(f"「{KEY}」", f'<em class="key">{KEY}</em>')
    pages.append(f'''<article class="spread" data-page="{p["n"]}"{" hidden" if p["n"]!=1 else ""}>
  <figure class="plate"><img src="data:image/jpeg;base64,{imgs[str(p["n"])]}" alt="第 {p["n"]} 页插图"></figure>
  <div class="prose"><span class="folio">{p["n"]}</span>{body}</div>
</article>''')

facts = "".join(f'<div class="fact"><dt>{k}</dt><dd>{v}</dd></div>' for k,v in story.get("facts",[]))
# 知识卡默认不显示：孩子只看图、听大人念，要讲的道理写进每页旁白里（2026-09-11 用户反馈）；想要就在 story 里加 "show_facts": true
facts_block = f'<section class="after"><h2>{story.get("facts_title","知识卡")}</h2><dl class="facts">{facts}</dl></section>' if facts and story.get("show_facts") else ""

print(f'''<title>{story["title"]}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;700&display=swap">
<style>
:root {{ --ink:{ink}; --ink-soft:{soft}; --ground:{grd}; --paper:{ppr};
  --bloom:{acc}; --bark:{bark}; --line:{line}; --shadow:rgba(34,57,46,.13); }}
@media (prefers-color-scheme:dark) {{ :root:not([data-theme="light"]) {{
  --ink:{ink_d}; --ink-soft:{soft_d}; --ground:{grd_d}; --paper:{ppr_d};
  --bloom:{acc_d}; --bark:{bark_d}; --line:{line_d}; --shadow:rgba(0,0,0,.45); }} }}
:root[data-theme="dark"] {{ --ink:{ink_d}; --ink-soft:{soft_d}; --ground:{grd_d}; --paper:{ppr_d};
  --bloom:{acc_d}; --bark:{bark_d}; --line:{line_d}; --shadow:rgba(0,0,0,.45); }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--ground); color:var(--ink);
  font-family:"Noto Serif SC",Songti SC,serif; min-height:100vh;
  display:flex; flex-direction:column; align-items:center; padding:24px 16px 32px; gap:20px; }}
header {{ text-align:center; }}
h1 {{ margin:0; font-size:clamp(22px,4.5vw,32px); font-weight:700; letter-spacing:.06em; }}
.sub {{ margin:6px 0 0; color:var(--ink-soft); font-size:14px; letter-spacing:.14em; }}
.book {{ width:min(1040px,100%); }}
.spread {{ display:grid; grid-template-columns:1fr; background:var(--paper);
  border:1px solid var(--line); border-radius:3px; overflow:hidden; box-shadow:0 12px 34px var(--shadow); }}
@media (min-width:820px) {{ .spread {{ grid-template-columns:1.05fr .95fr; }} }}
.spread[hidden] {{ display:none; }}   /* display:grid above would otherwise beat the hidden attribute when opened locally */
.plate {{ margin:0; background:var(--paper); }}
.plate img {{ display:block; width:100%; height:auto; }}
.prose {{ padding:clamp(24px,4vw,52px); display:flex; flex-direction:column;
  justify-content:center; gap:.7em; border-top:1px solid var(--line); }}
@media (min-width:820px) {{ .prose {{ border-top:0; border-left:1px solid var(--line); }} }}
.prose p {{ margin:0; font-size:clamp(17px,2vw,21px); line-height:1.95; letter-spacing:.02em; }}
.folio {{ font-size:12px; letter-spacing:.3em; color:var(--bark);
  font-variant-numeric:tabular-nums; margin-bottom:.9em; }}
.prose p:has(+ p) {{ }}\n.key {{ font-style:normal; font-weight:700; color:var(--bloom);
  box-shadow:inset 0 -.45em 0 color-mix(in srgb,var(--bloom) 16%,transparent); }}
nav {{ display:flex; align-items:center; gap:18px; }}
button {{ font:inherit; font-size:15px; color:var(--ink); background:var(--paper);
  border:1px solid var(--line); border-radius:2px; padding:9px 20px; cursor:pointer;
  transition:border-color .18s,color .18s; }}
button:hover:not(:disabled) {{ border-color:var(--bloom); color:var(--bloom); }}
button:disabled {{ opacity:.32; cursor:default; }}
button:focus-visible {{ outline:2px solid var(--bloom); outline-offset:2px; }}
.count {{ font-size:13px; letter-spacing:.22em; color:var(--ink-soft); font-variant-numeric:tabular-nums; }}
.after {{ width:min(1040px,100%); }}
.after h2 {{ font-size:13px; letter-spacing:.28em; color:var(--bark); font-weight:500; margin:0 0 14px; }}
.facts {{ display:grid; gap:1px; background:var(--line); border:1px solid var(--line); border-radius:3px; }}
@media (min-width:640px) {{ .facts {{ grid-template-columns:1fr 1fr; }} }}
.fact {{ background:var(--paper); padding:15px 20px; display:flex; flex-direction:column; gap:5px; }}
.fact dt {{ font-size:12px; letter-spacing:.16em; color:var(--ink-soft); }}
.fact dd {{ margin:0; font-size:17px; }}
footer {{ color:var(--ink-soft); font-size:12px; letter-spacing:.1em; text-align:center; }}
@media (prefers-reduced-motion:reduce) {{ * {{ transition:none !important; }} }}
</style>
<header><h1>{story["title"]}</h1><p class="sub">{story.get("subtitle","")}</p></header>
<main class="book">{"".join(pages)}</main>
<nav><button id="prev" disabled>← 上一页</button>
<span class="count"><span id="cur">1</span> / {len(story["pages"])}</span>
<button id="next">下一页 →</button></nav>
{facts_block}
<footer>用左右方向键也可以翻页</footer>
<script>
const pages=[...document.querySelectorAll(".spread")];
const prev=document.getElementById("prev"),next=document.getElementById("next"),cur=document.getElementById("cur");
let i=0;
function show(n){{ i=Math.max(0,Math.min(pages.length-1,n));
  pages.forEach((p,k)=>p.hidden=(k!==i)); cur.textContent=i+1;
  prev.disabled=(i===0); next.disabled=(i===pages.length-1);
  document.querySelector(".book").scrollIntoView({{behavior:"smooth",block:"nearest"}}); }}
prev.onclick=()=>show(i-1); next.onclick=()=>show(i+1);
addEventListener("keydown",e=>{{ if(e.key==="ArrowLeft")show(i-1);
  if(e.key==="ArrowRight"||e.key===" "){{e.preventDefault();show(i+1);}} }});
</script>''')
