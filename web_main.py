import asyncio

import pygame as pg

from application.game import Game
from infrastructure.audio import BrowserSound
from infrastructure.scores import BrowserHighScores
from theme import THEMES

WEB_PLAYER_NAME = 'Player 1'
WEB_THEME = THEMES[3]


async def main():
    scores = BrowserHighScores()
    game = Game(WEB_THEME, player_name=WEB_PLAYER_NAME, high_scores=scores, sound_factory=BrowserSound)
    await game.run_async(return_on_exit=False)


if __name__ == '__main__':
    asyncio.run(main())
