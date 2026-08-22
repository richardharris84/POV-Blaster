from pathlib import Path

import pygame as pg

MAPS_DIR = Path(__file__).resolve().parent / 'maps'
DEFAULT_MAP_NAME = '1_mini_map_default'


def load_map(map_name=DEFAULT_MAP_NAME):
    map_path = MAPS_DIR / f'{map_name}.txt'
    try:
        rows = [line.strip() for line in map_path.read_text(encoding='ascii').splitlines() if line.strip()]
    except FileNotFoundError:
        if map_name != DEFAULT_MAP_NAME:
            return load_map(DEFAULT_MAP_NAME)
        raise

    if not rows or len({len(row) for row in rows}) != 1:
        raise ValueError(f'Map must contain equally sized rows: {map_path}')

    result = []
    for row in rows:
        if any(cell != '.' and not cell.isdigit() for cell in row):
            raise ValueError(f'Map contains an invalid cell: {map_path}')
        result.append([0 if cell == '.' else int(cell) for cell in row])
    return result


class Map:
    def __init__(self, game, map_name=None):
        self.game = game
        self.map_name = map_name or DEFAULT_MAP_NAME
        self.mini_map = load_map(self.map_name)
        self.world_map = {}
        self.rows = len(self.mini_map)
        self.cols = len(self.mini_map[0])
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
         for pos in self.world_map]