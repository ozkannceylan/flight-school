"""SEE IT — Lab 07 path, Lab 08 traj, Lab 04 LQR, Lab 01 plant. media/lab08.gif."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from flightlab.control import linearize
from flightlab.dynamics import PlanarQuadrotor
from flightlab.integrate import rollout
from flightlab.resolve import get
from flightlab.viz import MEDIA, animate_planar_quad, ensure_media


def main() -> Path:
    impl = get("lab08")
    lab04 = get("lab04")  # banner if student Lab 04 is unfinished — that's the point
    plant = PlanarQuadrotor()
    A, B = linearize(plant.f, plant.reset(), plant.hover_input())
    Q, R = lab04.design_QR()
    K, _ = lab04.lqr(A, B, Q, R)
    t, xnom, unom = impl.sample_flat_traj(plant, dt=0.03, scale=1.0)

    def policy(x, tt):
        i = int(np.clip(round(tt / 0.03), 0, len(t) - 1))
        return impl.ff_fb_control(x, xnom[i], unom[i], K)

    t2, xs, us = rollout(plant.f, xnom[0], dt=0.03, t_end=float(t[-1]), policy=policy)
    ensure_media()
    gif = animate_planar_quad(
        t2,
        xs,
        plant,
        us,
        path=MEDIA / "lab08.gif",
        title="flat space → real space",
    )
    print(f"wrote {gif}")
    return gif


if __name__ == "__main__":
    main()
