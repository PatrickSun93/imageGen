import json, os, sys, base64, io
from PIL import Image

ROOT = r"C:\FlowDev\githubdevitems\comfyUIItems"

def b64jpeg(path, maxw=1080, q=84):
    im = Image.open(path).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
    return base64.b64encode(buf.getvalue()).decode(), buf.tell()

def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def main(story_path, out_html):
    st = json.load(open(story_path, encoding="utf-8"))
    outdir = os.path.join(ROOT, "storybook", "out", st["slug"] + "_lora")
    pages, total = [], 0
    for p in st["pages"]:
        f = os.path.join(outdir, f"page_{p['n']:02d}.png")
        data, n = b64jpeg(f); total += n
        zh = "<br>".join(esc(l) for l in p["zh"].split("\n"))
        pages.append(f"""
    <article class="pg">
      <figure><img src="data:image/jpeg;base64,{data}" alt="{esc(p['scene'][:110])}" loading="lazy" width="1080"></figure>
      <p class="zh">{zh}</p>
      <span class="num" aria-label="第 {p['n']} 页">{p['n']}</span>
    </article>""")
    dl, note = colophon(st)
    html = TEMPLATE.replace("{{TITLE}}", esc(st["title"])) \
                   .replace("{{SUB}}", esc(st["subtitle"])) \
                   .replace("{{STYLE_LABEL}}", esc(st["style_label"])) \
                   .replace("{{N}}", str(len(st["pages"]))) \
                   .replace("{{COLO}}", dl) \
                   .replace("{{NOTE}}", note) \
                   .replace("{{PAGES}}", "".join(pages))
    open(out_html, "w", encoding="utf-8").write(html)
    print(f"wrote {out_html}  images {total/1048576:.2f} MB  html {os.path.getsize(out_html)/1048576:.2f} MB")

def colophon(st):
    c = st["colophon"]
    # sampler settings come from the workflow the pages were rendered with
    wf = json.load(open(os.path.join(ROOT, st.get("workflow", "workflows/flux_dev_lora.json")), encoding="utf-8"))
    node = {v["class_type"]: v["inputs"] for v in wf.values()}
    ks, lat = node["KSampler"], node["EmptySD3LatentImage"]
    seed_base = st.get("seed_base", 2000)
    rows = [
        ("模型", esc(c["model"])),
        ("人物 LoRA", f'{esc(c["lora"])} · 强度 {c["strength"]}<br><span style="opacity:.7">'
                     f'{esc(c.get("lora_note", "触发词 ohwx boy，只挂在有人物的页"))}</span>'),
        ("采样", f'{ks["sampler_name"]} / {ks["scheduler"]} · {ks["steps"]} steps · CFG {ks["cfg"]}'
                f' · FluxGuidance {node["FluxGuidance"]["guidance"]}'),
        ("尺寸", f'{lat["width"]} × {lat["height"]}'),
        ("种子", ", ".join(str(seed_base + p["n"]) for p in st["pages"])
                + f'<br><span style="opacity:.7">({seed_base} + 页码，可复现)</span>'),
        ("画风词", esc(st["style"])),
    ]
    if "gpu" in c:
        rows.append(("显卡", esc(c["gpu"])))
    if "time" in c:
        rows.append(("耗时", "<br>".join(esc(l) for l in c["time"].split("\n"))))
    dl = "\n      ".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows)
    # note is the author's own HTML (it may carry <strong>), so it is not escaped
    note = f'\n    <p class="note">{c["note"]}</p>' if "note" in c else ""
    return dl, note

