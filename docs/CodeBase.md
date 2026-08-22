# POV-Blaster: Codebase Reconstruction Guide

## 1. What You Are Building

POV-Blaster is a small first-person shooter written in Python with Pygame. It recreates the visual style of early raycasting games such as Wolfenstein 3D and DOOM:

- The map is a 2D grid of cells.
- Walls are stored as integer texture IDs.
- A ray is cast for each vertical screen column to find the nearest wall.
- The wall distance is converted into a projected wall height.
- Enemies and scenery are 2D images projected into the same 3D view.
- The player moves with `WASD`, looks with the mouse, and fires with left click.
- NPCs use line-of-sight checks, simple state logic, and breadth-first pathfinding.
- The player wins when all living NPCs have been defeated.

This document explains the current implementation first, then gives a practical order for recreating it. It is written for a developer who is learning Python and needs enough context to maintain the project.

## 2. Prerequisites

Install:

1. Python 3.10 or newer.
2. Pygame.
3. Git, if you are cloning the repository.
4. A desktop environment with graphics and audio support.

The only declared dependency is in `requirements.txt`:

```text
pygame
```

On Windows, verify that the Python launcher is available:

```powershell
py --version
```

If `py` is unavailable, install Python from python.org and enable **Add Python to PATH**. The bare `python` command on some Windows installations is only a Microsoft Store alias.

Create and activate a virtual environment from the repository root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

Start the game with:

```powershell
py main.py
```

Run this command from the repository root. Runtime assets are selected from a theme directory such as `resources/default/textures/sky.png`; the application resolves paths from the project or executable location.

## 3. Repository Layout

```text
main.py              Application entry point and game loop
settings.py          Screen, movement, raycasting, and player constants
map.py               Grid map and wall lookup table
player.py            Player state, input, movement, health, and shooting
raycasting.py        First-person wall raycasting and wall-column projection
object_renderer.py   Background, walls, sprites, HUD, and end screens
sprite_object.py     Static and animated sprite projection
object_handler.py    Sprite/NPC registration, spawning, updates, and victory
npc.py               Enemy classes, visibility, attacks, damage, and animation
pathfinding.py       Grid graph and breadth-first NPC navigation
weapon.py            Shotgun animation and damage value
sound.py             Music and sound-effect loading
resources/           Textures, sprites, and audio
screenshots/         Project screenshots
```

The modules use wildcard imports for convenience, so many names appear to be available without an explicit import. This keeps the original code short but makes dependencies less obvious. When extending the project, prefer explicit imports in new code.

## 4. Core Design and Object Relationships

`Game` is a service container. Every major object receives the same `game` instance and reaches other systems through it, for example `self.game.player`, `self.game.map`, or `self.game.sound`.

The startup sequence is:

```text
Game.__init__
  -> pygame initialization and window creation
  -> new_game()
       -> Map
       -> Player
       -> ObjectRenderer
       -> RayCasting
       -> ObjectHandler
       -> Weapon
       -> Sound
       -> PathFinding
       -> start music
```

The important dependency order is intentional:

- `Player` must exist before sprites are created because sprites store a player reference.
- `ObjectRenderer` must exist before `RayCasting` because raycasting reads its wall textures.
- `ObjectHandler` must exist before `PathFinding` because pathfinding checks NPC occupancy.
- `Sound` must exist before gameplay can play attack and damage effects.

A new round calls `Game.new_game()` again. This rebuilds the map, player, renderer, enemies, weapon, sound, and pathfinding objects.

## 5. The Frame Loop

`Game.run()` repeats forever:

```text
check_events()
update()
draw()
```

### Input: `Game.check_events`

Pygame events are consumed once per frame. Quit and Escape terminate the process. A custom timer event fires every 40 milliseconds and sets `global_trigger`; animations use this shared pulse. Mouse button events are forwarded to `Player.single_fire_event`.

The mouse is hidden and grabbed by the window. `Player.mouse_control` recenters it when it approaches a border, reads horizontal movement, clamps the relative movement to `MOUSE_MAX_REL`, and changes the player angle.

### Update: `Game.update`

The current update order is:

