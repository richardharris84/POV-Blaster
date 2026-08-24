import math
from pathlib import Path

import pygame as pg

from infrastructure.settings import FLOOR_COLOR, HALF_HEIGHT, HEIGHT, RES, SCALE, TEXTURE_SIZE, WIDTH
from infrastructure.assets import AssetLoader


class ObjectRenderer:
    # bounds the per-round wall/sprite scale caches so a long session can't grow them
    # unboundedly; simply cleared on overflow rather than true LRU, since a full
    # raycasting-heavy renderer regenerates most entries within a handful of frames.
    SCALE_CACHE_LIMIT = 4096

    def __init__(self, game, image_loader=None):
        self.game = game
        self.screen = game.screen
        self.image_loader = image_loader or game.asset_loader.load_image
        self.wall_textures = self.load_wall_textures()
        self.wall_column_cache = {}
        self.sprite_scale_cache = {}
        self.sky_image = self.get_texture('textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('textures/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('textures/game_over.png', RES)
        self.win_image = self.get_texture('textures/win.png', RES)

    def cached_scale(self, cache, key, build_fn):
        cached = cache.get(key)
        if cached is None:
            cached = build_fn()
            if len(cache) >= self.SCALE_CACHE_LIMIT:
                cache.clear()
            cache[key] = cached
        return cached

    def draw(self, snapshot=None):
        self.draw_background()
        self.render_game_objects(snapshot)
        self.draw_player_health()
        self.draw_player_kills()
        self.draw_minimap()

    def draw_minimap(self):
        if not self.game.minimap_enabled:
            return

        map_grid = getattr(self.game.map, 'mini_map', None)
        if not map_grid or not map_grid[0]:
            return

        map_w = len(map_grid[0])
        map_h = len(map_grid)
        panel_size = 170
        margin = 12
        cell = max(4, min((panel_size / max(map_w, map_h)), 12))
        panel_w = max(4, cell * map_w)
        panel_h = max(4, cell * map_h)
        minimap = pg.Surface((panel_w + 2, panel_h + 2), pg.SRCALPHA)
        pg.draw.rect(minimap, (18, 22, 28, 190), minimap.get_rect(), border_radius=8)
        pg.draw.rect(minimap, (120, 130, 145, 200), minimap.get_rect(), width=2, border_radius=8)

        for y, row in enumerate(map_grid):
            for x, value in enumerate(row):
                if value:
                    pg.draw.rect(minimap, (214, 214, 214), (x * cell + 1, y * cell + 1, cell - 1, cell - 1))

        player_x = self.game.player.x * cell
        player_y = self.game.player.y * cell
        dir_x = math.cos(self.game.player.angle) * (cell * 1.5)
        dir_y = math.sin(self.game.player.angle) * (cell * 1.5)

        if hasattr(self.game, 'object_handler') and getattr(self.game.object_handler, 'npc_list', None):
            for npc in self.game.object_handler.npc_list:
                if getattr(npc, 'alive', False):
                    enemy_x = npc.x * cell
                    enemy_y = npc.y * cell
                    pg.draw.circle(minimap, (220, 50, 50), (int(enemy_x) + 1, int(enemy_y) + 1), max(2, int(cell * 0.35)))

        pg.draw.line(minimap, (120, 255, 80), (player_x + 1, player_y + 1), (player_x + dir_x + 1, player_y + dir_y + 1), 2)
        pg.draw.circle(minimap, (120, 255, 80), (int(player_x) + 1, int(player_y) + 1), max(3, int(cell * 0.35)))

        health_height = self.digit_size
        self.screen.blit(minimap, (margin, health_height + margin * 2))

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        health = str(max(0, self.game.player.health))
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

    def draw_player_kills(self):
        kills = str(max(0, self.game.player.kills))
        if not kills:
            kills = '0'
        start_x = WIDTH - ((len(kills) + 1) * self.digit_size) - 16
        for i, char in enumerate(kills):
            self.screen.blit(self.digits[char], (start_x + (i * self.digit_size), 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))
        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self, snapshot=None):
        objects = snapshot.objects if snapshot is not None else self.game.raycasting.objects_to_render
        list_objects = sorted(objects, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    def get_texture(self, path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        return self.image_loader(self.game.theme.path(path), size=res, alpha=True,
                                 fallback_label=Path(path).stem[:1].upper())

    def load_wall_textures(self):
        return {
            1: self.get_texture('textures/1.png'),
            2: self.get_texture('textures/2.png'),
            3: self.get_texture('textures/3.png'),
            4: self.get_texture('textures/4.png'),
            5: self.get_texture('textures/5.png'),
        }

