#!/usr/bin/env python3

def save_maze(
        program: str, grid: list[list[int]],
        entry: tuple[int, int], exit_post: tuple[int, int],
        path: str) -> None:
    """
    Saves the grid of the maze, the coordinates, and the resolution path
    in a .txt file.

    Arguments:
        program: Path of the output file in which the maze is stored.

        grid: Matriz bidimensional de enteros que representan las paredes.
        entry: Coordenadas iniciales (x,y) en el laberinto.
        exit_post: Coordenadas finales (x,y) en el laberinto.
        path: Secuencia de cadenas de caracteres con las direcciones
        cardinales para la solución.
    """
    with open(program, "w") as file:
        for grow in grid:
            tex = ""
            for value in grow:
                tex += f"{value:x}"
            file.write(f"{tex}\n")
        file.write("\n")
        e_x, e_y = entry
        p_x, p_y = exit_post
        file.write(f"{e_x},{e_y}\n")
        file.write(f"{p_x},{p_y}\n")
        pat = path.upper()
        pat = pat.strip()
        file.write(f"{pat}\n")

