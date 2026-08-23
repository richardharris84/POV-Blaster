import pygame as pg
import os
import re
import math
from collections import deque
from settings import (DELTA_ANGLE, HALF_HEIGHT, HALF_NUM_RAYS, HALF_WIDTH,
                      NUM_RAYS, RAY_EPSILON, SCALE, SCREEN_DIST, WIDTH)
from infrastructure.assets import create_fallback_surface, resolve_resource_path
from application.ports import GameContext


class SpriteObject:
    def __init__(self, game: GameContext, path='sprites/static_sprites/candlebra.png',
                 pos=(10.5, 3.5), scale=0.7, shift=0.27):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = game.asset_loader.load_image(game.theme.path(path), fallback_label='S')
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj
        width_px, height_px = max(1, int(proj_width)), max(1, int(proj_height))

        # cache the scaled (but not yet depth-masked) sprite: many NPCs of the same
        # type/frame share the same source Surface, so this reuses work across actors,
        # not just across frames of one actor.
        renderer = self.game.object_renderer
        cached = renderer.cached_scale(
            renderer.sprite_scale_cache, (id(self.image), width_px, height_px),
            lambda: pg.transform.scale(self.image, (width_px, height_px)),
        )

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2 + height_shift

        depth_buffer = self.game.raycasting.depth_buffer
        if depth_buffer:
            image = cached.copy()
            for image_x in range(image.get_width()):
                ray = int((pos[0] + image_x) / SCALE)
                if 0 <= ray < len(depth_buffer) and depth_buffer[ray] < self.norm_dist:
                    image.fill((0, 0, 0, 0), (image_x, 0, 1, image.get_height()))
        else:
            image = cached

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta / DELTA_ANGLE
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()


class AnimatedSprite(SpriteObject):
    def __init__(self, game, path='sprites/animated_sprites/green_light/0.png',
                 pos=(11.5, 3.5), scale=0.8, shift=0.16, animation_time=120):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = game.theme.path(path).parent
        self.images = self.get_images(self.path)
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def get_images(self, path):
        images = deque()
        resource_path = resolve_resource_path(path)
        if not resource_path.exists():
            return deque([create_fallback_surface((64, 64), 'A')])

        image_files = [
            file_name for file_name in os.listdir(resource_path)
            if os.path.isfile(os.path.join(resource_path, file_name))
            and os.path.splitext(file_name)[1].lower() in {'.png', '.jpg', '.jpeg'}
        ]
        def frame_sort_key(name):
            stem = os.path.splitext(name)[0]
            match = re.search(r'(\d+)$', stem)
            return int(match.group(1)) if match else 0, stem

        if not image_files:
            return deque([create_fallback_surface((64, 64), 'A')])

        for file_name in sorted(image_files, key=frame_sort_key):
            images.append(self.game.asset_loader.load_image(resource_path / file_name,
                                                            fallback_label=file_name[0].upper()))
        return images
