"""Numerical linearization of ẋ = f(x, u). Used by Labs 03–04."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

VectorField = Callable[[np.ndarray, np.ndarray], np.ndarray]


def linearize(
    f: VectorField,
    x0: np.ndarray,
    u0: np.ndarray,
    eps: float = 1e-5,
) -> tuple[np.ndarray, np.ndarray]:
    """Forward-difference Jacobians ``A = ∂f/∂x``, ``B = ∂f/∂u`` at ``(x0, u0)``."""
    x0 = np.asarray(x0, dtype=float).reshape(-1)
    u0 = np.asarray(u0, dtype=float).reshape(-1)
    f0 = np.asarray(f(x0, u0), dtype=float).reshape(-1)
    n, m = x0.size, u0.size
    A = np.zeros((n, n), dtype=float)
    B = np.zeros((n, m), dtype=float)
    for i in range(n):
        dx = np.zeros(n)
        dx[i] = eps
        A[:, i] = (np.asarray(f(x0 + dx, u0), dtype=float).reshape(-1) - f0) / eps
    for j in range(m):
        du = np.zeros(m)
        du[j] = eps
        B[:, j] = (np.asarray(f(x0, u0 + du), dtype=float).reshape(-1) - f0) / eps
    return A, B
