from mazegen.core import Maze
from parser.pydantic_model import MazeConfig
from mazegen.solver import bfs
from pathlib import Path


def write_maze(maze: Maze, config: MazeConfig) -> None:
    '''Function to read the generated maze and
    write it to the output file in the specified format.
    ARGS:
        maze: The generated maze to write.
        config: The configuration containing the output file path and
        entry/exit coordinates.
    '''

    output_path = Path(config.output_file)

    if output_path.parent.name != "output_dir":
        raise PermissionError(f"Cant write (Expected path: "
                              f"output_dir/OUTPUT_FILE.txt),"
                              f" Received: {output_path}")

    with open(config.output_file, "w") as file:
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                file.write(cell.to_hex())
            file.write("\n")
        file.write("\n")
        file.write(f"{config.entry}\n")
        file.write(f"{config.exit_}\n")
        file.write(f"{bfs.solve(maze, config.entry.x, config.entry.y,
                                config.exit_.x, config.exit_.y)}\n")
