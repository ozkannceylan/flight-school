"""CHECK — Lab 10. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

import numpy as np

from flightlab.checks import Criterion, assert_true, run_table
from flightlab.resolve import ROOT, _load_file
from flightlab.worlds import rooms_lab10, start_lab10, successors, wall_adjacent, wall_adjacent_mask

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "predict: OR together successors(grid, cell, action) for every True cell.",
    "update is intersection: belief & consistent.",
    "Without a measurement, pass consistent=None so the set only grows.",
    "If predict is a superset of the motion model, the true cell cannot escape.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab10_set_belief")
    return _load_file(LAB_DIR / "lab.py", "lab10_student_check")


def criteria(impl) -> list[Criterion]:
    grid = rooms_lab10()
    start = start_lab10()
    adj = wall_adjacent_mask(grid)
    actions = ((0, 1), (0, 1), (-1, 0), (0, -1), (1, 0))

    def grows_open_loop():
        bel = np.zeros((grid.rows, grid.cols), dtype=bool)
        bel[start] = True
        sizes = [int(bel.sum())]
        for a in actions:
            bel = impl.step(bel, grid, a, None)
            sizes.append(int(bel.sum()))
        assert_true(sizes[-1] > sizes[0], f"open-loop sizes {sizes} should grow")

    def shrinks_with_sensor():
        full = ~grid.occ
        cut = impl.update(full, adj)
        assert_true(int(cut.sum()) < int(full.sum()), "update should drop inconsistent cells")
        assert_true(bool(cut.any()), "do not wipe the whole set")

    def containment():
        n_ok = 0
        for seed in range(100):
            rr = np.random.default_rng(seed)
            truth = start
            bel = np.zeros((grid.rows, grid.cols), dtype=bool)
            bel[truth] = True
            ok = True
            for t in range(12):
                a = actions[t % len(actions)]
                opts = list(successors(grid, truth, a))
                if not opts:
                    ok = False
                    break
                truth = opts[int(rr.integers(0, len(opts)))]
                z = wall_adjacent(grid, truth)
                consistent = adj if z else (~adj & ~grid.occ)
                bel = impl.step(bel, grid, a, consistent)
                if not bel[truth]:
                    ok = False
                    break
            n_ok += int(ok)
        assert_true(n_ok == 100, f"true cell escaped the set on {100 - n_ok}/100 seeds")

    return [
        Criterion("open-loop set grows without measurements", grows_open_loop, HINTS[2]),
        Criterion("update intersects and shrinks the set", shrinks_with_sensor, HINTS[1]),
        Criterion("true cell stays inside the set, 100 seeds", containment, HINTS[3]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 10 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 10 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 10 — Where Could I Possibly Be?  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
