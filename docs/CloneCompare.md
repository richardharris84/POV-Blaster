# CloneCompare: Two DOOM-Style Game Projects

## Purpose

This report compares the two local projects below and turns the findings into a first-patch guide for POV-Blaster:

- `C:\Users\Richard\Dropbox\Workspace\Code\Python\DOOM-3D-FPS-Shooting-Game`
  - GitHub: `https://github.com/Saurabh-66/DOOM-3D-FPS-Shooting-Game`
- `C:\Users\Richard\Dropbox\Workspace\Code\Python\DOOM-style-Game`
  - GitHub: `https://github.com/StanislavPetrovV/DOOM-style-Game`

POV-Blaster is the current target project and was created as a fork of `DOOM-style-Game`.

The comparison focuses on source lineage, gameplay behavior, architecture, production quality, performance, assets, and the safest high-value improvements to bring into POV-Blaster.

## Executive Finding

`DOOM-3D-FPS-Shooting-Game` copies or derives from `DOOM-style-Game` at the source-code level. The available repository evidence does not show a shared Git ancestry, so it is not a Git fork in the technical sense. However, the implementation similarity is too strong to be an independent recreation:

- Both projects contain the same eleven core Python modules.
- `npc.py` is byte-for-byte identical.
- `sprite_object.py` is byte-for-byte identical.
- The other shared modules are nearly identical, with small changes such as removing diagonal correction, disabling mouse event grabbing, removing the pathfinding cache, changing audio volume, and adding final newlines.
- Both projects implement the same progression: raycasting, player movement, sprites, weapon animation, BFS pathfinding, three enemy types, health, damage, and end screens.
- The newer project README describes the same feature-development sequence and uses the same distinctive code concepts and assets.

The most likely history is that `DOOM-3D-FPS-Shooting-Game` was copied from, or manually reconstructed from, a version of `DOOM-style-Game`, then modified and documented with additional gameplay demonstrations. Exact authorship or licensing conclusions require reviewing the upstream licenses and commit provenance with the project owners; this report only states what the local source evidence supports.

## Repository Evidence

### Git remotes

The projects point to different GitHub repositories:

```text
DOOM-3D-FPS-Shooting-Game
origin https://github.com/Saurabh-66/DOOM-3D-FPS-Shooting-Game

DOOM-style-Game
origin https://github.com/StanislavPetrovV/DOOM-style-Game.git
```

Neither checkout has a remote pointing to the other repository, and their local histories do not share a visible commit ancestor.

### Commit chronology

`DOOM-style-Game` begins in June 2022 and contains later commits specifically named for gameplay changes:

```text
2022-06-22  Initial commit
2022-06-21  DOOM raycasting version
2022-07-30  Update sound.py
2023-03-17  fast diagjnal movement fix
2023-03-17  mouse fix
2023-07-23  path_finding cache
```

The local `DOOM-3D-FPS-Shooting-Game` history begins in January 2023, after the original project had already accumulated most of these features:

```text
2023-01-03  Initial commit
2023-01-03  Update README.md
2023-01-03  Add files via upload
2023-01-04  multiple README and asset updates
2023-01-07  Update README.md
```

The date ordering alone does not prove copying, because repositories can be created from private or unrecorded work. Combined with exact source matches and distinctive behavior, it is strong lineage evidence.

### Source hash comparison

SHA-256 comparison of same-named Python modules produced this result:

| Module | Same bytes? | Interpretation |
|---|---:|---|
| `npc.py` | Yes | Exact implementation match |
| `sprite_object.py` | Yes | Exact implementation match |
| `main.py` | No | One behavioral change plus formatting |
| `map.py` | No | Formatting/newline difference only |
| `object_handler.py` | No | Formatting/newline difference only |
| `object_renderer.py` | No | Formatting/newline difference only |
| `pathfinding.py` | No | Cache removal plus formatting |
| `player.py` | No | Diagonal correction removal plus formatting |
| `raycasting.py` | No | Formatting/newline difference only |
| `settings.py` | No | Formatting/newline difference only |
| `sound.py` | No | Music volume change plus formatting |
| `weapon.py` | No | Formatting/newline difference only |

This pattern is important: differences are concentrated in a few known changes rather than representing two independently designed engines.

### Asset and repository layout comparison

`DOOM-style-Game` contains the runtime `resources/` tree, `requirements.txt`, and `sreenshots/`. `DOOM-3D-FPS-Shooting-Game` contains `photos/` and demonstration GIFs but no visible `resources/` tree or `requirements.txt` in the local checkout. Its source still references paths such as `resources/textures/sky.png` and `resources/sound/theme.mp3`.

