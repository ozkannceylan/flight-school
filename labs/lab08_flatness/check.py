"""CHECK — Lab 08. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

import numpy as np

from flightlab.checks import Criterion, assert_close, assert_true, run_table
from flightlab.control import linearize
from flightlab.dynamics import PlanarQuadrotor
from flightlab.integrate import rollout
from flightlab.planning.flatness import flat_to_xu as flat_ref
from flightlab.resolve import ROOT, _load_file, get

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "θ = atan2(−ÿ, z̈+g). T = m*hypot(ÿ, z̈+g). Differentiate θ for ω, θ̈; τ = I θ̈.",
    "Loop eval_piecewise on y and z, then your flat_to_xu. durations = scale * DURATIONS.",
    "u = u_nom − K (x − x_nom). FB-only swaps u_nom for hover.",
    "Start on the trajectory. FF should almost cancel the plant; FB-only lags.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab08_flatness")
    return _load_file(LAB_DIR / "lab.py", "lab08_student_check")


def _K(plant):
    lab04 = get("lab04")
    A, B = linearize(plant.f, plant.reset(), plant.hover_input())
    Q, R = lab04.design_QR()
    K, _ = lab04.lqr(A, B, Q, R)
    return K


def _rmse(xs, xnom):
    e = xs[:, :2] - xnom[:, :2]
    return float(np.sqrt(np.mean(e**2)))


def criteria(impl) -> list[Criterion]:
    plant = PlanarQuadrotor()

    def invert_matches():
        x, u = impl.flat_to_xu(0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, plant)
        xr, ur = flat_ref(0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, plant)
        assert_close(x, xr, atol=1e-8, msg=f"hover state {x}")
        assert_close(u, ur, atol=1e-8, msg=f"hover u {u}")
        # accelerating +y should command negative θ (thrust tilts left? ÿ>0 → θ < 0)
        x2, _ = impl.flat_to_xu(0.0, 1.0, 0.0, 0.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, plant)
        assert_true(x2[2] < 0, f"ÿ>0 should give θ<0, got {x2[2]:.3f}")

    def samples_hover_at_t0():
        t, xs, us = impl.sample_flat_traj(plant, dt=0.05, scale=1.0)
        assert_true(len(t) > 10, "trajectory too short")
        assert_close(xs[0, :2], impl.WAYPOINTS[0], atol=1e-6, msg=f"start {xs[0,:2]}")
        assert_close(xs[-1, :2], impl.WAYPOINTS[-1], atol=5e-3, msg=f"end {xs[-1,:2]}")

    def ff_beats_fb():
        K = _K(plant)
        t, xnom, unom = impl.sample_flat_traj(plant, dt=0.02, scale=1.0)
        u_h = plant.hover_input()
        x0 = xnom[0].copy()

        def idx(tt):
            return int(np.clip(round(tt / 0.02), 0, len(t) - 1))

        def pi_ff(x, tt):
            i = idx(tt)
            return impl.ff_fb_control(x, xnom[i], unom[i], K)

        def pi_fb(x, tt):
            i = idx(tt)
            return impl.fb_only_control(x, xnom[i], u_h, K)

        _, xs_ff, _ = rollout(plant.f, x0, dt=0.02, t_end=float(t[-1]), policy=pi_ff)
        _, xs_fb, _ = rollout(plant.f, x0, dt=0.02, t_end=float(t[-1]), policy=pi_fb)
        r_ff, r_fb = _rmse(xs_ff, xnom), _rmse(xs_fb, xnom)
        assert_true(r_fb > 1e-6, "FB-only RMSE vanished — check the baseline")
        assert_true(r_ff * 5.0 <= r_fb + 1e-12, f"FF RMSE {r_ff:.4f} vs FB {r_fb:.4f} (need ≥5×)")

    return [
        Criterion("TODO 1 — flat inversion matches hover + tilt sign", invert_matches, HINTS[0]),
        Criterion("TODO 2 — sampled traj hits first and last waypoints", samples_hover_at_t0, HINTS[1]),
        Criterion("TODO 3 — FF+FB RMSE ≤ 1/5 of feedback-only", ff_beats_fb, HINTS[3]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 08 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 08 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 08 — Plan in Flat Space, Fly in Real Space  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
