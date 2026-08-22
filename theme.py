from dataclasses import dataclass
from pathlib import Path

from settings import RESOURCE_DIR


@dataclass(frozen=True)
class Theme:
    key: str
    label: str
    enemies: str

    @property
    def resource_dir(self):
        return RESOURCE_DIR / self.key

    def path(self, asset_path):
        return self.resource_dir / Path(asset_path)


THEMES = (
    Theme('default', 'Default', 'Soldier, Caco Demon, Cyber Demon'),
)


def choose_theme(input_func=input, output_func=print):
    output_func('Choose a theme:')
    for index, theme in enumerate(THEMES, start=1):
        output_func(f'{index}) {theme.label} [{theme.enemies}]')
    output_func('0) Exit')

    while True:
        choice = input_func('Selection: ').strip()
        if choice == '0':
            return None
        if choice.isdigit() and 1 <= int(choice) <= len(THEMES):
            return THEMES[int(choice) - 1]
        output_func('Invalid selection. Choose a listed theme or 0 to exit.')