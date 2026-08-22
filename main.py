import sys

from application.game import Game
from theme import choose_theme


if __name__ == '__main__':
    selected_theme = choose_theme()
    if selected_theme is None:
        sys.exit(0)
    Game(selected_theme).run()
