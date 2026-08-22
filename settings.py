import math
from pathlib import Path
import pygame as pg

BASE_DIR = Path(__file__).resolve().parent
RESOURCE_DIR = BASE_DIR / 'resources'
IMAGE_CACHE = {}


def resolve_resource_path(path):
	path = Path(path)
	return path if path.is_absolute() else BASE_DIR / path


def create_fallback_surface(size=(64, 64), label='?', bg=(44, 44, 44), accent=(220, 220, 220)):
	width, height = size
	surface = pg.Surface((width, height), flags=pg.SRCALPHA)
	surface.fill(bg)
	for y in range(0, height, 8):
		for x in range(0, width, 8):
			if (x // 8 + y // 8) % 2 == 0:
				surface.fill((max(0, bg[0] - 15), max(0, bg[1] - 15), max(0, bg[2] - 15), 255), (x, y, 8, 8))
	pg.draw.line(surface, accent, (0, 0), (width, height), 2)
	pg.draw.line(surface, accent, (width, 0), (0, height), 2)
	font = pg.font.SysFont('arial', max(10, min(width, height) // 4), bold=True)
	label_surface = font.render(str(label), True, accent)
	label_rect = label_surface.get_rect(center=(width // 2, height // 2))
	surface.blit(label_surface, label_rect)
	return surface


def load_image(path, size=None, alpha=True, fallback_label='?'):
	cache_key = (str(path), tuple(size) if size else None, alpha, fallback_label)
	if cache_key in IMAGE_CACHE:
		return IMAGE_CACHE[cache_key]

	resource_path = resolve_resource_path(path)
	try:
		surface = pg.image.load(str(resource_path))
	except (FileNotFoundError, OSError, pg.error):
		surface = create_fallback_surface(size or (64, 64), fallback_label)
	else:
		surface = surface.convert_alpha() if alpha else surface.convert()

	if size is not None:
		surface = pg.transform.scale(surface, size)

	IMAGE_CACHE[cache_key] = surface
	return surface

# game settings
RES = WIDTH, HEIGHT = 1600, 900
# RES = WIDTH, HEIGHT = 1920, 1080
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 0
MAX_DELTA_TIME = 100

PLAYER_POS = 1.5, 5  # mini_map
PLAYER_ANGLE = 0
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002
PLAYER_SIZE_SCALE = 60
PLAYER_MAX_HEALTH = 100

MOUSE_SENSITIVITY = 0.0024
LINUX_MOUSE_SENSITIVITY = 0.003
MOUSE_MAX_REL = 40
MOUSE_BORDER_LEFT = 100
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

FLOOR_COLOR = (30, 30, 30)

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = WIDTH // 2
HALF_NUM_RAYS = NUM_RAYS // 2
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 20
RAY_EPSILON = 1e-6

SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = WIDTH // NUM_RAYS

TEXTURE_SIZE = 256
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2