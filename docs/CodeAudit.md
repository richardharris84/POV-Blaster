# POV-Blaster Code Audit and Architecture Refactoring Plan

## Executive Summary

POV-Blaster is a promising raycasting prototype with a clear gameplay loop, working asset-driven sprites, three enemy types, and a compact grid world. It is not yet structured for production deployment or a large audience. The current code is organized around a single `Game` object that every subsystem can reach and mutate. That is convenient for a prototype, but it makes behavior difficult to test, easy to break during refactoring, and impossible to scale cleanly across rendering, simulation, tools, and online services.

The highest-priority improvements are:

1. Fix correctness hazards in the frame lifecycle, raycasting edge cases, health/HUD handling, spawning, and pathfinding cache behavior.
2. Separate pure game rules from Pygame and filesystem/audio APIs.
3. Replace wildcard imports and implicit global configuration with explicit interfaces and typed data models.
4. Build a renderer with reusable texture/frame caches, a depth buffer, and fewer per-frame allocations.
5. Make game state transitions non-blocking and explicit.
6. Add deterministic tests, headless execution, profiling, continuous integration, and asset validation.
7. Treat “millions of users” as a distribution and operations problem as well as an engine problem: the desktop client must remain self-contained, while telemetry, patching, accounts, matchmaking, and other services must be separate from the local simulation.

The recommended architecture is a modular monolith first: a clean, testable single-player engine with stable interfaces. Once that foundation exists, online or platform services can be added around it without coupling network code to frame-by-frame gameplay.

## Audit Scope and Rating Model

Reviewed the current source modules and the project reconstruction guide in [CodeBase.md](CodeBase.md):

- [main.py](main.py)
- [settings.py](settings.py)
- [map.py](map.py)
- [player.py](player.py)
- [raycasting.py](raycasting.py)
- [object_renderer.py](object_renderer.py)
- [sprite_object.py](sprite_object.py)
- [object_handler.py](object_handler.py)
- [npc.py](npc.py)
- [pathfinding.py](pathfinding.py)
- [weapon.py](weapon.py)
- [sound.py](sound.py)
- [requirements.txt](requirements.txt)

Severity levels:

- **Critical**: can prevent startup, corrupt a game session, or make a future production build unsafe.
- **High**: likely correctness, stability, or major performance problem.
- **Medium**: maintainability, testability, or scalability risk that will become expensive as content grows.
- **Low**: cleanup or design improvement with limited immediate user impact.

## Current Architecture

The current runtime is a synchronous client with these stages:

```text
Pygame event queue
        |
        v
Game.check_events() -> Player / global animation trigger
        |
        v
Player.update() -> RayCasting.update() -> ObjectHandler.update() -> Weapon.update()
        |                    |                    |
        |                    |                    +--> NPC AI, animation, victory
        |                    +--> wall columns and shared render list
        +--> movement, collision, mouse look, health recovery
        |
        v
Game.draw()
  -> ObjectRenderer background, world objects, HUD
  -> Weapon foreground
  -> display presentation
```

The design has useful prototype traits:

- Map coordinates are easy to understand.
- Gameplay values are centralized in `settings.py` or actor classes.
- `SpriteObject` provides a reusable base for scenery and animated actors.
- Wall and sprite projection use the same depth-sorted render collection.
- NPC subclasses express balance differences without duplicating the state machine.

The central architectural problem is that `Game` is both composition root and shared mutable dependency registry. For example, an NPC can directly call the renderer, sound system, player, weapon, object handler, map, and pathfinding service. This makes it hard to run NPC rules without a window, audio device, or fully initialized game.

## Findings

### Critical and High-Priority Findings

### H1. Frame presentation occurs before the current frame is drawn

**Location:** `Game.update` and `Game.draw` in [main.py](main.py)

`Game.update()` calls `pg.display.flip()` before `Game.run()` calls `draw()`. The display therefore presents the previous frame, then the next frame is drawn after presentation. This creates a one-frame visual delay and makes timing behavior harder to reason about.

**Recommendation:** use an explicit frame pipeline:

