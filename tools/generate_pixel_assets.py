"""Generate original, theme-specific pixel/cel-shaded assets.

This is intentionally deterministic so a release build can reproduce the art.
The installed VS Code pixel-agent extensions are authoring assistants, not batch
PNG exporters; this local renderer is the reproducible production fallback.
"""

from __future__ import annotations

import argparse
import hashlib
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
THEMES_ROOT = ROOT / "assets" / "themes"
DEFAULT = THEMES_ROOT / "default"
THEMES = {
    "candy_kingdom": {"bg": (255, 240, 195), "deep": (82, 35, 67), "mid": (238, 78, 143), "light": (255, 207, 91), "roles": {"marshmallow_man": "marshmallow", "springfield_doughnut": "doughnut", "gingerbread_golem": "gingerbread"}},
    "graveyard": {"bg": (25, 30, 47), "deep": (42, 20, 56), "mid": (113, 53, 94), "light": (151, 221, 193), "roles": {"ghost": "ghost", "vampire": "vampire", "werewolf": "werewolf"}},
    "hunting": {"bg": (42, 64, 48), "deep": (35, 30, 28), "mid": (111, 79, 48), "light": (211, 181, 111), "roles": {"hunter": "hunter", "deer": "deer", "bear": "bear"}},
    "space": {"bg": (12, 18, 42), "deep": (19, 28, 70), "mid": (35, 173, 190), "light": (126, 239, 225), "roles": {"alien_drone": "drone", "alien_warrior": "warrior", "alien_overlord": "overlord"}},
}
ANIMATIONS = {"idle": 8, "walk": 8, "attack": 6, "pain": 3, "death": 8}


def canvas(size, color=(0, 0, 0, 0)):
    return Image.new("RGBA", size, color)


def game_icon():
    image = Image.new("RGBA", (64, 64), (10, 18, 16, 255))
    draw = ImageDraw.Draw(image)
    dark = (19, 30, 27, 255)
    helmet = (61, 91, 72, 255)
    helmet_light = (101, 132, 98, 255)
    skin = (181, 111, 77, 255)
    skin_light = (226, 157, 111, 255)
    shadow = (91, 48, 42, 255)
    eye = (224, 219, 171, 255)
    black = (12, 15, 14, 255)
    draw.rectangle((8, 7, 55, 17), fill=dark)
    draw.polygon([(13, 16), (19, 10), (45, 10), (52, 17), (55, 32), (49, 47), (39, 56), (24, 56), (14, 47), (9, 31)], fill=helmet, outline=black, width=2)
    draw.rectangle((18, 13, 45, 20), fill=helmet_light)
    draw.rectangle((14, 20, 50, 27), fill=skin, outline=black, width=1)
    draw.polygon([(15, 26), (49, 26), (47, 45), (39, 54), (24, 54), (16, 44)], fill=skin, outline=black)
    draw.polygon([(16, 27), (29, 22), (47, 27), (43, 32), (31, 29), (20, 33)], fill=skin_light)
    draw.polygon([(17, 30), (28, 27), (27, 31), (18, 35)], fill=shadow)
    draw.polygon([(36, 27), (47, 30), (46, 35), (35, 31)], fill=shadow)
    draw.rectangle((20, 34, 28, 39), fill=eye, outline=black)
    draw.rectangle((36, 34, 44, 39), fill=eye, outline=black)
    draw.rectangle((24, 35, 27, 39), fill=black)
    draw.rectangle((37, 35, 40, 39), fill=black)
    draw.polygon([(30, 34), (34, 34), (35, 45), (29, 45)], fill=shadow)
    draw.rectangle((26, 46, 39, 49), fill=dark)
    draw.rectangle((29, 49, 36, 51), fill=black)
    draw.rectangle((11, 25, 16, 39), fill=helmet_light)
    draw.rectangle((48, 25, 53, 39), fill=helmet_light)
    return image


def palette(spec):
    return spec["deep"], spec["mid"], spec["light"], (245, 238, 215), (12, 14, 21)


