# flight-school

24 hands-on simulation labs that teach robotics from PD control to SLAM to RL —
pure NumPy, one quadrotor, no hardware required.

Princeton Intro to Robotics (IRoM / Majumdar). Every lab targets the **same
plant**: the planar quadrotor you write in Lab 01.

**Start here → `make lab00`**

## Quickstart

```bash
python3 -m pip install -e .
make lab00          # gif in media/  (uses reference/ until you fill TODOs)
make check          # pytest + reference lab tables
```

Then open `labs/lab00_hello_state/lab.py`, fill the TODOs, and grade yourself:

```bash
make check00        # your lab.py, partial-credit table, <5 s
make lab00          # re-render; resolve prefers your code once it smokes
```

Then the rest of Phase 1 (plant → cascade PD → LQR; 3D is a side quest):

```bash
make check01 && make lab01
make check03 && make lab03
make check04 && make lab04
make check02 && make lab02
```

`python -m pytest` is the same core suite as `make test`.

## How a lab works

**Explain** (`README.md`, ≤1 page) → **Tinker** (`lab.py`, the only file you
edit) → **Check** (`check.py`, a table not a stack trace) → **See it**
(`demo.py` → gif) → tick `PROGRESS.md`.

Downstream labs import through `flightlab.resolve.get`. If your earlier lab
isn't passing, you get a warning banner and the `reference/` implementation —
never a blocked week.

## Stack

NumPy + Matplotlib, 2D-first. SciPy for the occasional solver. No Drake, no
ROS, no Crazyflie. The 3D quadrotor and a unicycle show up later as secondary
plants.

## Repo map

```
flightlab/     shared core (integrators, plants, viz, checks, resolver)
labs/          one folder per lab; edit lab.py only
reference/     fallback implementations (spoilers; accepted)
tests/         core + every reference check
docs/          ARCHITECTURE, LECTURE_LAB_MAP, PLAN, BACKLOG
```

Built labs right now: **00–04** (Phase 1 control). The rest of the map is in
[`docs/LECTURE_LAB_MAP.md`](docs/LECTURE_LAB_MAP.md).
