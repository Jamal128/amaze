"""Parser package for A-Maze-ing project.

Provides configuration file parsing and validation using Pydantic.
"""

from parser.pydantic_model import MazeConfig
from parser.config_reader import parse_config

__all__ = ["MazeConfig", "parse_config"]