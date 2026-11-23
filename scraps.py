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
        if direction == 1:
            starting_y = [cell_y - 2, cell_y - 1]
            starting_x = [cell_x - 2, cell_x - 1, cell_x]
        elif direction == 4:
            starting_y = [cell_y - 1, cell_y]
            starting_x = [cell_x - 2, cell_x - 1, cell_x]
        elif direction == 2:
            starting_x = [cell_x - 1, cell_x]
            starting_y = [cell_y - 2, cell_y - 1, cell_y]
        elif direction == 8:
            starting_x = [cell_x - 2, cell_x - 1]
            starting_y = [cell_y - 2, cell_y - 1, cell_y]
        for y_check in starting_y:
            for x_check in starting_x:
                window_y = y_check
                window_x = x_check
                if window_y not in range(self.height - 2) or window_x not in range(self.width - 2):
                    continue
                else:
                    window_open: bool = True
                    for y in range(window_y, window_y + 3):
                        for x in range(window_x, window_x + 2):
                            if (y == cell_y and x == min(cell_x, neighbour_x) and window_x <= min(cell_x, neighbour_x) <= window_x + 1 and direction in (2, 8)):
                                pass
                            elif self.grid[y][x] & 2 and self.grid[y][x + 1] & 8:
                                window_open = False
                        if not window_open:
                            break
                    if window_open:
                        for x in range(window_x, window_x + 3):
                            for y in range(window_y, window_y + 2):
                                if (x == cell_x and y == min(cell_y, neighbour_y) and window_y <= min(cell_y, neighbour_y) <= window_y + 1 and direction in (1, 4)):
                                    pass
                                elif self.grid[y][x] & 4 and self.grid[y + 1][x] & 1:
                                    window_open = False
                            if not window_open:
                                break
                        if window_open:
                            return False
        return True