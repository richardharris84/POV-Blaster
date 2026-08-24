# POV-Blaster: Codebase Reconstruction Guide (Updated)

> This document reflects the **current** state of the project, which has evolved substantially since the original `docs/CodeBase.md`: the code is now organized into layered `application/`, `domain/`, `infrastructure/`, and `presentation/` packages, themes select entire enemy/asset sets, maps live in plain-text files, and the game ships as native desktop executables (Windows/Linux/macOS via PyInstaller) **and** as a browser build (via Pygbag/WASM) deployed automatically to GitHub Pages.

## 1. What You Are Building

POV-Blaster is a first-person shooter written in Python with Pygame. It recreates the visual style of early raycasting games such as Wolfenstein 3D and DOOM:

- The map is a 2D grid of cells, loaded from a plain-text file.
- Walls are integer texture IDs; a ray is cast per screen column to find the nearest wall and its projected height.
- Enemies and scenery are 2D images ("sprites") projected into the same 3D view, occluded by a per-column depth buffer.
- The player moves with `WASD`, looks with the mouse, and fires with left click.
- NPCs use line-of-sight raycasts, simple state machines, and breadth-first pathfinding to hunt the player.
- Five selectable **themes** (Doom, Candy Kingdom, Space, Graveyard, Hunting) swap enemy sprites, weapon art, textures, and music/sound without touching any game logic.
- The player wins when every living NPC has been defeated; losing all health ends the run.
- The exact same game logic runs three ways: as a desktop console-driven app, as standalone platform executables, and as an asynchronous browser build.

This document explains the current implementation, then gives a practical, ordered plan for recreating it from scratch. It assumes the reader knows basic Python but is new to Pygame, layered architecture, and building for the browser.

## 2. Prerequisites

Install:

1. Python 3.10+ (3.12/3.13 confirmed working; CI uses 3.13, the web build pins the Pygbag interpreter to 3.12).
2. Git, if cloning the repository.
3. A desktop environment with graphics and audio support (for the desktop build) — or just a modern browser (for the web build).

`requirements.txt`:

```text
pygame
pyinstaller
pygbag
imageio-ffmpeg
Pillow
opencv-python
scikit-image
```

- `pygame` — the only dependency needed to actually run the game.
- `pyinstaller` — only needed to produce Windows/Linux/macOS executables.
- `pygbag` — only needed to package/serve the browser build.
- `imageio-ffmpeg` — only needed by `build.py --web`; it bundles a portable `ffmpeg` binary (no system install required) used to transcode sound assets to OGG Vorbis for the browser.
- `Pillow`, `opencv-python`, and `scikit-image` — used by the integrated theme audit and Pixel-Harmony-compatible image comparisons.

On Windows, verify the Python launcher is available:

```powershell
py --version
```

Create and activate a virtual environment, then install dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

Run the desktop game with:

```powershell
py main.py
```

