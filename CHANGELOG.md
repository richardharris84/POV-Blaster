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

## Recommended architecture and migration steps for POV-Blaster.

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
- ☑ Theme selection and theme-specific asset routing. 
- ☑ Generatee themed content and asset tooling.
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

## Step 13. Asset Caching and Fallback Graphics

### Prompt

> Implement image caching and fast loading fallback graphics.

### Output

Implemented image caching and fast-loading fallback graphics for missing or unavailable assets.

Current branch state (post-branch correction):

- `main` is the active integration branch and includes the recent Step 13 onward work through commit `99cc77a` (`Minor content change`).
- `develop` is intentionally pinned to the graphics rollback baseline at commit `fe2f064` (`Graphics Upgrade Rollback`).
- The former `develop` tip was preserved as safety branch `backup/develop-2026-08-22` before branch pointers were adjusted.

Validation completed:

- Cached images load without repeated disk reads.
- Fallback graphics allow the game to continue when an image asset is unavailable.
- Headless startup and rendering smoke tests passed.

## Step 14. Theme Selection and Theme-Specific Asset Routing

### Prompt

> Implement Theme selection and theme-specific asset routing.
>
> - Move all current resources into a `resources/default` theme folder.
> - Add a startup choice for Default or Exit.

### Output

Implemented the initial theme system:

- Moved all existing assets under `resources/default`.
- Added a startup menu with `Default [Soldier, Caco Demon, Cyber Demon]` and `Exit` choices.
- Routed textures, sprites, weapon assets, NPC assets, and audio through the selected theme.
- Added a theme abstraction so additional resource folders can be added later.

Validation completed:

- Python compilation passed for all theme-aware modules.
- Default theme asset path resolution passed.
- Startup menu selection and Exit behavior passed.
- Headless startup smoke test passed.

## Step 15. Themed Content and Asset Tooling

### Prompt

> Create the ability to generate themed content and asset tooling.
>
> Create Candy Kingdom, Space, and Graveyard themes with their requested enemies and suitable death animations.

### Output

Added three generated themes:

- Candy Kingdom: Marshmallow Man, Springfield Doughnut, Gingerbread Golem.
- Space: Alien Drone, Alien Warrior, Alien Overlord.
- Graveyard: Ghost, Vampire, Werewolf.

Added `generate_themes.ps1` to generate theme textures and unique numbered NPC animation frames. Every generated NPC includes idle, walk, attack, pain, and death animations. Candy Kingdom death sequences depict melting for the Marshmallow Man and crumbling for the Springfield Doughnut and Gingerbread Golem.

Validation completed:

- All nine new NPCs have complete animation folder structures.
- Every generated NPC has six distinct death frames and unique regular animation frames.
- Default, Candy Kingdom, Space, and Graveyard headless startup and rendering passed.

## Step 16. Candy Kingdom Asset Refresh

### Prompt

> Modify Candy Kingdom using the assets already created in `DOOM-3D-FPS-Shooting-Game_KidCopy/resources/themes/CandyKingdom`.

### Output

Replaced the generated Candy Kingdom assets with the existing 119-file CandyKingdom asset set. The imported content includes the Marshmallow Man, Springfield Doughnut, and Gingerbread Golem animation frames, Candy Kingdom scenery, pastry-bag weapon, and frosting squeeze sound. Theme metadata now routes Candy Kingdom to its pastry-bag weapon and themed firing sound.

Validation completed:

- Candy Kingdom compiled and started through the full headless game path.
- A Candy Kingdom frame rendered successfully.
- All three Candy Kingdom NPCs contain six-frame death animations.
- Candy-specific weapon and audio assets resolved successfully.
- Duplicate nested asset directories were removed.

## Step 17. Candy Kingdom Weapon Sound

### Prompt

> Set the Candy Kingdom weapon sound to `floraphonic-thick-slime-18-229584.mp3`.

### Output

Updated Candy Kingdom theme routing so the pastry-bag weapon uses the Floraphonic thick slime MP3 sound.

Validation completed:

- The configured MP3 exists in the Candy Kingdom sound assets.
- Candy Kingdom headless startup and audio loading passed.

