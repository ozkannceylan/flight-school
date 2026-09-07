# Lab 19 — The Shape of the Descent

⏱ 40 min · ⇐ Lab 18 · Phase 4

## Why now?

Lab 18's gradient is a direction. *How* you step is a different lesson:
batch vs. momentum vs. Adam, and the learning-rate cliff.

## What's the idea?

A 2-D bowl ``(w0−1)² + 25(w1+0.5)²`` — skinny in one axis, so SGD zigzags
and momentum / Adam cut a cleaner path.

Sweep ``lr``. One of those values diverges. That boundary is the deliverable,
not a perfect optimiser.

## What will you see?

Three traces on one contour. `media/lab19.gif`.

![Lab 19 thumbnail](../../media/lab19_thumb.png)

## Cold Start

- ``loss`` and ``grad`` are provided. You write the three update rules.
- Adam bias-corrects with ``t`` starting at 1.
- Divergence here means ``loss > 80`` (or non-finite). Start at the origin.

## STOP HERE — good stopping point

SGD plus momentum is the lesson. Adam and the lr cliff are the plot.

## Run

```bash
python labs/lab19_sgd/check.py
python labs/lab19_sgd/demo.py
```
