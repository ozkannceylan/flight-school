"""CHECK — Lab 00. Runs in <5 s. Partial credit, one hint per red row.

    python labs/lab00_hello_state/check.py              # your lab.py
    python labs/lab00_hello_state/check.py --reference  # CI / spoiler path
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

import numpy as np

from flightlab.checks import Criterion, assert_close, assert_true, run_table
from flightlab.resolve import ROOT, _load_file

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "Euler is x + dt * f(x, u). No k2/k3 — that's RK4.",
    "RK4: four evaluations of f, weights 1/6, 2/6, 2/6, 1/6. Hold u fixed.",
    "z_dot is v. v_dot is -g - (c/m)*v*abs(v). Don't forget the sign of g.",
    "Energy of ẍ = −x is ½v² + ½x². Integrate the *conservative* f, not drag.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab00_hello_state")
    return _load_file(LAB_DIR / "lab.py", "lab00_student_check")


def _ho_f(x, u=None):
    """Unit harmonic oscillator — conservative, for the energy check."""
    return np.array([x[1], -x[0]], dtype=float)


def _energy(x) -> float:
    return 0.5 * float(x[0] ** 2 + x[1] ** 2)


def _roll(step_fn, f, x0, dt, t_end, u=None):
    n = int(round(t_end / dt))
    x = np.asarray(x0, dtype=float).reshape(-1)
    for _ in range(n):
        x = np.asarray(step_fn(f, x, u, dt), dtype=float).reshape(-1)
    return x


def criteria(impl) -> list[Criterion]:
    def todo1():
        def f(x, u):
            return np.array([1.0, 2.0])

        got = impl.euler(f, np.array([0.0, 0.0]), None, 0.1)
        assert_close(got, np.array([0.1, 0.2]), atol=1e-12, msg=f"got {got}")

    def todo2():
        # ẋ = −x is linear; one RK4 step has a known closed form.
        def f(x, u):
            return -x

        x0 = np.array([1.0])
        dt = 0.2
        k1 = -x0
        k2 = -(x0 + 0.5 * dt * k1)
        k3 = -(x0 + 0.5 * dt * k2)
        k4 = -(x0 + dt * k3)
        expected = x0 + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        got = impl.rk4(f, x0, None, dt)
        assert_close(got, expected, atol=1e-12, msg=f"got {got}")

    def todo3():
        xdot = impl.point_mass_f(np.array([10.0, 0.0]), None, m=1.0, g=9.81, c=0.15)
        assert_close(xdot, np.array([0.0, -9.81]), atol=1e-10, msg=f"at rest got {xdot}")
        xdot2 = impl.point_mass_f(np.array([4.0, -2.0]), None, m=1.0, g=9.81, c=0.5)
        # v̇ = -g - (c/m) v |v| = -9.81 - 0.5 * (-2) * 2 = -9.81 + 2.0
        assert_close(xdot2, np.array([-2.0, -7.81]), atol=1e-10, msg=f"with drag got {xdot2}")

    def energy_rk4():
        dt, t_end = 0.02, 10.0
        xT = _roll(impl.rk4, _ho_f, np.array([1.0, 0.0]), dt, t_end)
        drift = abs(_energy(xT) - 0.5)
        assert_true(
            drift < 1e-4,
            f"RK4 energy drift {drift:.2e} over 10 s (need < 1e-4)",
        )

    def euler_worse():
        dt, t_end = 0.02, 10.0
        x0 = np.array([1.0, 0.0])
        e_rk = abs(_energy(_roll(impl.rk4, _ho_f, x0, dt, t_end)) - 0.5)
        e_eu = abs(_energy(_roll(impl.euler, _ho_f, x0, dt, t_end)) - 0.5)
        assert_true(
            e_eu > 10.0 * max(e_rk, 1e-16),
            f"Euler drift {e_eu:.2e} should dwarf RK4 {e_rk:.2e}",
        )

    return [
        Criterion("TODO 1 — Euler step matches fixture", todo1, HINTS[0]),
        Criterion("TODO 2 — RK4 step matches fixture", todo2, HINTS[1]),
        Criterion("TODO 3 — point-mass f (rest + quadratic drag)", todo3, HINTS[2]),
        Criterion("RK4 energy drift < 1e-4 over 10 s (harmonic oscillator)", energy_rk4, HINTS[3]),
        Criterion("Euler energy drift ≫ RK4 at the same step", euler_worse, HINTS[3]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 00 checks")
    p.add_argument("--reference", action="store_true", help="grade reference/ instead of lab.py")
    p.add_argument("--hints", action="store_true", help="print hints and exit")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 00 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 00 — Hello, State  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
