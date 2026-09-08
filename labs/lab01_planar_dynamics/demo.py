"""SEE IT — hover, then a 1% nudge. Writes media/lab01.gif (<10 s)."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from flightlab.dynamics.planar_quad import PlanarQuadrotor as VizPlant
from flightlab.integrate import rollout
from flightlab.resolve import get
from flightlab.viz import MEDIA, animate_planar_quad, ensure_media


def main() -> Path:
    impl = get("lab01")
    plant = impl.PlanarQuadrotor()
    # Viz helpers only need m, L for drawing; use the same numbers.
    draw = VizPlant(m=plant.m, L=plant.L, I=plant.I, g=plant.g)

    x0 = plant.reset()
    u_hover = np.asarray(plant.hover_input(), dtype=float)
    # Short hover, then a 1.2 s nudge — long enough to tip, short enough to stay on screen.
    t1, xs1, us1 = rollout(plant.f, x0, dt=0.02, t_end=2.0, u=u_hover, method="rk4")
    u_nudge = u_hover * np.array([1.01, 0.99])
    t2, xs2, us2 = rollout(plant.f, xs1[-1], dt=0.02, t_end=1.2, u=u_nudge, method="rk4")

    t = np.concatenate([t1, t1[-1] + t2[1:]])
    xs = np.vstack([xs1, xs2[1:]])
    us = np.vstack([us1, us2[1:]])

    ensure_media()
    gif = animate_planar_quad(
        t,
        xs,
        draw,
        us,
        path=MEDIA / "lab01.gif",
        title="hover, then 1% thrust asymmetry",
    )
    print(f"wrote {gif}")
    print(f"wrote {MEDIA / 'lab01_thumb.png'}")
    return gif


if __name__ == "__main__":
    main()
