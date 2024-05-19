import sys
import numpy


def read_file(file_name: str) -> tuple[list[str], list[int], list[int]]:
    personas = []
    w = []
    v = []
    with open(file_name) as file:
        for line in file:
            parsed_line = line.split(",")
            personas.append(str(parsed_line[0]))
            w.append(int(parsed_line[1]))
            v.append(int(parsed_line[2]))
    return personas, w, v


def main(file_name: str, capacidad_max: int, peso_max: int):
    personas, w, v = read_file(file_name)
    n = len(personas)

    opt = numpy.zeros((n + 1, capacidad_max + 1, peso_max + 1), dtype=int)

    for j in range(1, n + 1):
        for p in range(1, capacidad_max + 1):
            for k in range(1, peso_max + 1):
                included = (v[j - 1] + opt[j - 1][p - 1][k - w[j - 1]]) if w[j - 1] <= k else 0
                excluded = opt[j - 1][p][k]

                opt[j][p][k] = max(int(included), int(excluded))

    pasajeros = []
    for j in range(n, 0, -1):
        if opt[j][capacidad_max][peso_max] != opt[j - 1][capacidad_max][peso_max]:
            pasajero = (personas[j - 1], v[j - 1], w[j - 1])
            pasajeros.append(pasajero)
            capacidad_max -= 1
            peso_max -= w[j - 1]

    print("Pasajeros:", ", ".join(p[0] for p in pasajeros))
    print("Peso total:", " + ".join(str(p[2]) for p in pasajeros), "=", sum(p[2] for p in pasajeros))
    print("Ganancia total:", " + ".join(str(p[1]) for p in pasajeros), "=", sum(p[1] for p in pasajeros))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python mision.py [personas] [capacidad] [peso]")
    else:
        main(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
