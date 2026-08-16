#!/usr/bin/env python3
"""HermesZen ADK — Daily Workflow (v1: Planner → Coder → Reviewer → Git).

Runs the team end-to-end and prints a summary. No Telegram yet (v2).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from agents.planner import plan_task
from agents.coder import build_task
from agents.reviewer import review_file
from agents import git as git_agent


def extract_plan(text: str) -> dict:
    """Parse planner output: TITLE / FILE / PLAN lines."""
    title = re.search(r"TITLE:\s*(.+)", text)
    fname = re.search(r"FILE:\s*([\w.\-/]+)", text)
    plan = re.search(r"PLAN:\s*(.+)", text, re.MULTILINE | re.DOTALL)
    return {
        "title": title.group(1).strip() if title else "daily-project",
        "file": fname.group(1).strip() if fname else "project.py",
        "plan": plan.group(1).strip()[:300] if plan else "build it",
    }


def main() -> dict:
    print("=== [1/4] Planner ===")
    plan_text = plan_task()
    print(plan_text[:200])
    plan = extract_plan(plan_text)
    print(f"→ decided: {plan['title']} → {plan['file']}")

    print("=== [2/4] Coder ===")
    code_text = build_task(plan["title"], plan["plan"])
    print(code_text[:200])

    print("=== [3/4] Reviewer ===")
    review = review_file(plan["file"])
    print(review[:200])
    if not review.startswith("PASS"):
        print("⚠ reviewer not fully happy — recorded for next iteration")
        plan["review"] = review[:150]
    else:
        plan["review"] = "PASS"

    print("=== [4/4] Git ===")
    result = git_agent.commit_day(plan["title"])
    print(result)

    plan["git"] = result
    return plan


if __name__ == "__main__":
    summary = main()
    print("\n=== SUMMARY ===")
    print(summary)