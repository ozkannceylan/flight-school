#!/usr/bin/env python3
"""Pick an unlocked, unfinished lab (``make random``)."""

from __future__ import annotations

import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILT = {
    "00": "lab00_hello_state",
    "01": "lab01_planar_dynamics",
    "02": "lab02_into_3d",
    "03": "lab03_cascade_pd",
    "04": "lab04_lqr",
}


def main() -> int:
    text = (ROOT / "PROGRESS.md").read_text(encoding="utf-8")
    open_ids = re.findall(r"- \[ \] \*\*Lab (\d+)\*\*", text)
    unlocked = [n.zfill(2) for n in open_ids if n.zfill(2) in BUILT]
    if not unlocked:
        print("all done (or nothing built yet).")
        return 0
    choice = random.choice(unlocked)
    folder = BUILT[choice]
    print(f"Lab {choice} — run: make lab{choice}   (labs/{folder})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
