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

from flightlab.dynamics.planar_quad import ITH, IY, IZ, PlanarQuadrotor
from flightlab.dynamics.quad3d import IPHI, ITH as ITH3, IX, IY as IY3, IZ as IZ3, rotation_zyx

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


def _quad3d_arms(x: np.ndarray, arm: float = 0.25) -> tuple[np.ndarray, np.ndarray]:
    R = rotation_zyx(float(x[IPHI]), float(x[ITH3]), float(x[5]))
    p = np.array([x[IX], x[IY3], x[IZ3]], dtype=float)
    right = p + R @ np.array([0.0, arm, 0.0])
    left = p + R @ np.array([0.0, -arm, 0.0])
    front = p + R @ np.array([arm, 0.0, 0.0])
    back = p + R @ np.array([-arm, 0.0, 0.0])
    return np.vstack([left, right]), np.vstack([back, front])


def animate_quad3d(
    t: np.ndarray,
    xs: np.ndarray,
    thetas_sweep: np.ndarray,
    rate_norm: np.ndarray,
    *,
    path: Path | str | None = None,
    title: str = "altitude hold  +  gimbal lock",
    fps: int = 16,
) -> Path:
    """Two-panel gif: 3D vehicle on the left, Euler-rate blow-up on the right."""
    dest = Path(path) if path else ensure_media() / "lab02.gif"
    fig = plt.figure(figsize=(9.2, 4.4))
    ax3 = fig.add_subplot(1, 2, 1, projection="3d")
    axr = fig.add_subplot(1, 2, 2)
    ax3.set_xlabel("x")
    ax3.set_ylabel("y")
    ax3.set_zlabel("z")
    ax3.set_title("first closed loop")
    span = 1.6
    ax3.set_xlim(-span, span)
    ax3.set_ylim(-span, span)
    z0 = float(xs[:, IZ3].min()) - 0.4
    z1 = float(xs[:, IZ3].max()) + 0.6
    ax3.set_zlim(max(0.0, z0), z1)
    (arm_y,) = ax3.plot([], [], [], color="#1f4e79", lw=3)
    (arm_x,) = ax3.plot([], [], [], color="#1f4e79", lw=3)
    (trail,) = ax3.plot([], [], [], color="#1f4e79", alpha=0.35, lw=1.0)

    axr.plot(np.degrees(thetas_sweep), rate_norm, color="#c0392b", lw=2.0)
    (dot,) = axr.plot([np.degrees(thetas_sweep[0])], [rate_norm[0]], "o", color="#c0392b")
    axr.axvline(90.0, color="#7f8c8d", ls="--", lw=1.0)
    axr.set_xlabel("pitch θ [deg]")
    axr.set_ylabel("|Euler rates|  for ω=[0,0,1]")
    axr.set_title("representation blows up at 90°")
    axr.grid(True, alpha=0.3)
    fig.suptitle(title)
    fig.tight_layout()

    n = min(len(t), len(thetas_sweep))
    idx = np.linspace(0, n - 1, min(n, fps * 4)).astype(int)

    def update(i: int):
        yy, xx = _quad3d_arms(xs[min(i, len(xs) - 1)])
        arm_y.set_data(yy[:, 0], yy[:, 1])
        arm_y.set_3d_properties(yy[:, 2])
        arm_x.set_data(xx[:, 0], xx[:, 1])
        arm_x.set_3d_properties(xx[:, 2])
        trail.set_data(xs[: i + 1, IX], xs[: i + 1, IY3])
        trail.set_3d_properties(xs[: i + 1, IZ3])
        j = min(i, len(thetas_sweep) - 1)
        dot.set_data([np.degrees(thetas_sweep[j])], [rate_norm[j]])
        return arm_y, arm_x, trail, dot

    anim = FuncAnimation(fig, update, frames=idx, blit=False, interval=1000 / fps)
    save_gif(anim, dest, fps=fps)
    update(int(idx[-1]))
    save_thumb(fig, dest.with_name(dest.stem + "_thumb.png"))
    plt.close(fig)
    return dest


