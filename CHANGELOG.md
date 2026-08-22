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