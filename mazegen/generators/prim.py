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
    """Generate a perfect maze using randomised Prim's algorithm.

    Produces mazes with many short dead-ends and a more uniform feel
    compared to DFS.

    Args:
        maze: The Maze instance to generate into.
        start_x: X coordinate of the starting cell.
        start_y: Y coordinate of the starting cell.
        seed: Optional RNG seed for reproducibility.
    """
    for step in generate_animated(maze, start_x, start_y, seed):
        pass


def generate_animated(
    maze: Maze,
    start_x: int,
    start_y: int,
    seed: int | None = None,
) -> Generator[Cell, None, None]:
    """Prim generator that yields the current cell at each carving step.

    Useful for animated rendering: iterate and redraw after each yield.

    Args:
        maze: The Maze instance to generate into.
        start_x: X coordinate of the starting cell.
        start_y: Y coordinate of the starting cell.
        seed: Optional RNG seed for reproducibility.

    Yields:
        The Cell being added to the maze at each step.
    """
    rng = random.Random(seed)

    start = maze.get_cell(start_x, start_y)
    start.visited = True

    # frontier: list of (source_cell, direction, target_cell)
    frontier: list[tuple[Cell, Direction, Cell]] = []
    _add_frontier(maze, start, frontier)

    while frontier:
        idx = rng.randrange(len(frontier))
        source, direction, target = frontier.pop(idx)

        if target.visited:
            continue

        maze.carve(source, direction)
        target.visited = True

        _add_frontier(maze, target, frontier)

        yield target


def _add_frontier(
    maze: Maze,
    cell: Cell,
    frontier: list[tuple[Cell, Direction, Cell]],
) -> None:
    """Append all unvisited, unlocked neighbours of cell to the frontier.

    Args:
        maze: The containing maze.
        cell: The recently visited cell.
        frontier: The mutable frontier list to extend.
    """
    for direction in Direction:
        neighbour = maze.neighbour(cell, direction)
        if neighbour and not neighbour.visited and not neighbour.locked:
            frontier.append((cell, direction, neighbour))
