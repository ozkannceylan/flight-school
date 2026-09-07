"""Reference implementation for Lab 17 — Motion From Brightness."""

from __future__ import annotations

import numpy as np


def _gradients(I: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    Iy, Ix = np.gradient(I.astype(float))
    return Ix, Iy


def lucas_kanade(I1: np.ndarray, I2: np.ndarray, pts: np.ndarray, win: int = 5) -> np.ndarray:
    I1 = np.asarray(I1, dtype=float)
    I2 = np.asarray(I2, dtype=float)
    Ix, Iy = _gradients(I1)
    It = I2 - I1
    h, w = I1.shape
    pts = np.asarray(pts, dtype=float).reshape(-1, 2)
    flow = np.zeros((len(pts), 2), dtype=float)
    for i, (u, v) in enumerate(pts):
        c, r = int(round(u)), int(round(v))
        r0, r1 = max(0, r - win), min(h, r + win + 1)
        c0, c1 = max(0, c - win), min(w, c + win + 1)
        ix = Ix[r0:r1, c0:c1].ravel()
        iy = Iy[r0:r1, c0:c1].ravel()
        it = It[r0:r1, c0:c1].ravel()
        A = np.column_stack([ix, iy])
        try:
            duv, *_ = np.linalg.lstsq(A, -it, rcond=None)
        except np.linalg.LinAlgError:
            duv = np.zeros(2)
        flow[i] = duv
    return flow


def flow_to_vy(flow: np.ndarray, fx: float, altitude: float) -> float:
    u = np.asarray(flow, dtype=float).reshape(-1, 2)[:, 0]
    u = u[np.isfinite(u)]
    if u.size == 0:
        return 0.0
    return float(-np.mean(u) * altitude / fx)


def flow_hover_pd(
    y: float,
    z: float,
    theta: float,
    vy_flow: float,
    vz: float,
    omega: float,
    y_des: float = 0.0,
    z_des: float = 1.0,
    *,
    m: float = 1.0,
    g: float = 9.81,
    L: float = 0.25,
    I: float = 0.01,
) -> np.ndarray:
    ey, ez = y_des - y, z_des - z
    ay = 8.0 * ey - 5.0 * vy_flow
    az = 16.0 * ez - 8.0 * vz
    th_des = float(np.clip(-ay / max(g, 1e-6), -0.4, 0.4))
    alpha = 80.0 * (th_des - theta) - 12.0 * omega
    T = float(np.clip(m * (g + az), 0.3 * m * g, 2.2 * m * g))
    tau = I * alpha
    # τ = L (u1 − u2), T = u1 + u2
    u1 = 0.5 * T + 0.5 * tau / L
    u2 = 0.5 * T - 0.5 * tau / L
    return np.array([u1, u2], dtype=float)
