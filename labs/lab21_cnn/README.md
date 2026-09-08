# Lab 21 — Weight Sharing Earns Its Keep

⏱ 45 min · ⇐ Lab 20 · Phase 4

## Why now?

Lab 20's polynomial wastes capacity on a 1-D toy. Images waste far more —
unless the weights *repeat*. That's convolution.

## What's the idea?

A 24×24 synthetic gate (a bright vertical bar). A 4-filter 3×3 conv plus a
linear readout vs. a flatten-MLP with about the same number of scalars.

```
conv  →  ReLU  →  mean over filters and rows  →  argmax over width  →  column
```

The CNN should win. The first-layer filters should look like edges. NumPy
is the default; ``BACKEND=torch`` is optional and not required for the check.

## What will you see?

A 2×2 grid of learned 3×3 filters. `media/lab21.gif`.

![Lab 21 thumbnail](../../media/lab21_thumb.png)

## Cold Start

- ``gate_dataset()`` returns images and the gate column.
- Valid conv shrinks the map by ``kh−1``. Mean-pool is ``.mean((2,3))``.
- Equal parameter count is part of the check — don't sneak a huge MLP.

## STOP HERE — good stopping point

``conv2d`` green is the lesson. The accuracy fight is the payoff.

## Run

```bash
python labs/lab21_cnn/check.py
BACKEND=torch python labs/lab21_cnn/check.py   # optional
python labs/lab21_cnn/demo.py
```
