#!/usr/bin/env python3

def save_maze(
        program: str, grid: list[list[int]],
        entry: tuple[int, int], exit_post: tuple[int, int],
        path: str) -> None:
    """
    Guarda la cuadrícula del laberinto, las coordenadas y
    la ruta de la solucion en un archivo.

    Argumentos:
        program: Ruta de archivo de salida donde se guardará el laberinto.
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
                tex += f"{value:X}"
            file.write(f"{tex}\n")
        file.write("\n")
        e_x, e_y = entry
        p_x, p_y = exit_post
        file.write(f"{e_x},{e_y}\n")
        file.write(f"{p_x},{p_y}\n")
        pat = path.upper()
        pat = pat.strip()
        file.write(f"{pat}\n")


if __name__ == "__main__":
    test_grid = [[9, 3], [12, 6]]
    test_entry = (0, 0)
    test_exit = (1, 1)
    test_path = "ES"
    save_maze("test_maze.txt", test_grid, test_entry, test_exit, test_path)
