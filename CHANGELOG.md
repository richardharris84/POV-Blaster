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

> Perform a full review of our patch. Upon QA, the change seems to have broken solider death. Also, fix all the libpng warning messages in the Terminal.

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