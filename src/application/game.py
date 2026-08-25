import os
import random
import socket
import sys
import asyncio

import pygame as pg

from application.renderer import Renderer
from application.snapshot import RenderSnapshot
from domain.game_state import GameState
from infrastructure.audio import Sound
from infrastructure.assets import AssetLoader
from infrastructure.scores import HighScores
from infrastructure.windowing import (focus_console_window, focus_game_window,
                                      position_game_window_on_console_monitor,
                                      set_game_icon)
from presentation.input import InputAdapter
from presentation.renderer import ObjectRenderer
from presentation.touch import TouchController, is_mobile_touch_device
from infrastructure.settings import FPS, HALF_HEIGHT, HALF_WIDTH, MAX_DELTA_TIME, RES
from application.map import Map
from application.object_handler import ObjectHandler
from application.pathfinding import PathFinding
from application.player import Player
from application.raycasting import RayCasting
from application.weapon import Weapon


class Game:
    def __init__(self, theme, player_name='Player', seed=None, high_scores=None, sound_factory=None):
        self.theme = theme
        self.player_name = player_name
        self.high_scores = high_scores or HighScores()
        self.sound_factory = sound_factory or Sound
        self.score_recorded = False
        self.kill_count = 0
        self.random = random.Random(seed)
        self.configure_display_backend()
        headless = os.environ.get('SDL_VIDEODRIVER') == 'dummy'
        if os.environ.get('SDL_VIDEODRIVER') == 'x11':
            os.environ.setdefault('SDL_VIDEO_WINDOW_POS', '0,0')
        elif not headless:
            position_game_window_on_console_monitor(RES)
        pg.init()
        self.screen = pg.display.set_mode(RES)
        set_game_icon()
        pg.display.set_caption('POV Blaster')
        self.touch_controller = TouchController(*RES) if is_mobile_touch_device() else None
        self.mobile_controls_enabled = self.touch_controller is not None
        pg.mouse.set_visible(self.mobile_controls_enabled)
        if not headless:
            focus_game_window()
        self.mouse_active = self.mobile_controls_enabled
        self.minimap_enabled = True
        self.mouse_center = (HALF_WIDTH, HALF_HEIGHT)
        if os.environ.get('SDL_VIDEODRIVER') != 'x11' and not self.mobile_controls_enabled:
            pg.event.set_grab(True)
            pg.mouse.set_pos(self.mouse_center)
        pg.event.pump()
        pg.mouse.get_rel()
        self.clock = pg.time.Clock()
        self.asset_loader = AssetLoader()
        self.input = InputAdapter()
        self.delta_time = 1
        self.game_state = GameState()
        self.render_snapshot = RenderSnapshot()
        self.global_trigger = False
        self.global_trigger_accum = 0
        pg.event.set_allowed([
            pg.QUIT, pg.KEYDOWN, pg.KEYUP, pg.MOUSEMOTION,
            pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP,
            pg.FINGERDOWN, pg.FINGERMOTION, pg.FINGERUP,
            pg.WINDOWFOCUSGAINED, pg.WINDOWFOCUSLOST,
        ])
        self.new_game()

    def activate_mouse(self):
        if self.mobile_controls_enabled:
            self.mouse_active = True
            return
        if self.mouse_active:
            return
        self.mouse_active = True
        if os.environ.get('SDL_VIDEODRIVER') != 'x11':
            pg.event.set_grab(True)
            pg.mouse.set_pos(self.mouse_center)
        pg.mouse.set_visible(False)
        pg.event.pump()
        pg.mouse.get_rel()

    def ensure_theme_started(self):
        ensure_theme = getattr(getattr(self, 'sound', None), 'ensure_theme_started', None)
        if callable(ensure_theme):
            ensure_theme()

    @staticmethod
    def configure_display_backend():
        if not sys.platform.startswith('linux') or os.environ.get('SDL_VIDEODRIVER'):
            return
        if os.path.isfile('/proc/version') and 'microsoft' in open('/proc/version').read().lower():
            try:
                with open('/proc/net/route') as route_file:
                    gateway = next(line for line in route_file if line.split()[1] == '00000000').split()[2]
                host = socket.inet_ntoa(bytes.fromhex(gateway)[::-1])
                with socket.create_connection((host, 6000), timeout=0.2):
                    os.environ['DISPLAY'] = f'{host}:0'
                    os.environ['SDL_VIDEODRIVER'] = 'x11'
                    os.environ.pop('WAYLAND_DISPLAY', None)
                    return
            except (OSError, StopIteration):
                pass
        if os.environ.get('WAYLAND_DISPLAY'):
            os.environ['SDL_VIDEODRIVER'] = 'wayland'

    def new_game(self):
        self.game_state.set('playing', 0)
        self.score_recorded = False
        self.minimap_enabled = True
        self.map = Map(self)
        self.player = Player(self)
        self.player.kills = self.kill_count
        self.kill_count = self.player.kills
        self.object_renderer: Renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self, self.random)
        self.weapon = Weapon(self)
        # theme (and therefore the sound backend's content) never changes across restarts
        # within one Game instance, so build it once instead of re-decoding every audio
        # file (costly on the web build, which re-embeds base64 <audio> data per instance).
        if getattr(self, 'sound', None) is None:
            self.sound = self.sound_factory(self)
        else:
            self.sound.stop_theme()
        self.pathfinding = PathFinding(self)
        self.render_snapshot = RenderSnapshot()
        self.sound.play_theme()

    def set_state(self, state):
        if state == 'game_over':
            self.record_score()
        self.game_state.set(state)

    def record_score(self):
        if not self.score_recorded:
            self.high_scores.add(self.player_name, self.player.kills)
            self.score_recorded = True

    def reset_kill_count(self):
        self.kill_count = 0
        if getattr(self, 'player', None) is not None:
            self.player.kills = 0

    def update(self):
        if self.game_state.name != 'playing':
            if self.game_state.advance(self.delta_time):
                self.new_game()
            return
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        self.render_snapshot = RenderSnapshot(
            objects=tuple(self.raycasting.objects_to_render),
            player_position=self.player.pos,
            player_angle=self.player.angle,
            player_health=self.player.health,
        )

    def draw(self):
        self.object_renderer.draw(self.render_snapshot)
        self.weapon.draw()
        if self.game_state.name == 'playing' and self.touch_controller is not None:
            self.touch_controller.draw(self.screen)
        if self.game_state.name == 'victory':
            self.object_renderer.win()
        elif self.game_state.name == 'game_over':
            self.object_renderer.game_over()

    def update_global_trigger(self):
        self.global_trigger_accum += self.delta_time
        self.global_trigger = self.global_trigger_accum >= 40
        if self.global_trigger:
            self.global_trigger_accum -= 40

    def check_events(self):
        for event in self.input.poll():
            if self.touch_controller is not None:
                self.touch_controller.handle_event(event)
                if self.game_state.name == 'playing' and self.touch_controller.consume_shoot():
                    self.player.fire()
            if event.type == pg.QUIT:
                if getattr(self, 'browser_mode', False):
                    continue
                self.record_score()
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                return True
            elif event.type == pg.KEYDOWN and event.key == pg.K_CAPSLOCK and self.game_state.name == 'playing':
                self.minimap_enabled = not self.minimap_enabled
            elif event.type == pg.WINDOWFOCUSLOST:
                self.mouse_active = False
                if os.environ.get('SDL_VIDEODRIVER') != 'x11':
                    pg.event.set_grab(False)
            elif event.type == pg.WINDOWFOCUSGAINED:
                self.activate_mouse()
            elif event.type in (pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP, pg.KEYDOWN):
                self.activate_mouse()
                self.ensure_theme_started()
            elif event.type == pg.MOUSEMOTION and self.game_state.name == 'playing':
                if self.mouse_active:
                    self.player.add_mouse_motion(event.rel[0])
            if self.game_state.name == 'playing':
                self.player.single_fire_event(event)
        return False

    def close(self):
        self.record_score()
        pg.event.set_grab(False)
        pg.mouse.set_visible(True)
        self.sound.stop_theme()
        pg.quit()
        if os.environ.get('SDL_VIDEODRIVER') != 'dummy':
            focus_console_window()

    def run(self):
        while True:
            self.ensure_theme_started()
            if self.check_events():
                self.close()
                return
            self.delta_time = min(self.clock.tick(FPS), MAX_DELTA_TIME)
            self.update_global_trigger()
            self.update()
            self.draw()
            pg.display.flip()
            if not getattr(self, 'browser_mode', False):
                pg.display.set_caption(f'{self.clock.get_fps() :.1f}')

    async def run_async(self, return_on_exit=True):
        self.browser_mode = not return_on_exit
        if self.browser_mode:
            pg.display.set_caption('POV Blaster')
        while True:
            self.ensure_theme_started()
            if self.check_events():
                self.record_score()
                if return_on_exit:
                    return
                self.new_game()
                continue
            self.delta_time = min(self.clock.tick(FPS), MAX_DELTA_TIME)
            self.update_global_trigger()
            self.update()
            self.draw()
            pg.display.flip()
            if not self.browser_mode:
                pg.display.set_caption(f'{self.clock.get_fps() :.1f}')
            await asyncio.sleep(0)

