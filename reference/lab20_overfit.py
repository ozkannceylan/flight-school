"""Reference implementation for Lab 20 — When Fitting Better Means Knowing Less."""

from __future__ import annotations

import numpy as np


def poly_features(x: np.ndarray, degree: int = 8) -> np.ndarray:
    x = np.asarray(x, dtype=float).reshape(-1)
    return np.stack([x**k for k in range(degree + 1)], axis=1)


def fit_poly(Phi: np.ndarray, y: np.ndarray, l2: float = 0.0) -> np.ndarray:
    Phi = np.asarray(Phi, dtype=float)
    y = np.asarray(y, dtype=float).reshape(-1)
    A = Phi.T @ Phi
    I = np.eye(A.shape[0])
    I[0, 0] = 0.0
    return np.linalg.solve(A + l2 * I, Phi.T @ y)


def mse(Phi: np.ndarray, y: np.ndarray, w: np.ndarray) -> float:
    r = np.asarray(Phi, dtype=float) @ np.asarray(w, dtype=float).reshape(-1) - np.asarray(y, dtype=float).reshape(-1)
    return float(np.mean(r * r))


def relative_gap(train_mse: float, val_mse: float) -> float:
    return float((val_mse - train_mse) / max(val_mse + train_mse, 1e-12))
