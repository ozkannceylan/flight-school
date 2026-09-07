"""CHECK — Lab 04. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

import numpy as np

from flightlab.checks import Criterion, assert_true, run_table
from flightlab.control import linearize as linearize_core
from flightlab.dynamics import PlanarQuadrotor
from flightlab.integrate import rollout
from flightlab.resolve import ROOT, _load_file, get

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "Q and R must be symmetric positive definite. Start with diagonals; put weight on y and z.",
    "P = solve_continuous_are(A,B,Q,R); K = solve(R, B.T @ P). Shapes: K is 2×6.",
    "u = u_hover − K (x − x_hover). Don't forget the feedforward hover input.",
    "Tiny R makes K huge — the policy will slam the rotors. That's the saturation check.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab04_lqr")
    return _load_file(LAB_DIR / "lab.py", "lab04_student_check")


def _AB(plant):
    return linearize_core(plant.f, plant.reset(), plant.hover_input())


def _traj(plant, policy, x0, t_end=4.0):
    return rollout(plant.f, x0, dt=0.02, t_end=t_end, policy=policy)


def _quad_cost(xs, us, x_eq, u_eq, Q, R) -> float:
    J = 0.0
    dt = 0.02
    for x, u in zip(xs, us, strict=False):
        e = x - x_eq
        v = u - u_eq
        J += float(e @ Q @ e + v @ R @ v) * dt
    return J


def criteria(impl) -> list[Criterion]:
    plant = PlanarQuadrotor()
    x_eq = plant.reset()
    u_eq = plant.hover_input()
    A, B = _AB(plant)
    lab03 = get("lab03")

    def qr_spd():
        Q, R = impl.design_QR()
        assert Q.shape == (6, 6) and R.shape == (2, 2)
        assert_true(np.all(np.linalg.eigvalsh(Q) > 1e-8), "Q must be SPD")
        assert_true(np.all(np.linalg.eigvalsh(R) > 1e-8), "R must be SPD")

    def k_shape_stable():
        Q, R = impl.design_QR()
        K, P = impl.lqr(A, B, Q, R)
        assert K.shape == (2, 6), f"K shape {K.shape}"
        ev = np.linalg.eigvals(A - B @ K)
        worst = float(np.max(ev.real))
        assert_true(worst < -0.05, f"A−BK slowest Re={worst:.3f}")

    def beats_pd():
        Q, R = impl.design_QR()
        K, _ = impl.lqr(A, B, Q, R)
        x0 = plant.reset(np.array([1.0, 1.0, 0.25, 0.0, 0.0, 0.0]))
        Qe, Re = np.diag([10.0, 8.0, 2.0, 1.0, 1.0, 0.4]), np.diag([0.2, 0.2])

        def pi_lqr(x, t):
            return impl.lqr_control(x, x_eq, u_eq, K)

        def pi_pd(x, t):
            return lab03.controller(x, t, plant=plant)

        _, xs_l, us_l = _traj(plant, pi_lqr, x0)
        _, xs_p, us_p = _traj(plant, pi_pd, x0)
        Jl = _quad_cost(xs_l, us_l, x_eq, u_eq, Qe, Re)
        Jp = _quad_cost(xs_p, us_p, x_eq, u_eq, Qe, Re)
        assert_true(Jl < Jp, f"LQR cost {Jl:.3f} should beat PD {Jp:.3f}")

    def bad_R_saturates():
        Q, _ = impl.design_QR()
        R_tiny = 1e-6 * np.eye(2)
        K, _ = impl.lqr(A, B, Q, R_tiny)
        x0 = plant.reset(np.array([1.5, 1.0, 0.4, 0.0, 0.0, 0.0]))

        def pi(x, t):
            return impl.lqr_control(x, x_eq, u_eq, K)

        _, _, us = _traj(plant, pi, x0, t_end=1.5)
        peak = float(np.max(np.abs(us)))
        hover = float(plant.m * plant.g / 2.0)
        assert_true(peak > 2.5 * hover, f"max |u|={peak:.2f} (need > {2.5*hover:.2f} with tiny R)")

    return [
        Criterion("TODO 1 — Q, R are SPD with the right shape", qr_spd, HINTS[0]),
        Criterion("TODO 2 — A−BK is Hurwitz", k_shape_stable, HINTS[1]),
        Criterion("integrated cost strictly below the Lab 03 PD", beats_pd, HINTS[2]),
        Criterion("deliberately tiny R saturates the rotors", bad_R_saturates, HINTS[3]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 04 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 04 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 04 — Let the Math Tune It  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
