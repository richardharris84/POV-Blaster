"""Async Pygame startup menu for the browser build."""

from __future__ import annotations

import asyncio
import platform
import sys

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
FOOTER_Y = HEIGHT - 28
NAME_RECT = pg.Rect(WIDTH // 2 - 300, 250, 600, 64)
CONTINUE_RECT = pg.Rect(WIDTH // 2 - 150, 395, 300, 58)
PRIVACY_RECT = pg.Rect(WIDTH // 2 - 120, 475, 240, 32)
START_GAME_RECT = pg.Rect(WIDTH // 2 - 150, 635, 300, 58)
BROWSER_NAME_INPUT_TOP = f"{(NAME_RECT.centery / HEIGHT) * 100:.4f}%"
BROWSER_NAME_INPUT_WIDTH = f"{(NAME_RECT.width / WIDTH) * 100:.4f}vw"
BROWSER_NAME_INPUT_HEIGHT = f"{(NAME_RECT.height / HEIGHT) * 100:.4f}vh"


def _font(size, bold=False):
    return pg.font.SysFont("dejavusans", size, bold=bold)


def _draw_centered(surface, text, font, color, y):
    rendered = font.render(text, True, color)
    surface.blit(rendered, rendered.get_rect(center=(WIDTH // 2, y)))


def _draw_text(surface, text, font, color, position):
    surface.blit(font.render(text, True, color), position)


def _draw_footer(surface):
    _draw_centered(surface, "Built by: Richard Harris", _font(17, bold=True), MUTED, FOOTER_Y)


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


def _open_privacy_notice():
    if sys.platform != 'emscripten':
        return
    try:
        platform.window.open('privacy.html', '_blank')
    except (AttributeError, TypeError):
        pass


class _BrowserNameInput:
    """Bridge the canvas name field to the mobile browser keyboard."""

    def __init__(self, on_change):
        self.element = None
        if sys.platform != "emscripten":
            return
        try:
            document = platform.document
            element = document.createElement("input")
            element.type = "text"
            element.maxLength = 24
            element.autocomplete = "off"
            element.autocapitalize = "words"
            element.spellcheck = False
            element.setAttribute("aria-label", "Player name")
            element.style.position = "fixed"
            element.style.left = "50%"
            element.style.top = BROWSER_NAME_INPUT_TOP
            element.style.transform = "translate(-50%, -50%)"
            # A near-zero-size input breaks caret tracking on some mobile
            # keyboards, which insert every keystroke at position 0 instead of
            # the end (typing "Richard" renders as "drahcIR"). Give it real
            # dimensions so the browser can compute the caret position correctly.
            element.style.width = BROWSER_NAME_INPUT_WIDTH
            element.style.height = BROWSER_NAME_INPUT_HEIGHT
            element.style.opacity = "0.01"
            element.style.fontSize = "16px"
            element.style.border = "0"
            element.style.padding = "0"
            element.style.margin = "0"
            element.style.background = "transparent"
            element.style.color = "transparent"
            element.style.caretColor = "transparent"
            element.style.outline = "none"
            element.style.boxSizing = "border-box"
            element.style.zIndex = "2147483647"
            element.addEventListener("input", on_change)
            document.body.appendChild(element)
            self.element = element
        except Exception:
            self.element = None

    def focus(self):
        if self.element is not None:
            self.element.focus()

    def set_value(self, value):
        if self.element is not None and self.element.value != value:
            self.element.value = value

    def value(self):
        return "" if self.element is None else str(self.element.value)

    def close(self):
        if self.element is not None:
            self.element.remove()
            self.element = None


    def deactivate(self):
        if self.element is not None:
            try:
                self.element.blur()
            except (AttributeError, TypeError):
                pass
            self.close()


def _browser_event_target(event, browser_name_input):
    if browser_name_input is None:
        return None
    try:
        target = event.target
    except (AttributeError, TypeError):
        target = None
    return target if target is not None else browser_name_input.element


async def choose_startup():
    """Return the selected (player name, theme), or None when Escape is pressed."""
    surface = pg.display.get_surface()
    if surface is None:
        surface = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    player_name = ""
    selected_theme = next(
        index for index, (_, theme) in enumerate(theme_menu_items())
        if theme.key == 'hunting'
    )
    phase = "name"
    error = ""
    focused = True
    browser_name_input = None
    browser_name_input_holder = {"input": None}

    def browser_name_changed(event):
        nonlocal player_name
        current_browser_name_input = browser_name_input_holder["input"]
        target = _browser_event_target(event, current_browser_name_input)
        try:
            value = str(target.value)
        except (AttributeError, TypeError):
            value = "" if current_browser_name_input is None else current_browser_name_input.value()
        player_name = value[:24]
        if current_browser_name_input is not None:
            current_browser_name_input.set_value(player_name)
        # Defensive: force the caret to stay at the end so a stray reset
        # cannot cause subsequent keystrokes to insert at the start again.
        try:
            if target is not None:
                target.setSelectionRange(len(player_name), len(player_name))
        except Exception:
            pass

    browser_name_input = _BrowserNameInput(browser_name_changed)
    browser_name_input_holder["input"] = browser_name_input
    pg.key.start_text_input()

    def advance_to_theme():
        nonlocal error, phase
        error = validate_player_name(player_name) or ""
        if error:
            return
        phase = "theme"
        browser_name_input.deactivate()

    browser_name_input.focus()
    try:
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return None
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return None
                    if phase == "name":
                        if event.key == pg.K_BACKSPACE and browser_name_input.element is None:
                            player_name = player_name[:-1]
                        elif event.key in (pg.K_RETURN, pg.K_KP_ENTER):
                            advance_to_theme()
                        elif event.key == pg.K_TAB:
                            focused = not focused
                    elif phase == "theme":
                        if event.key in (pg.K_UP, pg.K_w):
                            selected_theme = (selected_theme - 1) % len(theme_menu_items())
                        elif event.key in (pg.K_DOWN, pg.K_s):
                            selected_theme = (selected_theme + 1) % len(theme_menu_items())
                        elif event.key in (pg.K_RETURN, pg.K_KP_ENTER):
                            return player_name.strip(), theme_menu_items()[selected_theme][1]
                elif event.type == pg.TEXTINPUT and browser_name_input.element is None and phase == "name" and focused:
                    if len(player_name) < 24:
                        player_name += event.text
                        browser_name_input.set_value(player_name)
                elif event.type in (pg.MOUSEBUTTONDOWN, pg.FINGERDOWN):
                    if event.type == pg.MOUSEBUTTONDOWN and event.button != 1:
                        continue
                    pos = _event_position(event)
                    if pos is None:
                        continue
                    if phase == "name":
                        if NAME_RECT.collidepoint(pos):
                            focused = True
                            pg.key.start_text_input()
                            browser_name_input.focus()
                        elif CONTINUE_RECT.collidepoint(pos):
                            advance_to_theme()
                        elif PRIVACY_RECT.collidepoint(pos):
                            _open_privacy_notice()
                    else:
                        for index, (_, theme) in enumerate(theme_menu_items()):
                            rect = pg.Rect(WIDTH // 2 - 300, 195 + index * 76, 600, 60)
                            if rect.collidepoint(pos):
                                selected_theme = index
                        if START_GAME_RECT.collidepoint(pos):
                            return player_name.strip(), theme_menu_items()[selected_theme][1]

            surface.fill(BACKGROUND)
            if phase == "name":
                _draw_centered(surface, "ENTER YOUR NAME", _font(30, bold=True), TEXT, 170)
                pg.draw.rect(surface, PANEL, NAME_RECT, border_radius=8)
                pg.draw.rect(surface, ACCENT if focused else BORDER, NAME_RECT, width=3, border_radius=8)
                _draw_text(surface, player_name or "Type a name...", _font(26), TEXT if player_name else MUTED, (NAME_RECT.x + 20, NAME_RECT.y + 16))
                if focused and (pg.time.get_ticks() // 500) % 2 == 0:
                    caret_x = NAME_RECT.x + 20 + _font(26).size(player_name)[0]
                    pg.draw.rect(surface, ACCENT, (caret_x, NAME_RECT.y + 14, 3, 34))
                if error:
                    _draw_centered(surface, error, _font(20, bold=True), DANGER, 330)
                _button(surface, CONTINUE_RECT, "CONTINUE", selected=True)
                _draw_centered(surface, "Privacy Notice", _font(18, bold=True), ACCENT, 490)
                _draw_centered(surface, "Enter to continue  |  Esc to exit", _font(17), MUTED, 555)
                _draw_centered(surface, "Mobile controls: left joystick moves  |  right joystick looks  |  tap right joystick to fire", _font(17), MUTED, 610)
            else:
                _draw_centered(surface, f"WELCOME, {player_name.upper()}", _font(27, bold=True), TEXT, 105)
                _draw_centered(surface, "CHOOSE YOUR THEME", _font(22, bold=True), MUTED, 150)
                for index, (number, theme) in enumerate(theme_menu_items()):
                    rect = pg.Rect(WIDTH // 2 - 300, 195 + index * 76, 600, 60)
                    _button(surface, rect, f"{number}  {theme.label}", selected=index == selected_theme)
                _button(surface, START_GAME_RECT, "START GAME", selected=True)
                _draw_centered(surface, "Mobile: left joystick moves  |  right joystick looks  |  tap right joystick to fire", _font(17), MUTED, 730)
                _draw_centered(surface, "Enter selects  |  Esc exits", _font(17), MUTED, 765)
            _draw_footer(surface)
            pg.display.flip()
            clock.tick(60)
            await asyncio.sleep(0)
    finally:
        pg.key.stop_text_input()
        browser_name_input.close()