That means the newer repository, as checked out locally, appears incomplete for a clean runtime launch unless the missing runtime resources exist elsewhere or are intentionally omitted from the checkout. This is a release-quality regression, not just a documentation difference.

## How Both Projects Work

Both projects implement the same architecture:

```text
main.py
  -> initializes Pygame and constructs Game
  -> constructs map, player, renderer, raycaster, objects, weapon, sound, pathfinding
  -> polls events
  -> updates gameplay systems
  -> draws the frame

map.py              grid cells and wall dictionary
player.py           movement, collision, mouse look, health, firing
raycasting.py       horizontal/vertical grid ray traversal and wall columns
object_renderer.py  sky, floor, walls, sprites, HUD, end screens
sprite_object.py    billboard projection and animation frame loading
object_handler.py   scenery, NPC spawning, actor updates, win detection
npc.py              enemy animation, visibility, movement, attacks, damage
pathfinding.py      walkable graph and BFS first-step navigation
weapon.py           shotgun animation and damage
sound.py            Pygame sound/music loading
```

Each subsystem receives `game` and reaches other subsystems through it. A typical NPC call chain can directly touch the player, map, object handler, pathfinding, renderer, weapon, and sound manager. This is compact but creates high coupling and hidden update-order contracts.

## Behavioral Differences

### `main.py`: mouse capture

`DOOM-style-Game` calls `pg.event.set_grab(True)` during startup. `DOOM-3D-FPS-Shooting-Game` removes that call.

**Effect:** the newer project may allow the mouse to leave the game window or fail to provide the expected FPS mouse-look experience. POV-Blaster should keep mouse capture behind an input-platform adapter and expose a user setting, rather than relying on an unconditional global call.

### `player.py`: diagonal movement

`DOOM-style-Game` includes a diagonal correction factor of `1 / sqrt(2)` and applies it when movement input is present. `DOOM-3D-FPS-Shooting-Game` removes the correction.

**Effect:** holding two movement directions makes the player move approximately 41% faster than holding one direction. This is a gameplay and balance bug. POV-Blaster should retain the corrected vector normalization, but move the calculation into a pure movement system with tests.

### `pathfinding.py`: cache removal

`DOOM-style-Game` adds `@lru_cache` to `get_path`. `DOOM-3D-FPS-Shooting-Game` removes it.

**Effect:** the newer project avoids stale paths caused by the cache reading dynamic `npc_positions` without including occupancy in the cache key. This is a correctness improvement, although it may increase CPU use because BFS can run frequently.

The correct POV-Blaster solution is not to restore the unsafe cache. First remove it, then schedule path requests and cache only against explicit map and occupancy revisions.

### `sound.py`: music volume

The upstream project sets music volume to `0.3`; the newer project sets it to `0.4`.

**Effect:** presentation tuning only. POV-Blaster should make volume data-driven and separate master, music, effects, and UI volume groups.

### Formatting and line endings

Most remaining hash differences are final newline changes. They do not represent meaningful behavior. Formatting changes should not be mistaken for architectural improvements.

## Comparative Strengths

### What `DOOM-style-Game` does better

- Includes the runtime resource tree needed by the current code.
- Has a dependency file.
- Preserves diagonal movement correction.
- Preserves mouse event grabbing used by the original mouse-look flow.
- Has a commit explicitly introducing the pathfinding cache, which exposes the optimization history even though the implementation is unsafe.
- Is the clearer technical ancestor for understanding the code’s evolution.

### What `DOOM-3D-FPS-Shooting-Game` does better

- Provides extensive visual documentation through gameplay GIFs and staged demonstrations.
- Removes the stale pathfinding cache.
- Presents the project as a more complete game walkthrough for a learner.
- Includes a final README narrative covering movement, raycasting, sprites, weapon, pathfinding, enemies, and final gameplay.

### What neither project does well enough

- Neither has a clean separation between domain logic and Pygame.
- Neither has automated tests or CI.
- Neither has reproducible dependency locking.
- Both use wildcard imports and implicit transitive dependencies.
- Both perform expensive scaling and projection work every frame.
- Both use relative asset paths tied to the current working directory.
- Both use blocking delays during victory and game-over transitions.
- Both duplicate ray traversal logic for world rendering and NPC visibility.
- Both use mutable shared state through the `Game` object.
- Both lack a formal asset manifest, schema validation, packaging strategy, profiling baseline, or graceful headless mode.

## Code Quality and Correctness Audit

### Critical correctness risks

#### Ray traversal divisions

