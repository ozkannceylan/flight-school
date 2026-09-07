"""Lab 21 — Weight Sharing Earns Its Keep.

A tiny NumPy conv vs. a parameter-matched MLP on synthetic gates.

    BACKEND=numpy python labs/lab21_cnn/check.py
    BACKEND=torch python labs/lab21_cnn/check.py   # optional
"""

from __future__ import annotations

import os

import numpy as np


# ---------------------------------------------------------------------------
# TODO 1 — valid conv2d  (≤15 lines)
# ---------------------------------------------------------------------------
def conv2d(x: np.ndarray, w: np.ndarray) -> np.ndarray:
    """``x (N,H,W)``, ``w (F,kh,kw)`` → ``(N,F,H-kh+1,W-kw+1)``."""
    # TODO(1)
    raise NotImplementedError("TODO 1: conv2d")


# ---------------------------------------------------------------------------
# TODO 2 — CNN and MLP forward  (≤12 lines)
# ---------------------------------------------------------------------------
def cnn_forward(x: np.ndarray, conv_w: np.ndarray, fc_w: np.ndarray, fc_b: np.ndarray) -> np.ndarray:
    """ReLU conv, mean over filters+rows, ``argmax`` over width, plus 1 (valid-conv shift)."""
    # TODO(2)
    raise NotImplementedError("TODO 2: cnn_forward")


def mlp_forward(x: np.ndarray, W: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Flatten ``x`` and ``y = x W + b``. Same output."""
    # TODO(2)
    raise NotImplementedError("TODO 2: mlp_forward")


# ---------------------------------------------------------------------------
# TODO 3 — a training step (GD on the readout is enough)  (≤12 lines)
# ---------------------------------------------------------------------------
def train_readout(features: np.ndarray, y: np.ndarray, w: np.ndarray, b: np.ndarray, lr: float):
    """One MSE GD step on ``yhat = features @ w + b``. Return ``(w, b)``."""
    # TODO(3)
    raise NotImplementedError("TODO 3: train_readout")


def backend() -> str:
    return os.environ.get("BACKEND", "numpy").strip().lower()


def n_params_cnn(conv_w: np.ndarray, fc_w: np.ndarray, fc_b: np.ndarray) -> int:
    return int(conv_w.size + fc_w.size + fc_b.size)


def n_params_mlp(W: np.ndarray, b: np.ndarray) -> int:
    return int(W.size + b.size)
