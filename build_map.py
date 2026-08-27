"""Build a grid map and level configuration from a bitmap image.

Black pixels are walkable space. Non-black pixels become walls. Blue pixels map
to texture 1, brown pixels to texture 2, and pale pixels to texture 3. The
bitmap is sampled into a configurable 32x16 grid by default, with an outer
wall ring added to keep generated maps safe for raycasting. Use --mirror for
bilaterally symmetric office-style layouts and --min-walk-gap to reject maps
with isolated walkable cells.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from PIL import Image

DEFAULT_MAP_DIR = Path(__file__).resolve().parent / "assets" / "maps"
DEFAULT_LEVEL_DIR = Path(__file__).resolve().parent / "assets" / "levels"


def _texture_for_pixel(pixel: tuple[int, ...]) -> int:
    red, green, blue = pixel[:3]
    if max(pixel[:3]) < 30:
        return 0
    if min(pixel[:3]) > 240:
        return 3
    if blue > red * 1.25 and blue > green * 1.15:
        return 1
    if red > green * 1.25 and red > blue * 1.25:
        return 2
    if red > 150 and green > 130 and blue < 150:
        return 3
    return 2


def _sample_cell(image: Image.Image, x: int, y: int, columns: int, rows: int) -> int:
    left = x * image.width // columns
    right = (x + 1) * image.width // columns
    top = y * image.height // rows
    bottom = (y + 1) * image.height // rows
    cell_image = image.crop((left, top, right, bottom))
    pixels = cell_image.load()
    colors = [pixels[cell_x, cell_y]
              for cell_y in range(cell_image.height)
              for cell_x in range(cell_image.width)]
    counts = Counter(_texture_for_pixel(pixel) for pixel in colors)
    wall_counts = Counter({texture: count for texture, count in counts.items() if texture})
    if wall_counts and wall_counts.total() >= max(4, len(colors) // 25):
        return wall_counts.most_common(1)[0][0]
    return 0


def bitmap_to_grid(image_path: Path, columns: int, rows: int) -> list[list[int]]:
    if columns < 3 or rows < 3:
        raise ValueError("columns and rows must both be at least 3")
    with Image.open(image_path) as source:
        image = source.convert("RGB")
        grid = [
            [_sample_cell(image, x, y, columns, rows) for x in range(columns)]
            for y in range(rows)
        ]
    for y in range(rows):
        grid[y][0] = grid[y][-1] = 1
    grid[0] = [1] * columns
    grid[-1] = [1] * columns
    return grid


def mirror_grid(grid: list[list[int]]) -> list[list[int]]:
    rows = len(grid)
    columns = len(grid[0])
    return [
        [grid[min(y, rows - 1 - y)][min(x, columns - 1 - x)] for x in range(columns)]
        for y in range(rows)
    ]


def validate_walkable_gaps(grid: list[list[int]], minimum_gap: int = 2) -> None:
    if minimum_gap < 1:
        raise ValueError("minimum_gap must be at least 1")
    rows = len(grid)
    columns = len(grid[0])
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != 0:
                continue
            horizontal = sum(
                0 <= x + offset < columns and grid[y][x + offset] == 0
                for offset in range(-minimum_gap + 1, minimum_gap)
            )
            vertical = sum(
                0 <= y + offset < rows and grid[y + offset][x] == 0
                for offset in range(-minimum_gap + 1, minimum_gap)
            )
            if max(horizontal, vertical) < minimum_gap:
                raise ValueError(
                    f"walkable cell ({x}, {y}) does not have a {minimum_gap}-cell path"
                )


def _grid_text(grid: list[list[int]]) -> str:
    return "\n".join("".join("." if cell == 0 else str(cell) for cell in row) for row in grid) + "\n"


def _default_level_config(grid: list[list[int]], enemy_count: int) -> dict:
    rows = len(grid)
    columns = len(grid[0])
    return {
        "enemy_count": enemy_count,
        "enemy_weights": {
            "SoldierNPC": 70,
            "CacoDemonNPC": 20,
            "CyberDemonNPC": 10,
        },
        "restricted_area": {
            "x_range": [0, min(4, columns - 1)],
            "y_range": [0, min(4, rows - 1)],
        },
        "scenery": [],
    }


def build_map(
    image_path: Path,
    map_name: str,
    columns: int = 32,
    rows: int = 16,
    enemy_count: int = 8,
    mirror: bool = False,
    minimum_gap: int = 2,
    map_dir: Path = DEFAULT_MAP_DIR,
    level_dir: Path = DEFAULT_LEVEL_DIR,
) -> tuple[Path, Path]:
    grid = bitmap_to_grid(image_path, columns, rows)
    if mirror:
        grid = mirror_grid(grid)
    validate_walkable_gaps(grid, minimum_gap)
    map_dir.mkdir(parents=True, exist_ok=True)
    level_dir.mkdir(parents=True, exist_ok=True)
    map_path = map_dir / f"{map_name}.txt"
    level_path = level_dir / f"{map_name}.json"
    map_path.write_text(_grid_text(grid), encoding="utf-8")
    level_path.write_text(
        json.dumps(_default_level_config(grid, enemy_count), indent=4) + "\n",
        encoding="utf-8",
    )
    return map_path, level_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a .txt map and .json level from a bitmap.")
    parser.add_argument("image", type=Path, help="Input BMP/PNG/JPG bitmap.")
    parser.add_argument("map_name", help="Output map name without extension.")
    parser.add_argument("--columns", type=int, default=32, help="Grid columns (default: 32).")
    parser.add_argument("--rows", type=int, default=16, help="Grid rows (default: 16).")
    parser.add_argument("--enemy-count", type=int, default=8, help="NPC count in the generated level JSON.")
    parser.add_argument("--mirror", action="store_true", help="Mirror the sampled layout horizontally and vertically.")
    parser.add_argument("--min-walk-gap", type=int, default=2, help="Minimum contiguous walkable path length (default: 2).")
    parser.add_argument("--map-dir", type=Path, default=DEFAULT_MAP_DIR)
    parser.add_argument("--level-dir", type=Path, default=DEFAULT_LEVEL_DIR)
    args = parser.parse_args()
    if not args.image.is_file():
        parser.error(f"input bitmap not found: {args.image}")
    if args.enemy_count < 0:
        parser.error("--enemy-count must be non-negative")
    map_path, level_path = build_map(
        args.image,
        args.map_name,
        columns=args.columns,
        rows=args.rows,
        enemy_count=args.enemy_count,
        mirror=args.mirror,
        minimum_gap=args.min_walk_gap,
        map_dir=args.map_dir,
        level_dir=args.level_dir,
    )
    print(f"Created map: {map_path}")
    print(f"Created level: {level_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
