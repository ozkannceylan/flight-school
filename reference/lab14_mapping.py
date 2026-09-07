"""Reference implementation for Lab 14 — Known Pose, Unknown Map."""

from __future__ import annotations

import numpy as np

from flightlab.sensors import RangeSensor
from flightlab.worlds import OccupancyGrid

L_OCC = float(np.log(0.70 / 0.30))
L_FREE = float(np.log(0.30 / 0.70))


def inverse_beam(
    shape: tuple[int, int],
    pose: np.ndarray,
    z: float,
    angle: float,
    *,
    step: float = 0.25,
    max_range: float = 7.0,
    l_occ: float = L_OCC,
    l_free: float = L_FREE,
) -> np.ndarray:
    inc = np.zeros(shape, dtype=float)
    x, y, th = (float(pose[0]), float(pose[1]), float(pose[2]))
    a = th + float(angle)
    ca, sa = np.cos(a), np.sin(a)
    z = min(float(z), max_range)
    r = 0.0
    last = None
    rows, cols = shape
    while r + step < z:
        r += step
        c = int(np.floor(x + r * ca))
        rr = int(np.floor(y + r * sa))
        if rr < 0 or rr >= rows or c < 0 or c >= cols:
            break
        inc[rr, c] = l_free
        last = (rr, c)
    # occupied at the hit, if we actually hit something short of max range
    if z < max_range - 0.5 * step:
        c = int(np.floor(x + z * ca))
        rr = int(np.floor(y + z * sa))
        if 0 <= rr < rows and 0 <= c < cols:
            inc[rr, c] = l_occ
        elif last is not None:
            inc[last] = l_occ
    return inc


def logodds_update(l_map: np.ndarray, increment: np.ndarray, clip: float = 8.0) -> np.ndarray:
    return np.clip(np.asarray(l_map, dtype=float) + np.asarray(increment, dtype=float), -clip, clip)


def naive_miss(p: float, n: int, p_occ_given_miss: float = 0.05) -> float:
    q = float(p_occ_given_miss)
    p = float(p)
    for _ in range(int(n)):
        p = (p * q) / (p * q + (1.0 - p) * (1.0 - q))
    return p


def integrate_scan(
    l_map: np.ndarray,
    pose: np.ndarray,
    z: np.ndarray,
    sensor: RangeSensor,
) -> np.ndarray:
    out = np.asarray(l_map, dtype=float)
    for ang, zi in zip(sensor.angles, np.asarray(z, dtype=float), strict=True):
        inc = inverse_beam(out.shape, pose, float(zi), float(ang), max_range=sensor.max_range, step=sensor.step)
        out = logodds_update(out, inc)
    return out


def occupancy(l_map: np.ndarray) -> np.ndarray:
    return np.asarray(l_map, dtype=float) > 0.0
