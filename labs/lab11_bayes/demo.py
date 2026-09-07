"""SEE IT — three stacked histograms. media/lab11.gif."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from flightlab.resolve import get
from flightlab.viz import MEDIA, animate_bayes_stack, ensure_media
from flightlab.worlds import corridor_lab11


def main() -> Path:
    impl = get("lab11")
    doors, x0 = corridor_lab11()
    n = doors.size
    bel = np.full(n, 1.0 / n)
    x = x0
    priors, likes, posts, truths = [], [], [], []
    rng = np.random.default_rng(2)
    for _ in range(8):
        x = min(x + 1, n - 1)
        z = bool(doors[x]) if rng.random() < 0.92 else (not bool(doors[x]))
        pri = impl.predict(bel)
        like = impl.likelihood(doors, z)
        post = impl.update(pri, like)
        priors.append(pri)
        likes.append(like / max(like.max(), 1e-12))
        posts.append(post)
        truths.append(x)
        bel = post
    ensure_media()
    gif = animate_bayes_stack(priors, likes, posts, truths, doors, path=MEDIA / "lab11.gif")
    print(f"wrote {gif}  mode={int(np.argmax(bel))} truth={x}")
    return gif


if __name__ == "__main__":
    main()
