from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SHEET = ROOT / "assets" / "theme_reference" / "remaining_themes.jpg"
CANVAS = (76, 110)
ANIMATIONS = {"idle": 8, "walk": 8, "attack": 6, "pain": 3, "death": 8}

PANELS = {
    "marshmallow_man": (0, 0, 281, 355),
    "springfield_doughnut": (281, 0, 563, 355),
    "gingerbread_golem": (563, 0, 844, 355),
    "alien_overlord": (1126, 0, 1408, 355),
    "alien_drone": (0, 384, 281, 739),
    "alien_warrior": (281, 384, 563, 739),
    "ghost": (563, 384, 844, 739),
    "vampire": (844, 384, 1126, 739),
    "werewolf": (1126, 384, 1408, 739),
}

THEMES = {
    "candy_kingdom": ("marshmallow_man", "springfield_doughnut", "gingerbread_golem"),
    "space": ("alien_drone", "alien_warrior", "alien_overlord"),
    "graveyard": ("ghost", "vampire", "werewolf"),
}


def extract_base(sheet: Image.Image, bounds: tuple[int, int, int, int]) -> Image.Image:
    image = sheet.crop(bounds).convert("RGBA")
    pixels = image.load()
    for y in range(image.height):
        for x in range(image.width):
            red, green, blue, _ = pixels[x, y]
            value = (red + green + blue) // 3
            if max(red, green, blue) - min(red, green, blue) <= 5 and 25 <= value <= 120:
                pixels[x, y] = (red, green, blue, 0)
    bbox = image.getbbox()
    if bbox is None:
        raise ValueError(f"No character found in panel {bounds}")
    cropped = image.crop(bbox)
    scale = min(CANVAS[0] / cropped.width, CANVAS[1] / cropped.height)
    size = (max(1, int(cropped.width * scale)), max(1, int(cropped.height * scale)))
    resized = cropped.resize(size, Image.Resampling.NEAREST)
    result = Image.new("RGBA", CANVAS)
    result.alpha_composite(resized, ((CANVAS[0] - size[0]) // 2, CANVAS[1] - size[1]))
    return result


def frame(base: Image.Image, action: str, index: int) -> Image.Image:
    result = Image.new("RGBA", CANVAS)
    if action == "idle":
        offset = (index % 4) - 1
        result.alpha_composite(base, (offset, 0 if index % 2 else 1))
    elif action == "walk":
        offset = -2 if index % 2 else 2
        result.alpha_composite(base, (offset, 2 if index % 4 in (1, 2) else 0))
    elif action == "attack":
        result.alpha_composite(base, (min(index, 2), -min(index, 2)))
    elif action == "pain":
        result.alpha_composite(base, (-2 if index % 2 else 2, 0))
        draw = ImageDraw.Draw(result)
        draw.ellipse((49, 42, 61, 54), fill=(224, 62, 48, 220))
    else:
        faded = base.copy()
        faded.putalpha(faded.getchannel("A").point(lambda alpha: max(0, alpha * (7 - index) // 7)))
        result.alpha_composite(faded, (index * 2 - 7, index * 2))
    return result


def main() -> None:
    sheet = Image.open(SHEET).convert("RGB")
    for theme, characters in THEMES.items():
        for character in characters:
            target = ROOT / "assets" / "themes" / theme / "sprites" / "npc" / character
            base = extract_base(sheet, PANELS[character])
            target.mkdir(parents=True, exist_ok=True)
            for action, count in ANIMATIONS.items():
                folder = target / action
                folder.mkdir(exist_ok=True)
                for index in range(count):
                    frame(base, action, index).save(folder / f"{index}.png")
            base.save(target / "0.png")
    print("Imported reference-sheet NPCs for: " + ", ".join(THEMES))


if __name__ == "__main__":
    main()