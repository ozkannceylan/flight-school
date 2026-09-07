"""Tiny synthetic datasets for Labs 18–22."""

from __future__ import annotations

import numpy as np

from flightlab.control import linearize
from flightlab.dynamics import PlanarQuadrotor
from flightlab.render.texture import render_gate
from flightlab.resolve import get


def lqr_policy_dataset(n: int = 80, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """State / LQR-action pairs near hover. Uses ``get('lab04')``."""
    plant = PlanarQuadrotor()
    lab04 = get("lab04")
    A, B = linearize(plant.f, plant.reset(), plant.hover_input())
    Q, R = lab04.design_QR()
    K, _ = lab04.lqr(A, B, Q, R)
    rng = np.random.default_rng(seed)
    x_eq = plant.reset()
    u_eq = plant.hover_input()
    xs = x_eq + rng.normal(0.0, [0.08, 0.08, 0.05, 0.05, 0.05, 0.04], size=(n, 6))
    us = np.stack([lab04.lqr_control(x, x_eq, u_eq, K) for x in xs])
    return xs, us


def sine_dataset(
    n_train: int = 8,
    n_val: int = 30,
    seed: int = 0,
    noise: float = 0.08,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """1-D ``sin(2x)`` with a tiny train set (easy to overfit)."""
    rng = np.random.default_rng(seed)
    x_tr = rng.uniform(-1.0, 1.0, size=n_train)
    x_va = np.linspace(-1.0, 1.0, n_val)
    y_tr = np.sin(2.0 * x_tr) + rng.normal(0.0, noise, size=n_train)
    y_va = np.sin(2.0 * x_va)
    return x_tr.reshape(-1, 1), y_tr.reshape(-1, 1), x_va.reshape(-1, 1), y_va.reshape(-1, 1)


def gate_dataset(n: int = 120, size: int = 24, seed: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """Images + integer column of a vertical gate."""
    rng = np.random.default_rng(seed)
    cols = rng.integers(3, size - 3, size=n)
    imgs = np.stack([render_gate(float(c), size=size, seed=int(seed + i + 1)) for i, c in enumerate(cols)])
    return imgs.astype(float), cols.astype(float)
