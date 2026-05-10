import random
from collections.abc import Generator

from mazegen.core.cell import Cell
from mazegen.core.direction import Direction
from mazegen.core.maze import Maze


def generate(
    maze: Maze,
    start_x: int,
    start_y: int,
    seed: int | None = None,
) -> None:
    """Generate a perfect maze using iterative depth-first search.

    Visits every non-locked cell exactly once by maintaining a stack
    and randomly carving walls to unvisited neighbours.

    Args:
        maze: The Maze instance to generate into.
        start_x: X coordinate of the starting cell.
        start_y: Y coordinate of the starting cell.
        seed: Optional RNG seed for reproducibility.
    """
    for step in generate_animated(maze, start_x, start_y, seed):
        pass  # consume the generator without yielding


def generate_animated(
    maze: Maze,
    start_x: int,
    start_y: int,
    seed: int | None = None,
) -> Generator[Cell, None, None]:
    """DFS generator that yields the current cell at each carving step.

    Useful for animated rendering: iterate and redraw after each yield.

    Args:
        maze: The Maze instance to generate into.
        start_x: X coordinate of the starting cell.
        start_y: Y coordinate of the starting cell.
        seed: Optional RNG seed for reproducibility.

    Yields:
        The Cell being carved at each step.
    """
    rng = random.Random(seed)
    start = maze.get_cell(start_x, start_y)
    start.visited = True
    stack: list[Cell] = [start]

    while stack:
        current = stack[-1]
        neighbours = _unvisited_neighbours(maze, current)

        if not neighbours:
            stack.pop()
            continue

        direction, neighbour = rng.choice(neighbours)
        maze.carve(current, direction)
        neighbour.visited = True
        stack.append(neighbour)

        yield current
        yield neighbour


def _unvisited_neighbours(
    maze: Maze,
    cell: Cell,
) -> list[tuple[Direction, Cell]]:
    """Return all reachable, unvisited, unlocked neighbours of a cell.

    Args:
        maze: The maze containing the cell.
        cell: Source cell.

    Returns:
        List of (Direction, Cell) pairs for valid neighbours.
    """
    result = []
    for direction in Direction:
        neighbour = maze.neighbour(cell, direction)
        if neighbour and not neighbour.visited and not neighbour.locked:
            result.append((direction, neighbour))
    return result
