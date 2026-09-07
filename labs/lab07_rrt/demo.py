"""SEE IT — the tree growing. media/lab07.gif."""

from __future__ import annotations

from pathlib import Path

from flightlab.resolve import get
from flightlab.viz import MEDIA, animate_rrt, ensure_media
from flightlab.worlds import forest_lab07


def main() -> Path:
    impl = get("lab07")
    field, start, goal = forest_lab07()
    path, nodes, parents = impl.rrt(field, start, goal, seed=3, n_iter=400)
    path = impl.shortcut(path, field)
    # Fake growth snapshots by prefixes of the node list.
    snaps = []
    for k in range(2, len(nodes) + 1, max(1, len(nodes) // 24)):
        snaps.append((nodes[:k], parents[:k]))
    if snaps[-1][0].shape[0] != len(nodes):
        snaps.append((nodes, parents))
    ensure_media()
    gif = animate_rrt(
        field.bounds,
        [(c.center, c.radius) for c in field.circles],
        snaps,
        path,
        start,
        goal,
        dest=MEDIA / "lab07.gif",
    )
    print(f"wrote {gif}  path nodes={len(path)}")
    return gif


if __name__ == "__main__":
    main()
