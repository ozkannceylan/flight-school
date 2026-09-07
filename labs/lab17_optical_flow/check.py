"""CHECK — Lab 17. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

import numpy as np

from flightlab.checks import Criterion, assert_true, run_table
from flightlab.dynamics import PlanarQuadrotor
from flightlab.integrate import rollout
from flightlab.render import (
    FX,
    IMG_H,
    IMG_W,
    analytic_flow,
    blank,
    wavy,
    default_K,
    render_ground,
    sample_track_points,
)
from flightlab.resolve import ROOT, _load_file

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "Ix, Iy = np.gradient(I1); It = I2−I1. lstsq on the window. Order is (u, v) = (x, y).",
    "u_pix ≈ −fx vy / z  for a downward camera. Mean u, invert.",
    "A textureless patch makes G singular — LK noise, not signal.",
    "Swap true vy for vy_flow in a simple PD. It should almost hover.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab17_optical_flow")
    return _load_file(LAB_DIR / "lab.py", "lab17_student_check")


def criteria(impl) -> list[Criterion]:
    K = default_K()
    py, pz, th = 0.0, 1.5, 0.0
    dpy = 0.012
    I1 = render_ground(py, pz, th, texture=wavy)
    I2 = render_ground(py + dpy, pz, th, texture=wavy)
    pts = sample_track_points(IMG_W, IMG_H, n=25, margin=16)
    gt = analytic_flow(K, py, pz, th, dpy, 0.0, 0.0, pts)

    def flow_accurate():
        fl = impl.lucas_kanade(I1, I2, pts, win=6)
        err = np.nanmean(np.linalg.norm(fl - gt, axis=1))
        assert_true(err < 0.45, f"mean flow error {err:.3f} px (need <0.45)")

    def textureless_fails():
        B1 = render_ground(py, pz, th, texture=blank)
        B2 = render_ground(py + dpy, pz, th, texture=blank)
        fl = impl.lucas_kanade(B1, B2, pts, win=6)
        err = np.nanmean(np.linalg.norm(fl - gt, axis=1))
        assert_true(err > 0.6, f"textureless error {err:.3f} should be large")

    def vy_ok():
        fl = impl.lucas_kanade(I1, I2, pts, win=6)
        vy = impl.flow_to_vy(fl, FX, pz)
        assert_true(abs(vy - dpy) < 0.008, f"vŷ={vy:.3f} vs {dpy:.3f}")

    def hover_almost():
        plant = PlanarQuadrotor()
        x0 = plant.reset() + np.array([0.12, 0.0, 0.0, 0.0, 0.0, 0.0])

        def pi_full(x, _t):
            return impl.flow_hover_pd(
                x[0], x[1], x[2], x[3], x[4], x[5], m=plant.m, g=plant.g, L=plant.L, I=plant.I
            )

        def pi_flow_biased(x, _t):
            return impl.flow_hover_pd(
                x[0], x[1], x[2], 0.85 * x[3], x[4], x[5], m=plant.m, g=plant.g, L=plant.L, I=plant.I
            )

        _, xs_f, _ = rollout(plant.f, x0, dt=0.03, t_end=2.0, policy=pi_full)
        _, xs_b, _ = rollout(plant.f, x0, dt=0.03, t_end=2.0, policy=pi_flow_biased)
        drift_f = float(np.max(np.abs(xs_f[:, 0])))
        drift_b = float(np.max(np.abs(xs_b[:, 0])))
        assert_true(drift_f < 0.20, f"full-state drift {drift_f:.3f}")
        assert_true(drift_b < 10.0 * drift_f + 0.05, f"flow hover {drift_b:.3f} vs full {drift_f:.3f}")

    return [
        Criterion("LK flow error vs analytic GT", flow_accurate, HINTS[0]),
        Criterion("textureless region fails", textureless_fails, HINTS[2]),
        Criterion("flow inverts to the true Δy", vy_ok, HINTS[1]),
        Criterion("flow-velocity hover stays within 10× full-state", hover_almost, HINTS[3]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 17 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 17 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 17 — Motion From Brightness  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
