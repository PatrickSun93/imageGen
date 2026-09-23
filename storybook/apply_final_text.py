# -*- coding: utf-8 -*-
"""把 drafts/story_scripts_final.md（家长定稿的旁白）写回各本书。

搞笑系列 9 本：改 funny5.py 里每页的中文字符串（按书分块、按页顺序替换），再由 funny5.py 生成 story JSON；
最早 5 本：直接改 story_<slug>.json 的 zh。
「 / 」在定稿里是换行。
usage: apply_final_text.py [--dry]
"""
import io, json, os, re, sys

SB = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(SB, "drafts", "story_scripts_final.md")
TITLE = {"恐龙玩跷跷板": "seesaw", "恐龙想跟你玩": "dinowantsplay", "恐龙想加入": "dinojoin", "霸王龙输不起": "trexloses",
         "龙轮到了吗": "dragonturns", "恐龙第一天上学": "dinoschool", "霸王龙不想停": "trexwontstop",
         "恐龙爱泡泡浴": "dinobubbles", "龙最爱收袜子": "dragonsocks", "森林里最大的花": "rafflesia",
         "蚂蚁要搬家了": "ants", "恐龙没有走远": "dino", "海只来一点点": "sea", "寄居蟹换了新房子": "crab"}
EARLY = {"rafflesia", "ants", "dino", "sea", "crab"}


def parse():
    texts, slug = {}, None
    for line in io.open(MD, encoding="utf-8"):
        m = re.match(r"## \d+\. 《(.+?)》", line)
        if m:
            slug = TITLE[m.group(1)]; texts[slug] = []
            continue
        m = re.match(r"\| (\d+) \| .*? \| (.+) \|\s*$", line)
        if m and slug:
            texts[slug].append((int(m.group(1)), m.group(2).replace(" / ", "\n").strip()))
    return texts


def main(dry):
    texts = parse()
    assert len(texts) == 14, texts.keys()
    src = io.open(os.path.join(SB, "funny5.py"), encoding="utf-8").read()
    for slug, pages in texts.items():
        st = json.load(open(os.path.join(SB, f"story_{slug}.json"), encoding="utf-8"))
        assert [n for n, _ in pages] == [p["n"] for p in st["pages"]], slug
        if slug in EARLY:
            for p, (_, zh) in zip(st["pages"], pages):
                p["zh"] = zh
            if not dry:
                json.dump(st, open(os.path.join(SB, f"story_{slug}.json"), "w", encoding="utf-8", newline="\n"),
                          ensure_ascii=False, indent=2)
            continue
        a = src.index(f'dict(slug="{slug}"')
        nxt = src.find("dict(slug=", a + 10)
        b = nxt if nxt > 0 else src.index("\n]\n", a)
        blk, pos = src[a:b], 0
        for p, (_, zh) in zip(st["pages"], pages):
            old = json.dumps(p["zh"], ensure_ascii=False)
            i = blk.index(old, pos)
            new = json.dumps(zh, ensure_ascii=False)
            blk = blk[:i] + new + blk[i + len(old):]
            pos = i + len(new)
        src = src[:a] + blk + src[b:]
    if not dry:
        io.open(os.path.join(SB, "funny5.py"), "w", encoding="utf-8", newline="\n").write(src)
    print("ok", {k: len(v) for k, v in texts.items()})


if __name__ == "__main__":
    main("--dry" in sys.argv)
