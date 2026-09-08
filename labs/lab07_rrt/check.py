"""CHECK — Lab 07. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

import numpy as np

from flightlab.checks import Criterion, assert_true, run_table
from flightlab.resolve import ROOT, _load_file
from flightlab.worlds import forest_lab07

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "Nearest node, steer a fixed step, keep it if collide_segment is false. Bias samples at the goal.",
    "RRT*: in a radius, pick the parent with smallest path cost, then rewire neighbors.",
    "Shortcut: from i, jump to the farthest j whose segment is free.",
    "If success < 90%, raise n_iter or goal_bias — the forest is supposed to be easy.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab07_rrt")
    return _load_file(LAB_DIR / "lab.py", "lab07_student_check")


def _length(path: np.ndarray) -> float:
    if len(path) < 2:
        return np.inf
    return float(np.sum(np.linalg.norm(np.diff(path, axis=0), axis=1)))


def criteria(impl) -> list[Criterion]:
    field, start, goal = forest_lab07()

    def collision_free_and_success():
        ok = 0
        n = 50
        for seed in range(n):
            path, _, _ = impl.rrt(field, start, goal, seed=seed, n_iter=350)
            if len(path) < 2:
                continue
            if np.linalg.norm(path[0] - start) > 1e-6:
                continue
            if np.linalg.norm(path[-1] - goal) > 0.35:
                continue
            hit = any(field.collide_segment(path[i], path[i + 1]) for i in range(len(path) - 1))
            if not hit:
                ok += 1
        rate = ok / n
        assert_true(rate >= 0.90, f"success {rate:.0%} over 50 seeds (need ≥90%)")

    def star_cheaper():
        costs_r, costs_s = [], []
        for seed in range(12):
            pr, _, _ = impl.rrt(field, start, goal, seed=seed, n_iter=350)
            ps, _, _ = impl.rrt_star(field, start, goal, seed=seed, n_iter=350)
            if len(pr) >= 2 and len(ps) >= 2:
                costs_r.append(_length(pr))
                costs_s.append(_length(ps))
        assert_true(len(costs_s) >= 8, "RRT* failed too often")
        assert_true(
            float(np.mean(costs_s)) < float(np.mean(costs_r)),
            f"RRT* mean {np.mean(costs_s):.2f} should beat RRT {np.mean(costs_r):.2f}",
        )

    def shortcut_works():
        path, _, _ = impl.rrt(field, start, goal, seed=1, n_iter=400)
        short = impl.shortcut(path, field)
        assert_true(len(short) >= 2, "shortcut returned empty")
        hit = any(field.collide_segment(short[i], short[i + 1]) for i in range(len(short) - 1))
        assert_true(not hit, "shortcut walked through an obstacle")
        assert_true(len(short) <= len(path), "shortcut should not add vertices")

    return [
        Criterion("TODO 1 — collision-free, success ≥90% / 50 seeds", collision_free_and_success, HINTS[0]),
        Criterion("TODO 2 — RRT* mean cost < RRT", star_cheaper, HINTS[1]),
        Criterion("TODO 3 — shortcut stays free and shorter-or-equal", shortcut_works, HINTS[2]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 07 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 07 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 07 — Sampling Your Way Out  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
