import random


class MazeGenerator:
    def __init__(
            self, height: int, width: int, seed: int | None = None,
            perfect: bool | None = False
                ) -> None:
        self.height = height
        self.width = width
        self.seed = seed
        self.grid = None
        self.visited = None
        self.entry = None
        self.exit = None
        self.perfect = perfect
        self.random_generator = random.Random(seed)

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
        if self.height > 6 and self.width > 8:
            centre_height = (self.height - 6) // 2
            centre_width = (self.width - 8) // 2
            for y in range(len(pattern)):
                for x in range(len(pattern[0])):
                    current = pattern[y][x]
                    if current == "42":
                        maze_y = centre_height + y
                        maze_x = centre_width + x
                        self.visited[maze_y][maze_x] = True
        else:
            print("The maze is too small to include '42'")

    def entry_exit_valid(self):
        

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
