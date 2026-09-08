"""CHECK — Lab {{NUM}}.

    python labs/{{FOLDER}}/check.py
    python labs/{{FOLDER}}/check.py --reference
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

from flightlab.checks import Criterion, run_table
from flightlab.resolve import _load_file

LAB_DIR = Path(__file__).resolve().parent
HINTS = ["Read the README. Then fill TODO 1."]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.{{FOLDER}}")
    return _load_file(LAB_DIR / "lab.py", "lab{{NUM}}_student_check")


def criteria(impl) -> list[Criterion]:
    def placeholder():
        raise NotImplementedError("author: replace this criterion")

    return [Criterion("TODO 1 — replace me", placeholder, HINTS[0])]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB {{NUM}} hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB {{NUM}} — {{TITLE}}  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
