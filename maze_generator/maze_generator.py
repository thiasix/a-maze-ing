"""Tools for the generation of two types of mazes.

This module contains the class that provides all the associated methods and
validations for the creation of mazes.
"""

import random
from typing import Any


class MazeGenerator:
    """
    Provides the tools to create two types of mazes.

    Attributes:
        height (int): Height of the maze.
        width (int): Width of the maze.
        seed (int): Number to determine a pseudo-randomised specific maze
            (optional).
        grid (list of lists of ints): 2D list that represents the initial
            grid for the creation of the maze. The ints represent the wall
            values of each cell.
        visited (list of lists of bool): 2D list that represents the cells
            visited by the algorithm through the generation of passages.
            The bools represent whether a cell has been checked.
        blocked (list of lists of bool): 2D list that stores the 42 pattern
            within the maze. The bools represent whether the cell is blocked
            by the pattern.
        entry (tuple of two ints): Coordinates of the starting point of the
            resolution path.
        exit (tuple of two ints): Coordinates of the exit point of the
            resolution path.
        perfect (bool): Flag that indicates the type of maze. True indicates
            a single resolution path maze. False indicates a Pacman-style
            board.
        output_file (.txt): File that documents the cells in hexadecimal,
            the entry and exit coordinates, and the path followed to
            resolution.
        random_generator (random module): Stores the seed, if any, to
            determine reproducibility.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Initialise a MazeGenerator object.
        
        Parameters:
            config (dict of str keys and Any values): Maze creation values.
        """
        self.height: int = config["HEIGHT"]
        self.width: int = config["WIDTH"]
        self.seed: int | None = config.get("SEED", None)
        self.grid: list[list[int]]
        self.visited: list[list[bool]]
        self.blocked: list[list[bool]]
        self.entry: tuple[int, int] = config["ENTRY"]
        self.exit: tuple[int, int] = config["EXIT"]
        self.perfect: bool = config.get("PERFECT", False)
        self.output_file = config["OUTPUT_FILE"]
        self.random_generator = random.Random(self.seed)

    def create_grid(self
                    ) -> tuple[
                        list[list[int]], list[list[bool]], list[list[bool]]]:
        """
        Creation of the initial grid upon which the maze will be carved.
        
        Returns:
            tuple: three lists, first of maze cell initial values, second of
            bool values for maze-carving visited cells, and third of bool
            values to block the 42 pattern.
        """
        self.grid = []
        self.visited = []
        self.blocked = []
        for y in range(self.height):
            row = []
            visit_row = []
            block_row = []
            for x in range(self.width):
                row.append(15)
                visit_row.append(False)
                block_row.append(False)
            self.grid.append(row)
            self.visited.append(visit_row)
            self.blocked.append(block_row)
        return self.grid, self.visited, self.blocked

    def forty_two(self) -> None:
        """ Blocks cells belonging to the 42 pattern if size can fit it. """
        pattern = [["42", "--", "--", "--", "42", "42", "42"],
                   ["42", "--", "--", "--", "--", "--", "42"],
                   ["42", "42", "42", "--", "42", "42", "42"],
                   ["--", "--", "42", "--", "42", "--", "--"],
                   ["--", "--", "42", "--", "42", "42", "42"]]
        if self.height > 7 and self.width > 9:
            centre_height = (self.height - len(pattern)) // 2
            centre_width = (self.width - len(pattern[0])) // 2
            for y in range(len(pattern)):
                for x in range(len(pattern[0])):
                    current = pattern[y][x]
                    if current == "42":
                        maze_y = centre_height + y
                        maze_x = centre_width + x
                        self.blocked[maze_y][maze_x] = True
        else:
            print("The maze is too small to include '42'")

    def carve_maze(self) -> None:
        """ Carves the PERFECT maze by using Depth-First Search. """
        entry_x, entry_y = self.entry
        been_here_stack: list[tuple[int, int]] = []
        been_here_stack.append((entry_y, entry_x))
        self.visited[entry_y][entry_x] = True
        while been_here_stack:
            current_cell = been_here_stack[-1]
            curr_y, curr_x = current_cell
            neighbours: list[tuple[int, int, int]] = []
            # check NORTHERN neighbour
            if (curr_y > 0 and not self.visited[curr_y - 1][curr_x]
                    and not self.blocked[curr_y - 1][curr_x]):
                neighbours.append((curr_y - 1, curr_x, 1))
            # check SOUTHERN neighbour
            if (curr_y < (len(self.grid) - 1)
                    and not self.visited[curr_y + 1][curr_x]
                    and not self.blocked[curr_y + 1][curr_x]):
                neighbours.append((curr_y + 1, curr_x, 4))
            # check EASTERN neighbour
            if (curr_x < (len(self.grid[0]) - 1)
                    and not self.visited[curr_y][curr_x + 1]
                    and not self.blocked[curr_y][curr_x + 1]):
                neighbours.append((curr_y, curr_x + 1, 2))
            # check WESTERN neighbour
            if (curr_x > 0 and not self.visited[curr_y][curr_x - 1]
                    and not self.blocked[curr_y][curr_x - 1]):
                neighbours.append((curr_y, curr_x - 1, 8))
            if not neighbours:
                been_here_stack.pop()
            else:
                step = self.random_generator.choice(neighbours)
                step_y, step_x, direc = step
                been_here_stack.append((step_y, step_x))
                self.visited[step_y][step_x] = True
                # north
                if direc == 1:
                    self.grid[curr_y][curr_x] &= ~1
                    self.grid[step_y][step_x] &= ~4
                # south
                elif direc == 4:
                    self.grid[curr_y][curr_x] &= ~4
                    self.grid[step_y][step_x] &= ~1
                # east
                elif direc == 2:
                    self.grid[curr_y][curr_x] &= ~2
                    self.grid[step_y][step_x] &= ~8
                # west
                elif direc == 8:
                    self.grid[curr_y][curr_x] &= ~8
                    self.grid[step_y][step_x] &= ~2

    def verify_boundaries(self, cell: tuple[int, int], direction: int) -> bool:
        """
        Verifies boundaries and potential 42 placement of cell and of neighbouring cell.

        Arguments:
            cell (tuple of ints): Coordinates of cell.
            direction (int): direction towards neighbouring cell.
        
        Returns:
            bool: True if wall can be removed. False if it can't.
        """
        cell_y, cell_x = cell
        neighbour_y = cell_y
        neighbour_x = cell_x
        # assign NORTHERN neighbour
        if direction == 1:
            neighbour_y -= 1
        # assign EASTERN neighbour
        elif direction == 2:
            neighbour_x += 1
        # assign SOUTHERN neighbour
        elif direction == 4:
            neighbour_y += 1
        # assign WESTERN neighbour
        elif direction == 8:
            neighbour_x -= 1
        # boundary checks
        if neighbour_y < 0 or neighbour_y > self.height - 1:
            return False
        if neighbour_x < 0 or neighbour_x > self.width - 1:
            return False
        # 42 blockage check
        if (self.blocked[cell_y][cell_x]
                or self.blocked[neighbour_y][neighbour_x]):
            return False
        return True

    def three_by_three(self, wall: tuple[int, int]) -> bool:
        """
        Verifies whether removing a wall creates a forbidden 3x3 passage.

        Arguments:
            wall (tuple of ints): Coordinates of cell.
        
        Returns:
            bool: True if removing wall creates 3x3 passage. False if it doesn't.
        """
        cell_y, cell_x = wall
        if (
            # check first row, first cell east and south REVISE
            self.grid[cell_y][cell_x] & 2 == 0
            and self.grid[cell_y][cell_x] & 4 == 0
            # check first row, second cell east and south
            and self.grid[cell_y][cell_x + 1] & 2 == 0
            and self.grid[cell_y][cell_x + 1] & 4 == 0
            # check first row, third cell south
            and self.grid[cell_y][cell_x + 2] & 4 == 0
            # check second row, first cell east and south
            and self.grid[cell_y + 1][cell_x] & 2 == 0
            and self.grid[cell_y + 1][cell_x] & 4 == 0
            # check second row, second cell east and south
            and self.grid[cell_y + 1][cell_x + 1] & 2 == 0
            and self.grid[cell_y + 1][cell_x + 1] & 4 == 0
            # check second row, third cell south
            and self.grid[cell_y + 1][cell_x + 2] & 4 == 0
            # check third row, first cell east
            and self.grid[cell_y + 2][cell_x] & 2 == 0
            # check third row, second cell east
            and self.grid[cell_y + 2][cell_x + 1] & 2 == 0
            ):
            return True
        return False

    def fortytwo_deadend(self, wall: tuple[int, int]) -> bool:
        """
        Verifies if dead end is inside the shape of the 2 in the 42 pattern.

        Arguments:
            wall (tuple of ints): Coordinates of cell.
        
        Returns:
            bool: True if dead end belongs to the pattern. False if it doesn't.
        """
        y, x = wall
        if self.blocked[y - 1][x] and self.blocked[y + 1][x]:
            return True
        return False

    def throw_wall(self, wall: tuple[int, int], down: int) -> None:
        """
        Removes walls.

        Arguments:
            wall (tuple of ints): Coordinates of cell.
            down (int): Bit number of the cell wall to remove.
        """
        y, x = wall
        if down == 1:
            self.grid[y][x] &= ~1
            self.grid[y - 1][x] &= ~4
        elif down == 2:
            self.grid[y][x] &= ~2
            self.grid[y][x + 1] &= ~8
        elif down == 4:
            self.grid[y][x] &= ~4
            self.grid[y + 1][x] &= ~1
        elif down == 8:
            self.grid[y][x] &= ~8
            self.grid[y][x - 1] &= ~2

    def preserve_corners(self) -> None:
        """ Removes walls of corners of maze to create open corners. """
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                # check and remove (0,0) east and south walls
                if y == 0 and x == 0:
                    if self.grid[y][x] & 2 > 0:
                        self.grid[y][x] &= ~2
                        self.grid[y][x + 1] &= ~8
                    if self.grid[y][x] & 4 > 0:
                        self.grid[y][x] &= ~4
                        self.grid[y + 1][x] &= ~1
                # check and remove (0, width - 1) south and west walls
                if y == 0 and x == self.width - 1:
                    if self.grid[y][x] & 4 > 0:
                        self.grid[y][x] &= ~4
                        self.grid[y + 1][x] &= ~1
                    if self.grid[y][x] & 8 > 0:
                        self.grid[y][x] &= ~8
                        self.grid[y][x - 1] &= ~2
                # check and remove (height - 1, 0) east and north walls
                if y == self.height - 1 and x == 0:
                    if self.grid[y][x] & 2 > 0:
                        self.grid[y][x] &= ~2
                        self.grid[y][x + 1] &= ~8
                    if self.grid[y][x] & 1 > 0:
                        self.grid[y][x] &= ~1
                        self.grid[y - 1][x] &= ~4
                # check and remove (height - 1, width - 1) north and west walls
                if y == self.height - 1 and x == self.width - 1:
                    if self.grid[y][x] & 1 > 0:
                        self.grid[y][x] &= ~1
                        self.grid[y - 1][x] &= ~4
                    if self.grid[y][x] & 8 > 0:
                        self.grid[y][x] &= ~8
                        self.grid[y][x - 1] &= ~2

    def carve_pacman(self) -> None:
        """ Accounts for all dead ends in maze and removes walls to create connectivity. """
        self.preserve_corners()
        dead_ends: list[tuple[str, tuple[int, int]]] = []
        north: list[int] = [4, 2, 8]
        east: list[int] = [1, 4, 8]
        south: list[int] = [8, 1, 2]
        west: list[int] = [1, 4, 2]
        closed: list[int] = [1, 2, 4, 8]
        # adding all dead ends to list
        for y in range(len(self.grid)):
            for x in range(len(self.grid[0])):
                if self.grid[y][x] in (7, 11, 13, 14, 15):
                    # north check
                    if self.grid[y][x] == 14:
                        dead_ends.append(("north", (y, x)))
                    # east check
                    elif self.grid[y][x] == 13:
                        dead_ends.append(("east", (y, x)))
                    # south check
                    elif self.grid[y][x] == 11:
                        dead_ends.append(("south", (y, x)))
                    # west check
                    elif self.grid[y][x] == 7:
                        dead_ends.append(("west", (y, x)))
                    elif self.grid[y][x] == 15 and not self.blocked[y][x]:
                        dead_ends.append(("closed", (y, x)))
        # for each dead end, verify 3x3 passages and boundaries to down walls
        for wall in dead_ends:
            if not self.three_by_three(wall[1]):
                if (wall[0] == "north" and not self.fortytwo_deadend(
                        wall[1])):
                    down = self.random_generator.choice(north)
                    while not self.verify_boundaries(wall[1], down):
                        down = self.random_generator.choice(north)
                    if self.verify_boundaries(wall[1], down):
                        self.throw_wall(wall[1], down)
                if (wall[0] == "east" and not self.fortytwo_deadend(
                        wall[1])):
                    down = self.random_generator.choice(east)
                    while not self.verify_boundaries(wall[1], down):
                        down = self.random_generator.choice(east)
                    if self.verify_boundaries(wall[1], down):
                        self.throw_wall(wall[1], down)
                if (wall[0] == "south" and not self.fortytwo_deadend(
                        wall[1])):
                    down = self.random_generator.choice(south)
                    while not self.verify_boundaries(wall[1], down):
                        down = self.random_generator.choice(south)
                    if self.verify_boundaries(wall[1], down):
                        self.throw_wall(wall[1], down)
                if (wall[0] == "west" and not self.fortytwo_deadend(
                        wall[1])):
                    down = self.random_generator.choice(west)
                    while not self.verify_boundaries(wall[1], down):
                        down = self.random_generator.choice(west)
                    if self.verify_boundaries(wall[1], down):
                        self.throw_wall(wall[1], down)
                if (wall[0] == "closed" and not self.fortytwo_deadend(
                        wall[1])):
                    down = self.random_generator.choice(closed)
                    while not self.verify_boundaries(wall[1], down):
                        down = self.random_generator.choice(closed)
                    if self.verify_boundaries(wall[1], down):
                        self.throw_wall(wall[1], down)

    def maze_maker(self) -> None:
        """ Employs the maze-creation methods in the order necessary to create the mazes. """
        self.create_grid()
        self.forty_two()
        if self.perfect:
            self.carve_maze()
        else:
            self.carve_maze()
            self.carve_pacman()
