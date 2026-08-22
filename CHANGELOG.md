# DOOM style 3d (raycasting) game in Python (based on Wolfenstein 3d)

Control: 'WASD' + mouse

![doom](/screenshots/0.jpg)

## Step 1. Create the Repository

### Prompt

> Create a new Repo in my GitHub (https://github.com/richardharris84) called POV-Blaster which is a fork of https://github.com/StanislavPetrovV/DOOM-style-Game. It will be stored in C:\Users\Richard\Dropbox\Workspace\Code\Python on my local machine.

### Output

Completed end-to-end.

- Created a fork of `StanislavPetrovV/DOOM-style-Game` in the `richardharris84` GitHub account.
- Renamed the fork to `POV-Blaster`.
- Cloned it locally to `C:\Users\Richard\Dropbox\Workspace\Code\Python\POV-Blaster`.
- Configured the local remotes:
	- `origin`: `https://github.com/richardharris84/POV-Blaster.git`
	- `upstream`: `https://github.com/StanislavPetrovV/DOOM-style-Game.git`

Repository: https://github.com/richardharris84/POV-Blaster

## Step 2. How-To create the Code Base

### Prompt

> Background: This project is a fork we just created of https://github.com/StanislavPetrovV/DOOM-style-Game.
>
> Role: Act as a Senior Software Engineer building a production quality video game.
>
> Task: Reverse engineer this project's code and create a step by step guide on how to re-create this project. The report will be a Markdown file called CodeBase.md. The intended audience will be Junior Developer who is new to Python programming and needs to know everything required to take over the project.

### Output

Created the complete reconstruction guide in [CodeBase.md](docs/CodeBase.md).

The guide covers:

- Python and Pygame setup.
- Project structure and module responsibilities.
- The game loop and object relationships.
- Raycasting, rendering, sprites, NPC AI, and pathfinding.
- Weapon, audio, health, victory, and game-over behavior.
- Asset requirements and recreation order.
- Recommended tests and production hardening tasks.

Validation completed:

- Markdown diagnostics reported no errors.
- Python 3.13 compile check passed.
- Only `CodeBase.md` was added before this README update.

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

- Critical and high-priority correctness, stability, and performance findings.
- Rendering, raycasting, sprite scaling, depth handling, and pathfinding bottlenecks.
- Asset loading, audio lifecycle, timing, spawning, and game-state risks.
- Clean Architecture boundaries for domain, application, infrastructure, and presentation layers.
- A scalable target folder structure and file-by-file refactoring plan.
- A staged migration roadmap, testing strategy, CI baseline, and production checklist.
- Client, content, and service architecture considerations for supporting millions of users.

Validation completed:

- Markdown diagnostics reported no errors.
- `git diff --check` reported no formatting errors.

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

Created the detailed comparison report in [CloneCompare.md](docs/CloneCompare.md).

The report covers:

- Git remotes, commit chronology, source hashes, and asset layout comparison.
- Evidence that `DOOM-3D-FPS-Shooting-Game` is derived from `DOOM-style-Game` despite separate Git histories.
- Gameplay and implementation differences between the two projects.
- Code-quality, correctness, architecture, and runtime asset risks.
- Rendering, raycasting, sprite, NPC, and pathfinding bottlenecks.
- A focused first-patch plan for POV-Blaster.
- Clean Architecture boundaries and a suggested target folder structure.
- Current-to-target file mapping, testing requirements, and upgrade gates.
- Quality, scalability, maintainability, content, and distribution recommendations.

Validation completed:

- Markdown diagnostics reported no errors.
- Both comparison projects remained unmodified.

## Step 5. Organize Docs

### Prompt

> Task:
> - Move CodeBase.md, CodeAudit.md, and CloneCompare.md to a docs folder.
> - Fix folder name of sreenshots to screenshots. Update README.md accordingly.
> - Rename our existing README.md to CHANGELOG.md.
> - Copy README.md from DOOM-3D-FPS-Shooting-Game, but change any text and remove any images accordingly based on CodeAudit.md and CodeBase.md and CodeCompare.md to reflect this project's code. Reminder, this project is a direct fork of DOOM-style-Game. Under the Table of Contents, add a See Also section with links to our existing docs.

### Output

Organized the project documentation and assets:

- Moved the three reports into `docs/`.
- Renamed `sreenshots/` to `screenshots/`.
- Preserved the previous project README as `CHANGELOG.md`.
- Created a new POV-Blaster-specific README based on the related project’s structure.
- Removed copied demonstration images and updated the README to describe this fork’s actual code and `resources/` assets.
- Added a See Also section linking to the reconstruction, audit, and clone-comparison reports.
- Updated stale documentation links and screenshot references.

Validation completed:

- All documentation diagnostics reported no errors.
- All expected documentation and screenshot paths exist.
- No stale active links or `sreenshots` references remain.

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

- Added `screenshots/gameplay_1.gif` above the Controls section.
- Added the source project's unique gameplay, raycasting, sprite, weapon, pathfinding, and enemy demonstration images.
- Added a table of contents and a development walkthrough with applicable explanations for each gameplay system.
- Documented the source-code similarity findings from `docs/CloneCompare.md`.
- Resized the three Static and Animated Sprites sample images to a consistent `126px` width, matching the approximate enemy-image scale while preserving aspect ratios.
- Kept the larger decorated-environment gameplay image unchanged.

Validation completed:

- All README image references resolve to existing files.
- Markdown diagnostics reported no errors.
- `git diff --check` reported no formatting errors.

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

- Corrected frame timing and display presentation order.
- Added non-blocking `playing`, `victory`, and `game_over` states.
- Added bounded frame delta handling.
- Added project-relative resource paths using `pathlib`.
- Added deterministic animation frame ordering.
- Added raycasting epsilon guards for near-axis rays.
- Removed stale pathfinding caching.
- Clamped player health and hardened HUD rendering.
- Added unique NPC spawn locations and spawn-capacity validation.
- Added reliable round reset behavior.
- Added improved audio resource path handling.

Validation completed:

- Full Python `compileall` check passed.
- Headless Pygame startup passed.
- Headless update and draw cycle passed.
- Victory-to-new-round transition passed.
- Smoke test created 20 NPCs and 816 render entries successfully.
- Source diagnostics and `git diff --check` passed.

The interactive game loop was not left running during validation because it is intentionally an infinite desktop application loop. Non-fatal PNG color-profile warnings were observed while loading existing assets.

## Step 8. Patch #1.1

### Prompt

> Perform a full review of our patch.  Upon QA, the change seems to have broken solider death. Also, fix all the libpng warning messages in the Terminal.

### Output

Completed the patch QA review and fixes:

- Identified the soldier death regression in `sprite_object.py`.
- Corrected the animation loader so it accepts filenames such as `POSSM0.png` through `POSSU0.png`.
- Added deterministic sorting using trailing frame numbers and stable filename ordering.
- Verified Soldier, Cacodemon, and Cyberdemon death animations load correctly.
- Re-encoded all 111 runtime PNG files with problematic color-profile metadata removed.
- Preserved image dimensions, RGBA data, and gameplay visuals.

Validation completed:

- Soldier death regression test passed.
- All enemy death frame sequences loaded and advanced correctly.
- Headless Pygame startup and update/draw smoke test passed.
- Full Python compilation passed.
- Editor diagnostics passed.
- Fresh runtime output reported no `libpng` warnings.

## Step 9. POC Features

### Prompt

> Task:
> - Compare my earlier Proof-of-Concept (`C:\Users\Richard\Dropbox\Workspace\Code\Python\DOOM-3D-FPS-Shooting-Game_KidCopy`) to `C:\Users\Richard\Dropbox\Workspace\Code\Python\DOOM-3D-FPS-Shooting-Game`. Create a report in docs called POCFeatures.md. Outline what the main changes I did to _KidCopy and what packages I installed to implement them.

### Output

Created the detailed POC comparison report in [POCFeatures.md](docs/POCFeatures.md).

The report covers:

- ☑ Confirmed runtime/build packages: `pygame` and `PyInstaller`.
- ☑ PyInstaller executable build support.
- ☑ Mouse activation and Pygame event filtering. 
- ☑ Image caching, fallback graphics, and silent audio handling.
- ☐ Theme selection and theme-specific asset routing. 
- ☐ Generatee themed content and asset tooling.
- ⦸ Damage-based NPC scaling and themed enemy behavior.
- ⦸ Documentation, planned web/multiplayer work, and production limitations.
- ⦸ PowerShell/.NET `System.Drawing` tooling and Python standard-library usage.
- ⦸ Packages not confirmed as KidCopy dependencies, including Pillow, Flask, FastAPI, Requests, NumPy, and OpenGL.
- ☐ Recommended architecture and migration steps for POV-Blaster.

Validation completed:

- Markdown diagnostics reported no errors.
- Report references were checked and misleading workspace-relative links were removed.
- No source code was changed in POV-Blaster for this documentation task.

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

- Added [build.py](build.py) using PyInstaller.
- Added `pygame` and `pyinstaller` to [requirements.txt](requirements.txt).
- Bundled the complete `resources/` directory into each executable.
- Added `-w`/`--windows` and `-l`/`--linux` command-line targets.
- Generated `build/POV-Blaster_win.exe` on Windows.
- Generated a native Linux ELF executable at `build/POV-Blaster_lin` through WSL Ubuntu 22.04.
- Added native-platform guards so Windows builds run on Windows and Linux builds run on Linux/WSL.
- Added a Python shebang, Unix line endings, and executable permissions so WSL can run `./build.py -l` directly.
- Added WSL display detection that discovers the default gateway, tests VcXsrv on port `6000`, selects SDL X11, and clears inherited Wayland settings when VcXsrv is available.
- Added window positioning at `0,0` for X11/VcXsrv so the game is not created off-screen.
- Confirmed the previous VcXsrv issue: the game window was mapped at approximately `1600x900+1928+91`; the corrected window maps at `1600x900+0+0`.
- Updated `README.md` with separate Windows and Linux run/build instructions, expected artifact names, WSLg/VcXsrv guidance, and the native-build limitation.

Validation completed:

- PyInstaller 6.22.2 installed and verified on Windows and WSL.
- Windows build completed successfully.
- Linux build completed successfully through WSL.
- Linux artifact verified as an executable x86-64 ELF binary.
- Headless Pygame startup and frame rendering passed.
- Native WSLg Wayland source rendering passed.
- VcXsrv X11 connectivity passed with a minimal Pygame window.
- POV-Blaster source selected `DISPLAY=172.19.64.1:0` and SDL `x11` automatically under WSL.
- Rebuilt Linux executable mapped as a visible X11 window at `0,0` under VcXsrv.
- README, build script, and requirements diagnostics passed.

Known platform limitation: PyInstaller produces native binaries for the host operating system. A Linux build must be created on Linux or WSL, and a Windows build must be created on Windows. WSLg or VcXsrv must be running for a Linux graphical window to appear.

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

- Confirmed WSL2 Ubuntu 22.04 and WSLg were installed and exposing Wayland, X11, and PulseAudio.
- Confirmed VcXsrv was running and listening on Windows port `6000`.
- Verified a minimal Pygame window through VcXsrv using SDL X11.
- Found the game window was being mapped off-screen at approximately `1600x900+1928+91`.
- Updated `main.py` to position X11/VcXsrv windows at `0,0`.
- Added WSL default-gateway detection so the game can automatically select the reachable VcXsrv display instead of inheriting WSLg `DISPLAY=:0`.
- Added native Wayland fallback when VcXsrv is unavailable.
- Rebuilt `build/POV-Blaster_lin` through WSL after each display fix.
- Found the mouse right-turn bug was caused by cursor recentering before reading relative motion; VcXsrv reported the synthetic cursor warp as rightward movement.
- Updated `player.py` to read real relative motion before recentering and discard synthetic warp motion.
- Reduced mouse sensitivity and removed the incorrect frame-time multiplier so turning is frame-rate independent.
- Replaced unreliable X11/VcXsrv `pygame.mouse.get_rel()` handling with signed `pygame.MOUSEMOTION` event deltas.
- Added mouse-motion accumulation and forwarded signed motion events from `main.py` to `player.py`.
- Disabled cursor warping on the X11/VcXsrv path while preserving mouse capture.
- Set `LINUX_MOUSE_SENSITIVITY` to `0.003` while leaving other platform sensitivity unchanged.

Validation completed:

- Automatic WSL display selection reported `DISPLAY=172.19.64.1:0` and SDL `x11`.
- Native Wayland source rendering passed under WSLg.
- VcXsrv X11 connectivity passed with a minimal Pygame window.
- Rebuilt game window mapped at `1600x900+0+0` under VcXsrv.
- Left and right mouse movement boundary tests passed.
- Signed left/right mouse-motion event test passed.
- Linux sensitivity value test passed.
- Rebuilt Linux executable smoke tests passed with no stderr.
- Full Python compilation and source diagnostics passed.

Known environment requirement: when using VcXsrv, it must be running with X11 access enabled. WSLg and VcXsrv are alternative display providers; the game now prefers reachable VcXsrv under WSL and falls back to Wayland when appropriate.

## Step 12. Game Window Focus

### Prompt

> Implement Mouse activation and Pygame event filtering.

### Output

Implemented mouse activation and event filtering for the active gameplay window:

- Added a mouse-activation gate so input is only processed after the game window is truly active.
- Ignored stale motion and startup noise before activation.
- Restored capture and re-centering when the window regains focus.
- Kept the Linux/WSL and Windows input paths compatible with the existing platform-specific handling.

Validation completed:

- Fresh Python compilation passed for `main.py`, `player.py`, and `settings.py`.
- The input changes were kept compatible with the existing display backend logic.
- The game continued to run cleanly after the focus-handling update.