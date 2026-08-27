import math

from infrastructure.settings import MAX_DEPTH, RAY_EPSILON


def cast_wall_ray(origin, angle, world_map, max_depth=MAX_DEPTH):
    """Return the nearest wall hit as ``(depth, texture, offset, vertical)``.

    Keeping grid traversal in one place prevents rendering and visibility checks
    from drifting apart while retaining the lightweight tuple API used by the
    existing renderer.
    """
    ox, oy = origin
    x_map, y_map = int(ox), int(oy)
    sin_a = math.sin(angle)
    cos_a = math.cos(angle)
    if abs(sin_a) < RAY_EPSILON:
        sin_a = RAY_EPSILON if sin_a >= 0 else -RAY_EPSILON
    if abs(cos_a) < RAY_EPSILON:
        cos_a = RAY_EPSILON if cos_a >= 0 else -RAY_EPSILON

    y_hor, step_y = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
    depth_hor = (y_hor - oy) / sin_a
    x_hor = ox + depth_hor * cos_a
    delta_depth = step_y / sin_a
    step_x = delta_depth * cos_a
    texture_hor = None
    for _ in range(max_depth):
        tile = int(x_hor), int(y_hor)
        if tile in world_map:
            texture_hor = world_map[tile]
            break
        x_hor += step_x
        y_hor += step_y
        depth_hor += delta_depth

    x_vert, step_x = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
    depth_vert = (x_vert - ox) / cos_a
    y_vert = oy + depth_vert * sin_a
    delta_depth = step_x / cos_a
    step_y = delta_depth * sin_a
    texture_vert = None
    for _ in range(max_depth):
        tile = int(x_vert), int(y_vert)
        if tile in world_map:
            texture_vert = world_map[tile]
            break
        x_vert += step_x
        y_vert += step_y
        depth_vert += delta_depth

    if depth_vert < depth_hor:
        offset = y_vert % 1
        return depth_vert, texture_vert, offset if cos_a > 0 else 1 - offset, True
    offset = x_hor % 1
    return depth_hor, texture_hor, 1 - offset if sin_a > 0 else offset, False