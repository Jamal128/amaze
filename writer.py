from amazeing.mazegen.generator import create_maze
from mazegen.maze import Maze
from parser.pydantic_model import MazeConfig
from algo import bfs

def write_maze(maze: Maze, config: MazeConfig) -> None:
    '''Function to read the generated maze and write it to the output file in the specified format.
    ARGS:
        maze: The generated maze to write.
        config: The configuration containing the output file path and entry/exit coordinates.
    '''
    with open(config.output_file, "w") as file:
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                file.write(cell.to_hex())
            file.write("\n")
        file.write("\n")
        file.write(f"{config.entry}\n")
        file.write(f"{config.exit_}\n")
        file.write(f"{bfs.solve(maze, config.entry.x, config.entry.y, config.exit_.x, config.exit_.y)}\n")


def debug_maze(maze: Maze) -> None:
    """Imprime cada celda y sus muros para inspección."""
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            walls = [d.name for d in cell.walls]
            print(f"({x},{y}) locked={cell.locked} visited={cell.visited} walls={walls}")


if __name__ == "__main__":
    config = MazeConfig(
        WIDTH="10",
        HEIGHT="10",
        ENTRY="0,0",
        EXIT="9,9",
        OUTPUT_FILE="maze_output.txt",
        PERFECT="True",
        SEED="42"
    )
    maze = create_maze(config)
    debug_maze(maze)
    write_maze(maze, config)