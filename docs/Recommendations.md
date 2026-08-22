# POV-Blaster Recommendations

## Prompt

> Recommended architecture and migration steps for POV-Blaster.

## Response

The recommended architecture and migration plan are already documented in [docs/CodeAudit.md](CodeAudit.md).

**Recommended architecture:**

- ☑ Modular monolith first.
- ☑ Separate pure game rules from Pygame, audio, filesystem, and rendering.
- ☑ Use explicit typed interfaces instead of shared mutable `Game` dependencies.
- ☑ Organize into:
  - ☑ `domain`: entities, rules, combat, movement
  - ☑ `application`: game loop and use cases
  - ☑ `infrastructure`: assets, audio, persistence, networking
  - ☑ `presentation`: Pygame rendering and input
  - ☑ `tools`: asset generation and validation
- ☐ Keep online services separate from the local simulation.

**Migration order:**

1. ☑ Add tests and headless execution.
2. ☑ Replace wildcard imports and global state.
3. ☑ Extract player, NPC, combat, and game-state rules into pure modules.
4. ☑ Introduce explicit dependency interfaces.
5. ☑ Create asset, audio, and input adapters.
6. ☑ Move rendering behind a renderer interface.
7. ☑ Add deterministic simulation and render snapshots.
8. ☑ Improve texture/frame caching and depth-buffer rendering.
9. ☑ Add CI, profiling, packaging, and asset validation.
10. ☐ Add multiplayer services only after the single-player engine is stable.

The architecture migration is implemented and validated for the local modular monolith; multiplayer services remain intentionally deferred.
