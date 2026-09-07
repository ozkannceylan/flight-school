"""SEE IT — landmarks in the camera. media/lab16_thumb.png."""

from __future__ import annotations

from pathlib import Path

from flightlab.render import camera_from_planar, default_K, landmarks_lab16, pose_lab16, render_ground
from flightlab.resolve import get
from flightlab.viz import MEDIA, camera_world_figure, ensure_media


def main() -> Path:
    impl = get("lab16")
    K = default_K()
    py, pz, th = pose_lab16()
    R, C = camera_from_planar(py, pz, th)
    X = landmarks_lab16(5)
    uv = impl.project(K, R, C, X)
    Kh = impl.calibrate_K(X, uv, R, C)
    uv_re = impl.project(Kh, R, C, X)
    img = render_ground(py, pz, th)
    ensure_media()
    dest = camera_world_figure(img, uv, uv_re, path=MEDIA / "lab16_thumb.png")
    print(f"wrote {dest}  reproj={impl.reprojection_error(Kh, R, C, X, uv):.4f}px")
    return dest


if __name__ == "__main__":
    main()
