import pygame as pg
import sys
import os
import socket
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *


class Game:
    def __init__(self):
        self.configure_display_backend()
        if os.environ.get('SDL_VIDEODRIVER') == 'x11':
            os.environ.setdefault('SDL_VIDEO_WINDOW_POS', '0,0')
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        pg.display.set_caption('POV-Blaster')
        pg.event.set_grab(True)
        pg.mouse.set_pos((HALF_WIDTH, HALF_HEIGHT))
        pg.event.pump()
        pg.mouse.get_rel()
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.state = 'playing'
        self.state_time_remaining = 0
        self.global_trigger = False
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.new_game()

    @staticmethod
    def configure_display_backend():
        if not sys.platform.startswith('linux'):
            return
        if os.environ.get('SDL_VIDEODRIVER'):
            return

        if os.path.isfile('/proc/version') and 'microsoft' in open('/proc/version').read().lower():
            try:
                with open('/proc/net/route') as route_file:
                    route = next(line for line in route_file if line.split()[1] == '00000000')
                gateway = route.split()[2]
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
        self.state = 'playing'
        self.state_time_remaining = 0
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = PathFinding(self)
        pg.mixer.music.play(-1)

    def set_state(self, state):
        self.state = state
        self.state_time_remaining = 1500

    def update(self):
        if self.state != 'playing':
            self.state_time_remaining -= self.delta_time
            if self.state_time_remaining <= 0:
                self.new_game()
            return

        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()

    def draw(self):
        # self.screen.fill('black')
        self.object_renderer.draw()
        self.weapon.draw()
        if self.state == 'victory':
            self.object_renderer.win()
        elif self.state == 'game_over':
            self.object_renderer.game_over()
        # self.map.draw()
        # self.player.draw()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == self.global_event:
                self.global_trigger = True
            if self.state == 'playing':
                self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.delta_time = min(self.clock.tick(FPS), MAX_DELTA_TIME)
            self.update()
            self.draw()
            pg.display.flip()
            pg.display.set_caption(f'{self.clock.get_fps() :.1f}')


if __name__ == '__main__':
    game = Game()
    game.run()
