"""
C6 - Evidencia para elegir el algoritmo de ordenamiento del caso de la tienda.

Qué se ordena en la tienda: el catálogo de ~20 000 productos por código, para el
reporte de inventario (1 vez al día, ver hitos/h2/inventario.md) y, si se usara
búsqueda binaria, para dejar la lista lista antes de buscar (C4).

Como no sé en qué estado llega el catálogo, pruebo 5 formas posibles de los datos
con n = 20 000 (el tamaño real):

  aleatorio          recién importado de proveedores, sin orden
  casi ordenado      el catálogo de ayer ya ordenado + 10 productos fuera de lugar
                     (~10 altas al día, H2)
  ordenado           ya viene ordenado por código
  inverso            ordenado al revés
  5 % repetidos      aleatorio, con ~5 % de códigos duplicados (el problema de H1)

Mismos algoritmos y mismo protocolo que C5 (1 calentamiento + 3 repeticiones, promedio).

Ejecutar:  python eleccion.py
"""

import platform
import random
import statistics
import sys
import time

from importlib.machinery import SourceFileLoader

# Reutiliza los algoritmos de C5 para no duplicar código.
torneo = SourceFileLoader("torneo", "../c5/torneo.py").load_module()

SEMILLA = 42
N = 20_000
REPETICIONES = 3


def formas(n):
    base = [f"P{i:06d}" for i in range(1, n + 1)]
    rnd = random.Random(SEMILLA)

    aleatorio = base[:]
    rnd.shuffle(aleatorio)

    fuera = set(rnd.sample(range(n), 10))                     # 10 productos fuera de lugar
    casi = [c for i, c in enumerate(base) if i not in fuera] + [base[i] for i in sorted(fuera)]

    repetidos = [base[rnd.randrange(int(n * 0.95))] if rnd.random() < 0.05 else c
                 for c in base]
    rnd.shuffle(repetidos)

    return [("aleatorio", aleatorio),
            ("casi ordenado (10 fuera de lugar)", casi),
            ("ordenado", base[:]),
            ("inverso", base[::-1]),
            ("5 % repetidos", repetidos)]


def medir(f, datos):
    f(datos)                                                  # calentamiento
    t = []
    for _ in range(REPETICIONES):
        t0 = time.perf_counter()
        f(datos)
        t.append((time.perf_counter() - t0) * 1000)
    return t


def main():
    print(f"Equipo: Python {platform.python_version()} en {platform.system()} {platform.machine()}")
    print(f"n = {N:,} | Semilla: {SEMILLA} | Protocolo: 1 calentamiento + {REPETICIONES} repeticiones, promedio\n")

    algoritmos = torneo.ALGORITMOS
    nombres = [a for a, _ in algoritmos]
    print("Tiempo en ms (promedio; entre paréntesis, el ruido):\n")
    print("| Forma de los datos | " + " | ".join(nombres) + " |")
    print("|---|" + "---|" * len(nombres))
    for etiqueta, datos in formas(N):
        esperado = sorted(datos)
        celdas = []
        for nombre, f in algoritmos:
            assert f(datos) == esperado, f"{nombre} falla en {etiqueta}"
            t = medir(f, datos)
            celdas.append(f"{statistics.mean(t):,.1f} ({(max(t) - min(t)) / statistics.mean(t) * 100:.0f} %)")
        print(f"| {etiqueta} | " + " | ".join(celdas) + " |", flush=True)
        print(f"  {etiqueta} listo", file=sys.stderr, flush=True)


if __name__ == "__main__":
    main()
