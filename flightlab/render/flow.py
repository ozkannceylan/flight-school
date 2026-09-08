"""Analytic optical-flow ground truth for a downward camera (Lab 17)."""

from __future__ import annotations

import numpy as np

from flightlab.render.camera import camera_from_planar, project


def analytic_flow(
    K: np.ndarray,
    py: float,
    pz: float,
    theta: float,
    dpy: float,
    dpz: float,
    dtheta: float,
    uv: np.ndarray,
) -> np.ndarray:
    """Finite-difference flow of ground-plane pixels under a planar pose step.

    ``uv`` is ``(N, 2)``. Returns ``(N, 2)`` pixel displacements.
    """
    R0, C0 = camera_from_planar(py, pz, theta)
    R1, C1 = camera_from_planar(py + dpy, pz + dpz, theta + dtheta)
    # Back-project each pixel onto z=0, then reproject at the next pose.
    K = np.asarray(K, dtype=float)
    Kinv = np.linalg.inv(K)
    uv = np.asarray(uv, dtype=float).reshape(-1, 2)
    pix = np.column_stack([uv, np.ones(len(uv))])
    dirs_cam = pix @ Kinv.T
    dirs_w = dirs_cam @ R0
    dz = dirs_w[:, 2]
    out = np.full((len(uv), 2), np.nan)
    ok = np.abs(dz) > 1e-8
    s = np.zeros(len(uv))
    s[ok] = (0.0 - C0[2]) / dz[ok]
    hit = ok & (s > 1e-6)
    X = C0 + s[:, None] * dirs_w
    uv1 = project(K, R1, C1, X)
    out[hit] = uv1[hit] - uv[hit]
    return out


def sample_track_points(width: int, height: int, n: int = 36, margin: int = 12) -> np.ndarray:
    """A regular grid of LK track points, inset from the border."""
    xs = np.linspace(margin, width - 1 - margin, int(np.sqrt(n)))
    ys = np.linspace(margin, height - 1 - margin, int(np.sqrt(n)))
    xx, yy = np.meshgrid(xs, ys)
    return np.column_stack([xx.ravel(), yy.ravel()])
