"""
C4 - Búsqueda lineal vs búsqueda binaria en el caso de la tienda.

Proceso medido: una jornada de ventas = 700 búsquedas de producto por código
(500 ventas + ~200 consultas, ver hitos/h2/inventario.md), a productos que existen.

  Lineal:  recorre la lista sin orden desde el inicio          -> O(n) por búsqueda
  Binaria: lista ORDENADA por código, divide el rango a la mitad -> O(log n) por búsqueda

Las dos están escritas a mano (bucle de Python) para que la comparación sea justa:
no se usa `bisect`, que está en C y haría la comparación injusta.

Protocolo (igual que H2): 1 corrida de calentamiento (no se mide) + 3 repeticiones
medidas con time.perf_counter(); se reporta el promedio. Semilla fija = 42.

Ejecutar:  python busqueda.py
"""

import platform
import random
import statistics
import time

SEMILLA = 42
BUSQUEDAS = 700                                 # una jornada (H2)
TAMANOS = [5_000, 10_000, 20_000, 40_000]       # 20 000 = catálogo real de la tienda
REPETICIONES = 3


def busqueda_lineal(codigos, buscado):
    for i in range(len(codigos)):
        if codigos[i] == buscado:
            return i
    return -1


def busqueda_binaria(codigos_ordenados, buscado):
    bajo, alto = 0, len(codigos_ordenados) - 1
    while bajo <= alto:
        medio = (bajo + alto) // 2
        actual = codigos_ordenados[medio]
        if actual == buscado:
            return medio
        if actual < buscado:
            bajo = medio + 1
        else:
            alto = medio - 1
    return -1


def medir(accion):
    """1 calentamiento (no se mide) + REPETICIONES corridas medidas, en ms."""
    accion()
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
    print(f"Semilla: {SEMILLA} | Búsquedas por corrida: {BUSQUEDAS} | "
          f"Protocolo: 1 calentamiento + {REPETICIONES} repeticiones, promedio\n")

    filas = []
    for n in TAMANOS:
        rnd = random.Random(SEMILLA)
        codigos = [f"P{i:06d}" for i in range(1, n + 1)]
        rnd.shuffle(codigos)                                     # catálogo SIN orden
        pedidos = [codigos[rnd.randrange(n)] for _ in range(BUSQUEDAS)]
        ordenados = sorted(codigos)                              # copia ordenada

        # Comprobación: las dos encuentran el mismo producto (mismo código).
        for p in pedidos:
            assert codigos[busqueda_lineal(codigos, p)] == ordenados[busqueda_binaria(ordenados, p)] == p

        t_lin = medir(lambda: [busqueda_lineal(codigos, p) for p in pedidos])
        t_bin = medir(lambda: [busqueda_binaria(ordenados, p) for p in pedidos])
        t_ord = medir(lambda: sorted(codigos))                   # costo de ordenar UNA vez

        m_lin, m_bin, m_ord = map(statistics.mean, (t_lin, t_bin, t_ord))
        filas.append((n, m_lin, ruido(t_lin), m_bin, ruido(t_bin), m_lin / m_bin, m_ord, t_lin, t_bin))

    print(f"Tiempo de {BUSQUEDAS} búsquedas (una jornada), en ms, promedio de {REPETICIONES} repeticiones:\n")
    print("| n | Lineal: ms | Lineal: ruido | Binaria: ms | Binaria: ruido | Cociente lineal / binaria |")
    print("|---|---|---|---|---|---|")
    for n, ml, rl, mb, rb, q, _, _, _ in filas:
        print(f"| {n:,} | {ml:.2f} | {rl:.0f} % | {mb:.3f} | {rb:.0f} % | {q:.0f} |")

    print("\nLas 3 repeticiones de cada celda (ms):")
    print("| n | Lineal | Binaria |")
    print("|---|---|---|")
    for n, _, _, _, _, _, _, tl, tb in filas:
        print(f"| {n:,} | {' / '.join(f'{t:.2f}' for t in tl)} | {' / '.join(f'{t:.3f}' for t in tb)} |")

    print("\n¿Conviene ordenar primero? (ordenar UNA vez con sorted() + 700 binarias vs 700 lineales)")
    print("| n | Ordenar una vez: ms | Ordenar + binarias: ms | Solo lineales: ms | Búsquedas para amortizar el orden |")
    print("|---|---|---|---|---|")
    for n, ml, _, mb, _, _, mo, _, _ in filas:
        por_busqueda = (ml - mb) / BUSQUEDAS                      # ahorro por búsqueda
        equilibrio = mo / por_busqueda
        print(f"| {n:,} | {mo:.2f} | {mo + mb:.2f} | {ml:.2f} | {equilibrio:.0f} |")


if __name__ == "__main__":
    main()
