"""Continuous 2-D obstacle fields for RRT (Lab 07)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Circle:
    center: tuple[float, float]
    radius: float

    def contains(self, p: np.ndarray, clearance: float = 0.0) -> bool:
        d = np.linalg.norm(np.asarray(p, dtype=float) - np.asarray(self.center))
        return bool(d <= self.radius + clearance)


class ObstacleField:
    def __init__(
        self,
        circles: list[Circle],
        *,
        x_min: float = 0.0,
        x_max: float = 6.0,
        y_min: float = 0.0,
        y_max: float = 4.0,
    ) -> None:
        self.circles = circles
        self.bounds = (x_min, x_max, y_min, y_max)

    def in_bounds(self, p: np.ndarray) -> bool:
        x, y = float(p[0]), float(p[1])
        xmin, xmax, ymin, ymax = self.bounds
        return xmin <= x <= xmax and ymin <= y <= ymax

    def collide_point(self, p: np.ndarray, clearance: float = 0.05) -> bool:
        if not self.in_bounds(p):
            return True
        return any(c.contains(p, clearance) for c in self.circles)

    def collide_segment(self, a: np.ndarray, b: np.ndarray, n: int = 12) -> bool:
        a = np.asarray(a, dtype=float)
        b = np.asarray(b, dtype=float)
        for s in np.linspace(0.0, 1.0, n):
            if self.collide_point(a + s * (b - a)):
                return True
        return False

    def sample_free(self, rng: np.random.Generator) -> np.ndarray:
        xmin, xmax, ymin, ymax = self.bounds
        for _ in range(200):
            p = np.array([rng.uniform(xmin, xmax), rng.uniform(ymin, ymax)])
            if not self.collide_point(p):
                return p
        raise RuntimeError("failed to sample a free point")


def forest_lab07() -> tuple[ObstacleField, np.ndarray, np.ndarray]:
    field = ObstacleField(
        [
            Circle((1.6, 1.2), 0.55),
            Circle((2.8, 2.6), 0.65),
            Circle((4.2, 1.3), 0.50),
            Circle((3.3, 0.7), 0.35),
        ],
        x_min=0.0,
        x_max=6.0,
        y_min=0.0,
        y_max=4.0,
    )
    start = np.array([0.4, 0.4])
    goal = np.array([5.5, 3.5])
    return field, start, goal
