"""tools/new_lab.py scaffolds a lab folder from the template."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_new_lab_scaffold():
    dest = ROOT / "labs" / "lab98_unit_smoke"
    if dest.exists():
        for p in dest.iterdir():
            p.unlink()
        dest.rmdir()
    try:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools/new_lab.py"), "98", "Unit Smoke", "--slug", "unit_smoke"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        assert proc.returncode == 0, proc.stderr
        assert (dest / "lab.py").is_file()
        assert (dest / "check.py").is_file()
        assert "{{NUM}}" not in (dest / "README.md").read_text()
        assert "Lab 98" in (dest / "README.md").read_text()
    finally:
        if dest.exists():
            for p in dest.iterdir():
                p.unlink()
            dest.rmdir()
