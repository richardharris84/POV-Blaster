import math


def movement_delta(angle: float, speed: float, forward: bool, backward: bool,
                   left: bool, right: bool) -> tuple[float, float]:
    sine = math.sin(angle)
    cosine = math.cos(angle)
    delta_x = 0
    delta_y = 0
    directions = 0

    if forward:
        directions += 1
        delta_x += speed * cosine
        delta_y += speed * sine
    if backward:
        directions += 1
        delta_x -= speed * cosine
        delta_y -= speed * sine
    if left:
        directions += 1
        delta_x += speed * sine
        delta_y -= speed * cosine
    if right:
        directions += 1
        delta_x -= speed * sine
        delta_y += speed * cosine

    if directions > 1:
        correction = 1 / math.sqrt(2)
        delta_x *= correction
        delta_y *= correction

    return delta_x, delta_y
