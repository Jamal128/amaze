from mazegen.core.cell import Cell
from mazegen.core.direction import Direction

PATTERN_42 = [
    [1, 0, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [0, 0, 1, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 1, 1],
]

PATTERN_H = len(PATTERN_42)
PATTERN_W = len(PATTERN_42[0])


class Maze:
    """Represents the maze grid and exposes operations on it.

    Args:
        width: Number of columns.
        height: Number of rows.

    Attributes:
        grid: 2D list of Cell objects indexed as grid[y][x].
    """

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.grid: list[list[Cell]] = [
            [Cell(x, y) for x in range(width)]
            for y in range(height)
        ]

    def reset(self) -> None:
        for row in self.grid:
            for cell in row:
                cell.reset()

    def get_cell(self, x: int, y: int) -> Cell:
        """Return the cell at (x, y).

        Args:
            x: Column index.
            y: Row index.

        Returns:
            The Cell at the given position.
        """
        return self.grid[y][x]

    def in_bounds(self, x: int, y: int) -> bool:
        """Check whether (x, y) is inside the maze.

        Args:
            x: Column index.
            y: Row index.

        Returns:
            True if the coordinates are valid.
        """
        return 0 <= x < self.width and 0 <= y < self.height

    def neighbour(self, cell: Cell, direction: Direction) -> Cell | None:
        """Return the neighbouring cell in the given direction, or None.

        Args:
            cell: Source cell.
            direction: Direction to look.

        Returns:
            Adjacent Cell if it exists within bounds, otherwise None.
        """
        dx, dy = direction.delta()
        nx, ny = cell.x + dx, cell.y + dy
        if self.in_bounds(nx, ny):
            return self.get_cell(nx, ny)
        return None

    def carve(self, cell: Cell, direction: Direction) -> None:
        """Remove the wall between a cell and its neighbour in one step.

        Args:
            cell: The source cell.
            direction: Direction toward the neighbour.
        """

        neighbour = self.neighbour(cell, direction)

        if not neighbour:
            return

        if cell.locked or neighbour.locked:
            return

        cell.remove_wall(direction)
        neighbour.remove_wall(direction.opposite())

    def apply_pattern_42(self, origin_x: int, origin_y: int) -> None:
        """Mark the '42' pattern cells starting at the given origin.

        Args:
            origin_x: X offset for the pattern.
            origin_y: Y offset for the pattern.
        """
        for row_i, row in enumerate(PATTERN_42):
            for col_i, val in enumerate(row):
                if val == 1:
                    cell = self.get_cell(origin_x + col_i, origin_y + row_i)
                    cell.locked = True
        self.seal_locked_cells()

    def seal_locked_cells(self) -> None:
        """Close all walls of locked cells to make them impassable."""
        for row in self.grid:
            for cell in row:
                if cell.locked:
                    cell.close_all()

    def place_pattern_42(
        self,
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> bool:
        """Place the '42' pattern in the first valid position.

        Skips positions that would overlap entry or exit cells.

        Args:
            entry: (x, y) of the entry cell.
            exit_: (x, y) of the exit cell.

        Returns:
            True if the pattern was placed, False if the maze is too small.
        """
        if self.width < PATTERN_W or self.height < PATTERN_H:
            return False

        ox = (self.width - PATTERN_W) // 2
        oy = (self.height - PATTERN_H) // 2

        if self._pattern_conflicts(ox, oy, entry, exit_):
            raise ValueError(
                    "'42' pattern conflicts with entry/exit positions"
                            )

        self.apply_pattern_42(ox, oy)
        return True

    def _pattern_conflicts(
        self,
        ox: int,
        oy: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> bool:
        """Check whether the pattern at (ox, oy) overlaps entry or exit.

        Args:
            ox: X origin of the pattern.
            oy: Y origin of the pattern.
            entry: Entry coordinates.
            exit_: Exit coordinates.

        Returns:
            True if there is a conflict.
        """
        for row_i, row in enumerate(PATTERN_42):
            for col_i, val in enumerate(row):
                if val == 1:
                    x, y = ox + col_i, oy + row_i
                    if (x, y) in (entry, exit_):
                        return True
        return False

    def _is_open_3x3(self, sx: int, sy: int) -> bool:

        for y in range(sy, sy + 3):
            for x in range(sx, sx + 3):

                cell = self.get_cell(x, y)

                if cell.locked:
                    return False

                # Right neighbour must be open
                if x < sx + 2:
                    if Direction.EAST in cell.walls:
                        return False

                # Bottom neighbour must be open
                if y < sy + 2:
                    if Direction.SOUTH in cell.walls:
                        return False

        return True

    def _close_middle_wall(self, sx: int, sy: int) -> None:

        cell = self.get_cell(sx + 1, sy + 1)
        neighbour = self.neighbour(cell, Direction.EAST)

        if not neighbour:
            return

        cell.add_wall(Direction.EAST)
        neighbour.add_wall(Direction.WEST)

    def patch_large_open_areas(self) -> None:

        for y in range(self.height - 2):
            for x in range(self.width - 2):

                if self._is_open_3x3(x, y):
                    print(f"Patched large open area at ({x}, {y})")
                    self._close_middle_wall(x, y)
