*This project has been created as part of the 42 curriculum by <patperez>, <francysa>.*

<h1 align="center"> A-MAZE-ING </h1>

## Descripcion

## Instrucciones

## Recursos

* [Documentacion oficial de python](#Título)
* [Manual Oficial de GNU Make](#recursos:https://www.gnu.org/software/make/manual/make.html)
* [Para los colores](https://python-para-impacientes.blogspot.com/2016/09/dar-color-las-salidas-en-la-consola.html)
	https://xterm.codes/?utm_source=chatgpt.com&syntax=octal&lang=python
	

## Segunda Parte 

* La estructura y el formato completos de su archivo de configuración.:

El archivo de configuración utiliza el formato `CLAVE=VALOR` (una pareja por línea). Las líneas en blanco y las líneas que comienzan con `#` se consideran comentarios y son ignoradas.

| Clave | Obligatoria | Tipo | Descripción y reglas de validación |
| :--- | :---: | :--- | :--- |
| **`WIDTH`** | Sí | `int` | Ancho del laberinto en celdas. Debe ser mayor o igual que 1 o menor o igual a 50. |
| **`HEIGHT`** | Sí | `int` | Alto del laberinto en celdas. Debe ser mayor o igual que 1 o menor o igual a 50. |
| **`ENTRY`** | Sí | `x,y` | Coordenadas de entrada dentro de los límites. No puede coincidir con `EXIT`. |
| **`EXIT`** | Sí | `x,y` | Coordenadas de salida dentro de los límites. Debe ser distinta de `ENTRY`. |
| **`OUTPUT_FILE`** | Sí | `str` | Ruta o nombre del archivo donde se guardará el laberinto en hexadecimal. No puede estar vacío. |
| **`PERFECT`** | Sí | `bool` | Modo de generación (`True`: camino único sin bucles; `False`: tablero jugable estilo Pac-Man con múltiples rutas). Solo admite `True` o `False`. |
| **`SEED`** | No | `int` | Semilla entera para reproducir exactamente la misma generación aleatoria. Si se omite, se genera de forma aleatoria. |

El programa verifica que estén todas las claves obligatorias, rechaza claves duplicadas o desconocidas y valida que todos los valores estén dentro de los rangos permitidos.


• El algoritmo de generación de laberintos que elegiste.

• Por qué elegiste este algoritmo

• ¿Qué parte de tu código es reutilizable y cómo?

• Su equipo y gestión de proyectos con:

	* Las funciones de cada miembro del equipo
| Funcioón     | Miembro       | ¿que hace?   |
|:------------:|:-------------:|:------------:|
| Dato 1       | Dato 2        | Dato 3       |
| Dato 4       | Dato 5        | Dato 6       |

	* Su planificación prevista y cómo evolucionó hasta el final.
	* Qué funcionó bien y qué se podría mejorar
	* ¿Has utilizado alguna herramienta específica? ¿Cuáles?
	* Si implementa funciones avanzadas (múltiples algoritmos, opciones de visualización), descríbalas en este archivo README.md.

## Licencia

Este proyecto cuenta con licencia conforme a los terminos de la licencia --MIT--.Consulte el archivo LICENSE para conocer los derechos y limitaciones de la licencia.