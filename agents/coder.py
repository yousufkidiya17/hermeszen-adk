#!/usr/bin/env python3
"""HermesZen ADK — Coder Agent.

Writes the planned project using tools (write_file, run_bash for syntax check).
"""
from agents.llm_base import build_model, run_agent
from agents.tools import make_tools
from google.adk.agents import LlmAgent

SYSTEM = """
You are a Python developer agent. You build SMALL single-file projects.

Rules:
- Use the write_file tool to save code. Filename comes from the plan (FILE: ...).
- Keep it under 80 lines. No external dependencies beyond stdlib.
- After writing, call run_bash with:
  python3 -c "compile(open('<file>').read(), '<file>', 'exec')"
  to syntax-check. If it fails, fix the file and re-check.
- Reply with: DONE <filename> — <what it does>
"""


def build_task(title: str, plan: str) -> str:
    """Build one project from the planner's title+plan."""
    prompt = f"TITLE: {title}\nPLAN: {plan}\n\nNow create the file."
    model = build_model()
    agent = LlmAgent(
        name="coder_agent",
        model=model,
        instruction=SYSTEM,
        tools=make_tools(),
    )
    return run_agent(agent, prompt, session_id="coder")


if __name__ == "__main__":
    # test: pass a plan directly
    print(build_task("weather-cli", "weather.py that calls wttr.in and prints temp"))