Run it from the repository root — asset and map paths are resolved relative to the project (or the frozen executable's) location, not the current working directory.

## 3. Repository Layout

```text
main.py                Desktop/CLI entry point (theme + name prompt, then Game.run())
web_main.py             Async browser entry point (viewport startup menu, Game.run_async())
build.py                Multi-target build script: Windows/Linux/macOS executables + browser build
settings.py             Screen, movement, raycasting, and mouse-sensitivity constants
theme.py                Theme definitions (enemies, asset paths, weapon, fire sound) + CLI picker
map.py                  Plain-text map loading and wall lookup table (Map)
player.py               Player state, input, movement, health, and shooting
raycasting.py           First-person wall raycasting and wall-column projection
sprite_object.py        Static/animated sprite projection with depth-buffer occlusion
object_handler.py       Content-driven NPC/sprite registration, spawning, and victory check
npc.py                  NPC base class + SoldierNPC/CacoDemonNPC/CyberDemonNPC/HuntingBearNPC
pathfinding.py          Grid graph + breadth-first NPC navigation
weapon.py               Weapon animation, reload state, and damage value
sound.py                Thin re-export shim: `from infrastructure.audio import Sound`

application/            Composition root and cross-cutting contracts
  game.py                 Game: owns pygame lifecycle, the frame loop, and object wiring
  ports.py                Protocol definitions (GameContext, Renderer, AudioOutput, ...)
  renderer.py             Re-exports Renderer protocol for presentation layer
  snapshot.py             RenderSnapshot: immutable per-frame render data

domain/                 Pure game-rule logic with no Pygame/IO dependency
  health.py               Health value object (damage/recover/depleted)
  combat.py               Combatant value object (health + damage + accuracy)
  movement.py             movement_delta(): WASD -> (dx, dy), diagonal-normalized
  game_state.py           GameState: playing/game_over/victory + countdown timer

infrastructure/         Adapters to the outside world (files, audio devices, browser APIs)
  assets.py               AssetLoader: cached image loading with drawn fallback sprites
  audio.py                Sound (desktop, pg.mixer) and BrowserSound/BrowserClip (web, native <audio>)
  scores.py               HighScores (scores.xml) and BrowserHighScores (browser localStorage)
  input.py                Re-exports InputAdapter for the presentation layer

presentation/           Pygame-facing adapters behind the application layer's ports
  input.py                InputAdapter: wraps pg.event.get()
  renderer.py             ObjectRenderer: background/sky, walls, sprites, HUD, end screens

maps/                   Plain-text maps ('.' = empty, digit = wall texture id)
resources/<theme>/      Per-theme textures, sprites, and sound (default/candy_kingdom/graveyard/hunting/space)
tests/                  unittest suite (domain, map, audio, scores, NPC, assets, async loop)
audit_themes.py         Root entry point for the production theme asset audit
tools/audit_themes.py   Required asset, image quality, and animation audit implementation
tools/pixel_harmony_compare.py  Pixel-Harmony-compatible image comparison metrics
tools/profile_game.py   Headless cProfile harness for update()/draw()
docs/                   Design/audit/reconstruction documentation
.github/workflows/      CI (tests) and GitHub Pages deployment (web build)
build/                  Build outputs (gitignored): platform executables and the web bundle
```

Two things are easy to miss:

- `sound.py` at the project root is **not** the audio implementation — it's a one-line compatibility shim (`from infrastructure.audio import Sound`) kept so older imports (and some tooling) keep working after the audio code moved into `infrastructure/`.
- `object_renderer.py` at the project root doesn't exist as real logic either; `application/renderer.py` re-exports the `Renderer` **protocol**, while the real implementation is `presentation/renderer.py`'s `ObjectRenderer`. The indirection lets `application/game.py` depend only on the protocol, not the concrete Pygame-based renderer.

## 4. Architecture: Why the Layers Exist

The project follows a light hexagonal/ports-and-adapters split:

- **`domain/`** holds plain dataclasses with no imports of `pygame`, files, or the network: `Health`, `Combatant`, `GameState`, `movement_delta`. These are the actual game *rules* and are trivially unit-testable in isolation (see `tests/test_smoke.py`).
- **`application/ports.py`** defines `Protocol` classes — `GameContext`, `Renderer`, `AudioOutput`, `AssetLoaderPort`, `InputPort`, `ImageLoader` — describing what the application layer needs, without committing to *how* it's provided. `application/game.py` type-hints its collaborators (`self.object_renderer: Renderer = ...`) against these protocols.
- **`infrastructure/`** and **`presentation/`** provide concrete implementations of those ports: real Pygame image/sound loading, real file/localStorage-backed high scores, real `pg.event.get()`-based input.
- **`application/game.py`** is the composition root: it constructs every subsystem, wires them together via the shared `game` instance, and runs the frame loop.

This separation is what makes it possible to swap the **audio backend** (`Sound` vs `BrowserSound`) and the **high-score backend** (`HighScores` vs `BrowserHighScores`) purely by choosing which class to hand to `Game(...)`, without touching `player.py`, `npc.py`, or any other consumer — they all just call `self.game.sound.shotgun.play()` or `self.game.high_scores.add(...)` against the protocol, unaware of which concrete class is behind it.

## 5. Core Design and Object Relationships

`Game` is a service container: every subsystem receives the same `game` instance and reaches every other subsystem through it (`self.game.player`, `self.game.map`, `self.game.sound`, ...).

```python
class Game:
    def __init__(self, theme, player_name='Player', seed=None, high_scores=None, sound_factory=None):
        self.theme = theme
        self.high_scores = high_scores or HighScores()
        self.sound_factory = sound_factory or Sound   # <-- pluggable audio backend
        ...
        self.new_game()
```

`Game.new_game()` (re-)builds every subsystem in a deliberate order:

```text
new_game()
  -> Map                (needs nothing but the theme's map name)
  -> Player              (needs nothing but starting position/angle)
  -> ObjectRenderer      (needs the theme, for texture paths)
  -> RayCasting          (needs ObjectRenderer.wall_textures)
  -> ObjectHandler        (spawns NPCs onto the Map; needs Player to exist implicitly via game)
  -> Weapon              (needs the theme, for weapon sprite/animation)
  -> build sound_factory(self) on the first round, then stop/reuse it on restarts
  -> PathFinding          (needs ObjectHandler.npc_positions and Map.mini_map)
  -> play_theme()
```

The ordering matters:

- `RayCasting` reads `ObjectRenderer.wall_textures`, so the renderer must exist first.
- `PathFinding` checks NPC occupancy via `ObjectHandler`, so NPCs must be spawned first.
- The **old** sound backend's `stop_theme()` is called *before* constructing the new one. This was added to fix a real bug: the browser audio backend creates a brand-new `<audio>` element per game restart, and without explicitly stopping the previous one, the old and new theme tracks played simultaneously (desktop's `pg.mixer.music` masked the same bug because it's a single global channel that implicitly replaces itself).

`new_game()` runs once from `Game.__init__`, and again whenever the round restarts: after a win/loss countdown expires (`GameState.advance()` returns `True` in `update()`), or — in the browser build only — when the player presses `Escape` (`check_events()` returns `True`, and `run_async()` treats that as "restart" rather than "quit").

## 6. The Frame Loop

Two loop entry points exist, selected by which platform is running:

```python
def run(self):                       # desktop: blocking loop
    while True:
        if self.check_events():
            self.close()
            return
        self.delta_time = min(self.clock.tick(FPS), MAX_DELTA_TIME)
        self.update_global_trigger()
        self.update()
        self.draw()
        pg.display.flip()

async def run_async(self, return_on_exit=True):   # browser: cooperative loop
    self.browser_mode = not return_on_exit
    while True:
        if self.check_events():
            self.record_score()
            if return_on_exit:
                return
            self.new_game()          # Escape restarts instead of quitting, in the browser
            continue
        self.delta_time = min(self.clock.tick(FPS), MAX_DELTA_TIME)
        self.update_global_trigger()
        self.update()
        self.draw()
        pg.display.flip()
        await asyncio.sleep(0)       # yield to the browser's event loop every frame
```

`update_global_trigger()` replaced an older `pg.time.set_timer()`-based 40ms pulse used for animation timing:

```python
def update_global_trigger(self):
    self.global_trigger_accum += self.delta_time
    self.global_trigger = self.global_trigger_accum >= 40
    if self.global_trigger:
        self.global_trigger_accum -= 40
```

**Why:** `pg.time.set_timer()` raises `NotImplementedError: set_timer is not implemented on WASM yet` under Pygbag. The `delta_time`-accumulator approach produces the same 40ms pulse (`NPC.animate_death` and others read `self.game.global_trigger`) but works identically on desktop and in the browser — one code path, no platform branching.

### Input: `Game.check_events`

Reads `self.input.poll()` (a thin wrapper over `pg.event.get()`), and for each event:

- `pg.QUIT` — desktop: record score, `pg.quit()`, `sys.exit()`. Browser mode ignores it (there's no real window to close).
- `K_ESCAPE` — returns `True`, which `run()`/`run_async()` interpret as "end this session" (desktop) or "restart" (browser).
- Window focus lost/gained — releases/re-acquires mouse grab, so alt-tabbing doesn't trap the cursor.
- Any keydown/mouse click — calls `activate_mouse()`, which (re-)grabs the mouse and clears any pending relative-motion so the first frame after re-focusing doesn't snap the camera.
- Mouse motion while playing — forwarded to `Player.add_mouse_motion()`.
- Every event, while playing, is also forwarded to `Player.single_fire_event()` to detect the fire button.

## 7. Player, Movement, and Health (domain-driven)

`Player` doesn't implement health or movement math itself — it delegates to `domain/`:

```python
self.health_state = Health.full(PLAYER_MAX_HEALTH)   # domain.health.Health

def movement(self):
    dx, dy = movement_delta(self.angle, speed, keys[K_w], keys[K_s], keys[K_a], keys[K_d])
    self.check_wall_collision(dx, dy)
```

`domain.movement.movement_delta()` is a pure function: given the facing angle and which of W/A/S/D are held, it returns a `(dx, dy)` step, normalized by `1/sqrt(2)` when moving diagonally so diagonal speed isn't faster than axis-aligned speed. It has no Pygame dependency, so it's trivially unit-tested with plain booleans.

`domain.health.Health` clamps `current` between `0` and `maximum` on both `damage()` and `recover()`, and exposes `depleted` — used by `Player.check_game_over()` and by `Combatant.defeated` for NPCs.

Mouse look (`Player.mouse_control`) has three branches, each with its own sensitivity constant from `settings.py`:

| Platform | Sensitivity constant | Why it's different |
|---|---|---|
| Windows/macOS (SDL relative mouse mode) | `MOUSE_SENSITIVITY` | Baseline, tuned for native SDL mouse capture. |
| Linux under X11 forwarding (e.g. WSLg) | `LINUX_MOUSE_SENSITIVITY` | X11-forwarded relative motion needed a slightly higher value; detected via `SDL_VIDEODRIVER == 'x11'`. |
| Browser build | `WEB_MOUSE_SENSITIVITY = MOUSE_SENSITIVITY * 1.2 * 1.2` | Browser relative-motion events felt sluggish compared to native SDL capture; boosted ~44% on top of the baseline. Selected via `getattr(self.game, 'browser_mode', False)`, which only exists once `run_async()` has started. |

## 8. Raycasting and Rendering Pipeline

`RayCasting.ray_cast()` casts `NUM_RAYS` rays (one per 2 horizontal pixels, via `SCALE = WIDTH // NUM_RAYS`) using the classic DDA-style horizontal/vertical grid-intersection algorithm, picks whichever intersection (horizontal or vertical wall) is closer, corrects for the fisheye effect (`depth *= cos(player.angle - ray_angle)`), and stores `(depth, projected_height, texture_id, texture_offset)` per ray.

`RayCasting.get_objects_to_render()` turns that per-ray data into actual scaled `Surface` column blits, plus a `depth_buffer` (one depth value per ray) used later to occlude sprites standing behind walls.

`ObjectRenderer.draw(snapshot)` (in `presentation/renderer.py`) then:

1. Draws a horizontally-scrolling sky strip and a solid floor rectangle.
2. Blits every `(depth, image, pos)` tuple in the snapshot, sorted back-to-front (`reverse=True` on depth) so nearer sprites/walls draw over farther ones.
3. Draws the HUD health digits and, when relevant, the blood/game-over/win overlays.

`application/snapshot.py`'s `RenderSnapshot` is a frozen dataclass capturing `objects`, `player_position`, `player_angle`, and `player_health` for one frame. `Game.update()` rebuilds it every frame from live game state; `ObjectRenderer.draw()` accepts either a snapshot or `None` (falling back to reading `self.game.raycasting.objects_to_render` directly), which keeps rendering testable/replayable independent of live mutable state.

`SpriteObject.get_sprite()` projects an NPC/decoration into screen space (angle-to-player, screen X, distance), and `get_sprite_projection()` clips the sprite column-by-column against `raycasting.depth_buffer` so sprites are correctly hidden behind nearer walls. `AnimatedSprite` (both `NPC` and `Weapon` inherit from it) additionally cycles through a `deque` of frame images on its own `animation_time` timer, independent of the shared 40ms `global_trigger`.

## 9. NPCs, Combat, and Pathfinding

`NPC` (in `npc.py`) is an `AnimatedSprite` with a `domain.combat.Combatant` (health + attack damage + accuracy) and a small state machine driven each frame by `run_logic()`:

```text
alive?
  pain (just hit)         -> play pain animation
  can see player (raycast) -> in attack range? attack : walk toward player
  has seen player before   -> keep walking toward last known player position
  else                     -> idle
dead -> play death animation once, driven by the shared global_trigger pulse
```

`ray_cast_player_npc()` reuses the same horizontal/vertical DDA logic as `RayCasting`, but from the NPC's position toward the player, to determine line-of-sight (whether a wall is hit before reaching the player).

The standard subclasses (`SoldierNPC`, `CacoDemonNPC`, and `CyberDemonNPC`) differ in stats and defaults. `HuntingBearNPC` specializes the third role for the Hunting theme and routes its attack to a dedicated roar clip. Sprite folders are resolved from `game.theme.npc_assets`, so switching themes swaps enemy art without changing core gameplay.

`ObjectHandler.spawn_npc()` reads the enemy count, weights, restricted area, and scenery from `content/levels/<map_name>.json`, places NPCs across valid non-restricted map cells, and uses an injected `random.Random` instance (`Game.random`, seedable) so spawns are reproducible in tests. Hunting maps the third role to `HuntingBearNPC`.

`PathFinding` builds an 8-directional adjacency graph from the map once at construction, and runs a breadth-first search per NPC per frame (`get_path`), treating cells currently occupied by other living NPCs as temporarily blocked (`self.game.object_handler.npc_positions`) so NPCs don't stack on top of each other.

## 10. Weapon and Damage Flow

`Weapon` is an `AnimatedSprite` with no independent damage-application logic; it just tracks a `reloading` flag and steps through its fire animation. The actual hit registration lives on the **NPC** side:

1. `Player.single_fire_event()` sets `weapon.reloading = True` and `player.shot = True`, and plays `sound.shotgun`.
2. Every NPC's `check_hit_in_npc()` checks, each frame, whether it's currently visible (`ray_cast_value`) **and** `player.shot` is still `True` **and** its screen-space sprite width straddles the crosshair (screen center) — i.e. "was something shot, and am I the thing under the crosshair right now?" The first NPC to see `player.shot == True` under those conditions "claims" the hit and immediately clears `player.shot = False`, applies `weapon.damage` via `Combatant.take_damage()`, and plays the pain/death sound.

This means there's no real projectile or hitscan-vs-all-enemies loop — the crosshair-overlap check is evaluated independently by whichever NPC happens to be centered on screen when the flag is set, which is simple but assumes at most one enemy is realistically hittable per shot (true given the corridor-style map and narrow crosshair window).

## 11. Themes and Asset Resolution

`theme.py`'s `Theme` is a frozen dataclass: `key` (folder name under `resources/`), `label`, `enemies` (display names), `npc_assets` (sprite-folder names, index-matched to `SoldierNPC`/`CacoDemonNPC`/`CyberDemonNPC`), and optional `weapon_asset`/`fire_sound` overrides. `Theme.resource_dir` and `Theme.path(...)` are the *only* place theme-specific paths are constructed — every consumer (`ObjectRenderer`, `Weapon`, `Sound`, `SpriteObject`) calls `game.theme.path(...)` rather than hardcoding `resources/default/...`.

`infrastructure/assets.py`'s `AssetLoader` caches every loaded `Surface` by `(path, size, alpha, fallback_label)`, and — critically — **never raises** on a missing file: `load_image()` catches `FileNotFoundError`/`OSError`/`pg.error` and returns a procedurally drawn placeholder (`create_fallback_surface`: a checkerboard with an X and a single-letter label) instead. This means an incomplete or mismatched theme folder degrades gracefully to placeholder art rather than crashing, which is especially useful while building out new themes incrementally.

## 12. Maps

Maps are plain UTF-8 text files under `maps/`, one row per line, using `.` for empty and a single digit `1`-`5` for a wall texture ID. `map.load_map()`:

- Reads and validates the file (`Path.read_text(encoding='utf-8')` — note: **not** `'ascii'`; see the WASM pitfall below).
- Requires every row to be the same length (raises `ValueError` otherwise).
- Requires every cell to be `.` or a digit (raises `ValueError` otherwise).
- Falls back to `1_mini_map_default` if the requested map name doesn't exist, and re-raises if even the default is missing.

`Map.get_map()` (in `map.py`) turns the 2D grid into `world_map: dict[(x, y), texture_id]`, containing only wall cells — this sparse representation is what `RayCasting`, `NPC.check_wall`, and `Player.check_wall` all query with simple `(x, y) not in world_map` / `world_map[(x, y)]` lookups.

## 13. Audio: Two Backends Behind One Interface

`application/ports.py`'s `AudioOutput` protocol just requires `shotgun`, `npc_pain`, `npc_death`, `npc_shot`, `player_pain` (each with `.play()`/`.set_volume()`), and by convention (not in the protocol) `play_theme()`/`stop_theme()`. Two implementations exist in `infrastructure/audio.py`:

**`Sound`** (desktop) — thin wrapper over `pg.mixer`. Loads each effect via `pg.mixer.Sound(path)` and music via `pg.mixer.music.load(path)`, wrapping any load failure in a no-op `SilentClip` so a missing sound file never crashes the game. `_resolve()` prefers a `.ogg` sibling of the requested filename if one exists (used by the web build's transcoded assets), otherwise uses the original `.wav`/`.mp3`.

**`BrowserSound`/`BrowserClip`** (web) — pygame's SDL mixer under Pygbag/WASM proved unreliable (see pitfalls below): sounds fired inconsistently, and playback quality was garbled regardless of source format. Instead, `BrowserSound` embeds each sound file as a base64 **data URI**, and `BrowserClip` pre-creates and pre-loads a small pool (4) of real HTML5 `<audio>` elements per sound at construction time. Playing a sound just round-robins to the next pooled element, resets `currentTime = 0`, and calls `.play()` — no repeated decode-from-scratch per shot, which is what made rapid-fire playback (e.g. the shotgun) reliably keep up. The theme track is a single looping `<audio>` element (`loop = True`).

`Game.sound_factory` (defaulting to `Sound`) is how `web_main.py` swaps in `BrowserSound` without any other file needing to know which backend is active.

## 14. High Scores: Two Backends Behind One Interface

Same pattern as audio: `HighScores` (desktop) persists a sorted, capped list of `Score(player_name, kills)` to `scores.xml` via `xml.etree.ElementTree`. `BrowserHighScores` (web) stores the same data as JSON in the browser's `localStorage` (key `pov-blaster-high-scores`), falling back to an in-memory list if `localStorage` is unavailable for any reason. Both implement `load()`/`add()`/`display()` with identical sorting (`-kills`, then case-insensitive name).

## 15. Multi-Platform Builds (`build.py`)

One script, four targets, selected by mutually exclusive flags:

```powershell
py build.py -w    # --windows: PyInstaller onefile .exe (must run on Windows)
py build.py -l    # --linux:   PyInstaller onefile binary (must run on Linux)
py build.py -m    # --macos:   PyInstaller .app bundle (must run on macOS)
py build.py -b    # --web:     Pygbag browser bundle (works on any host)
```

The desktop targets bundle `resources/` and `maps/` via PyInstaller's `--add-data`, and refuse to run on the wrong host OS (a Windows build cannot be produced on Linux, etc.) since PyInstaller only produces native artifacts for the current host.

**The web target (`build_web()`) is the most involved:**

1. Copies the whole project into `build/web-source/`, excluding build artifacts, tests, docs, and (deliberately) the non-`default` theme resource folders — only the Doom theme ships to the browser, to keep the download small.
2. **`upgrade_web_audio()`** transcodes every `.wav`/`.mp3` under the copy into OGG Vorbis via a bundled `ffmpeg` (from `imageio-ffmpeg`, no system install needed), preserving each file's original channel count/sample rate at high quality (`-q:a 8`). Pygbag rejects raw WAV/MP3 packaging by default; OGG is what the browser audio backend reliably supports.
3. Overwrites `web-source/main.py` with a **thin wrapper**:
   ```python
   import asyncio
   import pygame  # noqa: F401 -- pygbag scans this file's *text* for 'import pygame'
   from web_main import main
   asyncio.run(main())
   ```
   The comment matters: Pygbag statically scans `main.py`'s source text (not its actual imports) to decide which WASM packages to preload. A version of this file that only did `from web_main import main` silently broke pygame preloading and crashed with `AttributeError: module 'pygame' has no attribute 'Surface'`.
4. Runs `python -m pygbag --build --ume_block=0 --disable-sound-format-error web-source`.
5. Copies the packaged `web-source/build/web` to the top-level `build/web`, downloads a local copy of `browserfs.min.js` (the CDN reference in Pygbag's default template 404s), and rewrites `index.html` to reference it locally.
6. **`apply_web_html_patches()`** patches the generated `index.html` **and** the Pygbag-cached HTML template (`build/web-source/build/web-cache/*.tmpl`) to: recolor the "Loading, please wait..." box (black background, white text, instead of green/blue), set unused page background space to black instead of `powderblue`, and make the canvas fill the browser window while preserving aspect ratio via `object-fit: contain` (instead of stretching to the container). Patching the *cached template*, not just the generated file, matters: `python -m pygbag build/web-source` (the local dev server) repacks from that cache on every restart, silently reverting any patch applied only to the generated `index.html`.

**Testing the web build locally** requires Pygbag's own dev server, not a plain HTTP server (it doesn't provide the `/cdn/` proxy route the runtime needs):

```powershell
py build.py --web
py -m pygbag build/web-source
# open http://localhost:8000
```

The dev server packs once at startup and does **not** hot-reload — after any `build.py --web` rerun, stop (Ctrl+C) and restart it.

## 16. Testing and Tooling

- `tests/test_smoke.py` — a `unittest` suite covering domain logic (`Health`, `GameState`, `Combatant`), map loading/validation/fallback, both high-score backends, and an async smoke test of `run_async()`'s Escape-to-restart behavior. It forces `SDL_VIDEODRIVER=dummy`/`SDL_AUDIODRIVER=dummy` so it runs headless in CI.
- `tools/profile_game.py` — constructs a headless `Game`, then calls `update()`/`draw()` in a loop under `cProfile`, to spot performance regressions without opening a window.
- `generate_themes.ps1` — PowerShell tooling for validating/generating theme asset sets (run with `-ValidateOnly` in CI to catch missing theme files before they ship).

## 17. Continuous Integration and Deployment

`.github/workflows/ci.yml` runs on every push/PR (Windows runner, dummy SDL drivers): installs dependencies, compiles all modules, runs the test suite, and validates theme assets.

The CI job also runs `python audit_themes.py --check`, which writes `build/theme_audit.json` and fails non-Default themes with missing required assets, invalid required dimensions, blank images, clipped NPC frames, missing animation folders, or duplicate animation frames. Run the same command locally before a release.

`.github/workflows/deploy-pages.yml` runs on every push to `main` (or manual dispatch): installs dependencies, runs `python build.py --web`, uploads `build/web` as a Pages artifact, and deploys it via `actions/deploy-pages`. One-time setup: repository **Settings → Pages → Source: GitHub Actions**. Once enabled, the live build is served at `https://<username>.github.io/<repo>/`.

## 18. Recreation Order (Practical Guide)

If rebuilding this project from scratch, this order minimizes rework:

1. **Domain first, with tests.** Write `domain/health.py`, `domain/combat.py`, `domain/game_state.py`, `domain/movement.py` — plain dataclasses/functions, no Pygame. Write their unit tests immediately; they're cheap to get right in isolation and everything else depends on them being correct.
2. **Settings and map loading.** `settings.py` (screen size, raycasting constants derived from `FOV`/`WIDTH`), then `map.py` with its plain-text format and default-map fallback.
3. **Ports.** Sketch `application/ports.py`'s protocols before writing concrete classes — deciding the shape of `GameContext`/`Renderer`/`AudioOutput` up front avoids circular-import headaches later, since almost every module type-hints against `GameContext` instead of importing `Game` directly.
4. **Themes and asset loading.** `theme.py`'s `Theme` dataclass and `THEMES` tuple, then `infrastructure/assets.py`'s `AssetLoader` with its fallback-surface behavior — build and test this before any rendering code needs real art.
5. **Player, raycasting, rendering.** `player.py` (movement + mouse look, no shooting yet), `raycasting.py`, `presentation/renderer.py`'s `ObjectRenderer`. Get a walkable, texture-mapped box on screen before adding enemies.
6. **Sprites, NPCs, pathfinding.** `sprite_object.py` (static then animated), `npc.py`, `pathfinding.py`, `object_handler.py`'s random spawn logic.
7. **Weapon and combat loop.** `weapon.py`, then wire `Player.single_fire_event()` and `NPC.check_hit_in_npc()` together.
8. **Audio and high scores, desktop first.** `infrastructure/audio.py`'s `Sound` and `infrastructure/scores.py`'s `HighScores`, wired through `Game.sound_factory`/`Game.high_scores` so the browser variants can be swapped in later without touching consumers.
9. **`application/game.py` composition root.** Wire everything above into `Game.new_game()` in dependency order (see Section 5), plus `run()`/`check_events()`/`update()`/`draw()`.
10. **Desktop CLI and executables.** `main.py`'s theme/name prompt, then `build.py`'s Windows/Linux/macOS PyInstaller targets.
11. **Browser build last.** `web_main.py`, `BrowserSound`/`BrowserHighScores`, `build.py --web`, and the HTML/audio-format fixes in Section 15 — expect several WASM-specific surprises here even with a working desktop build (see Section 19).
12. **CI/CD.** Test suite wired into `ci.yml`, then `deploy-pages.yml` once the web build works locally.

## 19. Common Pitfalls (Learned the Hard Way)

These are real issues hit while building the web target — worth knowing before you hit them yourself:

- **`pg.time.set_timer()` raises `NotImplementedError` on WASM.** If you need a periodic pulse, accumulate `delta_time` yourself instead (Section 6).
- **`Path.read_text(encoding='ascii')` raises `LookupError: unknown encoding: ascii` under Pygbag's CPython build.** Use `'utf-8'` (or omit the argument) for any file I/O that must also run in the browser.
- **Pygbag statically scans your entry script's *text*, not its actual imports**, to decide which WASM packages (like `pygame`) to preload. A generated/wrapper `main.py` that delegates to another module without a literal `import pygame` string can crash with a partially-initialized `pygame` module.
- **Pygbag's dev server (`python -m pygbag <dir>`) packs once at startup and does not hot-reload.** Restart it after every rebuild, or you'll debug against a stale bundle.
- **Pygbag's dev server also caches the generated HTML template** under `build/web-cache/*.tmpl` and reuses it on the next start *instead of* re-downloading/regenerating — any HTML/CSS patch needs to target that cache file too, or it reverts on the next `pygbag` invocation.
- **Pygbag rejects raw `.wav`/`.mp3` packaging by default**, insisting on OGG (or `--disable-sound-format-error` to bypass, at your own audio-quality risk).
- **SDL's mixer (`pg.mixer`) is unreliable under Pygbag/WASM** — sounds can trigger at the wrong time or sound garbled independent of source encoding. If you hit this, consider bypassing it entirely for the web build in favor of native browser `<audio>` elements (Section 13).
- **Calling a JS constructor via the Pygbag/`platform.window` bridge is not the same as `new Foo()`.** `window.Audio.new(...)` doesn't exist (returns `None`), and `window.Audio(...)` fails with "Please use the 'new' operator". `document.createElement('audio')` sidesteps the problem entirely for anything the DOM lets you construct that way.
- **Cloning and playing a fresh `<audio>` node per sound trigger is too slow for rapid-fire SFX** — each clone re-decodes its `src` from scratch. Pre-create and pre-load a small pool of elements up front and round-robin them instead.
- **A new backend instance per game restart needs explicit cleanup.** Creating a fresh `BrowserSound` (and thus a fresh `<audio>` element) every `new_game()` without stopping the previous instance's theme track first causes overlapping/duplicate music — desktop's single global `pg.mixer.music` channel hid this same bug by construction.

## Release Checkpoint: Steps 39-44

The project currently passes the automated graphics, gameplay, architecture, and web deployment gates. All five themes are ready for automated play testing. Physical mobile touch testing and a professional art-direction review remain manual release gates.
