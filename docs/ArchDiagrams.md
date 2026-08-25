# POV-Blaster System Architecture Diagrams

These diagrams use PlantUML syntax and can be previewed in VS Code with the PlantUML extension. Open this file and run **PlantUML: Preview Current Diagram** for the selected diagram block.

## System Context

```plantuml
@startuml
!theme plain
skinparam componentStyle rectangle
skinparam shadowing false
skinparam backgroundColor white

actor Player
actor Maintainer

package "Client Platforms" {
  component "Desktop Game\n(main.py / Pygame)" as Desktop
  component "Browser Game\n(Pygbag / WASM)" as Browser
}

package "Hosted Services" {
  component "GitHub Pages\nStatic Web Host" as Pages
  component "Render Free Web Service\nFastAPI + Uvicorn" as API
  database "Neon Free Postgres" as Neon
}

package "Developer Tooling" {
  component "GitHub Actions\nCI / Pages / Render hook" as Actions
  component "Local SQLite\ndata/scores.sqlite3" as LocalDB
}

Player --> Desktop : plays
Player --> Pages : opens web game
Pages --> Browser : serves bundle
Browser --> API : scores and sessions
API --> Neon : DATABASE_URL
Desktop --> LocalDB : local leaderboard
Maintainer --> Actions : pushes main
Actions --> Pages : deploys web bundle
Actions --> API : optional deploy hook
@enduml
```

## Web Score Sequence

```plantuml
@startuml
!theme plain
skinparam shadowing false
autonumber

actor Player
participant "Browser Game" as Browser
participant "FastAPI\napi/main.py" as API
participant "Neon Postgres" as DB
participant "ipapi.co" as Geo

Player -> Browser : Enter name and start game
Browser -> API : POST /sessions
API -> Geo : Lookup forwarded client IP
Geo --> API : city and country (best effort)
API -> DB : INSERT web_sessions
DB --> API : session record
API --> Browser : 201 Created

Player -> Browser : Finish run
Browser -> API : POST /scores
API -> Geo : Lookup forwarded client IP
Geo --> API : city and country (best effort)
API -> DB : INSERT scores
DB --> API : score record
API --> Browser : 201 Created

Browser -> API : GET /scores
API -> DB : SELECT scores ordered by kills
DB --> API : score rows
API --> Browser : score list
@enduml
```

## Local/Remote Score Synchronization

```plantuml
@startuml
!theme plain
skinparam shadowing false

actor Maintainer
participant "HighScores" as Local
 database "Local SQLite\ndata/scores.sqlite3" as SQLite
participant "FastAPI /scores" as API
 database "Neon Postgres" as Postgres

Maintainer -> Local : sync(api_url, direction="push")
Local -> SQLite : Read top-ten local scores
loop each local score
  Local -> API : POST /scores
  API -> Postgres : Insert score
  Postgres --> API : Created record
  API --> Local : 201 Created
end

Maintainer -> Local : sync(api_url, direction="pull")
Local -> API : GET /scores
API -> Postgres : Read ordered scores
Postgres --> API : Score list
API --> Local : Score list
Local -> SQLite : Replace local rows
@enduml
```

## Runtime Class Diagram

```plantuml
@startuml
!theme plain
skinparam classAttributeIconSize 0
skinparam shadowing false

class Game {
  +player_name: str
  +browser_mode: bool
  +player: Player
  +object_handler: ObjectHandler
  +weapon: Weapon
  +run()
  +run_async()
  +new_game()
}

class Player {
  +health_state: Health
  +movement()
  +mouse_control()
  +fire()
}

class NPC {
  +health_state: Health
  +run_logic()
  +update()
}

class SoldierNPC
class CacoDemonNPC
class CyberDemonNPC
class HuntingBearNPC

class ObjectHandler {
  +npcs: list[NPC]
  +sprites: list[SpriteObject]
  +update()
}

class SpriteObject {
  +image
  +get_sprite_projection()
}

class Weapon {
  +damage: int
  +update()
  +draw()
}

class ObjectRenderer {
  +draw(snapshot)
  +win()
  +game_over()
}

interface Renderer
interface GameContext
interface ScoreStore

class Health {
  +current: int
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
  +player_name: str
  +kills: int
}

' Has-A / composition relationships
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

' Is-A / inheritance and implementation relationships
SoldierNPC --|> NPC : is-a
CacoDemonNPC --|> NPC : is-a
CyberDemonNPC --|> NPC : is-a
HuntingBearNPC --|> NPC : is-a
ObjectRenderer ..|> Renderer : implements
Game ..|> GameContext : conforms to
HighScores ..|> ScoreStore : implements
BrowserHighScores ..|> ScoreStore : implements

@enduml
```

## API Class Diagram

```plantuml
@startuml
!theme plain
skinparam classAttributeIconSize 0
skinparam shadowing false

class FastAPIApp {
  GET /health
  GET /scores
  POST /scores
  GET /sessions
  POST /sessions
}

class ScoreSubmission {
  player_name: str
  kills: int
}

class ScoreRecord {
  id: int
  player_name: str
  kills: int
  city: str
  country: str
  created_at: str
}

class WebSessionSubmission {
  player_name: str
}

class WebSessionRecord {
  id: int
  player_name: str
  ip_address: str
  city: str
  country: str
  created_at: str
}

database "Neon Postgres\nproduction" as Postgres
database "SQLite\nlocal fallback" as SQLite

FastAPIApp ..> ScoreSubmission : validates
FastAPIApp ..> ScoreRecord : returns
FastAPIApp ..> WebSessionSubmission : validates
FastAPIApp ..> WebSessionRecord : returns
FastAPIApp --> Postgres : DATABASE_URL present
FastAPIApp --> SQLite : DATABASE_URL absent
ScoreRecord --|> ScoreSubmission : is-a response model
WebSessionRecord --|> WebSessionSubmission : is-a response model
@enduml
```

## Relationship Legend

- `--|>` means **Is-A** inheritance.
- `..|>` means interface implementation or protocol conformance.
- `*--` means strong **Has-A** composition: the owner creates and controls the part.
- `o--` means aggregation: the owner manages related objects that can exist independently.
- `-->` means a runtime dependency or request/data flow.
