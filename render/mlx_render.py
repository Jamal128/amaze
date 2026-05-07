"""MLX graphical renderer for the maze."""

import os
import random
from typing import Any

from mlx import Mlx  # type: ignore[import]

from mazegen.core.cell import Cell
from mazegen.core.maze import Maze
from mazegen.generators import generate_animated
from mazegen.solver.bfs import solve, path_to_coords
from render.animation import animate, animate_path
from parser.pydantic_model import MazeConfig

COLORS = ["red", "green", "blue", "cyan", "pink", "yellow"]


def render(maze: Maze, config: MazeConfig) -> None:
    """Launch the MLX window and enter the event loop.

    Args:
        maze: The generated Maze to display.
        config: MazeConfig holding entry, exit, dimensions, etc.
    """
    m = Mlx()
    p = m.mlx_init()
    assets = _load_assets(m, p, "assets")
    scale = _get_scale(m, p, config)

    state: dict[str, Any] = {
        "maze": maze,
        "color_i": random.randint(0, len(COLORS) - 1),
        "path_visible": False,
        "win": None,
    }

    state["win"] = _open_window(m, p, assets, config, scale)
    _render_cells(m, p, state["win"], assets, state["maze"], config, scale, state["color_i"])

    def on_mouse(button: int, x: int, y: int, _params: Any) -> None:
        _handle_mouse(m, p, assets, config, scale, state, x, y)

    def on_key(keynum: int, _params: Any) -> None:
        if keynum == 65307:  # Escape
            m.mlx_loop_exit(p)

    def on_close(_dummy: Any) -> None:
        m.mlx_loop_exit(p)

    m.mlx_mouse_hook(state["win"], on_mouse, None)
    m.mlx_key_hook(state["win"], on_key, None)
    m.mlx_hook(state["win"], 33, 0, on_close, None)

    m.mlx_loop(p)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _load_assets(m: Mlx, p: Any, directory: str) -> dict[str, Any]:
    """Walk *directory* and load every .png file.

    Args:
        m: MLX instance.
        p: MLX pointer.
        directory: Path to the assets folder.

    Returns:
        Dict mapping relative path (without extension) to MLX image.

    Raises:
        ValueError: If any PNG fails to load.
    """
    assets: dict[str, Any] = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith(".png"):
                continue
            path = os.path.join(root, file)
            key = os.path.relpath(path, directory).removesuffix(".png")
            img, _, _ = m.mlx_png_file_to_image(p, path)
            if not img:
                raise ValueError(f"Failed to load PNG: {path}")
            assets[key] = img
    return assets


def _get_scale(m: Mlx, p: Any, config: MazeConfig) -> int:
    """Choose tile size (32 or 64) based on screen and maze dimensions.

    Args:
        m: MLX instance.
        p: MLX pointer.
        config: Maze configuration.

    Returns:
        32 or 64 pixels per tile.
    """
    _w, screen_w, screen_h = m.mlx_get_screen_size(p)
    if config.width * 64 > screen_w or config.height * 64 > screen_h:
        return 32
    return 64


def _open_window(
    m: Mlx,
    p: Any,
    assets: dict[str, Any],
    config: MazeConfig,
    scale: int,
) -> Any:
    """Create and initialise the MLX window with the options bar.

    Args:
        m: MLX instance.
        p: MLX pointer.
        assets: Loaded asset dictionary.
        config: Maze configuration.
        scale: Tile size in pixels.

    Returns:
        The new MLX window handle.
    """
    height = max(scale * config.height, 512)
    win = m.mlx_new_window(p, scale * config.width, height + 200, "A-Maze-ing")
    m.mlx_clear_window(p, win)
    m.mlx_put_image_to_window(p, win, assets["options/regen"], 100, height)
    m.mlx_put_image_to_window(p, win, assets["options/color"], 400, height)
    m.mlx_put_image_to_window(p, win, assets["options/path"], 700, height)
    m.mlx_put_image_to_window(p, win, assets["options/close"], 1000, height)
    m.mlx_do_sync(p)
    return win


