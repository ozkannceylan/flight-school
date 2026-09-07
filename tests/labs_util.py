"""Helpers for invoking lab check.py from pytest."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_check(rel: str, *, reference: bool = False) -> int:
    cmd = [sys.executable, str(ROOT / rel)]
    if reference:
        cmd.append("--reference")
    proc = subprocess.run(cmd, cwd=ROOT, check=False)
    return proc.returncode
