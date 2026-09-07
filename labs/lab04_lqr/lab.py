"""Lab 04 — Let the Math Tune It.

Cost as design language. Solve the CARE. Race your Lab 03 PD.

    python labs/lab04_lqr/check.py
    python labs/lab04_lqr/demo.py
"""

from __future__ import annotations

import numpy as np
from scipy.linalg import solve_continuous_are

from flightlab.dynamics import PlanarQuadrotor
from flightlab.resolve import get

# ---------------------------------------------------------------------------
# TODO 1 — pick Q and R  (≤6 lines)
# ---------------------------------------------------------------------------
def design_QR() -> tuple[np.ndarray, np.ndarray]:
    """State cost Q (6×6) and input cost R (2×2). Both SPD.

    Bigger Q[i,i] = care more about that state. Bigger R = spend less thrust.
    """
    # TODO(1): return Q, R  — start with diagonals
    raise NotImplementedError("TODO 1: design Q and R")


# ---------------------------------------------------------------------------
# TODO 2 — solve the CARE  (≤5 lines)
# ---------------------------------------------------------------------------
def lqr(A: np.ndarray, B: np.ndarray, Q: np.ndarray, R: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return K, P with K = R⁻¹ Bᵀ P and P solving the CARE.

    ``scipy.linalg.solve_continuous_are(A, B, Q, R)`` is the P you want.
    """
    # TODO(2): P = solve_continuous_are(...); K = ...
    raise NotImplementedError("TODO 2: solve for K")


# ---------------------------------------------------------------------------
# TODO 3 — the policy  (≤4 lines)
# ---------------------------------------------------------------------------
def lqr_control(x: np.ndarray, x_eq: np.ndarray, u_eq: np.ndarray, K: np.ndarray) -> np.ndarray:
    """u = u_eq − K (x − x_eq)."""
    # TODO(3): return the hover-plus-feedback input
    raise NotImplementedError("TODO 3: implement lqr_control")


def controller(x: np.ndarray, t: float = 0.0, *, plant: PlanarQuadrotor | None = None) -> np.ndarray:
    """Resolved by later labs. Uses this file's Q, R, K."""
    plant = plant or PlanarQuadrotor()
    lab03 = get("lab03")
    x_eq = plant.reset()
    u_eq = plant.hover_input()
    A, B = lab03.linearize(plant.f, x_eq, u_eq)
    Q, R = design_QR()
    K, _ = lqr(A, B, Q, R)
    return lqr_control(x, x_eq, u_eq, K)
