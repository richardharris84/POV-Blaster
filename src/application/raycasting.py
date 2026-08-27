import pygame as pg
import math
from infrastructure.settings import (DELTA_ANGLE, FOV, HALF_FOV, HALF_HEIGHT, HALF_TEXTURE_SIZE,
                      NUM_RAYS, SCALE, SCREEN_DIST,
                      TEXTURE_SIZE, HEIGHT)
from application.ports import GameContext
from application.ray_engine import cast_wall_ray


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
            shade = renderer.cel_shade(depth)

            if proj_height < HEIGHT:
                height_px = max(1, int(proj_height))
                wall_column = renderer.cached_scale(
                    renderer.wall_column_cache, ('near', texture, src_x, height_px, shade),
                        lambda tex=texture, x=src_x, h=height_px, s=shade: renderer._apply_cel_shading(
                            pg.transform.scale(self.textures[tex].subsurface(x, 0, SCALE, TEXTURE_SIZE), (SCALE, h)), s
                        ),
                )
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = max(1, int(TEXTURE_SIZE * HEIGHT / proj_height))
                src_y = int(HALF_TEXTURE_SIZE - texture_height // 2)
                wall_column = renderer.cached_scale(
                    renderer.wall_column_cache, ('far', texture, src_x, src_y, texture_height, shade),
                    lambda tex=texture, x=src_x, y=src_y, th=texture_height, s=shade: renderer._apply_cel_shading(
                        pg.transform.scale(self.textures[tex].subsurface(x, y, SCALE, th), (SCALE, HEIGHT)), s
                    ),
                )
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):
            depth, texture, offset, _ = cast_wall_ray(
                self.game.player.pos, ray_angle, self.game.map.world_map
            )

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
