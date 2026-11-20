import random
from typing import Any


class MazeGenerator:
    def __init__(self, config: dict[str, Any]) -> None:
        self.height: int = config["HEIGHT"]
        self.width: int = config["WIDTH"]
        self.seed: int | None = config.get("SEED", None)
        self.grid = None
        self.visited = None
        self.blocked = None
        self.entry: tuple[int, int] = config["ENTRY"]
        self.exit: tuple[int, int] = config["EXIT"]
        self.perfect: bool = config.get("PERFECT", False)
        self.output_file = config["OUTPUT_FILE"]
        self.random_generator = random.Random(self.seed)

    def create_grid(self) -> tuple[list[list[int]], list[list[bool]], list[list[bool]]]:
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
            centre_height = (self.height - 7) // 2
            centre_width = (self.width - 9) // 2
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
            if curr_y > 0 and not self.visited[curr_y - 1][curr_x] and not self.blocked[curr_y - 1][curr_x]:
                neighbours.append((curr_y - 1, curr_x, 1))
            # check SOUTHERN neighbour
            if curr_y < (len(self.grid) - 1) and not self.visited[curr_y + 1][curr_x] and not self.blocked[curr_y + 1][curr_x]:
                neighbours.append((curr_y + 1, curr_x, 4))
            # check EASTERN neighbour
            if curr_x < (len(self.grid[0]) - 1) and not self.visited[curr_y][curr_x + 1] and not self.blocked[curr_y][curr_x + 1]:
                neighbours.append((curr_y, curr_x + 1, 2))
            # check WESTERN neighbour
            if curr_x > 0 and not self.visited[curr_y][curr_x - 1] and not self.blocked[curr_y][curr_x - 1]:
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

    def can_remove_wall(self, cell: tuple[int, int], direction: int) -> bool:
        cell_y, cell_x = cell
        neighbour_y = cell_y
        neighbour_x = cell_x
        opp_wall = 0
        # check NORTHERN neighbour
        if direction == 1:
            neighbour_y -= 1
            opp_wall = 4
        # check EASTERN neighbour
        elif direction == 2:
            neighbour_x += 1
            opp_wall = 8
        # check SOUTHERN neighbour
        elif direction == 4:
            neighbour_y += 1
            opp_wall = 1
        # check WESTERN neighbour
        elif direction == 8:
            neighbour_x -= 1
            opp_wall = 2
        # boundary checks
        if neighbour_y < 0 or neighbour_y > self.height - 1:
            return False
        if neighbour_x < 0 or neighbour_x > self.width - 1:
            return False
        # 42 blockage check
        if self.blocked[cell_y][cell_x] or self.blocked[neighbour_y][neighbour_x]:
            return False
        # closed wall check
        if not self.grid[cell_y][cell_x] & direction and not self.grid[neighbour_y][neighbour_x] & opp_wall:
            return False
        # 3x3 passage check
        for row in range(self.height - 2):
            if not self.grid[row][cell_x] & 2 and not self.grid[row][cell_x + 1] & 2
                and not self.grid[row + 1][cell_x] & 4:
                return False

    def carve_pacman(self):
        pass

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
