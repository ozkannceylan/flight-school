#!/usr/bin/env python3
"""README sections → timed narration beats (not prose).

ARCHITECTURE §7: you narrate; this tool only sequences. Optional `--regen`
runs that lab's demo.py so the gif/thumb is a deterministic diff.

    python tools/screencast.py --lab 17
    python tools/screencast.py --all
    python tools/screencast.py --lab 00 --regen
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABS = ROOT / "labs"
BUILD = ROOT / "build"

HEADING = re.compile(r"^(#{2,3})\s+(.*)$")
# Rough seconds per beat; a 45-min lab's README is a 90-second voiceover.
BEAT_S = {
    "Why now?": 12,
    "What's the idea?": 25,
    "What will you see?": 10,
    "Cold Start": 15,
    "STOP HERE — good stopping point": 8,
    "Run": 8,
}


def lab_dir(number: str) -> Path:
    n = number.zfill(2)
    hits = sorted(LABS.glob(f"lab{n}_*"))
    if not hits:
        raise FileNotFoundError(f"no labs/lab{n}_*")
    return hits[0]


def beats_from_readme(readme: Path) -> list[tuple[int, str, str]]:
    """Return (seconds, heading, one-line cue) for each ## / ###."""
    lines = readme.read_text(encoding="utf-8").splitlines()
    sections: list[tuple[str, list[str]]] = []
    current = None
    buf: list[str] = []
    for line in lines:
        m = HEADING.match(line)
        if m:
            if current is not None:
                sections.append((current, buf))
            current = m.group(2).strip()
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        sections.append((current, buf))

    beats = []
    for heading, body in sections:
        cue = next(
            (
                b.strip()
                for b in body
                if b.strip()
                and len(b.strip()) > 24
                and not b.strip().startswith("```")
                and not b.strip().startswith("![")
                and not b.strip().startswith("-")
            ),
            heading,
        )
        if len(cue) > 110:
            cue = cue[:107] + "…"
        beats.append((BEAT_S.get(heading, 10), heading, cue))
    return beats


def write_script(number: str) -> Path:
    folder = lab_dir(number)
    readme = folder / "README.md"
    title = readme.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
    beats = beats_from_readme(readme)
    t = 0
    rows = ["# Screencast beats — do not narrate this file verbatim\n", f"**{title}** · `{folder.relative_to(ROOT)}`\n", "| t | s | beat | cue |", "|---|---|---|---|"]
    for sec, heading, cue in beats:
        rows.append(f"| {t:02d} | {sec} | {heading} | {cue} |")
        t += sec
    rows.append(f"\nTotal ≈ {t}s. Record the demo gif (`make lab{number.zfill(2)}`), then cut to these beats.\n")
    BUILD.mkdir(parents=True, exist_ok=True)
    dest = BUILD / f"lab{number.zfill(2)}_script.md"
    dest.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return dest


def regen_demo(number: str) -> None:
    folder = lab_dir(number)
    demo = folder / "demo.py"
    if not demo.is_file():
        print(f"no demo.py in {folder}", file=sys.stderr)
        return
    subprocess.run([sys.executable, str(demo)], cwd=ROOT, check=True, env={**dict(**{k: v for k, v in __import__("os").environ.items()}), "MPLBACKEND": "Agg"})


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="README → narration beats under build/")
    p.add_argument("--lab", default="", help="lab number, e.g. 17")
    p.add_argument("--all", action="store_true")
    p.add_argument("--regen", action="store_true", help="also run that lab's demo.py")
    args = p.parse_args(argv)
    if not args.lab and not args.all:
        p.error("pass --lab NN or --all")
    nums = []
    if args.all:
        nums = [d.name[3:5] for d in sorted(LABS.glob("lab??_*")) if d.name[3:5].isdigit()]
    else:
        nums = [args.lab]
    for n in nums:
        dest = write_script(n)
        print(f"wrote {dest.relative_to(ROOT)}")
        if args.regen:
            regen_demo(n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
