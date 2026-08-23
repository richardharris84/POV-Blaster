"""Collaborators extracted from NPC: visibility, animation selection, and combat
resolution (including its audio side effects) used to all live directly on NPC,
mixing AI/animation/combat/audio in one class. Splitting them out keeps NPC itself
as a thin coordinator over its own state.
"""

import math

from random import random

from settings import HALF_WIDTH, MAX_DEPTH, RAY_EPSILON


def npc_can_see_player(npc):
    """Line-of-sight raycast from an NPC to the player.

    This intentionally duplicates the DDA grid-traversal algorithm in
    raycasting.RayCasting.ray_cast rather than sharing it -- see CodeAudit.md (H2)
    for the follow-up to unify both into one implementation.
    """
    game = npc.game
    if game.player.map_pos == npc.map_pos:
        return True

    wall_dist_v, wall_dist_h = 0, 0
    player_dist_v, player_dist_h = 0, 0

    ox, oy = game.player.pos
    x_map, y_map = game.player.map_pos

    ray_angle = npc.theta

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

    for _ in range(MAX_DEPTH):
        tile_hor = int(x_hor), int(y_hor)
        if tile_hor == npc.map_pos:
            player_dist_h = depth_hor
            break
        if tile_hor in game.map.world_map:
            wall_dist_h = depth_hor
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

    for _ in range(MAX_DEPTH):
        tile_vert = int(x_vert), int(y_vert)
        if tile_vert == npc.map_pos:
            player_dist_v = depth_vert
            break
        if tile_vert in game.map.world_map:
            wall_dist_v = depth_vert
            break
        x_vert += dx
        y_vert += dy
        depth_vert += delta_depth

    player_dist = max(player_dist_v, player_dist_h)
    wall_dist = max(wall_dist_v, wall_dist_h)

    if 0 < player_dist < wall_dist or not wall_dist:
        return True
    return False


class AnimationController:
    """Owns which animation deque an NPC is currently stepping through."""

    def __init__(self, npc):
        self.npc = npc

    def play_idle(self):
        self.npc.animate(self.npc.idle_images)

    def play_walk(self):
        self.npc.animate(self.npc.walk_images)

    def play_attack(self):
        self.npc.animate(self.npc.attack_images)

    def play_pain(self):
        self.npc.animate(self.npc.pain_images)
        if self.npc.animation_trigger:
            self.npc.pain = False

    def play_death(self):
        npc = self.npc
        if npc.game.global_trigger and npc.frame_counter < len(npc.death_images) - 1:
            npc.death_images.rotate(-1)
            npc.image = npc.death_images[0]
            npc.frame_counter += 1


class CombatResolver:
    """Resolves NPC attack/hit/death rules and their audio side effects, kept
    separate from AI/animation so damage/death handling isn't smeared across NPC."""

    def __init__(self, game):
        self.game = game

    def resolve_attack(self, npc):
        if npc.animation_trigger:
            self.game.sound.npc_shot.play()
            if npc.combat.attack_hits(random()):
                self.game.player.get_damage(npc.combat.attack_damage)

    def resolve_hit(self, npc):
        if npc.ray_cast_value and self.game.player.shot:
            if HALF_WIDTH - npc.sprite_half_width < npc.screen_x < HALF_WIDTH + npc.sprite_half_width:
                self.game.sound.npc_pain.play()
                self.game.player.shot = False
                npc.pain = True
                npc.combat.take_damage(self.game.weapon.damage)
                self.resolve_death(npc)

    def resolve_death(self, npc):
        if npc.combat.defeated:
            npc.alive = False
            self.game.player.kills += 1
            self.game.sound.npc_death.play()