## Step 18. Animation Validation and Repair

### Prompt

> In addition to death frame validation, validate attack, pain, and walk frames and generate a new image when required.

### Output

Extended `generate_themes.ps1` with animation validation for idle, attack, pain, walk, and death sequences. The validator checks minimum frame counts and detects missing numbered frames and duplicate image content using SHA-256 hashes. Existing assets can be checked without modification with `-ValidateOnly`; generated replacements require the explicit `-RepairFrames` option.

Validation completed:

- Duplicate Candy Kingdom idle and walk frames were detected; repairs are now opt-in so imported artwork is not silently replaced.
- Attack, pain, walk, and death validation passed for all generated themes.
- Candy Kingdom headless startup and rendering remained successful after repairs.

## Step 19. Candy Kingdom Asset Restoration

### Prompt

> Right now our `candy_kingdom` theme is broken. It is a weird blend of the provided theme and an egg-like character. Re-apply the assets from `C:\Users\Richard\Dropbox\Workspace\Code\Python\DOOM-3D-FPS-Shooting-Game_KidCopy\resources\themes\CandyKingdom` to this project's `candy_kingdom` theme.

### Output

Re-applied the original KidCopy CandyKingdom asset set to `resources/candy_kingdom`, removing the procedurally generated replacement artwork. Updated the asset validator so imported artwork is not modified during read-only validation; frame repairs now require the explicit `-RepairFrames` option.

- Repair mode now also preserves the restored Candy Kingdom artwork; it reports its imported frame issues without replacing those assets. Procedural repairs remain available for the generated themes.

Validation completed:

- Candy Kingdom assets match the specified source files byte-for-byte.
- Candy Kingdom startup and rendering passed.
- Read-only animation validation completed without modifying artwork.

## Step 20. Health Percent

### Prompt

> Fix `10.png` within `textures/digits` of the new themes. That is meant to be a `%`.
>
> In the startup menu, rename `Default` to `DOOM` and put it in the fourth position.
>
> The `10.png` texture should match its theme, not be a copy from Default.

### Output

- Fixed the health suffix texture so `10.png` renders as `%` in Candy Kingdom, Space, and Graveyard.
- Generated theme-specific percent textures using each theme's accent color instead of copying the DOOM/default texture.
- Improved the percent texture proportions and vertical alignment so the health indicator reads as a cohesive `100%` display.
- Renamed the startup menu's `Default` theme to `DOOM` and moved it to menu position 4.

Validation completed:

- All theme percent textures are 64x64.
- Candy Kingdom, Space, and Graveyard percent textures have distinct content from the DOOM/default texture.
- Menu option 4 selects the `DOOM` theme successfully.
- `git diff --check` passed.

## Step 21. Architecture

### Prompt

> Recommended architecture and migration steps for POV-Blaster.
>
> Iteratively work on each item in `Recommendations.md`. You can choose the order of priority, but provide frequent progress updates about the current work.

### Output

Implemented and validated the local modular-monolith architecture migration:

- Separated pure health, movement, combat, and game-state rules into `domain/` modules.
- Added explicit typed ports for game context, rendering, assets, audio, and input.
- Organized runtime ownership across `domain/`, `application/`, `infrastructure/`, `presentation/`, and `tools/`.
- Moved image caching into per-game `AssetLoader` instances and removed the global image cache.
- Added immutable render snapshots and deterministic seeded NPC layouts.
- Added depth-buffer-backed sprite occlusion.
- Added headless smoke tests, domain-boundary tests, CI configuration, and profiling support.
- Replaced wildcard imports with explicit dependencies.
- Checked off the completed architecture and migration items in `docs/Recommendations.md`.

Validation completed:

- Nine architecture, domain, cache, theme, and headless rendering tests passed.
- Full Python compilation passed.
- `git diff --check` passed.
- Multiplayer services remain intentionally deferred until the local single-player engine is stable.

## Step 22. Exit

### Prompt

> When the user presses the `Esc` key, bring them back to the startup menu.

### Output