1. `player.update()` handles movement, mouse look, and health recovery.
2. `raycasting.update()` calculates wall intersections and prepares wall columns.
3. `object_handler.update()` projects scenery, updates NPCs, and checks victory.
4. `weapon.update()` advances the firing animation.
5. The display is flipped and the clock calculates `delta_time`.

`delta_time` is measured in milliseconds. Movement uses it to remain approximately frame-rate independent. `FPS = 0` means Pygame does not cap the frame rate.

### Draw: `Game.draw`

`ObjectRenderer.draw()` draws the sky and floor, then the raycasted walls and projected sprites, then the numeric health HUD. The weapon is drawn last so it stays in front of the world.

The actual `pg.display.flip()` happens in `update()` immediately after drawing has not yet occurred in the current frame. This is a behavior worth correcting when hardening the game: call `draw()`, then `pg.display.flip()`, then tick the clock. The current loop still presents a frame because the previous frame remains on screen, but it introduces a one-frame presentation delay.

## 6. World Representation: `map.py`

`mini_map` is a list of rows. Each cell is either:

- `False` / `0`: walkable empty space.
- `1` through `5`: a solid wall and its texture ID.

`Map.get_map()` converts the grid into `world_map`, a dictionary keyed by `(x, y)` integer coordinates. A wall lookup is therefore simple:

```python
if (x, y) in game.map.world_map:
    texture_id = game.map.world_map[(x, y)]
```

Coordinates use map cells as world units. A position such as `(1.5, 5)` means the center area of a cell, while `map_pos` truncates the floating-point position to its containing cell.

To create a new level, edit the rows in `mini_map`. Keep every row the same width, keep the outside boundary closed, and ensure `PLAYER_POS` is in a walkable cell. Add a texture file and a matching integer ID in `ObjectRenderer.load_wall_textures` when adding a new wall type.

`Map.draw()` is a debugging aid for a top-down view. It is disabled in `Game.draw()`.

## 7. Player: `player.py`

The player owns position, viewing angle, health, and firing state.

### Movement and collision

`movement()` converts the facing angle into forward and sideways vectors using sine and cosine. The keys behave as follows:

- `W`: forward.
- `S`: backward.
- `A`: strafe left.
- `D`: strafe right.

When two movement directions are held, `diag_move_corr = 1 / sqrt(2)` prevents diagonal movement from being faster. `check_wall_collision` tests the proposed x and y movement separately, which lets the player slide along walls instead of stopping completely.

`PLAYER_SPEED` is expressed per millisecond, so the actual movement is `PLAYER_SPEED * delta_time`. `PLAYER_SIZE_SCALE` is used to look ahead for collision; it is a simple point-and-offset collision model rather than a true circular player collider.

### Health and game over

Damage subtracts from health, shows the blood overlay, and plays the pain sound. Health slowly recovers by one point after a 700 ms delay. Health below one triggers the game-over image, waits 1.5 seconds, and starts a new round.

### Shooting

A left mouse click sets `player.shot = True` and starts weapon reloading. The weapon consumes the shot state during its animation. NPCs test whether the shot is centered on their projected sprite; if so, they lose `weapon.damage` health.

## 8. Raycasting: `raycasting.py`

Raycasting is the main 3D technique.

`NUM_RAYS` is half the screen width, and `SCALE` is the width of each rendered vertical wall strip. For every ray:

1. Start at the player position and at the left edge of the field of view.
2. Calculate where the ray first crosses horizontal grid lines.
3. Step through horizontal cells until a wall is found or `MAX_DEPTH` is reached.
4. Repeat for vertical grid lines.
5. Choose the closer horizontal or vertical wall hit.
6. Calculate the texture offset within the hit wall.
7. Correct the distance with `cos(player_angle - ray_angle)` to remove the fishbowl effect.
8. Project the wall height with `SCREEN_DIST / depth`.
9. Store `(depth, projected_height, texture_id, offset)`.

`get_objects_to_render()` turns each ray result into a narrow image by taking a vertical subsection of the selected 256x256 wall texture and scaling it to the projected height. Very close walls are cropped from the texture so they do not scale beyond the screen unnecessarily.

The resulting wall columns are placed into `raycasting.objects_to_render`. Sprites append themselves to this same list, allowing the renderer to depth-sort all world images together.

