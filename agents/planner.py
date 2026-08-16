#!/usr/bin/env python3
"""HermesZen ADK — Planner Agent.

Decides: what to build today. Returns a short task plan as text.
"""
from agents.llm_base import build_model, run_agent
from google.adk.agents import LlmAgent

IDEAS = [
    "weather-cli: terminal weather checker (no API key, uses wttr.in)",
    "todo-api: minimal Flask/FastAPI todo list with JSON storage",
    "quiz-game: 10-question Python quiz from a questions.json file",
    "csv-analyzer: read CSV, print stats (rows, columns, totals)",
    "password-gen: CLI random password generator (strength flags)",
    "markdown-toc: script that adds a table-of-contents to a README",
]


def plan_task() -> str:
    """Pick one idea from the pool and make a short build plan."""
    pick = "\n".join(f"- {i}" for i in IDEAS)
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
        instruction="You are a concise project planner.",
    )
    return run_agent(agent, prompt, session_id="planner")


if __name__ == "__main__":
    print(plan_task())