```text
poll input
simulate with fixed or bounded delta time
build render snapshot
render
present
limit frame rate
```

Move `display.flip()` to the end of `draw()` or, preferably, to the end of the main loop. Call `clock.tick()` once per frame and pass the resulting delta into the simulation.

### H2. Raycasting can divide by values near zero

**Location:** `RayCasting.ray_cast` in [raycasting.py](raycasting.py), and the duplicate visibility algorithm in `NPC.ray_cast_player_npc` in [npc.py](npc.py)

Horizontal intersections divide by `sin_a`; vertical intersections divide by `cos_a`. The small starting angle offset does not protect every ray from a near-zero denominator. The NPC visibility code has the same risk. A ray aligned with an axis can create unstable depths, huge projections, or runtime exceptions.

**Recommendation:** use a single tested DDA/grid traversal implementation with epsilon handling. Treat an axis-aligned component below a small threshold as an infinite distance for that traversal. Return a structured `RayHit` with `hit`, `distance`, `cell`, `side`, and `texture_id`, including a defined miss result.

### H3. The renderer performs expensive work and allocations every frame

**Location:** `RayCasting.get_objects_to_render`, `SpriteObject.get_sprite_projection`, and `ObjectRenderer.render_game_objects`

For each wall ray, the current implementation creates a texture subsurface and scales it. For each visible sprite, it scales the source image every frame. It also creates a new render list and sorts the complete list every frame. At 1600x900, the game casts 800 rays, and this work is repeated without a cache or profiling budget.

**Recommendation:**

- Cache wall columns by texture, offset bucket, and projected-height bucket, or render columns through a more direct surface/buffer path.
- Cache sprite scale variants or use a bounded distance-based sprite cache.
- Replace per-object image scaling with a renderer-owned sprite batch/cache.
- Use a depth buffer so sprite pixels can be compared against wall depth instead of relying only on painter sorting.
- Measure before and after with `cProfile`, `py-spy`, or a custom frame-time overlay.
- Consider lowering ray count independently from window resolution and using a configurable quality tier.

### H4. `lru_cache` caches pathfinding results while NPC occupancy changes

**Location:** `PathFinding.get_path` in [pathfinding.py](pathfinding.py)

The cache key contains only `start` and `goal`. BFS also reads `game.object_handler.npc_positions`, which changes every frame. A cached result can therefore reflect stale obstacles and produce incorrect movement or congestion.

**Recommendation:** first remove `@lru_cache` for correctness. Later, use a navigation service with a map revision and occupancy revision, or calculate paths on a schedule rather than for every NPC on every frame. For larger maps, use hierarchical navigation, flow fields for groups, or an incremental pathfinding algorithm.

### H5. Game state transitions block the main loop

**Location:** `Player.check_game_over` and `ObjectHandler.check_win`

Both methods draw an overlay, call `pg.display.flip()`, and block with `pg.time.delay(1500)` before rebuilding the game. During the delay, input and window events are not processed. This can cause an unresponsive window and makes automated testing difficult.

**Recommendation:** create explicit states such as `PLAYING`, `GAME_OVER`, `VICTORY`, `PAUSED`, and `LOADING`. Each state has `enter`, `handle_event`, `update`, and `render` methods. Store a transition deadline and continue pumping events while the result screen is displayed.

### H6. New rounds repeatedly initialize audio and load assets

**Location:** `Game.new_game` in [main.py](main.py), `ObjectRenderer`, `Weapon`, `AnimatedSprite`, and [sound.py](sound.py)

Every win or loss constructs new renderers, sprites, weapon images, sounds, and music state. This increases transition latency and can leak or churn native resources. It also makes a repeated-round soak test more likely to expose resource problems.

**Recommendation:** separate long-lived services from per-round state. Load an `AssetManager`, `AudioManager`, and renderer once at application startup. Rebuild only a `WorldSession` or gameplay state on restart. Provide explicit `close()`/`shutdown()` methods.

### H7. Asset paths depend on the current working directory

**Location:** all relative asset loads, especially [object_renderer.py](object_renderer.py), [sprite_object.py](sprite_object.py), and [sound.py](sound.py)

