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
FOOTER_RECT = pg.Rect(WIDTH // 2 - 140, HEIGHT - 48, 280, 32)
NAME_RECT = pg.Rect(WIDTH // 2 - 300, 250, 600, 64)
CONTINUE_RECT = pg.Rect(WIDTH // 2 - 150, 395, 300, 58)
PRIVACY_RECT = pg.Rect(WIDTH // 2 - 120, 475, 240, 32)
START_GAME_RECT = pg.Rect(WIDTH // 2 - 150, 635, 300, 58)


def _font(size, bold=False):
    return pg.font.SysFont("dejavusans", size, bold=bold)


def _draw_centered(surface, text, font, color, y):
    rendered = font.render(text, True, color)
    surface.blit(rendered, rendered.get_rect(center=(WIDTH // 2, y)))


def _draw_text(surface, text, font, color, position):
    surface.blit(font.render(text, True, color), position)


def _draw_footer(surface):
    if sys.platform == "emscripten":
        return
    _draw_centered(surface, "Built by: Richard Harris", _font(17, bold=True), TEXT, FOOTER_Y)


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


def _open_project_link():
    if sys.platform != 'emscripten':
        return
    try:
        platform.window.open('https://github.com/richardharris84/POV-Blaster', '_blank')
    except (AttributeError, TypeError):
        pass


class _BrowserNameInput:
    """Bridge the canvas name field to the mobile browser keyboard."""

    def __init__(self, on_change):
        self.element = None
        self.window = None
        self.document = None
        if sys.platform != "emscripten":
            return
        try:
            self.window = platform.window
            document = platform.document
            self.document = document
            element = document.createElement("input")
            element.type = "text"
            element.maxLength = 24
            element.autocomplete = "off"
            element.autocapitalize = "words"
            element.spellcheck = False
            element.setAttribute("aria-label", "Player name")
            element.style.position = "fixed"
            element.style.margin = "0"
            element.style.padding = "0"
            element.style.border = "none"
            element.style.outline = "none"
            element.style.background = "transparent"
            element.style.color = "transparent"
            element.style.caretColor = "transparent"
            element.style.fontSize = "16px"
            element.style.zIndex = "2147483647"
            element.style.display = "none"
            element.addEventListener("input", on_change)
            document.body.appendChild(element)
            self.element = element
            self.sync_bounds()
        except Exception:
            self.element = None

    def sync_bounds(self):
        if self.element is None or self.window is None:
            return
        try:
            viewport_width = float(self.window.innerWidth)
            viewport_height = float(self.window.innerHeight)
        except (AttributeError, TypeError, ValueError):
            return
        self.element.style.left = f"{NAME_RECT.x * viewport_width / WIDTH:.2f}px"
        self.element.style.top = f"{NAME_RECT.y * viewport_height / HEIGHT:.2f}px"
        self.element.style.width = f"{NAME_RECT.width * viewport_width / WIDTH:.2f}px"
        self.element.style.height = f"{NAME_RECT.height * viewport_height / HEIGHT:.2f}px"

    def activate(self):
        if self.element is not None:
            self.sync_bounds()
            self.element.style.display = "block"
            self.element.style.pointerEvents = "auto"
            self.element.style.opacity = "0.02"

    def deactivate(self):
        if self.element is not None:
            self.element.style.display = "none"
            self.element.style.pointerEvents = "none"
            self.element.style.opacity = "0"
            try:
                self.element.blur()
            except Exception:
                pass

    def focus(self):
        if self.element is not None:
            self.activate()
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


def _browser_event_target(event, browser_name_input):
    if browser_name_input is None:
        return None
    try:
        target = event.target
    except (AttributeError, TypeError):
        target = None
    return target if target is not None else browser_name_input.element


def _browser_input_is_focused(browser_name_input):
    if browser_name_input is None or browser_name_input.element is None:
        return False
    document = getattr(browser_name_input, "document", None)
    if document is None:
        return False
    try:
        return document.activeElement is browser_name_input.element
    except (AttributeError, TypeError):
        return False


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

    def sync_player_name_from_browser():
        nonlocal player_name
        if browser_name_input is None or browser_name_input.element is None:
            return
        current_value = browser_name_input.value()[:24]
        if current_value != player_name:
            player_name = current_value
            browser_name_input.set_value(player_name)

    def advance_to_theme():
        nonlocal error, phase
        sync_player_name_from_browser()
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
                if phase == "name":
                    sync_player_name_from_browser()
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
                elif event.type == pg.TEXTINPUT and phase == "name" and focused:
                    browser_input_focused = _browser_input_is_focused(browser_name_input)
                    if (browser_name_input.element is None or not browser_input_focused) and len(player_name) < 24:
                        player_name += event.text
                        if browser_name_input is not None:
                            browser_name_input.set_value(player_name)
                elif event.type in (pg.MOUSEBUTTONDOWN, pg.FINGERDOWN):
                    if event.type == pg.MOUSEBUTTONDOWN and event.button != 1:
                        continue
                    pos = _event_position(event)
                    if pos is None:
                        continue
                    if FOOTER_RECT.collidepoint(pos):
                        _open_project_link()
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
                browser_name_input.sync_bounds()
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
                _draw_centered(surface, "Enter to continue  |  Esc to exit", _font(17), ACCENT, 490)
                _draw_centered(surface, "Privacy Notice", _font(18, bold=True), MUTED, 555)
                _draw_centered(surface, "Desktop: WASD moves  |  mouse looks  |  left click fires", _font(17), ACCENT, 585)
                _draw_centered(surface, "Mobile controls: left joystick moves  |  right joystick looks  |  tap right joystick to fire", _font(17), ACCENT, 610)
            else:
                _draw_centered(surface, f"WELCOME, {player_name.upper()}", _font(27, bold=True), TEXT, 105)
                _draw_centered(surface, "CHOOSE YOUR THEME", _font(22, bold=True), MUTED, 150)
                for index, (number, theme) in enumerate(theme_menu_items()):
                    rect = pg.Rect(WIDTH // 2 - 300, 195 + index * 76, 600, 60)
                    _button(surface, rect, f"{number}  {theme.label}", selected=index == selected_theme)
                _button(surface, START_GAME_RECT, "START GAME", selected=True)
                _draw_centered(surface, "Desktop: WASD moves  |  mouse looks  |  left click fires", _font(17), ACCENT, 730)
                _draw_centered(surface, "Mobile: left joystick moves  |  right joystick looks  |  tap right joystick to fire", _font(17), ACCENT, 755)
                _draw_centered(surface, "Enter selects  |  Esc exits", _font(17), MUTED, 785)
            _draw_footer(surface)
            pg.display.flip()
            clock.tick(60)
            await asyncio.sleep(0)
    finally:
        pg.key.stop_text_input()
        if browser_name_input is not None:
            browser_name_input.close()

