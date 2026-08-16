#!/usr/bin/env python3
"""HermesZen ADK — shared tools for agents (verified ADK 2.7 API).

FunctionTool(func=...) — simple Python functions as agent tools.
"""
import os
import subprocess
from pathlib import Path

WORK_DIR = Path(os.environ.get("ADK_WORK_DIR", "/home/SURFACE/hermeszen-adk/work"))


def write_file(path: str, content: str) -> str:
    """Write a file (relative to work dir or absolute). Saves code."""
    p = Path(path)
    if not p.is_absolute():
        p = WORK_DIR / p
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return f"WROTE {p} ({len(content)} chars)"


def read_file(path: str) -> str:
    """Read a file's contents."""
    p = Path(path)
    if not p.is_absolute():
        p = WORK_DIR / p
    if not p.exists():
        return f"FILE_NOT_FOUND: {p}"
    return p.read_text(encoding="utf-8")


def list_dir(path: str = ".") -> str:
    """List files in a directory."""
    p = Path(path)
    if not p.is_absolute():
        p = WORK_DIR / p
    if not p.exists():
        return f"DIR_NOT_FOUND: {p}"
    return "\n".join(sorted(str(x.name) for x in p.iterdir()))


def run_bash(command: str, timeout: int = 30) -> str:
    """Run a shell command and return stdout+stderr (syntax check / tests)."""
    try:
        r = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=timeout
        )
        out = (r.stdout or "") + ("\n" + r.stderr if r.stderr else "")
        return f"exit={r.returncode}\n{out[:2000]}"
    except subprocess.TimeoutExpired:
        return f"TIMEOUT after {timeout}s"
    except Exception as e:
        return f"RUN_ERROR: {e}"


TOOLS = [
    {"name": "write_file", "func": write_file},
    {"name": "read_file", "func": read_file},
    {"name": "list_dir", "func": list_dir},
    {"name": "run_bash", "func": run_bash},
]


def make_tools() -> list:
    """Build FunctionTool objects for ADK agents."""
    from google.adk.tools import FunctionTool
    return [FunctionTool(t["func"]) for t in TOOLS]


if __name__ == "__main__":
    print("TOOLS_OK:", [t["name"] for t in TOOLS])