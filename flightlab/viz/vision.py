"""Vision / learning visuals for Labs 16–22."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from flightlab.viz.core import ensure_media, save_gif, save_thumb


def camera_world_figure(
    img: np.ndarray,
    landmarks_uv: np.ndarray,
    landmarks_re: np.ndarray | None = None,
    *,
    path: Path | str | None = None,
) -> Path:
    dest = Path(path) if path else ensure_media() / "lab16_thumb.png"
    fig, ax = plt.subplots(figsize=(5.6, 4.2))
    ax.imshow(img, cmap="gray", vmin=0, vmax=1, origin="upper")
    ax.scatter(landmarks_uv[:, 0], landmarks_uv[:, 1], s=28, c="#c0392b", label="project")
    if landmarks_re is not None:
        ax.scatter(landmarks_re[:, 0], landmarks_re[:, 1], s=16, facecolors="none", edgecolors="#1f4e79", label="reproject")
    ax.set_title("camera view")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    save_thumb(fig, dest)
    plt.close(fig)
    return dest


def flow_quiver_figure(
    img: np.ndarray,
    pts: np.ndarray,
    flow: np.ndarray,
    flow_gt: np.ndarray | None = None,
    *,
    path: Path | str | None = None,
) -> Path:
    dest = Path(path) if path else ensure_media() / "lab17_thumb.png"
    fig, ax = plt.subplots(figsize=(5.8, 4.4))
    ax.imshow(img, cmap="gray", vmin=0, vmax=1, origin="upper")
    ax.quiver(pts[:, 0], pts[:, 1], flow[:, 0], flow[:, 1], color="#d35400", angles="xy", scale_units="xy", scale=1, width=0.004, label="LK")
    if flow_gt is not None:
        ax.quiver(pts[:, 0], pts[:, 1], flow_gt[:, 0], flow_gt[:, 1], color="#1f4e79", angles="xy", scale_units="xy", scale=1, width=0.003, alpha=0.7, label="analytic")
    ax.set_title("optical flow")
    ax.legend(frameon=False)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.tight_layout()
    save_thumb(fig, dest)
    plt.close(fig)
    return dest


def mlp_flight_figure(t: np.ndarray, ys: np.ndarray, zs: np.ndarray, *, path: Path | str | None = None) -> Path:
    dest = Path(path) if path else ensure_media() / "lab18_thumb.png"
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    ax.plot(t, ys, label="y", lw=1.8)
    ax.plot(t, zs, label="z", lw=1.8)
    ax.axhline(1.0, color="#888", ls="--", lw=0.8)
    ax.set_xlabel("t [s]")
    ax.set_title("MLP policy at hover")
    ax.legend(frameon=False)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    save_thumb(fig, dest)
    plt.close(fig)
    return dest


def descent_figure(
    paths: list[tuple[str, np.ndarray]],
    *,
    path: Path | str | None = None,
) -> Path:
    dest = Path(path) if path else ensure_media() / "lab19_thumb.png"
    w0 = np.linspace(-1.5, 3.0, 80)
    w1 = np.linspace(-2.0, 1.5, 80)
    W0, W1 = np.meshgrid(w0, w1)
    Z = (W0 - 1.0) ** 2 + 25.0 * (W1 + 0.5) ** 2
    fig, ax = plt.subplots(figsize=(5.8, 4.6))
    ax.contour(W0, W1, Z, levels=16, cmap="Greys")
    colors = ("#1f4e79", "#c0392b", "#27ae60")
    for (name, ws), col in zip(paths, colors, strict=False):
        ax.plot(ws[:, 0], ws[:, 1], color=col, lw=1.8, label=name)
        ax.scatter(ws[:1, 0], ws[:1, 1], c=col, s=24)
    ax.scatter([1.0], [-0.5], c="k", marker="*", s=80, label="min", zorder=5)
    ax.set_xlabel("w0")
    ax.set_ylabel("w1")
    ax.set_title("three descents")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    save_thumb(fig, dest)
    plt.close(fig)
    return dest


def learning_curves_figure(
    train: np.ndarray,
    val: np.ndarray,
    train_reg: np.ndarray,
    val_reg: np.ndarray,
    *,
    path: Path | str | None = None,
) -> Path:
    dest = Path(path) if path else ensure_media() / "lab20_thumb.png"
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(8.4, 3.6), sharey=True)
    ax0.plot(train, label="train")
    ax0.plot(val, label="val")
    ax0.set_title("no regularisation")
    ax1.plot(train_reg, label="train")
    ax1.plot(val_reg, label="val")
    ax1.set_title("with L2")
    for ax in (ax0, ax1):
        ax.set_xlabel("epoch")
        ax.legend(frameon=False)
        ax.grid(True, alpha=0.3)
    ax0.set_ylabel("MSE")
    fig.suptitle("when fitting better means knowing less")
    fig.tight_layout()
    save_thumb(fig, dest)
    plt.close(fig)
    return dest


def filter_grid_figure(filters: np.ndarray, *, path: Path | str | None = None) -> Path:
    dest = Path(path) if path else ensure_media() / "lab21_thumb.png"
    n = len(filters)
    cols = min(n, 4)
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(6.0, 2.2 * rows))
    axes = np.atleast_1d(axes).ravel()
    for i, ax in enumerate(axes):
        if i < n:
            ax.imshow(filters[i], cmap="gray")
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle("learned first-layer filters")
    fig.tight_layout()
    save_thumb(fig, dest)
    plt.close(fig)
    return dest


def rl_curve_figure(
    returns: np.ndarray,
    lqr_return: float,
    *,
    path: Path | str | None = None,
) -> Path:
    dest = Path(path) if path else ensure_media() / "lab22_thumb.png"
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.plot(returns, color="#1f4e79", lw=1.8, label="CEM")
    ax.axhline(lqr_return, color="#c0392b", ls="--", lw=1.6, label="LQR, zero samples")
    ax.set_xlabel("CEM iteration")
    ax.set_ylabel("episode return")
    ax.set_title("learning to hover")
    ax.legend(frameon=False)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    save_thumb(fig, dest)
    plt.close(fig)
    return dest
