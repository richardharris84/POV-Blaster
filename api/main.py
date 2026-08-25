"""FastAPI service for shared POV-Blaster scores."""

from __future__ import annotations

from contextlib import closing
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from fastapi import FastAPI, HTTPException, Request as FastAPIRequest
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB_PATH = PROJECT_ROOT / "data" / "pov_blaster.sqlite3"
DB_PATH = Path(os.environ.get("DB_PATH", str(DEFAULT_DB_PATH)))
GEOLOCATION_URL = "https://ipapi.co/{}/json/"

app = FastAPI(title="POV-Blaster Score API", version="1.0.0")
origins = [origin.strip() for origin in os.environ.get("CORS_ORIGINS", "*").split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


class ScoreSubmission(BaseModel):
    player_name: str = Field(min_length=1, max_length=24)
    kills: int = Field(ge=0, le=1_000_000)


class ScoreRecord(ScoreSubmission):
    id: int
    city: str | None = None
    country: str | None = None
    created_at: str


class WebSessionSubmission(BaseModel):
    player_name: str = Field(min_length=1, max_length=24)


class WebSessionRecord(WebSessionSubmission):
    id: int
    ip_address: str | None = None
    city: str | None = None
    country: str | None = None
    created_at: str


def _connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def _initialize_database() -> None:
    with closing(_connect()) as connection:
        with connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    kills INTEGER NOT NULL CHECK (kills >= 0),
                    city TEXT,
                    country TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS web_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    player_name TEXT NOT NULL,
                    ip_address TEXT,
                    city TEXT,
                    country TEXT,
                    created_at TEXT NOT NULL
                )
                """
            )


def _client_ip(request: FastAPIRequest) -> str | None:
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",", 1)[0].strip()
    return request.client.host if request.client else None


def _locate_ip(ip_address: str | None) -> tuple[str | None, str | None]:
    if not ip_address or ip_address in {"127.0.0.1", "::1"}:
        return None, None
    try:
        request = Request(GEOLOCATION_URL.format(quote(ip_address)), headers={"User-Agent": "POV-Blaster/1.0"})
        with urlopen(request, timeout=2) as response:
            payload = response.read().decode("utf-8")
        import json
        location = json.loads(payload)
        return (location.get("city") or None, location.get("country_name") or None)
    except (OSError, URLError, ValueError, TimeoutError):
        return None, None


def _record_from_row(row: sqlite3.Row) -> dict:
    return dict(row)


@app.on_event("startup")
def startup() -> None:
    _initialize_database()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/scores", response_model=list[ScoreRecord])
def list_scores() -> list[dict]:
    """Return every stored score, ordered from highest to lowest kills."""
    with closing(_connect()) as connection:
        rows = connection.execute(
            "SELECT id, player_name, kills, city, country, created_at "
            "FROM scores ORDER BY kills DESC, player_name COLLATE NOCASE ASC, id ASC"
        ).fetchall()
    return [_record_from_row(row) for row in rows]


@app.post("/scores", response_model=ScoreRecord, status_code=201)
def create_score(submission: ScoreSubmission, request: FastAPIRequest) -> dict:
    player_name = submission.player_name.strip()
    if not player_name:
        raise HTTPException(status_code=422, detail="Player name cannot be empty.")
    city, country = _locate_ip(_client_ip(request))
    created_at = datetime.now(timezone.utc).isoformat()
    with closing(_connect()) as connection:
        with connection:
            cursor = connection.execute(
                "INSERT INTO scores (player_name, kills, city, country, created_at) VALUES (?, ?, ?, ?, ?)",
                (player_name, submission.kills, city, country, created_at),
            )
            row = connection.execute(
                "SELECT id, player_name, kills, city, country, created_at FROM scores WHERE id = ?",
                (cursor.lastrowid,),
            ).fetchone()
    return _record_from_row(row)


@app.post("/sessions", response_model=WebSessionRecord, status_code=201)
def create_session(submission: WebSessionSubmission, request: FastAPIRequest) -> dict:
    """Record a web session with player name and IP geolocation."""
    player_name = submission.player_name.strip()
    if not player_name:
        raise HTTPException(status_code=422, detail="Player name cannot be empty.")
    ip_address = _client_ip(request)
    city, country = _locate_ip(ip_address)
    created_at = datetime.now(timezone.utc).isoformat()
    with closing(_connect()) as connection:
        with connection:
            cursor = connection.execute(
                "INSERT INTO web_sessions (player_name, ip_address, city, country, created_at) VALUES (?, ?, ?, ?, ?)",
                (player_name, ip_address, city, country, created_at),
            )
            row = connection.execute(
                "SELECT id, player_name, ip_address, city, country, created_at FROM web_sessions WHERE id = ?",
                (cursor.lastrowid,),
            ).fetchone()
    return _record_from_row(row)


@app.get("/sessions", response_model=list[WebSessionRecord])
def list_sessions() -> list[dict]:
    """Return all recorded web sessions."""
    with closing(_connect()) as connection:
        rows = connection.execute(
            "SELECT id, player_name, ip_address, city, country, created_at "
            "FROM web_sessions ORDER BY created_at DESC"
        ).fetchall()
    return [_record_from_row(row) for row in rows]
