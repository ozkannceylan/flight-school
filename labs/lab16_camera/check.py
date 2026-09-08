"""CHECK — Lab 16. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

import numpy as np

from flightlab.checks import Criterion, assert_true, run_table
from flightlab.render import camera_from_planar, default_K, landmarks_lab16, pose_lab16
from flightlab.render.camera import project as project_ref
from flightlab.resolve import ROOT, _load_file

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "Xc = R @ (X − C). Then u = fx X/Z + cx. Depth is Xc[2], not world z.",
    "xn = Xc/Zc. Stack [xn, 1] and lstsq against u. Same for v.",
    "RMSE of pixel residuals. Hover K is ~200 px, principal point at the image centre.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab16_camera")
    return _load_file(LAB_DIR / "lab.py", "lab16_student_check")


def criteria(impl) -> list[Criterion]:
    K = default_K()
    py, pz, th = pose_lab16()
    R, C = camera_from_planar(py, pz, th)
    X = landmarks_lab16(5)
    uv = project_ref(K, R, C, X)

    def project_ok():
        hat = impl.project(K, R, C, X)
        err = np.nanmax(np.abs(hat - uv))
        assert_true(err < 1e-8, f"project mismatch {err:.3e}")

    def calib_ok():
        uv_n = uv + np.random.default_rng(0).normal(0.0, 0.04, size=uv.shape)
        Kh = impl.calibrate_K(X, uv_n, R, C)
        rel = np.abs(Kh - K) / np.maximum(np.abs(K), 1.0)
        assert_true(rel[0, 0] < 0.02 and rel[1, 1] < 0.02, f"focal rel err {rel[0,0]:.3f}, {rel[1,1]:.3f}")
        assert_true(rel[0, 2] < 0.02 and rel[1, 2] < 0.02, f"principal-point rel err {rel[0,2]:.3f}")

    def rmse_ok():
        uv_n = uv + np.random.default_rng(1).normal(0.0, 0.05, size=uv.shape)
        Kh = impl.calibrate_K(X, uv_n, R, C)
        e = impl.reprojection_error(Kh, R, C, X, uv_n)
        assert_true(e < 0.5, f"reprojection RMSE {e:.3f} px (need <0.5)")

    return [
        Criterion("TODO 1 — pinhole matches the reference project", project_ok, HINTS[0]),
        Criterion("TODO 2 — recovered K within 2% of ground truth", calib_ok, HINTS[1]),
        Criterion("TODO 3 — reprojection RMSE < 0.5 px", rmse_ok, HINTS[2]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 16 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 16 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 16 — The Camera Is a Matrix  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
