import sys
import asyncio
import platform

from application.game import Game
from infrastructure.scores import BrowserHighScores
from theme import THEMES, choose_theme
from infrastructure.scores import HighScores


def choose_player_name(input_func=input):
    while True:
        player_name = input_func('\nPlayer Name: ').strip()
        if player_name:
            return player_name
        print('Player name cannot be empty.')


async def run_web():
    game = Game(THEMES[3], player_name='Player 1', high_scores=BrowserHighScores())
    await game.run_async(return_on_exit=False)


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
        Game(selected_theme, player_name=player_name, high_scores=high_scores).run()