Launching from outside the repository root can fail even when all assets exist. This will be especially fragile in packaged builds, test runners, and platform launchers.

**Recommendation:** use `pathlib.Path` and a resource root derived from the package or executable location. Centralize loading in an asset service and validate all required assets at startup with actionable errors.

### H8. NPC spawning is nondeterministic and can produce duplicate occupancy

**Location:** `ObjectHandler.spawn_npc` in [object_handler.py](object_handler.py)

Enemies are selected randomly and cells are repeatedly sampled until a valid cell is found. Spawned positions are not reserved, so several NPCs can occupy the same map cell. The loop also assumes that at least 20 valid cells remain after walls and the restricted area are removed.

**Recommendation:** build a list of valid spawn points once, validate the requested count, use a seeded random generator, sample without replacement, and keep the seed in a match/replay configuration. Make spawn rules data-driven rather than hard-coded in the handler.

### H9. Player health and HUD rendering are not robust to all values

**Location:** `Player.get_damage`, `Player.recover_health`, and `ObjectRenderer.draw_player_health`

Damage is not clamped. If health falls below zero, `str(health)` can contain a minus sign that is not present in the digit dictionary. The HUD loop also assumes the health string contains at least one valid digit. A future damage source could therefore produce a rendering exception during a critical game state.

**Recommendation:** model health as an invariant: `0 <= current <= maximum`. Clamp damage and healing in the domain model, render a numeric health value through a safe formatter, and keep the health icon separate from digit rendering.

### H10. NPC hitscan and world occlusion are approximate

**Location:** `NPC.check_hit_in_npc` and sprite projection in [npc.py](npc.py) and [sprite_object.py](sprite_object.py)

A shot hits when the NPC's projected horizontal bounds contain the screen center and the NPC has line of sight. There is no per-pixel or wall-depth comparison at the hit column, and the first qualifying NPC in update order may consume the shot rather than the nearest visible target. The shared painter sort also does not provide true per-column occlusion.

**Recommendation:** create a shot query from the camera through the depth buffer, select the nearest hit actor, and apply damage through a combat service. For a sprite-based renderer, test the projected hit column against wall depth and actor depth. Keep the simplified approach only as an explicitly documented gameplay choice.

### H11. The update graph contains hidden ordering dependencies

**Location:** [main.py](main.py), [object_handler.py](object_handler.py), and [npc.py](npc.py)

`ObjectHandler` rebuilds `npc_positions`, then NPCs move while reading that snapshot. NPCs also use their previously calculated projection fields during hit detection. The correctness of shooting, AI, and collision depends on update order that is not represented by interfaces.

**Recommendation:** divide simulation into phases: input collection, intent generation, movement/collision, combat resolution, animation, and render snapshot generation. Pass immutable snapshots or explicit services between phases. Avoid actors mutating unrelated systems during their own `update` calls.

### Medium-Priority Findings

### M1. Wildcard imports obscure dependencies and increase name collision risk

**Location:** all gameplay modules

Statements such as `from settings import *` and `from sprite_object import *` make it unclear where `math`, `pg`, `deque`, or constants originate. This is particularly misleading in `npc.py` and `weapon.py`, where names arrive indirectly through wildcard imports.

**Recommendation:** use explicit imports and package-qualified modules. Add a linter such as Ruff and enforce unused-import and undefined-name checks in CI.

### M2. Domain logic is coupled directly to Pygame APIs

Player rules call `pg.key.get_pressed`, `pg.mouse`, `pg.time.get_ticks`, display methods, and sound playback. NPC rules call renderer and sound objects directly. This prevents fast unit tests and complicates headless server or replay execution.

**Recommendation:** define ports/interfaces such as `InputSource`, `Clock`, `AudioPlayer`, and `PresentationSink`. Keep domain objects operating on commands, events, and elapsed time. Put Pygame adapters in an infrastructure layer.

### M3. Timing uses a shared event pulse instead of elapsed-time animation

**Location:** `Game.global_event`, `AnimatedSprite.check_animation_time`, and `NPC.animate_death`

