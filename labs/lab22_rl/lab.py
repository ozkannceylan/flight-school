"""Lab 22 — Learning to Hover Without Being Told How.

CEM on a linear policy. The LQR line is the honest baseline: zero samples.

    python labs/lab22_rl/check.py
    python labs/lab22_rl/demo.py
"""

from __future__ import annotations

import numpy as np

from flightlab.dynamics import PlanarQuadrotor
from flightlab.integrate import rk4


# ---------------------------------------------------------------------------
# TODO 1 — episode return for a linear gain matrix  (≤12 lines)
# ---------------------------------------------------------------------------
def episode_return(K: np.ndarray, plant: PlanarQuadrotor, x0: np.ndarray, *, dt: float = 0.02, t_end: float = 2.0) -> float:
    """``u = u_eq − K (x − x_eq)``. RK4. Return ``−Σ (y² + (z−1)² + 0.01‖u−u_eq‖²) dt``."""
    # TODO(1)
    raise NotImplementedError("TODO 1: episode_return")


# ---------------------------------------------------------------------------
# TODO 2 — CEM update  (≤12 lines)
# ---------------------------------------------------------------------------
def cem_update(samples: np.ndarray, scores: np.ndarray, n_elite: int) -> tuple[np.ndarray, np.ndarray]:
    """``samples (N, d)``, higher score is better. Return ``(mean, std)`` of the elite."""
    # TODO(2)
    raise NotImplementedError("TODO 2: cem_update")


# ---------------------------------------------------------------------------
# TODO 3 — the CEM loop  (≤15 lines)
# ---------------------------------------------------------------------------
def cem(
    plant: PlanarQuadrotor,
    *,
    n_iter: int = 8,
    n_samp: int = 16,
    n_elite: int = 4,
    seed: int = 0,
) -> tuple[np.ndarray, list[float]]:
    """Return ``(best_K 2×6, mean return per iter)``. Start from ``N(0, 0.4)`` on the 12 gains."""
    # TODO(3)
    raise NotImplementedError("TODO 3: cem")