In both implementations, wall raycasting divides by `sin_a` and `cos_a`. NPC line-of-sight raycasting duplicates the same approach. Axis-aligned or near-axis-aligned rays can produce unstable or invalid values.

**POV-Blaster action:** implement one tested DDA/grid traversal service with epsilon handling and a structured miss result. Reuse it for wall hits, visibility, and weapon queries.

#### Frame presentation order

Both versions call `pg.display.flip()` from `Game.update()` before `Game.draw()` is called by the loop. The displayed frame is therefore from the prior draw cycle.

**POV-Blaster action:** make the loop order explicit: collect input, update simulation, build render snapshot, draw, present, then tick.

#### Blocking end screens

Both versions call `pg.time.delay(1500)` during win and game-over handling. The window stops processing events during the delay.

**POV-Blaster action:** implement explicit `PLAYING`, `VICTORY`, `GAME_OVER`, and `PAUSED` states with non-blocking timers.

#### Health invariant failure

Damage can make health negative. The HUD then converts health to text and looks up each character in the digit map. A minus sign is not a valid digit key.

**POV-Blaster action:** clamp health to `[0, maximum]` and render health through a robust formatter.

#### Runtime asset mismatch in the newer project

The newer project’s code expects the `resources/` directory, but the checkout exposes `photos/` instead. A clean clone may fail at image or sound loading.

**POV-Blaster action:** centralize resource resolution, add an asset manifest check, and make a clean-install smoke test part of CI.

### Architecture risks

#### `Game` is a mutable service locator

Every actor receives a full game reference. This violates dependency inversion and makes unit testing require a Pygame window, loaded assets, audio, a map, and all managers.

**POV-Blaster action:** use explicit constructor dependencies and application ports. Domain code should not import Pygame.

#### Actors own too many responsibilities

`NPC` combines state, animation, rendering projection, line of sight, pathfinding, movement, attack timing, damage, and sound effects. `Player` similarly combines input polling, movement, collision, health, UI effects, audio, and state transitions.

**POV-Blaster action:** separate state/data from systems. Keep enemy profiles as data and use movement, visibility, combat, animation, and presentation systems.

#### Shared render queue is cross-system mutable state

Raycasting creates `objects_to_render`, while scenery and NPCs append to it during updates. The renderer later sorts and consumes it. Any update-order change can produce stale or missing objects.

**POV-Blaster action:** produce an immutable render snapshot after simulation. The renderer owns its command buffer.

#### Content is hard-coded

Enemy counts, weights, restricted regions, scenery locations, asset paths, wall IDs, and balance values are embedded in Python modules.

**POV-Blaster action:** define versioned level and entity data files, validate them during builds, and use stable content IDs.

## Performance Comparison and Bottlenecks

Both projects have essentially the same performance profile because their core implementations are the same.

### Per-frame renderer cost

At the default 1600x900 resolution:

- `NUM_RAYS` is 800.
- Each ray performs horizontal and vertical grid traversal.
- Each visible wall ray creates a subsurface and scales it.
- Each visible sprite can be scaled every frame.
- The renderer sorts the combined wall/sprite list every frame.

This creates significant Python object allocation and Pygame surface work. A larger map, more sprites, higher resolution, or more enemies will increase cost quickly.

### NPC cost

Each NPC can:

- Run sprite projection math.
- Run a visibility ray traversal.
- Request BFS navigation.
- Animate and possibly attack.
- Perform collision checks.

With 20 NPCs this may be acceptable on a desktop. It is not a scalable design for large actor counts or variable hardware.

### Better performance plan for POV-Blaster

1. Profile before changing algorithms. Record frame time, simulation time, render time, visible sprites, active NPCs, path requests, and allocations.
2. Precompute ray angles and trigonometric values when camera configuration is unchanged.
3. Implement DDA once and reuse it.
4. Add a depth buffer for wall columns.
5. Cache texture surfaces and bounded sprite scale variants.
6. Use quality tiers for ray count, texture resolution, sprite distance, and effects.
7. Schedule NPC visibility and pathfinding at different rates based on distance and state.
8. Use spatial partitioning for actor queries once levels grow.
9. Use typed render commands and avoid creating unnecessary lists/surfaces.
10. Re-evaluate the renderer backend only after profiling identifies the actual limit.

## Asset and Content Comparison

### Runtime asset design

`DOOM-style-Game` uses a predictable runtime tree:

```text
resources/
  sound/
  sprites/
    animated_sprites/
    npc/
    static_sprites/
    weapon/
  textures/
    digits/
```