- Changed the in-game `Esc` behavior from process exit to a clean return to the startup menu.
- Added a repeatable launcher flow so the user can select another theme after leaving a game.
- Preserved the window-close behavior for exiting the application.
- Added cleanup for mouse capture, cursor visibility, music playback, and Pygame state when returning to the menu.

Validation completed:

- Escape menu-return regression test passed.
- Full test suite passed with 10 tests.
- Python compilation passed.
- `git diff --check` passed.

## Step 23. Player Name

### Prompt

> Before asking for theme selection in the startup menu, ask for Player Name.
>
> If the user returns to the startup menu after pressing `Esc`, do not ask for their name a second time.

### Output

- Added a required player-name prompt before the theme-selection menu.
- Stored the selected name on the active game session.
- Kept the player name when `Esc` returns the user to the startup menu.
- Added validation for blank-name rejection, prompt order, and player-name propagation.

Validation completed:

- Player-name startup and persistence tests passed.
- Full test suite passed with 11 tests.
- Python compilation passed.
- `git diff --check` passed.

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

- Added XML-backed high-score persistence in `infrastructure/scores.py`.
- Creates `scores.xml` automatically when the game starts.
- Records the player's name and kill count once when Game Over begins or the player exits the game.
- Sorts scores by kills and retains the Top 10 entries.
- Displays the Top 10 scores before each theme-selection menu.
- Preserves the leaderboard when returning to the startup menu with `Esc`.
- Preserves the recorded score when the player selects `0) Exit` from the startup menu after returning from a game with `Esc`.
- Adds blank lines before the player-name prompt, Top 10 Scores heading, and theme-selection heading.
- Displays the startup menu theme as `Doom`.

Validation completed:

- Score XML creation and persistence passed.
- Top 10 ordering and lowest-score eviction passed.
- Game Over records a player's name and kills exactly once.
- Full test suite passed with 13 tests.
- Python compilation and `git diff --check` passed.

## Step 25. Mac Build

### Prompt

> Add macOS build capabilities to `build.py` via `build.py -m`.

### Output

- Added `-m`/`--macos` support to `build.py`.
- Restricted macOS builds to macOS hosts so PyInstaller produces a native artifact.
- Configured the output as `build/POV-Blaster_mac.app`.
- Documented macOS build and launch instructions in `README.md`.
- Updated the Escape control documentation to reflect its return to the startup menu.

Validation completed:

- `build.py --help` exposes the macOS target.
- The macOS host guard rejects `-m` on Windows.
- `build.py` compilation and `git diff --check` passed.

## Step 27. Web Build

### Prompt

> Convert POV-Blaster to a web-based Pygbag build while maintaining the existing `build.py` executable targets.

### Output

- Added `build.py -b`/`--web` for browser packaging through Pygbag.
- Added `web_main.py` with an asynchronous browser-compatible game loop.
- Preserved the existing Windows, Linux, and Mac PyInstaller targets.
- Added browser-local high-score storage with desktop memory fallback.
- Kept desktop XML persistence through `scores.xml`.
- Added web build documentation and platform-specific audio guidance.
- Updated the canonical `main.py` entry point to launch the async browser path under Emscripten instead of blocking on desktop console input.
- Added local BrowserFS packaging to avoid the unavailable Pygbag CDN BrowserFS reference that caused the grey startup screen.

Validation completed:

- Pygbag 0.9.3 installed successfully.
- `build.py -b` completed successfully and produced `build/web`.
- Browser score adapter and async Escape tests passed.
- Full test suite passed with 16 tests.
- Python compilation and `git diff --check` passed.

## Step 26. Map File

### Prompt

> Move `mini_map` out from `map.py` into a plain-text file type for storing predefined maps. Name the current `mini_map` example `mini_map_default`. The game should use this map by default at startup and whenever no other map is defined.
>
> Rename `mini_map_default.txt` to `1_mini_map_default.txt`.

### Output

- Moved the embedded map grid into `maps/1_mini_map_default.txt`.
- Added plain-text map loading with `.` for empty cells and digits for wall texture IDs.
- Set `1_mini_map_default` as the default map name.
- Added fallback to the default map when a requested map is unavailable.
- Added rectangular-grid and valid-cell validation.
- Included predefined maps in PyInstaller builds and documented the map directory.

