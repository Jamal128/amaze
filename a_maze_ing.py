
from parser import parse_config
from mazegen.Mazegen import MazeGenerator
from render.mlx_render import render
from output.writer import write_maze

def main() -> None:
    try:
        config = parse_config("config.txt")

        generator = MazeGenerator(
            width=config.width,
            height=config.height,
            seed=config.seed,
            algorithm=config.algorithm,
            perfect=config.perfect,
        )

        generator.generate(
            entry=(config.entry.x, config.entry.y),
            exit_=(config.exit_.x, config.exit_.y),
        )

        render(generator.maze, config, generator, config.algorithm, config.perfect)
        write_maze(generator.maze, config)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()