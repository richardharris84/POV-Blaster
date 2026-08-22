# Graphics Rollback Notes

## Goal

Preserve the experimental graphics-upgrade work without leaving the stable project state in a broken condition.

## What was done

The project was rolled back to the last known good commit and moved onto a dedicated `develop` branch. The experimental graphics changes were stashed so they could be restored later without risking the stable branch.

## Verified state

Fresh Git output confirmed:

- `git reset --hard HEAD` completed successfully
- `git status --short` returned empty after the reset
- `git stash list` showed the saved experimental work

## Current branch state

- Current branch: `develop`
- Saved stash: `stash@{0}: On main: WIP graphics upgrades before rollback`

## Recovery instructions

If you want to re-open the experimental graphics work later, run:

```bash
git stash apply stash@{0}
```

If you want to keep the stable baseline clean, leave the stash in place and continue working on `develop` without restoring it.

## Recommended workflow

- Keep `main` as the stable release baseline.
- Do experimental graphics work on `develop`.
- Only reapply the stash when you are ready to test incremental visual changes.
- Avoid mixing broken prototype work into the release branch.

## Appendix: Graphics Upgrade Prompt Archive

### Step 12A. Graphics Upgrade Plan

#### Prompt

> Take a look at the games listed here:
> - Valorant
> - Warhammer 40,000: Boltgun
> - Battlefield 1
> - Dusk
> - Half-Life 2
> - Far Cry 6
> - Bulletstorm: Full Clip Edition
> - Call of Duty: Black Ops 6
> - Borderlands 4
> - PUBG: Battlegrounds
> - Counter-Strike 2
> - Wolfenstein 2: New Colossus
> - I Am Your Beast
> - Metro Exodus
> - Superhot
> - Apex Legends
> - Black Mesa
> - Tom Clancy's Rainbow Six Siege
> - Marathon
>
> Is it possible to upscale the graphics in our game? How?
>
> Provide me with a list of 5 FPS modern games you could easily replicate the graphics of for our game.

#### Cleaned summary

Yes, the visuals in POV-Blaster can be upgraded within the existing engine, but only within the limits of a Pygame raycasting renderer. The realistic approach is to improve texture resolution, lighting, sprite presentation, atmosphere, post-process-style effects, and the clarity of the render pipeline without changing the core gameplay loop or engine architecture.

The best target references for a visual upgrade are stylized, readable retro-FPS games with strong contrast and punchy presentation, including:

- Warhammer 40,000: Boltgun
- Dusk
- I Am Your Beast
- Black Mesa
- Half-Life 2

These games are realistic visual targets for a controlled upgrade because they emphasize readable silhouettes, strong material contrast, atmospheric lighting, and stylized retro fidelity rather than photorealism.

### Step 12B. Prompt Creation > Graphics Upgrade

#### Prompt

> Role: Act as a world-renowned graphic designer and game designer.
>
> Objective: Perform a Visual-quality upgrade - use higher-resolution assets, better lighting, shadows, depth buffering, effects, and a stronger renderer. Make our current raycasting engine support the highest possible resolution textures, improved sprite art, lighting/fog, floor textures, depth buffering, muzzle flashes, particles, screen shake, and better environmental decoration.
>
> Requirements:
> - Update the media assets in resources/sprites & resources/textures.
> - Increase wall textures size by 100%. Re-finish the images to simulate an Unreal Engine look.
> - Replace the solid grey floor with a gravel texture.
> - Implement Cel-shading technique.
> - Add configurable quality settings.
>
> Validation:
> - The end result of our game should look as close as possible to I Am Your Best & Warhammer 40,000: Boltgun.
> - All images within a sprites sub-folder should be unique frames.

#### Cleaned summary

This was the initial prompt package for the graphics upgrade, but it was too broad and too optimistic for the current engine. It included several valid goals (higher texture resolution, lighting/fog, floor texture, cel shading, configurable settings) but also included a few risky elements that were likely to create regressions if applied broadly:

- scaling all textures without a technical validation pass
- claiming an Unreal-like finish without respecting the engine constraints
- broad asset replacement across multiple folders without preserving compatibility
- a requirement to improve the renderer beyond what the current raycasting architecture safely supports

This prompt was valuable as a design direction, but it needed tighter technical constraints to reduce bugs and avoid hallucinated engine features.

