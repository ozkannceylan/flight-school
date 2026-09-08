"""SEE IT — a neural net (badly) hovering. media/lab18_thumb.png."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from flightlab.dynamics import PlanarQuadrotor
from flightlab.integrate import rollout
from flightlab.learning import lqr_policy_dataset
from flightlab.resolve import get
from flightlab.viz import MEDIA, ensure_media, mlp_flight_figure


def main() -> Path:
    impl = get("lab18")
    xs, us = lqr_policy_dataset(120, seed=3)
    rng = np.random.default_rng(0)
    p = impl.init_params(rng)
    for _ in range(700):
        yhat, cache = impl.forward(xs, p["W1"], p["b1"], p["W2"], p["b2"])
        p = impl.gd_step(p, impl.backward(yhat, us, cache), 0.25)
    plant = PlanarQuadrotor()

    def pi(x, _t):
        yhat, _ = impl.forward(x.reshape(1, -1), p["W1"], p["b1"], p["W2"], p["b2"])
        return yhat.reshape(-1)

    x0 = plant.reset() + np.array([0.10, 0.04, 0.05, 0, 0, 0])
    t, xs_r, _ = rollout(plant.f, x0, dt=0.03, t_end=3.0, policy=pi)
    ensure_media()
    dest = mlp_flight_figure(t, xs_r[:, 0], xs_r[:, 1], path=MEDIA / "lab18_thumb.png")
    print(f"wrote {dest}")
    return dest


if __name__ == "__main__":
    main()
