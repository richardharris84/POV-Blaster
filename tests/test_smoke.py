import os
import ast
import asyncio
import tempfile
from collections import deque
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from pathlib import Path
import sys

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import pygame as pg

import build
from main import Game, choose_player_name
from application.map import DEFAULT_MAP_NAME, load_map
from application.theme import THEMES, choose_theme
from application.startup import theme_menu_items, validate_player_name
import presentation.web_startup as web_startup
from presentation.web_startup import choose_startup
from domain.health import Health
from domain.game_state import GameState
from domain.combat import Combatant
from domain.movement import movement_delta
from infrastructure.assets import AssetLoader
from infrastructure.scores import BrowserHighScores, HighScores
from infrastructure.windowing import set_game_icon
from application.npc_systems import npc_can_see_player
from presentation.touch import TouchController
from infrastructure.settings import HALF_WIDTH, NUM_RAYS


class BuildScriptTests(unittest.TestCase):
    def test_deploy_flag_allows_deploy_only_mode(self):
        with patch.object(sys, 'argv', ['build.py', '-d']):
            args = build.parse_args()

        self.assertTrue(args.deploy)
        self.assertFalse(args.windows)
        self.assertFalse(args.linux)
        self.assertFalse(args.macos)
        self.assertFalse(args.web)

    def test_browser_deploy_flag_combines_web_build_and_deploy(self):
        with patch.object(sys, 'argv', ['build.py', '-bd']):
            args = build.parse_args()

        self.assertTrue(args.web)
        self.assertTrue(args.deploy)


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


class MapAssetTests(unittest.TestCase):
    def test_default_map_is_loaded_from_plain_text(self):
        default_map = load_map()

        self.assertEqual(DEFAULT_MAP_NAME, '1_mini_map_default')
        self.assertEqual((len(default_map), len(default_map[0])), (32, 16))
        self.assertEqual(load_map('missing_map'), default_map)


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


class TouchControllerTests(unittest.TestCase):
    def test_left_and_right_joysticks_produce_isolated_axes(self):
        pg.init()
        try:
            touch = TouchController(1600, 900)
            left_id = 11
            right_id = 22
            touch.handle_event(pg.event.Event(pg.FINGERDOWN, finger_id=left_id, x=0.15, y=0.85, dx=0.0, dy=0.0, touch_id=0))
            touch.handle_event(pg.event.Event(pg.FINGERMOTION, finger_id=left_id, x=0.19, y=0.76, dx=0.04, dy=-0.09, touch_id=0))
            touch.handle_event(pg.event.Event(pg.FINGERDOWN, finger_id=right_id, x=0.85, y=0.85, dx=0.0, dy=0.0, touch_id=0))
            touch.handle_event(pg.event.Event(pg.FINGERMOTION, finger_id=right_id, x=0.94, y=0.85, dx=0.09, dy=0.0, touch_id=0))

            move_x, move_y, turn_x = touch.axes()
            self.assertGreater(move_x, 0.0)
            self.assertGreater(move_y, 0.0)
            self.assertGreater(turn_x, 0.0)

            touch.handle_event(pg.event.Event(pg.FINGERUP, finger_id=left_id, x=0.19, y=0.76, dx=0.0, dy=0.0, touch_id=0))
            touch.handle_event(pg.event.Event(pg.FINGERUP, finger_id=right_id, x=0.94, y=0.85, dx=0.0, dy=0.0, touch_id=0))
            self.assertEqual(touch.axes(), (0.0, 0.0, 0.0))
        finally:
            pg.quit()

    def test_tap_outside_joystick_zones_does_not_shoot(self):
        pg.init()
        try:
            touch = TouchController(1600, 900)
            finger_id = 33
            touch.handle_event(pg.event.Event(pg.FINGERDOWN, finger_id=finger_id, x=0.50, y=0.20, dx=0.0, dy=0.0, touch_id=0))
            touch.handle_event(pg.event.Event(pg.FINGERUP, finger_id=finger_id, x=0.50, y=0.20, dx=0.0, dy=0.0, touch_id=0))

            self.assertFalse(touch.consume_shoot())
        finally:
            pg.quit()

    def test_tap_on_right_joystick_queues_shot(self):
        pg.init()
        try:
            touch = TouchController(1600, 900)
            finger_id = 44
            touch.handle_event(pg.event.Event(pg.FINGERDOWN, finger_id=finger_id, x=0.85, y=0.85, dx=0.0, dy=0.0, touch_id=0))
            touch.handle_event(pg.event.Event(pg.FINGERUP, finger_id=finger_id, x=0.85, y=0.85, dx=0.0, dy=0.0, touch_id=0))

            self.assertTrue(touch.consume_shoot())
            self.assertFalse(touch.consume_shoot())
        finally:
            pg.quit()


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
            first = loader.load_image('assets/themes/default/textures/digits/10.png', (64, 64))
            second = loader.load_image('assets/themes/default/textures/digits/10.png', (64, 64))
            self.assertIs(first, second)
        finally:
            pg.quit()