### Step 12C. Graphics Upgrade Implementation

#### Prompt

> Role: Act as a senior graphics engineer, game designer, and production-quality technical artist.
>
> Project context:
> - POV-Blaster is a Python/Pygame raycasting game.
> - Preserve the existing gameplay, map geometry, asset folder structure, file names, and runtime compatibility unless a change is required.
> - The current desktop renderer must remain functional.
> - Do not replace the engine or migrate to WebGL in this task.
> - The target visual direction combines the stylized retro FPS look of Dusk, I Am Your Beast, and Warhammer 40,000: Boltgun.
>
> Objective:
> Perform a controlled visual-quality upgrade of the current raycasting renderer and assets. Improve visual fidelity while preserving gameplay behavior and maintaining stable performance.
>
> Before editing:
> 1. Inspect the current source files, asset dimensions, animation folders, and rendering pipeline.
> 2. Read docs/CodeBase.md, docs/CodeAudit.md, and docs/CloneCompare.md.
> 3. Record the current wall texture dimensions, ray count, frame time if measurable, and all sprite animation folders.
> 4. Identify any assets that already meet the requested dimensions.
> 5. Do not overwrite user changes unrelated to this task.
>
> Implementation requirements:
> - Update only assets under resources/textures and resources/sprites.
> - Preserve required file names and folder paths used by the code.
> - Increase each wall texture to exactly twice its current dimensions.
> - Use filtered resampling such as Lanczos or an equivalent high-quality method.
> - Preserve transparency for sprite assets.
> - Do not replace existing assets with placeholders.
> - Keep unrelated UI digit textures, end screens, and audio unchanged unless required for compatibility.
> - Treat every numbered or ordered image in an animation folder as a frame.
> - Preserve the correct frame order, including non-numeric names such as POSSM0.png.
> - Ensure every frame in each sprite animation folder is visually unique.
> - Validate uniqueness using pixel/content hashes, not filenames alone.
> - Add configurable quality settings.
> - Add a per-ray depth buffer.
> - Use the depth buffer to prevent sprites from rendering through walls.
> - Add distance-based lighting and fog with configurable color and intensity.
> - Add cel shading using discrete lighting bands.
> - Replace the solid grey floor with a gravel texture.
> - Add subtle environmental decoration using existing sprite conventions.
> - Add muzzle flash, impact flash, blood feedback, and screen shake only if the existing weapon/combat state supports them.
> - Ensure all effects expire through elapsed time and do not block the game loop.
> - Avoid per-frame disk access and asset loading.
>
> Validation requirements:
> - Run full Python compilation.
> - Run editor diagnostics or lint checks.
> - Run git diff --check.
> - Confirm no unrelated files were changed.
> - Confirm every wall texture is exactly twice its original dimensions.
> - Confirm every sprite animation folder has at least one frame.
> - Confirm every animation folder contains no duplicate frame content hashes.
> - Confirm the gravel floor texture exists and loads successfully.
> - Confirm depth-buffer validation and sprite occlusion.
> - Run Windows and Linux/WSL smoke tests.
> - Report files changed, assets changed, settings, tests, unresolved limitations, and visual compromises.
>
> Do not fabricate test results or visual improvements.

#### Cleaned summary

This was the most technically disciplined version of the graphics upgrade prompt and was the closest to a safe production attempt. It correctly established the constraints that prevent the project from drifting into an untestable visual rewrite:

- protect the existing engine and gameplay
- preserve file names, resources, compatibility, and runtime behavior
- limit changes to supported rendering features
- require validation for texture sizing, sprite uniqueness, and depth-buffer logic
- clearly separate engine-supported upgrades from speculative or unsafe enhancements

The prompt was also explicit about not fabricating results, which is important for a raycasting engine where visual improvements are limited by the architecture. The final outcome of the graphics-upgrade attempt was that the project was not kept in a stable visual state and was therefore rolled back to the last known good commit.

### Outcome

The graphics upgrade was never merged into the stable branch. The project was preserved on the safe baseline and the experimental work was stashed before rollback. The actual operating conclusion was: the visual upgrade direction was valid in concept, but the implementation was too broad for the current engine and unsafe to leave in the stable branch.

In short:

- valid design direction: yes
- safe implementation path: only incremental and validated changes
- final project state: stable baseline retained, experimental graphics work preserved separately
