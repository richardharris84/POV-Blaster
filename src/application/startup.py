"""Shared startup-menu rules used by desktop and web frontends."""

from __future__ import annotations

import re

from application.theme import THEMES

PROFANITY_PATTERN = re.compile(
    r"(?i)(?:\bass(?:hole)?\b|\bbastard\b|\bbitch\b|\bcrap\b|\bcunt\b|\bdick\b|\bfuck\b|\bpiss\b|\bshit\b|\bslut\b|\bwhore\b)"
)


def validate_player_name(name: str) -> str | None:
    """Return a user-facing error, or None when the name is acceptable."""
    candidate = name.strip()
    if not candidate:
        return "Player name cannot be empty."
    if PROFANITY_PATTERN.search(candidate):
        return "Please enter a different name."
    return None


def theme_menu_items():
    """Return the same ordered theme data displayed by the console menu."""
    return tuple((index, theme) for index, theme in enumerate(THEMES, start=1))

