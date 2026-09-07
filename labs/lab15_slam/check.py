"""CHECK — Lab 15. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

import numpy as np

from flightlab.checks import Criterion, assert_true, run_table
from flightlab.geometry import ominus
from flightlab.resolve import ROOT, _load_file
from flightlab.worlds import loop_dataset_lab15

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "e = ominus(z, ominus(xi, xj)). Identity measurement + identical poses → 0.",
    "Walk the odom edges with oplus. Pose 0 stays at the origin.",
    "edges = odom + [loop]. Call gauss_newton_step n_iter times.",
    "ATE is RMSE of (x,y). Loop closure should cut it by ≥60%.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab15_slam")
    return _load_file(LAB_DIR / "lab.py", "lab15_student_check")


def criteria(impl) -> list[Criterion]:
    gt, odom, loop, _open = loop_dataset_lab15(n_side=4, drift=0.18, seed=0)

    def error_zero():
        a = np.array([1.0, 2.0, 0.4])
        e = impl.edge_error(a, a, np.zeros(3))
        assert_true(np.linalg.norm(e) < 1e-9, f"identical poses should give 0, got {e}")
        b = np.array([1.5, 2.2, 0.7])
        z = ominus(a, b)
        e2 = impl.edge_error(a, b, z)
        assert_true(np.linalg.norm(e2) < 1e-8, f"true relative should give 0, got {e2}")

    def odom_chain():
        poses = impl.compose_odometry(len(gt), odom)
        assert_true(poses.shape == gt.shape, f"shape {poses.shape}")
        assert_true(np.allclose(poses[0], 0.0), "pose 0 must stay at the origin")
        # drifted chain should miss the origin at the end
        assert_true(np.hypot(poses[-1, 0], poses[-1, 1]) > 0.4, "open loop should drift")

    def loop_helps():
        before = impl.compose_odometry(len(gt), odom)
        after = impl.optimize(before, list(odom) + [loop], n_iter=8)
        a0 = impl.ate(before, gt)
        a1 = impl.ate(after, gt)
        assert_true(a0 > 0.3, f"open-loop ATE {a0:.3f} should be obviously drifted")
        assert_true(a1 <= 0.40 * a0, f"ATE {a0:.3f} → {a1:.3f} (need ≥60% drop)")
        assert_true(np.isfinite(after).all(), "optimize produced NaNs")

    return [
        Criterion("TODO 1 — edge_error is zero on a true measurement", error_zero, HINTS[0]),
        Criterion("TODO 2 — odometry chain starts at 0 and drifts", odom_chain, HINTS[1]),
        Criterion("loop closure cuts ATE by ≥ 60%", loop_helps, HINTS[3]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 15 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 15 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 15 — Both at Once  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
