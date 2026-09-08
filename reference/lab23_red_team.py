"""Reference implementation for Lab 23 — Red-Team Your Own Stack."""

from __future__ import annotations

import numpy as np

from flightlab.resolve import get


def failure_analysis() -> str:
    return """
# Failure analysis — this repo

Four assumptions we shipped, then watched fail. The files are the evidence.

## 1. A wrong sensor model is still a probability
`labs/lab11_bayes/check.py` criterion `confident_wrong` swaps `p_hit` and
`p_false` through `inverted_likelihood`. After eight door observations the
posterior is peaked and *wrong*. Bayes did not save us; it laundered the
modelling error into a number we would have trusted. Liability starts here:
the filter was calibrated, the likelihood was inverted, the mode looked
decisive.

## 2. Brightness change is velocity
`labs/lab17_optical_flow/check.py` criterion `textureless_fails` runs
Lucas–Kanade on `blank`. The analytic ground-truth flow is a few pixels;
LK returns noise because G is singular. A hover PD that treats that noise
as `vy` is a crash. I now refuse to publish a flow vector when
`texture_energy` is below the cutoff — `trusted_flow` returns `None`.

## 3. The training crop is the world
`labs/lab21_cnn/check.py` holds out right-side gates (`yte >= 10`) so a
parameter-matched MLP cannot memorise column indices it never saw. That
split is the distribution shift. A gate detector that only ever trained on
the left half of the image is not a gate detector. I refuse to quote CNN
accuracy without naming the held-out side.

## 4. A cheap reward is a hover
`labs/lab22_rl/README.md` is explicit: Lab 04's LQR is the zero-sample
line, and `dt` has to be 0.02 or that baseline bang-bangs. CEM on a 2 s
horizon with `K ≈ 0` can look cheap because the plant barely moves. That
is a reward hack, not a controller. I refuse to rank a policy against LQR
on a cost the LQR was not designed to look good on, at a step the LQR
cannot take.

## What I now refuse to assume
Texture ⇒ flow. A normalised belief ⇒ a true pose. Train accuracy ⇒
deployment. A high episode return ⇒ a hover. The durable form of that
refusal is `tests/test_lab23_assumption.py`.
""".strip()


def texture_energy(I: np.ndarray) -> float:
    I = np.asarray(I, dtype=float)
    Iy, Ix = np.gradient(I)
    return float(np.mean(np.hypot(Ix, Iy)))


def trusted_flow(I1: np.ndarray, I2: np.ndarray, pts: np.ndarray, *, min_energy: float = 0.04):
    if texture_energy(I1) < min_energy:
        return None
    lab17 = get("lab17")
    return lab17.lucas_kanade(I1, I2, pts)
