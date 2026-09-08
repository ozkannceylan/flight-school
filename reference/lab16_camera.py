"""Reference implementation for Lab 16 — The Camera Is a Matrix."""

from __future__ import annotations

import numpy as np

from flightlab.render import to_camera


def project(K: np.ndarray, R: np.ndarray, C: np.ndarray, X: np.ndarray) -> np.ndarray:
    Xc = to_camera(R, C, X)
    z = Xc[..., 2]
    uv = np.full(Xc.shape[:-1] + (2,), np.nan, dtype=float)
    ok = z > 1e-8
    uv[ok, 0] = K[0, 0] * Xc[ok, 0] / z[ok] + K[0, 2]
    uv[ok, 1] = K[1, 1] * Xc[ok, 1] / z[ok] + K[1, 2]
    return uv


def calibrate_K(X: np.ndarray, uv: np.ndarray, R: np.ndarray, C: np.ndarray) -> np.ndarray:
    Xc = to_camera(R, C, np.asarray(X, dtype=float))
    uv = np.asarray(uv, dtype=float).reshape(-1, 2)
    xn = Xc[:, 0] / Xc[:, 2]
    yn = Xc[:, 1] / Xc[:, 2]
    Au = np.column_stack([xn, np.ones(len(xn))])
    Av = np.column_stack([yn, np.ones(len(yn))])
    fx, cx = np.linalg.lstsq(Au, uv[:, 0], rcond=None)[0]
    fy, cy = np.linalg.lstsq(Av, uv[:, 1], rcond=None)[0]
    return np.array([[fx, 0.0, cx], [0.0, fy, cy], [0.0, 0.0, 1.0]], dtype=float)


def reprojection_error(K: np.ndarray, R: np.ndarray, C: np.ndarray, X: np.ndarray, uv: np.ndarray) -> float:
    hat = project(K, R, C, X)
    d = hat - np.asarray(uv, dtype=float).reshape(-1, 2)
    return float(np.sqrt(np.nanmean(np.sum(d * d, axis=1))))
