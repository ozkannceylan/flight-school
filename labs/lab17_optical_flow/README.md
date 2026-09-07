# Lab 17 — Motion From Brightness

⏱ 45 min · ⇐ Lab 16 · Phase 4

## Why now?

Lab 16 gave you pixels. Brightness constancy turns two frames into a
velocity — until the texture disappears.

## What's the idea?

Lucas–Kanade: in a small window, solve

```
[ Σ Ix²   Σ Ix Iy ] [ u ]   [ −Σ Ix It ]
[ Σ Ix Iy  Σ Iy²  ] [ v ] = [ −Σ Iy It ]
```

A downward camera converting mean ``u`` to ``vy`` is ``vy = −u z / fx``.
Feed that into a hover PD as the *only* lateral rate. It almost works.
A blank patch does not — that's the aperture problem, not a bug.

## What will you see?

Orange LK arrows on the wavy ground, blue analytic GT. `media/lab17.gif`.

![Lab 17 thumbnail](../../media/lab17_thumb.png)

## Cold Start

- ``render_ground`` / ``analytic_flow`` / ``sample_track_points`` are provided.
- ``np.gradient(I)`` returns ``(Iy, Ix)`` — row, then column.
- Lab 16's ``fx = 200``. Altitude is ``p_z``.

## STOP HERE — good stopping point

LK green first. The hover PD is a 10-line cousin of Lab 03.

## Run

```bash
python labs/lab17_optical_flow/check.py
python labs/lab17_optical_flow/demo.py
```
