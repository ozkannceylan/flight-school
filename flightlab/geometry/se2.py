"""Planar rigid poses ``(x, y, theta)``. Used by Labs 13 and 15."""

from __future__ import annotations

import numpy as np


def wrap(theta: float | np.ndarray) -> float | np.ndarray:
    """Wrap to (−π, π]."""
    return (np.asarray(theta, dtype=float) + np.pi) % (2.0 * np.pi) - np.pi


def ominus(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Relative pose of ``b`` in the frame of ``a``."""
    a = np.asarray(a, dtype=float).reshape(3)
    b = np.asarray(b, dtype=float).reshape(3)
    dx, dy = b[0] - a[0], b[1] - a[1]
    c, s = np.cos(a[2]), np.sin(a[2])
    return np.array([c * dx + s * dy, -s * dx + c * dy, wrap(b[2] - a[2])], dtype=float)


def oplus(a: np.ndarray, d: np.ndarray) -> np.ndarray:
    """Compose pose ``a`` with a body-frame increment ``d``."""
    a = np.asarray(a, dtype=float).reshape(3)
    d = np.asarray(d, dtype=float).reshape(3)
    c, s = np.cos(a[2]), np.sin(a[2])
    return np.array(
        [a[0] + c * d[0] - s * d[1], a[1] + s * d[0] + c * d[1], wrap(a[2] + d[2])],
        dtype=float,
    )


def ate_xy(est: np.ndarray, gt: np.ndarray) -> float:
    """RMSE of planar position (metres / cells)."""
    e = np.asarray(est, dtype=float)[:, :2] - np.asarray(gt, dtype=float)[:, :2]
    return float(np.sqrt(np.mean(np.sum(e * e, axis=1))))
