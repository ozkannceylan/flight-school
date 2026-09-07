"""CHECK — Lab 14. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

import numpy as np

from flightlab.checks import Criterion, assert_true, run_table
from flightlab.resolve import ROOT, _load_file
from flightlab.sensors import RangeSensor
from flightlab.worlds import mapping_lab14, mapping_poses_lab14

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "Walk the ray in steps. Cells before z get l_free; the hit cell gets l_occ.",
    "l ← clip(l + increment, ±8). Addition, not multiplication.",
    "Naive: p ← p q / (p q + (1-p)(1-q)) many times. It hits 0.0 in float64.",
    "IoU is over cells you actually observed (|l| > 0.25).",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab14_mapping")
    return _load_file(LAB_DIR / "lab.py", "lab14_student_check")


def _build_map(impl):
    grid = mapping_lab14()
    poses = mapping_poses_lab14()
    sensor = RangeSensor(n_beams=7, fov=np.pi, max_range=6.5, sigma=0.04, step=0.2)
    rng = np.random.default_rng(0)
    l_map = np.zeros(grid.occ.shape, dtype=float)
    for pose in poses:
        z = sensor.measure(pose, grid, rng)
        l_map = impl.integrate_scan(l_map, pose, z, sensor)
    return l_map, grid


def criteria(impl) -> list[Criterion]:
    def iou_ok():
        l_map, grid = _build_map(impl)
        observed = np.abs(l_map) > 0.25
        est = impl.occupancy(l_map)
        gt = grid.occ
        inter = np.logical_and(est, gt)[observed].sum()
        union = np.logical_or(est, gt)[observed].sum()
        iou = float(inter / max(int(union), 1))
        assert_true(iou >= 0.85, f"IoU {iou:.3f} (need ≥0.85) on observed cells")

    def logodds_stable():
        l = 0.0
        dl = float(np.log(0.05 / 0.95))
        for _ in range(400):
            l = float(impl.logodds_update(np.array([l]), np.array([dl]), clip=50.0)[0])
        assert_true(np.isfinite(l), "log-odds became non-finite")
        assert_true(l < -5.0, f"log-odds {l:.2f} should be a large negative after 400 misses")

    def naive_underflows():
        p = impl.naive_miss(0.5, 400, 0.05)
        assert_true(p == 0.0, f"naive p={p} should underflow to 0.0 after 400 misses")

    return [
        Criterion("map IoU vs ground truth ≥ 0.85", iou_ok, HINTS[0]),
        Criterion("log-odds stays finite after many misses", logodds_stable, HINTS[1]),
        Criterion("naive probability underflows to 0", naive_underflows, HINTS[2]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 14 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 14 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 14 — Known Pose, Unknown Map  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
