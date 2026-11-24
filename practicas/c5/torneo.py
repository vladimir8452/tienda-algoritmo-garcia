"""
C5 - Torneo de ordenamientos con los códigos de producto de la tienda.

Participantes (todos escritos a mano, salvo la referencia):
  Inserción   cuadrático O(n²)            (el "lento")
  MergeSort   O(n log n) siempre, usa memoria extra
  QuickSort   O(n log n) promedio, O(n²) en el peor caso; aquí con pivote al azar
              y partición en 3 vías (por los códigos repetidos del catálogo)
  sorted()    referencia: el Timsort que trae Python (en C); NO compite, solo orienta

Datos: códigos "P000001"... mezclados al azar con semilla fija (42), como un catálogo
recién importado sin orden. Cada algoritmo recibe una COPIA de la misma lista.

Protocolo (igual que H2): 1 corrida de calentamiento (no se mide) + 3 repeticiones
medidas con time.perf_counter(); se reporta el promedio.

Ejecutar:  python torneo.py
"""

import platform
import random
import statistics
import sys
import time

SEMILLA = 42
TAMANOS = [2_500, 5_000, 10_000, 20_000]       # se duplican; 20 000 = catálogo real
REPETICIONES = 3

sys.setrecursionlimit(10_000)


def insercion(datos):
    a = list(datos)
    for i in range(1, len(a)):
        actual = a[i]
        j = i - 1
        while j >= 0 and a[j] > actual:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = actual
    return a


def mergesort(datos):
    if len(datos) <= 1:
        return list(datos)
    medio = len(datos) // 2
    izq = mergesort(datos[:medio])
    der = mergesort(datos[medio:])
    mezcla = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:                    # <= mantiene el orden de los iguales (estable)
            mezcla.append(izq[i]); i += 1
        else:
            mezcla.append(der[j]); j += 1
    mezcla.extend(izq[i:])
    mezcla.extend(der[j:])
    return mezcla


def quicksort(datos, rnd=random.Random(SEMILLA)):
    a = list(datos)
    _quick(a, 0, len(a) - 1, rnd)
    return a


def _quick(a, bajo, alto, rnd):
    while bajo < alto:
        pivote = a[rnd.randint(bajo, alto)]
        # Partición en 3 vías: [< pivote | == pivote | > pivote]
        lt, i, gt = bajo, bajo, alto
        while i <= gt:
            if a[i] < pivote:
                a[lt], a[i] = a[i], a[lt]; lt += 1; i += 1
            elif a[i] > pivote:
                a[i], a[gt] = a[gt], a[i]; gt -= 1
            else:
                i += 1
        # Recursión sobre el lado más chico, bucle sobre el grande (pila acotada).
        if lt - bajo < alto - gt:
            _quick(a, bajo, lt - 1, rnd); bajo = gt + 1
        else:
            _quick(a, gt + 1, alto, rnd); alto = lt - 1


ALGORITMOS = [("Inserción", insercion), ("MergeSort", mergesort),
              ("QuickSort", quicksort), ("sorted() de Python", sorted)]


def medir(accion):
    accion()                                     # calentamiento, no se mide
    tiempos = []
    for _ in range(REPETICIONES):
        t0 = time.perf_counter()
        accion()
        tiempos.append((time.perf_counter() - t0) * 1000)
    return tiempos


def ruido(t):
    return (max(t) - min(t)) / statistics.mean(t) * 100


def main():
    print(f"Equipo: Python {platform.python_version()} en {platform.system()} {platform.machine()}")
    print(f"Semilla: {SEMILLA} | Protocolo: 1 calentamiento + {REPETICIONES} repeticiones, promedio\n")

    resultados = {}                              # (nombre, n) -> (promedio, ruido, tiempos)
    for n in TAMANOS:
        rnd = random.Random(SEMILLA)
        datos = [f"P{i:06d}" for i in range(1, n + 1)]
        rnd.shuffle(datos)
        esperado = sorted(datos)
        for nombre, f in ALGORITMOS:
            assert f(datos) == esperado, f"{nombre} no ordena bien (n={n})"
            t = medir(lambda: f(datos))
            resultados[(nombre, n)] = (statistics.mean(t), ruido(t), t)
        print(f"  n = {n:,} listo", file=sys.stderr, flush=True)

    nombres = [a for a, _ in ALGORITMOS]
    print("Tiempo en ms (promedio de 3 repeticiones; entre paréntesis, el ruido):\n")
    print("| n | " + " | ".join(nombres) + " |")
    print("|---|" + "---|" * len(nombres))
    for n in TAMANOS:
        celdas = []
        for nom in nombres:
            m, r, _ = resultados[(nom, n)]
            celdas.append(f"{m:,.1f} ({r:.0f} %)")
        print(f"| {n:,} | " + " | ".join(celdas) + " |")

    print("\nCuántas veces tarda más al duplicar n (esperado: Inserción ×4; MergeSort y QuickSort un poco más de ×2):")
    print("| n | " + " | ".join(nombres) + " |")
    print("|---|" + "---|" * len(nombres))
    for k, n in enumerate(TAMANOS):
        if k == 0:
            print(f"| {n:,} | " + " | ".join("—" for _ in nombres) + " |")
        else:
            ant = TAMANOS[k - 1]
            print(f"| {n:,} | " + " | ".join(
                f"{resultados[(nom, n)][0] / resultados[(nom, ant)][0]:.2f}" for nom in nombres) + " |")

    print("\nCuántas veces más lento que MergeSort / QuickSort es la Inserción:")
    print("| n | Inserción / MergeSort | Inserción / QuickSort | MergeSort / QuickSort |")
    print("|---|---|---|---|")
    for n in TAMANOS:
        i, m, q = (resultados[(x, n)][0] for x in ("Inserción", "MergeSort", "QuickSort"))
        print(f"| {n:,} | {i / m:.1f} | {i / q:.1f} | {m / q:.2f} |")

    print("\nLas 3 repeticiones de cada celda (ms):")
    print("| n | " + " | ".join(nombres) + " |")
    print("|---|" + "---|" * len(nombres))
    for n in TAMANOS:
        print(f"| {n:,} | " + " | ".join(
            " / ".join(f"{t:,.1f}" for t in resultados[(nom, n)][2]) for nom in nombres) + " |")


if __name__ == "__main__":
    main()
