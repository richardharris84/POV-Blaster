# POV-Blaster Code Audit and Architecture Refactoring Plan (Re-Audit)

> This report supersedes the original `CodeAudit.md`. The codebase has since undergone a substantial refactor (a `domain/application/infrastructure/presentation` split, a plain-text map format, a dual-backend audio/high-score system, and an entire second platform target — a Pygbag/WASM browser build). This re-audit credits what was fixed, re-flags what remains open, and adds new findings specific to the current architecture, including the browser build. For a full narrative walkthrough of the current implementation, see `docs/CodeBase.md` (the original walkthrough is archived at `docs/archive/CodeBase-Orig.md` and is now out of date).

## Executive Summary

POV-Blaster has matured from a single-file-per-concern prototype into a genuinely layered application: pure `domain/` rules, `application/` composition, `infrastructure/` adapters (Pygame audio/scores/assets *and* browser-native equivalents), and a `presentation/` renderer — all wired behind `Protocol`-based ports in `application/ports.py`. It now ships as native Windows/Linux/macOS executables **and** as a browser build deployed via GitHub Actions to GitHub Pages, backed by a test suite and CI.

That said, "millions of users" is still primarily a **client-performance and static-distribution** problem for this project — POV-Blaster is a local, single-player simulation with no server, so scale means: the client must run smoothly on a wide range of hardware/browsers, the web bundle must be small and cheap to serve from a CDN, and the codebase must be safe for many contributors to extend without regressions.

The highest-priority remaining items are:

1. ☑ The renderer re-scaled every wall column and visible sprite from scratch, every frame. **Fixed**: `ObjectRenderer` now owns bounded wall-column/sprite scale caches (`presentation/renderer.py`), used by `raycasting.py` and `sprite_object.py`. Measured ~33% faster over 300 profiled frames (17.0s → 11.4s), with `get_objects_to_render` ~67% faster and `pygame.transform.scale` no longer in the top 10 cost centers.
2. ☑ `NPC` still mixes AI decision-making, animation, combat resolution, and audio side effects in one class; `ObjectHandler` still hardcodes scenery/spawn tables in Python. **Fixed**: scenery/spawn data moved out of `object_handler.py` into `content/levels/<map_name>.json` (validated, fails loudly if missing); `PyInstaller` builds now bundle `content/` alongside `resources/`/`maps/`. `NPC` was further decomposed into `VisibilityService`, `CombatResolver`, and an `AnimationController` collaborator, with `NPC` reduced to a thin coordinator over its own state.
3. ☑ The web build's HTML/CSS patching in `build.py` is a pile of fragile exact-string `.replace()` calls with no test coverage — it will silently stop working the moment Pygbag's upstream template changes. **Fixed**: `apply_web_html_patches` now raises a clear `RuntimeError` when an expected substring is missing instead of silently no-op'ing, with unit tests covering both the happy path and the failure path.
4. ☑ `settings.py` remains a flat, unvalidated module of constants, and there are now **two independent definitions** of "where is the project root" (`settings.py` and `infrastructure/assets.py`) that must be kept in sync by hand. **Fixed** (the duplication): `infrastructure/assets.py` now imports `BASE_DIR` from `settings.py` instead of recomputing it. `settings.py` itself is still a flat, unvalidated module — that part of this finding remains open (see M9).
5. ☑ Per-round setup rebuilt the sound backend and re-embedded browser audio. **Fixed**: `Game.new_game()` now builds the sound backend once per `Game` instance (theme never changes across restarts) instead of every round, with a regression test asserting the backend identity is preserved across `new_game()` calls. Per-round gameplay objects are still intentionally rebuilt.

6. ☑ Theme asset quality and structure were not previously audited uniformly. **Fixed for the current asset gate**: `audit_themes.py` and `tools/audit_themes.py` inspect all five resource themes for required files, dimensions, blank images, clipping, animation folders, and duplicate frames; `tools/pixel_harmony_compare.py` provides Pixel-Harmony-compatible comparison metrics. CI runs the audit with `--check`.

The recommended path is still a modular-monolith-first approach: harden the existing layered engine, make content and platform differences data-driven instead of scattered `getattr(..., 'browser_mode', False)` checks, and keep the option open to swap rendering technology later without touching gameplay rules.

## Audit Scope and Rating Model

