# Lab 14 — Known Pose, Unknown Map

⏱ 40 min · ⇐ Lab 13 · Phase 3

## Why now?

Lab 13 knew the map and hunted the pose. Flip it: you know every pose
(ground-truth trajectory) and you paint the map.

## What's the idea?

Each range reading is a ray. Cells before the hit are free. The hit cell is
occupied. Accumulate in **log-odds** so updates are additions:

```
l ← clip(l + inverse_beam(z), ±8)
occupied  ⇔  l > 0
```

The naive cousin multiplies probabilities. After a few hundred misses it
underflows to ``0.0``. Log-odds just becomes a large negative number.

## What will you see?

Fog lifting off the map as the robot drives. `media/lab14.gif`.

![Lab 14 thumbnail](../../media/lab14_thumb.png)

## Cold Start

- ``mapping_lab14()`` / ``mapping_poses_lab14()`` are the world and the tour.
- ``raycast`` is how a beam *measures*. You write the *inverse* of that.
- ``integrate_scan`` is provided and calls your two functions.

## Run

```bash
python labs/lab14_mapping/check.py
python labs/lab14_mapping/demo.py
```