A Pygame timer event is used as a global animation trigger, while other animation methods use timestamps. This makes timing behavior depend on event delivery and complicates pause, replay, and deterministic simulation.

**Recommendation:** pass `delta_seconds` into animation components and accumulate local time. Use the same clock abstraction for all timers. Make animation frame selection independent of render frame rate.

### M4. Animation frame ordering is nondeterministic

**Location:** `AnimatedSprite.get_images` in [sprite_object.py](sprite_object.py)

`os.listdir` does not guarantee numeric frame order. An animation may load `10.png` before `2.png` depending on the filesystem.

**Recommendation:** filter image files and sort by a numeric frame key. Validate that every animation has at least one frame and consistent dimensions.

### M5. The map model mixes content data, navigation data, and renderer assumptions

**Location:** [map.py](map.py), [pathfinding.py](pathfinding.py), [object_renderer.py](object_renderer.py)

The map is a module-level mutable list, integer wall IDs double as texture IDs, and debug drawing assumes a 100-pixel tile size. This makes level variants, streaming, collision rules, and editor tooling harder to add.

**Recommendation:** introduce a `LevelDefinition` data model with dimensions, cell types, spawn markers, and asset references. Build separate `CollisionGrid`, `NavigationGrid`, and render-friendly wall data from that definition.

### M6. NPC classes combine data, AI, animation, rendering, combat, and audio

`NPC` is responsible for projected sprite state, animation frames, line-of-sight raycasting, movement, pathfinding, attacks, damage, and sound. Adding network replication, more weapons, status effects, or behavior trees will make this class grow rapidly.

**Recommendation:** split actor data/components from systems: `ActorState`, `NpcDecisionSystem`, `MovementSystem`, `VisibilitySystem`, `CombatSystem`, and `AnimationController`. Keep `Soldier`, `Cacodemon`, and `Cyberdemon` as data/configuration profiles.

### M7. The object manager has hard-coded content registration

**Location:** `ObjectHandler.__init__` in [object_handler.py](object_handler.py)

Scenery positions, enemy weights, restricted areas, and enemy count are embedded in Python code. Content changes require code changes and cannot be validated or authored by tools easily.

**Recommendation:** move level entities and spawn tables into JSON, TOML, or a versioned content format. Validate content schemas during build. Keep Python classes for behavior, not level placement.

### M8. Shared render lists are an unsafe cross-system mutable API

**Location:** `RayCasting.objects_to_render`, `SpriteObject.get_sprite_projection`, and `ObjectRenderer.render_game_objects`

Raycasting initializes the list, then sprites append to it during object updates. Any update-order change can cause missing or stale render entries. Tuple positions also do not express whether the item is a wall, sprite, UI element, or debug primitive.

**Recommendation:** introduce typed render commands or a `RenderSnapshot` built after simulation. Let the renderer own the command buffer and clear/submit it in one place.

### M9. Configuration is globally imported and not validated

**Location:** [settings.py](settings.py)

Changing resolution, FOV, ray count, or texture size can create incompatible derived values. There is no validation for positive dimensions, supported texture IDs, map shape, or player placement.

**Recommendation:** load a typed `GameConfig`, validate it at startup, and derive values through a configuration object. Keep gameplay tuning separate from display and renderer quality settings.

### M10. The dependency specification is not reproducible

**Location:** [requirements.txt](requirements.txt)

The dependency is unpinned. A future Pygame release or Python/platform combination could change behavior.

**Recommendation:** use a lock or constraints file for release builds, test supported Python/Pygame combinations, and keep a simple developer requirements file separate from production packaging metadata.

### Low-Priority Findings

### L1. Naming and style reduce maintainability

`mini_map` is not actually a minimap; the former `sreenshots` directory was misspelled; `IMAGE_WIDTH` and `SPRITE_SCALE` look like constants but are instance fields; and several methods contain commented-out debug code. These are small issues individually but accumulate in a project intended for handoff.

**Recommendation:** rename through a deliberate migration, remove dead code, use consistent `snake_case` for instance fields, and keep debug features behind a developer configuration.

### L2. List comprehensions are used for side effects

`Map.draw` and `ObjectHandler.update` use comprehensions only to invoke methods. This is less readable and needlessly creates a list.

