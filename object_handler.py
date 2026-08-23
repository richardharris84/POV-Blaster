import json
import random
from pathlib import Path

from application.ports import GameContext
from npc import CacoDemonNPC, CyberDemonNPC, SoldierNPC
from sprite_object import AnimatedSprite

CONTENT_DIR = Path(__file__).resolve().parent / 'content' / 'levels'
NPC_TYPES_BY_NAME = {
    'SoldierNPC': SoldierNPC,
    'CacoDemonNPC': CacoDemonNPC,
    'CyberDemonNPC': CyberDemonNPC,
}


def load_spawn_config(map_name):
    """Scenery placement and enemy spawn tables live in content/levels/<map_name>.json
    rather than hardcoded Python, so a new level's content doesn't require a code change."""
    config_path = CONTENT_DIR / f'{map_name}.json'
    if not config_path.is_file():
        raise FileNotFoundError(f'No spawn config found for map {map_name!r}: {config_path}')
    return json.loads(config_path.read_text(encoding='utf-8'))


class ObjectHandler:
    def __init__(self, game: GameContext, rng=None):
        self.game = game
        self.rng = rng or random.Random()
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'sprites/npc/'
        self.static_sprite_path = 'sprites/static_sprites/'
        self.anim_sprite_path = 'sprites/animated_sprites/'
        add_sprite = self.add_sprite
        self.npc_positions = {}

        config = load_spawn_config(game.map.map_name)

        # spawn npc
        self.enemies = config['enemy_count']
        self.npc_types = [NPC_TYPES_BY_NAME[name] for name in config['enemy_weights']]
        self.weights = list(config['enemy_weights'].values())
        x_lo, x_hi = config['restricted_area']['x_range']
        y_lo, y_hi = config['restricted_area']['y_range']
        self.restricted_area = {(i, j) for i in range(x_lo, x_hi) for j in range(y_lo, y_hi)}
        self.spawn_npc()

        # sprite map
        for entry in config['scenery']:
            pos = tuple(entry['pos'])
            if 'path' in entry:
                add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + entry['path'], pos=pos))
            else:
                add_sprite(AnimatedSprite(game, pos=pos))

    def spawn_npc(self):
        valid_positions = [
            (x, y)
            for y in range(self.game.map.rows)
            for x in range(self.game.map.cols)
            if (x, y) not in self.game.map.world_map and (x, y) not in self.restricted_area
        ]
        if self.enemies > len(valid_positions):
            raise ValueError('Not enough valid map cells to spawn all NPCs')

        for x, y in self.rng.sample(valid_positions, self.enemies):
            npc_type = self.rng.choices(self.npc_types, self.weights)[0]
            self.add_npc(npc_type(self.game, pos=(x + 0.5, y + 0.5)))

    def check_win(self):
        if not len(self.npc_positions):
            self.game.set_state('victory')

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        self.check_win()

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)