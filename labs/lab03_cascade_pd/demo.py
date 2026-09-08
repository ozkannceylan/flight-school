"""SEE IT — nine flights, one gain sweep. media/lab03.gif."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from flightlab.control import CascadeGains
from flightlab.dynamics import PlanarQuadrotor
from flightlab.integrate import rollout
from flightlab.resolve import get
from flightlab.viz import MEDIA, ensure_media, gain_sweep_figure


def main() -> Path:
    impl = get("lab03")
    plant = PlanarQuadrotor()
    base = impl.DEFAULT_GAINS
    # Outer kp_y × inner kp_θ. The middle cell is the tuned pair.
    grid = [
        (1.5, 40.0),
        (1.5, 300.0),
        (1.5, 600.0),
        (10.0, 40.0),
        (10.0, 300.0),
        (10.0, 600.0),
        (25.0, 40.0),
        (25.0, 300.0),
        (25.0, 600.0),
    ]
    results = []
    x0 = plant.reset(np.array([1.0, 1.0, 0.0, 0.0, 0.0, 0.0]))
    for kp_y, kp_th in grid:
        gains = CascadeGains(
            kp_y=kp_y,
            kd_y=base.kd_y,
            kp_z=base.kp_z,
            kd_z=base.kd_z,
            kp_th=kp_th,
            kd_th=base.kd_th,
        )

        def policy(x, t, g=gains):
            return impl.cascade_pd(plant, x, np.array([0.0, 1.0]), g)

        t, xs, _ = rollout(plant.f, x0, dt=0.02, t_end=3.0, policy=policy)
        # Clip wild unstable runs so the axes stay readable.
        y = np.clip(xs[:, 0], -3.0, 3.0)
        results.append((f"kp_y={kp_y:g}  kp_θ={kp_th:g}", t, y))
    ensure_media()
    gif = gain_sweep_figure(results, path=MEDIA / "lab03_thumb.png")
    print(f"wrote {gif}")
    print(f"wrote {MEDIA / 'lab03_thumb.png'}")
    return gif


if __name__ == "__main__":
    main()
