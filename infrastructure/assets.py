from pathlib import Path

import pygame as pg

from infrastructure.settings import BASE_DIR


def resolve_resource_path(path):
    path = Path(path)
    return path if path.is_absolute() else BASE_DIR / path


def create_fallback_surface(size=(64, 64), label='?', bg=(44, 44, 44), accent=(220, 220, 220)):
    width, height = size
    surface = pg.Surface((width, height), flags=pg.SRCALPHA)
    surface.fill(bg)
    for y in range(0, height, 8):
        for x in range(0, width, 8):
            if (x // 8 + y // 8) % 2 == 0:
                surface.fill((max(0, bg[0] - 15), max(0, bg[1] - 15), max(0, bg[2] - 15), 255), (x, y, 8, 8))
    pg.draw.line(surface, accent, (0, 0), (width, height), 2)
    pg.draw.line(surface, accent, (width, 0), (0, height), 2)
    font = pg.font.SysFont('arial', max(10, min(width, height) // 4), bold=True)
    label_surface = font.render(str(label), True, accent)
    label_rect = label_surface.get_rect(center=(width // 2, height // 2))
    surface.blit(label_surface, label_rect)
    return surface


class AssetLoader:
    def __init__(self):
        self.cache = {}

    def load_image(self, path, size=None, alpha=True, fallback_label='?'):
        cache_key = (str(path), tuple(size) if size else None, alpha, fallback_label)
        if cache_key in self.cache:
            return self.cache[cache_key]

        resource_path = resolve_resource_path(path)
        try:
            surface = pg.image.load(str(resource_path))
        except (FileNotFoundError, OSError, pg.error):
            surface = create_fallback_surface(size or (64, 64), fallback_label)
        else:
            surface = surface.convert_alpha() if alpha else surface.convert()

        if size is not None:
            surface = pg.transform.scale(surface, size)

        self.cache[cache_key] = surface
        return surface

