# New Theme / Character Art Prompt — Hunting NPC Redesign

This document captures a ready-to-use prompt for an external AI image
generator to produce **minimal reference art** for redesigning the Hunting
theme's three NPCs (Hunter, Deer, Bear). The project's own deterministic
pixel-art pipeline (`tools/generate_pixel_assets.py` and
`tools/generate_themes.ps1`) is then used to expand a single reference image
per character into the full animation set the engine needs (idle ×8, walk
×8, attack ×6, pain ×3, death ×8, plus one root icon — 34 frames per
character, 102 total across all three). Existing frames are transparent
76×110 px PNGs.

## Prompt

```
You are generating character concept art for a fan-made, non-commercial indie
game (a Wolfenstein/DOOM-style raycaster). Do NOT reproduce any copyrighted or
trademarked character design exactly. Instead, create wholly ORIGINAL pixel-art
characters that are only thematically/spiritually reminiscent of well-known
archetypes, using different exact color schemes, proportions, and details than
the source inspiration so the result is a distinct, original design.

Produce exactly 3 images — no more. Do not attempt to draw animation frames,
walk cycles, attack poses, or death sequences. A local deterministic pixel-art
pipeline in this project already exists to procedurally generate the full set
of idle/walk/attack/pain/death animation frames from a single reference image
plus a color palette, so your job is only to nail the character identity in one
clean reference pose per character.

For each of the 3 characters below, deliver ONE full-body, front-facing,
transparent-background pixel-art / cel-shaded character portrait in a
standing idle pose, foreground character only (no weapon prop needed in the
character art itself — weapons are rendered as a separate overlay). Aspect
ratio should be tall and narrow, approximately 0.69:1 (width:height) — for
example 512x744. Use a clean, limited color palette suitable for a retro
raycaster enemy sprite, with crisp readable silhouettes (no photorealistic
shading, no blur, no anti-aliased soft gradients).

Character 1 — "Hunter" replacement:
An original bumbling, comedic cartoon hunter character reminiscent in spirit
of a classic "clumsy hunter" archetype (evoking, without copying, the vibe of
Elmer Fudd): stout build, balding or bald head, round rosy cheeks, bulbous
nose, thick brows, a hunting cap with ear flaps, a plaid or forest-green
hunting jacket, suspenders, and boots. Comedic, slightly bumbling posture.

Character 2 — "Deer" replacement:
An original young woodland deer/fawn character reminiscent in spirit of a
classic gentle, doe-eyed young deer archetype (evoking, without copying, the
vibe of Bambi): large expressive eyes, slender legs, light brown coat with a
white underbelly and light spot markings, small or no antlers (young deer),
soft and innocent posture.

Character 3 — "Bear" replacement:
An original large, friendly, easygoing forest bear character reminiscent in
spirit of a classic laid-back, good-natured big bear archetype (evoking,
without copying, the vibe of Baloo): broad round-bellied build, relaxed
posture, a warm/friendly facial expression, brown fur, adapted to a forest
hunting-ground setting rather than a jungle.

Deliverables: 3 PNG files with transparent backgrounds, named
hunter_reference.png, deer_reference.png, and bear_reference.png.
```

## After the reference images are ready

1. Resize/pixel-snap each reference to the engine's exact 76×110 canvas.
2. Extract a primary/secondary color palette from each reference.
3. Feed the palette into `tools/generate_pixel_assets.py` (or
   `tools/generate_themes.ps1 -ThemeKey hunting`) to procedurally generate the
   full idle/walk/attack/pain/death frame sets and root `0.png` for all three
   NPCs.
4. Run `tools/audit_themes.py --check` and the test suite to confirm nothing
   regresses.
