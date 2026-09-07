# Lab 20 — When Fitting Better Means Knowing Less

⏱ 40 min · ⇐ Lab 19 · Phase 4

## Why now?

Lab 19 found the cliff. Capacity plus a tiny dataset is another way to
lose: the train loss goes to zero and the val loss does not.

## What's the idea?

Eight noisy samples of ``sin(2x)``. A degree-8 polynomial can interpolate
them. That's memorization.

```
w = (ΦᵀΦ + λ I)⁻¹ Φᵀ y     (leave the intercept un-penalised)
gap = (val − train) / (val + train)
```

Turn on ``λ`` and the gap drops under 0.18. Same model class, less
freedom.

## What will you see?

The textbook diverging-curves plot — from your own broken fit. `media/lab20.gif`.

![Lab 20 thumbnail](../../media/lab20_thumb.png)

## Cold Start

- ``sine_dataset()`` and ``poly_features`` are provided.
- Do not regularise ``w[0]``. Set ``I[0,0] = 0``.
- Closed form, not SGD. The demo uses GD only so the curve has a time axis.

## STOP HERE — good stopping point

The unregularised gap is the lesson. L2 is the one-line fix.

## Run

```bash
python labs/lab20_overfit/check.py
python labs/lab20_overfit/demo.py
```
