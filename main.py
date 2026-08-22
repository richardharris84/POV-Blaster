import sys

from application.game import Game
from theme import choose_theme


def choose_player_name(input_func=input):
    while True:
        player_name = input_func('Player Name: ').strip()
        if player_name:
            return player_name
        print('Player name cannot be empty.')


if __name__ == '__main__':
    player_name = choose_player_name()
    while True:
        selected_theme = choose_theme()
        if selected_theme is None:
            sys.exit(0)
        Game(selected_theme, player_name=player_name).run()