Important numerical edge cases for production hardening:

- Rays exactly aligned with an axis can make a division by a value near zero.
- A ray that reaches no wall needs a deliberate far-depth behavior.
- Texture subsurface coordinates and scaled dimensions should be clamped to valid integers.

## 9. Rendering: `object_renderer.py`

The renderer loads all image assets once during initialization.

`draw_background()` scrolls a panoramic sky horizontally according to mouse movement and fills the lower half of the screen with `FLOOR_COLOR`. It draws the sky twice so horizontal scrolling wraps cleanly.

`render_game_objects()` sorts the shared render list by normalized depth in reverse order. Far objects are drawn first and near objects later, giving the painter's-algorithm depth effect used by this small engine.

The HUD draws the player's health using digit images. The image named `10.png` is used as a health icon/suffix. End-state images are full-screen overlays:

- `win()` draws `win.png`.
- `game_over()` draws `game_over.png`.
- `player_damage()` draws `blood_screen.png`.

All asset paths are currently relative to the process working directory. A production version should build paths from `__file__` so the game works regardless of where it is launched.

## 10. Sprites and Animation: `sprite_object.py`

`SpriteObject` is the base class for scenery and other billboard images. It:

1. Calculates the vector from the player to the sprite.
2. Converts that vector to an angle and distance.
3. Converts the angle to a screen x coordinate.
4. Uses normalized distance to avoid perspective distortion.
5. Scales the original image according to distance and `SPRITE_SCALE`.
6. Appends the projected image and position to the raycasting render list.

Sprites are only projected when they are inside or near the screen and farther than 0.5 world units from the player.

`AnimatedSprite` loads every file in the directory containing the initial image into a `deque`. On each animation interval, it rotates the deque and displays the next frame. This is why animation folders contain numbered frames such as `0.png`, `1.png`, and so on.

The filesystem order returned by `os.listdir` is not guaranteed. For reliable animation, sort frame filenames numerically before loading them. Also use `os.path.join` or `pathlib.Path` consistently instead of mixing slash styles.

## 11. Object Management and NPC Spawning: `object_handler.py`

`ObjectHandler` owns two collections:

- `sprite_list`: scenery and animated lights.
- `npc_list`: enemies.

The default game spawns 20 random enemies selected with weighted probabilities:

- Soldier: 70%.
- Cacodemon: 20%.
- Cyberdemon: 10%.

Spawn cells cannot be walls or cells in `restricted_area`, which protects the player's starting region. NPCs are placed at the center of their selected cell.

The handler also registers the fixed scenery map. To add an object, instantiate `AnimatedSprite` or a subclass with a valid image path, position, scale, and vertical shift, then call `add_sprite`.

Each frame, the handler first creates `npc_positions` from living enemies. NPCs use this set to avoid moving into each other's cells. It then updates all scenery, updates all NPCs, and checks whether no living NPCs remain. Victory displays the win image, waits, and starts a new round.

Current risks to understand:

- Random spawning may place multiple enemies in the same cell.
- A pathfinding cache can retain a path even after NPC occupancy changes.
- The spawn loop assumes at least 20 valid cells exist outside the restricted area.
- Dead NPC objects remain in `npc_list`, although they are excluded from occupancy and victory checks.

## 12. NPC Behavior: `npc.py`

`NPC` extends `AnimatedSprite`, so an enemy is both a projected sprite and a stateful actor. It loads attack, death, idle, pain, and walk frame directories from the enemy's asset folder.

Each enemy has configurable:

- `attack_dist`: range at which it attacks.
- `speed`: movement speed per update.
- `health`.
- `attack_damage`.
- `accuracy`: probability an attack damages the player.

`run_logic()` is the state machine:

```text
alive?
  no  -> animate death
  yes -> can see player?
          yes and recently hit -> animate pain
          yes and within attack range -> attack animation and attack
          yes and outside attack range -> walk animation and move
          no but previously detected player -> walk and move toward player
          no and never detected -> idle animation
```

`ray_cast_player_npc()` casts from the player toward the NPC and checks whether the NPC is encountered before a wall. This gives the enemy line of sight. The enemy only begins pursuit after it has seen the player, but it continues pursuing after line of sight is lost.

