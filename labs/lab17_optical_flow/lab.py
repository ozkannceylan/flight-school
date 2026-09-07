"""Lab 17 — Motion From Brightness.

Lucas–Kanade on a synthetic pair, then a velocity from the flow.

    python labs/lab17_optical_flow/check.py
    python labs/lab17_optical_flow/demo.py
"""

from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------
# TODO 1 — Lucas–Kanade at a list of points  (≤15 lines)
# ---------------------------------------------------------------------------
def lucas_kanade(I1: np.ndarray, I2: np.ndarray, pts: np.ndarray, win: int = 5) -> np.ndarray:
    """Return ``(N, 2)`` flow. ``Ix, Iy`` from I1, ``It = I2 − I1``. Window ``2*win+1``."""
    # TODO(1): solve [ΣIx², ΣIxIy; ΣIxIy, ΣIy²] [u; v] = −[ΣIx It; ΣIy It]
    raise NotImplementedError("TODO 1: lucas_kanade")


# ---------------------------------------------------------------------------
# TODO 2 — mean flow → lateral velocity  (≤8 lines)
# ---------------------------------------------------------------------------
def flow_to_vy(flow: np.ndarray, fx: float, altitude: float) -> float:
    """Downward camera: ``u_pix ≈ −fx * vy / z``. Invert the mean u-component."""
    # TODO(2)
    raise NotImplementedError("TODO 2: flow_to_vy")


# ---------------------------------------------------------------------------
# TODO 3 — a hover PD that *only* sees flow for ẏ  (≤12 lines)
# ---------------------------------------------------------------------------
def flow_hover_pd(
    y: float,
    z: float,
    theta: float,
    vy_flow: float,
    vz: float,
    omega: float,
    y_des: float = 0.0,
    z_des: float = 1.0,
    *,
    m: float = 1.0,
    g: float = 9.81,
    L: float = 0.25,
    I: float = 0.01,
) -> np.ndarray:
    """Cascade-lite. Use ``vy_flow`` in place of true ``vy``."""
    # TODO(3): outer ay,az → θ_des; inner PD on θ; T = m(g+az); τ = I α
    raise NotImplementedError("TODO 3: flow_hover_pd")
