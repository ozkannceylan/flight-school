"""SEE IT — altitude hold, then the representation cliff. media/lab02.gif."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from flightlab.dynamics.quad3d import euler_zyx_rates
from flightlab.integrate import rollout
from flightlab.resolve import get
from flightlab.viz import MEDIA, animate_quad3d, ensure_media


def main() -> Path:
    impl = get("lab02")
    plant = impl.Quad3D()
    x0 = plant.reset()
    z_des = 2.0

    def policy(x, t):
        return plant.altitude_loop(x, z_des)

    t, xs, _ = rollout(plant.f, x0, dt=0.03, t_end=4.0, policy=policy, method="rk4")

    thetas = np.linspace(0.0, 1.56, len(t))
    rate_norm = np.array(
        [np.linalg.norm(euler_zyx_rates(0.0, th, np.array([0.0, 0.0, 1.0]))) for th in thetas]
    )
    ensure_media()
    gif = animate_quad3d(t, xs, thetas, rate_norm, path=MEDIA / "lab02.gif")
    print(f"wrote {gif}")
    print(f"wrote {MEDIA / 'lab02_thumb.png'}")
    return gif


if __name__ == "__main__":
    main()