class WindowIconTests(unittest.TestCase):
    def test_game_icon_is_applied_to_display(self):
        pg.init()
        pg.display.set_mode((1, 1))
        try:
            with patch.object(pg.display, 'set_icon') as set_icon:
                set_game_icon()
            set_icon.assert_called_once()
            self.assertEqual(set_icon.call_args.args[0].get_size(), (64, 64))
        finally:
            pg.quit()


class HighScoreTests(unittest.TestCase):
    def test_score_file_is_created_and_keeps_top_ten(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'scores.sqlite3'
            scores = HighScores(path)

            self.assertTrue(path.exists())
            for kills in range(10):
                scores.add(f'Player {kills}', kills)
            scores.add('Winner', 100)

            saved = scores.load()
            self.assertEqual(len(saved), 10)
            self.assertEqual(saved[0].player_name, 'Winner')
            self.assertEqual(saved[0].kills, 100)
            self.assertNotIn('Player 0', [score.player_name for score in saved])

    def test_browser_scores_fall_back_to_memory_on_desktop(self):
        scores = BrowserHighScores()

        scores.add('Browser Player', 12)

        self.assertEqual(scores.load()[0].player_name, 'Browser Player')
        self.assertEqual(scores.load()[0].kills, 12)


class ThemeSelectionTests(unittest.TestCase):
    def test_browser_name_input_is_positioned_over_the_visible_name_field(self):
        class FakeElement:
            def __init__(self):
                self.type = None
                self.maxLength = None
                self.autocomplete = None
                self.autocapitalize = None
                self.spellcheck = None
                self.style = SimpleNamespace()
                self.listeners = {}
                self.attributes = {}
                self.removed = False

            def setAttribute(self, name, value):
                self.attributes[name] = value

            def addEventListener(self, name, listener):
                self.listeners[name] = listener

            def remove(self):
                self.removed = True

        class FakeDocument:
            def __init__(self):
                self.body = SimpleNamespace(appendChild=self._append_child)
                self.appended = None

            def createElement(self, name):
                self.created_name = name
                return FakeElement()

            def _append_child(self, element):
                self.appended = element

        document = FakeDocument()
        with patch.object(sys, 'platform', 'emscripten'), patch.object(
            web_startup,
            'platform',
            SimpleNamespace(document=document),
        ):
            browser_input = web_startup._BrowserNameInput(lambda event: None)

        self.assertIs(browser_input.element, document.appended)
        self.assertEqual(document.created_name, 'input')
        self.assertEqual(browser_input.element.style.left, '50%')
        self.assertEqual(browser_input.element.style.top, web_startup.BROWSER_NAME_INPUT_TOP)
        self.assertEqual(browser_input.element.style.transform, 'translate(-50%, -50%)')
        self.assertEqual(browser_input.element.style.width, web_startup.BROWSER_NAME_INPUT_WIDTH)
        self.assertEqual(browser_input.element.style.height, web_startup.BROWSER_NAME_INPUT_HEIGHT)
        self.assertEqual(browser_input.element.attributes['aria-label'], 'Player name')
        self.assertIn('input', browser_input.element.listeners)

    def test_web_startup_focuses_browser_name_input_immediately(self):
        pg.init()
        pg.display.set_mode((1600, 900))

        class FakeBrowserNameInput:
            instances = []

            def __init__(self, on_change):
                self.element = object()
                self.focus_calls = 0
                self.close_calls = 0
                FakeBrowserNameInput.instances.append(self)

            def focus(self):
                self.focus_calls += 1

            def deactivate(self):
                self.close()

            def close(self):
                self.close_calls += 1
                self.element = None

        try:
            pg.event.post(pg.event.Event(pg.QUIT))
            with patch.object(web_startup, '_BrowserNameInput', FakeBrowserNameInput):
                self.assertIsNone(asyncio.run(choose_startup()))
        finally:
            pg.quit()

        self.assertEqual(len(FakeBrowserNameInput.instances), 1)
        self.assertEqual(FakeBrowserNameInput.instances[0].focus_calls, 1)
        self.assertEqual(FakeBrowserNameInput.instances[0].close_calls, 1)

    def test_player_name_is_requested_before_theme_selection(self):
        choices = iter(['', 'Alice'])

        self.assertEqual(choose_player_name(lambda prompt: next(choices), lambda message: None), 'Alice')

    def test_profane_player_name_is_rejected_and_reprompted(self):
        choices = iter(['fUcK pilot', 'Alice'])
        messages = []

        self.assertEqual(choose_player_name(lambda prompt: next(choices), messages.append), 'Alice')
        self.assertEqual(messages, ['Please enter a different name.'])

    def test_console_and_web_share_startup_rules(self):
        self.assertEqual(tuple(theme for _, theme in theme_menu_items()), THEMES)
        self.assertIsNone(validate_player_name('Alice'))
        self.assertIsNotNone(validate_player_name('shit pilot'))

    def test_web_startup_collects_name_and_theme_in_viewport(self):
        pg.init()
        pg.display.set_mode((1600, 900))
        try:
            pg.event.post(pg.event.Event(pg.TEXTINPUT, text='Alice'))
            pg.event.post(pg.event.Event(pg.KEYDOWN, key=pg.K_RETURN))
            pg.event.post(pg.event.Event(pg.KEYDOWN, key=pg.K_DOWN))
            pg.event.post(pg.event.Event(pg.KEYDOWN, key=pg.K_RETURN))
            player_name, selected_theme = asyncio.run(choose_startup())
            self.assertEqual(player_name, 'Alice')
            self.assertEqual(selected_theme, THEMES[3])
        finally:
            pg.quit()

    def test_web_startup_defaults_theme_to_hunting_and_requires_confirmation(self):
        pg.init()
        pg.display.set_mode((1600, 900))
        try:
            pg.event.post(pg.event.Event(pg.TEXTINPUT, text='Alice'))
            pg.event.post(pg.event.Event(pg.KEYDOWN, key=pg.K_RETURN))
            pg.event.post(pg.event.Event(pg.KEYDOWN, key=pg.K_RETURN))
            player_name, selected_theme = asyncio.run(choose_startup())
            self.assertEqual(player_name, 'Alice')
            self.assertEqual(selected_theme, THEMES[2])
        finally:
            pg.quit()

    def test_web_startup_accepts_touch_for_name_continue_and_theme(self):
        pg.init()
        pg.display.set_mode((1600, 900))
        try:
            pg.event.post(pg.event.Event(pg.FINGERDOWN, finger_id=1, x=0.5, y=(250 + 32) / 900, dx=0.0, dy=0.0, touch_id=0))
            pg.event.post(pg.event.Event(pg.TEXTINPUT, text='Alice'))
            pg.event.post(pg.event.Event(pg.FINGERDOWN, finger_id=2, x=0.5, y=(395 + 29) / 900, dx=0.0, dy=0.0, touch_id=0))
            pg.event.post(pg.event.Event(pg.FINGERDOWN, finger_id=3, x=0.5, y=(195 + (4 * 76) + 30) / 900, dx=0.0, dy=0.0, touch_id=0))
            pg.event.post(pg.event.Event(pg.FINGERDOWN, finger_id=4, x=0.5, y=(635 + 29) / 900, dx=0.0, dy=0.0, touch_id=0))

            player_name, selected_theme = asyncio.run(choose_startup())
            self.assertEqual(player_name, 'Alice')
            self.assertEqual(selected_theme, THEMES[4])
        finally:
            pg.quit()

    def test_theme_order_has_hunting_before_graveyard_and_doom_last(self):
        self.assertEqual(THEMES[2].key, 'hunting')
        self.assertEqual(THEMES[3].key, 'graveyard')
        self.assertEqual(THEMES[4].key, 'default')

    def test_blank_console_selection_uses_default_doom_theme(self):
        selected = choose_theme(lambda prompt: '', lambda message: None)

        self.assertEqual(selected.key, 'default')
        self.assertEqual(selected.label, 'Doom')

    def test_doom_is_menu_option_five(self):
        choices = iter(['5'])
        selected = choose_theme(lambda prompt: next(choices), lambda message: None)

        self.assertEqual(selected.key, 'default')
        self.assertEqual(selected.label, 'Doom')


class HeadlessSmokeTests(unittest.TestCase):
    def test_async_game_loop_returns_on_escape(self):
        game = Game(THEMES[0], player_name='Web Player', high_scores=BrowserHighScores())
        try:
            pg.event.post(pg.event.Event(pg.KEYDOWN, key=pg.K_ESCAPE))
            asyncio.run(game.run_async())
            self.assertTrue(game.score_recorded)
        finally:
            pg.quit()

    def test_game_over_records_player_score_once(self):
        with tempfile.TemporaryDirectory() as directory:
            scores = HighScores(Path(directory) / 'scores.xml')
            game = Game(THEMES[3], player_name='Alice', high_scores=scores)
            try:
                game.player.kills = 7
                game.set_state('game_over')
                game.set_state('game_over')

                saved = scores.load()
                self.assertEqual(len(saved), 1)
                self.assertEqual(saved[0].player_name, 'Alice')
                self.assertEqual(saved[0].kills, 7)
            finally:
                game.close()

    def test_escape_requests_startup_menu(self):
        with tempfile.TemporaryDirectory() as directory:
            scores = HighScores(Path(directory) / 'scores.xml')
            game = Game(THEMES[3], player_name='Alice', high_scores=scores)
            try:
                pg.event.post(pg.event.Event(pg.KEYDOWN, key=pg.K_ESCAPE))

                self.assertTrue(game.check_events())
                game.close()
                self.assertEqual(scores.load()[0].player_name, 'Alice')
                self.assertIsNone(choose_theme(lambda prompt: '0', lambda message: None))
                self.assertEqual(scores.load()[0].kills, 0)
            finally:
                pg.quit()

    def test_caps_lock_toggles_minimap_for_gameplay(self):
        game = Game(THEMES[3], player_name='Alice')
        try:
            self.assertTrue(game.minimap_enabled)
            pg.event.post(pg.event.Event(pg.KEYDOWN, key=pg.K_CAPSLOCK))
            self.assertFalse(game.check_events())
            self.assertFalse(game.minimap_enabled)
            pg.event.post(pg.event.Event(pg.KEYDOWN, key=pg.K_CAPSLOCK))
            self.assertFalse(game.check_events())
            self.assertTrue(game.minimap_enabled)
            game.draw()
        finally:
            pg.quit()

    def test_kills_persist_across_level_and_theme_reset_but_reset_on_death(self):
        game = Game(THEMES[0], player_name='Alice')
        try:
            game.player.kills = 7
            game.kill_count = 7
            game.new_game()
            self.assertEqual(game.player.kills, 7)
            self.assertEqual(game.kill_count, 7)

            game.player.kills = 11
            game.kill_count = 11
            game.player.health = 0
            game.player.check_game_over()
            self.assertEqual(game.player.kills, 0)
            self.assertEqual(game.kill_count, 0)

            game.player.kills = 9
            game.kill_count = 9
            game.new_game()
            self.assertEqual(game.player.kills, 9)
            self.assertEqual(game.kill_count, 9)
        finally:
            pg.quit()

    def test_game_initializes_and_renders_one_frame(self):
        game = Game(THEMES[3], player_name='Alice')
        try:
            self.assertEqual(game.player_name, 'Alice')
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

    def test_sound_backend_is_not_rebuilt_on_restart(self):
        game = Game(THEMES[3], seed=1)
        try:
            first_sound = game.sound
            game.new_game()
            self.assertIs(game.sound, first_sound)
        finally:
            pg.quit()


class NpcSystemsTests(unittest.TestCase):
    def test_visible_when_player_shares_the_npcs_cell(self):
        game = Game(THEMES[3], seed=7)
        try:
            npc = game.object_handler.npc_list[0]
            game.player.x, game.player.y = npc.x, npc.y
            self.assertTrue(npc_can_see_player(npc))
        finally:
            pg.quit()

    def test_resolve_hit_damages_npc_and_clears_the_shot_flag(self):
        game = Game(THEMES[3], seed=7)
        try:
            npc = game.object_handler.npc_list[0]
            npc.ray_cast_value = True
            npc.screen_x = HALF_WIDTH
            npc.sprite_half_width = 50
            game.player.shot = True
            starting_health = npc.health

            npc.combat_resolver.resolve_hit(npc)

            self.assertFalse(game.player.shot)
            self.assertTrue(npc.pain)
            self.assertLess(npc.health, starting_health)
        finally:
            pg.quit()

    def test_resolve_death_awards_a_kill_once_defeated(self):
        game = Game(THEMES[3], seed=7)
        try:
            npc = game.object_handler.npc_list[0]
            npc.combat.take_damage(npc.combat.health.maximum)
            starting_kills = game.player.kills

            npc.combat_resolver.resolve_death(npc)

            self.assertFalse(npc.alive)
            self.assertEqual(game.player.kills, starting_kills + 1)
        finally:
            pg.quit()

    def test_animation_controller_clears_pain_after_trigger(self):
        game = Game(THEMES[3], seed=7)
        try:
            npc = game.object_handler.npc_list[0]
            npc.pain = True
            npc.animation_trigger = True

            npc.animation_controller.play_pain()

            self.assertFalse(npc.pain)
        finally:
            pg.quit()


class WebHtmlPatchTests(unittest.TestCase):
    def test_patches_apply_to_a_representative_template(self):
        from build import apply_web_html_patches

        html = (
            '    platform.document.body.style.background = "#7f7f7f"\n'
            '<style>\n'
            '        #infobox {\n'
            '            position: fixed; /* center relative to viewport */\n'
            '            background: green;\n'
            '            color: blue;\n'
            '        }\n'
            '        body {\n'
            '            font-family: arial;\n'
            '            margin: 0;\n'
            '            padding: none;\n'
            '            background-color:powderblue;\n'
            '        }\n'
            '        canvas.emscripten {\n'
            '            width: 100%;\n'
            '            height: 100%;\n'
            '            z-index: 5;\n'
            '        }\n'
            '</style>'
        )

        patched = apply_web_html_patches(html)

        self.assertIn('background: black;', patched)
        self.assertIn('color: white;', patched)
        self.assertIn('background-color: #000000;', patched)
        self.assertIn('platform.document.body.style.background = "#000000"', patched)
        self.assertIn('object-fit: fill;', patched)
        self.assertIn('html {\n            width: 100%;\n            height: 100%;\n        }', patched)

    def test_raises_loudly_when_expected_markup_is_missing(self):
        from build import apply_web_html_patches

        with self.assertRaises(RuntimeError):
            apply_web_html_patches('<html><body>unexpected template</body></html>')


class AssetIntegrityTests(unittest.TestCase):
    def test_every_theme_loads_without_falling_back_to_a_placeholder(self):
        # regression test: assets/levels/*.json scenery paths must not duplicate the
        # 'sprites/animated_sprites/' prefix that object_handler.py already applies,
        # or the resulting path 404s and silently renders a placeholder instead.
        import infrastructure.assets as assets_module

        original_load_image = assets_module.AssetLoader.load_image
        missing_paths = []

        def load_image_and_record_misses(self, path, size=None, alpha=True, fallback_label='?'):
            resource_path = assets_module.resolve_resource_path(path)
            if not resource_path.is_file():
                missing_paths.append(str(resource_path))
            return original_load_image(self, path, size=size, alpha=alpha, fallback_label=fallback_label)

        assets_module.AssetLoader.load_image = load_image_and_record_misses
        try:
            for theme in THEMES:
                game = Game(theme, seed=1)
                pg.quit()
        finally:
            assets_module.AssetLoader.load_image = original_load_image

        self.assertEqual(missing_paths, [])

    def test_sound_theme_loads_successfully_for_every_theme(self):
        # regression test: pg.mixer.music.load() always returns None on success, so
        # Sound must not rely on that return value to know whether music loaded.
        for theme in THEMES:
            game = Game(theme, seed=1)
            self.assertTrue(game.sound.theme)
            pg.quit()

    def test_hunting_hunter_has_no_detached_upper_sprite_chunks(self):
        # regression test: hunter face/hat layers must not float as detached chunks
        # above the main sprite body.
        hunter_root = Path(__file__).parents[1] / 'assets' / 'hunting' / 'sprites' / 'npc' / 'hunter'
        phases = ('idle', 'walk', 'attack', 'pain', 'death')

        def connected_components(image):
            width, height = image.get_size()
            pixels = image.get_at
            visited = [[False] * height for _ in range(width)]
            groups = []

            for x in range(width):
                for y in range(height):
                    if visited[x][y] or pixels((x, y))[3] == 0:
                        continue
                    queue = deque([(x, y)])
                    visited[x][y] = True
                    component = []

                    while queue:
                        cx, cy = queue.popleft()
                        component.append((cx, cy))
                        for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                            if 0 <= nx < width and 0 <= ny < height and not visited[nx][ny] and pixels((nx, ny))[3] > 0:
                                visited[nx][ny] = True
                                queue.append((nx, ny))
                    groups.append(component)

            return groups

        offenders = []
        for phase in phases:
            for frame_path in sorted((hunter_root / phase).glob('*.png')):
                frame = pg.image.load(str(frame_path))
                components = connected_components(frame)
                if len(components) <= 1:
                    continue

                main = max(components, key=len)
                main_min_y = min(y for _, y in main)
                for component in components:
                    if component is main:
                        continue
                    # Ignore one-pixel AA dust, but block meaningful detached chunks.
                    if len(component) >= 20 and max(y for _, y in component) < main_min_y + 26:
                        offenders.append(f'{phase}/{frame_path.name}:{len(component)}')

        self.assertEqual(offenders, [])


if __name__ == '__main__':
    unittest.main()