The newer project uses `photos/` for demonstrations but does not show the runtime assets expected by the code. Demonstration media is not a substitute for packaged game content.

### Recommendations

- Keep source art, demonstration media, and runtime-generated assets separate.
- Add an asset manifest with stable IDs, hashes, dimensions, animation frames, and schema version.
- Validate every referenced asset during CI and packaging.
- Sort animation frames numerically; filesystem order is not guaranteed.
- Load assets once through an `AssetManager`; do not load them per round or per actor.
- Resolve paths relative to the installed package or executable.
- Use content-addressed bundles and patch manifests for future distribution.
- Track asset licenses and attribution separately from code provenance.

## First Patch Guidance for POV-Blaster

The first patch should improve the foundation without changing the game’s visual identity or replacing Pygame. Keep the patch narrow enough to review and test.

### Patch 1A: correctness and runtime reliability

Recommended scope:

- Move `display.flip()` to the end of the draw cycle.
- Clamp player health and harden the health HUD.
- Remove or avoid stale path caching.
- Add ray denominator guards and defined ray misses.
- Sort animation frame filenames deterministically.
- Validate map shape, player spawn, wall texture IDs, and asset presence.
- Sample unique NPC spawn cells.
- Replace blocking victory/game-over delays with a small state machine.
- Add graceful shutdown and optional no-audio mode.

This patch gives the highest immediate quality return and creates seams for later refactoring.

### Patch 1B: explicit dependencies and testable core

After reliability is protected:

- Replace wildcard imports.
- Add a package under `src/pov_blaster`.
- Extract pure geometry, map, collision, health, combat, and navigation code.
- Define `InputPort`, `ClockPort`, `AudioPort`, and `AssetCatalog` interfaces.
- Convert Pygame input/audio/display behavior into adapters.
- Add unit tests that run without a window.

Do not combine this with a graphics backend replacement. The first architectural goal is testability and clear ownership.

### Patch 1C: measured rendering improvements

Once tests exist:

- Add a depth buffer.
- Cache repeated wall and sprite transformations.
- Reduce render-list allocations.
- Add a frame-time overlay and profile representative maps.
- Add configurable quality tiers.

Only choose a new graphics library if measurements and product requirements demonstrate that the optimized raycaster cannot meet the target.

## Proposed Clean Architecture for POV-Blaster

### Domain

Pure Python game rules:

- `WorldState`, transforms, actor state, health, weapons.
- Map collision and navigation queries.
- Player movement and look rules.
- NPC state transitions and decisions.
- Combat and damage resolution.
- Victory and game-over rules.
- Deterministic random source.

### Application

Coordinates use cases and simulation phases:

- Input command handling.
- Fixed-step simulation.
- Movement and collision system.
- Visibility and navigation system.
- Combat system.
- Animation system.
- Game-state transition system.
- Render snapshot builder.

### Infrastructure

Implements external systems:

- Pygame window and event adapter.
- Pygame renderer.
- Asset manager and resource resolver.
- Audio adapter.
- Configuration/content parser.
- Optional persistence, telemetry, patching, and networking.

### Presentation

Consumes snapshots and renders them:

- Raycast wall renderer.
- Sprite renderer.
- HUD and menu renderer.
- Debug overlays.
- Victory/game-over screens.

The domain must not depend on any presentation or infrastructure module.

## Suggested Target Folder Structure

```text
POV-Blaster/
├── pyproject.toml
├── README.md
├── CodeBase.md
├── CodeAudit.md
├── CloneCompare.md
├── src/
│   └── pov_blaster/
│       ├── __main__.py
│       ├── app/
│       │   ├── bootstrap.py
│       │   ├── game_loop.py
│       │   ├── game_state.py
│       │   └── composition.py
│       ├── domain/
│       │   ├── actors/
│       │   ├── combat/
│       │   ├── navigation/
│       │   ├── world/
│       │   ├── events.py
│       │   └── geometry.py
│       ├── application/
│       │   ├── commands.py
│       │   ├── game_session.py
│       │   ├── snapshots.py
│       │   └── systems/
│       ├── ports/
│       │   ├── assets.py
│       │   ├── audio.py
│       │   ├── clock.py
│       │   ├── input.py
│       │   └── rendering.py
│       ├── presentation/
│       │   ├── renderer.py
│       │   ├── raycaster.py
│       │   ├── sprites.py
│       │   └── hud.py
│       ├── infrastructure/
│       │   ├── assets/
│       │   ├── audio/
│       │   ├── config/
│       │   ├── input/
│       │   └── pygame_platform/
│       └── content/
│           ├── levels/
│           ├── entities/
│           ├── textures/
│           ├── sprites/
│           └── audio/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── tools/
│   ├── validate_assets.py
│   └── profile_game.py
└── resources/
```

