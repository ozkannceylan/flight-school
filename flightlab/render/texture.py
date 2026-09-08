"""Procedural ground textures and a pinhole renderer (Labs 16–17, 21)."""

from __future__ import annotations

import numpy as np

from flightlab.render.camera import IMG_H, IMG_W, camera_from_planar, default_K


def checker(xw: np.ndarray, yw: np.ndarray, period: float = 0.35) -> np.ndarray:
    """0/1 checkerboard on the ground plane."""
    i = np.floor(xw / period)
    j = np.floor(yw / period)
    return np.mod(i + j, 2.0)


def stripes(xw: np.ndarray, yw: np.ndarray, period: float = 0.25) -> np.ndarray:
    """Soft vertical stripes (vary in y) — good LK texture along x-flow."""
    return 0.5 + 0.5 * np.sin(2.0 * np.pi * yw / period)


def wavy(xw: np.ndarray, yw: np.ndarray, period: float = 0.35) -> np.ndarray:
    """Smooth 2-D sinusoid. LK needs gradients, not hard edges."""
    return 0.5 + 0.5 * np.sin(2.0 * np.pi * xw / period) * np.sin(2.0 * np.pi * yw / period)


def blank(xw: np.ndarray, yw: np.ndarray) -> np.ndarray:
    """Textureless — the aperture / LK failure case."""
    return np.full_like(np.asarray(xw, dtype=float), 0.45)


def render_ground(
    py: float,
    pz: float,
    theta: float = 0.0,
    *,
    K: np.ndarray | None = None,
    width: int = IMG_W,
    height: int = IMG_H,
    texture=checker,
    period: float = 0.35,
) -> np.ndarray:
    """Ray-cast each pixel onto ``z=0``. Returns a float image in ``[0, 1]``."""
    K = default_K() if K is None else np.asarray(K, dtype=float)
    R, C = camera_from_planar(py, pz, theta)
    # Pixel grid → camera rays: d = K^{-1} [u, v, 1]
    us = np.arange(width, dtype=float)
    vs = np.arange(height, dtype=float)
    uu, vv = np.meshgrid(us, vs, indexing="xy")
    pix = np.stack([uu, vv, np.ones_like(uu)], axis=-1)
    Kinv = np.linalg.inv(K)
    dirs_cam = pix @ Kinv.T
    # Ray in world: X(s) = C + s * R.T @ d_cam. Hit z=0.
    dirs_w = dirs_cam @ R
    dz = dirs_w[..., 2]
    img = np.full((height, width), 0.15, dtype=float)
    ok = np.abs(dz) > 1e-8
    s = np.zeros_like(dz)
    s[ok] = (0.0 - C[2]) / dz[ok]
    hit = ok & (s > 1e-6)
    X = np.zeros(dirs_w.shape)
    X[hit] = C + s[hit, None] * dirs_w[hit]
    try:
        val = texture(X[hit, 0], X[hit, 1], period)
    except TypeError:
        val = texture(X[hit, 0], X[hit, 1])
    img[hit] = np.clip(val, 0.0, 1.0)
    return img


def render_gate(col: float, *, size: int = 24, width: int = 3, seed: int = 0) -> np.ndarray:
    """Tiny synthetic 'gate': a bright vertical bar on noise. Label is the column."""
    rng = np.random.default_rng(seed)
    img = 0.25 + 0.08 * rng.normal(size=(size, size))
    c0 = int(np.clip(round(col) - width // 2, 0, size - width))
    img[:, c0 : c0 + width] = 0.95
    return np.clip(img, 0.0, 1.0)