**Recommendation:** use ordinary `for` loops. The intent is clearer and future error handling is easier.

### L3. Blocking and direct resource behavior complicates shutdown

There is no central cleanup path for display, mixer, timer, or mouse grab state. A production client needs graceful shutdown for window close, exceptions, and platform termination.

**Recommendation:** use a top-level `try/finally` that calls application shutdown, stops music, releases input capture, and calls `pygame.quit()`.

## Performance and Rendering Strategy

### Current cost centers

The current renderer is CPU-bound Python/Pygame work:

- Approximately 800 rays at the default 1600-pixel width.
- Two grid traversals per ray.
- A texture crop and scale for many wall columns.
- A sprite projection and scale for every registered visible object.
- A complete depth sort of walls plus sprites.
- NPC line-of-sight ray traversal and BFS requests during updates.
- Image and sound work that is currently owned by gameplay objects rather than a shared cache.

The prototype can be made much faster without immediately replacing Pygame, but millions of concurrent users would not be served by scaling one Python process. The client runs locally for each user; server scale belongs in separately designed services.

### Recommended renderer evolution

**Phase 1: preserve the raycaster**

- Use a depth array indexed by ray/column.
- Implement DDA traversal once for walls and visibility queries.
- Precompute trigonometric values for the ray angles when the FOV/ray count is unchanged.
- Cache texture surfaces and integer source rectangles.
- Avoid repeated `smoothscale` calls during steady-state rendering.
- Use integer coordinates at the final blit boundary.
- Add quality settings for ray count, texture resolution, sprite distance, and shadow/detail effects.

**Phase 2: introduce a render snapshot**

- Simulation produces camera state, wall hits, actor transforms, and UI state.
- Renderer consumes that snapshot without mutating gameplay.
- Render commands are typed and owned by the renderer.
- A depth buffer handles world occlusion and nearest-target selection.

**Phase 3: choose a graphics backend based on product goals**

If the game remains a retro single-player title, optimized Pygame or a small SDL/OpenGL layer may be sufficient. If the project expands to high-resolution lighting, many actors, multiplayer spectators, or modern effects, evaluate an established engine such as Godot or another suitable engine rather than building a complete GPU renderer in Python. The architecture should keep gameplay rules portable so this decision remains possible.

### Simulation performance

- Use a fixed simulation timestep with an accumulator for deterministic movement and combat.
- Bound incoming frame delta after pauses or debugger breaks.
- Update distant NPCs at lower frequency or use simplified awareness/movement tiers.
- Schedule pathfinding work over frames instead of running BFS for every active NPC every frame.
- Use spatial partitioning for actors and visibility candidates once the world grows.
- Pool transient effects and render commands if profiling proves allocation pressure significant.
- Measure frame time, simulation time, render time, active actors, path requests, and asset cache misses.

## Scalability Architecture for Millions of Users

“Millions of users” should not mean putting millions of actors or network requests into one game loop. It means designing independent clients and services that can scale horizontally.

### Client

The desktop client should own:

- Input and local presentation.
- Local deterministic simulation for the current game mode.
- Asset cache and patchable content.
- Accessibility, settings, and platform integration.
- Crash reporting and privacy-conscious telemetry.

The client should not require a database, account service, or internet connection for a local single-player mode.

### Game services, if multiplayer is added later

Keep these outside the renderer and local domain model:

- Authentication/account service.
- Matchmaking or session allocation service.
- Authoritative match server.
- Presence and social service.
- Content manifest and patch distribution service.
- Telemetry/analytics pipeline.
- Leaderboard or progression service.

Use stateless horizontally scalable APIs where possible. Keep match state in a dedicated session process or actor model. Define a versioned protocol and validate all client input on the server. Do not make Pygame objects or render surfaces part of the network contract.

### Content and asset scale

The current repository loads files directly from a local folder. For a larger product:

- Build an asset manifest containing IDs, hashes, dimensions, animation metadata, and compatibility version.
- Validate assets in CI.
- Use compressed release bundles and content-addressed caching.
- Separate source assets from generated runtime assets.
- Stream large optional content rather than loading every asset at startup.
- Keep content IDs stable so levels and replays remain compatible.
- Version level schemas and provide migrations.

