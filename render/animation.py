"""Animation helpers for step-by-step maze rendering.

These utilities are rendering-backend agnostic: they drive the generator
and call a user-supplied draw callback after each step.
"""

import time
from collections.abc import Callable, Generator

from mazegen.core.cell import Cell
from mazegen.core.maze import Maze


def animate(
    generator: Generator[Cell, None, None],
    draw_cell: Callable[[Cell], None],
    delay: float = 0.01,
) -> None:
    """Drive a maze generator and call *draw_cell* after each carved cell.

    Args:
        generator: An animated generator from ``generators.dfs`` or
            ``generators.prim`` (yielding Cell objects).
        draw_cell: Callback that receives the just-carved Cell and
            redraws it on screen.
        delay: Seconds to sleep between steps. Set to 0 to disable.
    """
    for cell in generator:
        draw_cell(cell)
        if delay > 0:
            time.sleep(delay)


def animate_path(
    coords: list[tuple[int, int]],
    draw_coord: Callable[[int, int], None],
    delay: float = 0.02,
) -> None:
    """Animate drawing the solution path coordinate by coordinate.

    Args:
        coords: Ordered list of (x, y) positions along the path.
        draw_coord: Callback that receives (x, y) and renders that step.
        delay: Seconds to sleep between steps. Set to 0 to disable.
    """
    for x, y in coords:
        draw_coord(x, y)
        if delay > 0:
            time.sleep(delay)