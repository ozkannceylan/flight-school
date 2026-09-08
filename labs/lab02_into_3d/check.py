"""CHECK — Lab 02. Runs in <5 s."""

from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

import numpy as np

from flightlab.checks import Criterion, assert_close, assert_true, run_table
from flightlab.dynamics.quad3d import euler_zyx_rates as rates_ref
from flightlab.integrate import rollout
from flightlab.resolve import ROOT, _load_file

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

LAB_DIR = Path(__file__).resolve().parent
HINTS = [
    "φ̇ = p + q sinφ tanθ + r cosφ tanθ; θ̇ = q cosφ − r sinφ; ψ̇ = (q sinφ + r cosφ)/cosθ.",
    "World accel = (T/m) R[:,2] − [0,0,g]. ω̇ = I⁻¹(τ − ω×Iω). Kinematics copy v and Euler rates.",
    "T = mg + kp(z_des−z) − kd vz. Leave the three torques at 0.",
    "At θ→π/2, tanθ and 1/cosθ explode. A 1 rad/s pitch rate should look huge in Euler rates.",
]


def load_impl(*, reference: bool):
    if reference:
        return importlib.import_module("reference.lab02_into_3d")
    return _load_file(LAB_DIR / "lab.py", "lab02_student_check")


def criteria(impl) -> list[Criterion]:
    plant = impl.Quad3D()

    def euler_level():
        got = np.asarray(plant.euler_zyx_rates(0.0, 0.0, np.array([0.2, -0.3, 0.4])))
        assert_close(got, np.array([0.2, -0.3, 0.4]), atol=1e-12, msg=f"at θ=0 got {got}")

    def euler_tilted():
        phi, theta = 0.3, 0.4
        omega = np.array([0.1, 0.2, 0.3])
        got = np.asarray(plant.euler_zyx_rates(phi, theta, omega))
        assert_close(got, rates_ref(phi, theta, omega), atol=1e-10, msg=f"got {got}")

    def hover_eq():
        xdot = np.asarray(plant.f(plant.reset(), plant.hover_input()), dtype=float)
        assert_close(xdot, np.zeros(12), atol=1e-9, msg=f"hover ẋ = {xdot}")

    def gravity_unpowered():
        xdot = np.asarray(plant.f(np.zeros(12), np.zeros(4)), dtype=float)
        assert_close(xdot[6:9], np.array([0.0, 0.0, -plant.g]), atol=1e-12, msg=f"accel {xdot[6:9]}")

    def altitude_tracks():
        z_des = 2.0
        x0 = plant.reset()  # z=1

        def policy(x, t):
            return plant.altitude_loop(x, z_des)

        _, xs, _ = rollout(plant.f, x0, dt=0.02, t_end=4.0, policy=policy, method="rk4")
        err = abs(float(xs[-1, 2]) - z_des)
        assert_true(err < 0.15, f"final |z−2| = {err:.3f} m (need < 0.15)")

    def gimbal_lock():
        theta = 1.56  # ~89.4°
        # At φ=0 a pure pitch rate q is just θ̇=q. Yaw rate r is divided by cosθ.
        omega = np.array([0.0, 0.0, 1.0])
        rates = np.asarray(plant.euler_zyx_rates(0.0, theta, omega))
        nrm = float(np.linalg.norm(rates))
        assert_true(nrm > 20.0, f"|Euler rates| at θ=1.56 for r=1 is {nrm:.2f} (need > 20)")
        level = np.linalg.norm(plant.euler_zyx_rates(0.0, 0.0, omega))
        assert_true(nrm > 10.0 * level, "near 90° should dwarf the level-hover rates")

    return [
        Criterion("TODO 1 — Euler rates match body rates at θ=0", euler_level, HINTS[0]),
        Criterion("TODO 1 — Euler rates at a tilted pose", euler_tilted, HINTS[0]),
        Criterion("TODO 2 — hover is an equilibrium", hover_eq, HINTS[1]),
        Criterion("TODO 2 — unpowered free-fall gravity", gravity_unpowered, HINTS[1]),
        Criterion("TODO 3 — altitude setpoint tracked to 15 cm", altitude_tracks, HINTS[2]),
        Criterion("gimbal lock: Euler rates explode near 90°", gimbal_lock, HINTS[3]),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Lab 02 checks")
    p.add_argument("--reference", action="store_true")
    p.add_argument("--hints", action="store_true")
    args = p.parse_args(argv)
    if args.hints:
        print("LAB 02 hints")
        for i, h in enumerate(HINTS, 1):
            print(f"  {i}. {h}")
        return 0
    impl = load_impl(reference=args.reference)
    src = "reference" if args.reference else "lab.py"
    report = run_table(f"LAB 02 — Into 3D, and the First Loop  ({src})", criteria(impl))
    return 0 if report.ok else 1


if __name__ == "__main__":
    sys.exit(main())
