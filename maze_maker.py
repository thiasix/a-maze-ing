#!/usr/bin/env python3

import random


def create_grid(width: int, height: int) -> tuple[list[list[int]], list[list[bool]]]:
    grid = []
    visited = []
    for y in range(height):
        row = []
        visit_row = []
        for x in range(width):
            row.append(15)
            visit_row.append(False)
        grid.append(row)
        visited.append(visit_row)
    return grid, visited


def carve_maze(
        maze: tuple[list[list[int]], list[list[bool]]],
        entry: tuple[int, int], exit: tuple[int, int]):
    grid, visited = maze
    entry_x, entry_y = entry
    been_here_stack: list[tuple[int, int]] = []
    been_here_stack.append((entry_y, entry_x))
    visited[entry_y][entry_x] = True
    while been_here_stack:
        current_cell = been_here_stack[-1]
        curr_y, curr_x = current_cell
        neighbours: list[tuple[int, int, int]] = []
        # check NORTHERN neighbour
        if curr_y > 0 and not visited[curr_y - 1][curr_x]:
            neighbours.append((curr_y - 1, curr_x, 1))
        # check SOUTHERN neighbour
        if curr_y < (len(grid) - 1) and not visited[curr_y + 1][curr_x]:
            neighbours.append((curr_y + 1, curr_x, 4))
        # check EASTERN neighbour
        if curr_x < (len(grid[0]) - 1) and not visited[curr_y][curr_x + 1]:
            neighbours.append((curr_y, curr_x + 1, 2))
        # check WESTERN neighbour
        if curr_x > 0 and not visited[curr_y][curr_x - 1]:
            neighbours.append((curr_y, curr_x - 1, 8))
        if not neighbours:
            been_here_stack.pop()
        else:
            step = random.choice(neighbours)
            step_y, step_x, direc = step
            been_here_stack.append((step_y, step_x))
            visited[step_y][step_x] = True
            if direc == 1:
                grid[curr_y][curr_x] &= ~1
                grid[step_y][step_x] &= ~4
            elif direc == 4:
                grid[curr_y][curr_x] &= ~4
                grid[step_y][step_x] &= ~1
            elif direc == 2:
                grid[curr_y][curr_x] &= ~2
                grid[step_y][step_x] &= ~8
            elif direc == 8:
                grid[curr_y][curr_x] &= ~8
                grid[step_y][step_x] &= ~2
    counter = 0
    for cell_y in range(len(visited)):
        for cell_x in range(len(visited[0])):
            if visited[cell_y][cell_x] == True:
                counter += 1
    print(counter)
    return grid, visited

        
""" def draw_grid(grid: list[list]):
    for row in grid:
        print("".join(row)) """


if __name__ == "__main__":
    width: int = 5
    height: int = 5
    entry: tuple = (0,0)
    exit: tuple = (7,14)
    grid = create_grid(width, height)
    carve_maze(grid, entry, exit)
    #draw_grid(grid)
