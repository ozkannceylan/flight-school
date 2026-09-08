"""SEE IT — BFS blooms, DFS snakes. media/lab05.gif."""

from __future__ import annotations

from pathlib import Path

from flightlab.resolve import get
from flightlab.viz import MEDIA, animate_search, ensure_media
from flightlab.worlds import maze_lab05


def main() -> Path:
    impl = get("lab05")
    grid, start, goal = maze_lab05()
    bpath, bexp = impl.bfs(grid, start, goal)
    dpath, dexp = impl.dfs(grid, start, goal)
    ensure_media()
    gif = animate_search(grid, bexp, dexp, bpath, dpath, start, goal, path=MEDIA / "lab05.gif")
    print(f"wrote {gif}")
    print(f"BFS {len(bpath)-1} edges, {len(bexp)} expanded; DFS {len(dpath)-1} edges, {len(dexp)} expanded")
    return gif


if __name__ == "__main__":
    main()
