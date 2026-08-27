import sys
import asyncio
import platform
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from application.game import Game
from application.map import choose_map
from application.startup import validate_player_name
from application.theme import THEMES, choose_theme
from infrastructure.scores import HighScores


def choose_player_name(input_func=input, output_func=print):
    while True:
        player_name = input_func('\nPlayer Name: ')
        error = validate_player_name(player_name)
        if error:
            output_func(error)
        else:
            return player_name.strip()


async def run_web():
    from application.web_main import main as web_main

    await web_main()


if sys.platform == 'emscripten' or hasattr(platform, 'window'):
    asyncio.run(run_web())
elif __name__ == '__main__':
    player_name = choose_player_name()
    high_scores = HighScores()
    while True:
        high_scores.display()
        selected_theme = choose_theme()
        if selected_theme is None:
            sys.exit(0)
        selected_map = choose_map()
        if selected_map is None:
            sys.exit(0)
        Game(selected_theme, player_name=player_name, high_scores=high_scores, map_name=selected_map).run()