Reviewed the current source tree (root gameplay modules, `application/`, `domain/`, `infrastructure/`, `presentation/`, `build.py`, `tests/`, `.github/workflows/`) against the walkthrough in [CodeBase.md](CodeBase.md):

- [main.py](../main.py), [web_main.py](../web_main.py), [build.py](../build.py)
- [settings.py](../settings.py), [theme.py](../theme.py), [map.py](../map.py)
- [player.py](../player.py), [raycasting.py](../raycasting.py), [sprite_object.py](../sprite_object.py)
- [object_handler.py](../object_handler.py), [npc.py](../npc.py), [pathfinding.py](../pathfinding.py), [weapon.py](../weapon.py)
- [application/game.py](../application/game.py), [application/ports.py](../application/ports.py), [application/snapshot.py](../application/snapshot.py)
- [domain/health.py](../domain/health.py), [domain/combat.py](../domain/combat.py), [domain/movement.py](../domain/movement.py), [domain/game_state.py](../domain/game_state.py)
- [infrastructure/assets.py](../infrastructure/assets.py), [infrastructure/audio.py](../infrastructure/audio.py), [infrastructure/scores.py](../infrastructure/scores.py), [infrastructure/input.py](../infrastructure/input.py)
- [presentation/renderer.py](../presentation/renderer.py), [presentation/input.py](../presentation/input.py)
- [tests/test_smoke.py](../tests/test_smoke.py), [requirements.txt](../requirements.txt)
- [audit_themes.py](../audit_themes.py), [tools/audit_themes.py](../tools/audit_themes.py), [tools/pixel_harmony_compare.py](../tools/pixel_harmony_compare.py)

Severity levels (unchanged from the original audit):

- **Critical**: can prevent startup, corrupt a game session, or make a production build unsafe.
- **High**: likely correctness, stability, or major performance problem.
- **Medium**: maintainability, testability, or scalability risk that grows expensive as content/platforms grow.
- **Low**: cleanup or design improvement with limited immediate user impact.

## What Has Already Been Fixed

Credit where due — the following findings from the original audit are **resolved** in the current codebase:

| Original finding | Status | Evidence |
|---|---|---|
| H1: frame presented before it's drawn | **Fixed** | `Game.run()`/`run_async()` now call `update()` → `draw()` → `pg.display.flip()` in that order. |
| H4: `lru_cache` on pathfinding read stale occupancy | **Fixed** | `PathFinding.get_path` no longer caches; BFS re-runs against live `npc_positions` each call. |
| H5: game-over/victory blocked the loop with `pg.time.delay` | **Fixed** | `domain.game_state.GameState` is a non-blocking countdown (`advance(delta_time)`); `Game.update()` keeps polling events/rendering during the transition. |
| H7: asset paths depended on the current working directory | **Fixed** | `settings.BASE_DIR`/`infrastructure.assets.resolve_resource_path` resolve relative to `__file__`, not CWD (see M4 below for a residual duplication issue). |
| H8: NPC spawning could duplicate occupancy, unseeded | **Fixed** | `ObjectHandler.spawn_npc` samples unique cells via an injected `random.Random` (`rng.sample`, no replacement), and raises if there aren't enough valid cells. |
| H9: health/HUD not robust to invalid values | **Fixed** | `domain.health.Health.damage()`/`recover()` clamp `0 <= current <= maximum` unconditionally. |
| M1: wildcard imports | **Fixed** | Every module now uses explicit `from module import (name, ...)` imports. |
| M3: shared Pygame timer event drove animation pulses | **Fixed** (and for a good reason) | `pg.time.set_timer()` raises `NotImplementedError` under Pygbag/WASM; `Game.update_global_trigger()` now accumulates `delta_time` instead — one code path for desktop and browser. |
| M4: animation frames loaded in non-deterministic OS order | **Fixed** | `AnimatedSprite.get_images()` sorts by a numeric suffix extracted from the filename (`frame_sort_key`). |
| M5 (partial): map was a mutable Python literal | **Improved** | Maps are now plain-text files under `maps/`, loaded and validated (`load_map`: rectangular grid, valid cell characters, fallback to the default map). Still not a full `LevelDefinition` (no spawn markers/entity metadata in the format — see M5 below). |

## Findings

### Critical / High-Priority

#### H1 (new). The renderer re-scales every wall column and sprite from scratch, every frame

