"""SEE IT — before / after the loop closure. media/lab15_thumb.png."""

from __future__ import annotations

from pathlib import Path

from flightlab.resolve import get
from flightlab.viz import MEDIA, ensure_media, slam_before_after
from flightlab.worlds import loop_dataset_lab15


def main() -> Path:
    impl = get("lab15")
    gt, odom, loop, _ = loop_dataset_lab15(n_side=4, drift=0.18, seed=0)
    before = impl.compose_odometry(len(gt), odom)
    after = impl.optimize(before, list(odom) + [loop], n_iter=8)
    a0, a1 = impl.ate(before, gt), impl.ate(after, gt)
    ensure_media()
    dest = slam_before_after(gt, before, after, path=MEDIA / "lab15_thumb.png")
    print(f"wrote {dest}  ATE {a0:.3f} → {a1:.3f}  ({100*(1-a1/a0):.0f}% drop)")
    return dest


if __name__ == "__main__":
    main()
