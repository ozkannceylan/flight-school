"""Estimation visuals: belief clouds, Bayes stacks, particles, maps, pose graphs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Ellipse

from flightlab.viz.core import ensure_media, save_gif, save_thumb
from flightlab.worlds import OccupancyGrid


def _occ_rgb(grid: OccupancyGrid) -> np.ndarray:
    img = np.ones((*grid.occ.shape, 3))
    img[grid.occ] = (0.18, 0.18, 0.18)
    return img


def animate_belief_set(
    grid: OccupancyGrid,
    beliefs: list[np.ndarray],
    truths: list[tuple[int, int]],
    *,
    path: Path | str | None = None,
    fps: int = 6,
) -> Path:
    dest = Path(path) if path else ensure_media() / "lab10.gif"
    base = _occ_rgb(grid)
    fig, ax = plt.subplots(figsize=(6.2, 4.6))
    im = ax.imshow(base, interpolation="nearest")
    ax.set_xticks([])
    ax.set_yticks([])
    title = ax.set_title("possibility set")
    fig.tight_layout()

    def paint(k: int):
        out = base.copy()
        bel = beliefs[min(k, len(beliefs) - 1)]
        out[bel] = (0.35, 0.62, 0.95)
        tr = truths[min(k, len(truths) - 1)]
        out[tr] = (0.95, 0.25, 0.2)
        n = int(bel.sum())
        title.set_text(f"possibility set  |  {n} cells  t={k}")
        return out

    frames = list(range(len(beliefs)))

    def update(k: int):
        im.set_data(paint(k))
        return (im,)

    anim = FuncAnimation(fig, update, frames=frames, blit=False, interval=1000 / fps)
    save_gif(anim, dest, fps=fps)
    update(len(beliefs) - 1)
    save_thumb(fig, dest.with_name(dest.stem + "_thumb.png") if dest.suffix == ".gif" else dest)
    plt.close(fig)
    return dest


def animate_bayes_stack(
    priors: list[np.ndarray],
    likes: list[np.ndarray],
    posts: list[np.ndarray],
    truths: list[int],
    doors: np.ndarray,
    *,
    path: Path | str | None = None,
    fps: int = 4,
) -> Path:
    dest = Path(path) if path else ensure_media() / "lab11.gif"
    n = priors[0].size
    xs = np.arange(n)
    fig, axes = plt.subplots(3, 1, figsize=(7.2, 5.4), sharex=True)
    bars = []
    titles = ("prior  p(x)", "likelihood  p(z|x)", "posterior  p(x|z)")
    for ax, title in zip(axes, titles, strict=True):
        b = ax.bar(xs, np.zeros(n), color="#1f4e79", width=0.85)
        ax.set_ylim(0.0, 1.05)
        ax.set_ylabel(title)
        ax.grid(True, axis="y", alpha=0.25)
        bars.append(b)
    axes[-1].set_xlabel("cell")
    for d in np.where(doors)[0]:
        for ax in axes:
            ax.axvline(d, color="#c0392b", ls="--", lw=0.8, alpha=0.5)
    fig.suptitle("discrete Bayes")
    fig.tight_layout()

    def update(k: int):
        for b, data in zip(bars, (priors[k], likes[k], posts[k]), strict=True):
            m = float(np.max(data)) if np.max(data) > 0 else 1.0
            for rect, v in zip(b, data, strict=True):
                rect.set_height(v / m if m > 1.0 else v)
        t = truths[k]
        for b in bars:
            for i, rect in enumerate(b):
                rect.set_color("#c0392b" if i == t else "#1f4e79")
        return []

    anim = FuncAnimation(fig, update, frames=len(priors), blit=False, interval=1000 / fps)
    save_gif(anim, dest, fps=fps)
    update(len(priors) - 1)
    save_thumb(fig, dest.with_name("lab11_thumb.png"))
    plt.close(fig)
    return dest


def kf_pf_figure(
    xs: np.ndarray,
    mus: np.ndarray,
    sigmas: np.ndarray,
    particles: np.ndarray,
    *,
    path: Path | str | None = None,
) -> Path:
    dest = Path(path) if path else ensure_media() / "lab12_thumb.png"
    fig, (ax_k, ax_p) = plt.subplots(1, 2, figsize=(8.6, 4.0), sharex=True, sharey=True)
    ax_k.plot(xs[:, 0], xs[:, 1], color="#222", lw=1.4, label="truth")
    ax_k.plot(mus[:, 0], mus[:, 1], color="#1f4e79", lw=1.6, label="KF mean")
    # last covariance ellipse in (y, z)
    P = sigmas[-1][:2, :2]
    evals, evecs = np.linalg.eigh(P)
    evals = np.clip(evals, 1e-8, None)
    ang = np.degrees(np.arctan2(evecs[1, 1], evecs[0, 1]))
    w, h = 2 * np.sqrt(evals)
    ell = Ellipse(
        (mus[-1, 0], mus[-1, 1]),
        w,
        h,
        angle=ang,
        fill=False,
        ec="#1f4e79",
        lw=1.6,
    )
    ax_k.add_patch(ell)
    ax_k.scatter(xs[-1, 0], xs[-1, 1], c="#c0392b", s=28, zorder=5)
    ax_k.set_title("Kalman — covariance")
    ax_k.set_xlabel("y")
    ax_k.set_ylabel("z")
    ax_k.legend(frameon=False, loc="upper right")
    ax_k.grid(True, alpha=0.3)

    ax_p.plot(xs[:, 0], xs[:, 1], color="#222", lw=1.4)
    ax_p.scatter(particles[:, 0], particles[:, 1], s=8, c="#d35400", alpha=0.45)
    ax_p.scatter(xs[-1, 0], xs[-1, 1], c="#c0392b", s=28, zorder=5)
    ax_p.set_title("particles")
    ax_p.set_xlabel("y")
    ax_p.grid(True, alpha=0.3)
    fig.suptitle("two beliefs, one flight")
    fig.tight_layout()
    save_thumb(fig, dest)
    plt.close(fig)
    return dest


def animate_mcl(
    grid: OccupancyGrid,
    poses: list[np.ndarray],
    clouds: list[np.ndarray],
    *,
    path: Path | str | None = None,
    fps: int = 6,
) -> Path:
    dest = Path(path) if path else ensure_media() / "lab13.gif"
    base = _occ_rgb(grid)
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    ax.imshow(base, interpolation="nearest")
    sc = ax.scatter([], [], s=8, c="#f39c12", alpha=0.55)
    (truth,) = ax.plot([], [], "o", color="#c0392b", ms=8)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("Monte Carlo localization")
    fig.tight_layout()

    def update(k: int):
        pts = clouds[k]
        sc.set_offsets(np.column_stack([pts[:, 0], pts[:, 1]]))
        p = poses[k]
        truth.set_data([p[0]], [p[1]])
        return sc, truth

    anim = FuncAnimation(fig, update, frames=len(poses), blit=True, interval=1000 / fps)
    save_gif(anim, dest, fps=fps)
    update(len(poses) - 1)
    save_thumb(fig, dest.with_name("lab13_thumb.png"))
    plt.close(fig)
    return dest


def animate_mapping(
    grid: OccupancyGrid,
    logodds_seq: list[np.ndarray],
    poses: np.ndarray,
    *,
    path: Path | str | None = None,
    fps: int = 4,
) -> Path:
    dest = Path(path) if path else ensure_media() / "lab14.gif"
    fig, ax = plt.subplots(figsize=(5.4, 4.4))
    vmax = 4.0
    im = ax.imshow(np.zeros(grid.occ.shape), cmap="gray", vmin=-vmax, vmax=vmax)
    (tr,) = ax.plot([], [], "r.-", lw=1.0, ms=4)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("log-odds map")
    fig.tight_layout()

    def update(k: int):
        im.set_data(logodds_seq[k])
        tr.set_data(poses[: k + 1, 0], poses[: k + 1, 1])
        return im, tr

    anim = FuncAnimation(fig, update, frames=len(logodds_seq), blit=True, interval=1000 / fps)
    save_gif(anim, dest, fps=fps)
    update(len(logodds_seq) - 1)
    save_thumb(fig, dest.with_name("lab14_thumb.png"))
    plt.close(fig)
    return dest


def slam_before_after(
    gt: np.ndarray,
    before: np.ndarray,
    after: np.ndarray,
    *,
    path: Path | str | None = None,
) -> Path:
    dest = Path(path) if path else ensure_media() / "lab15_thumb.png"
    fig, (ax_b, ax_a) = plt.subplots(1, 2, figsize=(8.6, 4.0), sharex=True, sharey=True)
    for ax, est, title in (
        (ax_b, before, "odometry only"),
        (ax_a, after, "after loop closure"),
    ):
        ax.plot(gt[:, 0], gt[:, 1], "k--", lw=1.4, label="truth")
        ax.plot(est[:, 0], est[:, 1], color="#1f4e79", lw=1.8, label="estimate")
        ax.scatter(gt[0, 0], gt[0, 1], c="#c0392b", s=36, zorder=5)
        ax.set_aspect("equal", adjustable="box")
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        ax.legend(frameon=False, loc="upper right")
    fig.suptitle("pose-graph SLAM")
    fig.tight_layout()
    save_thumb(fig, dest)
    plt.close(fig)
    return dest
