#!/usr/bin/env python3

import random
from typing import Any


class MazeGenerator:
    def __init__(self, config: dict[str, Any]) -> None:
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

    def entry_exit_valid(self) -> bool:
        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit
        valid = True
        # validating entry and exit coordinates in same cell
        if self.entry == self.exit:
            valid = False
        # validating entry coordinates
        if entry_y < 0 or entry_y > self.height - 1:
            valid = False
        if entry_x < 0 or entry_x > self.width - 1:
            valid = False
        # validating exit coordinates
        if exit_y < 0 or exit_y > self.height - 1:
            valid = False
        if exit_x < 0 or exit_x > self.width - 1:
            valid = False
        # validating entry and exit coordinates in 42 pattern
        if valid:
            if self.blocked[entry_y][entry_x]:
                valid = False
            if self.blocked[exit_y][exit_x]:
                valid = False
        return valid

    def carve_maze(self) -> None:
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

    # 3x3 passage check
    def three_by_three(self, wall: tuple[int, int]) -> bool:
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
        y, x = wall
        if self.blocked[y - 1][x] and self.blocked[y + 1][x]:
            return True
        return False

    def throw_wall(self, wall: tuple[int, int], down: int) -> None:
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
                    down = random.choice(north)
                    while not self.verify_boundaries(wall[1], down):
                        down = random.choice(north)
                    if self.verify_boundaries(wall[1], down):
                        self.throw_wall(wall[1], down)
                if (wall[0] == "east" and not self.fortytwo_deadend(
                        wall[1])):
                    down = random.choice(east)
                    while not self.verify_boundaries(wall[1], down):
                        down = random.choice(east)
                    if self.verify_boundaries(wall[1], down):
                        self.throw_wall(wall[1], down)
                if (wall[0] == "south" and not self.fortytwo_deadend(
                        wall[1])):
                    down = random.choice(south)
                    while not self.verify_boundaries(wall[1], down):
                        down = random.choice(south)
                    if self.verify_boundaries(wall[1], down):
                        self.throw_wall(wall[1], down)
                if (wall[0] == "west" and not self.fortytwo_deadend(
                        wall[1])):
                    down = random.choice(west)
                    while not self.verify_boundaries(wall[1], down):
                        down = random.choice(west)
                    if self.verify_boundaries(wall[1], down):
                        self.throw_wall(wall[1], down)
                if (wall[0] == "closed" and not self.fortytwo_deadend(
                        wall[1])):
                    down = random.choice(closed)
                    while not self.verify_boundaries(wall[1], down):
                        down = random.choice(closed)
                    if self.verify_boundaries(wall[1], down):
                        self.throw_wall(wall[1], down)

    def maze_maker(self) -> None:
        self.create_grid()
        self.forty_two()
        valid = self.entry_exit_valid()
        if not valid:
            print("Invalid maze creation parameters")
        else:
            if self.perfect:
                self.carve_maze()
            else:
                self.carve_maze()
                self.carve_pacman()

