"""Lab 19 — The Shape of the Descent.

SGD, momentum, Adam on a 2-D bowl. Then sweep the learning rate until it snaps.

    python labs/lab19_sgd/check.py
    python labs/lab19_sgd/demo.py
"""

from __future__ import annotations

import numpy as np


def loss(w: np.ndarray) -> float:
    """``(w0−1)² + 25 (w1+0.5)²``. Provided."""
    w = np.asarray(w, dtype=float).reshape(2)
    return float((w[0] - 1.0) ** 2 + 25.0 * (w[1] + 0.5) ** 2)


def grad(w: np.ndarray) -> np.ndarray:
    """Analytic gradient. Provided."""
    w = np.asarray(w, dtype=float).reshape(2)
    return np.array([2.0 * (w[0] - 1.0), 50.0 * (w[1] + 0.5)], dtype=float)


# ---------------------------------------------------------------------------
# TODO 1 — SGD  (≤4 lines)
# ---------------------------------------------------------------------------
def sgd_step(w: np.ndarray, g: np.ndarray, lr: float) -> np.ndarray:
    # TODO(1)
    raise NotImplementedError("TODO 1: sgd_step")


# ---------------------------------------------------------------------------
# TODO 2 — momentum  (≤6 lines)
# ---------------------------------------------------------------------------
def momentum_step(w: np.ndarray, g: np.ndarray, v: np.ndarray, lr: float, beta: float = 0.8):
    """Return ``(w, v)`` with ``v ← β v + g``, ``w ← w − lr v``."""
    # TODO(2)
    raise NotImplementedError("TODO 2: momentum_step")


# ---------------------------------------------------------------------------
# TODO 3 — Adam  (≤12 lines)
# ---------------------------------------------------------------------------
def adam_step(
    w: np.ndarray,
    g: np.ndarray,
    m: np.ndarray,
    v: np.ndarray,
    t: int,
    lr: float,
    b1: float = 0.9,
    b2: float = 0.999,
    eps: float = 1e-8,
):
    """Return ``(w, m, v)``. Bias-correct ``m`` and ``v``."""
    # TODO(3)
    raise NotImplementedError("TODO 3: adam_step")


# ---------------------------------------------------------------------------
# TODO 4 — learning-rate sweep  (≤10 lines)
# ---------------------------------------------------------------------------
def first_divergent_lr(lrs: np.ndarray, n_steps: int = 40, w0: np.ndarray | None = None) -> float:
    """Smallest ``lr`` in ``lrs`` (sorted) whose SGD loss explodes (``>80`` or non-finite)."""
    # TODO(4)
    raise NotImplementedError("TODO 4: first_divergent_lr")