def _render_cells(
    m: Mlx,
    p: Any,
    win: Any,
    assets: dict[str, Any],
    maze: Maze,
    config: MazeConfig,
    scale: int,
    color_i: int,
) -> None:
    """Draw every cell, then overlay the entry and exit markers.

    Args:
        m: MLX instance.
        p: MLX pointer.
        win: MLX window handle.
        assets: Loaded asset dictionary.
        maze: The maze to draw.
        config: Maze configuration (provides entry/exit positions).
        scale: Tile size in pixels.
        color_i: Index into COLORS for the current wall colour.
    """
    m.mlx_do_sync(p)
    color = COLORS[color_i]
    for y, row in enumerate(maze.grid):
        m.mlx_do_sync(p)
        for x, cell in enumerate(row):
            m.mlx_put_image_to_window(
                p, win, assets[f"color/{color}"], x * scale, y * scale
            )
            m.mlx_put_image_to_window(
                p, win, assets[f"cell_images/{cell.to_hex()}"], x * scale, y * scale
            )

    ex, ey = config.entry.x * scale, config.entry.y * scale
    m.mlx_put_image_to_window(p, win, assets["options/entry"], ex, ey)
    xx, xy = config.exit_.x * scale, config.exit_.y * scale
    m.mlx_put_image_to_window(p, win, assets["options/exit"], xx, xy)
    m.mlx_do_sync(p)


def _draw_path(
    m: Mlx,
    p: Any,
    win: Any,
    assets: dict[str, Any],
    maze: Maze,
    config: MazeConfig,
    scale: int,
) -> None:
    """Solve and animate the shortest path onto the window.

    Args:
        m: MLX instance.
        p: MLX pointer.
        win: MLX window handle.
        assets: Loaded asset dictionary.
        maze: The maze to solve.
        config: Maze configuration (provides entry/exit positions).
        scale: Tile size in pixels.
    """
    path = solve(
        maze,
        config.entry.x, config.entry.y,
        config.exit_.x, config.exit_.y,
    )
    coords = path_to_coords(config.entry.x, config.entry.y, path)

    def draw_coord(x: int, y: int) -> None:
        m.mlx_put_image_to_window(
            p, win, assets["options/light"], x * scale, y * scale
        )
        m.mlx_do_sync(p)

    animate_path(coords, draw_coord, delay=0.02)


def _handle_mouse(
    m: Mlx,
    p: Any,
    assets: dict[str, Any],
    config: MazeConfig,
    scale: int,
    state: dict[str, Any],
    x: int,
    y: int,
) -> None:
    """Dispatch mouse clicks to the appropriate action.

    Args:
        m: MLX instance.
        p: MLX pointer.
        assets: Loaded asset dictionary.
        config: Maze configuration.
        scale: Tile size in pixels.
        state: Mutable render state (maze, color_i, path_visible, win).
        x: Mouse X coordinate.
        y: Mouse Y coordinate.
    """
    maze_height = max(scale * state["maze"].height, 512)
    if y < maze_height:
        return  # click was inside the maze area

    if x < 400:  # Regenerate
        new_maze = Maze(config.width, config.height)
        new_maze.place_pattern_42(
            (config.entry.x, config.entry.y),
            (config.exit_.x, config.exit_.y),
        )
        m.mlx_destroy_window(p, state["win"])
        state["win"] = _open_window(m, p, assets, config, scale)

        gen = generate_animated(
            new_maze,
            config.entry.x, config.entry.y,
            seed=random.randint(0, 10 ** 9),
        )

        def draw_cell(cell: Cell) -> None:
            color = COLORS[state["color_i"]]
            m.mlx_put_image_to_window(
                p, state["win"],
                assets[f"color/{color}"],
                cell.x * scale, cell.y * scale,
            )
            m.mlx_put_image_to_window(
                p, state["win"],
                assets[f"cell_images/{cell.to_hex()}"],
                cell.x * scale, cell.y * scale,
            )
            m.mlx_do_sync(p)

        animate(gen, draw_cell, delay=0.005)
        new_maze.seal_locked_cells()
        state["maze"] = new_maze
        state["path_visible"] = False

        m.mlx_mouse_hook(state["win"], lambda b, mx, my, pr: _handle_mouse(
            m, p, assets, config, scale, state, mx, my
        ), None)
        m.mlx_key_hook(state["win"], lambda k, pr: m.mlx_loop_exit(p) if k == 65307 else None, None)
        m.mlx_hook(state["win"], 33, 0, lambda d: m.mlx_loop_exit(p), None)

    elif x < 700:  # Colour
        state["color_i"] = (state["color_i"] + 1) % len(COLORS)
        _render_cells(
            m, p, state["win"], assets, state["maze"],
            config, scale, state["color_i"]
        )
        if state["path_visible"]:
            _draw_path(m, p, state["win"], assets, state["maze"], config, scale)

    elif x < 1000:  # Toggle path
        if state["path_visible"]:
            _render_cells(
                m, p, state["win"], assets, state["maze"],
                config, scale, state["color_i"]
            )
            state["path_visible"] = False
        else:
            _draw_path(m, p, state["win"], assets, state["maze"], config, scale)
            state["path_visible"] = True

    else:  # Close
        m.mlx_loop_exit(p)