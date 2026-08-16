#!/usr/bin/env python3
"""HermesZen ADK — Git Agent.

Commits daily work to the repo and pushes via SSH deploy key.
No LLM needed — pure script (fast, reliable).
"""
import os
import subprocess
from datetime import date
from pathlib import Path

REPO = Path(os.environ.get("ADK_REPO_DIR", "/home/SURFACE/hermeszen-adk"))
WORK = Path(os.environ.get("ADK_WORK_DIR", str(REPO / "work")))


def git(*args: str, cwd: Path = REPO) -> str:
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return (r.stdout or "").strip() + ("\n" + r.stderr if r.stderr else "").strip()


def commit_day(task_title: str) -> dict:
    """Commit today's work folder + push. Returns {commit, pushed}."""
    today = date.today().isoformat()
    folder = WORK / today
    git("add", "-A")
    # skip if nothing new
    diff = git("diff", "--cached", "--stat")
    if not diff:
        return {"commit": None, "pushed": False, "note": "nothing to commit"}

    msg = f"feat({today}): {task_title}"
    commit = git("commit", "-m", msg).split("\n")[0]
    push = git("push", "origin", "main")
    ok = "main" in push and "->" in push or "up to date" in push or "Everything" in push
    return {"commit": commit, "pushed": ok, "note": push[-80:]}


if __name__ == "__main__":
    import sys
    title = sys.argv[1] if len(sys.argv) > 1 else "daily work"
    print(commit_day(title))