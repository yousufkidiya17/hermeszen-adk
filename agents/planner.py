#!/usr/bin/env python3
"""HermesZen ADK — Planner Agent v2.

Decides: what to build today — SKIPS already-built projects (checks work/).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agents.llm_base import build_model, run_agent
from google.adk.agents import LlmAgent

WORK_DIR = Path("/home/SURFACE/hermeszen-adk/work")

IDEAS = [
    "todo-api: minimal Flask/FastAPI todo list with JSON storage",
    "quiz-game: 10-question Python quiz from a questions.json file",
    "csv-analyzer: read CSV, print stats (rows, columns, totals)",
    "password-gen: CLI random password generator (strength flags)",
    "markdown-toc: script that adds a table-of-contents to a README",
    "file-organizer: moves files into folders by extension",
    "reminder-cli: terminal reminders stored in JSON",
    "url-shortener: tiny URL hash generator (hash + map file)",
]


def _already_built() -> list:
    """Return names of projects already in work/ (from filenames)."""
    if not WORK_DIR.exists():
        return []
    return [f.stem.lower().replace("_", "-") for f in WORK_DIR.glob("*.py")]


def plan_task() -> str:
    """Pick ONE idea NOT already built."""
    built = _already_built()
    available = [
        i for i in IDEAS
        if not any(b in i.lower() for b in built)
    ]
    if not available:
        available = ["coffee-bot: simple CLI that prints a coffee brewing guide"]

    pick = "\n".join(f"- {i}" for i in available)
    prompt = (
        "You are a project planner. Pick ONE idea from the pool below and "
        "write a tiny build plan (3-4 lines): what file to create, what it does.\n\n"
        f"POOL:\n{pick}\n\n"
        "Respond with:\n"
        "TITLE: <name>\n"
        "FILE: <filename.py>\n"
        "PLAN: <2-3 lines what the code does>"
    )
    model = build_model()
    agent = LlmAgent(
        name="planner_agent",
        model=model,
        instruction="You are a concise project planner. Never repeat an idea.",
    )
    return run_agent(agent, prompt, session_id="planner")


if __name__ == "__main__":
    print("already built:", _already_built())
    print(plan_task())