**Status: Fixed.** `ObjectRenderer` (`presentation/renderer.py`) now owns bounded `wall_column_cache`/`sprite_scale_cache` dicts with a shared `cached_scale()` helper. `raycasting.py`'s `get_objects_to_render` snaps the continuous offset/height values to integer pixel buckets and caches the scaled wall column per `(texture, position, size)` key; `sprite_object.py`'s `get_sprite_projection` caches the pre-occlusion scaled sprite per `(image_id, width, height)` key (occlusion masking still copies per-frame, since it's cheap and depth-dependent). Measured on `tools/profile_game.py` over 300 frames: total runtime 17.0s → 11.4s (~33% faster), `get_objects_to_render` cumulative time 3.61s → 1.19s (~67% faster), and `pygame.transform.scale` dropped out of the top-10 cost centers entirely.

**Location:** `RayCasting.get_objects_to_render` (wall columns), `SpriteObject.get_sprite_projection` (sprites)

The renderer still processes up to `NUM_RAYS` (currently `WIDTH // 2` = 800 at the default resolution), but scaled wall columns and sprite variants are now cached on integer projection buckets. Occlusion masking remains per-frame because it depends on the depth buffer.

#### H2 (new). Duplicated, hand-rolled DDA raycasting algorithm

**Status: Partially addressed.** The NPC-visibility copy of the algorithm was extracted out of `NPC` into a standalone `npc_can_see_player()` function in `npc_systems.py` (as part of the M6 fix below), which at least isolates it to one clearly-named place with its own tests. The underlying duplication against `RayCasting.ray_cast` is unchanged — unifying both into one shared implementation remains open and was out of scope for this pass (it touches the performance-critical, already-optimized wall-rendering path from H1).

**Location:** `RayCasting.ray_cast` and `npc_systems.npc_can_see_player` (formerly `NPC.ray_cast_player_npc`)

The exact same horizontal/vertical grid-traversal algorithm (including the same `RAY_EPSILON` axis-alignment guards) is implemented twice — once for wall rendering, once for NPC line-of-sight. Any future bug fix or optimization (e.g. the now-fixed H1) has to be applied twice and can silently drift apart.

**Recommendation:** extract a single `cast_ray(origin, angle, world_map) -> RayHit` function (or class) used by both the renderer and NPC visibility checks.

#### H3 (new). NPC hit resolution is still "first NPC under the crosshair wins," not nearest-visible-target

**Location:** `NPC.check_hit_in_npc`

Every alive NPC independently checks "am I visible, and is `player.shot` still `True`, and does my projected sprite width straddle screen center?" — whichever NPC's `update()` runs first while those conditions hold claims the hit and clears `player.shot`. There's still no depth-buffer-based nearest-target query. With the corridor-style maps currently shipped this is rarely user-visible, but it's a latent correctness gap for denser layouts (two enemies overlapping the crosshair) and this was flagged (as H10) in the original audit without being addressed.

**Recommendation:** build a single hit query from the camera through `raycasting.depth_buffer`, select the *nearest* candidate actor whose projected bounds contain the crosshair, and resolve the hit once per shot rather than via independent per-NPC checks.

#### H4 (new). Per-round teardown/rebuild is expensive, and worse on the web build

**Status: Fixed.** `Game.new_game()` now builds the sound backend once per `Game` instance (only on the first call) instead of on every restart, since the theme — and therefore the sound backend's content — never changes across restarts within one `Game` instance. Only `stop_theme()`/`play_theme()` run on subsequent restarts. Covered by `test_sound_backend_is_not_rebuilt_on_restart`, which asserts `game.sound` is the exact same object before and after `new_game()`.

**Location:** `Game.new_game()`

Every restart reconstructs per-round gameplay objects (`ObjectRenderer`, `RayCasting`, `ObjectHandler`, and `Weapon`), while the sound backend is created once per `Game` instance and reused. Browser audio files are therefore not re-embedded on each restart.

**Remaining recommendation:** separate more load-once theme assets from per-round state so renderer, raycaster, object-handler, and weapon construction can also be reduced on restart. Sound backend reuse is implemented and covered by regression tests.

### Medium-Priority

#### M1 (new). `infrastructure/audio.py` mixes four unrelated concerns in one file

**Location:** `infrastructure/audio.py`

`SilentClip`, `Sound` (desktop/`pg.mixer`), `BrowserClip`, and `BrowserSound` (web/native `<audio>`) all live in a single ~140-line module. The two backends have essentially nothing in common beyond satisfying the same `AudioOutput` shape, and the browser-specific classes only make sense when running under Pygbag.

**Recommendation:** split into `infrastructure/audio/desktop.py` (`Sound`, `SilentClip`) and `infrastructure/audio/browser.py` (`BrowserSound`, `BrowserClip`), re-exported from `infrastructure/audio/__init__.py` for backward compatibility with existing imports.

#### M2 (new). Platform branching is scattered `getattr(..., 'browser_mode', False)` checks instead of one seam

**Location:** `application/game.py` (`check_events`), `player.py` (`mouse_control`)

Two unrelated files independently probe `getattr(self.game, 'browser_mode', False)` (or the equivalent) to decide platform-specific behavior (Escape = quit vs. restart; mouse sensitivity). Each new platform-specific behavior risks becoming a third or fourth ad-hoc `getattr` check rather than going through one place.

**Recommendation:** introduce a small `Platform`/`PlatformConfig` value passed into `Game` (e.g. `platform='desktop' | 'browser'`), exposing named properties (`platform.restarts_on_escape`, `platform.mouse_sensitivity`) instead of scattering `getattr` probes across consumers.

#### M3 (new). `build.py`'s web HTML/CSS patching is fragile, untested, exact-string matching

**Status: Fixed.** `apply_web_html_patches` now routes every substitution through a `_require_replace()` helper that raises a clear `RuntimeError` (naming which fix failed) when the expected substring isn't found, instead of silently no-op'ing. Added `WebHtmlPatchTests` (a happy-path test against a representative fixture template, and a test asserting the loud failure on unexpected markup), and re-verified against a real `build.py --web` run to confirm the stricter matching still succeeds against the actual Pygbag template.

**Location:** `build.py`'s `apply_web_html_patches`, `upgrade_web_audio`

`apply_web_html_patches` chains several exact-substring `.replace()` calls against Pygbag's generated template (colors, background rules, canvas CSS). None of these have a test, and none fail loudly if the substring no longer matches (a `.replace()` on a missing substring is a silent no-op) — a Pygbag version bump that reformats its template would silently undo these fixes with no error and no test failure to catch it.

**Recommendation:** assert the expected substring is present before replacing (raise a clear error if not), and add a unit test that runs `apply_web_html_patches` against a fixture HTML string and asserts the expected output — this was learned the hard way this session (the "loading box" color, background color, and canvas aspect-ratio fixes all needed re-discovery multiple times because they weren't caught by any test).

#### M4 (new). Two independent definitions of "project root"

**Status: Fixed.** `infrastructure/assets.py` now imports `BASE_DIR` from `settings.py` instead of recomputing it independently. (The broader M9 finding — `settings.py` itself being a flat, unvalidated module — is unchanged and still open.)

**Location:** `settings.py` (`BASE_DIR = Path(__file__).resolve().parent`) and `infrastructure/assets.py` (`BASE_DIR = Path(__file__).resolve().parent.parent`)

Both resolve to the same directory today only because of where each file happens to live in the tree. Moving either file, or adding another path-resolution helper elsewhere, risks silent drift between the two.

**Recommendation:** define `PROJECT_ROOT` once (e.g. in a small `paths.py` or in `settings.py`) and have `infrastructure/assets.py` import it rather than recomputing it.

#### M5. Map format still doesn't carry entity/spawn metadata (partial carry-over from the original M5)

**Status: Fixed**, via the sibling-manifest option explicitly allowed by the original recommendation. See M7 below — scenery/spawn tables now live in `content/levels/<map_name>.json`, keyed by the map's own name, rather than in `object_handler.py`.

**Location:** `maps/*.txt`, `object_handler.py`

Maps now validate rectangular shape and cell characters (an improvement), but NPC/scenery placement is still entirely separate, hardcoded Python (`ObjectHandler.__init__`'s `add_sprite(...)` calls and `spawn_npc`'s random sampling) rather than being expressed in the map/level data itself.

**Recommendation:** extend the map format (or add a sibling manifest) to carry scenery/spawn markers, so a level's content and its walkable layout live in one file.

#### M6. `NPC` still combines AI, animation, combat, and audio in one class

**Status: Fixed.** `npc.py` now delegates to three collaborators in the new `npc_systems.py` module: `npc_can_see_player()` (visibility raycast), `AnimationController` (idle/walk/attack/pain/death animation selection), and `CombatResolver` (attack/hit/death resolution and their audio side effects). `NPC` itself is now a thin coordinator: `run_logic()` reads as a state machine delegating to `self.animation_controller`/`self.combat_resolver` rather than calling its own mixed-concern methods. `SoldierNPC`/`CacoDemonNPC`/`CyberDemonNPC` are unaffected (they only override data). Covered by four new `NpcSystemsTests` exercising visibility, hit resolution, death/kill-count, and animation-state transitions.

**Location:** `npc.py`, `npc_systems.py`

Unchanged from the original audit's M6: `NPC` is responsible for line-of-sight raycasting, movement/pathfinding requests, animation frame selection, damage application, and playing sound effects, all in one class. `SoldierNPC`/`CacoDemonNPC`/`CyberDemonNPC` correctly express *data* differences without duplicating logic, which is good, but the base class itself is still doing too much.

**Recommendation:** as originally suggested — split into `VisibilitySystem`, `MovementSystem` (thin wrapper over `PathFinding`), `CombatSystem`, and an `AnimationController`, with `NPC` reduced to a data holder plus a small coordinator.

#### M7. Scenery/spawn tables are still hardcoded Python

**Status: Fixed.** Scenery placements and enemy spawn weights moved from hardcoded Python in `ObjectHandler.__init__` into `content/levels/<map_name>.json`, loaded by `load_spawn_config()` (which raises a clear `FileNotFoundError` if a map's config is missing, rather than silently falling back). This also surfaced and fixed a packaging gap: `build.py`'s PyInstaller targets now bundle `content/` alongside `resources/`/`maps/` (previously would have shipped executables that crashed on startup, since the config is now required at runtime).

**Location:** `ObjectHandler.__init__`, `content/levels/1_mini_map_default.json`

`self.enemies = 20`, `self.npc_types`/`self.weights`, `self.restricted_area`, and ~20 hardcoded `add_sprite(...)` calls with literal coordinates are unchanged from the original audit's M7.

**Recommendation:** unchanged from before — move to a data file (JSON/TOML) validated at build/CI time, ideally alongside the M5 map-format extension.

#### M8. Render list is still a shared mutable structure, now merely *wrapped* by a snapshot afterward

**Location:** `RayCasting.objects_to_render`, `SpriteObject.get_sprite_projection`, `application/snapshot.py`

`RenderSnapshot` was introduced (a genuine improvement — `Game.update()` now produces an immutable-looking snapshot each frame, and `ObjectRenderer.draw()` accepts either a snapshot or `None`), but the underlying mechanism is unchanged: `RayCasting` still initializes a shared list and `SpriteObject.get_sprite_projection` still `append()`s directly into `self.game.raycasting.objects_to_render` during each sprite's own `update()`. The snapshot is a copy taken *after* this mutation dance, not a replacement for it.

**Recommendation:** have each system return its render contributions explicitly (walls from `RayCasting`, sprites from `ObjectHandler`), and have `Game.update()` assemble them into the snapshot, rather than having sprites reach into another system's mutable list.

#### M9. `settings.py` remains flat, global, and unvalidated

**Location:** `settings.py`

Resolution, FOV, ray count, mouse sensitivities, and other derived values remain module-level constants without grouped typed configuration or startup validation.

**Recommendation:** group settings into typed configs (`DisplayConfig`, `RaycastConfig`, `InputConfig`) and validate derived values at startup rather than trusting hand-tuned constants.

#### M10. Dependencies remain unpinned

**Location:** `requirements.txt`

`requirements.txt` now also declares `Pillow`, `opencv-python`, and `scikit-image` for theme auditing, but all dependencies remain unpinned.

**Recommendation:** unchanged — pin or constrain for release builds; separate a dev-tools requirements file (linter, type checker, test runner) from the runtime/build set.

#### M11 (new). No automated coverage for the browser-specific code paths

**Location:** `infrastructure/audio.py`'s `BrowserSound`/`BrowserClip`, `build.py`'s HTML/audio patch functions

`tests/test_smoke.py` covers domain rules, map loading, both high-score backends, and an async smoke test of `run_async()`'s restart behavior — good coverage for what it covers. But the entire browser-audio code path (which needed multiple rounds of manual debugging this session: wrong JS calling convention, cloning-vs-pooling, duplicate theme playback) and all of `build.py`'s web-specific logic have zero automated tests. These are exactly the areas most likely to silently regress.

**Recommendation:** add unit tests for `BrowserClip`/`BrowserSound` using fake `document`/`window` objects (they only need `createElement`, and the returned object needs `.play()`/`.pause()`/attribute assignment — trivial to fake), and tests for `build.py`'s pure functions (`apply_web_html_patches`, path resolution) that don't require actually invoking `pygbag`.

### Low-Priority

#### L1 (carried over, still true). Naming and style cleanup

`mini_map` is still not a minimap (it's the full map grid); `IMAGE_WIDTH`/`SPRITE_SCALE`-style constants are still instance fields that read like class constants; commented-out debug code (`# self.draw_ray_cast()`, `# pg.draw.rect(...)`) is still present in `npc.py`/`player.py`.

#### L2 (carried over, still true). List comprehensions used only for side effects

`ObjectHandler.update()` still uses `[sprite.update() for sprite in self.sprite_list]` purely for its side effects.

#### L3 (new). `sound.py` and `application/renderer.py` are pure re-export shims

**Location:** `sound.py` (`from infrastructure.audio import Sound`), `application/renderer.py` (`from application.ports import Renderer`)

Both are one-line compatibility shims left over from the migration to the layered structure. They're harmless but easy to mistake for real implementations when navigating the codebase (a new contributor opening `sound.py` expecting to find the audio logic will be confused).

**Recommendation:** either remove them (fixing up the handful of remaining imports) or add a one-line module docstring explaining they're compatibility re-exports.

## Performance and Rendering Strategy

The prior audit's cost-center analysis is still accurate and still mostly unaddressed:

- ~800 rays at the default 1600px width, two grid traversals per ray, per frame.
- Cached wall-column and sprite scaling variants, with per-frame depth-dependent occlusion masking (H1 above).
- A full depth sort of the combined wall+sprite render list every frame.
- Per-NPC line-of-sight raycast and pathfinding BFS request every frame, with no distance-based update-frequency tiering.

**Phase 1 (still the right next step):** cache scaled wall columns and sprite variants (H1); extract one shared DDA implementation (H2); precompute per-ray trig values when FOV/ray-count haven't changed.

**Phase 2:** replace the mutate-then-snapshot render list (M8) with systems that explicitly return typed render contributions, assembled by `Game.update()`.

**Phase 3:** if the project's ambitions grow beyond a retro single-player title (many more actors, dynamic lighting, mobile/touch support), re-evaluate whether continuing in pure Pygame/Python is still the right call versus an engine such as Godot — the layered architecture already in place (domain rules with no Pygame dependency) is exactly what keeps that decision open rather than foreclosed.

Simulation-side recommendations are unchanged from the original audit and still open: fixed simulation timestep with an accumulator, distance-based NPC update tiering, scheduled (rather than every-frame-per-NPC) pathfinding requests, and frame-time/cache-hit telemetry to make future optimization work measurable instead of guesswork.

## Scalability for "Millions of Users" (Revised for the Current Client-Only Reality)

POV-Blaster has no server component and (per the browser build) is now distributed as a static site. "Millions of users" therefore breaks down into three concrete, already-partially-addressed concerns:

### 1. Client performance across a wide hardware/browser matrix

Covered above (Performance and Rendering Strategy). The web build in particular needs to perform acceptably on modest laptops and integrated GPUs running a WASM-compiled Python interpreter — a meaningfully higher bar than the native desktop build. The still-open per-frame scaling/allocation issue (H1) matters *more*, not less, in the browser.

### 2. Static-asset distribution at scale

The web build is already served via GitHub Pages behind GitHub's CDN (`.github/workflows/deploy-pages.yml`), which is a reasonable starting point for a small game. As the asset set grows (more themes shipped to the browser, higher-resolution art):

- Consider shipping only the default theme to the browser build (already done — `build.py`'s `ignore_web_files` excludes the other three theme folders) and evaluate whether the remaining themes should be lazy-loaded on selection rather than bundled at all if the browser build ever exposes theme choice.
- Add cache-control/versioning awareness for the packaged `web-source.tar.gz`/`.apk` so returning users aren't forced to re-download an unchanged bundle, and new deploys aren't blocked by stale browser caches (a real issue hit during this session's manual testing).
- Keep the OGG-transcoding step in `build.py` (already in place) rather than shipping uncompressed WAV — this was a deliberate, correct choice already made.

### 3. Codebase scalability for contributors, not just players

With CI (`ci.yml`) running tests and asset validation, and a deploy pipeline (`deploy-pages.yml`) already in place, the remaining scalability gap is **content and platform extensibility**: adding a fifth theme, a new enemy type, or a third platform target currently means editing multiple hardcoded Python locations (M5, M7, M2) rather than adding a data file. This is the practical meaning of "scalability" for a project with no server: how much can grow (content, platforms, contributors) without a proportional increase in code that has to change everywhere at once.

If the project ever *does* grow a server-side component (leaderboards beyond `localStorage`, matchmaking, accounts), the original audit's guidance still applies unchanged: keep those services entirely outside the local simulation, define a versioned protocol, and never make Pygame surfaces or render snapshots part of a network contract.

## Clean Architecture: Current State vs. Target

The current dependency direction is already correct and should be preserved, not replaced:

```text
                    +----------------------+
                    |  application (Game)  |
                    |  composition root,   |
                    |  frame loop, ports   |
                    +----------+-----------+
                               |
        +----------------------+----------------------+
        |                                             |
+-------v--------+                           +--------v--------+
| infrastructure |                           |   presentation  |
| pg.mixer/audio,|                           | ObjectRenderer, |
| scores, assets,|                           | InputAdapter    |
| browser adapters|                          |                 |
+-------+--------+                           +--------+--------+
        |                                             |
        +----------------------+----------------------+
                               v
                    +----------------------+
                    |        domain        |
                    | Health, Combatant,   |
                    | GameState, movement  |
                    +----------------------+
```

The gap between this and the target is narrower than it was: `domain/` genuinely has zero Pygame/IO imports today. The remaining work is less about introducing layers (done) and more about **finishing the migration** — moving logic that's still sitting in root-level actor classes (`Player`, `NPC`, `ObjectHandler`) into the layers that already exist for it (M6, M7, M2 above).

## Suggested Folder Structure (Evolving the Current Layout, Not Replacing It)

The project already adopted top-level `application/`, `domain/`, `infrastructure/`, `presentation/` packages rather than a `src/pov_blaster/` layout — that decision is sound (it matches the actual migration that happened) and should be kept. The suggested next step is to keep root-level gameplay modules moving *into* those packages rather than proposing a new layout:

```text
POV-Blaster/
├── main.py                     # desktop entry point (thin)
├── web_main.py                 # browser entry point (thin)
├── build.py                    # split per refactoring plan below
├── settings.py                 # -> becomes infrastructure/config/settings.py long-term
├── theme.py                    # -> becomes domain/content/theme.py + CLI picker split out
│
├── application/
│   ├── game.py
│   ├── ports.py
│   ├── snapshot.py
│   └── platform.py             # NEW: Platform/PlatformConfig (M2)
│
├── domain/
│   ├── health.py, combat.py, movement.py, game_state.py   # unchanged
│   ├── map.py                  # NEW: map.load_map/Map move here (pure data + validation)
│   ├── raycasting.py           # NEW: shared cast_ray() used by renderer and NPC visibility (H2)
│   └── content/
│       └── theme.py            # NEW: Theme dataclass + THEMES data
│
├── infrastructure/
│   ├── assets.py, scores.py, input.py   # unchanged
│   └── audio/                  # NEW: split per M1
│       ├── __init__.py
│       ├── desktop.py          # Sound, SilentClip
│       └── browser.py          # BrowserSound, BrowserClip
│
├── presentation/
│   ├── renderer.py             # gains wall/sprite scale caches (H1)
│   └── input.py                # unchanged
│
├── gameplay/                   # NEW: actor coordinators that still need Pygame + domain together
│   ├── player.py
│   ├── npc.py                  # slimmed per M6, delegates to domain.raycasting + systems
│   ├── object_handler.py       # spawn tables move to content/ data files (M7)
│   ├── pathfinding.py
│   ├── sprite_object.py
│   └── weapon.py
│
├── content/                    # NEW: data-driven spawn tables, per M7 (format TBD: JSON/TOML)
│   └── levels/
│
├── maps/, resources/, tests/, tools/, docs/, .github/    # unchanged
└── build/                                                 # unchanged (gitignored output)
```

This keeps the already-correct dependency direction, avoids a disruptive full-repo reshuffle, and gives each of the open findings above a concrete destination.

## File-by-File Refactoring Plan

- ☑ **`raycasting.py` + `npc.py`/`npc_systems.py`**: NPC visibility was extracted into `npc_systems.npc_can_see_player` (M6). The shared DDA traversal itself is still duplicated against `RayCasting.ray_cast`, not yet unified into one `domain/raycasting.py` implementation (H2, still open).
- ☑ **`presentation/renderer.py`**: added wall-column and sprite-scale caches (H1).
- ☑ **`npc.py`**: split into a slim `NPC` coordinator plus `AnimationController`/`CombatResolver` collaborators and a standalone `npc_can_see_player()` function, all in `npc_systems.py` (M6). Hit resolution still claims the first NPC whose crosshair check passes rather than querying the nearest target via the depth buffer (H3, still open, out of scope for this pass).
- ☑ **`object_handler.py`**: scenery positions and enemy weight tables moved into `content/levels/<map_name>.json`, validated (fails loudly if missing) (M7, extends M5).
- ☐ **`infrastructure/audio.py`**: still one file with all four classes; splitting into `infrastructure/audio/desktop.py` and `infrastructure/audio/browser.py` (M1) remains open. `BrowserClip`/theme-level data URI caching (H4's audio-specific angle) also remains open — H4 was addressed at the `Game.new_game()` level (not rebuilding the backend at all on restart) rather than by caching within `BrowserClip` itself.
- ☐ **`application/game.py`**: still no `Platform`/`PlatformConfig` object; `getattr(..., 'browser_mode', False)` checks remain scattered (M2, open).
- ☑ **`build.py`**: `apply_web_html_patches` now raises loudly on a missing substring instead of silently no-op'ing (M3), with unit tests for both the patch functions and the failure path. PyInstaller targets now also bundle `content/` (a gap surfaced by the M7 fix). Splitting `build.py` into separate desktop/web modules, and adding fakeable `BrowserSound`/`BrowserClip` tests (M11), remain open.
- ☑ **`settings.py`**/**`infrastructure/assets.py`**: resolved the duplicate `BASE_DIR` definition (M4). Grouping `settings.py` into small validated config objects (M9) remains open.
- ☐ **`requirements.txt`**: still unpinned (M10, open).

## Summary of Suggested Changes

All five highest-priority items from the Executive Summary are now resolved:

1. ☑ **Performance:** wall-column and sprite scale caching (H1) — measured ~33% faster over 300 profiled frames, ~67% faster specifically in `get_objects_to_render`.
2. ☑ **`NPC` decomposition + hardcoded tables:** `NPC` now delegates to `AnimationController`/`CombatResolver`/`npc_can_see_player` (M6); scenery/spawn tables moved to `content/levels/*.json` (M7), with a packaging fix so PyInstaller builds still work.
3. ☑ **Web-build robustness:** `build.py`'s HTML patching now fails loudly instead of silently, with test coverage (M3).
4. ☑ **Duplicate project-root definition:** `infrastructure/assets.py` now imports `BASE_DIR` from `settings.py` (M4).
5. ☑ **Per-round rebuild waste:** the sound backend is now built once per `Game` instance instead of every restart (H4).

Remaining open items, not part of this pass but worth prioritizing next:

- **H2/H3 (correctness/maintainability):** fully deduplicate the raycasting DDA algorithm; resolve NPC hits against the nearest visible target instead of "first NPC to notice."
- **M1/M2 (housekeeping/extensibility):** split `infrastructure/audio.py` by platform; introduce a `Platform`/`PlatformConfig` object instead of scattered `getattr(..., 'browser_mode', False)` checks.
- **M9/M10/M11 (hardening):** validate `settings.py`'s derived constants; pin dependencies; add fakeable unit tests for `BrowserSound`/`BrowserClip`.

None of this required undoing the layered architecture already in place — it was a matter of finishing the migration into it.