## Current-to-Target File Map

| Current file | Target ownership |
|---|---|
| `main.py` | `app/bootstrap.py`, `app/game_loop.py`, `app/composition.py` |
| `settings.py` | `infrastructure/config/` typed configuration |
| `map.py` | `domain/world/`, content level loader, presentation debug map |
| `player.py` | `domain/actors/`, application movement/combat systems, input adapter |
| `raycasting.py` | pure domain geometry plus `presentation/raycaster.py` |
| `object_renderer.py` | `presentation/renderer.py`, `presentation/hud.py` |
| `sprite_object.py` | `presentation/sprites.py`, animation domain/controller, asset manager |
| `object_handler.py` | application actor registry and spawn system |
| `npc.py` | domain actor profiles plus AI, visibility, movement, and combat systems |
| `pathfinding.py` | `domain/navigation/` and application navigation scheduler |
| `weapon.py` | domain combat weapon model plus presentation weapon renderer |
| `sound.py` | `ports/audio.py` and `infrastructure/audio/pygame_audio.py` |
| `requirements.txt` | `pyproject.toml` and locked release constraints |
| `resources/` | validated `content/` and packaged asset bundles |

## Tests Required Before Calling the First Patch Complete

### Pure unit tests

- Map dimensions and wall conversion.
- Invalid map and spawn validation.
- Player movement normalization.
- Collision against walls and sliding behavior.
- Ray hits, misses, axis-aligned rays, and near-wall rays.
- BFS route validity and no-route behavior.
- Dynamic occupancy behavior without stale cache results.
- Unique valid NPC spawning.
- Health clamping and recovery.
- Damage, death, victory, and game-over events.
- Deterministic random spawn results from a seed.
- Numeric animation frame ordering.

### Integration tests

- Startup from a clean checkout.
- Asset manifest validation.
- Headless game-session update without a display.
- Pygame adapter startup with audio disabled.
- One complete render frame with a known map.
- Repeated victory/game-over round resets without resource growth.
- Packaging smoke test from outside the repository root.

### Performance tests

- Baseline frame time at default settings.
- Frame time at higher NPC counts.
- Pathfinding requests per second.
- Asset load time and memory usage.
- Ten-minute soak test with repeated animation and combat.
- Repeated round restart memory/resource test.

## Upgrade Plan: Quality, Scalability, and Maintainability Requirements

The upgrade plan must meet these standards:

### Quality gates

- No unhandled asset or audio startup failures.
- No blocking calls in the game loop.
- No hidden cross-system mutation for gameplay-critical behavior.
- All domain invariants enforced at their boundary.
- Deterministic tests for all core rules.
- Clean shutdown on quit, exception, or platform close.

### Scalability gates

- Rendering cost measured and bounded by quality settings.
- NPC updates scheduled by relevance, not blindly every frame.
- Pathfinding work budgeted per frame.
- Asset loading cached and separated from round lifecycle.
- Content delivered through manifests and versioned bundles.
- Optional online services isolated from the local game core.
- No assumption that one process, one map, or one machine serves all users.

### Maintainability gates

- Explicit imports and typed public interfaces.
- Clear dependency direction toward the domain.
- One owner for each state transition and each render buffer.
- No hard-coded level content in behavior classes.
- CI runs linting, type checks, unit/integration tests, asset checks, and packaging checks.
- Architecture decisions and compatibility constraints are documented.

## Final Recommendation

POV-Blaster should take the strongest parts of both projects without copying either implementation forward unchanged:

- Take the complete runtime asset organization and diagonal movement correction from `DOOM-style-Game`.
- Take the removal of the unsafe dynamic path cache and the learner-friendly visual documentation approach from `DOOM-3D-FPS-Shooting-Game`.
- Do not adopt either project’s tightly coupled `Game` service-locator architecture as the long-term design.
- Do not treat the newer project’s `photos/` demonstrations as runtime assets; preserve a validated `resources/` or packaged `content/` tree.
- Build the first patch around correctness, deterministic behavior, asset reliability, and tests.
- Follow with explicit domain/application/infrastructure/presentation boundaries and measured renderer improvements.

The goal is not merely to make POV-Blaster a cleaner clone. It should become the most reliable and extensible version: a portable game core, a replaceable renderer, validated high-quality content, predictable performance, and a service boundary that can support large-scale distribution without contaminating the local game loop.
