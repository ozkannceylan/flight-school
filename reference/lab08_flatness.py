"""Reference implementation for Lab 08 — Plan in Flat Space, Fly in Real Space."""

from __future__ import annotations

import numpy as np

from flightlab.dynamics import PlanarQuadrotor
from flightlab.planning.flatness import eval_piecewise, flat_to_xu as flat_to_xu_core
from flightlab.planning.flatness import piecewise_quintic

WAYPOINTS = np.array(
    [
        [0.0, 1.0],
        [1.0, 1.55],
        [2.1, 1.15],
        [3.0, 1.70],
    ]
)
DURATIONS = np.array([1.4, 1.4, 1.4])


def flat_to_xu(y, z, yd, zd, ydd, zdd, yj, zj, ys, zs, plant: PlanarQuadrotor):
    return flat_to_xu_core(y, z, yd, zd, ydd, zdd, yj, zj, ys, zs, plant)


def sample_flat_traj(plant: PlanarQuadrotor, dt: float = 0.02, scale: float = 1.0):
    durs = scale * DURATIONS
    sy = piecewise_quintic(WAYPOINTS[:, 0], durs)
    sz = piecewise_quintic(WAYPOINTS[:, 1], durs)
    T = float(np.sum(durs))
    n = int(round(T / dt))
    t = np.linspace(0.0, n * dt, n + 1)
    xs = np.zeros((n + 1, 6))
    us = np.zeros((n + 1, 2))
    for i, ti in enumerate(t):
        y, yd, ydd, yj, ys = eval_piecewise(sy, durs, ti)
        z, zd, zdd, zj, zs = eval_piecewise(sz, durs, ti)
        xs[i], us[i] = flat_to_xu(y, z, yd, zd, ydd, zdd, yj, zj, ys, zs, plant)
    return t, xs, us


def ff_fb_control(x, x_nom, u_nom, K):
    return np.asarray(u_nom, dtype=float) - K @ (
        np.asarray(x, dtype=float).reshape(-1) - np.asarray(x_nom, dtype=float).reshape(-1)
    )


def fb_only_control(x, x_nom, u_hover, K):
    return np.asarray(u_hover, dtype=float) - K @ (
        np.asarray(x, dtype=float).reshape(-1) - np.asarray(x_nom, dtype=float).reshape(-1)
    )
