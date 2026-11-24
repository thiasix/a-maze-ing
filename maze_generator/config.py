"""
Lectura, validación y conversión de la configuración del laberinto.
"""
from typing import Any


def parse_values(data: dict[str, str]) -> dict[str, Any]:  # convierte datos
    """
    Convierte y valida los tipos de datos de la configuración.

    Args:
        data: Diccionario con las claves y valores crudos en texto.

    Returns:
        Diccionario con los valores convertidos a sus tipos finales.

    Raises:
        ValueError: Si algún valor está fuera de rango o mal formateado.
    """
    new_data: dict[str, Any] = {}
    for key in ("WIDTH", "HEIGHT"):
        size = int(data[key])
        if size < 2 or size > 50:
            raise ValueError(f"{key} must be greater that 0 and less than 50")
        new_data[key] = size
    for key in ("ENTRY", "EXIT"):
        coor = data[key].split(",")
        if len(coor) != 2:
            raise ValueError(f"{key} must have format x,y")
        x = int(coor[0].strip())
        y = int(coor[1].strip())

        width = new_data["WIDTH"]
        height = new_data["HEIGHT"]
        if x < 0 or x >= width:
            raise ValueError(f"{key} coordinates ({x}, {y}) are out of bounds")
        if y < 0 or y >= height:
            raise ValueError(f"{key} coordinates ({x}, {y}) are out of bounds")
        new_data[key] = (x, y)
    if new_data["ENTRY"] == new_data["EXIT"]:
        raise ValueError("ENTRY and EXIT cannot be the same cell")
    if data["PERFECT"] == "True":
        new_data["PERFECT"] = True
    elif data["PERFECT"] == "False":
        new_data["PERFECT"] = False
    else:
        raise ValueError("PERFECT must be 'True' or 'False'")
    if not data["OUTPUT_FILE"]:
        raise ValueError("OUTPUT_FILE cannot be empty")
    new_data["OUTPUT_FILE"] = data["OUTPUT_FILE"]

    if "SEED" in data:  # semilla que puede ser opcional
        new_data["SEED"] = int(data["SEED"])

    # print(new_data)
    return new_data


# validamos con un set las claves que esten sean correctos
def validate_keys(data: dict[str, str]) -> None:
    """
    Comprueba que existan las claves obligatorias y no haya desconocidas.

    Args:
        data: Diccionario con las claves extraídas del archivo.

    Raises:
        ValueError: Si falta alguna clave obligatoria o hay claves no válidas.
    """
    keys = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}
    optional_key = {"SEED"}
    allowed_keys = keys | optional_key  # Unimos
    received_key = set(data.keys())
    missing = keys - received_key  # miramos cual falta y cual sobra
    if missing:
        raise ValueError(
            f"Required key missing: {missing}\n"
            "Go to your file: <config.txt>")
    unknown = received_key - allowed_keys
    if unknown:
        raise ValueError(f"Invaid Keys: {unknown}")


def load_config(program: str) -> dict[str, Any]:
    """
    Lee, valida y carga los parámetros desde un archivo de configuración.

    Args:
        program: Ruta o nombre del archivo de configuración a leer.

    Returns:
        Diccionario con todos los parámetros validados y tipados.

    Raises:
        ValueError: Si hay errores de sintaxis, claves duplicadas o inválidas.
    """
    data: dict[str, str] = {}
    with open(program, "r") as file:
        for line in file:
            line = line.strip()
            if len(line) > 0:
                if line[0] == "#":
                    continue
            else:
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                clean_key = key.strip()
                if clean_key in data:
                    raise ValueError(f"Duplicate key: '{clean_key}'")
                data[key.strip()] = value.strip()
            else:
                raise ValueError(
                    "Syntax error, correct your file <config.txt>")
        validate_keys(data)
        config = parse_values(data)
        # print("es valida")
        # print(config)
    return config
