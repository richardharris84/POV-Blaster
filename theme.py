from dataclasses import dataclass
from pathlib import Path

from settings import RESOURCE_DIR


@dataclass(frozen=True)
class Theme:
    key: str
    label: str
    enemies: tuple
    npc_assets: tuple
    weapon_asset: str = 'sprites/weapon/shotgun/0.png'
    fire_sound: str = 'shotgun.wav'

    @property
    def resource_dir(self):
        return RESOURCE_DIR / self.key

    def path(self, asset_path):
        return self.resource_dir / Path(asset_path)


THEMES = (
    Theme(
        'candy_kingdom',
        'Candy Kingdom',
        ('Marshmallow Man', 'Springfield Doughnut', 'Gingerbread Golem'),
        ('marshmallow_man', 'springfield_doughnut', 'gingerbread_golem'),
        'sprites/weapon/pastry_bag/0.png',
        'floraphonic-thick-slime-18-229584.mp3',
    ),
    Theme(
        'space',
        'Space',
        ('Alien Drone', 'Alien Warrior', 'Alien Overlord'),
        ('alien_drone', 'alien_warrior', 'alien_overlord'),
    ),
    Theme(
        'graveyard',
        'Graveyard',
        ('Ghost', 'Vampire', 'Werewolf'),
        ('ghost', 'vampire', 'werewolf'),
    ),
    Theme(
        'default',
        'Doom',
        ('Soldier', 'Caco Demon', 'Cyber Demon'),
        ('soldier', 'caco_demon', 'cyber_demon'),
        'sprites/weapon/shotgun/0.png',
        'shotgun.wav',
    ),
)


def choose_theme(input_func=input, output_func=print):
    output_func('')
    output_func('Choose a theme:')
    for index, theme in enumerate(THEMES, start=1):
        output_func(f'{index}) {theme.label} [{", ".join(theme.enemies)}]')
    output_func('0) Exit')

    while True:
        choice = input_func('Selection: ').strip()
        if choice == '0':
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(THEMES):
            return THEMES[int(choice) - 1]
        output_func('Invalid selection. Choose a listed theme or 0 to exit.')