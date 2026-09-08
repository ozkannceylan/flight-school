"""SEE IT — LQR vs your Lab 03 PD, same disturbance. media/lab04.gif."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from flightlab.control import linearize
from flightlab.dynamics import PlanarQuadrotor
from flightlab.integrate import rollout
from flightlab.resolve import get
from flightlab.viz import MEDIA, ensure_media, lqr_vs_pd_figure


def main() -> Path:
    impl = get("lab04")
    lab03 = get("lab03")
    plant = PlanarQuadrotor()
    x_eq = plant.reset()
    u_eq = plant.hover_input()
    A, B = linearize(plant.f, x_eq, u_eq)
    Q, R = impl.design_QR()
    K, _ = impl.lqr(A, B, Q, R)
    x0 = plant.reset(np.array([1.0, 1.0, 0.25, 0.0, 0.0, 0.0]))

    def pi_lqr(x, t):
        return impl.lqr_control(x, x_eq, u_eq, K)

    def pi_pd(x, t):
        return lab03.controller(x, t, plant=plant)

    t, xs_l, us_l = rollout(plant.f, x0, dt=0.02, t_end=4.0, policy=pi_lqr)
    _, xs_p, us_p = rollout(plant.f, x0, dt=0.02, t_end=4.0, policy=pi_pd)
    ensure_media()
    gif = lqr_vs_pd_figure(t, xs_p, xs_l, us_p, us_l, path=MEDIA / "lab04_thumb.png")
    print(f"wrote {gif}")
    print(f"wrote {MEDIA / 'lab04_thumb.png'}")
    return gif


if __name__ == "__main__":
    main()
