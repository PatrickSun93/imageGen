# -*- coding: utf-8 -*-
"""搞笑系列 9 本和最早 5 本的英文版：图和中文版同一套，只换旁白。

读 story_<slug>.json，写 story_<slug>_en.json：
  lang="en"、text_key="en"（每页旁白放在 "en"，中文 "zh" 留着对照）、
  image_slug=<slug>（make_print / 打包都用中文版的图），早期 5 本另有 image_dir。
英文旁白在 english_text.json（2026-09-23 按家长定稿的新中文重译）；这里只放书名和图目录。
书名不套 *Dragons Love Tacos* 的「X Love Y」句式——只学手法，不学它的名字。

usage: english.py            （全部）
       english.py seesaw ... （只做这几本）
"""
import json, os, sys

SB = os.path.dirname(os.path.abspath(__file__))
TEXT = json.load(open(os.path.join(SB, "english_text.json"), encoding="utf-8"))

# slug: (书名, 副标题[, 早期书的图目录])
EN = {
 "dragonsocks": ("The Dragons Took Your Sock", "Where did your other sock go?"),
 "dinobubbles": ("Bubble Bath for Dinosaurs", "Never bring a squeaky duck"),
 "dinowantsplay": ("The Dinosaur Wants to Play", "Never tell a dinosaur “No!”"),
 "trexwontstop": ("T. Rex Won't Stop", "Is your little drummer knocking?"),
 "dinojoin": ("The Dinosaurs' Secret Password", "Say it when you want to join in"),
 "trexloses": ("T. Rex Hates to Lose", "It's okay to lose. Let's play again."),
 "dinoschool": ("Dinosaur's First Day of School", "You don't have to bring your house"),
 "dragonturns": ("Is It My Turn Yet?", "One swing, seven dragons"),
 "seesaw": ("Dinosaurs on the Seesaw", "Stop! I don't like that."),
 "rafflesia": ("The Biggest Flower in the Forest", "A flower that can't make its own food", "_art_rafflesia"),
 "ants": ("The Ants Are Moving", "They know it's going to rain before I do", "ants_pub"),
 "dino": ("The Dinosaurs Didn't Go Far", "The sparrows in the yard are their children", "dino_pub"),
 "sea": ("The Sea Only Comes a Little Way", "The waves come in, and go back out", "sea_pub"),
 "crab": ("The Hermit Crab's New House", "When you grow, you need a bigger one", "crab_pub"),
}


def build(slug):
    title, subtitle, *image_dir = EN[slug]
    lines = TEXT[slug]
    st = json.load(open(os.path.join(SB, f"story_{slug}.json"), encoding="utf-8"))
    assert len(lines) == len(st["pages"]), (slug, len(lines), len(st["pages"]))
    st.update(title=title, subtitle=subtitle, slug=f"{slug}_en", lang="en", text_key="en", image_slug=slug)
    if image_dir:
        st["image_dir"] = image_dir[0]
        assert os.path.exists(os.path.join(SB, "out", image_dir[0], "page_01.png")), image_dir
    for p, en in zip(st["pages"], lines):
        p["en"] = en
    json.dump(st, open(os.path.join(SB, f"story_{slug}_en.json"), "w", encoding="utf-8", newline="\n"),
              ensure_ascii=False, indent=2)
    words = sum(len(l.split()) for l in lines)
    print(f"{slug:14} {title:34} {len(lines)} pages, {words} words")


if __name__ == "__main__":
    for s in sys.argv[1:] or EN:
        build(s)