## Target Clean Architecture

Use dependency direction from the inside outward:

```text
                    +----------------------+
                    |  Composition / App   |
                    +----------+-----------+
                               |
        +----------------------+----------------------+
        |                                             |
+-------v--------+                           +--------v--------+
| Infrastructure |                           |   Presentation  |
| Pygame, audio, |                           | renderer, HUD,  |
| files, network |                           | input adapters  |
+-------+--------+                           +--------+--------+
        |                                             |
        +----------------------+----------------------+
                               v
                    +----------------------+
                    |      Application    |
                    | use cases, phases,  |
                    | commands/events     |
                    +----------+-----------+
                               |
                               v
                    +----------------------+
                    |        Domain        |
                    | world, actors, rules,|
                    | collision, combat    |
                    +----------------------+
```

### Domain layer

Pure Python. No Pygame imports, file reads, sound calls, or display references.

Suggested responsibilities:

- `WorldState`, `Entity`, `Transform`, `Health`, and `WeaponState`.
- Map collision and navigation queries.
- Player movement rules.
- NPC state and decision rules.
- Combat and damage resolution.
- Game phase transitions.
- Deterministic random source passed explicitly into systems.

### Application layer

Coordinates use cases and simulation phases:

- `GameSession`.
- `InputCommand` processing.
- Fixed-step update loop.
- `NpcUpdateSystem`.
- `CombatSystem`.
- `NavigationSystem`.
- `AnimationSystem`.
- `RenderSnapshotBuilder`.
- `VictorySystem` and `GameOverSystem`.

The application layer depends on domain interfaces such as `Clock`, `Navigator`, `AudioPort`, and `AssetCatalog`, not on concrete Pygame classes.

### Infrastructure layer

Concrete adapters:

- Pygame window and event adapter.
- Pygame texture and sprite loader.
- Pygame audio adapter.
- Filesystem/resource locator.
- Optional telemetry, networking, persistence, and patch clients.
- Configuration and content parsers.

### Presentation layer

Consumes immutable snapshots:

- Raycast renderer.
- Sprite renderer.
- HUD renderer.
- Menus and state screens.
- Debug overlay.

Presentation may use Pygame, but domain and application code should not call into it directly.

## Suggested New Folder Structure

```text
POV-Blaster/
├── pyproject.toml
├── README.md
├── CodeBase.md
├── CodeAudit.md
├── LICENSE
├── src/
│   └── pov_blaster/
│       ├── __init__.py
│       ├── __main__.py
│       ├── app/
│       │   ├── bootstrap.py
│       │   ├── game_loop.py
│       │   ├── game_state.py
│       │   └── service_container.py
│       ├── domain/
│       │   ├── actors/
│       │   │   ├── actor.py
│       │   │   ├── player.py
│       │   │   └── enemy_profiles.py
│       │   ├── combat/
│       │   │   ├── combat_service.py
│       │   │   ├── damage.py
│       │   │   └── weapons.py
│       │   ├── navigation/
│       │   │   ├── collision.py
│       │   │   ├── grid.py
│       │   │   └── pathfinder.py
│       │   ├── world/
│       │   │   ├── level.py
│       │   │   ├── map_model.py
│       │   │   └── spawn_rules.py
│       │   ├── events.py
│       │   ├── geometry.py
│       │   └── value_objects.py
│       ├── application/
│       │   ├── commands.py
│       │   ├── game_session.py
│       │   ├── systems/
│       │   │   ├── actor_system.py
│       │   │   ├── animation_system.py
│       │   │   ├── combat_system.py
│       │   │   ├── movement_system.py
│       │   │   └── navigation_system.py
│       │   └── snapshots.py
│       ├── ports/
│       │   ├── asset_catalog.py
│       │   ├── audio.py
│       │   ├── clock.py
│       │   ├── input.py
│       │   └── navigation.py
│       ├── presentation/
│       │   ├── hud.py
│       │   ├── render_snapshot.py
│       │   ├── renderer.py
│       │   ├── raycaster.py
│       │   └── sprite_renderer.py
│       ├── infrastructure/
│       │   ├── assets/
│       │   │   ├── asset_manager.py
│       │   │   └── manifest.py
│       │   ├── audio/
│       │   │   └── pygame_audio.py
│       │   ├── config/
│       │   │   └── settings.py
│       │   ├── input/
│       │   │   └── pygame_input.py
│       │   ├── platform/
│       │   │   └── pygame_window.py
│       │   └── persistence/
│       └── content/
│           ├── levels/
│           ├── entities/
│           ├── textures/
│           ├── sprites/
│           └── audio/
├── tests/
│   ├── unit/
│   │   ├── test_collision.py
│   │   ├── test_combat.py
│   │   ├── test_map.py
│   │   ├── test_pathfinding.py
│   │   └── test_spawning.py
│   ├── integration/
│   │   ├── test_game_session.py
│   │   └── test_asset_loading.py
│   └── fixtures/
├── tools/
│   ├── validate_assets.py
│   └── profile_game.py
└── resources/  # temporary compatibility location during migration
```

