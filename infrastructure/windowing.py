"""Windows-only helpers so the console window and the pygame game window play
nicely together: the game window opens on whichever monitor shows the console,
takes focus when it opens, and the console regains focus when the game closes.
No-ops on any other platform (Linux/macOS keep their existing behavior)."""

import ctypes
import os
import sys

_IS_WINDOWS = sys.platform == 'win32'
_MONITOR_DEFAULTTONEAREST = 2


class _RECT(ctypes.Structure):
    _fields_ = [('left', ctypes.c_long), ('top', ctypes.c_long),
                ('right', ctypes.c_long), ('bottom', ctypes.c_long)]


class _MONITORINFO(ctypes.Structure):
    _fields_ = [('cbSize', ctypes.c_ulong), ('rcMonitor', _RECT),
                ('rcWork', _RECT), ('dwFlags', ctypes.c_ulong)]


def _console_window_handle():
    if not _IS_WINDOWS:
        return None
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    return hwnd or None


def position_game_window_on_console_monitor(window_size):
    """Set SDL_VIDEO_WINDOW_POS (must be called before pg.display.set_mode()) so the
    game window opens centered on whichever monitor currently shows the console."""
    if not _IS_WINDOWS:
        return
    hwnd = _console_window_handle()
    if hwnd is None:
        return
    try:
        monitor = ctypes.windll.user32.MonitorFromWindow(hwnd, _MONITOR_DEFAULTTONEAREST)
        info = _MONITORINFO()
        info.cbSize = ctypes.sizeof(_MONITORINFO)
        if not ctypes.windll.user32.GetMonitorInfoW(monitor, ctypes.byref(info)):
            return
        work = info.rcWork
        width, height = window_size
        x = work.left + max(0, ((work.right - work.left) - width) // 2)
        y = work.top + max(0, ((work.bottom - work.top) - height) // 2)
        os.environ['SDL_VIDEO_WINDOW_POS'] = f'{x},{y}'
    except OSError:
        pass


def focus_game_window():
    """Bring the just-opened pygame window to the foreground, above the console."""
    if not _IS_WINDOWS:
        return
    try:
        import pygame as pg
        hwnd = pg.display.get_wm_info().get('window')
        if hwnd:
            ctypes.windll.user32.SetForegroundWindow(hwnd)
    except (ImportError, OSError, KeyError):
        pass


def focus_console_window():
    """Bring the console back to the foreground, e.g. after Esc closes the game
    window and control returns to the console's theme/name menu."""
    hwnd = _console_window_handle()
    if hwnd is None:
        return
    try:
        ctypes.windll.user32.SetForegroundWindow(hwnd)
    except OSError:
        pass
