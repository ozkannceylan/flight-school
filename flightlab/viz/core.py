"""Matplotlib helpers: time-series scopes, 2-D animation, gif export.

Deterministic: no wall-clock, no unseeded RNG. Always use the Agg backend
when saving (demos import this module first).
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.patches import Circle

from flightlab.dynamics.planar_quad import IY, IZ, PlanarQuadrotor

ROOT = Path(__file__).resolve().parents[2]
MEDIA = ROOT / "media"


def ensure_media() -> Path:
    MEDIA.mkdir(parents=True, exist_ok=True)
    return MEDIA


def save_gif(anim: FuncAnimation, path: Path | str, *, fps: int = 20, dpi: int = 90) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    anim.save(str(path), writer=PillowWriter(fps=fps), dpi=dpi)
    return path


def save_thumb(fig: plt.Figure, path: Path | str) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=110, bbox_inches="tight")
    return path


def scope(
    t: np.ndarray,
    series: Sequence[np.ndarray],
    labels: Sequence[str],
    *,
    title: str = "",
    ylabel: str = "",
) -> plt.Figure:
    """Overlay 1-D signals vs time."""
    fig, ax = plt.subplots(figsize=(7, 3.6))
    for y, lab in zip(series, labels, strict=True):
        ax.plot(t, y, label=lab, lw=1.8)
    ax.set_xlabel("t [s]")
    if ylabel:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    ax.legend(frameon=False)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def falling_mass_figure(
    t: np.ndarray,
    z_euler: np.ndarray,
    z_rk4: np.ndarray,
    q_euler: np.ndarray | None = None,
    q_rk4: np.ndarray | None = None,
) -> plt.Figure:
    """Static hook: falling-mass z(t) plus an oscillator phase portrait."""
    if q_euler is None or q_rk4 is None:
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.plot(t, z_euler, "--", lw=1.8, label="Euler", color="#c0392b")
        ax.plot(t, z_rk4, lw=2.0, label="RK4", color="#1f4e79")
        ax.set_xlabel("t [s]")
        ax.set_ylabel("height z [m]")
        ax.set_title("Same plant, same step — two clocks")
        ax.legend(frameon=False)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        return fig

    fig, (ax_z, ax_ph) = plt.subplots(1, 2, figsize=(8.8, 4.0))
    ax_z.plot(t, z_euler, "--", lw=1.8, label="Euler", color="#c0392b")
    ax_z.plot(t, z_rk4, lw=2.0, label="RK4", color="#1f4e79")
    ax_z.set_xlabel("t [s]")
    ax_z.set_ylabel("height z [m]")
    ax_z.set_title("falling mass + drag")
    ax_z.legend(frameon=False)
    ax_z.grid(True, alpha=0.3)

    ax_ph.plot(q_euler[:, 0], q_euler[:, 1], "--", lw=1.6, color="#c0392b", label="Euler")
    ax_ph.plot(q_rk4[:, 0], q_rk4[:, 1], lw=2.0, color="#1f4e79", label="RK4")
    ax_ph.set_xlabel("q")
    ax_ph.set_ylabel("v")
    ax_ph.set_title("same clocks on ẍ = −x")
    ax_ph.set_aspect("equal", adjustable="box")
    ax_ph.legend(frameon=False)
    ax_ph.grid(True, alpha=0.3)
    fig.suptitle("Same step, two clocks", y=1.02)
    fig.tight_layout()
    return fig


def animate_falling_mass(
    t: np.ndarray,
    z_euler: np.ndarray,
    z_rk4: np.ndarray,
    *,
    q_euler: np.ndarray | None = None,
    q_rk4: np.ndarray | None = None,
    path: Path | str | None = None,
    fps: int = 20,
) -> Path:
    """Gif: two falling masses + optional oscillator phase portrait."""
    dest = Path(path) if path else ensure_media() / "lab00.gif"
    zmin = float(min(z_euler.min(), z_rk4.min()) - 0.5)
    zmax = float(max(z_euler.max(), z_rk4.max()) + 0.5)
    n_panel = 3 if q_euler is not None and q_rk4 is not None else 2
    fig, axes = plt.subplots(1, n_panel, figsize=(4.2 * n_panel, 4.0))
    ax_w, ax_s = axes[0], axes[1]
    ax_w.set_xlim(-1.2, 1.2)
    ax_w.set_ylim(zmin, zmax)
    ax_w.set_aspect("equal", adjustable="box")
    ax_w.set_title("world")
    ax_w.set_xticks([])
    ax_w.set_ylabel("z [m]")
    e_dot = ax_w.plot([-0.35], [z_euler[0]], "o", color="#c0392b", ms=12, label="Euler")[0]
    r_dot = ax_w.plot([0.35], [z_rk4[0]], "o", color="#1f4e79", ms=12, label="RK4")[0]
    ax_w.legend(loc="upper right", frameon=False)

    ax_s.plot(t, z_euler, "--", color="#c0392b", lw=1.4, alpha=0.7)
    ax_s.plot(t, z_rk4, color="#1f4e79", lw=1.4, alpha=0.7)
    e_trace = ax_s.plot([t[0]], [z_euler[0]], "o", color="#c0392b", ms=6)[0]
    r_trace = ax_s.plot([t[0]], [z_rk4[0]], "o", color="#1f4e79", ms=6)[0]
    ax_s.set_xlim(t[0], t[-1])
    ax_s.set_ylim(zmin, zmax)
    ax_s.set_xlabel("t [s]")
    ax_s.set_ylabel("z [m]")
    ax_s.set_title("height vs time")
    ax_s.grid(True, alpha=0.3)

    artists = [e_dot, r_dot, e_trace, r_trace]
    if n_panel == 3:
        ax_ph = axes[2]
        ax_ph.plot(q_euler[:, 0], q_euler[:, 1], "--", color="#c0392b", lw=1.2, alpha=0.55)
        ax_ph.plot(q_rk4[:, 0], q_rk4[:, 1], color="#1f4e79", lw=1.2, alpha=0.55)
        e_ph = ax_ph.plot([q_euler[0, 0]], [q_euler[0, 1]], "o", color="#c0392b", ms=7)[0]
        r_ph = ax_ph.plot([q_rk4[0, 0]], [q_rk4[0, 1]], "o", color="#1f4e79", ms=7)[0]
        pad = 0.15 * max(np.abs(q_euler).max(), np.abs(q_rk4).max(), 1.0)
        lim = max(np.abs(q_euler).max(), np.abs(q_rk4).max()) + pad
        ax_ph.set_xlim(-lim, lim)
        ax_ph.set_ylim(-lim, lim)
        ax_ph.set_aspect("equal", adjustable="box")
        ax_ph.set_xlabel("q")
        ax_ph.set_ylabel("v")
        ax_ph.set_title("ẍ = −x  (Euler grows)")
        ax_ph.grid(True, alpha=0.3)
        artists.extend([e_ph, r_ph])
    fig.tight_layout()

    def update(i: int):
        e_dot.set_data([-0.35], [z_euler[i]])
        r_dot.set_data([0.35], [z_rk4[i]])
        e_trace.set_data([t[i]], [z_euler[i]])
        r_trace.set_data([t[i]], [z_rk4[i]])
        if n_panel == 3:
            e_ph.set_data([q_euler[i, 0]], [q_euler[i, 1]])
            r_ph.set_data([q_rk4[i, 0]], [q_rk4[i, 1]])
        return tuple(artists)

    idx = np.linspace(0, len(t) - 1, min(len(t), fps * 4)).astype(int)
    anim = FuncAnimation(fig, update, frames=idx, blit=True, interval=1000 / fps)
    save_gif(anim, dest, fps=fps)
    thumb = dest.with_name(dest.stem + "_thumb.png")
    update(int(idx[-1]))
    save_thumb(fig, thumb)
    plt.close(fig)
    return dest


def _quad_artists(ax, plant: PlanarQuadrotor, color: str = "#1f4e79"):
    (body,) = ax.plot([], [], "-", color=color, lw=4, solid_capstyle="round")
    r_rotor = Circle((0, 0), 0.06, color=color, zorder=3)
    l_rotor = Circle((0, 0), 0.06, color=color, zorder=3)
    ax.add_patch(r_rotor)
    ax.add_patch(l_rotor)
    (thrust_r,) = ax.plot([], [], color="#e67e22", lw=2)
    (thrust_l,) = ax.plot([], [], color="#e67e22", lw=2)
    return body, r_rotor, l_rotor, thrust_r, thrust_l


def _place_quad(artists, plant: PlanarQuadrotor, x: np.ndarray, u: np.ndarray | None) -> None:
    body, r_rotor, l_rotor, thrust_r, thrust_l = artists
    y, z, th = float(x[IY]), float(x[IZ]), float(x[ITH])
    L = plant.L
    cy, sz = np.cos(th), np.sin(th)
    # Body axis (along +y_body): endpoints of the arm.
    ry, rz = y + L * cy, z + L * sz
    ly, lz = y - L * cy, z - L * sz
    body.set_data([ly, ry], [lz, rz])
    r_rotor.center = (ry, rz)
    l_rotor.center = (ly, lz)
    # Thrust ticks along body +z = (-sin θ, cos θ).
    bz_y, bz_z = -sz, cy
    scale = 0.18
    if u is None:
        u1 = u2 = 0.0
    else:
        u1, u2 = float(u[0]), float(u[1])
    hover = plant.m * plant.g / 2.0
    tr, tl = scale * (u1 / hover), scale * (u2 / hover)
    thrust_r.set_data([ry, ry + tr * bz_y], [rz, rz + tr * bz_z])
    thrust_l.set_data([ly, ly + tl * bz_y], [lz, lz + tl * bz_z])


def animate_planar_quad(
    t: np.ndarray,
    xs: np.ndarray,
    plant: PlanarQuadrotor,
    us: np.ndarray | None = None,
    *,
    path: Path | str | None = None,
    title: str = "planar quadrotor",
    fps: int = 20,
    trail: bool = True,
) -> Path:
    dest = Path(path) if path else ensure_media() / "lab01.gif"
    pad = 1.2
    ymin, ymax = float(xs[:, IY].min() - pad), float(xs[:, IY].max() + pad)
    zmin, zmax = float(max(0.0, xs[:, IZ].min() - pad)), float(xs[:, IZ].max() + pad)
    # Keep a usable window even if the vehicle barely moves.
    if ymax - ymin < 3:
        mid = 0.5 * (ymin + ymax)
        ymin, ymax = mid - 1.5, mid + 1.5
    if zmax - zmin < 3:
        mid = 0.5 * (zmin + zmax)
        zmin, zmax = max(0.0, mid - 1.5), mid + 1.5

    fig, ax = plt.subplots(figsize=(6.2, 5.4))
    ax.set_xlim(ymin, ymax)
    ax.set_ylim(zmin, zmax)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("y [m]")
    ax.set_ylabel("z [m]")
    ax.set_title(title)
    ax.axhline(0.0, color="#95a5a6", lw=1.2)
    ax.grid(True, alpha=0.25)
    artists = _quad_artists(ax, plant)
    (trail_line,) = ax.plot([], [], color="#1f4e79", alpha=0.35, lw=1.2)
    time_txt = ax.text(0.02, 0.98, "", transform=ax.transAxes, va="top")

    def update(i: int):
        ui = None if us is None else us[min(i, len(us) - 1)]
        _place_quad(artists, plant, xs[i], ui)
        if trail:
            trail_line.set_data(xs[: i + 1, IY], xs[: i + 1, IZ])
        time_txt.set_text(f"t = {t[i]:.2f} s")
        return (*artists, trail_line, time_txt)

    idx = np.linspace(0, len(t) - 1, min(len(t), fps * 5)).astype(int)
    anim = FuncAnimation(fig, update, frames=idx, blit=True, interval=1000 / fps)
    save_gif(anim, dest, fps=fps)
    update(idx[-1])
    save_thumb(fig, dest.with_name(dest.stem + "_thumb.png"))
    plt.close(fig)
    return dest
