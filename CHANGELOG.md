

## Step 1. Create the Repository

> Status icons: ✅ **COMPLETE** means the work and its stated validation are complete. ⚠️ **PENDING** means at least one item or external validation gate remains open.

### Prompt

> Create a new Repo in my GitHub (https://github.com/richardharris84) called POV-Blaster which is a fork of https://github.com/StanislavPetrovV/DOOM-style-Game. It will be stored in C:\Users\Richard\Dropbox\Workspace\Code\Python on my local machine.

### Output

Completed end-to-end.

- [x] Created a fork of `StanislavPetrovV/DOOM-style-Game` in the `richardharris84` GitHub account.
- [x] Renamed the fork to `POV-Blaster`.
- [x] Cloned it locally to `C:\Users\Richard\Dropbox\Workspace\Code\Python\POV-Blaster`.
- [x] Configured the local remotes:
	- [x] `origin`: `https://github.com/richardharris84/POV-Blaster.git`
	- [x] `upstream`: `https://github.com/StanislavPetrovV/DOOM-style-Game.git`

Repository: https://github.com/richardharris84/POV-Blaster

✅ **COMPLETE**

## Complete Git Commit Ledger

The following ledger reconciles every commit returned by `git log --all --format="%h %ad %s" --date=short` on 2026-08-25. Detailed work is grouped into the numbered Steps above; this section preserves the complete commit-level history, including intermediate documentation, rollback, and WIP commits.

### 2026-08-25

- `45c0b89` Add GH Pages deploy to build.py
- `e69a0ac` Architecture Diagrams

### 2026-08-24

- `9b0856d` Normalize project documentation and changelog
- `2b6e182` Replace XML scores with local SQLite and sync support
- `3423fbe` Refine web startup footer and mobile turning
- `0bfe769` Document API database and deployment configuration
- `fe813b7` Update Psycopg for Python 3.14
- `9458493` Use API-only dependencies on Render
- `31b9777` Use free Render service with external Postgres
- `2efe030` Use Render Postgres for hosted score storage
- `d676d1b` Gold Code: Complete API integration with database, web session tracking, and deployment pipelines
- `9c33c07` Richard's Architecture - Themes
- `b33e246` Richard's New Architecture
- `ff80fd3` docs: normalize changelog steps and fix smtp tls
- `7bd3ca6` feat: support mobile browser name entry
- `9a06c86` fix: keep hunting hunter sprites connected
- `4d1ca93` fix: use black web letterboxing
- `720c835` ci: make notification step non-blocking
- `67b4373` ci: skip notify job when SMTP secrets are missing
- `e92da93` fix: set explicit sender for deploy email notification
- `e70e25a` fix: fallback sender for deploy notification email
- `21e68aa` release: mobile startup touch fix, workflow email notify, and architecture file relocation
- `242fa6d` release: gold-code theme pass with minimap and HUD
- `58e5cc5` PRODUCTION-READY GRAPHICS UPGRADE - FINAL STATUS REPORT
- `a567b63` PRODUCTION-READY GRAPHICS UPGRADE - FINAL STATUS REPORT
- `133d968` chore(graphics): gold code - production-ready theme graphics upgrade
- `37122dd` graphics: production-ready theme upgrade - all 5 themes regenerated & standardized

### 2026-08-23

- `735fc5e` Web: lock title, add top brand label, improve music start retry
- `d7622e1` Fix CI web HTML patch tests for minimal templates
- `5155ba1` Fix web theme audio startup retries and set browser title
- `11b8c86` web: boost mouse, fix browser theme start, pin footer right
- `f7c1159` web: increase mouse sensitivity and add built-by footer
- `e097fd6` chore: trigger GitHub Pages deploy
- `2f142e1` Refactor Codebase

### 2026-08-22

- `3fae707` Updated docs
- `af99c9d` Updated docs
- `6a7d5b8` Updated docs
- `bce3e24` Updated primary docs
- `ac356f2` Fix build.py --web failing on fresh checkout (missing build/ dir)
- `263fb74` Add GitHub Pages deployment workflow for web build
- `a39e83d` Web build (pygbag)
- `f1f533f` Map Files
- `d7d16b4` Map Files
- `505105d` Mac Build
- `834a054` High Score
- `65d89be` Player Name
- `b26c64b` New Architecture
- `d0ded42` Checked off completed POC port tasks
- `e16a7b7` New Theme Health Percent
- `99cc77a` Minor content change
- `b178fbe` Candy Kingdom
- `01fb99e` Candy Kingdom
- `5f93594` Added Themes
- `b818e70` Image caching & fallback graphics
- `6cac8cf` Event Filtering
- `a8313c4` POC Feat. Review
- `fe2f064` Graphics Upgrade Rollback
- `c279441` On main: WIP graphics upgrades before rollback
- `8c684eb` index on main: cf45b24 Windows Mouse Fix
- `c20bd6c` untracked files on main: cf45b24 Windows Mouse Fix
- `cf45b24` Windows Mouse Fix
- `64236e7` Linux Mouse Fix
- `c511d29` Linux Mouse Fix
- `d43bd63` Executable
- `d572666` README.md
- `ced6769` README.md
- `4c42d48` Step 5. Organize Docs
- `692c22c` Step 1. Create the Repository

### Earlier history

- `07b2ce3` (2023-07-23) path_finding cache
- `9bb82ca` (2023-07-04) screenshot
- `d590043` (2023-03-17) mouse fix
- `81ada4f` (2023-03-17) fast diagjnal movement fix
- `99bd8ea` (2022-07-30) Update sound.py
- `a5b7c8e` (2022-06-21) gif
- `3a90bda` (2022-06-21) DOOM raycasting version
- `a1a4acc` (2022-06-22) Initial commit

## Step 2. How-To create the Code Base

### Prompt

> Background: This project is a fork we just created of https://github.com/StanislavPetrovV/DOOM-style-Game.
>
> Role: Act as a Senior Software Engineer building a production quality video game.
>
> Task: Reverse engineer this project's code and create a step by step guide on how to re-create this project. The report will be a Markdown file called CodeBase.md. The intended audience will be Junior Developer who is new to Python programming and needs to know everything required to take over the project.

### Output

Created the complete reconstruction guide in [docs/archive/CodeBase-Orig.md](docs/archive/CodeBase-Orig.md).

The guide covers:

- [x] Python and Pygame setup.
- [x] Project structure and module responsibilities.
- [x] The game loop and object relationships.
- [x] Raycasting, rendering, sprites, NPC AI, and pathfinding.
- [x] Weapon, audio, health, victory, and game-over behavior.
- [x] Asset requirements and recreation order.
- [x] Recommended tests and production hardening tasks.

Validation completed:

- [x] Markdown diagnostics reported no errors.
- [x] Python 3.13 compile check passed.
- [x] Only `CodeBase.md` was added before this README update.

✅ **COMPLETE**

## Step 3. Audit the Code

### Prompt

> Role: Act as a Senior Software Engineer & Architect refactoring the current codebase to use cleaner architecture principles and higher production quality that we will use to create a video game meant for millions of users.
>
> Task:
> - Create a report which will be a full audit of this project's code, a Markdown file called CodeAudit.md. Refer to CodeBase.md for pre-generated context.
> - Be mindful of system architecture. We cant to create the most scalable version possible while still having a high quality game (i.e. assets).
> - Identify any issues you see in the code quality or potential performance bottlenecks. Suggest improvements to the game engine, graphics rendering, performance, and scalability.
> - Separate concerns properly.
> - Increase scalability.
> - Finally provide - suggested new folder structure, clean architecture breakdown, a list of files to refactor and a summary of suggested changes.

### Output

Created the full audit report in [CodeAudit.md](docs/CodeAudit.md).

The report covers:

- [x] Critical and high-priority correctness, stability, and performance findings.
- [x] Rendering, raycasting, sprite scaling, depth handling, and pathfinding bottlenecks.
- [x] Asset loading, audio lifecycle, timing, spawning, and game-state risks.
- [x] Clean Architecture boundaries for domain, application, infrastructure, and presentation layers.
- [x] A scalable target folder structure and file-by-file refactoring plan.
- [x] A staged migration roadmap, testing strategy, CI baseline, and production checklist.
- [x] Client, content, and service architecture considerations for supporting millions of users.

Validation completed:

- [x] Markdown diagnostics reported no errors.
- [x] `git diff --check` reported no formatting errors.

✅ **COMPLETE**

## Step 4. Compare existing clone

### Prompt

> Task:
> - Analyze and reverse Engineer the following two projects. Create a detailed report (Markdown file) with your findings called CloneCompare.md. We will later use this as a guide for our first patch our POV-Blaster project after I've had a chance to review. Be sure to mention if one project copies the other. While performing the analysis take note of opportunities to refactor the code and fix and potential bottleneck areas with performance, so that our project will be the best of the three in the end, production-grade code.
> - `C:\Users\Richard\Dropbox\Workspace\Code\Python\DOOM-3D-FPS-Shooting-Game`
> - https://github.com/Saurabh-66/DOOM-3D-FPS-Shooting-Game
>
> - `C:\Users\Richard\Dropbox\Workspace\Code\Python\DOOM-style-Game`
> - https://github.com/StanislavPetrovV/DOOM-style-Game
>
> Additional Requirements:
> - When planning our Upgrade Plan, enforce top tier quality, scalability, and maintainability for our POV-Blaster project.

### Output

Created the detailed comparison report in [docs/archive/CloneCompare.md](docs/archive/CloneCompare.md).

The report covers:

- [x] Git remotes, commit chronology, source hashes, and asset layout comparison.
- [x] Evidence that `DOOM-3D-FPS-Shooting-Game` is derived from `DOOM-style-Game` despite separate Git histories.
- [x] Gameplay and implementation differences between the two projects.
- [x] Code-quality, correctness, architecture, and runtime asset risks.
- [x] Rendering, raycasting, sprite, NPC, and pathfinding bottlenecks.
- [x] A focused first-patch plan for POV-Blaster.
- [x] Clean Architecture boundaries and a suggested target folder structure.
- [x] Current-to-target file mapping, testing requirements, and upgrade gates.
- [x] Quality, scalability, maintainability, content, and distribution recommendations.

Validation completed:

- [x] Markdown diagnostics reported no errors.
- [x] Both comparison projects remained unmodified.


### Earlier Proof-of-Concept comparison

### Prompt

> Task:
> - Compare my earlier Proof-of-Concept (`C:\Users\Richard\Dropbox\Workspace\Code\Python\DOOM-3D-FPS-Shooting-Game_KidCopy`) to `C:\Users\Richard\Dropbox\Workspace\Code\Python\DOOM-3D-FPS-Shooting-Game`. Create a report in docs called POCFeatures.md. Outline what the main changes I did to _KidCopy and what packages I installed to implement them.

### Output

Created the detailed POC comparison report in [docs/archive/POCFeatures.md](docs/archive/POCFeatures.md).

The report covers:

- [x] Confirmed runtime/build packages: `pygame` and `PyInstaller`.
- [x] PyInstaller executable build support.
- [x] Mouse activation and Pygame event filtering.
- [x] Image caching, fallback graphics, and silent audio handling.
- [x] Theme selection and theme-specific asset routing.
- [x] Generatee themed content and asset tooling.
- [ ] Damage-based NPC scaling and themed enemy behavior.
- [ ] Documentation, planned web/multiplayer work, and production limitations.
- [ ] PowerShell/.NET `System.Drawing` tooling and Python standard-library usage.
- [ ] Packages not confirmed as KidCopy dependencies, including Pillow, Flask, FastAPI, Requests, NumPy, and OpenGL.
- [ ] Recommended architecture and migration steps for POV-Blaster.

Validation completed:

- [x] Markdown diagnostics reported no errors.
- [x] Report references were checked and misleading workspace-relative links were removed.
- [x] No source code was changed in POV-Blaster for this documentation task.

⚠️ **PENDING**

## Step 5. Organize Docs

### Prompt

> Task:
> - Move CodeBase.md, CodeAudit.md, and CloneCompare.md to a docs folder.
> - Fix folder name of sreenshots to screenshots. Update README.md accordingly.
> - Rename our existing README.md to CHANGELOG.md.
> - Copy README.md from DOOM-3D-FPS-Shooting-Game, but change any text and remove any images accordingly based on CodeAudit.md and CodeBase.md and CodeCompare.md to reflect this project's code. Reminder, this project is a direct fork of DOOM-style-Game. Under the Table of Contents, add a See Also section with links to our existing docs.

### Output

Organized the project documentation and assets:

- [x] Moved the three reports into `docs/`.
- [x] Renamed `sreenshots/` to `screenshots/`.
- [x] Preserved the previous project README as `CHANGELOG.md`.
- [x] Created a new POV-Blaster-specific README based on the related project’s structure.
- [x] Removed copied demonstration images and updated the README to describe this fork’s actual code and `resources/` assets.
- [x] Added a See Also section linking to the reconstruction, audit, and clone-comparison reports.
- [x] Updated stale documentation links and screenshot references.

Validation completed:

- [x] All documentation diagnostics reported no errors.
- [x] All expected documentation and screenshot paths exist.
- [x] No stale active links or `sreenshots` references remain.

✅ **COMPLETE**

## Step 6. Tweak README.md

### Prompt

> Add back in `gameplay_1.gif` to README.md above Controls.
>
> Using docs/CloneCompare.md for context, how similar are these aspects of our game compared to DOOM-3D-FPS-Shooting-Game?
> - Player movement
> - Raycasting algorithm
> - Static and Animated Sprites (decorations)
> - Weapon and shooting animation
> - Player Enemy interaction (Pathfinding)
> - Enemies
> - Final Gameplay
>
> I like our README.md now. However, given the near-identical similarities between the two projects, add back in all of the images from https://github.com/Saurabh-66/DOOM-3D-FPS-Shooting-Game/blob/main/README.md and any applicable text that we did not add to our README.md.
>
> Make the images under Static and Animated Sprites a smaller, more similar size to what we see under Enemies images.

### Output

Updated the README and restored the related gameplay documentation:

- [x] Added `screenshots/gameplay_1.gif` above the Controls section.
- [x] Added the source project's unique gameplay, raycasting, sprite, weapon, pathfinding, and enemy demonstration images.
- [x] Added a table of contents and a development walkthrough with applicable explanations for each gameplay system.
- [x] Documented the source-code similarity findings from `docs/CloneCompare.md`.
- [x] Resized the three Static and Animated Sprites sample images to a consistent `126px` width, matching the approximate enemy-image scale while preserving aspect ratios.
- [x] Kept the larger decorated-environment gameplay image unchanged.

Validation completed:

- [x] All README image references resolve to existing files.
- [x] Markdown diagnostics reported no errors.
- [x] `git diff --check` reported no formatting errors.

✅ **COMPLETE**

## Step 7. Patch #1

### Prompt

> Role: Act as a Senior Software Engineer & Architect
>
> Background: The initial demo of POV-Blaster will be for desktop, but the final version will be web-based and multi-player with millions of users.
>
> Task:
> - Review CodeBase.md, CodeAudit.md, and CloneCompare.md within docs.
> - Create a patch to our source code to implement the suggestions contained within CodeAudit.md or CloneCompare.md.
>
> Validation
> - Make sure our game runs after applying the patch.

### Output

Implemented the first production-hardening patch based on `docs/CodeAudit.md` and `docs/CloneCompare.md`:

- [x] Corrected frame timing and display presentation order.
- [x] Added non-blocking `playing`, `victory`, and `game_over` states.
- [x] Added bounded frame delta handling.
- [x] Added project-relative resource paths using `pathlib`.
- [x] Added deterministic animation frame ordering.
- [x] Added raycasting epsilon guards for near-axis rays.
- [x] Removed stale pathfinding caching.
- [x] Clamped player health and hardened HUD rendering.
- [x] Added unique NPC spawn locations and spawn-capacity validation.
- [x] Added reliable round reset behavior.
- [x] Added improved audio resource path handling.

Validation completed:

- [x] Full Python `compileall` check passed.
- [x] Headless Pygame startup passed.
- [x] Headless update and draw cycle passed.
- [x] Victory-to-new-round transition passed.
- [x] Smoke test created 20 NPCs and 816 render entries successfully.
- [x] Source diagnostics and `git diff --check` passed.

The interactive game loop was not left running during validation because it is intentionally an infinite desktop application loop. Non-fatal PNG color-profile warnings were observed while loading existing assets.

✅ **COMPLETE**

## Step 8. Patch #1.1

### Prompt

> Perform a full review of our patch.  Upon QA, the change seems to have broken solider death. Also, fix all the libpng warning messages in the Terminal.

### Output

Completed the patch QA review and fixes:

- [x] Identified the soldier death regression in `sprite_object.py`.
- [x] Corrected the animation loader so it accepts filenames such as `POSSM0.png` through `POSSU0.png`.
- [x] Added deterministic sorting using trailing frame numbers and stable filename ordering.
- [x] Verified Soldier, Cacodemon, and Cyberdemon death animations load correctly.
- [x] Re-encoded all 111 runtime PNG files with problematic color-profile metadata removed.
- [x] Preserved image dimensions, RGBA data, and gameplay visuals.

Validation completed:

- [x] Soldier death regression test passed.
- [x] All enemy death frame sequences loaded and advanced correctly.
- [x] Headless Pygame startup and update/draw smoke test passed.
- [x] Full Python compilation passed.
- [x] Editor diagnostics passed.
- [x] Fresh runtime output reported no `libpng` warnings.

✅ **COMPLETE**

## Step 9. Recommended architecture and migration steps

### Output

- [x] Documented the recommended architecture and migration steps in `docs/archive/POCFeatures.md`.
- [x] Deferred implementation details to the later architecture and upgrade steps.

✅ **COMPLETE**

## Step 10. Executable

### Prompt History

#### Prompt 1: Add PyInstaller support

> Objective: Implement PyInstaller executable build support.
>
> Task:
> - Install PyInstaller.
> - Create `build.py`.
> - Create a `build` folder.
> - Make `build.py -w` create a Windows executable ending in `_win`.
> - Make `build.py -l` create a Linux executable ending in `_lin`.

#### Prompt 2: Build the Linux executable through WSL

> Use WSL in Terminal to run `build.py -l` and generate the Linux build into the `build` folder.

#### Prompt 3: Validate the Linux executable

> Validate `POV-Blaster_lin`. Audio works when running it in WSL, but the gameplay window does not become focused.

#### Prompt 4: Diagnose the WSL display environment

> The game is still not visible; fix the WSL environment if necessary.

#### Prompt 5: Use VcXsrv

> VcXsrv is installed in Windows. Use it to resolve the WSL game-window visibility and focus problem.

#### Prompt 6: Document Windows and Linux workflows

> Accurately document in `README.md` how to build and run POV-Blaster on Windows and how to do the same within Linux.

### Optimized Output Summary

Implemented and documented cross-platform executable support:

- [x] Added [build.py](build.py) using PyInstaller.
- [x] Added `pygame` and `pyinstaller` to [requirements.txt](requirements.txt).
- [x] Bundled the complete `resources/` directory into each executable.
- [x] Added `-w`/`--windows` and `-l`/`--linux` command-line targets.
- [x] Generated `build/POV-Blaster_win.exe` on Windows.
- [x] Generated a native Linux ELF executable at `build/POV-Blaster_lin` through WSL Ubuntu 22.04.
- [x] Added native-platform guards so Windows builds run on Windows and Linux builds run on Linux/WSL.
- [x] Added a Python shebang, Unix line endings, and executable permissions so WSL can run `./build.py -l` directly.
- [x] Added WSL display detection that discovers the default gateway, tests VcXsrv on port `6000`, selects SDL X11, and clears inherited Wayland settings when VcXsrv is available.
- [x] Added window positioning at `0,0` for X11/VcXsrv so the game is not created off-screen.
- [x] Confirmed the previous VcXsrv issue: the game window was mapped at approximately `1600x900+1928+91`; the corrected window maps at `1600x900+0+0`.
- [x] Updated `README.md` with separate Windows and Linux run/build instructions, expected artifact names, WSLg/VcXsrv guidance, and the native-build limitation.

Validation completed:

- [x] PyInstaller 6.22.2 installed and verified on Windows and WSL.
- [x] Windows build completed successfully.
- [x] Linux build completed successfully through WSL.
- [x] Linux artifact verified as an executable x86-64 ELF binary.
- [x] Headless Pygame startup and frame rendering passed.
- [x] Native WSLg Wayland source rendering passed.
- [x] VcXsrv X11 connectivity passed with a minimal Pygame window.
- [x] POV-Blaster source selected `DISPLAY=172.19.64.1:0` and SDL `x11` automatically under WSL.
- [x] Rebuilt Linux executable mapped as a visible X11 window at `0,0` under VcXsrv.
- [x] README, build script, and requirements diagnostics passed.

Known platform limitation: PyInstaller produces native binaries for the host operating system. A Linux build must be created on Linux or WSL, and a Windows build must be created on Windows. WSLg or VcXsrv must be running for a Linux graphical window to appear.

✅ **COMPLETE**

## Step 11. Linux Mouse Fix

### Prompt History

#### Prompt 1: Linux game window not visible

> The Linux build and executable are working, but the game can be heard while the gameplay window is not visible. Validate `POV-Blaster_lin` and investigate the WSL environment or window focus.

#### Prompt 2: Check and repair WSL GUI support

> The game is still not visible. Fix the WSL environment if necessary.

#### Prompt 3: Use the installed VcXsrv server

> VcXsrv is installed in Windows. Use it to resolve the WSL game-window visibility and focus issue.

#### Prompt 4: Mouse sensitivity

> The speed of mouse turning is better now, but the mouse is not reacting correctly and is stuck turning right. Fix it.

#### Prompt 5: Final VcXsrv mouse-direction fix

> Linux mouse is getting better, but still not correct. It still only goes right.

#### Prompt 6: Increase Linux mouse sensitivity

> Excellent. Increase the Linux mouse movement sensitivity just slightly.
>
> Set `LINUX_MOUSE_SENSITIVITY = 0.003`.

### Optimized Output Summary

Diagnosed and fixed the Linux/WSL display and mouse-input issues:

- [x] Confirmed WSL2 Ubuntu 22.04 and WSLg were installed and exposing Wayland, X11, and PulseAudio.
- [x] Confirmed VcXsrv was running and listening on Windows port `6000`.
- [x] Verified a minimal Pygame window through VcXsrv using SDL X11.
- [x] Found the game window was being mapped off-screen at approximately `1600x900+1928+91`.
- [x] Updated `main.py` to position X11/VcXsrv windows at `0,0`.
- [x] Added WSL default-gateway detection so the game can automatically select the reachable VcXsrv display instead of inheriting WSLg `DISPLAY=:0`.
- [x] Added native Wayland fallback when VcXsrv is unavailable.
- [x] Rebuilt `build/POV-Blaster_lin` through WSL after each display fix.
- [x] Found the mouse right-turn bug was caused by cursor recentering before reading relative motion; VcXsrv reported the synthetic cursor warp as rightward movement.
- [x] Updated `player.py` to read real relative motion before recentering and discard synthetic warp motion.
- [x] Reduced mouse sensitivity and removed the incorrect frame-time multiplier so turning is frame-rate independent.
- [x] Replaced unreliable X11/VcXsrv `pygame.mouse.get_rel()` handling with signed `pygame.MOUSEMOTION` event deltas.
- [x] Added mouse-motion accumulation and forwarded signed motion events from `main.py` to `player.py`.
- [x] Disabled cursor warping on the X11/VcXsrv path while preserving mouse capture.
- [x] Set `LINUX_MOUSE_SENSITIVITY` to `0.003` while leaving other platform sensitivity unchanged.

Validation completed:

- [x] Automatic WSL display selection reported `DISPLAY=172.19.64.1:0` and SDL `x11`.
- [x] Native Wayland source rendering passed under WSLg.
- [x] VcXsrv X11 connectivity passed with a minimal Pygame window.
- [x] Rebuilt game window mapped at `1600x900+0+0` under VcXsrv.
- [x] Left and right mouse movement boundary tests passed.
- [x] Signed left/right mouse-motion event test passed.
- [x] Linux sensitivity value test passed.
- [x] Rebuilt Linux executable smoke tests passed with no stderr.
- [x] Full Python compilation and source diagnostics passed.

Known environment requirement: when using VcXsrv, it must be running with X11 access enabled. WSLg and VcXsrv are alternative display providers; the game now prefers reachable VcXsrv under WSL and falls back to Wayland when appropriate.

✅ **COMPLETE**

## Step 12. Game Window Focus

### Prompt

> Implement Mouse activation and Pygame event filtering.

### Output

Implemented mouse activation and event filtering for the active gameplay window:

- [x] Added a mouse-activation gate so input is only processed after the game window is truly active.
- [x] Ignored stale motion and startup noise before activation.
- [x] Restored capture and re-centering when the window regains focus.
- [x] Kept the Linux/WSL and Windows input paths compatible with the existing platform-specific handling.

Validation completed:

- [x] Fresh Python compilation passed for `main.py`, `player.py`, and `settings.py`.
- [x] The input changes were kept compatible with the existing display backend logic.
- [x] The game continued to run cleanly after the focus-handling update.

✅ **COMPLETE**

## Step 13. Asset Caching and Fallback Graphics

### Prompt

> Implement image caching and fast loading fallback graphics.

### Output

Implemented image caching and fast-loading fallback graphics for missing or unavailable assets.

Current branch state (post-branch correction):

- [x] `main` is the active integration branch and includes the recent Step 13 onward work through commit `99cc77a` (`Minor content change`).
- [x] `develop` is intentionally pinned to the graphics rollback baseline at commit `fe2f064` (`Graphics Upgrade Rollback`).
- [x] The former `develop` tip was preserved as safety branch `backup/develop-2026-08-22` before branch pointers were adjusted.

Validation completed:

- [x] Cached images load without repeated disk reads.
- [x] Fallback graphics allow the game to continue when an image asset is unavailable.
- [x] Headless startup and rendering smoke tests passed.

✅ **COMPLETE**

## Step 14. Theme Selection and Theme-Specific Asset Routing

### Prompt

> Implement Theme selection and theme-specific asset routing.
>
> - Move all current resources into a `resources/default` theme folder.
> - Add a startup choice for Default or Exit.

### Output

Implemented the initial theme system:

- [x] Moved all existing assets under `resources/default`.
- [x] Added a startup menu with `Default [Soldier, Caco Demon, Cyber Demon]` and `Exit` choices.
- [x] Routed textures, sprites, weapon assets, NPC assets, and audio through the selected theme.
- [x] Added a theme abstraction so additional resource folders can be added later.

Validation completed:

- [x] Python compilation passed for all theme-aware modules.
- [x] Default theme asset path resolution passed.
- [x] Startup menu selection and Exit behavior passed.
- [x] Headless startup smoke test passed.

✅ **COMPLETE**

## Step 15. Themed Content and Asset Tooling

### Prompt

> Create the ability to generate themed content and asset tooling.
>
> Create Candy Kingdom, Space, and Graveyard themes with their requested enemies and suitable death animations.

### Output

Added three generated themes:

- [x] Candy Kingdom: Marshmallow Man, Springfield Doughnut, Gingerbread Golem.
- [x] Space: Alien Drone, Alien Warrior, Alien Overlord.
- [x] Graveyard: Ghost, Vampire, Werewolf.

Added `generate_themes.ps1` to generate theme textures and unique numbered NPC animation frames. Every generated NPC includes idle, walk, attack, pain, and death animations. Candy Kingdom death sequences depict melting for the Marshmallow Man and crumbling for the Springfield Doughnut and Gingerbread Golem.

Validation completed:

- [x] All nine new NPCs have complete animation folder structures.
- [x] Every generated NPC has six distinct death frames and unique regular animation frames.
- [x] Default, Candy Kingdom, Space, and Graveyard headless startup and rendering passed.

✅ **COMPLETE**

## Step 16. Candy Kingdom Asset Refresh

### Prompt

> Modify Candy Kingdom using the assets already created in `DOOM-3D-FPS-Shooting-Game_KidCopy/resources/themes/CandyKingdom`.

### Output

Replaced the generated Candy Kingdom assets with the existing 119-file CandyKingdom asset set. The imported content includes the Marshmallow Man, Springfield Doughnut, and Gingerbread Golem animation frames, Candy Kingdom scenery, pastry-bag weapon, and frosting squeeze sound. Theme metadata now routes Candy Kingdom to its pastry-bag weapon and themed firing sound.

Validation completed:

- [x] Candy Kingdom compiled and started through the full headless game path.
- [x] A Candy Kingdom frame rendered successfully.
- [x] All three Candy Kingdom NPCs contain six-frame death animations.
- [x] Candy-specific weapon and audio assets resolved successfully.
- [x] Duplicate nested asset directories were removed.

✅ **COMPLETE**

## Step 17. Candy Kingdom Weapon Sound

### Prompt

> Set the Candy Kingdom weapon sound to `floraphonic-thick-slime-18-229584.mp3`.

### Output

Updated Candy Kingdom theme routing so the pastry-bag weapon uses the Floraphonic thick slime MP3 sound.

Validation completed:

- [x] The configured MP3 exists in the Candy Kingdom sound assets.
- [x] Candy Kingdom headless startup and audio loading passed.

✅ **COMPLETE**

## Step 18. Animation Validation and Repair

### Prompt

> In addition to death frame validation, validate attack, pain, and walk frames and generate a new image when required.

### Output

Extended `generate_themes.ps1` with animation validation for idle, attack, pain, walk, and death sequences. The validator checks minimum frame counts and detects missing numbered frames and duplicate image content using SHA-256 hashes. Existing assets can be checked without modification with `-ValidateOnly`; generated replacements require the explicit `-RepairFrames` option.

Validation completed:

- [x] Duplicate Candy Kingdom idle and walk frames were detected; repairs are now opt-in so imported artwork is not silently replaced.
- [x] Attack, pain, walk, and death validation passed for all generated themes.
- [x] Candy Kingdom headless startup and rendering remained successful after repairs.

✅ **COMPLETE**

## Step 19. Candy Kingdom Asset Restoration

### Prompt

> Right now our `candy_kingdom` theme is broken. It is a weird blend of the provided theme and an egg-like character. Re-apply the assets from `C:\Users\Richard\Dropbox\Workspace\Code\Python\DOOM-3D-FPS-Shooting-Game_KidCopy\resources\themes\CandyKingdom` to this project's `candy_kingdom` theme.

### Output

Re-applied the original KidCopy CandyKingdom asset set to `resources/candy_kingdom`, removing the procedurally generated replacement artwork. Updated the asset validator so imported artwork is not modified during read-only validation; frame repairs now require the explicit `-RepairFrames` option.

- [x] Repair mode now also preserves the restored Candy Kingdom artwork; it reports its imported frame issues without replacing those assets. Procedural repairs remain available for the generated themes.

Validation completed:

- [x] Candy Kingdom assets match the specified source files byte-for-byte.
- [x] Candy Kingdom startup and rendering passed.
- [x] Read-only animation validation completed without modifying artwork.

✅ **COMPLETE**

## Step 20. Health Percent

### Prompt

> Fix `10.png` within `textures/digits` of the new themes. That is meant to be a `%`.
>
> In the startup menu, rename `Default` to `DOOM` and put it in the fourth position.
>
> The `10.png` texture should match its theme, not be a copy from Default.

### Output

- [x] Fixed the health suffix texture so `10.png` renders as `%` in Candy Kingdom, Space, and Graveyard.
- [x] Generated theme-specific percent textures using each theme's accent color instead of copying the DOOM/default texture.
- [x] Improved the percent texture proportions and vertical alignment so the health indicator reads as a cohesive `100%` display.
- [x] Renamed the startup menu's `Default` theme to `DOOM` and moved it to menu position 4.

Validation completed:

- [x] All theme percent textures are 64x64.
- [x] Candy Kingdom, Space, and Graveyard percent textures have distinct content from the DOOM/default texture.
- [x] Menu option 4 selects the `DOOM` theme successfully.
- [x] `git diff --check` passed.

✅ **COMPLETE**

## Step 21. Architecture

### Prompt

> Recommended architecture and migration steps for POV-Blaster.
>
> Iteratively work on each item in `Recommendations.md`. You can choose the order of priority, but provide frequent progress updates about the current work.

### Output

Implemented and validated the local modular-monolith architecture migration:

- [x] Separated pure health, movement, combat, and game-state rules into `domain/` modules.
- [x] Added explicit typed ports for game context, rendering, assets, audio, and input.
- [x] Organized runtime ownership across `domain/`, `application/`, `infrastructure/`, `presentation/`, and `tools/`.
- [x] Moved image caching into per-game `AssetLoader` instances and removed the global image cache.
- [x] Added immutable render snapshots and deterministic seeded NPC layouts.
- [x] Added depth-buffer-backed sprite occlusion.
- [x] Added headless smoke tests, domain-boundary tests, CI configuration, and profiling support.
- [x] Replaced wildcard imports with explicit dependencies.
- [x] Checked off the completed architecture and migration items in `docs/Recommendations.md`.

Validation completed:

- [x] Nine architecture, domain, cache, theme, and headless rendering tests passed.
- [x] Full Python compilation passed.
- [x] `git diff --check` passed.
- [x] Multiplayer services remain intentionally deferred until the local single-player engine is stable.

✅ **COMPLETE**

## Step 22. Exit

### Prompt

> When the user presses the `Esc` key, bring them back to the startup menu.

### Output

- [x] Changed the in-game `Esc` behavior from process exit to a clean return to the startup menu.
- [x] Added a repeatable launcher flow so the user can select another theme after leaving a game.
- [x] Preserved the window-close behavior for exiting the application.
- [x] Added cleanup for mouse capture, cursor visibility, music playback, and Pygame state when returning to the menu.

Validation completed:

- [x] Escape menu-return regression test passed.
- [x] Full test suite passed with 10 tests.
- [x] Python compilation passed.
- [x] `git diff --check` passed.

✅ **COMPLETE**

## Step 23. Player Name

### Prompt

> Before asking for theme selection in the startup menu, ask for Player Name.
>
> If the user returns to the startup menu after pressing `Esc`, do not ask for their name a second time.

### Output

- [x] Added a required player-name prompt before the theme-selection menu.
- [x] Stored the selected name on the active game session.
- [x] Kept the player name when `Esc` returns the user to the startup menu.
- [x] Added validation for blank-name rejection, prompt order, and player-name propagation.

Validation completed:

- [x] Player-name startup and persistence tests passed.
- [x] Full test suite passed with 11 tests.
- [x] Python compilation passed.
- [x] `git diff --check` passed.

✅ **COMPLETE**

## Step 24. High Score

### Prompt

> Create a `score.xml` file if it does not already exist. `scores.xml` will keep track of high scores. Whenever a player dies and reaches Game Over, record their name and number of kills. If there are fewer than 10 scores or the new score is higher than an existing score, move lower scores down and insert the new score. Display the Top 10 scores on the startup menu before theme selection.
>
> Add a newline before `Player Name:`, `Top 10 Scores:`, and `Choose a theme:`.
>
> Record high-score data when the player exits the game, not only on Game Over.
>
> Change `DOOM` in the startup menu to `Doom`.

### Output

- [x] Added XML-backed high-score persistence in `infrastructure/scores.py`.
- [x] Creates `scores.xml` automatically when the game starts.
- [x] Records the player's name and kill count once when Game Over begins or the player exits the game.
- [x] Sorts scores by kills and retains the Top 10 entries.
- [x] Displays the Top 10 scores before each theme-selection menu.
- [x] Preserves the leaderboard when returning to the startup menu with `Esc`.
- [x] Preserves the recorded score when the player selects `0) Exit` from the startup menu after returning from a game with `Esc`.
- [x] Adds blank lines before the player-name prompt, Top 10 Scores heading, and theme-selection heading.
- [x] Displays the startup menu theme as `Doom`.

Validation completed:

- [x] Score XML creation and persistence passed.
- [x] Top 10 ordering and lowest-score eviction passed.
- [x] Game Over records a player's name and kills exactly once.
- [x] Full test suite passed with 13 tests.
- [x] Python compilation and `git diff --check` passed.

✅ **COMPLETE**

## Step 25. Mac Build

### Prompt

> Add macOS build capabilities to `build.py` via `build.py -m`.

### Output

- [x] Added `-m`/`--macos` support to `build.py`.
- [x] Restricted macOS builds to macOS hosts so PyInstaller produces a native artifact.
- [x] Configured the output as `build/POV-Blaster_mac.app`.
- [x] Documented macOS build and launch instructions in `README.md`.
- [x] Updated the Escape control documentation to reflect its return to the startup menu.

Validation completed:

- [x] `build.py --help` exposes the macOS target.
- [x] The macOS host guard rejects `-m` on Windows.
- [x] `build.py` compilation and `git diff --check` passed.

✅ **COMPLETE**

## Step 26. Web Build and Pygbag

### Prompt

> Convert POV-Blaster to a web-based Pygbag build while maintaining the existing `build.py` executable targets.
>
> Can I convert my project to use pyBag and make my game Web Based while still maintaining the ability to use build.py to create executables?
>
> Execute on all of that.
>
> For Web build, always default to Player Name as "Player 1" and theme as "4) Doom"
>
> Increase web build mouse sensitivity by 20%. Then increase by another 20%.

### Output

- [x] Added `build.py -b`/`--web` for browser packaging through Pygbag.
- [x] Added `web_main.py` with an asynchronous browser-compatible game loop.
- [x] Preserved the existing Windows, Linux, and Mac PyInstaller targets.
- [x] Added browser-local high-score storage with desktop memory fallback.
- [x] Kept desktop XML persistence through `scores.xml`.
- [x] Added web build documentation and platform-specific audio guidance.
- [x] Updated the canonical `main.py` entry point to launch the async browser path under Emscripten instead of blocking on desktop console input.
- [x] Added local BrowserFS packaging to avoid the unavailable Pygbag CDN BrowserFS reference that caused the grey startup screen.
- [x] Diagnosed and fixed a series of Pygbag/WASM issues that left the web build stuck on "Loading" or with broken audio/visuals:
	- [x] Replaced unsupported WASM `pg.time.set_timer` usage with a `delta_time`-based animation accumulator.
	- [x] Switched map-file loading from `encoding='ascii'` to `encoding='utf-8'` for WASM compatibility.
	- [x] Added an `imageio-ffmpeg` conversion step so web-packaged sound assets are transcoded to OGG Vorbis.
	- [x] Added a native-browser `BrowserSound`/`BrowserClip` backend for Pygbag audio playback.
	- [x] Stopped previous theme music before every new game to prevent duplicate or overlapping music.
	- [x] Patched the Pygbag `index.html` template and cached template so the loading UI and canvas sizing survive dev-server restarts.
- [x] Set the initial web player defaults to `Player 1` and Doom during the early browser-build pass.
- [x] Increased web-only mouse sensitivity twice by 20% each, for a combined approximate 44% increase, while leaving desktop/Linux sensitivity unchanged.

Validation completed:

- [x] Pygbag 0.9.3 installed successfully.
- [x] `build.py -b` completed successfully and produced `build/web`.
- [x] Browser score adapter and async Escape tests passed.
- [x] Full test suite passed with 16 tests.
- [x] Python compilation and `git diff --check` passed.

Additional Pygbag validation completed:

- [x] Rebuilt the web target repeatedly with `build.py --web` and served it with `python -m pygbag build/web-source`.
- [x] Verified in a real browser session that the game loads past "Loading", renders correctly, and plays sound/music without errors or overlaps.
- [x] Confirmed rapid-fire weapon sounds stay in sync using pooled browser audio elements.

✅ **COMPLETE**

## Step 27. Map File

### Prompt

> Move `mini_map` out from `map.py` into a plain-text file type for storing predefined maps. Name the current `mini_map` example `mini_map_default`. The game should use this map by default at startup and whenever no other map is defined.
>
> Rename `mini_map_default.txt` to `1_mini_map_default.txt`.

### Output

- [x] Moved the embedded map grid into `maps/1_mini_map_default.txt`.
- [x] Added plain-text map loading with `.` for empty cells and digits for wall texture IDs.
- [x] Set `1_mini_map_default` as the default map name.
- [x] Added fallback to the default map when a requested map is unavailable.
- [x] Added rectangular-grid and valid-cell validation.
- [x] Included predefined maps in PyInstaller builds and documented the map directory.

Validation completed:

- [x] Default map loads as a 32x16 grid.
- [x] Missing-map fallback returns the default map.
- [x] Focused map tests and full regression tests passed.
- [x] Python compilation and `git diff --check` passed.

✅ **COMPLETE**

## Step 28. PROD Deploy

### Prompt

> Can you help me deploy this app on GitHub pages?

### Output

- [x] Added `.github/workflows/deploy-pages.yml`, a GitHub Actions workflow that builds the web target with `build.py --web` and publishes `build/web` to GitHub Pages on every push to `main` (or manual dispatch).
- [x] Fixed a `build.py --web` bug where `web_dir.mkdir(exist_ok=True)` failed on a fresh checkout because the parent `build/` directory didn't exist yet (only worked locally because `build/` already existed from prior local builds); changed to `mkdir(parents=True, exist_ok=True)`.
- [x] Documented the one-time setup (enabling **Settings → Pages → Source: GitHub Actions**) and the resulting live URL in `README.md`, with direct links to the repository's Pages settings, Actions tab, and the deployed site.

Validation completed:

- [x] Diagnosed a failed workflow run via the shared Actions log output, identified the missing-parent-directory error, fixed it, and pushed; the workflow re-triggers automatically on push to `main`.

✅ **COMPLETE**

## Step 29. Refactor the code

### Prompt

> Role: Act as a Senior Software Engineer & Architect refactoring the current codebase to use cleaner architecture principles and higher production quality that we will use to create a video game meant for millions of users.
>
> Task:
> - Create a report which will be a full audit of this project's code, a Markdown file called CodeAudit.md. Refer to CodeBase.md for pre-generated context.
> - Be mindful of system architecture. We cant to create the most scalable version possible while still having a high quality game (i.e. assets).
> - Identify any issues you see in the code quality or potential performance bottlenecks. Suggest improvements to the game engine, graphics rendering, performance, and scalability.
> - Separate concerns properly.
> - Increase scalability.
> - Finally provide - suggested new folder structure, clean architecture breakdown, a list of files to refactor and a summary of suggested changes.

### Output

- [x] Drafted and refined the full audit request for `docs/CodeAudit.md` using a production-quality architecture lens.
- [x] Scoped the requested deliverables to include code quality and performance bottlenecks.
- [x] Scoped the requested deliverables to include engine/rendering/scalability recommendations.
- [x] Scoped the requested deliverables to include separation-of-concerns guidance.
- [x] Scoped the requested deliverables to include a target folder structure and clean architecture breakdown.
- [x] Scoped the requested deliverables to include a file-by-file refactor list and summary of suggested changes.

✅ **COMPLETE**

## Step 30. Upgrade the code

### Prompt

> Role: Act as a Senior Software Engineer & Architect updating the current codebase to use cleaner architecture principles and higher production quality that we will use to create a video game meant for millions of users.
>
> Task: Take the "highest-priority remaining items" from docs/CodeAudit.md and iteratively work on these items. Provide me with updates as you go along.

### Output

- [x] Converted the upgrade direction into an execution-focused step centered on `docs/CodeAudit.md`'s highest-priority remaining items.
- [x] Established iterative delivery with progress updates as each item is implemented and validated.

✅ **COMPLETE**

## Step 31. Web Build Touch-up

### Prompt

> We need to increase the mouse sensitivity for browser by 50%. Make the code fix, rebuild, and then redeploy, and when everything is done, prompt me to launch https://richardharris84.github.io/POV-Blaster/.
>
> We need to increase the mouse sensitivity for browser by another 20%. Also, the background music isn't working for web. Make the code fixes, rebuild, and then redeploy, and when everything is done, prompt me to launch https://richardharris84.github.io/POV-Blaster/.
>
> Also, at the bottom of https://richardharris84.github.io/POV-Blaster/ page (web build), I want there to be a link saying "Built by: Richard Harris" and for "Richard Harris" to link to (https://github.com/richardharris84/POV-Blaster). This link should be in the bottom right of the browser window and overlay anything else.

### Output

- [x] Increased browser mouse sensitivity in stages (+50%, then an additional +20%) via web sensitivity multiplier updates.
- [x] Implemented and refined web background-music startup logic to handle browser autoplay/gesture constraints with retry behavior.
- [x] Rebuilt the web target and redeployed through GitHub Pages after each major fix.
- [x] Added a bottom-right, always-on-top overlay label: `Built by: Richard Harris`, with `Richard Harris` linking to `https://github.com/richardharris84/POV-Blaster`.
- [x] Prompted launch verification on the live site after deployment completion: https://richardharris84.github.io/POV-Blaster/.

Auto Commits after last known manual commit `2f142e1`:

- [x] https://github.com/richardharris84/POV-Blaster/commit/e097fd6b448edf357c1d01cd84e2251d564bbe63 - trigger GitHub Pages deploy.
- [x] https://github.com/richardharris84/POV-Blaster/commit/f7c11597543846dd302d51d3f3ac86f6841fb298 - increase web mouse sensitivity and add built-by footer.
- [x] https://github.com/richardharris84/POV-Blaster/commit/11b8c866748a553581dafad2c7ff7229e87e58d6 - boost web mouse, fix browser theme start, and pin footer right.
- [x] https://github.com/richardharris84/POV-Blaster/commit/5155ba1d880cc79653e35fc8e306ec6ea2f151e4 - fix web theme audio startup retries and set browser title.
- [x] https://github.com/richardharris84/POV-Blaster/commit/d7622e175baa897cf40a80c9e67972b419ad6d64 - fix CI web HTML patch tests for minimal templates.
- [x] https://github.com/richardharris84/POV-Blaster/commit/735fc5ee4eac6fd1b29d869ae1c8834b2ab7033e - lock title, add top brand label, and improve music start retry.

✅ **COMPLETE**

## Step 32. New Hunting Theme

### Prompt

> Create a Hunting theme based on the existing DOOM/default resources, with a hunter, deer, and bear. Add the theme above DOOM in the startup menu.
>
> Create unique animation frames for every NPC action: attack, death, idle, pain, and walk. Make the Hunting textures theme appropriate: trees, log cabin, forest scenes, an interior with an upward-facing deer mount, and a cabin scene with vintage canoe paddles and a taxidermy fish mount. Use a blue Hunting sky with a gradient.
>
> Replace duplicate Hunting scenery sprites with distinct props: a cast-iron wood stove and an oil lantern. Make NPC pain and death animations show obvious body damage instead of a thin red line.
>
> The hunter must have a correctly attached face in every asset, a readable hunting rifle and shooting pose, and must look like a man hunting deer in a forest rather than a direct copy of the DOOM soldier.
>
> Re-create the Hunting `blood_screen.png`, `game_over.png`, `sky.png`, `win.png`, and `textures/digits` assets to match the theme and meet the quality of the DOOM/default theme. Ensure every NPC body remains inside its animation frame.

### Output


Completed:

- [x] Added the Hunting theme and mapped Hunter, Deer, and Bear into the startup theme list.
- [x] Added complete Hunting NPC animation folders for idle, walk, attack, pain, and death.
- [x] Generated unique Hunting animation frames with the local deterministic pixel-asset generator.
- [x] Re-created Hunting wall textures, sky, UI screens, and health digits with Hunting-specific palettes.
- [x] Added Hunting-specific forest, cabin, deer-mount, mounted-fish, and separated-paddle compositions to the wall textures.
- [x] Added a blue Hunting sky with the requested 30%-darker bottom gradient.
- [x] Replaced Hunting scenery outputs with a cast-iron stove and oil lantern.
- [x] Added automated checks for dimensions, alpha data, brightness, blank images, clipping, missing animation frames, and duplicate frames.
- [x] Verified the Hunting assets with the repository audit and regression suite.

Not completed and still requiring a dedicated art pass:

- [ ] Hunting scenery still needs the requested leaf and large tree-stump variants in addition to the stove and lantern.
- [ ] Hunter artwork has a readable face, rifle profile, and shooting cue, but does not yet meet the requested detailed forest-hunter quality bar.
- [ ] Pain and death artwork has animation variation, but does not yet meet the requested high-detail wound, bruising, and collapse treatment.
- [ ] The audit does not yet verify semantic object identity, facial anatomy, detached parts, or visual quality equal to Quake.

Auto Commits after last known manual commit `2f142e1`:

- [x] https://github.com/richardharris84/POV-Blaster/commit/9a06c86dd4c6c5a76ea7c52d84d6683311aa92e8 - keep Hunting hunter sprites connected.

Validation completed:

- [x] Hunting UI texture dimensions match the renderer contract, including `sky.png` at 1200x400.
- [x] Hunting digits 0 through 10 are present and nonblank.
- [x] All Hunting NPC animation folders meet their minimum frame counts.
- [x] Current audit reports no blank, clipped, or duplicated Hunting NPC frames.
- [x] Theme generator Python syntax validation passed.
- [x] Full regression suite passed with 27 tests.

⚠️ **PENDING**

## Step 33. Graphics Upgrade

### Prompt

> Bring every playable theme under `resources/` to production-ready visual quality equal to or better than `default`, using the installed Pixel Agents, OpenGame AI Game Generator, Unity, Hootbu Pixel Agent, and Copilot Pixel Agents extensions when available.
>
> Use Pixel-Harmony to compare themes against Default for contrast, brightness, palette consistency, silhouette readability, sprite scale, animation consistency, texture cohesion, visual density, frame dimensions, and alpha quality. Regenerate all non-default theme assets, preserve the asset contract, and audit every texture, UI image, digit, sprite, weapon, scenery asset, and NPC action.
>
> Every NPC must provide meaningful `idle`, `walk`, `attack`, `pain`, and `death` animation. Reject placeholders, generic recolors, detached parts, clipping, unexplained artifacts, duplicate frames, and ambiguous silhouettes. Validate with `python audit_themes.py --check`, tests, builds, runtime smoke tests, and visual review.

### Output

- [x] Added deterministic local pixel/cel-shaded generation in `tools/generate_pixel_assets.py` for Candy Kingdom, Graveyard, Hunting, and Space.
- [x] Regenerated non-default textures, UI screens, digits, scenery, weapons, and NPC animation sets.
- [x] Added role-specific NPC silhouettes and attacks, including the Space paired-headed middle-tier alien inspired by classic retro sci-fi aliens without copying protected artwork.
- [x] Added distinct Space Drone and Overlord silhouettes.
- [x] Added Hunting forest, cabin, deer-mount, mounted-fish, paddle, stove, lantern, bear, deer, hunter, rifle, and blue-gradient artwork.
- [x] Replaced generic NPC pain cross-lines with localized wound clusters, impact cores, bruising, and blood details. Cross-lines are reserved for temporary development/QA indicators only.
- [x] Added role-specific death cues for animals, hunters, supernatural enemies, and science-fiction enemies.
- [x] Integrated image dimensions, aspect ratio, color count, alpha, brightness, blank-image, clipping, duplicate-frame, missing-asset, comparison, and per-theme status reporting into the audit tooling.
- [x] Made generation deterministic across Python processes.
- [x] Removed the redundant `resources/hunting/sprites/animated_sprites/animated_sprites` directory.
- [x] Verified the installed authoring extensions. They provide interactive panels or integrations, not a documented batch PNG export API; no unavailable AI generation was claimed.

Auto Commits after last known manual commit `2f142e1`:

- [x] https://github.com/richardharris84/POV-Blaster/commit/37122dd57b458c1012817595f6fd527d082ca6d9 - production-ready theme upgrade with regenerated and standardized themes.
- [x] https://github.com/richardharris84/POV-Blaster/commit/133d968296d516db051e31a998332f3c4818ba0b - gold-code graphics final status report tooling.
- [x] https://github.com/richardharris84/POV-Blaster/commit/a567b63f8e093a540a646e8aa25a1dd2f54b34bf - production-ready graphics upgrade final status report.
- [x] https://github.com/richardharris84/POV-Blaster/commit/58e5cc511beb7743b1e8b5361fa11ec534b05259 - production-ready graphics upgrade final status report follow-up.

### Validation

- [x] Candy Kingdom, Graveyard, Hunting, and Space pass non-default required asset gates.
- [x] All five themes initialize and render headlessly.
- [x] Full regression suite passes with 29 tests at the latest graphics/web checkpoint.
- [x] Windows executable builds successfully.
- [x] Web bundle builds successfully after including all selectable theme directories.
- [x] Pixel-Harmony-compatible comparisons were run against Default.
- [ ] The generated artwork has not been verified as equal to or better than Quake or Counter-Strike 1.6.
- [ ] A professional high-detail art pass, full interactive playtest, and complete screenshot review remain required before final graphics approval.

⚠️ **PENDING**

## Step 34. Name Curse Word Validation

### Prompt

> Add a regular-expression validator to the startup Player Name prompt. Reject curse words and ask for the name again.

### Output

- [x] Added shared case-insensitive profanity validation in `application/startup.py`.
- [x] Console name entry now reprompts for empty or profane names.
- [x] Web name entry uses the same validator.
- [x] Added regression coverage for rejection and reprompt behavior.
- [x] Full regression suite passes with 29 tests at the latest checkpoint.

✅ **COMPLETE**

## Step 35. Web Menu

### Prompt

> Replicate the console startup menu in the web build game viewport. Analyze the local `pygame-menu`, `pygame-text-input`, and `pygbag` projects. Add a process so console and web startup menus remain synchronized.

### Output

- [x] Added shared startup rules and theme ordering in `application/startup.py`.
- [x] Added an asynchronous Pygame viewport menu in `web_startup.py` for explicit name entry and theme selection.
- [x] Added keyboard, mouse, Enter, Escape, Backspace, Up/Down, and W/S interaction.
- [x] Removed implicit web selection of `Player 1` and the Default theme.
- [x] Fixed web theme and Continue button hitboxes to match their rendered positions.
- [x] Added headless web-menu interaction tests proving shared desktop/web behavior.
- [x] Updated documentation to describe the interactive web startup menu.
- [x] Included all selectable themes in the web bundle instead of excluding non-default themes.
- [x] Updated the web canvas packaging to fill the viewport edge to edge.
- [x] Applied the footer attribution `👨‍💻🧠💡🎮  Richard Harris 💻🛠️✨👾` in the web build template.
- [x] Rebuilt the web bundle and verified the staged Graveyard assets are present.
- [x] Pygbag packaging and local serving were exercised; BrowserFS staging was corrected for the served source directory.
- [x] Linux and macOS native builds remain documented as host-specific work and require their respective operating systems.

✅ **COMPLETE**

## Step 36. Hunting Weapon

### Prompt

> We have redundancy in our weapon folder for hunting theme. Move `C:\Users\Richard\Dropbox\Workspace\Code\Python\POV-Blaster\resources\hunting\sprites\weapon\weapon\shotgun` into `C:\Users\Richard\Dropbox\Workspace\Code\Python\POV-Blaster\resources\hunting\sprites\weapon\shotgun`.

### Output

- [x] Moved the redundant Hunting shotgun asset from the nested `weapon/weapon/shotgun` directory to the expected `resources/hunting/sprites/weapon/shotgun` path.
- [x] Normalized the Hunting weapon asset structure so the theme loader resolves a single canonical shotgun folder.
- [x] Removed the duplicate path ambiguity that could cause theme-asset lookup confusion during startup or builds.
- [x] Kept the asset contract intact for the Hunting weapon sprites and load pipeline.

Validation completed:

- [x] Hunting weapon asset lookup resolves without missing-file or path errors.
- [x] Hunting theme initialization and headless render smoke tests passed.
- [x] No remaining duplicate Hunting weapon directory structure remained in the repo.

✅ **COMPLETE**

## Step 37. Theme adjustment

### Prompt

> Replace hunting 4.png with something like this (still forward facing for ours though):
> https://c7.alamy.com/comp/3D6MWEH/pixel-art-deer-head-with-detailed-antlers-on-blue-background-vector-illustration-3D6MWEH.jpg
>
> Replace hunting npc bear with something like this:
> https://c7.alamy.com/comp/2GDTT96/bear-pixel-art-animal-retro-video-game-cartoon-2GDTT96.jpg
>
> Replace hunting npc hunter with something like this:
> https://www.shutterstock.com/shutterstock/photos/776350228/display_1500/stock-vector-hunter-icon-pixel-art-old-school-computer-graphic-style-games-elements-776350228.jpg
>
> Replace space textures with images that look like this:
> "C:\Users\Richard\Downloads\space"

### Output

- [x] Replaced the Hunting `4.png` texture with a forward-facing deer-head composition inspired by the provided reference while preserving the game’s forward-facing render orientation.
- [x] Replaced the Hunting bear NPC artwork with a retro pixel-art bear silhouette and palette aligned to the forest/cabin theme.
- [x] Replaced the Hunting hunter NPC artwork with a retro pixel-art hunter silhouette using a readable weapon silhouette and a forest-hunting pose.
- [x] Updated the Space theme textures to a dark sci-fi corridor look inspired by the supplied reference folder, while retaining the game’s existing wall-tile convention and renderable surface behavior.
- [x] Kept the theme asset sizing and file conventions aligned with the renderer contract so the art remains valid across all menu and gameplay paths.

Validation completed:

- [x] Hunting and Space textures remain within the expected renderable dimensions and format contract.
- [x] Hunting theme loads successfully through the startup theme selection flow.
- [x] Space theme loads successfully without missing asset errors.
- [x] Visual review confirms the forward-facing deer composition, themed bear/hunter silhouettes, and sci-fi space look are aligned with the requested mood and structure.

✅ **COMPLETE**

## Step 38. Production Graphics Gate

### Output

- [x] Audited all five playable themes with required dimensions, nonblank, alpha, clipping, duplicate-frame, and animation checks.
- [x] Repaired Hunting hunter frame geometry so the rifle remains attached and every non-death frame stays inside its canvas.
- [x] Confirmed each NPC has meaningful `idle`, `walk`, `attack`, `pain`, and `death` animation folders.
- [x] Confirmed all themes are ready for automated play testing: Candy Kingdom, Space, Hunting, Graveyard, and Doom.
- [ ] A professional art-direction review against Quake or Counter-Strike 1.6 remains outside automated validation.

⚠️ **PENDING**

## Step 39. Gameplay HUD and Minimap

### Output

- [x] Added the player kill counter in the top-right using each theme's digit textures.
- [x] Preserved kills across level completion and theme changes; reset kills only when the player dies.
- [x] Added Caps Lock minimap toggling during gameplay.
- [x] Added regression coverage for kill persistence and minimap toggling.

✅ **COMPLETE**

## Step 40. Default Theme Selection

### Output

- [x] Kept Doom as menu option 5 and preserved blank console selection as Doom for compatibility.
- [x] The web menu starts with an explicit first-theme highlight and requires name/theme confirmation rather than silently starting a game.
- [x] Covered the shared selection behavior with startup tests.

✅ **COMPLETE**

## Step 41. Mobile Controls

### Output

- [x] Added mobile and browser touch detection.
- [x] Added isolated left and right virtual joystick axes for movement and turning.
- [x] Added tap-to-shoot outside the joystick zones.
- [x] Added touch startup-menu interaction coverage.

Auto Commits after last known manual commit `2f142e1`:

- [x] https://github.com/richardharris84/POV-Blaster/commit/7bd3ca6a1a45221c39223bd734f1cd59757d47a3 - support mobile browser name entry.

Validation completed:

- [x] Desktop and phone-sized browser viewports load the deployed game.
- [x] Desktop name entry, Doom selection, Enter confirmation, and gameplay were exercised on GitHub Pages.
- [ ] Physical-device touch play testing remains required; browser emulation does not replace a real phone or tablet test.

⚠️ **PENDING**

## Step 42. Clean Architecture Refactor

### Output

- [x] Kept domain rules isolated from Pygame and infrastructure concerns.
- [x] Kept application orchestration separate from presentation and runtime adapters.
- [x] Kept build and audit tooling outside the application layers.
- [x] Validated the architecture with the full regression suite and headless rendering tests.

Auto Commits after last known manual commit `2f142e1`:

- [x] https://github.com/richardharris84/POV-Blaster/commit/21e68aa2a1829661fd563389409c028565173510 - mobile startup touch fix, workflow email notification, and architecture file relocation.

✅ **COMPLETE**

## Step 43. Release Documentation and Deployment

### Output

- [x] Updated the release record with Steps 38-43 and per-theme play-test readiness.
- [x] Updated web build documentation for black letterboxing around the fixed-aspect canvas.
- [x] Pages deployment run `32738819389` completed successfully for the graphics release.
- [x] SMTP notification completed successfully for that Pages deployment.
- [ ] CI run `32738820065` remains the final graphics-release gate to verify.

Auto Commits after last known manual commit `2f142e1`:

- [x] https://github.com/richardharris84/POV-Blaster/commit/242fa6d6d04477bcd1320320ac62e8774d2db41f - gold-code theme pass with minimap and HUD.
- [x] https://github.com/richardharris84/POV-Blaster/commit/e70e25a535af3663c2389c4fb493d6c68ed59d98 - fallback sender for deploy notification email.
- [x] https://github.com/richardharris84/POV-Blaster/commit/e92da9315f9119a761a3f72bfb24e5ebbb4d8378 - explicit sender for deploy email notification.
- [x] https://github.com/richardharris84/POV-Blaster/commit/67b43733eddc8fd4f2daf7e5c567257c7d830f2b - skip notify job when SMTP secrets are missing.
- [x] https://github.com/richardharris84/POV-Blaster/commit/720c8359b8654e1fa0074c3fbbfcd2824549900d - make notification step non-blocking.
- [x] https://github.com/richardharris84/POV-Blaster/commit/4d1ca93105d5106b641052e052158376ba32bd31 - use black web letterboxing.
- [x] https://github.com/richardharris84/POV-Blaster/commit/ff80fd376516c5339eaf45cd5cd7df265e0305a0 - normalize changelog steps and fix SMTP TLS.

Final release status: automated graphics and gameplay gates pass; production art approval and physical mobile play testing remain open before declaring gold-code complete.

⚠️ **PENDING**

## Step 44. Workspace Root Cleanup

### Prompt

> Role: Act as a Senior Software Engineer & Architect refactoring this Python/Pygame codebase toward cleaner architecture, better maintainability, and production-quality project organization.
>
> Task: Clean up the workspace root so it is as bare as practical while preserving all current desktop, web, build, test, audit, and GitHub Pages behavior.
>
> Requirements:
> - Rename `resources/` to `assets/`.
> - Move `maps/` to `assets/maps/`.
> - Move `content/levels/` to `assets/levels/`.
> - Move `application/`, `domain/`, `infrastructure/`, and `presentation/` into `src/` while preserving root commands such as `py main.py`, `py build.py --web`, and the existing test command.
> - Move `generate_themes.ps1` into `tools/`.
> - Move or ignore `pygbag*.log` files.
> - Treat `scores.xml` as mutable runtime data and move it to `data/` if score persistence remains reliable.
> - Update code, tests, build scripts, CI, README, CodeBase, CodeAudit, and CHANGELOG references.
> - Validate with compile checks, tests, theme validation/audit, web build, stale-reference search, and `git diff --check`.

### Output

- [x] Created `src/` and moved the importable source packages under it: `application/`, `domain/`, `infrastructure/`, and `presentation/`.
- [x] Kept `main.py` and `build.py` at the workspace root as thin entry/build points.
- [x] Added root/bootstrap path handling so `main.py`, tests, tools, PyInstaller, and the Pygbag wrapper can import packages from `src/`.
- [x] Renamed `resources/` to `assets/` and preserved all playable theme folders under `assets/themes/<theme>/`.
- [x] Moved `maps/1_mini_map_default.txt` to `assets/maps/1_mini_map_default.txt`.
- [x] Moved `content/levels/1_mini_map_default.json` to `assets/levels/1_mini_map_default.json`.
- [x] Updated map loading and spawn-config loading to read from `assets/maps/` and `assets/levels/`.
- [x] Updated asset root configuration so theme assets resolve from `assets/`.
- [x] Updated PyInstaller packaging to bundle `assets/` as the runtime content tree.
- [x] Updated Pygbag packaging to copy `src/` and `assets/` into `build/web-source` and write a browser wrapper that bootstraps `src/`.
- [x] Moved `generate_themes.ps1` to `tools/generate_themes.ps1` and updated CI plus script root detection.
- [x] Moved `scores.xml` to `data/scores.xml` and updated `HighScores` default persistence to use `data/`.
- [x] Moved existing `pygbag*.log` files under `logs/` and added explicit ignore coverage for generated logs.
- [x] Kept `tests/` and `tools/` at the root as standard non-application project support folders.
- [x] Updated `README.md`, `docs/CodeBase.md`, `docs/CodeAudit.md`, and status tooling to describe `src/`, `assets/`, `data/`, and moved tooling.
- [x] Verified active references no longer point to the removed root `resources/`, `maps/`, `content/levels`, or root `generate_themes.ps1` paths.

Final root layout:

```text
POV-Blaster/
├── assets/
├── data/
├── docs/
├── logs/
├── screenshots/
├── src/
├── tests/
├── tools/
├── .github/
├── build.py
├── main.py
├── requirements.txt
├── README.md
└── CHANGELOG.md
```

Validation completed:

- [x] `py -m compileall -q main.py build.py src tests tools` passed.
- [x] `py -m unittest discover -s tests -p 'test_*.py' -v` passed with 36 tests.
- [x] `./tools/generate_themes.ps1 -ValidateOnly` passed.
- [x] `py tools\audit_themes.py --check` passed.
- [x] `py build.py --web` completed successfully and produced `build/web`.
- [x] `py build.py --windows` completed successfully and produced `build/POV-Blaster_win.exe`.
- [x] Active stale-reference sweep passed for removed root paths.
- [x] Workspace diagnostics reported no errors.
- [x] `git diff --check` passed; Git only warned that `build.py` line endings may normalize from LF to CRLF next time Git touches it.

✅ **COMPLETE**

## Step 45. Theme Assets Folder

### Prompt

> Move `candy_kingdom`, `default`, `graveyard`, `hunting`, and `space` into a new sub-folder called `themes`. Update source code to reflect the change.

### Output

- [x] Moved all five playable themes into `assets/themes/`.
- [x] Kept shared map and level content in `assets/maps/` and `assets/levels/`.
- [x] Added a dedicated `THEME_DIR` setting and updated theme resource resolution.
- [x] Updated theme generation, pixel-asset generation, and theme-audit tooling to use `assets/themes/`.
- [x] Updated asset-path tests and project documentation for the new layout.

Validation completed:

- [x] Full Python compilation passed.
- [x] Full regression suite passed with 36 tests.
- [x] `tools/generate_themes.ps1 -ValidateOnly` passed.
- [x] `tools/audit_themes.py --check` passed against `assets/themes/`.
- [x] `build.py --web` completed successfully and staged all five themes.
- [x] No stale direct `assets/<theme>` references remain.
- [x] Workspace diagnostics and `git diff --check` passed.

✅ **COMPLETE**

## Step 46. Game Icon

### Prompt

> Change game icon from pygame default to something that looks like doom guy.

### Output

- [x] Added an original 64x64 pixel-art marine face at `assets/icon.png`.
- [x] Applied the custom icon to desktop Pygame windows.
- [x] Applied the custom icon to the browser Pygame display.
- [x] Replaced the generated browser favicon with the same project-owned icon.
- [x] Added a regression test for Pygame icon application.

Validation completed:

- [x] Focused icon regression test passed.
- [x] Full regression suite passed with 37 tests.
- [x] Browser build completed successfully.
- [x] Web output contains `favicon.png` and references it from `index.html`.
- [x] Touched-file diagnostics and `git diff --check` passed.

✅ **COMPLETE**

## Step 47. Project Description Review

### Prompt

> Based on the project Markdown files, evaluate this description:
>
> A cross-platform, retro FPS game engine, built in Python, developed solely
> using Copilot other than the initial fork's codebase (see CHANGELOG). It
> replicates 90s pseudo-3D graphics (e.g., Wolfenstein 3D). It utilizes a
> custom raycasting algorithm to project 2D grid maps into textured 3D
> perspectives in real time (RC since BSP suited for C/C++).

### Output

The description was broadly accurate, with several claims qualified for
technical precision:

- Described the project as a retro FPS built on a custom raycasting renderer,
	rather than overstating it as a general-purpose engine.
- Replaced the difficult-to-prove claim that development was performed
	"solely" using Copilot with the more defensible description of extensive
	Copilot-assisted development documented in the changelog.
- Identified the visuals as Wolfenstein 3D-inspired textured pseudo-3D views.
- Specified the renderer as a custom DDA raycasting renderer over 2D grid maps.
- Clarified that raycasting fits this grid-based project because of its
	simplicity, rather than claiming BSP is unsuitable for Python or limited to
	C/C++.

Recommended description:

> A cross-platform retro FPS game built in Python and Pygame, evolved from an
> initial DOOM-style fork through extensive Copilot-assisted development
> documented in the CHANGELOG. It recreates Wolfenstein 3D-inspired pseudo-3D
> visuals using a custom DDA raycasting renderer that projects 2D grid maps
> into textured first-person views in real time. Raycasting was chosen for its
> simplicity and suitability for the project's grid-based design, rather than
> using a more complex polygonal or BSP-based rendering approach.

✅ **COMPLETE**

<!-- AUTOMATED 72-HOUR SYNC:START -->
## Automated 72-Hour Sync

Generated: 2026-08-27T12:09:07-04:00 (window: last 72 hours)

### Git Commits

- `ddfd146` (2026-08-27) Auto Refactor
- `66958e1` (2026-08-27) Deploy GitHub Pages
- `c3d4391` (2026-08-27) Add map selection, sharpen theme HUD digits, tune death animations, and asset fallback
- `f2e65d2` (2026-08-26) Complete recent prompt work and changelog sync
- `ee2177f` (2026-08-26) Finalize Copilot policy and web footer
- `412bc48` (2026-08-26) Add inactive gate to Copilot policy
- `1d15f0e` (2026-08-26) Generalize block auto-pilot prompt
- `72fc549` (2026-08-26) Fix desktop controls and web footer emojis
- `241a1fd` (2026-08-26) Add footer emoji styling
- `977e21e` (2026-08-26) Bold Auto-pilot activation command
- `662fd85` (2026-08-26) Add Auto-pilot disable command
- `cc4b2e4` (2026-08-26) Auto-Pilot
- `fece0aa` (2026-08-26) Add optional Auto-pilot workflow
- `19019c8` (2026-08-26) Fix responsive web name input
- `c0ca702` (2026-08-26) Fix browser startup name entry fallback
- `2445b12` (2026-08-26) Add browser name sync fallback
- `b039225` (2026-08-26) Handle unfocused web name input typing
- `8963d6f` (2026-08-26) Add web name typing fallback
- `654eacb` (2026-08-26) Merge pull request #3 from richardharris84/copilot/fix-github-actions-job-failure
- `7d789ff` (2026-08-26) Rework browser name input overlay
- `a4cd9e1` (2026-08-26) Repair failing theme assets
- `d4ed4bf` (2026-08-26) Exercise browser input fallback path
- `4cf0a97` (2026-08-26) Guard final browser input cleanup
- `fadf3b5` (2026-08-26) Refine browser input fallback safety
- `c7aaf02` (2026-08-26) Stabilize browser input regression test
- `dd0678c` (2026-08-26) Harden browser name input handling
- `9f8d84e` (2026-08-26) Tighten browser input cleanup
- `4f78b96` (2026-08-26) Fix web startup input handling
- `bdb777f` (2026-08-26) Add gameplay project highlights
- `4bce238` (2026-08-26) Expand project highlights
- `56eb651` (2026-08-26) Document project highlights
- `59833a8` (2026-08-26) fix: resolve theme audit CI failures in candy_kingdom, graveyard, and space themes
- `1f5bbae` (2026-08-26) Themes Completed
- `89af429` (2026-08-26) Update remaining theme character assets
- `0c4fcdc` (2026-08-26) Fix mobile tap firing and web theme default
- `593c38e` (2026-08-26) Refresh hunting hunter and shotgun assets
- `fbd955b` (2026-08-26) REAME.md
- `a7cb3c3` (2026-08-26) Fix mobile name input bug, default theme to Doom, double minimap size, README updates
- `4f17fff` (2026-08-25) Merge pull request #2 from richardharris84/copilot/pov-blaster-update
- `905949f` (2026-08-26) Add Hello World line to README
- `f3ffa73` (2026-08-25) Merge pull request #1 from richardharris84/copilot/research-task-orientation
- `fa73bc8` (2026-08-26) docs: add quick orientation section to CodeBase.md
- `414f70a` (2026-08-25) Fixed Architecture Diagrams
- `19717d7` (2026-08-25) Update docs, mobile controls, and release assets
- `f9afb24` (2026-08-25) Deploy GitHub Pages
- `3cdfde3` (2026-08-25) Deploy GitHub Pages
- `45c0b89` (2026-08-25) Add GH Pages deploy to build.py
- `e69a0ac` (2026-08-25) Architecture Diagrams
- `9b0856d` (2026-08-24) Normalize project documentation and changelog
- `2b6e182` (2026-08-24) Replace XML scores with local SQLite and sync support
- `3423fbe` (2026-08-24) Refine web startup footer and mobile turning
- `0bfe769` (2026-08-24) Document API database and deployment configuration
- `fe813b7` (2026-08-24) Update Psycopg for Python 3.14
- `9458493` (2026-08-24) Use API-only dependencies on Render
- `31b9777` (2026-08-24) Use free Render service with external Postgres
- `2efe030` (2026-08-24) Use Render Postgres for hosted score storage
- `d676d1b` (2026-08-24) Gold Code: Complete API integration with database, web session tracking, and deployment pipelines
- `9c33c07` (2026-08-24) Richard's Architecture - Themes
- `b33e246` (2026-08-24) Richard's New Architecture
- `ff80fd3` (2026-08-24) docs: normalize changelog steps and fix smtp tls
- `7bd3ca6` (2026-08-24) feat: support mobile browser name entry

### Prompt Files Changed

- [`.github/prompts/auto-pilot.prompt.md`](.github/prompts/auto-pilot.prompt.md)
- [`.github/prompts/block-auto-pilot.prompt.md`](.github/prompts/block-auto-pilot.prompt.md)

### Copilot Prompt/Output Excerpts

- No session log supplied; pass `--session-log <path>` to include excerpts.

<!-- AUTOMATED 72-HOUR SYNC:END -->
