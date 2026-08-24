import math
from random import randint
import pygame as pg
from sprite_object import AnimatedSprite
from domain.combat import Combatant
from npc_systems import AnimationController, CombatResolver, npc_can_see_player
from application.ports import GameContext


class NPC(AnimatedSprite):
    def __init__(self, game: GameContext, path='sprites/npc/soldier/0.png', pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_images = self.get_images(self.path / 'attack')
        self.death_images = self.get_images(self.path / 'death')
        self.idle_images = self.get_images(self.path / 'idle')
        self.pain_images = self.get_images(self.path / 'pain')
        self.walk_images = self.get_images(self.path / 'walk')

        self.attack_dist = randint(3, 6)
        self.speed = 0.03
        self.size = 20
        self.combat = Combatant.create(100, 10, 0.15)
        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.frame_counter = 0
        self.player_search_trigger = False
        self.animation_controller = AnimationController(self)
        self.combat_resolver = CombatResolver(game)
        self.attack_sound_name = 'npc_shot'

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()
        # self.draw_ray_cast()

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.game.player.map_pos)
        next_x, next_y = next_pos

        # pg.draw.rect(self.game.screen, 'blue', (100 * next_x, 100 * next_y, 100, 100))
        if next_pos not in self.game.object_handler.npc_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

    @property
    def health(self):
        return self.combat.health.current

    @health.setter
    def health(self, value):
        self.combat.health.current = max(0, min(self.combat.health.maximum, value))

    @property
    def attack_damage(self):
        return self.combat.attack_damage

    @attack_damage.setter
    def attack_damage(self, value):
        self.combat.attack_damage = value

    @property
    def accuracy(self):
        return self.combat.accuracy

    @accuracy.setter
    def accuracy(self, value):
        self.combat.accuracy = value

    def run_logic(self):
        if self.alive:
            self.ray_cast_value = npc_can_see_player(self)
            self.combat_resolver.resolve_hit(self)

            if self.pain:
                self.animation_controller.play_pain()

            elif self.ray_cast_value:
                self.player_search_trigger = True

                if self.dist < self.attack_dist:
                    self.animation_controller.play_attack()
                    self.combat_resolver.resolve_attack(self)
                else:
                    self.animation_controller.play_walk()
                    self.movement()

            elif self.player_search_trigger:
                self.animation_controller.play_walk()
                self.movement()

            else:
                self.animation_controller.play_idle()
        else:
            self.animation_controller.play_death()

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def draw_ray_cast(self):
        pg.draw.circle(self.game.screen, 'red', (100 * self.x, 100 * self.y), 15)
        if npc_can_see_player(self):
            pg.draw.line(self.game.screen, 'orange', (100 * self.game.player.x, 100 * self.game.player.y),
                         (100 * self.x, 100 * self.y), 2)


class SoldierNPC(NPC):
    def __init__(self, game, path=None, pos=(10.5, 5.5),
                 scale=0.6, shift=0.38, animation_time=180):
        path = path or f'sprites/npc/{game.theme.npc_assets[0]}/0.png'
        super().__init__(game, path, pos, scale, shift, animation_time)

class CacoDemonNPC(NPC):
    def __init__(self, game, path=None, pos=(10.5, 6.5),
                 scale=0.7, shift=0.27, animation_time=250):
        path = path or f'sprites/npc/{game.theme.npc_assets[1]}/0.png'
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 1.0
        self.health = 150
        self.attack_damage = 25
        self.speed = 0.05
        self.accuracy = 0.35

class CyberDemonNPC(NPC):
    def __init__(self, game, path=None, pos=(11.5, 6.0),
                 scale=1.0, shift=0.04, animation_time=210):
        path = path or f'sprites/npc/{game.theme.npc_assets[2]}/0.png'
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 6
        self.health = 350
        self.attack_damage = 15
        self.speed = 0.055
        self.accuracy = 0.25


class HuntingBearNPC(CyberDemonNPC):
    def __init__(self, game, path=None, pos=(11.5, 6.0),
                 scale=1.0, shift=0.04, animation_time=210):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_sound_name = 'bear_roar'





