def gain_sweep_figure(
    results: list[tuple[str, np.ndarray, np.ndarray]],
    *,
    path: Path | str | None = None,
) -> Path:
    """3×3 (or n) side-by-side y(t) flights from a gain sweep."""
    dest = Path(path) if path else ensure_media() / "lab03_thumb.png"
    n = len(results)
    cols = 3
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(9.0, 2.8 * rows), sharex=True, sharey=True)
    axes = np.atleast_2d(axes)
    for k, (label, t, y) in enumerate(results):
        ax = axes[k // cols, k % cols]
        ax.plot(t, y, color="#1f4e79", lw=1.6)
        ax.axhline(0.0, color="#95a5a6", lw=0.8)
        ax.set_title(label, fontsize=9)
        ax.grid(True, alpha=0.25)
        if k // cols == rows - 1:
            ax.set_xlabel("t [s]")
        if k % cols == 0:
            ax.set_ylabel("y [m]")
    for k in range(n, rows * cols):
        axes[k // cols, k % cols].axis("off")
    fig.suptitle("gain sweep — sluggish / tuned / unstable")
    fig.tight_layout()
    save_thumb(fig, dest)
    gif = dest.with_name("lab03.gif")
    # One-frame gif so `make lab03` still emits the contract artifact.
    anim = FuncAnimation(fig, lambda _i: [], frames=[0], blit=False)
    save_gif(anim, gif, fps=4)
    plt.close(fig)
    return gif


def lqr_vs_pd_figure(
    t: np.ndarray,
    xs_pd: np.ndarray,
    xs_lqr: np.ndarray,
    us_pd: np.ndarray,
    us_lqr: np.ndarray,
    *,
    path: Path | str | None = None,
) -> Path:
    dest_thumb = Path(path) if path else ensure_media() / "lab04_thumb.png"
    fig, (ax_y, ax_u) = plt.subplots(1, 2, figsize=(8.8, 3.8))
    (pd_y,) = ax_y.plot([], [], "--", color="#c0392b", lw=1.8, label="PD (Lab 03)")
    (lq_y,) = ax_y.plot([], [], color="#1f4e79", lw=2.0, label="LQR")
    ax_y.set_xlabel("t [s]")
    ax_y.set_ylabel("y [m]")
    ax_y.set_title("same disturbance")
    ax_y.set_xlim(t[0], t[-1])
    ypad = 0.1
    ymin = min(xs_pd[:, IY].min(), xs_lqr[:, IY].min()) - ypad
    ymax = max(xs_pd[:, IY].max(), xs_lqr[:, IY].max()) + ypad
    ax_y.set_ylim(ymin, ymax)
    ax_y.legend(frameon=False)
    ax_y.grid(True, alpha=0.3)

    T_pd = us_pd[:, 0] + us_pd[:, 1]
    T_lq = us_lqr[:, 0] + us_lqr[:, 1]
    (pd_u,) = ax_u.plot([], [], "--", color="#c0392b", lw=1.6, label="PD thrust")
    (lq_u,) = ax_u.plot([], [], color="#1f4e79", lw=1.8, label="LQR thrust")
    ax_u.set_xlabel("t [s]")
    ax_u.set_ylabel("T = u1+u2 [N]")
    ax_u.set_title("the math spends effort differently")
    ax_u.set_xlim(t[0], t[-1])
    tmin = min(T_pd.min(), T_lq.min()) - 0.2
    tmax = max(T_pd.max(), T_lq.max()) + 0.2
    ax_u.set_ylim(tmin, tmax)
    ax_u.legend(frameon=False)
    ax_u.grid(True, alpha=0.3)
    fig.suptitle("LQR vs your hand-tuned PD")
    fig.tight_layout()

    def update(i: int):
        pd_y.set_data(t[: i + 1], xs_pd[: i + 1, IY])
        lq_y.set_data(t[: i + 1], xs_lqr[: i + 1, IY])
        pd_u.set_data(t[: i + 1], T_pd[: i + 1])
        lq_u.set_data(t[: i + 1], T_lq[: i + 1])
        return pd_y, lq_y, pd_u, lq_u

    idx = np.linspace(0, len(t) - 1, min(len(t), 48)).astype(int)
    anim = FuncAnimation(fig, update, frames=idx, blit=True, interval=50)
    gif = dest_thumb.with_name("lab04.gif")
    save_gif(anim, gif, fps=16)
    update(int(idx[-1]))
    save_thumb(fig, dest_thumb)
    plt.close(fig)
    return gif
