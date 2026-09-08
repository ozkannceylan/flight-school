"""Pinhole camera sitting on the planar quadrotor, looking down.

World: ``+y`` right, ``+z`` up, ``+x`` out of the page (same as Lab 01).
Camera centre is ``(0, p_y, p_z)``. Optical axis is ``−body z``.
"""

from __future__ import annotations

import numpy as np

# Default calibration used by Labs 16–17 and 21.
IMG_W, IMG_H = 160, 120
FX = FY = 200.0
CX, CY = 80.0, 60.0


def default_K() -> np.ndarray:
    return np.array([[FX, 0.0, CX], [0.0, FY, CY], [0.0, 0.0, 1.0]], dtype=float)


def camera_from_planar(py: float, pz: float, theta: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
    """World→camera ``R`` and camera centre ``C`` for a planar-quad pose."""
    c, s = np.cos(theta), np.sin(theta)
    # Rows of R are camera axes in world. x_cam = body y, y_cam = body x, z_cam = −body z.
    R = np.array(
        [
            [0.0, c, s],
            [1.0, 0.0, 0.0],
            [0.0, s, -c],
        ],
        dtype=float,
    )
    C = np.array([0.0, float(py), float(pz)], dtype=float)
    return R, C


def to_camera(R: np.ndarray, C: np.ndarray, X: np.ndarray) -> np.ndarray:
    """``X`` is ``(..., 3)`` world points → camera-frame points."""
    X = np.asarray(X, dtype=float)
    return (R @ (X - C).T).T


def project(K: np.ndarray, R: np.ndarray, C: np.ndarray, X: np.ndarray) -> np.ndarray:
    """Pinhole projection. Returns ``(..., 2)`` pixel coords. Behind-camera → nan."""
    Xc = to_camera(R, C, X)
    z = Xc[..., 2]
    uv = np.full(Xc.shape[:-1] + (2,), np.nan, dtype=float)
    ok = z > 1e-8
    uv[ok, 0] = K[0, 0] * Xc[ok, 0] / z[ok] + K[0, 2]
    uv[ok, 1] = K[1, 1] * Xc[ok, 1] / z[ok] + K[1, 2]
    return uv


def landmarks_lab16(n: int = 5) -> np.ndarray:
    """A grid of ground-plane (z=0) landmarks. Shape ``(n*n, 3)``."""
    xs = np.linspace(-1.2, 1.2, n)
    ys = np.linspace(-1.6, 1.6, n)
    xx, yy = np.meshgrid(xs, ys, indexing="xy")
    return np.column_stack([xx.ravel(), yy.ravel(), np.zeros(xx.size)])


def pose_lab16() -> tuple[float, float, float]:
    """A comfortable downward-looking hover: ``(p_y, p_z, θ)``."""
    return 0.15, 1.6, 0.05
