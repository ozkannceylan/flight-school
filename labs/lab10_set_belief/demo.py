"""SEE IT — the possibility cloud breathing. media/lab10.gif."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from flightlab.resolve import get
from flightlab.viz import MEDIA, animate_belief_set, ensure_media
from flightlab.worlds import rooms_lab10, start_lab10, successors, wall_adjacent, wall_adjacent_mask


def main() -> Path:
    impl = get("lab10")
    grid = rooms_lab10()
    adj = wall_adjacent_mask(grid)
    actions = ((0, 1), (0, 1), (0, 1), (-1, 0), (0, -1), (0, -1), (1, 0), (1, 0))
    rng = np.random.default_rng(1)
    truth = start_lab10()
    bel = np.zeros((grid.rows, grid.cols), dtype=bool)
    bel[truth] = True
    beliefs = [bel.copy()]
    truths = [truth]
    for a in actions * 2:
        opts = list(successors(grid, truth, a))
        truth = opts[int(rng.integers(0, len(opts)))]
        z = wall_adjacent(grid, truth)
        consistent = adj if z else (~adj & ~grid.occ)
        bel = impl.step(bel, grid, a, consistent)
        beliefs.append(bel.copy())
        truths.append(truth)
    ensure_media()
    gif = animate_belief_set(grid, beliefs, truths, path=MEDIA / "lab10.gif")
    print(f"wrote {gif}  final set {int(bel.sum())} cells")
    return gif


if __name__ == "__main__":
    main()
