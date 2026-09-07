"""SEE IT — trust vs refuse. media/lab23_thumb.png."""

from __future__ import annotations

from pathlib import Path

from flightlab.render import IMG_H, IMG_W, blank, render_ground, sample_track_points, wavy
from flightlab.resolve import get
from flightlab.viz import MEDIA, ensure_media, red_team_figure


def main() -> Path:
    impl = get("lab23")
    py, pz, th, dpy = 0.0, 1.5, 0.0, 0.015
    I_ok = render_ground(py, pz, th, texture=wavy)
    I_ok2 = render_ground(py + dpy, pz, th, texture=wavy)
    I_bad = render_ground(py, pz, th, texture=blank)
    I_bad2 = render_ground(py + dpy, pz, th, texture=blank)
    pts = sample_track_points(IMG_W, IMG_H, n=25, margin=16)
    fl = impl.trusted_flow(I_ok, I_ok2, pts)
    refused = impl.trusted_flow(I_bad, I_bad2, pts)
    ensure_media()
    dest = red_team_figure(I_ok, pts, fl, I_bad, refused is None, path=MEDIA / "lab23_thumb.png")
    print(f"wrote {dest}  wavy={fl is not None}  blank_refused={refused is None}")
    return dest


if __name__ == "__main__":
    main()
