#!/usr/bin/env python3


def get_path_coords(
        entry: tuple[int, int], path: str
) -> set[tuple[int, int]]:
    """
    Convierte una ruta de direcciones ('N', 'E', 'S', 'O') en coordenadas.
    """
    x, y = entry
    coords: set[tuple[int, int]] = set()
    for step in path.upper():
        if step == "N":
            y -= 1
        elif step == "S":
            y += 1
        elif step == "E":
            x += 1
        elif step == "W":
            x -= 1
        coords.add((x, y))
    return coords


def render_ascii(
        grid: list[list[int]],
        entry: tuple[int, int],
        exit_post: tuple[int, int],
        theme: dict[str, str],
        theme_42: dict[str, str],
        path: str = "",
        show_path: bool = False) -> None:
    """Dibuja el laberinto en la terminal usando caracteres ASCII.

    Recorre la matriz de máscaras de bits fila por fila, mostrando las
    paredes externas e internas junto con la entrada y la salida.

    Args:
        grid: Matriz bidimensional con los valores enteros de las paredes.
        entry: Coordenadas (x, y) de la entrada del laberinto.
        exit_post: Coordenadas (x, y) de la salida del laberinto.
    """
    color = theme["wall"]
    entry_sq = theme["entry"]
    exit_sq = theme["exit"]
    reset = theme["reset"]
    block_color = theme_42["block_42"]
    fund_color = theme["fund"]
    path_theme = theme["path"]
    fund_42 = theme_42["fund_42"]

    # coordenadas del camino
    path_coords = get_path_coords(entry, path) if show_path else set()
    # ruta completa
    route_nodes = path_coords | {entry, exit_post} if show_path else set()
    # mantiene la parte superior el laberinto cada vez que pinta

    for y, row in enumerate(grid):
        top_line = ""
        mid_line = ""
        for x, cell in enumerate(row):
            # nos aseguramos de definir las celdas
            is_42 = (cell == 15)
            top_42 = (y > 0 and grid[y - 1][x] == 15)
            left_42 = (x > 0 and grid[y][x - 1] == 15)
            diag_42 = (x > 0 and y > 0 and grid[y - 1][x - 1] == 15)
            c_corner = (
                block_color
                if (is_42 or top_42 or left_42 or diag_42)
                else color)
            c_north = block_color if (is_42 or top_42) else color
            c_west = block_color if (is_42 or left_42) else color

            # empezamos a acumular los colores que formaran el norte
            top_line += c_corner + "  " + reset
            if cell & 1:
                top_line += c_north + "  " + reset
            # miramos si esta en el camino
            elif show_path and (
                x, y) in route_nodes and (
                    x, y - 1) in route_nodes:
                top_line += path_theme + "  " + reset
            else:
                top_line += fund_color + "  " + reset
            # hacemos lo mismo con el lado
            if cell & 8:
                mid_line += c_west + "  " + reset
            elif show_path and (
                x, y) in route_nodes and (
                    x - 1, y) in route_nodes:
                mid_line += path_theme + "  " + reset
            else:
                mid_line += fund_color + "  " + reset

            # miramos los bloques, entrada y salida y camino
            if is_42:
                mid_line += fund_42 + "  " + reset
            elif (x, y) == entry:
                mid_line += entry_sq + "  " + reset
            elif (x, y) == exit_post:
                mid_line += exit_sq + "  " + reset
            elif (x, y) in path_coords:
                mid_line += path_theme + "  " + reset
            else:
                mid_line += fund_color + "  " + reset
        top_line += color + "  " + reset
        if row[-1] & 2:
            mid_line += color + "  " + reset
        else:
            mid_line += fund_color + "  " + reset
        print(top_line)
        print(mid_line)

    # añadimos el cierre de abajo y el lateral
    bottom_line = ""
    for cell in grid[-1]:
        bottom_line += color + "  " + reset
        if cell & 4:
            bottom_line += color + "  " + reset
        else:
            bottom_line += fund_color + "  " + reset
    bottom_line += color + "  " + reset
    print(bottom_line)
