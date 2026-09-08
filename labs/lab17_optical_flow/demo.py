"""SEE IT — LK quiver vs analytic. media/lab17_thumb.png."""

from __future__ import annotations

from pathlib import Path

from flightlab.render import (
    FX,
    IMG_H,
    IMG_W,
    analytic_flow,
    wavy,
    default_K,
    render_ground,
    sample_track_points,
)
from flightlab.resolve import get
from flightlab.viz import MEDIA, ensure_media, flow_quiver_figure


def main() -> Path:
    impl = get("lab17")
    K = default_K()
    py, pz, th, dpy = 0.0, 1.5, 0.0, 0.015
    I1 = render_ground(py, pz, th, texture=wavy)
    I2 = render_ground(py + dpy, pz, th, texture=wavy)
    pts = sample_track_points(IMG_W, IMG_H, n=36, margin=14)
    fl = impl.lucas_kanade(I1, I2, pts, win=6)
    gt = analytic_flow(K, py, pz, th, dpy, 0.0, 0.0, pts)
    vy = impl.flow_to_vy(fl, FX, pz)
    ensure_media()
    dest = flow_quiver_figure(I1, pts, fl, gt, path=MEDIA / "lab17_thumb.png")
    print(f"wrote {dest}  vŷ={vy:.3f}  true Δy={dpy:.3f}")
    return dest


if __name__ == "__main__":
    main()