TEMPLATE = r"""<title>{{TITLE}}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=ZCOOL+KuaiLe&family=Noto+Sans+SC:wght@400;500;700&family=Space+Mono:wght@400;700&display=swap">
<style>
  :root{
    --paper:#FDFAF3; --panel:#FFFFFF; --ink:#23201C; --soft:#6E6659; --rule:#E6DDCA;
    --red:#E2402F; --blue:#2F6FB5; --green:#57A044; --yellow:#F2B705; --dirt:#C6873C;
    --shadow:0 10px 34px rgba(66,52,28,.13);
  }
  @media (prefers-color-scheme:dark){
    :root:not([data-theme="light"]){
      --paper:#171A1F; --panel:#1E222A; --ink:#F1ECE1; --soft:#A7A08F; --rule:#2F3540;
      --red:#FF6A57; --blue:#6DA8E8; --green:#7CC768; --yellow:#FFD24A; --dirt:#DDA363;
      --shadow:0 12px 36px rgba(0,0,0,.5);
    }
  }
  :root[data-theme="dark"]{
    --paper:#171A1F; --panel:#1E222A; --ink:#F1ECE1; --soft:#A7A08F; --rule:#2F3540;
    --red:#FF6A57; --blue:#6DA8E8; --green:#7CC768; --yellow:#FFD24A; --dirt:#DDA363;
    --shadow:0 12px 36px rgba(0,0,0,.5);
  }
  *{box-sizing:border-box}
  body{
    background:var(--paper); color:var(--ink);
    font-family:"Noto Sans SC","PingFang SC","Microsoft YaHei",system-ui,sans-serif;
    padding-inline:20px; padding-block:0;
  }
  .wrap{max-width:760px;margin:0 auto}

  /* cover */
  .cover{padding-block:56px 40px;text-align:center;position:relative}
  .crayons{display:flex;gap:6px;justify-content:center;margin-bottom:26px}
  .crayons i{display:block;width:34px;height:9px;border-radius:5px}
  h1{
    font-family:"ZCOOL KuaiLe",cursive; font-weight:400;
    font-size:clamp(2.6rem,10vw,4.1rem); line-height:1.12; margin:0;
    text-wrap:balance; letter-spacing:.02em;
  }
  .sub{font-size:1.05rem;color:var(--soft);margin:14px 0 0;letter-spacing:.06em}
  .meta{
    font-family:"Space Mono",ui-monospace,monospace; font-size:.72rem;
    color:var(--soft); letter-spacing:.13em; text-transform:uppercase; margin-top:26px;
  }

  /* pages */
  .pg{position:relative;margin-block:0 clamp(52px,9vw,84px)}
  figure{margin:0;border-radius:3px;overflow:hidden;box-shadow:var(--shadow);background:var(--panel)}
  img{display:block;width:100%;height:auto;max-width:100%}
  .zh{
    font-size:clamp(1.3rem,4.4vw,1.72rem); font-weight:700; line-height:1.95;
    text-align:center; margin:26px auto 0; max-width:24em; letter-spacing:.03em;
  }
  .num{
    position:absolute; top:-14px; left:-10px; z-index:2;
    width:46px;height:46px;display:grid;place-items:center;
    font-family:"ZCOOL KuaiLe",cursive; font-size:1.3rem; color:#fff;
    background:var(--red); border-radius:50% 48% 52% 50%;
    box-shadow:0 4px 12px rgba(0,0,0,.22);
  }
  .pg:nth-child(3n+2) .num{background:var(--blue)}
  .pg:nth-child(3n+3) .num{background:var(--green)}

  .end{
    font-family:"ZCOOL KuaiLe",cursive; font-size:2rem; text-align:center;
    color:var(--dirt); margin-block:8px 60px;
  }

  /* colophon */
  .colo{border-top:2px dashed var(--rule);padding-block:30px 70px}
  .colo h2{
    font-family:"Space Mono",monospace;font-size:.74rem;letter-spacing:.2em;
    text-transform:uppercase;color:var(--soft);margin:0 0 20px;font-weight:700;
  }
  dl{display:grid;grid-template-columns:auto 1fr;gap:11px 22px;margin:0;
     font-family:"Space Mono",ui-monospace,monospace;font-size:.79rem;line-height:1.65}
  dt{color:var(--soft);white-space:nowrap}
  dd{margin:0;word-break:break-word;font-variant-numeric:tabular-nums}
  .note{
    margin-top:26px;padding:15px 17px;border-left:3px solid var(--yellow);
    background:color-mix(in srgb,var(--yellow) 9%,transparent);
    font-size:.87rem;line-height:1.75;color:var(--soft);border-radius:0 4px 4px 0;
  }
  @media (max-width:430px){ dl{grid-template-columns:1fr;gap:3px 0} dt{margin-top:9px} }
</style>

<div class="wrap">
  <header class="cover">
    <div class="crayons" aria-hidden="true">
      <i style="background:var(--red)"></i><i style="background:var(--yellow)"></i>
      <i style="background:var(--green)"></i><i style="background:var(--blue)"></i>
      <i style="background:var(--dirt)"></i>
    </div>
    <h1>{{TITLE}}</h1>
    <p class="sub">{{SUB}}</p>
    <p class="meta">{{STYLE_LABEL}} · 共 {{N}} 页</p>
  </header>

  <main>{{PAGES}}
  </main>

  <p class="end">— 完 —</p>

  <section class="colo">
    <h2>制作配方 / Colophon</h2>
    <dl>
      {{COLO}}
    </dl>{{NOTE}}
  </section>
</div>
"""

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
