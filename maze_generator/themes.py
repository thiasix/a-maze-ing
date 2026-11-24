
RESET = "\033[0m"

CL_GRAY = "\033[48;5;239m"
CL_WHITE = "\033[48;5;15m"
CL_FUCHSIA = "\033[48;5;198m"
CL_GREEN = "\033[48;5;28m"
CL_RED = "\033[48;5;160m"
CL_BLACK = "\033[48;5;233m"
CL_DARK_GRAY = "\033[48;5;240m"
CL_DARK_RED = "\033[48;5;88m"
CL_LIGHT_RED = "\033[48;5;9m"
CL_WINE_RED = "\033[48;5;52m"
L_WHITE_FU = "\033[1;38;5;198;48;5;15m"
L_WHITE_GREY = "\033[1;38;5;52;48;5;15m"
L_WHITE_RED = "\033[1;38;5;245;48;5;15m"
L_WHITE = "\033[1;38;5;15m"
L_PINK = "\033[1;38;5;219m"
L_GRAY = "\033[1;38;5;253m"
L_RED = "\033[1;38;5;196m"
PATH_PINK = "\033[1;48;5;212m"
PATH_DARCK = "\033[1;48;5;146m"
PATH_RED = "\033[48;5;230m"


THEMES: list[dict[str, str]] = [
    {
        "name": "Pinck (gray and pink)",
        "title": L_WHITE_FU,
        "menu": L_WHITE,
        "prompt": L_PINK,
        "wall": CL_GRAY,
        "block_42": CL_FUCHSIA,
        "entry": CL_GREEN,
        "exit": CL_RED,
        "path": PATH_PINK,
        "reset": RESET,
        "fund": CL_WHITE,
    },
    {
        "name": "Darck (black and white)",
        "title": L_WHITE_RED,
        "menu": L_WHITE,
        "prompt": L_GRAY,
        "wall": CL_WHITE,
        "block_42": CL_DARK_GRAY,
        "entry": CL_GREEN,
        "exit": CL_RED,
        "path": PATH_DARCK,
        "reset": RESET,
        "fund": CL_BLACK,
    },
    {
        "name": "RED",
        "title": L_WHITE_GREY,
        "menu": L_WHITE,
        "prompt": L_RED,
        "wall": CL_DARK_RED,
        "block_42": CL_WINE_RED,
        "entry": CL_GREEN,
        "exit": CL_RED,
        "path": PATH_RED,
        "reset": RESET,
        "fund": CL_LIGHT_RED,
    },
]
