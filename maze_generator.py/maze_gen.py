import random
from typing import Any


class MazeGenerator:
    def __init__(self, config: dict[str, Any]) -> None:
        self.height: int = config["HEIGHT"]
        self.width: int = config["WIDTH"]
        self.seed: int | None = config.get("SEED", None)
        self.grid = None
        self.visited = None
        self.entry: tuple[int, int] = config["ENTRY"]
        self.exit: tuple[int, int] = config["EXIT"]
        self.perfect: bool = config.get("PERFECT", False)
        self.output_file = config["OUTPUT_FILE"]
        self.random_generator = random.Random(self.seed)

    def create_grid(self) -> tuple[list[list[int]], list[list[bool]]]:
        self.grid = []
        self.visited = []
        for y in range(self.height):
            row = []
            visit_row = []
            for x in range(self.width):
                row.append(15)
                visit_row.append(False)
            self.grid.append(row)
            self.visited.append(visit_row)
        return self.grid, self.visited

    def forty_two(self) -> None:
        pattern = [["42", "--", "--", "--", "42", "42", "42"],
                   ["42", "--", "--", "--", "--", "--", "42"],
                   ["42", "42", "42", "--", "42", "42", "42"],
                   ["--", "--", "42", "--", "42", "--", "--"],
                   ["--", "--", "42", "--", "42", "42", "42"]]
        if self.height > 7 and self.width > 9:
            centre_height = (self.height - 7) // 2
            centre_width = (self.width - 9) // 2
            for y in range(len(pattern)):
                for x in range(len(pattern[0])):
                    current = pattern[y][x]
                    if current == "42":
                        maze_y = centre_height + y
                        maze_x = centre_width + x
                        self.visited[maze_y][maze_x] = True
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
            if self.visited[entry_y][entry_x]:
                valid = False
            if self.visited[exit_y][exit_x]:
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
            if curr_y > 0 and not self.visited[curr_y - 1][curr_x]:
                neighbours.append((curr_y - 1, curr_x, 1))
            # check SOUTHERN neighbour
            if curr_y < (len(self.grid) - 1) and not self.visited[curr_y + 1][curr_x]:
                neighbours.append((curr_y + 1, curr_x, 4))
            # check EASTERN neighbour
            if curr_x < (len(self.grid[0]) - 1) and not self.visited[curr_y][curr_x + 1]:
                neighbours.append((curr_y, curr_x + 1, 2))
            # check WESTERN neighbour
            if curr_x > 0 and not self.visited[curr_y][curr_x - 1]:
                neighbours.append((curr_y, curr_x - 1, 8))
            if not neighbours:
                been_here_stack.pop()
            else:
                step = self.random_generator.choice(neighbours)
                step_y, step_x, direc = step
                been_here_stack.append((step_y, step_x))
                self.visited[step_y][step_x] = True
                if direc == 1:
                    self.grid[curr_y][curr_x] &= ~1
                    self.grid[step_y][step_x] &= ~4
                elif direc == 4:
                    self.grid[curr_y][curr_x] &= ~4
                    self.grid[step_y][step_x] &= ~1
                elif direc == 2:
                    self.grid[curr_y][curr_x] &= ~2
                    self.grid[step_y][step_x] &= ~8
                elif direc == 8:
                    self.grid[curr_y][curr_x] &= ~8
                    self.grid[step_y][step_x] &= ~2

    def carve_pacman():
        for y in self.grid:
            for x in self.grid:
                if cell[y][x] == 14:
                    if 

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
                self.carve_pacman()
