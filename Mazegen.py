"""mazegen reusable maze generation package.

Quickstart::

    from amazeing.mazegen import MazeGenerator

    gen = MazeGenerator(width=20, height=15, seed=42, algorithm="dfs")
    gen.generate(entry=(0, 0))
    path = gen.solve(entry=(0, 0), exit_=(19, 14))
    print(path)          # e.g. "EESSWW..."
    print(gen.to_hex())  # list of hex 
    """
    
from mazegen.core.maze import Maze
from mazegen.generators.dfs import generate as dfs_generate
from mazegen.generators.dfs import generate_animated
from mazegen.generators.prim import generate as prim_generate
from mazegen.solver.bfs import solve


class MazeGenerator:
    """High-level interface for maze generation and solving.

    Args:
        width: Number of columns (>= 2).
        height: Number of rows (>= 2).
        seed: Optional RNG seed for reproducibility.
        algorithm: Generation algorithm – ``"dfs"`` or ``"prim"``.

    Example::

        gen = MazeGenerator(20, 15, seed=1, algorithm="prim")
        gen.generate(entry=(0, 0), exit_=(19, 14))
        path = gen.solve((0, 0), (19, 14))
    """

    def __init__(
        self,
        width: int,
        height: int,
        seed: int | None = None,
        algorithm: str = "dfs",
    ) -> None:
        self.width = width
        self.height = height
        self.seed = seed
        self.algorithm = algorithm
        self.maze = Maze(width, height)

    def generate(
        self,
        entry: tuple[int, int],
        exit_: tuple[int, int] | None = None,
    ) -> None:
        """Generate the maze, placing the '42' pattern when possible.

        Args:
            entry: (x, y) start cell for generation.
            exit_: (x, y) exit cell; used to avoid pattern overlap.
        """
        placed = self.maze.place_pattern_42(
            entry, exit_ if exit_ is not None else entry
        )
        if not placed and (self.maze.width >= 7 and self.maze.height >= 5):
            print("Warning: maze too small to place '42' pattern.")

        if self.algorithm == "dfs":
            dfs_generate(
                self.maze,
                entry[0],
                entry[1],
                self.seed,
            )

        elif self.algorithm == "prim":
            prim_generate(
                self.maze,
                entry[0],
                entry[1],
                self.seed,
            )

        else:
            raise ValueError(
                f"Unknown algorithm: {self.algorithm}"
            )

    def generate_animated(
        self,
        entry: tuple[int, int],
        exit_: tuple[int, int] | None = None,
    ) -> object:
        """Return an animated generator for step-by-step rendering.

        Args:
            entry: (x, y) start cell.
            exit_: (x, y) exit cell; used to avoid pattern overlap.

        Returns:
            Generator yielding each carved Cell.
        """
        self.maze.place_pattern_42(
            entry, exit_ if exit_ is not None else entry
        )
        return generate_animated(
            self.maze, entry[0], entry[1], self.algorithm, self.seed
        )

    def solve(
        self,
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> str:
        """Return the shortest path from entry to exit as a direction string.

        Args:
            entry: (x, y) of the entry cell.
            exit_: (x, y) of the exit cell.

        Returns:
            String of N/E/S/W characters, or ``""`` if no path found.
        """
        return solve(self.maze, entry[0], entry[1], exit_[0], exit_[1])

    def to_hex(self) -> list[str]:
        """Return the maze as a list of hex strings, one per row.

        Returns:
            List of strings where each character encodes one cell's walls.
        """
        return [
            "".join(cell.to_hex() for cell in row)
            for row in self.maze.grid
        ]

