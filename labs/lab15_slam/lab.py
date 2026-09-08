"""Lab 15 — Both at Once.

2-D pose-graph SLAM. Odometry edges, one loop closure, Gauss-Newton.

    python labs/lab15_slam/check.py
    python labs/lab15_slam/demo.py
"""

from __future__ import annotations

import numpy as np

from scipy.sparse import csc_matrix
from scipy.sparse.linalg import spsolve

from flightlab.geometry import ominus, oplus, wrap


# ---------------------------------------------------------------------------
# TODO 1 — relative-pose error  (≤8 lines)
# ---------------------------------------------------------------------------
def edge_error(xi: np.ndarray, xj: np.ndarray, z: np.ndarray) -> np.ndarray:
    """``e = ominus(z, ominus(xi, xj))`` — 3-vector, angle wrapped."""
    # TODO(1)
    raise NotImplementedError("TODO 1: edge_error")


# ---------------------------------------------------------------------------
# TODO 2 — compose the open-loop odometry chain  (≤8 lines)
# ---------------------------------------------------------------------------
def compose_odometry(n: int, odom_edges: list) -> np.ndarray:
    """Start at the origin. For each ``(i, j, z, info)`` do ``x[j] = oplus(x[i], z)``."""
    # TODO(2)
    raise NotImplementedError("TODO 2: compose_odometry")


# ---------------------------------------------------------------------------
# TODO 3 — Gauss-Newton on the pose graph  (≤15 lines)
# ---------------------------------------------------------------------------
def optimize(
    poses: np.ndarray,
    edges: list,
    *,
    n_iter: int = 8,
    damp: float = 1e-4,
) -> np.ndarray:
    """Hold pose 0 fixed. ``gauss_newton_step`` is provided — call it ``n_iter`` times."""
    # TODO(3)
    raise NotImplementedError("TODO 3: optimize")


def residual_and_jacobian(poses: np.ndarray, edges: list) -> tuple[np.ndarray, np.ndarray]:
    """Stack edge errors. Numerical Jacobian wrt poses 1..N-1. Provided."""
    poses = np.asarray(poses, dtype=float)
    n = len(poses)
    r_list = [edge_error(poses[i], poses[j], z) for i, j, z, _info in edges]
    r = np.concatenate(r_list) if r_list else np.zeros(0)
    dim = 3 * (n - 1)
    J = np.zeros((r.size, dim))
    eps = 1e-5
    for k in range(1, n):
        for d in range(3):
            plus = poses.copy()
            plus[k, d] += eps
            rp = np.concatenate([edge_error(plus[i], plus[j], z) for i, j, z, _ in edges])
            J[:, 3 * (k - 1) + d] = (rp - r) / eps
    return r, J


def gauss_newton_step(poses: np.ndarray, edges: list, *, damp: float = 1e-4) -> np.ndarray:
    """One sparse-friendly dense GN step. Pose 0 stays put. Provided."""
    poses = np.asarray(poses, dtype=float).copy()
    r, J = residual_and_jacobian(poses, edges)
    if r.size == 0:
        return poses
    omegas = []
    for _i, _j, _z, info in edges:
        omegas.append(np.asarray(info, dtype=float))
    W = _block_diag(omegas)
    H = J.T @ W @ J + damp * np.eye(J.shape[1])
    g = J.T @ W @ r
    try:
        dx = -np.asarray(spsolve(csc_matrix(H), g), dtype=float)
    except Exception:  # noqa: BLE001
        dx = -np.linalg.pinv(H) @ g
    # Same chart as the finite-difference Jacobian: add in (x, y, θ), not ⊕.
    for k in range(1, len(poses)):
        d = dx[3 * (k - 1) : 3 * k]
        poses[k, 0] += d[0]
        poses[k, 1] += d[1]
        poses[k, 2] = wrap(poses[k, 2] + d[2])
    return poses


def _block_diag(mats: list[np.ndarray]) -> np.ndarray:
    n = sum(m.shape[0] for m in mats)
    out = np.zeros((n, n))
    i = 0
    for m in mats:
        s = m.shape[0]
        out[i : i + s, i : i + s] = m
        i += s
    return out


def ate(est: np.ndarray, gt: np.ndarray) -> float:
    e = np.asarray(est)[:, :2] - np.asarray(gt)[:, :2]
    return float(np.sqrt(np.mean(np.sum(e * e, axis=1))))
