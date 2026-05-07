from enum import Enum


class Direction(Enum):
    """Enum representing the four cardinal directions in the maze.

    Each member holds a (dx, dy) tuple indicating movement in the grid.
    """

    NORTH = (0, -1)
    EAST = (1,  0)
    SOUTH = (0,  1)
    WEST = (-1, 0)

    def delta(self) -> tuple[int, int]:
        """Return the (dx, dy) movement vector for this direction.

        Returns:
            A tuple (dx, dy) representing the grid displacement.
        """
        return self.value  # type: ignore[return-value]

    def opposite(self) -> "Direction":
        """Return the opposite cardinal direction.

        Returns:
            The Direction facing the opposite way.
        """
        if self == Direction.NORTH:
            return Direction.SOUTH
        if self == Direction.SOUTH:
            return Direction.NORTH
        if self == Direction.EAST:
            return Direction.WEST
        return Direction.EAST