Keep the existing `resources/` folder during migration. Move or copy content only after the asset manager and packaging process are ready.

## File-by-File Refactoring Plan

### [main.py](main.py)

- Reduce `Game` to composition root and lifecycle coordinator.
- Move event translation into a Pygame input adapter.
- Move frame timing into `GameLoop`.
- Add explicit state machine and non-blocking transitions.
- Present the frame after drawing.
- Add graceful shutdown.

### [settings.py](settings.py)

- Replace wildcard-imported constants with `GameConfig`, `DisplayConfig`, `RenderConfig`, and `GameplayConfig`.
- Validate derived values and keep quality settings separate.
- Add supported-resolution and quality profiles.

### [map.py]

- Replace module-level mutable map data with a `LevelDefinition`.
- Validate rectangular dimensions, boundary walls, texture IDs, and player spawn.
- Generate collision and navigation views from one source.
- Move debug drawing to presentation/debug code.

### [player.py](player.py)

- Move health, movement, and firing rules into domain/application services.
- Accept input commands and elapsed time rather than reading Pygame directly.
- Return events such as `PlayerDamaged`, `ShotRequested`, and `PlayerDefeated`.
- Use a proper collision shape and clamped health invariant.

### [raycasting.py](raycasting.py)

- Extract pure DDA/grid traversal.
- Remove dependency on `game` and renderer textures.
- Return typed ray-hit data.
- Add axis-aligned, miss, boundary, and near-wall tests.
- Add depth-buffer output.

### [object_renderer.py](object_renderer.py)

- Split background, world, HUD, and end-state rendering.
- Consume a render snapshot rather than reading mutable game objects.
- Centralize asset access and cache scaled resources.
- Make dimensions and integer surface operations explicit.

### [sprite_object.py](sprite_object.py)

- Split sprite transform/projection math from image loading and animation.
- Sort animation frames deterministically.
- Store asset IDs instead of raw paths.
- Return sprite render commands instead of appending to a shared raycast list.

### [object_handler.py](object_handler.py)

- Rename to an entity/world repository or actor registry with a narrow responsibility.
- Move content definitions and spawn tables to data files.
- Sample unique spawn locations and seed randomness.
- Move victory detection to a game-session/system layer.
- Remove dead objects or use lifecycle states and explicit cleanup.

### [npc.py](npc.py)

- Split actor state, NPC decision-making, visibility, movement, animation, and combat.
- Remove direct audio, renderer, and Pygame dependencies.
- Use a shared visibility/raycast service.
- Represent enemy differences as profiles/configuration.
- Add deterministic state-machine tests.

### [pathfinding.py](pathfinding.py)

- Remove stale caching immediately.
- Return a path/result object that can report no route.
- Separate static map graph from dynamic occupancy policy.
- Schedule path requests and add diagonal corner validation.

### [weapon.py](weapon.py)

- Separate weapon gameplay state from shotgun animation and Pygame surfaces.
- Add a combat command or hitscan query.
- Define fire rate, reload duration, range, spread, and damage in data/configuration.

