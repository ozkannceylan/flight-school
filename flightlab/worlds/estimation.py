"""Maps, corridors, and a drifted loop for Labs 10–15."""

from __future__ import annotations

import numpy as np

from flightlab.geometry.se2 import ominus, oplus, wrap
from flightlab.worlds.grid import OccupancyGrid, occupancy_from_ascii

# 4-connected slips around an intended cell — Lab 10's bounded disturbance.
SLIPS: tuple[tuple[int, int], ...] = ((0, 0), (-1, 0), (1, 0), (0, -1), (0, 1))


def rooms_lab10() -> OccupancyGrid:
    """Two rooms and a hallway. Small enough that a set-belief check is <1 s."""
    return occupancy_from_ascii(
        [
            "###########",
            "#....#....#",
            "#....#....#",
            "#....#....#",
            "##.#####.##",
            "#.........#",
            "#.........#",
            "###########",
        ]
    )


def start_lab10() -> tuple[int, int]:
    return (5, 1)


def wall_adjacent(grid: OccupancyGrid, cell: tuple[int, int]) -> bool:
    """True if a 4-neighbour is a wall or off the map."""
    r, c = cell
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nxt = (r + dr, c + dc)
        if not grid.in_bounds(nxt) or grid.occ[nxt]:
            return True
    return False


def wall_adjacent_mask(grid: OccupancyGrid) -> np.ndarray:
    mask = np.zeros((grid.rows, grid.cols), dtype=bool)
    for r in range(grid.rows):
        for c in range(grid.cols):
            if grid.is_free((r, c)):
                mask[r, c] = wall_adjacent(grid, (r, c))
    return mask


def successors(grid: OccupancyGrid, cell: tuple[int, int], action: tuple[int, int]) -> set[tuple[int, int]]:
    """Intended cell plus a 4-neighbourhood slip; blocked cells bounce to stay."""
    ir, ic = cell[0] + action[0], cell[1] + action[1]
    out: set[tuple[int, int]] = set()
    for dr, dc in SLIPS:
        nxt = (ir + dr, ic + dc)
        if grid.is_free(nxt):
            out.add(nxt)
    if not out and grid.is_free(cell):
        out.add(cell)
    return out


def corridor_lab11() -> tuple[np.ndarray, int]:
    """1-D corridor: 1 = door. Start at the left wall. Length 20."""
    doors = np.array([0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], dtype=bool)
    return doors, 0


def office_lab13() -> OccupancyGrid:
    """Asymmetric office — unique range signatures for MCL."""
    return occupancy_from_ascii(
        [
            "##############",
            "#......#.....#",
            "#......#.....#",
            "#..##..#..#..#",
            "#......#..#..#",
            "####.###..#..#",
            "#............#",
            "#............#",
            "#..###.......#",
            "##############",
        ]
    )


def start_pose_lab13() -> np.ndarray:
    # Hallway, facing +x.
    return np.array([2.5, 6.5, 0.0], dtype=float)


def mapping_lab14() -> OccupancyGrid:
    """Compact two-room map the Lab 14 trajectory can cover in a few poses."""
    return occupancy_from_ascii(
        [
            "#########",
            "#.......#",
            "#..###..#",
            "#..#.#..#",
            "#.......#",
            "#########",
        ]
    )


def mapping_poses_lab14() -> np.ndarray:
    """Ground-truth poses that sweep the interior."""
    return np.array(
        [
            [1.5, 1.5, 0.0],
            [3.5, 1.5, 0.0],
            [6.5, 1.5, np.pi / 2],
            [6.5, 3.5, np.pi],
            [4.5, 4.5, np.pi],
            [1.5, 4.5, -np.pi / 2],
            [1.5, 2.5, 0.0],
            [3.5, 4.5, np.pi / 4],
        ],
        dtype=float,
    )


def loop_dataset_lab15(*, n_side: int = 4, drift: float = 0.18, seed: int = 0):
    """Square loop with noisy odometry plus one accurate loop-closure.

    Odometry is zero-mean around the true relative pose (so Gauss-Newton can
    recover GT) but noisy enough that the open-loop chain misses the origin.
    ``drift`` scales that noise. The loop-closure edge is exact.

    Returns ``gt (N,3)``, ``odom_edges`` list of ``(i, j, z, info)``,
    ``loop_edge``, and the open-loop compose.
    """
    n = 4 * n_side
    gt = np.zeros((n, 3), dtype=float)
    side = 4.0
    step = side / n_side
    headings = (0.0, np.pi / 2, np.pi, -np.pi / 2)
    k = 0
    x, y = 0.0, 0.0
    for h in headings:
        for _ in range(n_side):
            gt[k] = (x, y, h)
            x += step * np.cos(h)
            y += step * np.sin(h)
            k += 1
    gt[0] = np.array([0.0, 0.0, 0.0])
    rng = np.random.default_rng(seed)
    odom_edges = []
    # Weak odometry, strong loop — the loop is what actually saves you.
    info = np.diag([12.0, 12.0, 6.0])
    composed = gt[0].copy()
    open_loop = [composed.copy()]
    # Constant gyro bias: open-loop is a spiral. The loop snaps it shut.
    gyro_bias = 0.55 * drift
    for i in range(n - 1):
        z_true = ominus(gt[i], gt[i + 1])
        z = z_true.copy()
        z[0] += float(rng.normal(0.0, 0.03))
        z[1] += float(rng.normal(0.0, 0.03))
        z[2] = wrap(z[2] + gyro_bias + float(rng.normal(0.0, 0.01)))
        odom_edges.append((i, i + 1, z, info.copy()))
        composed = oplus(composed, z)
        open_loop.append(composed.copy())
    z_loop = ominus(gt[-1], gt[0])
    loop_info = np.diag([500.0, 500.0, 200.0])
    loop_edge = (n - 1, 0, z_loop, loop_info)
    return gt, odom_edges, loop_edge, np.asarray(open_loop)