Validation completed:

- Default map loads as a 32x16 grid.
- Missing-map fallback returns the default map.
- Focused map tests and full regression tests passed.
- Python compilation and `git diff --check` passed.

## Step. 27 Pygbag

### Prompt

> Can I convert my project to use pyBag and make my game Web Based while still maintaining the ability to use build.py to create executables?
>
> Execute on all of that.
>
> For Web build, always default to Player Name as "Player 1" and theme as "4) Doom"
>
> Increase web build mouse sensitivity by 20%. Then increase by another 20%.

### Output

- Diagnosed and fixed a series of Pygbag/WASM issues that left the web build stuck on "Loading" or with broken audio/visuals:
	- `pg.time.set_timer` is unsupported on WASM; replaced with a `delta_time`-based accumulator for the animation pulse.
	- `map.py` failed to load on WASM due to `encoding='ascii'` not being registered; switched to `encoding='utf-8'`.
	- `build.py`'s web packaging excluded the `sound` resource folder entirely, and Pygbag rejects raw WAV/MP3; added an `imageio-ffmpeg`-based conversion step to transcode all sound assets to OGG Vorbis.
	- SDL's mixer plays back garbled/incorrect audio under Pygbag/WASM regardless of encoding; added a `BrowserSound`/`BrowserClip` backend in `infrastructure/audio.py` that plays sounds via native browser `<audio>` elements (pre-loaded and pooled to stay in sync under rapid fire) instead of `pg.mixer`, selected automatically for the web build via a new `sound_factory` hook on `Game`.
	- Fixed duplicate/overlapping theme music by stopping the previous sound backend's theme before creating a new one on every `new_game()`.
	- Patched the Pygbag-generated `index.html` (and its cached template, so the fix survives dev-server restarts) to recolor the loading box/background and make the canvas fill the browser window while preserving aspect ratio via `object-fit: contain`.
- `web_main.py` always launches with `WEB_PLAYER_NAME = 'Player 1'` and `WEB_THEME = THEMES[3]` (the Doom theme).
- Increased web-only mouse sensitivity via a new `WEB_MOUSE_SENSITIVITY` setting, applied in `player.py` only when `game.browser_mode` is set, leaving desktop/Linux sensitivity unchanged. Raised it twice at the user's request (20%, then another 20% on top, for a combined ~44% increase).
- Preserved all existing Windows, Linux, and macOS PyInstaller build targets in `build.py` unchanged.
- Documented the full browser build/serve/rebuild workflow in `README.md`, including that the Pygbag dev server must be restarted after every rebuild since it doesn't hot-reload.

Validation completed:

- Rebuilt the web target repeatedly with `build.py --web` and served it with `python -m pygbag build/web-source`, verifying in a real browser session that the game loads past "Loading", renders correctly, and plays sound/music without errors or overlaps.
- Confirmed rapid-fire weapon sounds stay in sync using the pooled `BrowserClip` audio elements.

## Step. 28 PROD Deploy

### Prompt

> Can you help me deploy this app on GitHub pages?

### Output

- Added `.github/workflows/deploy-pages.yml`, a GitHub Actions workflow that builds the web target with `build.py --web` and publishes `build/web` to GitHub Pages on every push to `main` (or manual dispatch).
- Fixed a `build.py --web` bug where `web_dir.mkdir(exist_ok=True)` failed on a fresh checkout because the parent `build/` directory didn't exist yet (only worked locally because `build/` already existed from prior local builds); changed to `mkdir(parents=True, exist_ok=True)`.
- Documented the one-time setup (enabling **Settings → Pages → Source: GitHub Actions**) and the resulting live URL in `README.md`, with direct links to the repository's Pages settings, Actions tab, and the deployed site.

Validation completed:

- Diagnosed a failed workflow run via the shared Actions log output, identified the missing-parent-directory error, fixed it, and pushed; the workflow re-triggers automatically on push to `main`.