import os
import ast
import unittest
from pathlib import Path

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')

import pygame as pg

from main import Game
from theme import THEMES, choose_theme
from domain.health import Health
from domain.game_state import GameState
from domain.combat import Combatant
from domain.movement import movement_delta
from infrastructure.assets import AssetLoader
from settings import NUM_RAYS


class HealthTests(unittest.TestCase):
    def test_damage_and_recovery_are_clamped(self):
        health = Health.full(100)

        self.assertEqual(health.damage(125), 0)
        self.assertTrue(health.depleted)
        self.assertEqual(health.recover(10), 10)
        self.assertEqual(health.recover(1000), 100)


class GameStateTests(unittest.TestCase):
    def test_terminal_state_expires_after_elapsed_time(self):
        state = GameState()

        state.set('victory', 100)

        self.assertFalse(state.advance(40))
        self.assertTrue(state.advance(60))


class CombatTests(unittest.TestCase):
    def test_combatant_tracks_damage_and_accuracy(self):
        combatant = Combatant.create(50, 10, 0.25)

        self.assertTrue(combatant.attack_hits(0.1))
        self.assertFalse(combatant.attack_hits(0.25))
        self.assertEqual(combatant.take_damage(60), 0)
        self.assertTrue(combatant.defeated)


class MovementTests(unittest.TestCase):
    def test_diagonal_movement_is_normalized(self):
        diagonal = movement_delta(0, 1, True, False, False, True)

        self.assertAlmostEqual(diagonal[0], 1 / 2**0.5)
        self.assertAlmostEqual(diagonal[1], 1 / 2**0.5)


class DomainBoundaryTests(unittest.TestCase):
    def test_domain_modules_have_no_framework_imports(self):
        domain_root = Path(__file__).parents[1] / 'domain'
        forbidden = {'pygame', 'infrastructure', 'presentation'}

        for module_path in domain_root.glob('*.py'):
            tree = ast.parse(module_path.read_text(encoding='utf-8'))
            imports = {
                node.names[0].name.split('.')[0]
                for node in ast.walk(tree)
                if isinstance(node, ast.Import) and node.names
            }
            imports.update(
                node.module.split('.')[0]
                for node in ast.walk(tree)
                if isinstance(node, ast.ImportFrom) and node.module
            )
            self.assertTrue(forbidden.isdisjoint(imports), module_path.name)


class AssetCacheTests(unittest.TestCase):
    def test_repeated_texture_load_reuses_cached_surface(self):
        pg.init()
        pg.display.set_mode((1, 1))
        loader = AssetLoader()
        try:
            first = loader.load_image('resources/default/textures/digits/10.png', (64, 64))
            second = loader.load_image('resources/default/textures/digits/10.png', (64, 64))
            self.assertIs(first, second)
        finally:
            pg.quit()


class ThemeSelectionTests(unittest.TestCase):
    def test_doom_is_menu_option_four(self):
        choices = iter(['4'])
        selected = choose_theme(lambda prompt: next(choices), lambda message: None)

        self.assertEqual(selected.key, 'default')
        self.assertEqual(selected.label, 'DOOM')


class HeadlessSmokeTests(unittest.TestCase):
    def test_game_initializes_and_renders_one_frame(self):
        game = Game(THEMES[3])
        try:
            game.check_events()
            game.update()
            game.draw()
            pg.display.flip()
            self.assertEqual(len(game.raycasting.depth_buffer), NUM_RAYS)
        finally:
            pg.quit()

    def test_seeded_game_repeats_npc_layout(self):
        layouts = []
        for _ in range(2):
            game = Game(THEMES[3], seed=42)
            layouts.append([(npc.map_pos, type(npc).__name__) for npc in game.object_handler.npc_list])
            pg.quit()

        self.assertEqual(layouts[0], layouts[1])


if __name__ == '__main__':
    unittest.main()
