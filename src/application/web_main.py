import asyncio

import pygame as pg

from application.game import Game
from infrastructure.audio import BrowserSound
from infrastructure.scores import BrowserHighScores
from infrastructure.settings import SCORE_API_URL
from infrastructure.windowing import set_game_icon


async def main():
    pg.init()
    pg.display.set_mode((1600, 900))
    set_game_icon()
    from presentation.web_startup import choose_startup

    scores = BrowserHighScores(api_url=SCORE_API_URL)
    player_name = None
    session_recorded = False
    while True:
        startup = await choose_startup(player_name=player_name, high_scores=scores)
        if startup is None:
            pg.quit()
            return
        player_name, selected_theme, selected_map = startup
        if not session_recorded:
            scores.record_session(player_name)  # Record that this player started a web session
            session_recorded = True
        game = Game(selected_theme, player_name=player_name, high_scores=scores, sound_factory=BrowserSound,
                    map_name=selected_map)
        await game.run_async(return_on_exit=True, browser_mode=True)


if __name__ == '__main__':
    asyncio.run(main())

