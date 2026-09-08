"""CHECK — Lab 01. Runs in <5 s. Partial credit, one hint per red row.

    python labs/lab01_planar_dynamics/check.py
    python labs/lab01_planar_dynamics/check.py --reference
"""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

import numpy as np

from flightlab.checks import Criterion, assert_close, assert_true, run_table
from flightlab.integrate import rollout
from flightlab.resolve import ROOT, _load_file

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "ẏ=v_y, ż=v_z, θ̇=ω. Forces: ÿ=-(T/m)sinθ, z̈=(T/m)cosθ-g, T=u1+u2.",
    "Hover is u1=u2=mg/2. No extra terms — gravity is already in f.",
    "If hover drifts, f is wrong at θ=0 or hover_input isn't mg/2.",
    "ω̇ = L(u1-u2)/I. A 1% split (1.01 vs 0.99) must produce nonzero ω̇.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab01_planar_dynamics")
    return _load_file(LAB_DIR / "lab.py", "lab01_student_check")


def criteria(impl) -> list[Criterion]:
    plant = impl.PlanarQuadrotor()

    def hover_u():
        u = np.asarray(plant.hover_input(), dtype=float).reshape(-1)
        expected = np.array([plant.m * plant.g / 2.0, plant.m * plant.g / 2.0])
        assert_close(u, expected, atol=1e-12, msg=f"got {u}, need {expected}")

    def f_gravity():
        x = np.zeros(6)
        u = np.zeros(2)
        xdot = np.asarray(plant.f(x, u), dtype=float)
        assert_close(xdot, np.array([0, 0, 0, 0, -plant.g, 0]), atol=1e-12, msg=f"got {xdot}")

    def f_kinematics():
        x = np.array([0.0, 0.0, 0.0, 1.5, -0.4, 0.3])
        xdot = np.asarray(plant.f(x, np.zeros(2)), dtype=float)
        assert_close(xdot[:3], np.array([1.5, -0.4, 0.3]), atol=1e-12, msg=f"kinematics {xdot[:3]}")

    def f_tilted():
        theta = 0.4
        u = np.array([3.0, 1.0])
        x = np.array([0.0, 0.0, theta, 0.0, 0.0, 0.0])
        xdot = np.asarray(plant.f(x, u), dtype=float)
        T = 4.0
        exp_ay = -(T / plant.m) * np.sin(theta)
        exp_az = (T / plant.m) * np.cos(theta) - plant.g
        exp_aw = (plant.L * (3.0 - 1.0)) / plant.I
        assert_close(
            xdot[3:],
            np.array([exp_ay, exp_az, exp_aw]),
            atol=1e-10,
            msg=f"accel {xdot[3:]}",
        )

    def hover_hold():
        x0 = plant.reset()
        u = plant.hover_input()
        _, xs, _ = rollout(plant.f, x0, dt=0.01, t_end=5.0, u=u, method="rk4")
        drift = float(np.linalg.norm(xs[-1, :2] - x0[:2]))
        assert_true(drift < 0.01, f"hover drifted {drift*100:.2f} cm in 5 s (need < 1 cm)")

    def tumble():
        x0 = plant.reset()
        u_h = np.asarray(plant.hover_input(), dtype=float)
        u = u_h * np.array([1.01, 0.99])
        _, xs, _ = rollout(plant.f, x0, dt=0.01, t_end=5.0, u=u, method="rk4")
        theta = float(xs[-1, 2])
        omega = float(xs[-1, 5])
        assert_true(
            abs(theta) > 0.5 or abs(omega) > 1.0,
            f"1% asymmetry should tumble; got θ={theta:.3f}, ω={omega:.3f}",
        )

    return [
        Criterion("TODO 2 — hover input is mg/2, mg/2", hover_u, HINTS[1]),
        Criterion("TODO 1 — free-fall gravity at the origin", f_gravity, HINTS[0]),
        Criterion("TODO 1 — kinematics copy the velocities", f_kinematics, HINTS[0]),
        Criterion("TODO 1 — tilted + uneven thrust", f_tilted, HINTS[0]),
        Criterion("hover equilibrium: drift < 1 cm over 5 s", hover_hold, HINTS[2]),
        Criterion("1% thrust asymmetry tumbles", tumble, HINTS[3]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 01 checks")
    p.add_argument("--reference", action="store_true", help="grade reference/ instead of lab.py")
    p.add_argument("--hints", action="store_true", help="print hints and exit")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 01 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 01 — Six States and Two Thrusts  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
