"""Collaborators extracted from NPC: visibility, animation selection, and combat
resolution (including its audio side effects) used to all live directly on NPC,
mixing AI/animation/combat/audio in one class. Splitting them out keeps NPC itself
as a thin coordinator over its own state.
"""

import math

from random import random

from infrastructure.settings import HALF_WIDTH
from application.ray_engine import cast_wall_ray


def npc_can_see_player(npc):
    """Line-of-sight raycast from an NPC to the player.

    The wall distance comes from the same DDA implementation used for rendering.
    """
    game = npc.game
    if game.player.map_pos == npc.map_pos:
        return True

    wall_dist, _, _, _ = cast_wall_ray(
        game.player.pos, npc.theta, game.map.world_map
    )
    player_dist = math.hypot(npc.x - game.player.x, npc.y - game.player.y)
    return player_dist < wall_dist


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
            attack_sound = getattr(self.game.sound, npc.attack_sound_name, self.game.sound.npc_shot)
            attack_sound.play()
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
            self.game.kill_count = self.game.player.kills
            self.game.sound.npc_death.play()