def texture(spec, index, seed):
    image = Image.new("RGB", (1024, 1024), spec["bg"])
    draw = ImageDraw.Draw(image)
    deep, mid, light, cream, outline = palette(spec)
    rng = random.Random(seed + index)
    draw.rectangle((0, 0, 1023, 1023), fill=deep)
    tile = 256
    for y in range(-tile, 1024, tile):
        for x in range(-tile, 1024, tile):
            shade = (mid if (x // tile + y // tile) % 2 else spec["bg"])
            inset = 12 + (index * 3) % 14
            draw.rectangle((x + inset, y + inset, x + tile - inset, y + tile - inset), fill=shade, outline=outline, width=8)
            for _ in range(18):
                px = x + rng.randrange(22, tile - 22)
                py = y + rng.randrange(22, tile - 22)
                draw.rectangle((px, py, px + rng.randrange(3, 14), py + rng.randrange(3, 14)), fill=light)
    if index % 2:
        for x in range(-1024, 2048, 128):
            draw.line((x, 0, x + 1024, 1024), fill=light, width=5)
    return image


def sky(spec):
    image = Image.new("RGB", (1200, 400), spec["bg"])
    draw = ImageDraw.Draw(image)
    deep, mid, light, _, _ = palette(spec)
    for y in range(0, 400, 24):
        draw.rectangle((0, y, 1200, y + 24), fill=deep if (y // 24) % 2 else spec["bg"])
    for x in range(0, 1200, 48):
        draw.rectangle((x, 270 + (x % 5) * 8, x + 22, 400), fill=mid)
    for x in range(40, 1200, 137):
        draw.rectangle((x, 48 + x % 90, x + 8, 56 + x % 90), fill=light)
    return image


def hunting_texture(index, seed):
    image = Image.new("RGB", (1024, 1024), (126, 166, 196))
    draw = ImageDraw.Draw(image)
    rng = random.Random(seed + index)
    bark = (64, 48, 37); forest = (48, 82, 50); pine = (34, 67, 47); snow = (183, 202, 202)
    draw.rectangle((0, 0, 1023, 1023), fill=forest)
    if index in {1, 3}:
        draw.rectangle((0, 0, 1023, 300), fill=(116, 156, 184) if index == 1 else (91, 133, 160))
        draw.polygon([(0, 270), (180, 130), (360, 260), (560, 80), (780, 255), (930, 145), (1023, 245), (1023, 390), (0, 390)], fill=(104, 119, 113))
        draw.polygon([(0, 310), (180, 170), (360, 300), (560, 120), (780, 295), (930, 185), (1023, 285), (1023, 410), (0, 410)], fill=(161, 166, 145))
        draw.rectangle((0, 390, 1023, 1023), fill=(55, 82, 53))
        draw.polygon([(0, 620), (160, 520), (330, 650), (530, 500), (730, 650), (900, 545), (1023, 620), (1023, 1023), (0, 1023)], fill=(68, 92, 57))
        for tree in range(16):
            x = rng.randrange(-40, 1000); trunk = rng.randrange(18, 38); base = rng.randrange(650, 1020); top = rng.randrange(120, 470)
            draw.rectangle((x, top + 90, x + trunk, base), fill=bark, outline=(24, 31, 28), width=6)
            for layer in range(4):
                y = top + layer * 65
                half = 42 + layer * 13 + rng.randrange(12)
                draw.polygon([(x + trunk // 2, y), (x - half, y + 115), (x + trunk + half, y + 115)], fill=pine if layer % 2 else (54, 94, 61), outline=(24, 45, 34))
            draw.rectangle((x + trunk // 2, top + 100, x + trunk // 2 + 7, base - 30), fill=(104, 80, 50))
        for _ in range(32):
            x = rng.randrange(0, 1020); y = rng.randrange(520, 980)
            draw.rectangle((x, y, x + rng.randrange(8, 28), y + rng.randrange(4, 12)), fill=(92, 116, 62))
    elif index in {2, 4, 5}:
        draw.rectangle((0, 0, 1023, 1023), fill=(109, 73, 47))
        for y in range(80, 1024, 160): draw.line((0, y, 1023, y), fill=(56, 39, 29), width=12)
        draw.rectangle((130, 210, 894, 900), fill=(73, 46, 33), outline=(29, 24, 21), width=18)
        for x in range(160, 870, 118): draw.line((x, 230, x, 880), fill=(40, 29, 24), width=8)
        if index == 2:
            draw.rectangle((290, 450, 734, 880), fill=(31, 27, 24), outline=(164, 116, 67), width=16)
            draw.rectangle((350, 570, 674, 880), fill=(20, 19, 18), outline=(102, 73, 45), width=10)
        elif index == 4:
            mount = (101, 63, 42); fur = (152, 104, 66); fur_light = (187, 145, 88); antler = (211, 174, 109); dark = (25, 22, 20)
            draw.ellipse((292, 300, 728, 790), fill=mount, outline=dark, width=16)
            draw.polygon([(382, 420), (638, 420), (675, 610), (600, 760), (510, 800), (420, 760), (345, 610)], fill=fur, outline=dark)
            draw.polygon([(420, 610), (600, 610), (570, 760), (510, 800), (450, 760)], fill=fur_light, outline=dark, width=8)
            draw.ellipse((396, 452, 456, 512), fill=(239, 213, 157), outline=dark, width=7); draw.ellipse((564, 452, 624, 512), fill=(239, 213, 157), outline=dark, width=7)
            draw.ellipse((420, 468, 445, 500), fill=dark); draw.ellipse((575, 468, 600, 500), fill=dark)
            draw.ellipse((455, 580, 565, 660), fill=dark, outline=(12, 12, 12), width=6)
            draw.ellipse((477, 596, 505, 620), fill=(12, 12, 12)); draw.ellipse((515, 596, 543, 620), fill=(12, 12, 12))
            draw.line((510, 650, 510, 735), fill=dark, width=8)
            draw.polygon([(345, 438), (270, 385), (295, 545), (390, 510)], fill=fur, outline=dark)
            draw.polygon([(675, 438), (750, 385), (725, 545), (630, 510)], fill=fur, outline=dark)
            draw.line((405, 445, 335, 295), fill=antler, width=20); draw.line((335, 295, 285, 220), fill=antler, width=15); draw.line((335, 295, 355, 190), fill=antler, width=15); draw.line((335, 295, 300, 170), fill=antler, width=12)
            draw.line((615, 445, 685, 295), fill=antler, width=20); draw.line((685, 295, 735, 220), fill=antler, width=15); draw.line((685, 295, 665, 190), fill=antler, width=15); draw.line((685, 295, 720, 170), fill=antler, width=12)
        else:
            draw.ellipse((310, 400, 714, 760), fill=(34, 28, 24), outline=(13, 13, 12), width=12)
            draw.polygon([(390, 570), (510, 430), (635, 570), (570, 720), (430, 720)], fill=(92, 61, 41), outline=(24, 20, 17))
            draw.ellipse((450, 530, 490, 570), fill=(187, 145, 88)); draw.ellipse((530, 530, 570, 570), fill=(187, 145, 88))
            for x, y, angle in ((230, 320, -1), (760, 320, 1), (510, 180, 0)):
                draw.polygon([(x, y), (x + 24 * angle, y + 430), (x + 54 * angle, y + 430), (x + 30, y)], fill=(180, 128, 66), outline=(27, 22, 18))
                draw.rectangle((x - 8, y - 25, x + 38, y + 25), fill=(211, 174, 109), outline=(27, 22, 18), width=6)
    return image


def hunting_sky():
    image = Image.new("RGB", (1200, 400))
    pixels = image.load()
    top = (126, 166, 196)
    bottom = tuple(int(channel * 0.7) for channel in top)
    for y in range(400):
        ratio = y / 399
        color = tuple(int(top[i] * (1 - ratio) + bottom[i] * ratio) for i in range(3))
        for x in range(1200): pixels[x, y] = color
    draw = ImageDraw.Draw(image)
    for x in range(40, 1200, 137): draw.rectangle((x, 50 + x % 90, x + 8, 58 + x % 90), fill=(221, 232, 226))
    return image


def ui(spec, kind, size):
    image = Image.new("RGBA", size, (*spec["bg"], 255))
    draw = ImageDraw.Draw(image)
    deep, mid, light, cream, outline = palette(spec)
    draw.rectangle((32, 32, size[0] - 33, size[1] - 33), fill=deep, outline=light, width=18)
    draw.rectangle((70, 70, size[0] - 71, size[1] - 71), outline=mid, width=8)
    for x in range(100, size[0] - 100, 160):
        draw.rectangle((x, size[1] - 160, x + 70, size[1] - 100), fill=light)
    label = {"game_over": "Game Over", "win": "You Win", "blood_screen": ""}[kind] if spec["bg"] == (42, 64, 48) else {"game_over": "DOWN", "win": "CLEAR", "blood_screen": ""}[kind]
    if label:
        font = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", max(48, size[0] // 9))
        box = draw.textbbox((0, 0), label, font=font)
        x = (size[0] - (box[2] - box[0])) // 2
        y = (size[1] - (box[3] - box[1])) // 2
        draw.text((x + 10, y + 10), label, font=font, fill=outline)
        draw.text((x, y), label, font=font, fill=light)
    elif kind == "blood_screen":
        for x in range(0, size[0], 90):
            draw.line((x, 0, x + 180, size[1]), fill=(*mid, 120), width=20)
    return image


def npc_frame(spec, role, action, frame):
    image = canvas((76, 110))
    draw = ImageDraw.Draw(image)
    deep, mid, light, cream, outline = palette(spec)
    phase = (frame % 4) - 1.5
    bob = int(phase) if action in {"idle", "walk"} else 0
    dying = action == "death"
    progress = frame / 7
    if dying:
        bob += int(progress * 28)
    if role == "marshmallow":
        body = (12, 28 + bob, 64, 89 + bob); draw.rounded_rectangle(body, 8, fill=cream, outline=outline, width=4)
        draw.rectangle((22, 52 + bob, 54, 76 + bob), fill=light)
        draw.ellipse((25, 42 + bob, 33, 51 + bob), fill=outline); draw.ellipse((45, 42 + bob, 53, 51 + bob), fill=outline)
    elif role == "doughnut":
        draw.ellipse((10, 25 + bob, 66, 86 + bob), fill=mid, outline=outline, width=4); draw.ellipse((29, 43 + bob, 47, 62 + bob), fill=spec["bg"], outline=outline, width=3)
        for x in (18, 52): draw.rectangle((x, 66 + bob, x + 7, 91 + bob), fill=mid)
    elif role == "gingerbread":
        draw.ellipse((25, 12 + bob, 51, 38 + bob), fill=mid, outline=outline, width=3)
        draw.line((38, 38 + bob, 38, 78 + bob), fill=mid, width=14)
        draw.line((38, 48 + bob, 16, 66 + bob), fill=mid, width=8); draw.line((38, 48 + bob, 60, 66 + bob), fill=mid, width=8)
        draw.line((38, 76 + bob, 22, 103), fill=mid, width=9); draw.line((38, 76 + bob, 54, 103), fill=mid, width=9)
        draw.rectangle((31, 24 + bob, 35, 28 + bob), fill=light); draw.rectangle((41, 24 + bob, 45, 28 + bob), fill=light)
    elif role == "vampire":
        draw.ellipse((25, 12 + bob, 51, 39 + bob), fill=light, outline=outline, width=3)
        draw.polygon([(38, 34 + bob), (8, 92 + bob), (38, 80 + bob), (68, 92 + bob)], fill=mid, outline=outline)
        draw.rectangle((30, 37 + bob, 46, 48 + bob), fill=spec["bg"])
        draw.rectangle((31, 25 + bob, 35, 29 + bob), fill=outline); draw.rectangle((41, 25 + bob, 45, 29 + bob), fill=outline)
    elif role == "bear":
        draw.ellipse((11, 35 + bob, 67, 86 + bob), fill=mid, outline=outline, width=4)
        draw.ellipse((18, 14 + bob, 38, 39 + bob), fill=mid, outline=outline, width=3)
        draw.ellipse((40, 14 + bob, 60, 39 + bob), fill=mid, outline=outline, width=3)
        draw.ellipse((19, 22 + bob, 37, 39 + bob), fill=light, outline=outline, width=2)
        draw.ellipse((41, 22 + bob, 59, 39 + bob), fill=light, outline=outline, width=2)
        draw.ellipse((18, 48 + bob, 58, 76 + bob), fill=deep, outline=outline, width=3)
        draw.ellipse((28, 55 + bob, 49, 71 + bob), fill=light, outline=outline, width=2)
        draw.rectangle((34, 54 + bob, 43, 61 + bob), fill=outline)
        draw.rectangle((22, 42 + bob, 30, 50 + bob), fill=light); draw.rectangle((47, 42 + bob, 55, 50 + bob), fill=light)
        draw.line((24, 78 + bob, 16, 106), fill=mid, width=12); draw.line((52, 78 + bob, 60, 106), fill=mid, width=12)
        draw.rectangle((11, 99, 24, 107), fill=light); draw.rectangle((53, 99, 66, 107), fill=light)
        draw.rectangle((29 + frame % 3, 76 + bob, 35 + frame % 3, 80 + bob), fill=light)
    elif role == "werewolf":
        draw.ellipse((12, 28 + bob, 64, 83 + bob), fill=mid, outline=outline, width=4)
        draw.polygon([(16, 35 + bob), (14, 13 + bob), (30, 26 + bob), (46, 26 + bob), (62, 13 + bob), (60, 35 + bob)], fill=mid, outline=outline)
        draw.ellipse((25, 47 + bob, 51, 67 + bob), fill=deep, outline=outline, width=3)
        draw.rectangle((24, 41 + bob, 32, 49 + bob), fill=light); draw.rectangle((44, 41 + bob, 52, 49 + bob), fill=light)
        draw.line((24, 78 + bob, 16, 104), fill=mid, width=11); draw.line((52, 78 + bob, 60, 104), fill=mid, width=11)
    elif role == "deer":
        draw.ellipse((27, 25 + bob, 53, 53 + bob), fill=mid, outline=outline, width=3)
        draw.polygon([(28, 47 + bob), (49, 47 + bob), (59, 78 + bob), (20, 78 + bob)], fill=mid, outline=outline)
        draw.polygon([(29, 55 + bob), (48, 55 + bob), (44, 72 + bob), (25, 72 + bob)], fill=light)
        draw.line((28, 73 + bob, 20, 106), fill=mid, width=6); draw.line((46, 73 + bob, 55, 106), fill=mid, width=6)
        draw.line((35, 73 + bob, 33, 106), fill=light, width=5); draw.line((51, 73 + bob, 61, 103), fill=light, width=5)
        draw.line((30, 29 + bob, 18, 12 + bob), fill=light, width=4); draw.line((18, 12 + bob, 10, 20 + bob), fill=light, width=3); draw.line((18, 12 + bob, 16, 5 + bob), fill=light, width=3)
        draw.line((50, 29 + bob, 62, 12 + bob), fill=light, width=4); draw.line((62, 12 + bob, 70, 20 + bob), fill=light, width=3); draw.line((62, 12 + bob, 64, 5 + bob), fill=light, width=3)
        draw.rectangle((35, 35 + bob, 39, 39 + bob), fill=outline); draw.rectangle((45, 35 + bob, 49, 39 + bob), fill=outline)
    elif role == "warrior":
        head_shift = 5 if frame % 2 else 0
        draw.ellipse((10 + head_shift, 12 + bob, 38 + head_shift, 43 + bob), fill=light, outline=outline, width=3)
        draw.ellipse((38 - head_shift, 12 + bob, 66 - head_shift, 43 + bob), fill=light, outline=outline, width=3)
        draw.rectangle((28, 37 + bob, 48, 53 + bob), fill=mid, outline=outline, width=3)
        draw.rectangle((18 + head_shift, 24 + bob, 24 + head_shift, 31 + bob), fill=deep)
        draw.rectangle((52 - head_shift, 24 + bob, 58 - head_shift, 31 + bob), fill=deep)
        draw.polygon([(21, 48 + bob), (55, 48 + bob), (63, 84 + bob), (13, 84 + bob)], fill=mid, outline=outline)
        draw.line((22, 79 + bob, 10, 105), fill=mid, width=8); draw.line((52, 79 + bob, 66, 105), fill=mid, width=8)
        draw.line((18, 61 + bob, 4, 76), fill=light, width=6); draw.line((58, 61 + bob, 72, 76), fill=light, width=6)
    elif role == "hunter":
        hat_shift = (frame % 3) - 1
        draw.polygon([(18 + hat_shift, 14 + bob), (58 - hat_shift, 14 + bob), (63, 23 + bob), (13, 23 + bob)], fill=deep, outline=outline, width=3)
        draw.rectangle((19 + hat_shift, 22 + bob, 57 - hat_shift, 28 + bob), fill=mid, outline=outline, width=2)
        draw.line((16 + hat_shift, 27 + bob, 25, 30 + bob), fill=mid, width=3)
        draw.rectangle((25, 27 + bob, 51, 45 + bob), fill=light, outline=outline, width=3)
        draw.rectangle((28, 34 + bob, 32, 38 + bob), fill=outline); draw.rectangle((44, 34 + bob, 48, 38 + bob), fill=outline)
        draw.rectangle((35, 39 + bob, 41, 43 + bob), fill=cream)
        draw.rectangle((21, 45 + bob, 55, 63 + bob), fill=mid, outline=outline, width=3)
        draw.polygon([(24, 62 + bob), (16, 78 + bob), (26, 78 + bob), (30, 65 + bob)], fill=deep, outline=outline, width=2)
        draw.polygon([(52, 62 + bob), (60, 78 + bob), (50, 78 + bob), (46, 65 + bob)], fill=deep, outline=outline, width=2)
        draw.rectangle((27, 63 + bob, 49, 69 + bob), fill=cream)
        draw.line((28, 84 + bob, 20, 103 + bob), fill=light, width=8); draw.line((48, 84 + bob, 56, 103 + bob), fill=light, width=8)
        draw.line((20, 72 + bob, 8, 90 + bob), fill=mid, width=6); draw.line((56, 72 + bob, 68, 90 + bob), fill=mid, width=6)
        draw.line((50, 60 + bob, 58, 58 + bob), fill=mid, width=4)
        draw.rectangle((56, 56 + bob, 70, 60 + bob), fill=mid, outline=outline, width=2)
        draw.rectangle((68, 54 + bob, 75, 58 + bob), fill=light, outline=outline, width=2)
    elif role == "drone":
        draw.ellipse((8, 35 + bob, 68, 70 + bob), fill=mid, outline=outline, width=4)
        draw.polygon([(18, 50 + bob), (29, 17 + bob), (47, 17 + bob), (58, 50 + bob)], fill=deep, outline=outline)
        draw.ellipse((29, 22 + bob, 47, 42 + bob), fill=light, outline=cream, width=3)
        draw.rectangle((34, 27 + bob, 42, 36 + bob), fill=spec["bg"])
        draw.line((20, 66 + bob, 12, 88), fill=light, width=6); draw.line((56, 66 + bob, 64, 88), fill=light, width=6)
    elif role == "overlord":
        draw.ellipse((19, 20 + bob, 57, 58 + bob), fill=mid, outline=outline, width=4)
        draw.polygon([(14, 42 + bob), (62, 42 + bob), (66, 87 + bob), (52, 78 + bob), (38, 95 + bob), (24, 78 + bob), (10, 87 + bob)], fill=mid, outline=outline)
        draw.polygon([(20, 22 + bob), (27, 5 + bob), (34, 19 + bob), (42, 5 + bob), (49, 22 + bob)], fill=light, outline=outline)
        draw.ellipse((29, 32 + bob, 47, 50 + bob), fill=light, outline=cream, width=2)
        draw.rectangle((34, 37 + bob, 42, 45 + bob), fill=deep)
        draw.line((23, 62 + bob, 10, 91), fill=light, width=8); draw.line((53, 62 + bob, 66, 91), fill=light, width=8)
    elif role == "ghost":
        draw.ellipse((13, 18 + bob, 63, 72 + bob), fill=mid, outline=outline, width=4); draw.polygon([(13, 57 + bob), (63, 57 + bob), (57, 98 + bob), (45, 84 + bob), (34, 99 + bob), (22, 84 + bob)], fill=mid, outline=outline)
        draw.rectangle((24, 38 + bob, 33, 48 + bob), fill=light); draw.rectangle((44, 38 + bob, 53, 48 + bob), fill=light)
    else:
        draw.ellipse((15, 18 + bob, 61, 66 + bob), fill=mid, outline=outline, width=4); draw.polygon([(17, 55 + bob), (59, 55 + bob), (67, 91 + bob), (51, 84 + bob), (25, 97 + bob), (9, 88 + bob)], fill=mid, outline=outline)
        draw.rectangle((22, 41 + bob, 31, 50 + bob), fill=light); draw.rectangle((45, 41 + bob, 54, 50 + bob), fill=light)
    detail_x = 18 + (frame % 7)
    draw.rectangle((detail_x, 30 + bob, detail_x + 4, 34 + bob), fill=light)
    if action == "walk":
        draw.line((30, 78 + bob, 22 - int(phase * 3), 105), fill=light, width=7); draw.line((48, 78 + bob, 56 + int(phase * 3), 105), fill=light, width=7)
    if action == "attack":
        if role == "hunter":
            draw.line((35, 60 + bob, 67, 44 + bob), fill=deep, width=6)
            draw.rectangle((62, 39 + bob, 74, 47 + bob), fill=light, outline=outline, width=2)
            draw.rectangle((68, 36 + bob, 76, 41 + bob), fill=cream, outline=outline, width=2)
            draw.ellipse((58, 34 + bob, 66, 42 + bob), outline=light, width=2)
            draw.rectangle((48, 60 + bob, 52, 70 + bob), fill=cream)
        elif role in {"bear", "werewolf"}:
            draw.line((27, 65 + bob, 10, 48), fill=light, width=7); draw.line((49, 65 + bob, 66, 48), fill=light, width=7)
            draw.line((8, 46, 15, 52), fill=cream, width=3); draw.line((66, 46, 59, 52), fill=cream, width=3)
            if role == "bear":
                draw.ellipse((29, 55 + bob, 47, 72 + bob), fill=outline)
                draw.rectangle((33, 66 + bob, 43, 72 + bob), fill=(224, 62, 48))
                draw.rectangle((21 + frame % 4, 78 + bob, 27 + frame % 4, 83 + bob), fill=light)
        elif role == "deer":
            draw.line((39, 58 + bob, 68, 48), fill=light, width=6); draw.polygon([(67, 48), (73, 44), (73, 52)], fill=cream)
        elif role == "warrior":
            draw.line((47, 60 + bob, 69, 44), fill=light, width=5)
            draw.ellipse((61, 36 - frame, 73, 48 - frame), fill=cream, outline=light, width=2)
            draw.rectangle((66, 40 - frame, 70, 44 - frame), fill=deep)
        elif role in {"ghost", "vampire", "drone", "overlord"}:
            draw.ellipse((58, 37 - frame, 70, 49 - frame), fill=light, outline=cream, width=2)
            draw.line((49, 55 + bob, 64, 43 - frame), fill=light, width=5)
        else:
            draw.line((46, 58 + bob, 67, 42 - frame * 2), fill=light, width=6)
            draw.rectangle((60, 32 - frame * 2, 69, 42 - frame * 2), fill=cream)
    if action == "pain":
        wound = (224, 62, 48)
        wound_x = 28 + frame * 5
        wound_y = 48 + frame * 4
        draw.ellipse((wound_x - 6, wound_y - 6, wound_x + 8, wound_y + 8), fill=wound, outline=outline, width=2)
        draw.polygon([(wound_x - 10, wound_y - 2), (wound_x - 3, wound_y - 7), (wound_x + 3, wound_y - 1), (wound_x + 10, wound_y - 5), (wound_x + 4, wound_y + 4), (wound_x - 5, wound_y + 7)], fill=(122, 25, 30), outline=outline)
        draw.rectangle((wound_x - 2, wound_y - 2, wound_x + 3, wound_y + 3), fill=(255, 157, 102))
        draw.rectangle((19 + frame * 4, 76, 28 + frame * 4, 88), fill=wound, outline=outline, width=2)
        draw.ellipse((wound_x + 12, wound_y + 8, wound_x + 16, wound_y + 13), fill=wound)
        draw.ellipse((wound_x - 15, wound_y + 12, wound_x - 11, wound_y + 17), fill=wound)
    if dying:
        ground_y = int(88 + progress * 18)
        draw.rectangle((8, ground_y, 68, ground_y + 12), fill=mid)
        if frame >= 3:
            draw.ellipse((18, ground_y - 8, 34, ground_y + 4), fill=(224, 62, 48), outline=outline, width=2)
            draw.rectangle((42, ground_y - 4, 52, ground_y + 5), fill=deep)
        if role == "bear":
            draw.ellipse((28, ground_y - 13, 48, ground_y + 2), fill=deep, outline=outline, width=2)
            draw.line((20, ground_y - 5, 12, ground_y + 5), fill=mid, width=5)
            draw.line((56, ground_y - 5, 64, ground_y + 5), fill=mid, width=5)
        elif role == "deer":
            draw.line((30, ground_y - 5, 18, ground_y + 6), fill=light, width=4)
            draw.line((48, ground_y - 5, 60, ground_y + 6), fill=light, width=4)
            draw.line((31, ground_y - 9, 18, ground_y - 19), fill=light, width=3)
            draw.line((49, ground_y - 9, 62, ground_y - 19), fill=light, width=3)
        elif role == "hunter":
            draw.line((47, ground_y - 10, 70, ground_y + 2), fill=deep, width=4)
            draw.rectangle((65, ground_y - 1, 73, ground_y + 5), fill=light)
        elif role in {"drone", "warrior", "overlord"}:
            burst = 8 + frame * 2
            draw.line((38 - burst, ground_y - 20, 38 + burst, ground_y + 2), fill=light, width=2)
            draw.line((38, ground_y - 20 - burst // 2, 38, ground_y + burst // 3), fill=cream, width=2)
        elif role in {"ghost", "vampire", "werewolf"}:
            draw.ellipse((26, ground_y - 16, 32, ground_y - 10), fill=light)
            draw.ellipse((45, ground_y - 24, 51, ground_y - 18), fill=light)
            draw.ellipse((55, ground_y - 10, 61, ground_y - 4), fill=light)
    if role == "hunter":
        inset = Image.new("RGBA", image.size)
        inset.alpha_composite(image, (-2, -2))
        return inset
    return image


def weapon(spec, size, frame):
    image = canvas(size); draw = ImageDraw.Draw(image); deep, mid, light, cream, outline = palette(spec)
    w, h = size
    if spec["bg"] == (42, 64, 48):
        draw.polygon([(w // 2 - 120, h), (w // 2 - 50, h // 2), (w // 2 + 42, h // 2), (w // 2 + 130, h), (w // 2 + 35, h - 30), (w // 2 - 35, h - 30)], fill=mid, outline=outline)
        draw.rectangle((w // 2 - 28, h // 2 - 120, w // 2 + 42, h // 2 + 25), fill=light, outline=outline, width=10)
        draw.line((w // 2 + 8, h // 2 - 115, w // 2 + 8, 90 + frame * 4), fill=deep, width=16)
        draw.line((w // 2 - 80, h // 2 - 105, w // 2 + 80, h // 2 - 105), fill=cream, width=12)
        draw.rectangle((w // 2 - 110, h // 2 - 120, w // 2 - 75, h // 2 - 90), fill=light, outline=outline, width=5)
    else:
        draw.polygon([(w // 2 - 120, h), (w // 2 - 50, h // 2), (w // 2 + 42, h // 2), (w // 2 + 130, h), (w // 2 + 35, h - 30), (w // 2 - 35, h - 30)], fill=mid, outline=outline)
        draw.rectangle((w // 2 - 28, h // 2 - 120, w // 2 + 42, h // 2 + 25), fill=light, outline=outline, width=10)
        draw.line((w // 2 + 8, h // 2 - 115, w // 2 + 8, 90 + frame * 4), fill=cream, width=16)
    return image


def scenery(spec, size, name, frame):
    image = canvas(size)
    draw = ImageDraw.Draw(image)
    deep, mid, light, cream, outline = palette(spec)
    width, height = size
    center = width // 2
    if spec["bg"] == (42, 64, 48) and name == "green_light":
        draw.rectangle((center - width // 4, height // 3, center + width // 4, height - 30), fill=(35, 35, 31), outline=outline, width=max(3, width // 24))
        draw.rectangle((center - width // 3, height // 3 - 20, center + width // 3, height // 3 + 8), fill=deep, outline=outline, width=max(2, width // 30))
        draw.rectangle((center - width // 5, height // 6, center + width // 5, height // 3), fill=(92, 58, 36), outline=outline, width=max(2, width // 30))
        draw.ellipse((center - width // 8, height // 7, center + width // 8, height // 4), fill=(255, 166, 54), outline=cream, width=max(2, width // 30))
    elif spec["bg"] == (42, 64, 48) and name == "red_light":
        draw.rectangle((center - width // 10, height // 5, center + width // 10, height - 35), fill=(102, 73, 42), outline=outline, width=max(2, width // 30))
        draw.ellipse((center - width // 4, height // 7, center + width // 4, height // 3), fill=(217, 170, 84), outline=cream, width=max(2, width // 30))
        draw.rectangle((center - width // 5, height // 3, center + width // 5, height // 3 + 12), fill=deep)
    elif name in {"green_light", "red_light"}:
        glow = (80, 255, 160) if name == "green_light" else (255, 80, 95)
        draw.rectangle((center - max(8, width // 16), height // 4, center + max(8, width // 16), height - 30), fill=deep, outline=outline, width=max(2, width // 32))
        radius = max(12, width // 5)
        pulse = (frame % 3) * max(2, width // 30)
        draw.ellipse((center - radius - pulse, height // 8 - pulse, center + radius + pulse, height // 8 + radius * 2 + pulse), fill=(*glow, 55))
        draw.ellipse((center - radius, height // 8, center + radius, height // 8 + radius * 2), fill=glow, outline=cream, width=max(2, width // 24))
        draw.rectangle((center - radius // 3, height // 8 + radius // 3, center + radius // 3, height // 8 + radius), fill=cream)
    else:
        base_y = height - max(20, height // 8)
        stem = max(5, width // 16)
        draw.rectangle((center - stem, base_y - height // 2, center + stem, base_y), fill=deep, outline=outline, width=max(2, width // 32))
        draw.rectangle((center - width // 3, base_y, center + width // 3, base_y + height // 12), fill=mid, outline=outline, width=max(2, width // 32))
        for branch in (-2, -1, 1, 2):
            branch_x = center + branch * width // 7
            branch_y = base_y - height // 3 - abs(branch) * height // 20
            draw.line((center, branch_y + height // 10, branch_x, branch_y), fill=mid, width=stem)
            draw.ellipse((branch_x - width // 10, branch_y - width // 5, branch_x + width // 10, branch_y + width // 10), fill=light, outline=outline, width=max(2, width // 32))
            draw.rectangle((branch_x - width // 24, branch_y - width // 8, branch_x + width // 24, branch_y), fill=cream)
    return image


def generate(theme_name, theme):
    root = THEMES_ROOT / theme_name
    textures = root / "textures"; sprites = root / "sprites"
    textures.mkdir(parents=True, exist_ok=True)
    seed = int.from_bytes(hashlib.sha256(theme_name.encode("ascii")).digest()[:4], "big")
    for index in range(1, 6):
        renderer = hunting_texture if theme_name == "hunting" else texture
        image = renderer(index, seed) if theme_name == "hunting" else renderer(theme, index, seed)
        image.save(textures / f"{index}.png")
    (hunting_sky() if theme_name == "hunting" else sky(theme)).save(textures / "sky.png")
    for kind, size in {"blood_screen": (1600, 900), "game_over": (1600, 900), "win": (1920, 1080)}.items(): ui(theme, kind, size).save(textures / f"{kind}.png")
    digits = textures / "digits"; digits.mkdir(exist_ok=True)
    for index in range(11):
        source = Image.open(DEFAULT / "textures" / "digits" / f"{index}.png").convert("RGBA")
        pixels = source.load(); tint = theme["light"]
        for y in range(source.height):
            for x in range(source.width):
                if pixels[x, y][3]: pixels[x, y] = (*tint, pixels[x, y][3])
        source.save(digits / f"{index}.png")
    npc_root = sprites / "npc"
    for name, role in theme["roles"].items():
        for action, count in ANIMATIONS.items():
            folder = npc_root / name / action; folder.mkdir(parents=True, exist_ok=True)
            for frame in range(count): npc_frame(theme, role, action, frame).save(folder / f"{frame}.png")
        npc_frame(theme, role, "idle", 0).save(npc_root / name / "0.png")
    for category in ("weapon", "animated_sprites", "static_sprites"):
        source_root = DEFAULT / "sprites" / category
        target_root = sprites / category
        for source in source_root.rglob("*.png"):
            relative = source.relative_to(source_root); target = target_root / relative; target.parent.mkdir(parents=True, exist_ok=True)
            size = Image.open(source).size
            frame = int(source.stem) if source.stem.isdigit() else 0
            renderer = weapon if category == "weapon" else scenery
            if category == "weapon":
                renderer(theme, size, frame).save(target)
            else:
                renderer(theme, size, relative.parts[0], frame).save(target)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--themes", nargs="*", choices=sorted(THEMES), default=sorted(THEMES))
    args = parser.parse_args()
    game_icon().save(ROOT / "assets" / "icon.png")
    for name in args.themes: generate(name, THEMES[name])
    print("Generated original pixel assets for: " + ", ".join(args.themes))


if __name__ == "__main__":
    main()