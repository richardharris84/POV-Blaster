import pygame as pg
import math
import os
import sys
from infrastructure.settings import (HALF_HEIGHT, HALF_WIDTH, HEIGHT, LINUX_MOUSE_SENSITIVITY,
                      MOUSE_BORDER_LEFT, MOUSE_BORDER_RIGHT, MOUSE_MAX_REL,
                      MOUSE_SENSITIVITY, PLAYER_ANGLE, PLAYER_MAX_HEALTH,
                      PLAYER_POS, PLAYER_ROT_SPEED, PLAYER_SIZE_SCALE,
                      PLAYER_SPEED, WEB_MOUSE_SENSITIVITY, MOBILE_TOUCH_SENSITIVITY,
                      MOVEMENT_SMOOTHING_MS, WIDTH)
from domain.health import Health
from domain.movement import movement_delta
from application.ports import GameContext


class Player:
    def __init__(self, game: GameContext):
        self.game = game
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.kills = 0
        self.health_state = Health.full(PLAYER_MAX_HEALTH)
        self.rel = 0
        self.health_recovery_delay = 700
        self.time_prev = pg.time.get_ticks()
        self.mouse_motion = 0
        self.motion_x = 0.0
        self.motion_y = 0.0
        self.diag_move_corr = 1 / math.sqrt(2)

    def add_mouse_motion(self, relative_x):
        if abs(relative_x) <= 1000:
            self.mouse_motion += relative_x

    def recover_health(self):
        if self.check_health_recovery_delay() and self.health < PLAYER_MAX_HEALTH:
            self.health_state.recover()

    def check_health_recovery_delay(self):
        time_now = pg.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def check_game_over(self):
        if self.health < 1:
            self.health = 0
            self.game.record_score()
            self.game.reset_kill_count()
            self.game.set_state('game_over')

    def get_damage(self, damage):
        self.health_state.damage(damage)
        self.game.object_renderer.player_damage()
        self.game.sound.player_pain.play()
        self.check_game_over()

    @property
    def health(self):
        return self.health_state.current

    @health.setter
    def health(self, value):
        self.health_state.current = max(0, min(self.health_state.maximum, value))

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.fire()

    def fire(self):
        if not self.shot and not self.game.weapon.reloading:
            self.game.sound.shotgun.play()
            self.shot = True
            self.game.weapon.reloading = True

    def movement(self):
        speed = PLAYER_SPEED * self.game.delta_time
        touch_controller = getattr(self.game, 'touch_controller', None)
        if touch_controller is not None:
            move_x, move_y, _ = touch_controller.axes()
            target_dx = speed * (move_y * math.cos(self.angle) - move_x * math.sin(self.angle))
            target_dy = speed * (move_y * math.sin(self.angle) + move_x * math.cos(self.angle))
            self.apply_smoothed_motion(target_dx, target_dy)
            self.angle %= math.tau
            return

        keys = pg.key.get_pressed()
        target_dx, target_dy = movement_delta(
            self.angle,
            speed,
            keys[pg.K_w],
            keys[pg.K_s],
            keys[pg.K_a],
            keys[pg.K_d],
        )

        self.apply_smoothed_motion(target_dx, target_dy)

        # if keys[pg.K_LEFT]:
        #     self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        # if keys[pg.K_RIGHT]:
        #     self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau

    def apply_smoothed_motion(self, target_dx, target_dy):
        smoothing = min(1.0, self.game.delta_time / MOVEMENT_SMOOTHING_MS)
        self.motion_x += (target_dx - self.motion_x) * smoothing
        self.motion_y += (target_dy - self.motion_y) * smoothing
        self.check_wall_collision(self.motion_x, self.motion_y)

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
                    (self.x * 100 + WIDTH * math.cos(self.angle),
                     self.y * 100 + WIDTH * math. sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def mouse_control(self):
        touch_controller = getattr(self.game, 'touch_controller', None)
        if touch_controller is not None:
            _, _, turn_x = touch_controller.axes()
            sensitivity = MOBILE_TOUCH_SENSITIVITY if getattr(self.game, 'browser_mode', False) else MOUSE_SENSITIVITY
            self.rel = turn_x * MOUSE_MAX_REL
            self.angle += self.rel * sensitivity
            return

        if not self.game.mouse_active:
            self.rel = 0
            self.mouse_motion = 0
            return

        if os.environ.get('SDL_VIDEODRIVER') == 'x11':
            self.rel = self.mouse_motion
            self.mouse_motion = 0
        else:
            self.rel = pg.mouse.get_rel()[0]
        mx, my = pg.mouse.get_pos()
        if os.environ.get('SDL_VIDEODRIVER') == 'x11':
            self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
            sensitivity = LINUX_MOUSE_SENSITIVITY if sys.platform.startswith('linux') else MOUSE_SENSITIVITY
            self.angle += self.rel * sensitivity
            return
        if mx <= MOUSE_BORDER_LEFT or mx >= MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
            pg.event.pump()
            pg.mouse.get_rel()
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        sensitivity = WEB_MOUSE_SENSITIVITY if getattr(self.game, 'browser_mode', False) else MOUSE_SENSITIVITY
        self.angle += self.rel * sensitivity

    def update(self):
        self.movement()
        self.mouse_control()
        self.recover_health()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
