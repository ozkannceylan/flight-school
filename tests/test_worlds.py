"""Grids, costmaps, and obstacle fields."""

from __future__ import annotations

import numpy as np

from flightlab.worlds import forest_lab07, manhattan, maze_lab05, terrain_lab06


def test_maze_has_start_goal_and_path():
    grid, start, goal = maze_lab05()
    assert grid.is_free(start) and grid.is_free(goal)
    assert start != goal
    assert len(grid.neighbors(start)) >= 1


def test_terrain_has_expensive_door():
    cmap, start, goal = terrain_lab06()
    assert cmap.enter_cost((4, 7)) > 5
    assert cmap.grid.is_free(start) and cmap.grid.is_free(goal)
    assert manhattan(start, goal) > 0


def test_forest_start_goal_free():
    field, start, goal = forest_lab07()
    assert not field.collide_point(start)
    assert not field.collide_point(goal)
    assert field.collide_segment(np.array([1.6, 1.2]), np.array([1.6, 1.2]))
