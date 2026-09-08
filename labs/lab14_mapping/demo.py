"""SEE IT — the map fogging in. media/lab14.gif."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from flightlab.resolve import get
from flightlab.sensors import RangeSensor
from flightlab.viz import MEDIA, animate_mapping, ensure_media
from flightlab.worlds import mapping_lab14, mapping_poses_lab14


def main() -> Path:
    impl = get("lab14")
    grid = mapping_lab14()
    poses = mapping_poses_lab14()
    sensor = RangeSensor(n_beams=7, fov=np.pi, max_range=6.5, sigma=0.04, step=0.2)
    rng = np.random.default_rng(0)
    l_map = np.zeros(grid.occ.shape, dtype=float)
    seq = [l_map.copy()]
    for pose in poses:
        z = sensor.measure(pose, grid, rng)
        l_map = impl.integrate_scan(l_map, pose, z, sensor)
        seq.append(l_map.copy())
    ensure_media()
    gif = animate_mapping(grid, seq, poses, path=MEDIA / "lab14.gif")
    print(f"wrote {gif}")
    return gif


if __name__ == "__main__":
    main()
