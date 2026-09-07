"""CHECK — Lab 03. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

import numpy as np

from flightlab.checks import Criterion, assert_close, assert_true, run_table
from flightlab.dynamics import PlanarQuadrotor
from flightlab.integrate import rollout
from flightlab.resolve import ROOT, _load_file

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "A[:,i] ≈ (f(x+eps e_i, u) − f(x,u)) / eps. Same idea down the columns of B.",
    "At hover, ÿ ≈ −g θ so A[3,2] ≈ −g. B[4,:] ≈ 1/m; B[5,:] ≈ [L/I, −L/I].",
    "θ_des = −ay/g, T = m(az+g), τ = I(kp_θ eθ − kd_θ ω), split across the two rotors.",
    "Inner must be faster: √(kp_θ / kp_y) ≥ 5. If it rings, raise kp_θ or lower kp_y.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab03_cascade_pd")
    return _load_file(LAB_DIR / "lab.py", "lab03_student_check")


def _closed_loop_eigs(impl, plant, gains):
    x_eq = plant.reset()
    u_eq = plant.hover_input()

    def f_cl(x, _u=None):
        return plant.f(x, impl.cascade_pd(plant, x, x_eq[:2], gains))

    A, _ = impl.linearize(f_cl, x_eq, u_eq)
    return np.linalg.eigvals(A)


def _step_response(impl, plant, gains, t_end=4.0):
    x0 = plant.reset(np.array([1.0, 1.0, 0.0, 0.0, 0.0, 0.0]))
    yd = np.array([0.0, 1.0])

    def policy(x, t):
        return impl.cascade_pd(plant, x, yd, gains)

    t, xs, _ = rollout(plant.f, x0, dt=0.01, t_end=t_end, policy=policy)
    return t, xs


def criteria(impl) -> list[Criterion]:
    plant = PlanarQuadrotor()
    gains = impl.DEFAULT_GAINS

    def A_hover():
        x_eq, u_eq = plant.reset(), plant.hover_input()
        A, B = impl.linearize(plant.f, x_eq, u_eq)
        assert A.shape == (6, 6) and B.shape == (6, 2)
        assert_close(A[3, 2], -plant.g, atol=2e-3, msg=f"A[vy,θ]={A[3,2]:.3f}, need ≈ −g")
        assert_close(B[4], np.array([1 / plant.m, 1 / plant.m]), atol=2e-3, msg=f"B[vz]={B[4]}")
        assert_close(
            B[5],
            np.array([plant.L / plant.I, -plant.L / plant.I]),
            atol=2e-3,
            msg=f"B[ω]={B[5]}",
        )

    def hover_u():
        x = plant.reset()
        u = impl.cascade_pd(plant, x, x[:2], gains)
        assert_close(u, plant.hover_input(), atol=0.05, msg=f"at eq got u={u}")

    def eigs_lhp():
        ev = _closed_loop_eigs(impl, plant, gains)
        worst = float(np.max(ev.real))
        assert_true(worst < -0.05, f"slowest Re(λ)={worst:.3f} (need all in open LHP)")

    def settling():
        t, xs = _step_response(impl, plant, gains)
        y = xs[:, 0]
        band = 0.05
        inside = np.abs(y) < band
        # first index after which we stay inside
        ok = False
        ts = None
        for i in range(len(t)):
            if np.all(inside[i:]):
                ts = float(t[i])
                ok = True
                break
        assert_true(ok and ts is not None and ts < 2.5, f"settling {ts} s (need < 2.5)")

    def overshoot():
        t, xs = _step_response(impl, plant, gains)
        y = xs[:, 0]
        os = float(max(0.0, -np.min(y)))  # started at +1, target 0
        assert_true(os < 0.20, f"overshoot {os*100:.1f}% (need < 20%)")

    def timescale():
        ratio = float(gains.timescale_ratio())
        assert_true(ratio >= 5.0, f"√(kp_θ/kp_y) = {ratio:.2f} (need ≥ 5)")

    return [
        Criterion("TODO 1 — hover linearization matches known A,B", A_hover, HINTS[1]),
        Criterion("TODO 2 — cascade holds hover", hover_u, HINTS[2]),
        Criterion("closed-loop eigenvalues in the LHP", eigs_lhp, HINTS[2]),
        Criterion("settling < 2.5 s on a 1 m lateral step", settling, HINTS[3]),
        Criterion("overshoot < 20%", overshoot, HINTS[3]),
        Criterion("timescale ratio √(kp_θ/kp_y) ≥ 5", timescale, HINTS[3]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 03 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 03 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 03 — Cascade PD  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
