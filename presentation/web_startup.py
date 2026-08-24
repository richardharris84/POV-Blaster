"""Async Pygame startup menu for the browser build."""

from __future__ import annotations

import asyncio

import pygame as pg

from application.startup import theme_menu_items, validate_player_name
from infrastructure.settings import HEIGHT, WIDTH

BACKGROUND = (13, 19, 29)
PANEL = (24, 34, 48)
PANEL_ACTIVE = (35, 57, 70)
TEXT = (239, 244, 241)
MUTED = (158, 175, 181)
ACCENT = (255, 196, 76)
DANGER = (255, 112, 105)
BORDER = (72, 95, 105)


def _font(size, bold=False):
    return pg.font.SysFont("dejavusans", size, bold=bold)


def _draw_centered(surface, text, font, color, y):
    rendered = font.render(text, True, color)
    surface.blit(rendered, rendered.get_rect(center=(WIDTH // 2, y)))


def _draw_text(surface, text, font, color, position):
    surface.blit(font.render(text, True, color), position)


def _button(surface, rect, label, selected=False):
    pg.draw.rect(surface, PANEL_ACTIVE if selected else PANEL, rect, border_radius=8)
    pg.draw.rect(surface, ACCENT if selected else BORDER, rect, width=3, border_radius=8)
    rendered = _font(24, bold=True).render(label, True, TEXT)
    surface.blit(rendered, rendered.get_rect(center=rect.center))


def _event_position(event):
    if hasattr(event, 'pos'):
        return event.pos
    if hasattr(event, 'x') and hasattr(event, 'y'):
        return int(event.x * WIDTH), int(event.y * HEIGHT)
    return None


async def choose_startup():
    """Return the selected (player name, theme), or None when Escape is pressed."""
    surface = pg.display.get_surface()
    if surface is None:
        surface = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    player_name = ""
    selected_theme = len(theme_menu_items()) - 1
    phase = "name"
    error = ""
    focused = True
    pg.key.start_text_input()
    try:
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return None
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return None
                    if phase == "name":
                        if event.key == pg.K_BACKSPACE:
                            player_name = player_name[:-1]
                        elif event.key in (pg.K_RETURN, pg.K_KP_ENTER):
                            error = validate_player_name(player_name) or ""
                            if not error:
                                phase = "theme"
                        elif event.key == pg.K_TAB:
                            focused = not focused
                    elif phase == "theme":
                        if event.key in (pg.K_UP, pg.K_w):
                            selected_theme = (selected_theme - 1) % len(theme_menu_items())
                        elif event.key in (pg.K_DOWN, pg.K_s):
                            selected_theme = (selected_theme + 1) % len(theme_menu_items())
                        elif event.key in (pg.K_RETURN, pg.K_KP_ENTER):
                            return player_name.strip(), theme_menu_items()[selected_theme][1]
                elif event.type == pg.TEXTINPUT and phase == "name" and focused:
                    if len(player_name) < 24:
                        player_name += event.text
                elif event.type in (pg.MOUSEBUTTONDOWN, pg.FINGERDOWN):
                    if event.type == pg.MOUSEBUTTONDOWN and event.button != 1:
                        continue
                    pos = _event_position(event)
                    if pos is None:
                        continue
                    if phase == "name":
                        name_rect = pg.Rect(WIDTH // 2 - 300, 250, 600, 64)
                        if name_rect.collidepoint(pos):
                            focused = True
                            pg.key.start_text_input()
                        elif pg.Rect(WIDTH // 2 - 150, 395, 300, 58).collidepoint(pos):
                            error = validate_player_name(player_name) or ""
                            if not error:
                                phase = "theme"
                    else:
                        for index, (_, theme) in enumerate(theme_menu_items()):
                            rect = pg.Rect(WIDTH // 2 - 300, 195 + index * 76, 600, 60)
                            if rect.collidepoint(pos):
                                selected_theme = index
                                return player_name.strip(), theme

            surface.fill(BACKGROUND)
            if phase == "name":
                _draw_centered(surface, "ENTER YOUR NAME", _font(30, bold=True), TEXT, 170)
                name_rect = pg.Rect(WIDTH // 2 - 300, 250, 600, 64)
                pg.draw.rect(surface, PANEL, name_rect, border_radius=8)
                pg.draw.rect(surface, ACCENT if focused else BORDER, name_rect, width=3, border_radius=8)
                _draw_text(surface, player_name or "Type a name...", _font(26), TEXT if player_name else MUTED, (name_rect.x + 20, name_rect.y + 16))
                if focused and (pg.time.get_ticks() // 500) % 2 == 0:
                    caret_x = name_rect.x + 20 + _font(26).size(player_name)[0]
                    pg.draw.rect(surface, ACCENT, (caret_x, name_rect.y + 14, 3, 34))
                if error:
                    _draw_centered(surface, error, _font(20, bold=True), DANGER, 330)
                _button(surface, pg.Rect(WIDTH // 2 - 150, 395, 300, 58), "CONTINUE", selected=True)
                _draw_centered(surface, "Enter to continue  |  Esc to exit", _font(17), MUTED, 535)
            else:
                _draw_centered(surface, f"WELCOME, {player_name.upper()}", _font(27, bold=True), TEXT, 105)
                _draw_centered(surface, "CHOOSE YOUR THEME", _font(22, bold=True), MUTED, 150)
                for index, (number, theme) in enumerate(theme_menu_items()):
                    rect = pg.Rect(WIDTH // 2 - 300, 195 + index * 76, 600, 60)
                    _button(surface, rect, f"{number}  {theme.label}", selected=index == selected_theme)
                _draw_centered(surface, "Game controls: W/A/S/D move  |  Mouse look  |  Left click fire  |  Caps Lock toggles mini-map  |  Esc exit", _font(17), MUTED, 650)
            pg.display.flip()
            clock.tick(60)
            await asyncio.sleep(0)
    finally:
        pg.key.stop_text_input()

