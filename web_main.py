import asyncio

import pygame as pg

from application.game import Game
from infrastructure.audio import BrowserSound
from infrastructure.scores import BrowserHighScores


async def main():
    pg.init()
    pg.display.set_mode((1600, 900))
    from web_startup import choose_startup

    startup = await choose_startup()
    if startup is None:
        pg.quit()
        return
    player_name, selected_theme = startup
    scores = BrowserHighScores()
    game = Game(selected_theme, player_name=player_name, high_scores=scores, sound_factory=BrowserSound)
    await game.run_async(return_on_exit=False)


if __name__ == '__main__':
    asyncio.run(main())
