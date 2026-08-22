# POV-Blaster

POV-Blaster is a Python and Pygame first-person shooter built with a classic raycasting renderer. It is a direct fork of [StanislavPetrovV/DOOM-style-Game](https://github.com/StanislavPetrovV/DOOM-style-Game), based on the same Wolfenstein 3D-inspired approach.

The game uses a 2D grid map to produce a pseudo-3D view. It supports textured walls, animated scenery, mouse-look, WASD movement, a shotgun, enemy line of sight, BFS pathfinding, health, damage, victory, and game-over states.

## Controls

- `W`, `A`, `S`, `D`: move and strafe
- Mouse: look around
- Left mouse button: fire
- `Esc`: quit

## Requirements

- Python 3.10 or newer
- Pygame
- A desktop environment with graphics and audio support

Install the dependency from the project root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

Run the game from the project root so the runtime resource paths resolve correctly:

```powershell
py main.py
```

## Project Structure

```text
main.py              Game startup, event loop, update, and draw lifecycle
settings.py          Display, player, raycasting, and gameplay constants
map.py               Grid map and wall texture IDs
player.py            Player movement, collision, health, and firing
raycasting.py        Wall ray traversal and wall-column projection
object_renderer.py   Background, walls, sprites, HUD, and end screens
sprite_object.py     Static and animated billboard sprites
object_handler.py    Scenery, NPC spawning, updates, and victory checks
npc.py               Enemy behavior, visibility, combat, and animation
pathfinding.py       Grid graph and breadth-first navigation
weapon.py            Shotgun animation and damage
sound.py             Music and sound effects
resources/           Runtime textures, sprites, and audio
screenshots/         Project screenshots
```

## How the Game Works

### Player movement

The player moves through a grid-based world using floating-point coordinates. Wall collision checks prevent movement into solid map cells, and diagonal movement is normalized so moving in two directions is not faster than moving in one direction. Mouse movement updates the camera angle.

### Raycasting

The renderer casts rays across the camera field of view. Each ray finds a horizontal or vertical wall intersection, calculates corrected distance, selects a wall texture, and projects a vertical wall strip onto the screen. The result is a lightweight pseudo-3D environment without a full 3D engine.

### Sprites and animation

Scenery, enemies, and the weapon use transparent 2D images projected into the first-person view. Animation folders contain frame sequences for idle, walk, attack, pain, death, lighting, and weapon recoil states.

### Enemies and pathfinding

Soldier, Cacodemon, and Cyberdemon enemies have different health, speed, attack range, damage, and accuracy settings. Enemies use line-of-sight checks to detect the player and breadth-first search to navigate around walls.

### Combat and game states

The shotgun fires from the center of the screen and applies damage to a visible enemy in the shot path. Player health recovers over time. Defeating all living enemies produces a victory state; health reaching zero produces a game-over state.

## Assets

Runtime assets are stored under `resources/`:

```text
resources/
├── sound/
├── sprites/
│   ├── animated_sprites/
│   ├── npc/
│   ├── static_sprites/
│   └── weapon/
└── textures/
    └── digits/
```

Keep asset paths relative to the project resource root. The asset-loading and packaging strategy is scheduled for improvement as part of the production refactoring plan.

## Development Notes

The current implementation is a compact prototype and is intentionally being evolved toward cleaner architecture. The next improvements should prioritize:

- Correct frame presentation and non-blocking game-state transitions.
- Safe raycasting edge-case handling and a shared traversal implementation.
- Deterministic animation loading and valid, unique NPC spawning.
- Asset caching, stable resource paths, and audio fallback behavior.
- Separation of domain rules from Pygame rendering, input, audio, and filesystem code.
- Unit tests, headless integration tests, profiling, and CI validation.

See the audit and comparison reports before making foundational changes.

## See Also

- [CodeBase.md](docs/CodeBase.md): reconstruction guide and codebase walkthrough
- [CodeAudit.md](docs/CodeAudit.md): architecture, quality, performance, and scalability audit
- [CloneCompare.md](docs/CloneCompare.md): comparison of the related game projects and first-patch recommendations
- [CHANGELOG.md](CHANGELOG.md): project history and prior development prompts

## Project Lineage

POV-Blaster is a direct fork of [StanislavPetrovV/DOOM-style-Game](https://github.com/StanislavPetrovV/DOOM-style-Game). The related [Saurabh-66/DOOM-3D-FPS-Shooting-Game](https://github.com/Saurabh-66/DOOM-3D-FPS-Shooting-Game) project was also compared during planning; see [CloneCompare.md](docs/CloneCompare.md) for the source-similarity evidence and recommended improvements.
