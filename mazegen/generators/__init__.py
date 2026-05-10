from mazegen.generators import dfs, prim
from mazegen.generators.prim import generate_animated as prim_generate_animated
from mazegen.generators.dfs import generate_animated as dfs_generate_animated
from mazegen.generators.prim import generate as prim_generate
from mazegen.generators.dfs import generate as dfs_generate

__all__ = [
    "dfs",
    "prim",
    "generate_animated",
    "prim_generate_animated",
    "dfs_generate_animated",
    "prim_generate",
    "dfs_generate",
]