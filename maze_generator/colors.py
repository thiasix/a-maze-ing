#!/usr/bin/env python3

for i in range(256):
    # Imprime el bloque de color con su número encima
    print(f"\033[48;5;{i}m {i:3d} \033[0m", end="")
    # Salto de línea para ordenar los bloques visualmente
    if i == 15 or (i > 15 and (i - 15) % 12 == 0):
        print()

print("\033[1;38;5;198;48;5;15m" "Holi" "\033[0m")
print("\033[1;38;5;52;48;5;15m" "Holi" "\033[0m")
print("\033[1;38;5;245;48;5;15m" "Holi" "\033[0m")

