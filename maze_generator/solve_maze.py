def solve_maze(
        grid: list[list[int]],
        entry: tuple[int, int],
        exit_pos: tuple[int, int]
) -> str:
    """
    Solucion del laberinto, busca siguiendo el patron de algoritmos BFS
    para encontrar el camino mas corto entre ENTRY y EXIT.

    Retorna un string con el camino desde la entrada a la salida.
    """
    # lista de espera
    queue: list[tuple[int, int]] = [entry]
    # para no repetir casillas
    visited: set[tuple[int, int]] = {entry}
    # rastro del camino
    came_from: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}

    while queue:
        # nos aseguramos de listar en cola con pop
        # (en 0 lo que hace es mandarnos siempre el primero)
        current = queue.pop(0)
        if current == exit_pos:
            break
        x, y = current
        cell = grid[y][x]
        # comprobar norte
        if not (cell & 1):
            neighbor = (x, y - 1)
            if neighbor not in visited:
                came_from[neighbor] = (current, "N")
                visited.add(neighbor)
                queue.append(neighbor)

        # comprobar este
        if not (cell & 2):
            neighbor = (x + 1, y)
            if neighbor not in visited:
                came_from[neighbor] = (current, "E")
                visited.add(neighbor)
                queue.append(neighbor)

        # comprobar el Sur
        if not (cell & 4):
            neighbor = (x, y + 1)
            if neighbor not in visited:
                came_from[neighbor] = (current, "S")
                visited.add(neighbor)
                queue.append(neighbor)

        # comprobar Oeste
        if not (cell & 8):
            neighbor = (x - 1, y)
            if neighbor not in visited:
                came_from[neighbor] = (current, "W")
                visited.add(neighbor)
                queue.append(neighbor)

    # captura los caminos imposibles y si Entry o Exit estan en 42
    if exit_pos not in came_from and exit_pos != entry:
        raise ValueError("The entry or exit has landed on block 42,\n"
                         "  Try another <ENTRY> or <EXIT>")
    # cogemos con una variable nueva la salida
    # y vamos recorriendo de la salida, a la entrada
    curr = exit_pos
    steps: list[str] = []
    while curr != entry:
        prev_cell, letter = came_from[curr]
        steps.append(letter)
        curr = prev_cell
    # cambiamos el orden de las letras
    steps.reverse()
    # retornamos el string
    path = "".join(steps)
    return path
