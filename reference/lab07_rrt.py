"""Reference implementation for Lab 07 — Sampling Your Way Out."""

from __future__ import annotations

import numpy as np

from flightlab.worlds import ObstacleField


def _steer(a: np.ndarray, b: np.ndarray, step: float) -> np.ndarray:
    d = b - a
    n = float(np.linalg.norm(d))
    if n < 1e-12:
        return a.copy()
    return a + d * (min(step, n) / n)


def _path(nodes: np.ndarray, parents: np.ndarray, last: int) -> np.ndarray:
    idx = []
    i = last
    while i >= 0:
        idx.append(i)
        i = int(parents[i])
    idx.reverse()
    return nodes[idx]


def rrt(
    field: ObstacleField,
    start: np.ndarray,
    goal: np.ndarray,
    *,
    seed: int = 0,
    n_iter: int = 400,
    step: float = 0.35,
    goal_bias: float = 0.12,
    goal_tol: float = 0.30,
):
    rng = np.random.default_rng(seed)
    nodes = [np.asarray(start, dtype=float).reshape(2)]
    parents = [-1]
    last = 0
    for _ in range(n_iter):
        sample = np.asarray(goal, dtype=float) if rng.random() < goal_bias else field.sample_free(rng)
        dists = np.linalg.norm(np.stack(nodes) - sample, axis=1)
        i_near = int(np.argmin(dists))
        new = _steer(nodes[i_near], sample, step)
        if field.collide_segment(nodes[i_near], new):
            continue
        nodes.append(new)
        parents.append(i_near)
        last = len(nodes) - 1
        if np.linalg.norm(new - goal) <= goal_tol and not field.collide_segment(new, goal):
            nodes.append(np.asarray(goal, dtype=float).reshape(2))
            parents.append(last)
            last = len(nodes) - 1
            break
    path = _path(np.stack(nodes), np.array(parents), last)
    return path, np.stack(nodes), np.array(parents)


def rrt_star(
    field: ObstacleField,
    start: np.ndarray,
    goal: np.ndarray,
    *,
    seed: int = 0,
    n_iter: int = 400,
    step: float = 0.35,
    goal_bias: float = 0.12,
    goal_tol: float = 0.30,
    radius: float = 0.8,
):
    rng = np.random.default_rng(seed)
    nodes = [np.asarray(start, dtype=float).reshape(2)]
    parents = [-1]
    cost = [0.0]
    last = 0
    for _ in range(n_iter):
        sample = np.asarray(goal, dtype=float) if rng.random() < goal_bias else field.sample_free(rng)
        arr = np.stack(nodes)
        i_near = int(np.argmin(np.linalg.norm(arr - sample, axis=1)))
        new = _steer(nodes[i_near], sample, step)
        if field.collide_segment(nodes[i_near], new):
            continue
        # cheapest parent in the ball
        dists = np.linalg.norm(arr - new, axis=1)
        ball = np.where(dists <= radius)[0]
        parent = i_near
        best = cost[i_near] + float(np.linalg.norm(new - nodes[i_near]))
        for j in ball:
            if field.collide_segment(nodes[j], new):
                continue
            cand = cost[j] + float(np.linalg.norm(new - nodes[j]))
            if cand < best:
                best, parent = cand, int(j)
        nodes.append(new)
        parents.append(parent)
        cost.append(best)
        new_i = len(nodes) - 1
        # rewire
        for j in ball:
            extra = float(np.linalg.norm(nodes[j] - new))
            if cost[new_i] + extra + 1e-12 < cost[j] and not field.collide_segment(new, nodes[j]):
                parents[j] = new_i
                cost[j] = cost[new_i] + extra
        last = new_i
        if np.linalg.norm(new - goal) <= goal_tol and not field.collide_segment(new, goal):
            nodes.append(np.asarray(goal, dtype=float).reshape(2))
            parents.append(last)
            cost.append(cost[last] + float(np.linalg.norm(goal - new)))
            last = len(nodes) - 1
            break
    path = _path(np.stack(nodes), np.array(parents), last)
    return path, np.stack(nodes), np.array(parents)


def shortcut(path: np.ndarray, field: ObstacleField, passes: int = 8) -> np.ndarray:
    pts = [np.asarray(p, dtype=float).reshape(2) for p in path]
    if len(pts) < 3:
        return np.stack(pts) if pts else np.zeros((0, 2))
    for _ in range(passes):
        i = 0
        new: list[np.ndarray] = [pts[0]]
        while i < len(pts) - 1:
            j = len(pts) - 1
            while j > i + 1 and field.collide_segment(pts[i], pts[j]):
                j -= 1
            new.append(pts[j])
            i = j
        pts = new
    return np.stack(pts)
