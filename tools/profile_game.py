import argparse
import cProfile
import os
import pstats
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')

import pygame as pg

from main import Game
from application.theme import THEMES


def run(frames):
    game = Game(THEMES[3])
    try:
        for _ in range(frames):
            game.update()
            game.draw()
    finally:
        pg.quit()


def main():
    parser = argparse.ArgumentParser(description='Profile headless POV-Blaster frames.')
    parser.add_argument('--frames', type=int, default=30)
    parser.add_argument('--output', default='profile.stats')
    args = parser.parse_args()

    profiler = cProfile.Profile()
    profiler.enable()
    run(max(1, args.frames))
    profiler.disable()
    profiler.dump_stats(args.output)
    pstats.Stats(profiler).strip_dirs().sort_stats('cumulative').print_stats(10)


if __name__ == '__main__':
    main()

