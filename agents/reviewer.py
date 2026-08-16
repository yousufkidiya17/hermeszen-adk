#!/usr/bin/env python3
"""HermesZen ADK — Reviewer Agent.

Checks the coder's file: syntax, logic, security basics. Returns PASS or FIX list.
"""
from agents.llm_base import build_model, run_agent
from agents.tools import make_tools
from google.adk.agents import LlmAgent

SYSTEM = """
You are a code reviewer for small Python projects. Rule: be strict but fair.

Steps:
1. read_file the project file.
2. run_bash: python3 -c "compile(open('<file>').read(), '<file>', 'exec')"
3. Check for security basics: no eval/exec of user input, no hardcoded secrets,
   no unsafe subprocess shell=True with user input.
4. Reply EXACTLY with one line:
   PASS — <one line why it's fine>
   or
   FIX — <list the specific problems, max 2>
"""


def review_file(filename: str) -> str:
    """Review a written file. Returns PASS... or FIX..."""
    prompt = f"Review this file: {filename}"
    model = build_model()
    agent = LlmAgent(
        name="reviewer_agent",
        model=model,
        instruction=SYSTEM,
        tools=make_tools(),
    )
    return run_agent(agent, prompt, session_id="reviewer")


if __name__ == "__main__":
    print(review_file("weather.py"))