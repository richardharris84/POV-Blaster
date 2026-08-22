import pygame as pg
from pathlib import Path
from settings import FLOOR_COLOR, HALF_HEIGHT, HEIGHT, RES, SCALE, TEXTURE_SIZE, WIDTH
from infrastructure.assets import AssetLoader


class ObjectRenderer:
    def __init__(self, game, image_loader=None):
        self.game = game
        self.screen = game.screen
        self.image_loader = image_loader or game.asset_loader.load_image
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture('textures/sky.png', (WIDTH, HALF_HEIGHT))
        self.sky_offset = 0
        self.blood_screen = self.get_texture('textures/blood_screen.png', RES)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f'textures/digits/{i}.png', [self.digit_size] * 2)
                             for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture('textures/game_over.png', RES)
        self.win_image = self.get_texture('textures/win.png', RES)

    def draw(self, snapshot=None):
        self.draw_background()
        self.render_game_objects(snapshot)
        self.draw_player_health()

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def draw_player_health(self):
        health = str(max(0, self.game.player.health))
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], (i * self.digit_size, 0))
        self.screen.blit(self.digits['10'], ((i + 1) * self.digit_size, 0))

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
