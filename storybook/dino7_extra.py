# -*- coding: utf-8 -*-
"""第七批补渲的素材：本来用几何图元凑出来的真实物体，改成让模型画。

2026-09-16 五个代理把 217 页示意图页过了一遍，找出 66 页拿椭圆、多边形、圆角
矩形拼真实物体——西瓜是一个圆加三道条纹、猫是椭圆加两个三角耳朵、一整团企鹅
是 61 个圆点。这些东西和同一页里模型画的素材摆在一起，一眼就是两种画风，
正是「对比图还是太简笔」说的那件事。

放在单独一个文件里，原来的 dino7_*.py 一个字不动，已有素材的下标也就不会变；
新素材从每本书原有素材的下一个号开始排。dino7_build.py 把这里的追加到
b["assets"] 后面。
"""
from dino7_a import BG

EXTRA = {
    # —— pages7_b ——
    "stego": [
        "One single walnut in its hard shell, resting on its side and seen from its broad face, "
        "the two halves meeting along one wavy raised seam, the shell deeply wrinkled all over.",
    ],
    "ankylo": [
        "One single whole watermelon lying on its side, seen from the side, its dark green rind "
        "marked with broad wavy pale-green stripes and a short curled stem at one end.",
    ],
    "claws": [
        "One single horny claw sheath lying on its side, seen from the side, hollow and wide at "
        "its open base and tapering along one long smooth bend to a single sharp tip, its "
        "surface marked with fine lengthwise ridges.",
        "One single back foot of a two-legged dinosaur, seen from the side and standing on two "
        "spread toes, the inner toe raised clear of the ground and carrying one large hooked "
        "sickle claw.",
        "One single three-fingered dinosaur hand, seen from the side with its fingers spread "
        "wide apart, each finger ending in one long hooked claw, the palm short and thick.",
        "One single three-fingered dinosaur hand, seen from the side with its three fingers "
        "curled together so that the three claw tips almost touch, the palm short and thick.",
        "One single long hooked claw standing upright, seen from the side, narrow at its base "
        "and bending through one strong curve to a sharp point.",
        "One single moderately curved grasping claw standing upright, seen from the side, thick "
        "at its base and bending gently to a blunt point.",
        "One single broad blunt digging claw standing upright, seen from the side, very thick at "
        "its base and flaring out to a wide rounded chisel edge at its tip.",
        "One single short stubby claw standing upright, seen from the side, thick at its base "
        "and hardly longer than it is wide, its tip worn round.",
    ],
    "fingers": [
        "One single dinosaur front hand seen from the front with its fingers spread apart: exactly "
        "three bony fingers stand up from one broad short palm, and there is no fourth and no "
        "fifth finger anywhere on it.",
        "One single dinosaur front hand seen from the front: exactly two short bony fingers stand "
        "up from one broad short palm, and there is no third, fourth or fifth finger anywhere "
        "on it.",
        "One single dinosaur front hand seen from the front, nothing else: one sharp straight "
        "spike stands up where the thumb should be, three short blunt hoof-tipped fingers in "
        "the middle, and one thin outer finger bends inwards. It is a hand only, with no head, "
        "no body and no animal attached to it.",
        "One single bare tree twig held upright, seen from the side, a thin brown woody stem "
        "with two small side shoots.",
        "One single bird wing spread wide open, seen from above, layered rows of short covert feathers along its front edge and long pointed flight feathers along its back edge, floating alone with nothing around it and nothing under it.",
    ],
    "herd": [
        "One single leafy tree standing upright, seen from the side, one straight trunk rising "
        "into two spreading branches carrying a crown of separate small oval leaves.",
        "One single bare tree standing upright, seen from the side, one straight trunk rising "
        "into two spreading branches with no leaves left on them at all.",
    ],
    "mother": [
        "One single row of six small pointed teeth set into a strip of pale gum, seen from the side, each tooth a narrow sharp cone of the same height, hard white enamel, no leaves anywhere.",
        "One single straight strip of pale gum lying flat, seen from the side, with six short "
        "flat-topped white stubs standing in a row along its upper edge, all the same height. "
        "There is no mouth, no jaw, no head and no animal in the picture, only the strip.",
    ],
    # —— pages7_c ——
    "dinosleep": [
        "One single very large long-bodied dinosaur lying flat asleep on the ground, seen from "
        "the side facing left, its belly pressed down and its head laid out in front of it.",
    ],
    "fight": [
        "One single back foot and lower leg of a small feathered two-legged dinosaur, seen from "
        "the side facing left, the flat foot standing with two long toes down and the inner toe "
        "held up.",
    ],
    "tiny": [
        "One single two-pan balance scale seen from the side, one straight level beam resting on "
        "a triangular stand, with one shallow round pan hanging by cords from each end.",
        "One single needle-thin dinosaur fang standing upright, straight and very narrow, "
        "tapering from a slightly wider root to one sharp point.",
        "One single open human hand held palm up, seen from directly above, the fingers spread a "
        "little and the palm cupped hollow in the middle.",
    ],
    "sail": [
        "One single small family car seen from the side facing left, four round wheels on the "
        "ground and a row of windows along its low roof.",
        "One single tall fin of thin pale skin stretched over a row of long bony rods that fan up from its base, seen from the side, a body part of an animal and not a ship, floating alone with nothing around it and nothing under it.",
        "One single tall fin of thin skin flushed deep red stretched over a row of long bony rods that fan up from its base, seen from the side, a body part of an animal and not a ship, floating alone with nothing around it and nothing under it.",
    ],
    "climb": [
        "One single strongly curved bird claw seen from the side, one smooth hook sweeping from "
        "a thick base to one sharp point.",
        "One single nearly straight bird claw seen from the side, thick at its base and tapering "
        "to one blunt point.",
        "One single very large three-toed dinosaur track pressed into bare ground, seen from "
        "directly above, three broad toe marks each ending in one claw dent.",
    ],
    "eras": [
        "One single large five-toed reptile track pressed into flat mud, seen from directly "
        "above, five short spread toe marks around one round pad.",
        "One single three-toed dinosaur track pressed into flat mud, seen from directly above, "
        "three long toe marks spreading forward from one rounded heel pad.",
    ],
    # —— pages7_d ——
    "oldworld": [
        "One single tuft of green grass growing from the ground, seen from the side, about a "
        "dozen narrow blades spreading up and outwards from one root.",
        "One single planet Earth seen from space as a round globe, blue oceans and green land "
        "shapes across its face, thin white cloud swirls over it.",
    ],
    "california": [
        "One single fossil dinosaur leg bone lying flat on its side, seen from the side, a "
        "straight shaft with a thick knobbly swelling at each end, pale brown and pitted.",
    ],
    "firstfind": [
        "One single pointed fossil spike bone standing upright with its tip pointing up, seen "
        "from the side, a wide rounded base narrowing to a sharp point, pale bone brown.",
    ],
    "dinonames": [
        "One single small green lizard standing on four legs, seen from the side facing left, a "
        "long tapering tail and a scaly back.",
        "One single pointed animal horn standing upright with its tip pointing up, seen from the "
        "side, a wide ridged base tapering to a sharp point.",
        "One single horned dinosaur head seen face on from the front, three horns on its face "
        "and a broad bony frill spreading behind it.",
        "One single golden crown of a king seen from the front, a wide band with five pointed "
        "peaks and round red jewels set along it.",
        "One single row of large pointed teeth set along one open dinosaur jaw, seen from the "
        "side, the teeth white and cone-shaped.",
        "One single speckled dinosaur egg lying on its side, seen from the side, a smooth oval "
        "shell with small dark brown spots.",
        "One single rock hammer lying flat, seen from the side, a wooden handle and a heavy "
        "steel head with a flat face at one end and a chisel edge at the other.",
        "One single fossil dinosaur leg bone lying flat on its side, seen from the side, a "
        "straight shaft with a thick knobbly swelling at each end, pale brown and pitted.",
    ],
    "cloud": [
        "One single ball of white cotton wool, seen from the side, soft fluffy fibres standing out all round it, floating alone with nothing around it and nothing under it.",
        "One single grey puff of smoke, seen from the side, thick and dense at one end and thinning to wisps at the other, floating alone with nothing around it and nothing under it.",
        "One single clear round drop of water with one tiny dark grain of dust at its very "
        "centre, seen from the side, light shining through the drop, floating alone with "
        "nothing around it and nothing under it.",
        "One single drop of water seen from the side, rounded and heavy at one end and drawn out to a point at the other, floating alone with nothing around it and nothing under it, no sky and no rain in the picture.",
    ],
    "fog": [
        "One single white puffy cloud floating on its own, seen from the side, a flat level base "
        "and a rounded billowing top.",
    ],
    "hail": [
        "One single passenger aeroplane flying level, seen from the side facing left, a long "
        "body, one swept wing, two engines and a tall tail fin.",
        "One single clear round drop of water seen from the side, light shining through it.",
    ],
    "tornado": [
        "One single very thin rope-like funnel of grey air, seen from the side, twisting and much narrower at its foot than at its top, floating alone with nothing around it and nothing under it.",
    ],
    # —— pages7_e ——
    "forecast": [
        "One single outdoor thermometer standing upright, seen straight from the front, a slim "
        "glass tube with a red line rising inside it and a round bulb at the bottom.",
        "One single round dial gauge standing upright, seen straight from the front, a white "
        "face with small marks around its rim and one thin pointer needle.",
    ],
    "dew": [
        "One single small white cloud floating alone, seen from the side, a soft lumpy top and a "
        "flat grey underside.",
        "One single blade of green grass standing upright and curving over at its tip, seen from "
        "the side, its surface completely dry and plain.",
        "One single round clear water drop resting on a flat surface, seen from the side, its "
        "top catching one small highlight.",
    ],
    "whisker": [
        "One single short-haired cat seen from straight above, lying stretched out with its head "
        "at the top and its tail straight behind it, its long whiskers spreading out sideways "
        "past its cheeks.",
        "One single head of a short-haired cat seen from the side facing right, its long "
        "straight whiskers spreading out in a wide fan above and below its muzzle.",
    ],
    "dognose": [
        "One single cat paw print pressed into soft earth, seen from straight above, one large "
        "rounded pad with four small round toe marks curving above it.",
    ],
    "bat": [
        "One single human ear seen from the side, its outer rim curving round to the lobe and "
        "the opening shaded dark in the middle.",
        "One single small survey boat seen straight from the side, a rounded hull with a low cabin and one short funnel, floating alone with nothing around it and nothing under it (no water, no waves).",
    ],
    "octopus": [
        "One single octopus arm lying alone and curving in a gentle S, seen from the side with "
        "its underside turned to the viewer, two neat rows of round suckers running along it.",
        "One single rounded grey boulder sitting on flat ground, seen from the side, its surface "
        "rough and weathered with one dark hollow opening at its base.",
    ],
    "penguin": [
        "One single emperor penguin seen from straight above standing upright, its dark back and "
        "short flippers making a rounded oval and its beak just showing at the top.",
    ],
    # —— pages7_f ——
    "tadpole": [
        "One single tadpole seen from the side facing left, a round head and a long flat tail, "
        "two small back legs just grown out where the tail begins.",
        "One single tadpole seen from the side facing left with four legs, two long back legs "
        "and two small front legs just pushed out from behind its head, a long flat tail.",
        "One single tadpole seen from the side facing left, a round head and a long flat tail, "
        "a soft feathery gill tuft on each side of its neck.",
    ],
    "seaturtle": [
        "One single heap of round white turtle eggs piled loosely together, seen from the side, "
        "soft leathery shells with shallow dents on them.",
    ],
    "whale": [
        "One single fish seen from the side facing left, three curved gill slits behind its "
        "head, one round eye and a fan-shaped tail.",
    ],
    "spider": [
        "One single bare twig standing upright with no leaves on it, rough grey brown bark and "
        "one small side knot.",
        "One single broad green leaf hanging from a short stalk, seen flat from the front, its "
        "veins showing.",
    ],
    "giraffe": [
        "One single giraffe head on its long neck, seen from the side facing left, the neck held "
        "straight upright and ending at the shoulder, two short horns on top of the head, brown "
        "patches on pale cream hide.",
        "One single arm of a human child seen from the side, held out straight with the open "
        "palm flat and the five fingers together.",
    ],
}

EXTRA = {k: [s + " " + BG for s in v] for k, v in EXTRA.items()}
