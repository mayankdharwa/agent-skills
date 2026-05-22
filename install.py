#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

MARKETPLACE = "mayank-skills"
GITHUB_REPO = "mayankdharwa/agent-skills"
PLUGIN_KEY = f"{MARKETPLACE}@{MARKETPLACE}"

CLAUDE_DIR = Path.home() / ".claude"


def run(cmd):
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        sys.exit(f"Command failed: {cmd}")


def main():
    if not CLAUDE_DIR.exists():
        sys.exit("Error: ~/.claude not found. Install Claude Code first.")

    print(f"Installing {PLUGIN_KEY} ...")

    run(f"claude plugin marketplace add {GITHUB_REPO}")
    print("  marketplace registered")

    run(f"claude plugin install {PLUGIN_KEY}")
    print("  plugin installed")

    print("\nDone. Skills are ready.")


if __name__ == "__main__":
    main()
