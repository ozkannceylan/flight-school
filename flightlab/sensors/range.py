"""2-D beam range sensor on an occupancy grid.

World frame matches the array: ``x`` is column, ``y`` is row, ``θ = 0`` faces
+x (right). Out-of-bounds counts as a hit. Cell size is 1 unless given.
"""

from __future__ import annotations

import numpy as np

from flightlab.sensors.noise import as_rng
from flightlab.worlds.grid import OccupancyGrid


def raycast(
    grid: OccupancyGrid,
    pose: np.ndarray,
    angle: float,
    max_range: float,
    *,
    step: float = 0.2,
    cell_size: float = 1.0,
) -> float:
    """Walk a ray until a wall or ``max_range``. ``pose`` is ``(x, y, theta)``."""
    x, y, th = (float(pose[0]), float(pose[1]), float(pose[2]))
    a = th + float(angle)
    ca, sa = np.cos(a), np.sin(a)
    r = 0.0
    rows, cols = grid.rows, grid.cols
    while r < max_range:
        r += step
        xi = x + r * ca
        yi = y + r * sa
        c = int(np.floor(xi / cell_size))
        rr = int(np.floor(yi / cell_size))
        if rr < 0 or rr >= rows or c < 0 or c >= cols or grid.occ[rr, c]:
            return min(r, max_range)
    return max_range


class RangeSensor:
    """``n_beams`` rays, equally spaced over ``fov``, centred on the heading."""

    def __init__(
        self,
        n_beams: int = 5,
        fov: float = np.pi,
        max_range: float = 8.0,
        sigma: float = 0.12,
        step: float = 0.2,
    ) -> None:
        self.n_beams = int(n_beams)
        self.fov = float(fov)
        self.max_range = float(max_range)
        self.sigma = float(sigma)
        self.step = float(step)
        if self.n_beams == 1:
            self.angles = np.array([0.0])
        else:
            self.angles = np.linspace(-0.5 * self.fov, 0.5 * self.fov, self.n_beams)

    def expected(self, pose: np.ndarray, grid: OccupancyGrid) -> np.ndarray:
        pose = np.asarray(pose, dtype=float).reshape(3)
        return np.array(
            [raycast(grid, pose, a, self.max_range, step=self.step) for a in self.angles],
            dtype=float,
        )

    def measure(
        self,
        pose: np.ndarray,
        grid: OccupancyGrid,
        rng: int | np.random.Generator | None = 0,
    ) -> np.ndarray:
        z = self.expected(pose, grid)
        noise = as_rng(rng).normal(0.0, self.sigma, size=z.shape)
        return np.clip(z + noise, 0.0, self.max_range)
