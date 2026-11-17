#!/usr/bin/env python3

import random

""" CELL = 15
NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

opposite = {NORTH: SOUTH,
            EAST: WEST,
            SOUTH: NORTH,
            WEST: EAST} """

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
    entry_y, entry_x = entry
    been_here_stack: list[tuple[int, int]] = []
    been_here_stack.append((entry_x, entry_y))
    visited[entry_y][entry_x] = True
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            neighbours: list[tuple[int, int, int]] = []
            # check NORTHERN neighbour
            if y > 0 and not visited[y - 1][x]:
                neighbours.append((x, y - 1, 1))
            # check SOUTHERN neighbour
            if y < (len(grid) - 1) and not visited[y + 1][x]:
                neighbours.append((x, y + 1, 4))
            # check EASTERN neighbour
            if x < (len(grid[0]) - 1) and not visited[y][x + 1]:
                neighbours.append((x + 1, y, 2))
            # check WESTERN neighbour
            if x > 0 and not visited[y][x - 1]:
                neighbours.append((x - 1, y, 8))
            if not neighbours:
                # backtracking
            else:
                random.choice(neighbours)


def draw_grid(grid: list[list]):
    for row in grid:
        print("".join(row))


if __name__ == "__main__":
    width: int = 21
    height: int = 21
    entry: tuple = (0,0)
    exit: tuple = (7,14)
    grid = create_grid(width, height)
    carve_maze(grid, entry, exit)
    draw_grid(grid)
