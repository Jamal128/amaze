from parser import parse_config
from mazegen.Mazegen import MazeGenerator
from render.mlx_render import render
from output.writer import write_maze


def main() -> None:
    try:
        # Parse configuration from file
        config = parse_config("config.txt")

        # Create maze generator instance with specified parameters
        generator = MazeGenerator(
            width=config.width,
            height=config.height,
            seed=config.seed,
            algorithm=config.algorithm or "dfs",
            perfect=config.perfect,
        )
        # Generate the maze with specified entry and exit points
        generator.generate(
            entry=(config.entry.x, config.entry.y),
            exit_=(config.exit_.x, config.exit_.y),
        )
        # Render the generated maze using MLX
        render(generator.maze, config, generator,
               config.algorithm or "dfs", config.perfect)
        # Write the generated maze to the output file
        write_maze(generator.maze, config)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
