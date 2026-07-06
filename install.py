#!/usr/bin/env python3
"""
Install the local-eyes skill into Claude Code.

Copies vision.py, SKILL.md, and config.json to ~/.claude/skills/local-eyes/
"""

import os
import sys
import shutil
from pathlib import Path

SKILL_NAME = "local-eyes"
SKILLS_DIR = Path.home() / ".claude" / "skills" / SKILL_NAME

FILES = {
    "vision.py":    "core vision script",
    "SKILL.md":     "skill instructions for Claude",
    "config.json":  "settings (model, host, timeout)",
}


def main():
    project_dir = Path(__file__).resolve().parent

    print(f"Installing '{SKILL_NAME}' into Claude Code...")
    print()
    print(f"  Source: {project_dir}")
    print(f"  Target: {SKILLS_DIR}")
    print()

    SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    for src_name, desc in FILES.items():
        src = project_dir / src_name
        dst = SKILLS_DIR / src_name

        if not src.exists():
            print(f"  SKIP  {src_name} ({desc}) — not found")
            continue

        shutil.copy2(src, dst)
        print(f"  COPY  {src_name} -> {dst}")

    # Make vision.py executable on non-Windows
    vision_py = SKILLS_DIR / "vision.py"
    if vision_py.exists() and os.name != "nt":
        vision_py.chmod(0o755)

    print()
    print("Done. The skill is installed.")
    print()
    print("Quick test:")
    print("  1. Press Win+Shift+S to take a screenshot")
    print(f"  2. Run: python \"{SKILLS_DIR / 'vision.py'}\"")
    print("  3. You should see a description of your screenshot")
    print()
    print("Now just mention a screenshot in Claude Code and it'll use its eyes.")


if __name__ == "__main__":
    main()
