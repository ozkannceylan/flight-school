# Lab 23 — Red-Team Your Own Stack

⏱ 45 min · ⇐ everything · Phase 5

## Why now?

Every earlier lab made an assumption and then, if you were paying
attention, showed you the failure. This lab is those failures taken
seriously — ethics, liability, the economy of what you refuse to assume.
Not a bolt-on lecture.

## What's the idea?

Two parts.

**(a) Written.** A one-page failure analysis of *this* repo. Cite the
files, not the vibes:

- `labs/lab11_bayes/check.py` — inverted likelihood, confident and wrong
- `labs/lab17_optical_flow/check.py` — textureless LK
- `labs/lab21_cnn/check.py` — held-out right-side gates
- `labs/lab22_rl/README.md` — CEM vs "LQR, zero samples"

**(b) Code.** `trusted_flow`: run Lab 17's LK only when the image has
texture. Otherwise return `None`. That `None` is the mitigation.

The check is red against the old assumption (LK on `blank` is garbage)
and green against the mitigation (we refuse).

## What will you see?

Left: flow you trust. Right: the word **REFUSED**. `media/lab23.gif`.

![Lab 23 thumbnail](../../media/lab23_thumb.png)

## Cold Start

- ``texture_energy`` is mean ``|∇I|``. ``np.gradient`` returns ``(Iy, Ix)``.
- ``get("lab17")`` for ``lucas_kanade``. Unfinished Lab 17 is a banner.
- Paste the four paths *verbatim*. The check is a substring test.

## STOP HERE — good stopping point

The analysis plus ``texture_energy`` is enough. ``trusted_flow`` is a
three-line `if`.

## Run

```bash
python labs/lab23_red_team/check.py
python labs/lab23_red_team/demo.py
```
