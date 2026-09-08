"""Lab 12 — Two Ways to Carry a Belief.

A Gaussian closed form vs. a bag of samples. Same flight, two pictures.

    python labs/lab12_kf_pf/check.py
    python labs/lab12_kf_pf/demo.py
"""

from __future__ import annotations

import numpy as np

from flightlab.dynamics import PlanarQuadrotor
from flightlab.integrate import euler


# ---------------------------------------------------------------------------
# TODO 1 — Kalman predict  (≤6 lines)
# ---------------------------------------------------------------------------
def kf_predict(mu: np.ndarray, P: np.ndarray, A: np.ndarray, Q: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """``μ ← Aμ``, ``P ← APAᵀ + Q``. Call on ``μ−x_eq``, then add ``x_eq+B(u−u_eq)``."""
    # TODO(1)
    raise NotImplementedError("TODO 1: kf_predict")


# ---------------------------------------------------------------------------
# TODO 2 — Kalman update  (≤10 lines)
# ---------------------------------------------------------------------------
def kf_update(
    mu: np.ndarray,
    P: np.ndarray,
    H: np.ndarray,
    z: np.ndarray,
    R: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Innovation ``y = z − Hμ``, ``K = P Hᵀ (HPHᵀ+R)⁻¹``, then μ and P."""
    # TODO(2)
    raise NotImplementedError("TODO 2: kf_update")


# ---------------------------------------------------------------------------
# TODO 3 — particle predict  (≤10 lines)
# ---------------------------------------------------------------------------
def pf_predict(
    particles: np.ndarray,
    u: np.ndarray,
    plant: PlanarQuadrotor,
    dt: float,
    std: float,
    rng: np.random.Generator,
) -> np.ndarray:
    """One Euler step of ``plant.f`` on each row, then ``N(0, std²)`` process noise."""
    # TODO(3)
    raise NotImplementedError("TODO 3: pf_predict")


# ---------------------------------------------------------------------------
# TODO 4 — systematic resample  (≤12 lines)
# ---------------------------------------------------------------------------
def resample(particles: np.ndarray, weights: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Systematic resample. ``weights`` already sum to 1. Return ``(N, n)``."""
    # TODO(4): cdf; start u0 ~ U[0, 1/N]; then u0 + k/N
    raise NotImplementedError("TODO 4: resample")


def pf_weights(particles: np.ndarray, z: np.ndarray, H: np.ndarray, R: np.ndarray) -> np.ndarray:
    """Gaussian observation weights. Provided — not a TODO."""
    innov = z.reshape(1, -1) - particles @ H.T
    Rinv = np.linalg.inv(R)
    q = np.sum((innov @ Rinv) * innov, axis=1)
    w = np.exp(-0.5 * (q - q.min()))
    s = w.sum()
    return w / s if s > 0 else np.full(len(w), 1.0 / len(w))


def nees(mu: np.ndarray, P: np.ndarray, x: np.ndarray) -> float:
    e = np.asarray(x, dtype=float).reshape(-1) - np.asarray(mu, dtype=float).reshape(-1)
    return float(e @ np.linalg.solve(P, e))
