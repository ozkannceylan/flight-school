"""SEE IT — covariance ellipse vs particle cloud. media/lab12_thumb.png."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from flightlab.control import linearize
from flightlab.dynamics import PlanarQuadrotor
from flightlab.resolve import get
from flightlab.sensors import H, discrete_hover, hover_dataset
from flightlab.viz import MEDIA, ensure_media, kf_pf_figure


def main() -> Path:
    impl = get("lab12")
    lab04 = get("lab04")
    plant = PlanarQuadrotor()
    A, B = linearize(plant.f, plant.reset(), plant.hover_input())
    Q, R = lab04.design_QR()
    K, _ = lab04.lqr(A, B, Q, R)
    dt = 0.02
    xs, us, zs = hover_dataset(
        plant, K, plant.reset() + np.array([0.12, 0.0, 0.08, 0, 0, 0]), dt=dt, n=50, seed=5
    )
    Ad, Bd = discrete_hover(plant, dt)
    Qp = (0.025**2) * np.eye(6)
    Rm = np.diag([0.04, 0.04, 0.03]) ** 2
    mu = xs[0].copy()
    P = (0.1**2) * np.eye(6)
    rng = np.random.default_rng(5)
    parts = mu + rng.normal(0.0, 0.1, size=(90, 6))
    mus, sigmas = [], []
    x_eq = plant.reset()
    u_eq = plant.hover_input()
    for i in range(len(xs)):
        if i > 0:
            dmu, P = impl.kf_predict(mu - x_eq, P, Ad, Qp)
            mu = x_eq + dmu + Bd @ (us[i - 1] - u_eq)
            parts = impl.pf_predict(parts, us[i - 1], plant, dt, 0.03, rng)
        mu, P = impl.kf_update(mu, P, H, zs[i], Rm)
        parts = impl.resample(parts, impl.pf_weights(parts, zs[i], H, Rm), rng)
        mus.append(mu.copy())
        sigmas.append(P.copy())
    ensure_media()
    dest = kf_pf_figure(xs, np.asarray(mus), np.asarray(sigmas), parts, path=MEDIA / "lab12_thumb.png")
    print(f"wrote {dest}")
    return dest


if __name__ == "__main__":
    main()
