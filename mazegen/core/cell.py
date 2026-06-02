from mazegen.core.direction import Direction


class Cell:
    '''Class cell which represents a cell in the maze.'''
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.walls: set[Direction] = {
                                Direction.NORTH, Direction.EAST,
                                Direction.SOUTH, Direction.WEST
                                 }
        self.visited: bool = False
        self.locked: bool = False

    def remove_wall(self, direction: Direction) -> None:
        '''Removes the wall in the given direction.'''
        self.walls.discard(direction)

    def add_wall(self, direction: Direction) -> None:
        self.walls.add(direction)

    def has_wall(self, direction: Direction) -> bool:
        '''Returns True if the cell has a wall in the
        given direction, False otherwise.'''
        return direction in self.walls

    def close_all(self) -> None:
        '''Closes all walls of the cell.'''
        self.walls = {
            Direction.NORTH, Direction.EAST,
            Direction.SOUTH, Direction.WEST
        }

    def to_hex(self) -> str:
        '''Returns a hexadecimal representation of the cell's walls.'''
        value = 0
        if Direction.NORTH in self.walls:
            value += 1
        if Direction.EAST in self.walls:
            value += 2
        if Direction.SOUTH in self.walls:
            value += 4
        if Direction.WEST in self.walls:
            value += 8
        return format(value, "X")

    def reset(self) -> None:
        '''Resets the cell to its initial state
        (all walls closed, not visited)'''
        self.visited = False
        self.close_all()
