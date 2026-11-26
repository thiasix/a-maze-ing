"""Punto de entrada principal y menú interactivo de A-Maze-ing."""

import sys
from typing import Any
from parcer import load_config
from maze_generator.maze_generator import MazeGenerator
from render import render_ascii
from save_maze import save_maze
from themes import THEMES, THEMES_42
from solve_maze import solve_maze


def create_and_save(
        data: dict[str, Any], theme: dict[str, str]
) -> MazeGenerator:
    """
    Genera un nuevo laberinto, lo guarda en disco y lo dibuja.
    """
    # Vuelve a la posición guardada y limpia desde ahí hacia abajo
    print("\033[u\033[J", end="")
    generator = MazeGenerator(data)
    generator.maze_maker()
    # path = "ESEENEEESSSEESESSESESSSSEEEEEESES"
    show_path = False
    if generator.grid is not None:
        path = solve_maze(generator.grid, data["ENTRY"], data["EXIT"])
        print("\033[s", end="")
        render_ascii(
            generator.grid,
            data["ENTRY"],
            data["EXIT"],
            theme,
            theme, path, show_path)
        save_maze(
            data["OUTPUT_FILE"],
            generator.grid,
            data["ENTRY"],
            data["EXIT"],
            path,
        )
    return generator


def print_menu(theme: dict[str, str]) -> str:
    """
    Muestra el menú interactivo aplicando los colores del tema activo.
    """
    reset = theme["reset"]
    title = theme["title"]
    menu = theme["menu"]
    prompt = theme["prompt"]

    print(f"\n{title}=== A-Maze-ing ==={reset}")
    print(f"{menu}1. Re-generate a new maze")
    print("2. Show / Hide the shortest path")
    print("3. Rotate the wall colours")
    print("4. Color of 42 pattern")
    print(f"5. Quit{reset}")
    # comando para limpiar pantalla
    print("\033[J", end="")
    return input(f"{prompt}Choice? (1-5): {reset}").strip()


def main() -> None:
    """
    Carga la configuración, genera el laberinto y gestiona el menú.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config.txt>")
        return
    # Limpia toda la terminal (pantalla + historial) al arrancar
    print("\033c", end="", flush=True)

    try:
        data = load_config(sys.argv[1])
        theme_idx = 0
        theme_42_idx = 0
        custom_42: dict[str, str] | None = None
        show_path = False
        # Guardamos la posicion del cursor:
        print("\033[s", end="")
        generator = create_and_save(data, THEMES[theme_idx])
        if generator.grid is None:
            return

        while True:
            active_42 = custom_42 or THEMES[theme_idx]
            choice = print_menu(THEMES[theme_idx])
            if choice == "1":
                data["SEED"] = None
                generator = create_and_save(data, THEMES[theme_idx])
            elif choice == "2":
                if show_path is False:
                    show_path = True
                else:
                    show_path = False
                path = solve_maze(generator.grid, data["ENTRY"], data["EXIT"])
                # Devuelve el cursor a las guardadas en "\033[s"
                # y con la j, borrado todo haia arriba.
                print("\033[u\033[J", end="")
                render_ascii(
                    generator.grid,
                    data["ENTRY"],
                    data["EXIT"],
                    THEMES[theme_idx],
                    THEMES[theme_idx], path, show_path
                )
            elif choice == "3":
                theme_idx = (theme_idx + 1) % len(THEMES)
                custom_42 = None
                path = solve_maze(generator.grid, data["ENTRY"], data["EXIT"])
                show_path = True
                print("\033[u\033[J", end="")
                render_ascii(
                    generator.grid,
                    data["ENTRY"],
                    data["EXIT"],
                    THEMES[theme_idx],
                    THEMES[theme_idx], path, show_path
                )
            elif choice == "4":
                custom_42 = THEMES_42[theme_42_idx]
                theme_42_idx = (theme_42_idx + 1) % len(THEMES_42)
                path = solve_maze(generator.grid, data["ENTRY"], data["EXIT"])
                print("\033[u\033[J", end="")
                render_ascii(
                    generator.grid, data["ENTRY"], data["EXIT"],
                    THEMES[theme_idx], custom_42, path, show_path
        )
            elif choice == "5":
                break
            else:
                print(
                    f"{"\033[1;38;5;160m"}Invalid option."
                    f" Please enter a number from 1 to 4.{"\033[0m"}"
                )

    except (OSError, ValueError) as e:
        print(f"{"\033[1;38;5;160m"}Error: {e}{"\033[0m"}")


if __name__ == "__main__":
    main()
