"""Lab 11 — Prior, Likelihood, Posterior.

Same picture as Lab 10, with weights. Predict, then multiply by p(z|x).

    python labs/lab11_bayes/check.py
    python labs/lab11_bayes/demo.py
"""

from __future__ import annotations

import numpy as np


# ---------------------------------------------------------------------------
# TODO 1 — motion predict  (≤12 lines)
# ---------------------------------------------------------------------------
def predict(bel: np.ndarray, p_fwd: float = 0.8, p_stay: float = 0.2) -> np.ndarray:
    """1-D corridor, try to step +1. Clip at the last cell. Must still sum to 1."""
    # TODO(1): out[i] += p_stay * bel[i]; out[min(i+1, n-1)] += p_fwd * bel[i]
    raise NotImplementedError("TODO 1: predict")


# ---------------------------------------------------------------------------
# TODO 2 — Bayes update  (≤10 lines)
# ---------------------------------------------------------------------------
def likelihood(doors: np.ndarray, z_door: bool, p_hit: float = 0.9, p_false: float = 0.2) -> np.ndarray:
    """p(z|x) for each cell. ``z_door`` is the binary door detector."""
    # TODO(2): at a door, p(z=door)=p_hit; elsewhere p(z=door)=p_false
    raise NotImplementedError("TODO 2: likelihood")


def update(bel: np.ndarray, like: np.ndarray) -> np.ndarray:
    """Unnormalized posterior, then divide by the sum."""
    # TODO(2)
    raise NotImplementedError("TODO 2: update")


# ---------------------------------------------------------------------------
# TODO 3 — a wrong sensor model (for the confident-and-wrong check)  (≤4 lines)
# ---------------------------------------------------------------------------
def inverted_likelihood(doors: np.ndarray, z_door: bool, p_hit: float = 0.9, p_false: float = 0.2) -> np.ndarray:
    """Swap hit and false-alarm. Same API as ``likelihood``."""
    # TODO(3): call likelihood with p_hit/p_false swapped, or invert ``doors``
    raise NotImplementedError("TODO 3: inverted_likelihood")
