# Remaining Themes / Character Art Prompt

This document captures a ready-to-use prompt for an external AI image
generator to produce **minimal reference art** for the remaining three themes:
Candy Kingdom, Space, and Graveyard. The project's deterministic pixel-art
pipeline (`tools/generate_pixel_assets.py` and `tools/generate_themes.ps1`)
will expand one reference image per character into the full animation sets the
engine needs (idle x8, walk x8, attack x6, pain x3, death x8, plus one root
icon). Existing NPC frames are transparent 76x110 px PNGs.

## Prompt

```
You are generating character concept art for a fan-made, non-commercial indie
game (a retro raycasting FPS). Create wholly ORIGINAL pixel-art characters.
Do not reproduce any copyrighted or trademarked character, costume, logo, or
franchise design exactly. Use only broad genre archetypes as inspiration, with
original silhouettes, proportions, colors, names, and details.

Produce exactly 9 images -- no more. Do not draw animation frames, walk cycles,
attack poses, pain poses, or death sequences. A local deterministic pixel-art
pipeline already exists to generate those frames from a single reference image
and a palette. Your job is to establish each character's identity in one clean
reference pose.

For each character below, deliver ONE full-body, front-facing, transparent-
background pixel-art or cel-shaded portrait in a standing idle pose. Show only
the character, with no environment, text, logo, or weapon prop. Weapons are
rendered separately by the game. Use a tall, narrow composition suitable for a
76x110 retro FPS sprite; a larger source image is acceptable if it preserves
that approximate 0.69:1 width-to-height ratio. Use crisp readable silhouettes,
limited colors, hard pixel edges, and no blur, photorealism, anti-aliased soft
gradients, or background checkerboard.

THEME 1 -- CANDY KINGDOM

Character 1 -- "Marshmallow Man" replacement:
An original soft, puffy candy guardian with a rounded marshmallow body, toasted
edges, a simple expressive face, candy-button details, and a whimsical but
slightly intimidating stance. Use white, cream, toasted brown, and a bright
candy accent. Do not resemble any existing marshmallow mascot.

Character 2 -- "Springfield Doughnut" replacement:
An original sentient frosted doughnut creature with a bold ring silhouette,
colorful icing, sprinkles, tiny expressive eyes, and short cartoon limbs. Make
the flavor, frosting pattern, and face design original and clearly readable at
small sprite scale.

Character 3 -- "Gingerbread Golem" replacement:
An original sturdy gingerbread guardian with cracked baked-cookie texture,
icing trim, candy details, chunky arms, and heavy feet. Give it a distinct
shape and expression rather than copying a familiar gingerbread character.

THEME 2 -- SPACE

Character 4 -- "Alien Drone" replacement:
An original compact hovering or insect-like extraterrestrial scout with a
bright sensor core, asymmetrical armor, antennae or fins, and a narrow hostile
silhouette. Use teal, cyan, or another original accent against dark space
colors. No recognizable franchise armor or insignia.

Character 5 -- "Alien Warrior" replacement:
An original tall extraterrestrial combatant with an unusual anatomy, layered
organic or technological armor, a distinctive head shape, and a strong
forward-facing stance. Keep the design readable as a retro FPS enemy without
copying a space marine, famous alien, or existing game costume.

Character 6 -- "Alien Overlord" replacement:
An original imposing alien leader with an oversized head or crown-like anatomy,
large shoulders, ceremonial armor, and a memorable central glowing feature.
Make the silhouette clearly larger and more powerful than the Drone and
Warrior, with original colors and details.

THEME 3 -- GRAVEYARD

Character 7 -- "Ghost" replacement:
An original translucent undead apparition with a ragged lower body, a unique
face or mask, and a readable floating silhouette. Use pale spectral colors and
limited dark outlines; avoid copying any famous ghost mascot or sheet ghost.

Character 8 -- "Vampire" replacement:
An original gothic vampire with a high-collared coat or cape, angular features,
subtle fangs, and a confident forward-facing stance. Use a distinct palette and
costume details; do not copy a specific film, comic, or game vampire.

Character 9 -- "Werewolf" replacement:
An original wild wolf-like humanoid with broad shoulders, pointed ears, fur
silhouette, claws, and a dramatic but readable stance. Use original fur
patterns, proportions, and colors rather than resembling a particular famous
werewolf design.

Deliverables: 9 transparent PNG files named
marshmallow_man_reference.png, springfield_doughnut_reference.png,
gingerbread_golem_reference.png, alien_drone_reference.png,
alien_warrior_reference.png, alien_overlord_reference.png,
ghost_reference.png, vampire_reference.png, and werewolf_reference.png.
```

## After the reference images are ready

1. Resize and pixel-snap each reference to the engine's exact 76x110 canvas.
2. Extract a primary/secondary color palette from each reference.
3. Feed the references and palettes into `tools/generate_pixel_assets.py` (or
   `tools/generate_themes.ps1`) to generate each theme's idle/walk/attack/pain/
   death frames and root `0.png`.
4. Run `tools/audit_themes.py --check` and the test suite to confirm nothing
   regresses.
