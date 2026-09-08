"""SEE IT — two clocks, one falling mass. Writes media/lab00.gif (<10 s)."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from flightlab.resolve import get
from flightlab.viz import MEDIA, animate_falling_mass, ensure_media, falling_mass_figure, save_thumb

DT = 0.2
T_END = 6.0
Z0 = np.array([12.0, 0.0])
Q0 = np.array([1.0, 0.0])


def _simulate(step_fn, f, x0, dt, t_end):
    n = int(round(t_end / dt))
    x0 = np.asarray(x0, dtype=float).reshape(-1)
    xs = np.zeros((n + 1, x0.size))
    x = x0.copy()
    xs[0] = x
    for i in range(n):
        x = np.asarray(step_fn(f, x, None, dt), dtype=float).reshape(-1)
        xs[i + 1] = x
    t = np.linspace(0.0, n * dt, n + 1)
    return t, xs


def _ho_f(x, u=None):
    return np.array([x[1], -x[0]], dtype=float)


def main() -> Path:
    impl = get("lab00")
    t, xs_e = _simulate(impl.euler, impl.point_mass_f, Z0, DT, T_END)
    _, xs_r = _simulate(impl.rk4, impl.point_mass_f, Z0, DT, T_END)
    _, qe = _simulate(impl.euler, _ho_f, Q0, DT, T_END)
    _, qr = _simulate(impl.rk4, _ho_f, Q0, DT, T_END)
    ensure_media()
    gif = animate_falling_mass(
        t,
        xs_e[:, 0],
        xs_r[:, 0],
        q_euler=qe,
        q_rk4=qr,
        path=MEDIA / "lab00.gif",
    )
    fig = falling_mass_figure(t, xs_e[:, 0], xs_r[:, 0], q_euler=qe, q_rk4=qr)
    save_thumb(fig, MEDIA / "lab00_thumb.png")
    print(f"wrote {gif}")
    print(f"wrote {MEDIA / 'lab00_thumb.png'}")
    return gif


if __name__ == "__main__":
    main()
