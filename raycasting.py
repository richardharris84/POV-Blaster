import pygame as pg
import math
from settings import (DELTA_ANGLE, FOV, HALF_FOV, HALF_HEIGHT, HALF_TEXTURE_SIZE,
                      MAX_DEPTH, NUM_RAYS, RAY_EPSILON, SCALE, SCREEN_DIST,
                      TEXTURE_SIZE, HEIGHT)
from application.ports import GameContext


class RayCasting:
    def __init__(self, game: GameContext):
        self.game = game
        self.ray_casting_result = []
        self.depth_buffer = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        self.depth_buffer = [result[0] for result in self.ray_casting_result]
        renderer = self.game.object_renderer
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values
            # snap the continuous offset/height to integer pixel buckets so identical
            # (texture, position, size) combinations reuse a cached scaled surface
            # instead of re-cropping and re-scaling from scratch every single frame.
            src_x = int(offset * (TEXTURE_SIZE - SCALE))

            if proj_height < HEIGHT:
                height_px = max(1, int(proj_height))
                wall_column = renderer.cached_scale(
                    renderer.wall_column_cache, ('near', texture, src_x, height_px),
                    lambda tex=texture, x=src_x, h=height_px: pg.transform.scale(
                        self.textures[tex].subsurface(x, 0, SCALE, TEXTURE_SIZE), (SCALE, h)
                    ),
                )
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = max(1, int(TEXTURE_SIZE * HEIGHT / proj_height))
                src_y = int(HALF_TEXTURE_SIZE - texture_height // 2)
                wall_column = renderer.cached_scale(
                    renderer.wall_column_cache, ('far', texture, src_x, src_y, texture_height),
                    lambda tex=texture, x=src_x, y=src_y, th=texture_height: pg.transform.scale(
                        self.textures[tex].subsurface(x, y, SCALE, th), (SCALE, HEIGHT)
                    ),
                )
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []
        texture_vert, texture_hor = 1, 1
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)
            if abs(sin_a) < RAY_EPSILON:
                sin_a = RAY_EPSILON if sin_a >= 0 else -RAY_EPSILON
            if abs(cos_a) < RAY_EPSILON:
                cos_a = RAY_EPSILON if cos_a >= 0 else -RAY_EPSILON

            # horizontals
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # depth, texture offset
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # remove fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # projection
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # ray casting result
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()