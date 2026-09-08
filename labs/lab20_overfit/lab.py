"""Lab 20 — When Fitting Better Means Knowing Less.

A high-order polynomial on 8 points. Then L2, and the gap closes.

    python labs/lab20_overfit/check.py
    python labs/lab20_overfit/demo.py
"""

from __future__ import annotations

import numpy as np


def poly_features(x: np.ndarray, degree: int = 8) -> np.ndarray:
    """``[1, x, x², …, x^d]``. Provided."""
    x = np.asarray(x, dtype=float).reshape(-1)
    return np.stack([x**k for k in range(degree + 1)], axis=1)


# ---------------------------------------------------------------------------
# TODO 1 — ridge / OLS closed form  (≤8 lines)
# ---------------------------------------------------------------------------
def fit_poly(Phi: np.ndarray, y: np.ndarray, l2: float = 0.0) -> np.ndarray:
    """``w = (ΦᵀΦ + λ I)⁻¹ Φᵀ y``. Do not regularise the bias (row 0 of I = 0)."""
    # TODO(1)
    raise NotImplementedError("TODO 1: fit_poly")


# ---------------------------------------------------------------------------
# TODO 2 — train and val MSE  (≤6 lines)
# ---------------------------------------------------------------------------
def mse(Phi: np.ndarray, y: np.ndarray, w: np.ndarray) -> float:
    # TODO(2)
    raise NotImplementedError("TODO 2: mse")


# ---------------------------------------------------------------------------
# TODO 3 — the gap  (≤6 lines)
# ---------------------------------------------------------------------------
def relative_gap(train_mse: float, val_mse: float) -> float:
    """``(val − train) / (val + train)``. ~1 when you memorised, small when they agree."""
    # TODO(3)
    raise NotImplementedError("TODO 3: relative_gap")
