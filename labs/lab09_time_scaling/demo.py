"""SEE IT — three scalings, saturation band shaded. media/lab09.gif."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from flightlab.dynamics import PlanarQuadrotor
from flightlab.resolve import get
from flightlab.viz import MEDIA, ensure_media, thrust_scaling_figure


def main() -> Path:
    impl = get("lab09")
    plant = PlanarQuadrotor()
    u_max = 0.72 * plant.m * plant.g
    s = impl.min_feasible_scale(plant, u_max)
    curves = []
    for label, scale in (
        (f"min feasible  s={s:.2f}", s),
        (f"20% slower    s={1.2*s:.2f}", 1.2 * s),
        (f"5% faster     s={0.95*s:.2f}", 0.95 * s),
    ):
        t, _, us = impl.sample_scaled(plant, scale)
        peak = np.max(np.abs(us), axis=1)
        curves.append((label, t, peak))
    ensure_media()
    gif = thrust_scaling_figure(curves, u_max, path=MEDIA / "lab09_thumb.png")
    print(f"wrote {gif}  s*={s:.3f}")
    return gif


if __name__ == "__main__":
    main()
