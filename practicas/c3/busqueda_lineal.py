"""
C3 - Primera tabla de mediciones: búsqueda lineal en el caso de la tienda.

Proceso medido: buscar un producto por código recorriendo la lista desde el inicio.
Se busca un código que NO existe, así que cada corrida recorre los n elementos
(peor caso, siempre el mismo trabajo).

Protocolo del taller: 1 corrida de calentamiento (no se mide) + 5 corridas medidas
con time.perf_counter(), se reporta el promedio, con n, 4n y 16n.
n se eligió para que cada corrida dure varios ms.

Ejecutar:  python busqueda_lineal.py
"""

import platform
import statistics
import time

N = 50_000
TAMANOS = [N, 4 * N, 16 * N]
CORRIDAS = 5


def busqueda_lineal(codigos, buscado):
    for i in range(len(codigos)):
        if codigos[i] == buscado:
            return i
    return -1


def medir(codigos, buscado):
    busqueda_lineal(codigos, buscado)                    # calentamiento, no se mide
    tiempos = []
    for _ in range(CORRIDAS):
        t0 = time.perf_counter()
        busqueda_lineal(codigos, buscado)
        tiempos.append((time.perf_counter() - t0) * 1000)
    return tiempos


def main():
    print(f"Equipo: Python {platform.python_version()} en {platform.system()} {platform.machine()}")
    print(f"Protocolo: 1 calentamiento + {CORRIDAS} corridas, promedio | n = {N:,}, 4n, 16n\n")

    print("| n | Promedio (ms) | Razón vs fila anterior | Esperado | Ruido |")
    print("|---|---|---|---|---|")
    anterior = None
    corridas = {}
    for n in TAMANOS:
        codigos = ["P" + str(i).zfill(7) for i in range(n)]
        t = medir(codigos, "NO-EXISTE")
        corridas[n] = t
        prom = statistics.mean(t)
        razon = "—" if anterior is None else f"{prom / anterior:.2f}"
        esperado = "—" if anterior is None else "≈ 4"
        ruido = (max(t) - min(t)) / prom * 100
        print(f"| {n:,} | {prom:.3f} | {razon} | {esperado} | {ruido:.0f} % |")
        anterior = prom

    print("\nLas 5 corridas de cada fila (ms):")
    for n, t in corridas.items():
        print(f"n = {n:,}: " + " / ".join(f"{x:.3f}" for x in t))


if __name__ == "__main__":
    main()
