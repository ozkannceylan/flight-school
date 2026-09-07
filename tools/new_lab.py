#!/usr/bin/env python3
"""Scaffold a lab directory from tools/templates/lab.

    python tools/new_lab.py 02 "Into 3D, and the First Loop" --slug into_3d
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "tools/templates/lab"


def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")[:32]


def render(text: str, mapping: dict[str, str]) -> str:
    for k, v in mapping.items():
        text = text.replace(f"{{{{{k}}}}}", v)
    return text


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Create labs/labNN_slug/ from the template.")
    p.add_argument("number", help="lab number, e.g. 02")
    p.add_argument("title", help='human title, e.g. "Into 3D"')
    p.add_argument("--slug", default="", help="folder suffix (default: slugified title)")
    p.add_argument("--force", action="store_true")
    args = p.parse_args(argv)

    num = args.number.zfill(2)
    slug = args.slug or slugify(args.title)
    dest = ROOT / "labs" / f"lab{num}_{slug}"
    if dest.exists() and not args.force:
        print(f"refusing to overwrite {dest} (pass --force)", file=sys.stderr)
        return 1

    mapping = {
        "NUM": num,
        "TITLE": args.title,
        "SLUG": slug,
        "FOLDER": dest.name,
    }
    dest.mkdir(parents=True, exist_ok=True)
    for src in TEMPLATE.iterdir():
        if src.is_file():
            (dest / src.name).write_text(render(src.read_text(), mapping), encoding="utf-8")
    print(f"created {dest.relative_to(ROOT)}")
    print("next: add a row to PROGRESS.md and a resolve.LabSpec.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
