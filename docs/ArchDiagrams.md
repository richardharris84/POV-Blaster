# POV-Blaster System Architecture Diagrams

These diagrams use Mermaid syntax. GitHub renders the diagrams directly, and they can be previewed in VS Code with the built-in Markdown preview. Open the preview with **Markdown: Open Preview** or **Markdown: Open Preview to the Side** while viewing this file.

## System Context

```mermaid
flowchart LR
    Player([Player])
    Maintainer([Maintainer])
    subgraph Client[Client Platforms]
        Desktop[Desktop Game<br/>main.py / Pygame]
        Browser[Browser Game<br/>Pygbag / WASM]
    end
    subgraph Hosted[Hosted Services]
        Pages[GitHub Pages<br/>Static Web Host]
        API[Render Free Web Service<br/>FastAPI + Uvicorn]
        Neon[(Neon Free Postgres)]
    end
    subgraph Tools[Developer Tooling]
        Actions[GitHub Actions<br/>CI / Pages / Render hook]
        LocalDB[(Local SQLite<br/>data/scores.sqlite3)]
    end
    Player -->|plays| Desktop
    Player -->|opens web game| Pages
    Pages -->|serves bundle| Browser
    Browser -->|scores and sessions| API
    API -->|DATABASE_URL| Neon
    Desktop -->|local leaderboard| LocalDB
    Maintainer -->|pushes main| Actions
    Actions -->|deploys web bundle| Pages
    Actions -->|optional deploy hook| API
```

## Web Score Sequence

```mermaid
sequenceDiagram
  autonumber
  actor Player
  participant Browser as Browser Game
  participant API as FastAPI api/main.py
  participant DB as Neon Postgres
  participant Geo as ipapi.co
  Player->>Browser: Enter name and start game
  Browser->>API: POST /sessions
  API->>Geo: Lookup forwarded client IP
  Geo-->>API: city and country (best effort)
  API->>DB: INSERT web_sessions
  DB-->>API: session record
  API-->>Browser: 201 Created
  Player->>Browser: Finish run
  Browser->>API: POST /scores
  API->>Geo: Lookup forwarded client IP
  Geo-->>API: city and country (best effort)
  API->>DB: INSERT scores
  DB-->>API: score record
  API-->>Browser: 201 Created
  Browser->>API: GET /scores
  API->>DB: SELECT scores ordered by kills
  DB-->>API: score rows
  API-->>Browser: score list
```

## Local/Remote Score Synchronization

```mermaid
sequenceDiagram
    actor Maintainer
    participant Local as HighScores
    participant SQLite as Local SQLite<br/>data/scores.sqlite3
    participant API as FastAPI /scores
    participant Postgres as Neon Postgres
    Maintainer->>Local: sync(api_url, direction="push")
    Local->>SQLite: Read top-ten local scores
    loop each local score
        Local->>API: POST /scores
        API->>Postgres: Insert score
        Postgres-->>API: Created record
        API-->>Local: 201 Created
    end
    Maintainer->>Local: sync(api_url, direction="pull")
    Local->>API: GET /scores
    API->>Postgres: Read ordered scores
    Postgres-->>API: Score list
    API-->>Local: Score list
    Local->>SQLite: Replace local rows
```

## Runtime Class Diagram

```mermaid
classDiagram
    class Game {
        +str player_name
        +bool browser_mode
        +Player player
        +ObjectHandler object_handler
        +Weapon weapon
        +run()
        +run_async()
        +new_game()
    }
    class Player {
        +Health health_state
        +movement()
        +mouse_control()
        +fire()
    }
    class NPC {
        +Health health_state
        +run_logic()
        +update()
    }
    class SoldierNPC
    class CacoDemonNPC
    class CyberDemonNPC
    class HuntingBearNPC
    class ObjectHandler {
        +list~NPC~ npcs
        +list~SpriteObject~ sprites
        +update()
    }
    class SpriteObject {
        +image
        +get_sprite_projection()
    }
    class Weapon {
        +int damage
        +update()
        +draw()
    }
    class ObjectRenderer {
        +draw(snapshot)
        +win()
        +game_over()
    }
    class Renderer
    class GameContext
    class ScoreStore
    <<interface>> Renderer
    <<interface>> GameContext
    <<interface>> ScoreStore
    class Health {
        +int current
        +damage(amount)
        +recover(amount)
    }
    class HighScores {
        +load()
        +add(player_name, kills)
        +sync(api_url, direction)
    }
    class BrowserHighScores {
        +load()
        +add(player_name, kills)
        +record_session(player_name)
    }
    class Score {
        +str player_name
        +int kills
    }
    Game *-- Player : has-a
    Game *-- ObjectHandler : has-a
    Game *-- Weapon : has-a
    Game *-- ObjectRenderer : has-a
    Player *-- Health : has-a
    NPC *-- Health : has-a
    ObjectHandler o-- NPC : manages
    ObjectHandler o-- SpriteObject : manages
    HighScores o-- Score : stores
    BrowserHighScores o-- Score : caches
    SoldierNPC --|> NPC : is-a
    CacoDemonNPC --|> NPC : is-a
    CyberDemonNPC --|> NPC : is-a
    HuntingBearNPC --|> NPC : is-a
    ObjectRenderer ..|> Renderer : implements
    Game ..|> GameContext : conforms to
    HighScores ..|> ScoreStore : implements
    BrowserHighScores ..|> ScoreStore : implements
```

## API Class Diagram

```mermaid
classDiagram
    class FastAPIApp {
        GET /health
        GET /scores
        POST /scores
        GET /sessions
        POST /sessions
    }
    class ScoreSubmission {
        str player_name
        int kills
    }
    class ScoreRecord {
        int id
        str player_name
        int kills
        str city
        str country
        str created_at
    }
    class WebSessionSubmission {
        str player_name
    }
    class WebSessionRecord {
        int id
        str player_name
        str ip_address
        str city
        str country
        str created_at
    }
    class Postgres
    class SQLite
    Postgres : Neon Postgres production
    SQLite : SQLite local fallback
    FastAPIApp ..> ScoreSubmission : validates
    FastAPIApp ..> ScoreRecord : returns
    FastAPIApp ..> WebSessionSubmission : validates
    FastAPIApp ..> WebSessionRecord : returns
    FastAPIApp --> Postgres : DATABASE_URL present
    FastAPIApp --> SQLite : DATABASE_URL absent
    ScoreRecord --|> ScoreSubmission : response model
    WebSessionRecord --|> WebSessionSubmission : response model
```

## Relationship Legend

- `--|>` means **Is-A** inheritance.
- `..|>` means interface implementation or protocol conformance.
- `*--` means strong **Has-A** composition: the owner creates and controls the part.
- `o--` means aggregation: the owner manages related objects that can exist independently.
- `-->` means a runtime dependency or request/data flow.
