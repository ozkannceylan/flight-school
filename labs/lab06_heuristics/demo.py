"""SEE IT — three expansion heatmaps. media/lab06.gif."""

from __future__ import annotations

from pathlib import Path

from flightlab.resolve import get
from flightlab.viz import MEDIA, ensure_media, expansion_heatmaps
from flightlab.worlds import manhattan, terrain_lab06


def main() -> Path:
    impl = get("lab06")
    cmap, start, goal = terrain_lab06()
    pd, ed, cd = impl.dijkstra(cmap, start, goal)
    pa, ea, ca = impl.astar(cmap, start, goal, manhattan)
    pw, ew, cw = impl.astar(cmap, start, goal, impl.inflate(manhattan, 2.0))
    ensure_media()
    gif = expansion_heatmaps(
        cmap.cost.shape,
        [
            (f"Dijkstra  cost={cd:.1f}  n={len(ed)}", ed, pd),
            (f"A*  cost={ca:.1f}  n={len(ea)}", ea, pa),
            (f"A*  h×2  cost={cw:.1f}  n={len(ew)}", ew, pw),
        ],
        path=MEDIA / "lab06_thumb.png",
    )
    print(f"wrote {gif}")
    return gif


if __name__ == "__main__":
    main()
