"""Planning visuals: frontier flood, heatmaps, RRT trees, thrust plots."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from flightlab.viz.core import ensure_media, save_gif, save_thumb
from flightlab.worlds import OccupancyGrid


def _occ_rgb(grid: OccupancyGrid) -> np.ndarray:
    img = np.ones((*grid.occ.shape, 3))
    img[grid.occ] = (0.2, 0.2, 0.2)
    return img


def animate_search(
    grid: OccupancyGrid,
    bfs_expanded: list[tuple[int, int]],
    dfs_expanded: list[tuple[int, int]],
    bfs_path: list[tuple[int, int]],
    dfs_path: list[tuple[int, int]],
    start: tuple[int, int],
    goal: tuple[int, int],
    *,
    path: Path | str | None = None,
    fps: int = 12,
) -> Path:
    dest = Path(path) if path else ensure_media() / "lab05.gif"
    base = _occ_rgb(grid)
    fig, (ax_b, ax_d) = plt.subplots(1, 2, figsize=(9.0, 4.2))
    im_b = ax_b.imshow(base, interpolation="nearest")
    im_d = ax_d.imshow(base.copy(), interpolation="nearest")
    for ax, title in ((ax_b, "BFS blooms"), (ax_d, "DFS snakes")):
        ax.set_title(title)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle("frontier expansion")
    fig.tight_layout()

    def paint(img, expanded, path_cells, k):
        out = img.copy()
        for i, cell in enumerate(expanded[:k]):
            t = 0.35 + 0.5 * i / max(len(expanded), 1)
            out[cell] = (0.35, 0.55, 0.95) if expanded is bfs_expanded else (0.90, 0.45, 0.25)
            out[cell] = (
                out[cell][0] * t + 0.15,
                out[cell][1] * t + 0.15,
                out[cell][2] * t + 0.2,
            )
        if k >= len(expanded):
            for cell in path_cells:
                out[cell] = (0.15, 0.75, 0.35)
        out[start] = (1.0, 0.85, 0.1)
        out[goal] = (0.85, 0.15, 0.7)
        return out

    n = max(len(bfs_expanded), len(dfs_expanded), 1)
    idx = np.linspace(1, n, min(n, fps * 4)).astype(int)

    def update(k: int):
        im_b.set_data(paint(base, bfs_expanded, bfs_path, min(k, len(bfs_expanded))))
        im_d.set_data(paint(base, dfs_expanded, dfs_path, min(k, len(dfs_expanded))))
        return im_b, im_d

    anim = FuncAnimation(fig, update, frames=idx, blit=True, interval=1000 / fps)
    save_gif(anim, dest, fps=fps)
    update(n)
    save_thumb(fig, dest.with_name(dest.stem + "_thumb.png"))
    plt.close(fig)
    return dest


def expansion_heatmaps(
    grid_shape: tuple[int, int],
    panels: list[tuple[str, list[tuple[int, int]], list[tuple[int, int]]]],
    *,
    path: Path | str | None = None,
) -> Path:
    dest = Path(path) if path else ensure_media() / "lab06_thumb.png"
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.4))
    for ax, (title, expanded, path_cells) in zip(axes, panels, strict=True):
        heat = np.full(grid_shape, np.nan)
        for i, cell in enumerate(expanded):
            heat[cell] = i
        ax.imshow(heat, cmap="magma", interpolation="nearest")
        if path_cells:
            rr, cc = zip(*path_cells, strict=False)
            ax.plot(cc, rr, color="cyan", lw=1.4)
        ax.set_title(title, fontsize=10)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle("expansion heatmaps — Dijkstra / A* / inflated")
    fig.tight_layout()
    save_thumb(fig, dest)
    gif = dest.with_name("lab06.gif")
    anim = FuncAnimation(fig, lambda _i: [], frames=[0], blit=False)
    save_gif(anim, gif, fps=4)
    plt.close(fig)
    return gif


def animate_rrt(
    bounds: tuple[float, float, float, float],
    circles: list[tuple[tuple[float, float], float]],
    snapshots: list[tuple[np.ndarray, np.ndarray]],
    path: np.ndarray | None,
    start: np.ndarray,
    goal: np.ndarray,
    *,
    dest: Path | str | None = None,
    fps: int = 12,
) -> Path:
    """``snapshots`` is a list of (parents_xy, nodes_xy) as the tree grows."""
    out = Path(dest) if dest else ensure_media() / "lab07.gif"
    xmin, xmax, ymin, ymax = bounds
    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")
    ax.set_title("the tree growing")
    for (cx, cy), r in circles:
        ax.add_patch(plt.Circle((cx, cy), r, color="#7f8c8d", alpha=0.45))
    (edges,) = ax.plot([], [], color="#1f4e79", lw=0.6, alpha=0.7)
    (path_ln,) = ax.plot([], [], color="#27ae60", lw=2.2)
    ax.plot(*start, "o", color="#f1c40f", ms=8)
    ax.plot(*goal, "o", color="#8e44ad", ms=8)
    fig.tight_layout()

    def update(i: int):
        nodes, parent_idx = snapshots[i]
        xs, ys = [], []
        for k, p in enumerate(parent_idx):
            if p < 0:
                continue
            xs += [nodes[p, 0], nodes[k, 0], np.nan]
            ys += [nodes[p, 1], nodes[k, 1], np.nan]
        edges.set_data(xs, ys)
        if i == len(snapshots) - 1 and path is not None and len(path):
            path_ln.set_data(path[:, 0], path[:, 1])
        return edges, path_ln

    idx = np.linspace(0, len(snapshots) - 1, min(len(snapshots), fps * 4)).astype(int)
    anim = FuncAnimation(fig, update, frames=idx, blit=True, interval=1000 / fps)
    save_gif(anim, out, fps=fps)
    update(len(snapshots) - 1)
    save_thumb(fig, out.with_name(out.stem + "_thumb.png"))
    plt.close(fig)
    return out


def thrust_scaling_figure(
    curves: list[tuple[str, np.ndarray, np.ndarray]],
    u_max: float,
    *,
    path: Path | str | None = None,
) -> Path:
    dest = Path(path) if path else ensure_media() / "lab09_thumb.png"
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    colors = ["#1f4e79", "#27ae60", "#c0392b"]
    for (label, t, thrust), c in zip(curves, colors, strict=False):
        ax.plot(t, thrust, lw=1.8, label=label, color=c)
    ax.axhspan(0, u_max, color="#27ae60", alpha=0.08)
    ax.axhline(u_max, color="#7f8c8d", ls="--", lw=1.0, label="u_max")
    ax.set_xlabel("t [s]")
    ax.set_ylabel("peak rotor |u| [N]")
    ax.set_title("time is the free variable")
    ax.legend(frameon=False)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    save_thumb(fig, dest)
    gif = dest.with_name("lab09.gif")
    anim = FuncAnimation(fig, lambda _i: [], frames=[0], blit=False)
    save_gif(anim, gif, fps=4)
    plt.close(fig)
    return gif
