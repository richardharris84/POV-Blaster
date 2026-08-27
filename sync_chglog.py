"""Synchronize a marked CHANGELOG section with recent Git and prompt activity.

The script preserves hand-written changelog entries and replaces only the
section between the AUTOMATED 72-HOUR SYNC markers. Copilot session data is
private to VS Code, so prompt/output excerpts are included only when a JSONL
session export is supplied with --session-log.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

START_MARKER = "<!-- AUTOMATED 72-HOUR SYNC:START -->"
END_MARKER = "<!-- AUTOMATED 72-HOUR SYNC:END -->"


def _run_git(repo_root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout


def _recent_commits(repo_root: Path, since: datetime) -> list[tuple[str, str, str]]:
    since_arg = since.astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
    output = _run_git(
        repo_root,
        "log",
        "--all",
        f"--since={since_arg}",
        "--date=short",
        "--pretty=format:%h%x09%ad%x09%s",
    )
    commits = []
    for line in output.splitlines():
        parts = line.split("\t", 2)
        if len(parts) == 3:
            commits.append((parts[0], parts[1], parts[2]))
    return commits


def _recent_prompt_files(repo_root: Path, since: datetime) -> list[str]:
    output = _run_git(
        repo_root,
        "log",
        "--all",
        f"--since={since.astimezone().strftime('%Y-%m-%dT%H:%M:%S%z')}",
        "--name-only",
        "--pretty=format:",
        "--",
        "*.prompt.md",
        ".github/prompts",
    )
    paths = {
        line.strip().replace("\\", "/")
        for line in output.splitlines()
        if line.strip().endswith(".prompt.md")
    }
    ignored_parts = {".git", "build", "__pycache__"}
    for path in repo_root.rglob("*.prompt.md"):
        if ignored_parts.intersection(path.parts):
            continue
        modified_at = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
        if modified_at >= since:
            paths.add(path.relative_to(repo_root).as_posix())
    return sorted(paths)


def _session_excerpts(session_log: Path | None) -> list[tuple[str, str]]:
    if session_log is None or not session_log.is_file():
        return []
    excerpts = []
    for line in session_log.read_text(encoding="utf-8").splitlines():
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(payload, dict):
            continue
        for key, label in (("user_message", "Prompt"), ("user", "Prompt"), ("assistant_response", "Output"), ("assistant", "Output")):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                compact = " ".join(value.split())
                excerpts.append((label, compact[:240]))
    return excerpts[-20:]


def _bullet_list(items: list[str], empty: str) -> list[str]:
    return [f"- {item}" for item in items] if items else [f"- {empty}"]


def _render_section(commits, prompt_files, excerpts, generated_at: str, hours: int) -> str:
    lines = [
        START_MARKER,
        "## Automated 72-Hour Sync",
        "",
        f"Generated: {generated_at} (window: last {hours} hours)",
        "",
        "### Git Commits",
        "",
    ]
    lines.extend(
        _bullet_list(
            [f"`{short}` ({date}) {subject}" for short, date, subject in commits],
            "No Git commits found in the selected window.",
        )
    )
    lines.extend(["", "### Prompt Files Changed", ""])
    lines.extend(_bullet_list([f"[`{path}`]({path})" for path in prompt_files], "No prompt files changed in the selected window."))
    lines.extend(["", "### Copilot Prompt/Output Excerpts", ""])
    if excerpts:
        lines.extend(f"- **{label}:** {text}" for label, text in excerpts)
    else:
        lines.append("- No session log supplied; pass `--session-log <path>` to include excerpts.")
    lines.extend(["", END_MARKER])
    return "\n".join(lines)


def _update_changelog(changelog: Path, section: str) -> None:
    content = changelog.read_text(encoding="utf-8")
    start = content.find(START_MARKER)
    end = content.find(END_MARKER)
    if (start >= 0) != (end >= 0):
        raise ValueError("CHANGELOG.md contains only one automated sync marker")
    if start >= 0:
        end += len(END_MARKER)
        content = content[:start].rstrip() + "\n\n" + section + content[end:]
    else:
        content = content.rstrip() + "\n\n" + section + "\n"
    changelog.write_text(content, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync CHANGELOG.md with recent Git and Copilot prompt activity.")
    parser.add_argument("--hours", type=int, default=72, help="Look-back window in hours (default: 72).")
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parent, help="Repository root.")
    parser.add_argument("--changelog", type=Path, default=None, help="Changelog path, relative to --repo by default.")
    parser.add_argument("--session-log", type=Path, default=None, help="Optional Copilot JSONL session export.")
    args = parser.parse_args()
    if args.hours <= 0:
        parser.error("--hours must be greater than zero")

    repo_root = args.repo.resolve()
    changelog = (args.changelog or repo_root / "CHANGELOG.md").resolve()
    since = datetime.now(timezone.utc) - timedelta(hours=args.hours)
    commits = _recent_commits(repo_root, since)
    prompt_files = _recent_prompt_files(repo_root, since)
    excerpts = _session_excerpts(args.session_log.resolve() if args.session_log else None)
    section = _render_section(commits, prompt_files, excerpts, datetime.now().astimezone().isoformat(timespec="seconds"), args.hours)
    _update_changelog(changelog, section)
    print(f"Updated {changelog} with {len(commits)} commits and {len(prompt_files)} prompt files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
