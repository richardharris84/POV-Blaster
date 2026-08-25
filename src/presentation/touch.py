from __future__ import annotations

import math
import sys
from dataclasses import dataclass

import pygame as pg


MOBILE_USER_AGENT_HINTS = (
    'android',
    'iphone',
    'ipad',
    'ipod',
    'mobile',
    'tablet',
)


def is_mobile_touch_device() -> bool:
    if sys.platform != 'emscripten':
        return False
    return _has_touch_device() or _user_agent_looks_mobile()


def _has_touch_device() -> bool:
    get_num_devices = getattr(getattr(pg, 'touch', None), 'get_num_devices', None)
    if not callable(get_num_devices):
        return False
    try:
        return get_num_devices() > 0
    except Exception:
        return False


def _user_agent_looks_mobile() -> bool:
    try:
        import platform

        window = getattr(platform, 'window', None)
        navigator = getattr(window, 'navigator', None)
        user_agent = str(getattr(navigator, 'userAgent', '')).lower()
        return any(token in user_agent for token in MOBILE_USER_AGENT_HINTS)
    except Exception:
        return False


@dataclass
class FingerState:
    origin: tuple[float, float]
    position: tuple[float, float]
    started_ms: int
    moved: bool = False


class TouchController:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.radius = max(46.0, min(width, height) * 0.11)
        self.knob_radius = self.radius * 0.45
        margin_x = max(28.0, width * 0.07)
        margin_y = max(24.0, height * 0.08)
        self.left_anchor = (margin_x + self.radius, height - margin_y - self.radius)
        self.right_anchor = (width - margin_x - self.radius, height - margin_y - self.radius)
        self.left_finger_id: int | None = None
        self.right_finger_id: int | None = None
        self.left_finger: FingerState | None = None
        self.right_finger: FingerState | None = None
        self.other_touches: dict[int, FingerState] = {}
        self.tap_ms_threshold = 220
        self.tap_drag_threshold = max(12.0, self.radius * 0.22)
        self._shoot_queued = False

    def handle_event(self, event: object) -> None:
        event_type = getattr(event, 'type', None)
        if event_type == pg.FINGERDOWN:
            self._on_finger_down(event)
        elif event_type == pg.FINGERMOTION:
            self._on_finger_motion(event)
        elif event_type == pg.FINGERUP:
            self._on_finger_up(event)

    def axes(self) -> tuple[float, float, float]:
        left = self._normalized_vector(self.left_finger)
        right = self._normalized_vector(self.right_finger)
        move_x = self._deadzone(left[0], 0.12)
        move_y = self._deadzone(-left[1], 0.12)
        turn_x = self._deadzone(right[0], 0.08)
        return move_x, move_y, turn_x

    def consume_shoot(self) -> bool:
        queued = self._shoot_queued
        self._shoot_queued = False
        return queued

    def draw(self, surface: pg.Surface) -> None:
        self._draw_stick(surface, self.left_anchor, self.left_finger)
        self._draw_stick(surface, self.right_anchor, self.right_finger)

    def _on_finger_down(self, event) -> None:
        finger_id = int(event.finger_id)
        position = self._to_pixels(event.x, event.y)
        state = FingerState(position, position, pg.time.get_ticks())
        if self.left_finger_id is None and self._in_left_zone(position):
            self.left_finger_id = finger_id
            self.left_finger = state
            return
        if self.right_finger_id is None and self._in_right_zone(position):
            self.right_finger_id = finger_id
            self.right_finger = state
            return
        self.other_touches[finger_id] = state

    def _on_finger_motion(self, event) -> None:
        finger_id = int(event.finger_id)
        position = self._to_pixels(event.x, event.y)
        if finger_id == self.left_finger_id and self.left_finger is not None:
            self._update_finger_state(self.left_finger, position)
            return
        if finger_id == self.right_finger_id and self.right_finger is not None:
            self._update_finger_state(self.right_finger, position)
            return
        state = self.other_touches.get(finger_id)
        if state is not None:
            self._update_finger_state(state, position)

    def _on_finger_up(self, event) -> None:
        finger_id = int(event.finger_id)
        now = pg.time.get_ticks()
        if finger_id == self.left_finger_id and self.left_finger is not None:
            self.left_finger_id = None
            self.left_finger = None
            return
        if finger_id == self.right_finger_id and self.right_finger is not None:
            state = self.right_finger
            self.right_finger_id = None
            self.right_finger = None
            duration = now - state.started_ms
            if duration <= self.tap_ms_threshold and not state.moved:
                self._shoot_queued = True
            return
        self.other_touches.pop(finger_id, None)

    def _update_finger_state(self, state: FingerState, position: tuple[float, float]) -> None:
        state.position = position
        dx = position[0] - state.origin[0]
        dy = position[1] - state.origin[1]
        if dx * dx + dy * dy >= self.tap_drag_threshold * self.tap_drag_threshold:
            state.moved = True

    def _normalized_vector(self, state: FingerState | None) -> tuple[float, float]:
        if state is None:
            return 0.0, 0.0
        dx = state.position[0] - state.origin[0]
        dy = state.position[1] - state.origin[1]
        distance = math.hypot(dx, dy)
        if distance <= 0.0:
            return 0.0, 0.0
        if distance > self.radius:
            scale = self.radius / distance
            dx *= scale
            dy *= scale
        return dx / self.radius, dy / self.radius

    def _draw_stick(self, surface: pg.Surface, anchor: tuple[float, float], state: FingerState | None) -> None:
        base_center = anchor
        if state is not None:
            base_center = state.origin
        vector = self._normalized_vector(state)
        knob_center = (
            base_center[0] + vector[0] * self.radius,
            base_center[1] + vector[1] * self.radius,
        )
        pg.draw.circle(surface, (25, 28, 34, 160), (int(base_center[0]), int(base_center[1])), int(self.radius), width=0)
        pg.draw.circle(surface, (150, 166, 180), (int(base_center[0]), int(base_center[1])), int(self.radius), width=3)
        pg.draw.circle(surface, (88, 108, 124), (int(knob_center[0]), int(knob_center[1])), int(self.knob_radius), width=0)
        pg.draw.circle(surface, (210, 220, 232), (int(knob_center[0]), int(knob_center[1])), int(self.knob_radius), width=2)

    def _in_left_zone(self, position: tuple[float, float]) -> bool:
        return position[0] <= self.width * 0.48 and position[1] >= self.height * 0.42

    def _in_right_zone(self, position: tuple[float, float]) -> bool:
        return position[0] >= self.width * 0.52 and position[1] >= self.height * 0.42

    def _to_pixels(self, x: float, y: float) -> tuple[float, float]:
        return x * self.width, y * self.height

    @staticmethod
    def _deadzone(value: float, threshold: float) -> float:
        if abs(value) < threshold:
            return 0.0
        return max(-1.0, min(1.0, value))