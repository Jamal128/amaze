from collections import deque

from mazegen.core.direction import Direction
from mazegen.core.maze import Maze


def solve(
    maze: Maze,
    start_x: int,
    start_y: int,
    end_x: int,
    end_y: int,
) -> str:
    """Find the shortest path through the maze using BFS.

    Args:
        maze: The maze to solve.
        start_x: X coordinate of the start cell.
        start_y: Y coordinate of the start cell.
        end_x: X coordinate of the end cell.
        end_y: Y coordinate of the end cell.

    Returns:
        String of direction initials (N, E, S, W) representing the path,
        or an empty string if no path exists.
    """
    start = (start_x, start_y)
    end = (end_x, end_y)

    queue: deque[tuple[tuple[int, int], str]] = deque([(start, "")])
    visited: set[tuple[int, int]] = set()

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) == end:
            return path

        if (x, y) in visited:
            continue
        visited.add((x, y))

        cell = maze.get_cell(x, y)
        for direction in Direction:
            if cell.has_wall(direction):
                continue

            dx, dy = direction.delta()
            nx, ny = x + dx, y + dy

            if not maze.in_bounds(nx, ny) or (nx, ny) in visited:
                continue

            queue.append(((nx, ny), path + direction.name[0]))

    return ""


def path_to_coords(
    start_x: int,
    start_y: int,
    path: str,
) -> list[tuple[int, int]]:
    """Convert a direction string into a list of (x, y) coordinates.

    Args:
        start_x: X of the starting position.
        start_y: Y of the starting position.
        path: Direction string as returned by ``solve``.

    Returns:
        List of (x, y) coordinates visited along the path,
        including the start but excluding the last step.
    """
    deltas: dict[str, tuple[int, int]] = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0),
    }
    x, y = start_x, start_y
    coords: list[tuple[int, int]] = [(x, y)]
    for char in path[:-1]:
        dx, dy = deltas[char]
        x, y = x + dx, y + dy
        coords.append((x, y))
    return coords
