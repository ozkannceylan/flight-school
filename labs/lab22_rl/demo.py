"""SEE IT — CEM curve vs the LQR dashed line. media/lab22_thumb.png."""

from __future__ import annotations

from pathlib import Path

from flightlab.control import linearize
from flightlab.dynamics import PlanarQuadrotor
from flightlab.resolve import get
from flightlab.viz import MEDIA, ensure_media, rl_curve_figure


def main() -> Path:
    impl = get("lab22")
    lab04 = get("lab04")
    plant = PlanarQuadrotor()
    K, hist = impl.cem(plant, n_iter=8, n_samp=16, n_elite=4, seed=0)
    A, B = linearize(plant.f, plant.reset(), plant.hover_input())
    Q, R = lab04.design_QR()
    Klqr, _ = lab04.lqr(A, B, Q, R)
    x0 = plant.reset() + __import__("numpy").array([0.12, 0.04, 0.05, 0.0, 0.0, 0.0])
    r_lqr = impl.episode_return(Klqr, plant, x0)
    r_cem = impl.episode_return(K, plant, x0)
    ensure_media()
    dest = rl_curve_figure(__import__("numpy").asarray(hist), r_lqr, path=MEDIA / "lab22_thumb.png")
    print(f"wrote {dest}  CEM {r_cem:.3f} vs LQR {r_lqr:.3f}  (samples={8*16})")
    return dest


if __name__ == "__main__":
    main()
