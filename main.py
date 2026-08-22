import sys

from application.game import Game
from theme import choose_theme
from infrastructure.scores import HighScores


def choose_player_name(input_func=input):
    while True:
        player_name = input_func('\nPlayer Name: ').strip()
        if player_name:
            return player_name
        print('Player name cannot be empty.')


if __name__ == '__main__':
    player_name = choose_player_name()
    high_scores = HighScores()
    while True:
        high_scores.display()
        selected_theme = choose_theme()
        if selected_theme is None:
            sys.exit(0)
        Game(selected_theme, player_name=player_name, high_scores=high_scores).run()
