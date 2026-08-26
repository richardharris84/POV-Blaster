# POV-Blaster

POV-Blaster is a Python and Pygame first-person shooter built with a classic raycasting renderer. It is a direct fork of [StanislavPetrovV/DOOM-style-Game](https://github.com/StanislavPetrovV/DOOM-style-Game), based on the same Wolfenstein 3D-inspired approach.

The game uses a 2D grid map to produce a pseudo-3D view. It supports textured walls, animated scenery, mouse-look, WASD movement, a shotgun, enemy line of sight, BFS pathfinding, health, damage, victory, and game-over states.

## Controls

- `W`, `A`, `S`, `D`: move
- Mouse: look around
- Left click: fire
- Mobile: left joystick moves, right joystick looks, and tapping the right joystick fires
- `Caps Lock`: toggle the mini-map in the top-left during gameplay
- `Esc`: exit to the startup menu

<p align="center">
  <a href="https://richardharris84.github.io/POV-Blaster/">
    <span style="display:inline-block; width:208px; height:45px; box-sizing:border-box; background:#ffffff; color:#000000; border:3px solid #000000; border-radius:12px; font-family:'Arial Black','Trebuchet MS',sans-serif; font-size:25px; font-weight:900; letter-spacing:0.14em; line-height:39px; text-align:center; text-decoration:none;">PLAY</span>
  </a>
</p>

<div style="height:24px;"></div>

![POV-Blaster gameplay](screenshots/gameplay_1.gif)

## Table of Contents

- [Additional Documentation](#additional-documentation)
- [Controls](#controls)
- [Requirements](#requirements)
- [Running the Script](#running-the-script)
- [Build Executables](#build-executables)
  - [Windows build](#windows-build)
  - [Linux build](#linux-build)
  - [macOS build](#macos-build)
  - [Browser build](#browser-build)
  - [Deploying to GitHub Pages](#deploying-to-github-pages)
  - [GitHub Actions](#github-actions)
- [Hosted API and Database](#hosted-api-and-database)
- [Deployment Settings](#deployment-settings)
- [Development History](#development-history)
- [Project Structure](#project-structure)
- [How the Game Works](#how-the-game-works)
- [Development Walkthrough](#development-walkthrough)
- [Assets](#assets)
- [Development Notes](#development-notes)
- [Project Lineage](#project-lineage)

## Additional Documentation

- [ArchDiagrams.md](docs/ArchDiagrams.md): Mermaid architecture, runtime, API, and deployment diagrams
- [CHANGELOG.md](CHANGELOG.md): project history and prior development prompts
- [CodeAudit.md](docs/CodeAudit.md): architecture, quality, performance, and scalability audit
- [CodeBase.md](docs/CodeBase.md): up-to-date reconstruction guide and codebase walkthrough (the original, now superseded, walkthrough is archived at [docs/archive/CodeBase-Orig.md](docs/archive/CodeBase-Orig.md))
- [GraphicsRollback.md](docs/GraphicsRollback.md): graphics rollback and asset history
- [docs/archive/CodeBase-Orig.md](docs/archive/CodeBase-Orig.md): archived pre-refactor codebase walkthrough
- [docs/archive/Recommendations.md](docs/archive/Recommendations.md): archived architecture recommendations
- [docs/archive/CloneCompare.md](docs/archive/CloneCompare.md): comparison of the related game projects and first-patch recommendations
- [docs/archive/POCFeatures.md](docs/archive/POCFeatures.md): archived proof-of-concept feature record

## Hosted API and Database

The desktop build keeps a local SQLite leaderboard at `data/scores.sqlite3`. The browser build uses localStorage for immediate offline play and submits scores in the background to the optional FastAPI service. The browser also records a web session when a player starts a game.

The FastAPI application in `api/main.py` exposes:

- `GET /health`: Render health check.
- `GET /scores`: public scores ordered by kills.
- `POST /scores`: validates and stores a player name and kill count.
- `GET /sessions`: lists recorded web sessions.
- `POST /sessions`: records a player name, request IP, UTC timestamp, and best-effort city/country lookup.

Production uses [Neon Postgres](https://console.neon.tech/) through the `DATABASE_URL` environment variable. The API creates the `scores` and `web_sessions` tables on startup and uses Psycopg for Postgres connections. Raw IP addresses are not stored with score records; session records retain the request IP for session analytics. Local development and tests use SQLite automatically when `DATABASE_URL` is absent. `HighScores.sync(api_url, direction='push')` uploads the local SQLite leaderboard to the API, while `direction='pull'` replaces the local leaderboard with the remote scores. The browser name-entry screen links to [privacy.html](privacy.html), which explains the location data use and deletion request process.

[Render](https://dashboard.render.com/) hosts the `pov-blaster-api` Free web service. Its [api/render.yaml](api/render.yaml) Blueprint uses `requirements-api.txt`, which deliberately excludes Pygame and other desktop/web build dependencies, and starts the service with Uvicorn.

<div align="right"><a href="#table-of-contents">^ TOC</a></div>

## Requirements

- Python 3.10 or newer
- Pygame — required to run the game
- PyInstaller — only needed to build the Windows/Linux/macOS executables
- Pygbag — only needed to build/serve the browser version
- imageio-ffmpeg — only needed by `build.py --web`; bundles a portable `ffmpeg` binary used to transcode sound assets to OGG for the browser build
- Pillow, opencv-python, and scikit-image — used by the theme asset audit and Pixel-Harmony-compatible image comparisons
- A desktop environment with graphics and audio support (for the desktop build)

## Running the Script

Run these commands from the project root so the runtime resource paths resolve correctly.

### Windows

Create and activate a virtual environment, install the dependencies, and run the script:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
py main.py
```

The game opens as a Windows desktop window. Press `Esc` to quit.

### Linux

Create and activate a virtual environment, install the dependencies, and run the script:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
python3 main.py
```

On WSL, the game needs a GUI provider. WSLg is supported automatically. If using VcXsrv, start VcXsrv with X11 access enabled, then run:

```bash
./build/POV-Blaster_lin
```

The Linux executable automatically detects a reachable VcXsrv display when running under WSL. If necessary, set `DISPLAY` manually to the Windows host display, for example `DISPLAY=172.19.64.1:0`.

<div align="right"><a href="#table-of-contents">^ TOC</a></div>

## Build Executables

PyInstaller creates a native executable for the operating system where the build runs. Build Windows on Windows and Linux on Linux or WSL. Install the dependencies first using the instructions in [Running the Script](#running-the-script).

### Windows build

```powershell
py build.py -w
```

This creates:

```text
build/POV-Blaster_win.exe
```

### Linux build

Run on Linux or inside WSL:

```bash
./build.py -l
```

Or from PowerShell, invoking WSL with the Windows project path explicitly mounted:

```powershell
wsl bash -lc "cd /mnt/c/Users/Richard/Dropbox/Workspace/Code/Python/POV-Blaster && ./build.py -l"
```

This creates:

```text
build/POV-Blaster_lin
```

### macOS build

Run on macOS with Python, Pygame, and PyInstaller installed:

```bash
python3 build.py -m
```

This creates:

```text
build/POV-Blaster_mac.app
```

Open the application bundle from Finder or run it with:

```bash
open build/POV-Blaster_mac.app
```

### Browser build

Install the dependencies, then run the Pygbag target from the project root:

```bash
py build.py -b
# or: py build.py --web
```

This creates the browser build under `build/web`.

### Deploy to GitHub Pages

Use the build script to publish the browser artifact directly to the `gh-pages` branch for GitHub Pages:

```bash
py build.py -d
```

This deploys the pre-built `build/web` output to GitHub Pages. If you want the script to build the browser bundle first and then deploy it in one step, use:

```bash
py build.py -bd
# or: py build.py --web --deploy
```

The `-bd` flow is the one-step browser build + deploy command. The `-d` flow assumes `build/web` already exists and only publishes it.

To run it locally, start Pygbag's runtime-aware server against the staged web source:

```bash
py -m pygbag build/web-source
```

Then open `http://localhost:8000`. Pygbag's server provides the required `/cdn/` runtime route; a plain HTTP server is not sufficient. The web entry point uses an asynchronous game loop and <u>browser-local storage for high scores</u>. Desktop builds continue to use `data/scores.xml`. Pygbag's runtime may require a user click to unlock browser media before starting.

The Pygbag dev server re-packages the app fresh each time it starts, but not while running — so after any `py build.py --web` rebuild, you must stop and restart the dev server (Ctrl+C, then run `py -m pygbag build/web-source` again) for changes to actually take effect.

The `build.py` script rejects builds requested from the wrong operating system, preventing incorrectly named non-native executables. macOS builds must run on macOS because PyInstaller creates native artifacts for the host platform.

#### Deploying to GitHub Pages

`.github/workflows/deploy-pages.yml` builds the web target and publishes `build/web` to GitHub Pages automatically on every push to `main`. To enable it:

1. Go to [Settings → Pages](https://github.com/richardharris84/POV-Blaster/settings/pages) and set **Source** to **GitHub Actions**.
2. Push to `main` (or run the workflow manually from the [Actions](https://github.com/richardharris84/POV-Blaster/actions) tab).
3. Once the workflow finishes, the game is served at **https://richardharris84.github.io/POV-Blaster/**.

#### GitHub Actions

The repository has three GitHub Actions workflows:

- `.github/workflows/ci.yml` runs on every push and pull request. It uses `actions/checkout@v4` and `actions/setup-python@v5` on Windows, installs `requirements.txt`, compiles Python modules, runs the full test suite, validates theme assets, and audits theme images. On successful pushes to `main`, it uses `dawidd6/action-send-mail@v3` for an optional CI email.
- `.github/workflows/deploy-pages.yml` runs on every push to `main` or manually. It uses `actions/checkout@v4`, `actions/setup-python@v5`, `actions/upload-pages-artifact@v3`, and `actions/deploy-pages@v4` to build and publish `build/web` to the `github-pages` environment. It reads the `POV_BLASTER_API_URL` repository variable during the build and optionally sends a completion email.
- `.github/workflows/deploy-render.yml` runs when API/deployment files change on `main` or manually. If configured, it calls the Render deploy hook with `curl`; without the hook it reports setup instructions and does not trigger a deployment. It can optionally send a deployment email.

### GitHub Actions settings

In repository **Settings → Pages**, set **Source** to **GitHub Actions**. In **Settings → Secrets and variables → Actions → Variables**, add:

```text
POV_BLASTER_API_URL=https://pov-blaster-api.onrender.com
```

The value must be the Render service URL without a trailing slash. Do not put the Neon connection string in GitHub because it is only needed by Render.

Optional email notifications use these repository **Actions secrets**: `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USERNAME`, and `SMTP_PASSWORD`. The Render workflow also accepts the optional `RENDER_DEPLOY_HOOK` secret.

## Deployment Settings

### Render

Create the web service from the repository Blueprint using [api/render.yaml](api/render.yaml), branch `main`, and the Free plan. Set `DATABASE_URL` in the Render service environment to the Neon connection string, including `sslmode=require`. Keep the value secret. The Blueprint sets `CORS_ORIGINS` to `https://richardharris84.github.io`; this is the origin only and intentionally does not include `/POV-Blaster/`.

The Render build command is `pip install -r requirements-api.txt`, and the start command is `uvicorn api.main:app --host 0.0.0.0 --port $PORT`. Verify the deployment at `https://pov-blaster-api.onrender.com/health`. Render Free services can sleep after inactivity, so the first request may be delayed.

### Neon

Create a free Neon Postgres project and copy its pooled or direct connection string into Render's `DATABASE_URL` environment variable. Neon Auth is not required. Never commit the connection string to the repository or expose it in logs.

### GitHub Pages

After `POV_BLASTER_API_URL` is configured, run **Actions → Deploy web build to GitHub Pages → Run workflow** on `main`. The published game URL is `https://richardharris84.github.io/POV-Blaster/`.

<div align="right"><a href="#table-of-contents">^ TOC</a></div>

<div align="right"><a href="#table-of-contents">^ TOC</a></div>

## Project Structure

```text
main.py                Desktop/CLI entry point (theme + name prompt, then Game.run())
build.py               Multi-target build script: Windows/Linux/macOS executables + browser build
api/                   FastAPI service for health, scores, and web-session endpoints
src/ (Standard Choice) Primary Python code parent folder. `src` is a universal standard across Python and general software development, so anyone opening the repository immediately knows where the runnable Python code lives.
src/application/       Game actors, gameplay systems, startup flow, and orchestration
src/domain/            Pure game-rule logic with no Pygame/IO dependency
src/infrastructure/    Filesystem, audio, input, settings, scores, and platform adapters
src/presentation/      Pygame-facing rendering, input, touch, and web menu adapters
assets/themes/<theme>/ Per-theme textures, sprites, and sound (default/candy_kingdom/graveyard/hunting/space)
assets/maps/           Plain-text maps ('.' = empty, digit = wall texture id)
assets/levels/         Data-driven scenery placement and NPC spawn tables, keyed by map name
data/                  Mutable local runtime data, including ignored scores.sqlite3
tests/                 unittest suite (domain, map, audio, scores, NPC systems, assets, web patches, API, integration)
tools/audit_themes.py  Required asset, image quality, clipping, and animation audit implementation
tools/generate_themes.ps1  Procedural theme and animation asset generator/validator
tools/pixel_harmony_compare.py  Pixel-Harmony-compatible image comparison metrics
tools/profile_game.py  Headless cProfile harness for update()/draw()
docs/                  Design/audit/reconstruction documentation
.github/workflows/     CI, GitHub Pages, and Render deployment workflows
requirements-api.txt   API-only dependencies used by Render
api/render.yaml        Render Free web-service and Neon DATABASE_URL configuration
build/                 Build outputs (gitignored): platform executables and the web bundle
logs/                  Local generated logs (gitignored)
screenshots/           Project screenshots
```

See [docs/CodeBase.md](docs/CodeBase.md) for a full walkthrough of how these pieces fit together.

<div align="right"><a href="#table-of-contents">^ TOC</a></div>

## How the Game Works

### Player movement

The player moves through a grid-based world using floating-point coordinates. Wall collision checks prevent movement into solid map cells, and diagonal movement is normalized so moving in two directions is not faster than moving in one direction. Mouse movement updates the camera angle.

### Raycasting

The renderer casts rays across the camera field of view. Each ray finds a horizontal or vertical wall intersection, calculates corrected distance, selects a wall texture, and projects a vertical wall strip onto the screen. The result is a lightweight pseudo-3D environment without a full 3D engine.

### Sprites and animation

Scenery, enemies, and the weapon use transparent 2D images projected into the first-person view. Animation folders contain frame sequences for idle, walk, attack, pain, death, lighting, and weapon recoil states.

### Enemies and pathfinding

Soldier, Cacodemon, and Cyberdemon enemies have different health, speed, attack range, damage, and accuracy settings. Enemies use line-of-sight checks to detect the player and breadth-first search to navigate around walls.

### Themes

The startup menu provides five content choices:

- Candy Kingdom: Marshmallow Man, Springfield Doughnut, Gingerbread Golem
- Space: Alien Drone, Alien Warrior, Alien Overlord
- Hunting: Hunter, Deer, Bear
- Graveyard: Ghost, Vampire, Werewolf
- Doom: Soldier, Caco Demon, Cyber Demon

Theme assets live under `assets/themes/<theme>/`. To regenerate the themed textures and NPC animation frames on Windows, run:

```powershell
.\tools\generate_themes.ps1
```

To validate existing animation folders without changing artwork, run:

```powershell
.\tools\generate_themes.ps1 -ValidateOnly
```

To explicitly generate replacements for missing or duplicate numbered frames, add `-RepairFrames`.

For a complete deterministic regeneration of every non-default PNG asset, use the
production pixel renderer:

```powershell
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" tools\generate_pixel_assets.py
& "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe" tools\audit_themes.py --check
```

The installed Pixel Agents, OpenGame, Unity, Hootbu Pixel Agent, and Copilot Pixel
Agents extensions were verified locally. They provide interactive authoring panels
or development integration, not a documented batch PNG export API. Pixel-Harmony
is used as a visual comparison reference; the local renderer is retained as the
reproducible release-generation path rather than claiming unavailable automated AI
asset output.

Each generated NPC includes unique idle, walk, attack, pain, and death sequences. Candy Kingdom uses the imported CandyKingdom asset set, including the pastry-bag weapon and thick slime firing sound; its deaths melt the Marshmallow Man and crumble the Springfield Doughnut and Gingerbread Golem.

### Combat and game states

The shotgun fires from the center of the screen and applies damage to a visible enemy in the shot path. Player health recovers over time. Defeating all living enemies produces a victory state; health reaching zero produces a game-over state.

<div align="right"><a href="#table-of-contents">^ TOC</a></div>

## Development Walkthrough

The following stages describe how POV-Blaster grows from a 2D map into a playable raycast shooter. The demonstrations are included for visual reference and represent the current project style and feature set.

### Player Movement

The player moves forward, backward, and sideways relative to the current viewing angle. Wall collision checks keep the player inside walkable cells, while diagonal movement correction keeps combined WASD input from increasing movement speed. Mouse-look changes the viewing angle and recenters the cursor when it approaches the configured screen border.

![Player movement demonstration](screenshots/player_1.gif)

### Raycasting Algorithm

The camera field of view is the interval from the player angle minus half the FOV to the player angle plus half the FOV. POV-Blaster casts one ray for each configured screen column across that interval. Each ray stops at the first wall cell, providing the depth used to calculate the height of its projected vertical wall strip.

![Raycasting grid traversal](screenshots/raycast_1.gif)

![Raycast projection](screenshots/raycast_2.gif)

Distance correction removes the fishbowl effect that would otherwise make walls at the sides of the view appear distorted. Distance-based shading is a future rendering opportunity; the current renderer uses textured walls, a sky background, and a floor color.

![Raycast scene shading reference](screenshots/raycast_3.gif)

![Textured raycast environment](screenshots/raycast_4.gif)

### Static and Animated Sprites

Scenery is added as transparent 2D billboard images positioned in the map. Animated sprites are sequences of images displayed over time. This supports environmental details such as lights and decorations without requiring a full polygonal 3D engine.

<img src="screenshots/assets_1.png" alt="Static sprite reference" width="126">

<img src="screenshots/assets_2.gif" alt="Animated sprite reference" width="126">

<img src="screenshots/assets_3.gif" alt="Additional animated sprite reference" width="126">

![Decorated game environment](screenshots/gameplay_2.gif)

### Weapon and Shooting Animation

The shotgun is a foreground sprite animated from a sequence of recoil frames. Left-click starts the firing sound and animation, and the reload lockout prevents another shot until the animation completes. The current weapon uses a center-screen hitscan interaction with visible enemies.

![Shotgun firing animation](screenshots/weapon_1.gif)

### Player-Enemy Interaction and Pathfinding

Enemies first use line of sight to detect the player. A direct movement approach would fail when a wall blocks the straight-line route, so POV-Blaster uses breadth-first search over walkable map cells to find a route around obstacles. NPC occupancy is considered when enemies select their next cell.

![Direct enemy pursuit reference](screenshots/player_enemy_1.gif)

![BFS pathfinding reference](screenshots/player_enemy_2.gif)

![Multiple-enemy pursuit reference](screenshots/player_enemy_3.gif)

The current implementation is intentionally simple. Future improvements should schedule pathfinding work, avoid stale cache results, prevent diagonal corner cutting, and separate navigation rules from NPC rendering and combat.

### Enemies

POV-Blaster includes three enemy profiles. Each profile uses idle, walk, attack, pain, and death animations and has its own health, speed, attack range, damage, and accuracy values.

#### Soldier

![Soldier idle and combat reference](screenshots/soldier_1.gif)

![Soldier movement reference](screenshots/soldier_2.gif)

![Soldier attack reference](screenshots/soldier_3.gif)

#### Cacodemon

![Cacodemon idle and combat reference](screenshots/cacodemon_1.gif)

![Cacodemon movement reference](screenshots/cacodemon_2.gif)

![Cacodemon attack reference](screenshots/cacodemon_3.gif)

#### Cyberdemon

![Cyberdemon idle and combat reference](screenshots/cyberdemon_1.gif)

![Cyberdemon movement reference](screenshots/cyberdemon_2.gif)

![Cyberdemon attack reference](screenshots/cyberdemon_3.gif)

### Final Gameplay

The complete gameplay loop combines movement, mouse-look, raycast rendering, textured walls, animated scenery, enemy detection and navigation, shotgun combat, health and damage feedback, sound effects, and victory/game-over transitions.

![POV-Blaster final gameplay](screenshots/gameplay_1.gif)

<div align="right"><a href="#table-of-contents">^ TOC</a></div>

## Assets

Runtime assets are stored under `assets/`:

```text
assets/
├── default/
├── candy_kingdom/
├── graveyard/
├── hunting/
├── space/
├── maps/
└── levels/
```

Keep asset paths relative to the project asset root. Mutable runtime data belongs in `data/`, not under `assets/`.

<div align="right"><a href="#table-of-contents">^ TOC</a></div>

## Development Notes

The current implementation is a compact prototype and is intentionally being evolved toward cleaner architecture. The next improvements should prioritize:

- Correct frame presentation and non-blocking game-state transitions.
- Safe raycasting edge-case handling and a shared traversal implementation.
- Deterministic animation loading and valid, unique NPC spawning.
- Asset caching, stable resource paths, and audio fallback behavior.
- Separation of domain rules from Pygame rendering, input, audio, and filesystem code.
- Unit tests, headless integration tests, profiling, and CI validation.

See the audit and comparison reports before making foundational changes.

<div align="right"><a href="#table-of-contents">^ TOC</a></div>

<div align="right"><a href="#table-of-contents">^ TOC</a></div>

## Project Lineage

POV-Blaster is a direct fork of [StanislavPetrovV/DOOM-style-Game](https://github.com/StanislavPetrovV/DOOM-style-Game). The related [Saurabh-66/DOOM-3D-FPS-Shooting-Game](https://github.com/Saurabh-66/DOOM-3D-FPS-Shooting-Game) project was also compared during planning. The archived [docs/archive/CloneCompare.md](docs/archive/CloneCompare.md) records the source-similarity evidence, while [docs/archive/CodeBase-Orig.md](docs/archive/CodeBase-Orig.md) preserves the original flat-module architecture and runtime assumptions.

### Similarity Analysis

**POV-Blaster vs. `DOOM-style-Game` — ~35–40% similar**

POV-Blaster started as a literal fork, so the *conceptual lineage* of the core engine is still clearly traceable: the DDA raycasting math in `src/application/raycasting.py`, the sprite-projection formula in `src/application/sprite_object.py`, the NPC line-of-sight check in `src/application/npc.py`, and the BFS pathfinding in `src/application/pathfinding.py` are essentially unchanged algorithms. But almost nothing is byte-identical anymore, because POV-Blaster has since:

- Split the original ~12 flat modules into a layered `src/application/` / `src/domain/` / `src/infrastructure/` / `src/presentation/` architecture (health, combat, movement, and game-state logic extracted into pure, dependency-free `src/domain/` classes).
- Added a 5-theme system (Doom/Candy Kingdom/Space/Graveyard/Hunting) that swaps enemies, art, weapon, and sound per theme — the original has exactly one fixed asset set.
- Added an entire second platform target: a browser build (Pygbag/WASM), with its own audio backend (`BrowserSound`), high-score backend (`BrowserHighScores`), and HTML/CSS patching pipeline — none of this exists upstream.
- Added a `tests/` suite, CI, GitHub Pages deployment, plain-text map files (vs. a hardcoded grid), multi-platform PyInstaller builds, and reproducible theme asset tooling.
- Added `tools/audit_themes.py`, which compares every theme with the Default baseline and checks required assets, dimensions, blank images, clipping, animation folders, and duplicate frames. Pixel-Harmony-compatible comparison metrics are available through `tools/pixel_harmony_compare.py`.
- Added theme-specific NPC animation and audio behavior, including Candy Kingdom melt/crumble deaths, Hunting Bear roar/spit attacks, and custom Hunting forest-cabin artwork. These are project-owned adaptations rather than replacements with unverified third-party assets.

The current POV-Blaster workspace is substantially larger than the original because it includes layered application code, five theme resource trees, browser packaging, automated tests, CI, and asset QA. The majority of that growth is net-new platform, content, and validation work rather than changes to the original raycasting algorithm.

**POV-Blaster vs. `DOOM-3D-FPS-Shooting-Game` — ~30–35% similar**

Slightly lower than above. Per `CloneCompare.md`, `DOOM-3D-FPS-Shooting-Game` is itself an almost-unmodified copy of `DOOM-style-Game`, with a handful of small intentional deviations — it *removed* the diagonal-movement correction and mouse-grab call that `DOOM-style-Game` has. POV-Blaster explicitly *kept* the diagonal correction (now `src/domain/movement.py`'s `movement_delta()`) and kept mouse-grab handling (now with an X11/browser-aware branch), so on those specific points POV-Blaster tracks closer to `DOOM-style-Game` than to `DOOM-3D-FPS-Shooting-Game`'s variant — pushing its similarity to the latter slightly lower.

**`DOOM-style-Game` vs. `DOOM-3D-FPS-Shooting-Game` — ~95–98% similar**

A direct hash/diff comparison of all 12 shared modules:

```
main.py             1 line differs
map.py               identical (content)
npc.py                byte-identical
object_handler.py     identical (content)
object_renderer.py    identical (content)
pathfinding.py       2 lines differ
player.py           12 lines differ
raycasting.py         identical (content)
settings.py           identical (content)
sound.py             2 lines differ
sprite_object.py      byte-identical
weapon.py             identical (content)
```

Only **17 lines differ** out of **958 total shared lines** — about 98.2% line-for-line identical, confirming `CloneCompare.md`'s original finding that this is a copy/near-copy rather than an independent implementation.

<div align="right"><a href="#table-of-contents">^ TOC</a></div>
