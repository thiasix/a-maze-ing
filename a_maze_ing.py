"""Punto de entrada principal y menú interactivo de A-Maze-ing."""

import sys
from typing import Any
from config import load_config
from maze_generator.maze_generator import MazeGenerator
from render import render_ascii
from output import save_maze
from themes import THEMES
from solve_maze import solve_maze


def create_and_save(
        data: dict[str, Any], theme: dict[str, str]
        ) -> MazeGenerator:
    """
    Genera un nuevo laberinto, lo guarda en disco y lo dibuja.
    """
    generator = MazeGenerator(data)
    generator.maze_maker()
    # path = "ESEENEEESSSEESESSESESSSSEEEEEESES"
    show_path = True
    if generator.grid is not None:
        path = solve_maze(generator.grid, data["ENTRY"], data["EXIT"])
        render_ascii(
            generator.grid,
            data["ENTRY"],
            data["EXIT"],
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
    print(f"4. Quit{reset}")
    print("\033[J")  # comando para limpiar pantalla
    return input(f"{prompt}Choice? (1-4): {reset}").strip()


def main() -> None:
    """
    Carga la configuración, genera el laberinto y gestiona el menú.
    """
    try:
        if len(sys.argv) != 2:
            print("Usage: python3 a_maze_ing.py <config.txt>")
            return
        data = load_config(sys.argv[1])
        theme_idx = 0
        show_path = True
        # 33[2J borra toda la pantalla actua,
        # H mueve el cursor a la esquina superior izquierda
        # y end" evita los saltos de linea extras
        print("\033[2J\033[H", end="")
        generator = create_and_save(data, THEMES[theme_idx])
        if generator.grid is None:
            return

        while True:
            choice = print_menu(THEMES[theme_idx])
            if choice == "1":
                generator = create_and_save(data, THEMES[theme_idx])
            elif choice == "2":
                if show_path is True:
                    show_path = False
                else:
                    show_path = True
                path = solve_maze(generator.grid, data["ENTRY"], data["EXIT"])
                render_ascii(
                    generator.grid,
                    data["ENTRY"],
                    data["EXIT"],
                    THEMES[theme_idx], path, show_path
                )
            elif choice == "3":
                theme_idx = (theme_idx + 1) % len(THEMES)
                path = solve_maze(generator.grid, data["ENTRY"], data["EXIT"])
                show_path = True
                render_ascii(
                    generator.grid,
                    data["ENTRY"],
                    data["EXIT"],
                    THEMES[theme_idx], path, show_path
                )
            elif choice == "4":
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