`check_hit_in_npc()` treats a shot as a hit when the NPC's projected horizontal bounds contain the screen center. This is a simple hitscan implementation. It clears the shot flag after a hit, plays pain audio, sets the pain state, and subtracts weapon damage.

The three subclasses only change tuning values and default asset paths:

- `SoldierNPC`: balanced default enemy.
- `CacoDemonNPC`: close-range, tougher, faster, and more accurate.
- `CyberDemonNPC`: high-health enemy with long attack range.

## 13. Pathfinding: `pathfinding.py`

At startup, `PathFinding.get_graph()` creates a graph node for every walkable map cell. Each node can connect to eight neighboring cells, including diagonals, as long as the neighbor is not a wall.

`get_path(start, goal)` runs breadth-first search and reconstructs the first step toward the goal. NPC movement asks for that first step, calculates an angle to the center of the target cell, and moves toward it unless another NPC currently occupies the cell.

The graph is static, but NPC occupancy is dynamic. The `@lru_cache` decorator only keys on `start` and `goal`, not on the current NPC positions. This is acceptable for a prototype but can produce stale decisions. Remove the cache, clear it after occupancy changes, or include a stable occupancy version in the cache key when improving the AI.

Diagonal paths can also pass around corners in ways that a strict grid game may not want. Prevent diagonal movement when both adjacent cardinal cells are walls if corner cutting becomes a gameplay problem.

## 14. Weapon and Audio

`Weapon` extends `AnimatedSprite` but places the shotgun at the bottom center of the screen. It loads the shotgun frames, scales them by `0.4`, and rotates the frame deque while `reloading` is true.

The fire flow is:

```text
left click
  -> Player.shot = True
  -> Weapon.reloading = True
  -> shotgun sound plays
  -> weapon animation advances
  -> NPC projected at screen center consumes the shot
  -> final weapon frame clears reloading
```

`Weapon.damage` is currently 50.

`Sound` initializes the mixer, loads five sound effects, loads `theme.mp3` as music, and sets volumes. `Game.new_game()` starts the music in a loop. On machines without an audio device, mixer initialization may fail; a production build should either configure a fallback audio driver or handle audio initialization failure gracefully.

## 15. Settings to Understand First

`settings.py` contains the tuning surface:

- `RES`: window resolution, currently 1600x900.
- `FPS`: frame cap, currently unlimited (`0`).
- `PLAYER_SPEED` and `PLAYER_ROT_SPEED`: movement/turn rates.
- `MOUSE_SENSITIVITY`: mouse look sensitivity.
- `FOV`: field of view, currently 60 degrees.
- `NUM_RAYS`: horizontal ray count.
- `MAX_DEPTH`: maximum grid cells each ray checks.
- `SCREEN_DIST`: projection-plane distance derived from FOV.
- `TEXTURE_SIZE`: expected wall texture size.

Changing resolution affects `WIDTH`, `HEIGHT`, ray count, wall-strip scale, HUD layout, weapon placement, and mouse borders. Test these together rather than changing only one value.

## 16. Recommended Recreation Order

Follow this order when rebuilding the project from an empty directory:

1. Create a virtual environment and install Pygame.
2. Create `settings.py` with resolution, player, FOV, ray, texture, and color constants.
3. Create `map.py` with a small closed grid and a `Map` class that builds `world_map`.
4. Create `main.py` with Pygame startup, a `Game` object, and a temporary colored-screen loop.
5. Add `player.py` with position, keyboard movement, angle, and grid collision.
6. Add `object_renderer.py` to load wall textures and draw the sky/floor.
7. Add `raycasting.py` and implement horizontal and vertical grid intersection checks.
8. Render wall strips from ray results and confirm the map appears in first person.
9. Add `sprite_object.py` and project one scenery image into the shared render list.
10. Add `object_handler.py` and register scenery objects.
11. Add `weapon.py` and connect mouse firing to a frame animation.
12. Add `sound.py` and verify audio separately from rendering.
13. Add `npc.py` with one enemy, visibility checks, attacks, health, and death animation.
14. Add `pathfinding.py`, then connect NPC movement to the first BFS step.
15. Add random spawning and enemy subclasses.
16. Add health, damage overlay, win screen, and game-over restart behavior.
17. Replace temporary debug drawing with the intended renderer calls.
18. Add tests and hardening before adding new gameplay features.

