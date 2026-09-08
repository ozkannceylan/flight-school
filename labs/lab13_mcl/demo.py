"""SEE IT — the cloud collapses, scatters, re-collapses. media/lab13.gif."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from flightlab.geometry import oplus
from flightlab.resolve import get
from flightlab.sensors import RangeSensor
from flightlab.viz import MEDIA, animate_mcl, ensure_media
from flightlab.worlds import office_lab13, start_pose_lab13


def main() -> Path:
    impl = get("lab13")
    grid = office_lab13()
    sensor = RangeSensor(n_beams=5, fov=np.pi, max_range=7.0, sigma=0.12, step=0.25)
    rng = np.random.default_rng(9)
    pose = start_pose_lab13()
    parts = impl.uniform_particles(180, grid, rng)
    poses = [pose.copy()]
    clouds = [parts.copy()]
    cmds = [(0.4, 0.0)] * 7 + [(0.0, 1.2)] + [(0.35, 0.0)] * 5 + [(0.0, -1.0)] + [(0.3, 0.0)] * 6
    for t, u in enumerate(cmds):
        pose = oplus(pose, np.array([u[0], 0.0, u[1]]))
        if t == 10:
            pose = np.array([10.5, 2.5, np.pi])
        z = sensor.measure(pose, grid, rng)
        parts = impl.motion_update(parts, np.asarray(u), rng)
        w = impl.weight(parts, z, grid, sensor)
        parts = impl.resample(parts, w, rng, grid, inject=0.16)
        poses.append(pose.copy())
        clouds.append(parts.copy())
    ensure_media()
    gif = animate_mcl(grid, poses, clouds, path=MEDIA / "lab13.gif")
    print(f"wrote {gif}")
    return gif


if __name__ == "__main__":
    main()
