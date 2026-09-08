# Lab 10 — Where Could I Possibly Be?

⏱ 40 min · ⇐ Lab 05 · Phase 3

## Why now?

Planning gave you a path. Estimation asks the prior question: *which states
are still possible?* Do this with sets, before probabilities.

## What's the idea?

A belief is a boolean mask on the grid.

```
predict  →  grow: every live cell fans out by successors(grid, cell, action)
update   →  cut:  keep only cells consistent with the sensor
```

The motion model is *nondeterministic* — intended step plus a 4-neighbour
slip. The sensor is binary: wall-adjacent or not. If your predict is a
**superset** of what can actually happen, the true cell cannot leave the set.

## What will you see?

A blue possibility cloud breathing in and out, red dot = truth. `media/lab10.gif`.

![Lab 10 thumbnail](../../media/lab10_thumb.png)

## Cold Start

- ``successors(grid, cell, action)`` is provided. Action is ``(dr, dc)``.
- ``wall_adjacent_mask(grid)`` is the set of cells that would report "wall".
- No quadrotor in this lab. A cell is a state.

## STOP HERE — good stopping point

After TODO 1+2 pass, `step` is a one-liner. That's the lab.

## Run

```bash
python labs/lab10_set_belief/check.py
python labs/lab10_set_belief/demo.py
```