At every stage, keep the game launchable. A useful milestone is a static first-person wall view before adding enemies; another is one manually placed enemy before adding random spawning.

## 17. Assets Contract

The code expects these groups of files:

```text
resources/default/textures/1.png ... 5.png
resources/default/textures/sky.png
resources/default/textures/blood_screen.png
resources/default/textures/game_over.png
resources/default/textures/win.png
resources/default/textures/digits/0.png ... 10.png
resources/default/sound/shotgun.wav
resources/default/sound/npc_pain.wav
resources/default/sound/npc_death.wav
resources/default/sound/npc_attack.wav
resources/default/sound/player_pain.wav
resources/default/sound/theme.mp3
resources/default/sprites/weapon/shotgun/0.png ...
resources/default/sprites/npc/<type>/<animation>/*.png
resources/default/sprites/animated_sprites/<object>/*.png
resources/default/sprites/static_sprites/candlebra.png
```

The asset loader calls `convert_alpha()`, so display mode must be initialized before images are loaded. This is why image loading occurs after `pg.display.set_mode` in `Game.__init__`.

When adding art:

- Keep animation frames in one directory.
- Keep frame dimensions consistent.
- Use transparent PNGs for sprites.
- Update the constructor path if the folder name changes.
- Test missing or malformed files with a clear startup error.

## 18. Production Hardening Checklist

Before treating this as production-quality software, address these items:

- Use explicit imports instead of wildcard imports.
- Resolve resource paths relative to the project or executable location.
- Move `display.flip()` into the draw phase and tick the clock after presentation.
- Add a finite FPS cap or document why unlimited FPS is intentional.
- Sort animation filenames deterministically.
- Guard raycasting divisions near zero and handle rays with no wall hit.
- Clamp health to a valid range and make HUD rendering robust for zero or negative values.
- Prevent duplicate NPC spawn cells and validate that enough spawn cells exist.
- Invalidate or redesign cached paths when NPC occupancy changes.
- Handle mixer/display initialization failures with useful error messages.
- Separate game state transitions from blocking `time.delay` calls.
- Add automated tests for map conversion, collision, graph construction, pathfinding, spawn validity, and player damage.
- Add a headless or dependency-injected test mode for CI.
- Log asset-loading failures with the exact path and expected format.
- Replace magic numbers such as `100` in debug map drawing with a named tile-size constant.
- Package the game with a reliable resource strategy if distributing an executable.

## 19. Suggested Tests for a Junior Developer

Start with pure logic tests that do not open a window:

- A wall cell appears in `world_map`; an empty cell does not.
- Player movement into a wall does not change the blocked coordinate.
- Diagonal movement is normalized.
- The pathfinder returns a walkable first step.
- The pathfinder does not route through wall cells.
- NPC damage reduces health and marks an enemy dead when health reaches zero.
- Spawned NPCs are not in wall cells or the restricted area.

Then add integration checks:

- The game starts from the repository root with all assets present.
- The first-person view contains wall columns.
- Mouse movement changes the view angle.
- Left click starts the shotgun animation.
- Killing every NPC displays the win screen.
- Reducing player health below one displays the game-over screen and resets the round.

## 20. Takeover Workflow

When changing the game, use this sequence:

1. Identify which system owns the behavior.
2. Find the state that controls it and the update method that mutates it.
3. Make the smallest change in that owning module.
4. Run a syntax/import check and a focused test.
5. Launch from the repository root and manually verify the affected interaction.
6. Check that asset paths, frame timing, and restart behavior still work.
7. Only then refactor shared code or tune unrelated systems.

For example, a new weapon should primarily change `weapon.py`, `player.py` for input/state, `sound.py` for audio, and `object_handler.py` or `npc.py` for hit effects. A new wall type should primarily change `map.py`, `object_renderer.py`, and the resource directory.

The central mental model is simple: the map supplies geometry, raycasting converts geometry into wall columns, sprites add projected objects to the same render queue, NPCs mutate gameplay state during updates, and the renderer presents the resulting frame. Once that flow is understood, the rest of the project is tuning and content.