### [sound.py](sound.py)

- Implement an `AudioPort` and a Pygame adapter.
- Load sounds once through an asset/audio manager.
- Support no-audio/headless mode.
- Add explicit stop, pause, volume groups, and shutdown behavior.

### [requirements.txt](requirements.txt)

- Migrate to `pyproject.toml`.
- Pin or constrain release dependencies.
- Add development tools: test runner, linter, formatter, type checker, and profiler.
- Document supported Python and Pygame versions.

## Migration Roadmap

### Milestone 0: Protect the current behavior

- Add a smoke-launch command and asset validation script.
- Add unit tests for map conversion, collision, spawning, and pathfinding.
- Add Ruff, formatting, and type-checking configuration.
- Capture a baseline frame-time profile.
- Record current gameplay behavior with a deterministic random seed.

### Milestone 1: Fix immediate correctness issues

- Correct frame presentation order.
- Remove stale path cache.
- Clamp health and harden HUD rendering.
- Handle raycast denominators and ray misses.
- Sort animation frames.
- Make NPC spawning unique and validated.
- Add graceful audio/display failure paths.

### Milestone 2: Introduce ports and pure domain rules

- Create `GameConfig`, `InputCommand`, `WorldState`, and actor value objects.
- Move movement/collision, health, combat, and win/loss rules out of Pygame classes.
- Add Pygame adapters implementing input, clock, audio, and presentation ports.
- Keep the existing visual output while changing internal ownership.

### Milestone 3: Separate simulation from rendering

- Add a fixed-step simulation loop.
- Build immutable render snapshots after simulation.
- Replace shared `objects_to_render` mutation with typed render commands.
- Add depth-buffer rendering and profile wall/sprite costs.

### Milestone 4: Make content data-driven

- Define a versioned level schema.
- Move entity placements, spawn rules, and enemy profiles out of Python.
- Add asset manifests and CI validation.
- Add a content build step for release bundles.

### Milestone 5: Prepare distribution

- Package the client with stable resource lookup.
- Test Windows and other supported platforms in clean environments.
- Add crash reporting, opt-in telemetry, update channels, and version compatibility.
- Keep all online services behind separate ports and clients.

### Milestone 6: Evaluate the engine boundary

After profiling and content requirements are known, decide whether optimized Pygame remains suitable. Preserve domain/application tests regardless of the graphics backend decision. A backend change should replace adapters and presentation code, not rewrite combat, maps, AI rules, or game state.

## Quality and Operations Baseline

Add these checks to CI:

```text
format check
lint and undefined-name check
type check
unit tests
headless integration tests
asset manifest validation
package/build smoke test
```

Add runtime diagnostics:

- Frame time and simulation time.
- Ray count and visible sprite count.
- NPC count and active path requests.
- Asset cache hit/miss counts.
- Memory usage during repeated round restarts.
- Loading duration and startup failure reason.

Test matrix:

- Supported Python versions.
- Supported operating systems.
- Windowed and fullscreen modes.
- Audio available and unavailable.
- Normal and high-DPI displays.
- Clean install from a packaged build.
- Long-running sessions and repeated victory/game-over loops.

## Summary of Suggested Changes

The current prototype should evolve in this order:

1. Make the current loop correct and robust.
2. Separate domain rules from Pygame and resource APIs.
3. Make simulation deterministic, fixed-step, and independently testable.
4. Replace cross-object mutation with explicit commands, events, systems, and snapshots.
5. Optimize the raycaster, sprite scaling, depth handling, pathfinding schedule, and allocations based on measurements.
6. Move levels, enemy profiles, spawn rules, and assets into validated, versioned content.
7. Package the client reliably and add CI, profiling, crash diagnostics, and asset checks.
8. Add network/platform services as separate scalable systems only when product requirements justify them.

The key architectural decision is to preserve a small, portable game core. Rendering and Pygame should be replaceable infrastructure, not the place where game rules live. That gives the project room to remain a polished retro game, grow its content, or move to a stronger graphics backend without discarding the mechanics that make POV-Blaster itself.
