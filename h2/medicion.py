"""
H2 - Medición: registrar ventas en el inventario de la tienda
(buscar el producto por código y descontarle una unidad de stock).

  Estructura ingenua:  lista sin orden + recorrido lineal        -> O(n) por venta
  Estructura adecuada: diccionario (código -> producto)          -> O(1) promedio por venta

Protocolo: 1 corrida de calentamiento (no se mide) + 3 repeticiones medidas;
se reporta el promedio. Los tamaños se duplican.

Ejecutar:  python medicion.py
"""

import platform
import random
import statistics
import time

SEMILLA = 42                                  # misma semilla = datos repetibles
VENTAS = 1000                                 # ventas procesadas en cada corrida
TAMANOS = [10_000, 20_000, 40_000, 80_000]    # cuatro tamaños que se duplican
REPETICIONES = 3
STOCK_INICIAL = 1_000_000                     # alto para que el stock no llegue a cero


class Producto:
    __slots__ = ("codigo", "nombre", "stock")

    def __init__(self, codigo, nombre, stock):
        self.codigo = codigo
        self.nombre = nombre
        self.stock = stock


def generar_codigos(n, rnd):
    """Códigos únicos P00001, P00002, ... mezclados con la semilla."""
    codigos = [f"P{i:06d}" for i in range(1, n + 1)]
    rnd.shuffle(codigos)
    return codigos


def vender_en_lista(lista, pedidos):
    """Ingenua: para cada venta recorre la lista hasta encontrar el código."""
    vendidas = 0
    for codigo in pedidos:
        for producto in lista:
            if producto.codigo == codigo:
                producto.stock -= 1
                vendidas += 1
                break
    return vendidas


def vender_en_diccionario(diccionario, pedidos):
    """Adecuada: para cada venta va directo al producto por su código."""
    vendidas = 0
    for codigo in pedidos:
        producto = diccionario.get(codigo)
        if producto is not None:
            producto.stock -= 1
            vendidas += 1
    return vendidas


def medir(accion):
    """1 corrida de calentamiento (no se mide) + REPETICIONES corridas medidas, en ms."""
    accion()
    tiempos = []
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        accion()
        fin = time.perf_counter()
        tiempos.append((fin - inicio) * 1000)
    return tiempos


def ruido(tiempos):
    """Dispersión relativa: (máximo - mínimo) / promedio, en %."""
    return (max(tiempos) - min(tiempos)) / statistics.mean(tiempos) * 100


def main():
    print(f"Equipo: Python {platform.python_version()} en {platform.system()} {platform.machine()}")
    print(f"Semilla: {SEMILLA} | Ventas por corrida: {VENTAS:,} | "
          f"Protocolo: 1 calentamiento + {REPETICIONES} repeticiones, promedio")
    print()

    filas = []
    anterior_lista = None
    anterior_dic = None

    for n in TAMANOS:
        rnd = random.Random(SEMILLA)
        codigos = generar_codigos(n, rnd)

        # Dos copias independientes del inventario: una por estructura.
        lista = [Producto(c, "Producto " + c, STOCK_INICIAL) for c in codigos]
        diccionario = {c: Producto(c, "Producto " + c, STOCK_INICIAL) for c in codigos}

        # Mismas ventas para las dos estructuras (todas a productos que existen).
        pedidos = [codigos[rnd.randrange(n)] for _ in range(VENTAS)]

        t_lista = medir(lambda: vender_en_lista(lista, pedidos))
        t_dic = medir(lambda: vender_en_diccionario(diccionario, pedidos))

        # Comprobación: las dos estructuras terminan con el mismo stock total.
        corridas = 1 + REPETICIONES
        esperado = n * STOCK_INICIAL - VENTAS * corridas
        stock_lista = sum(p.stock for p in lista)
        stock_dic = sum(p.stock for p in diccionario.values())
        if stock_lista != esperado or stock_dic != esperado:
            print(f"ADVERTENCIA: stock distinto en n={n} "
                  f"(lista={stock_lista}, dict={stock_dic}, esperado={esperado})")

        prom_lista = statistics.mean(t_lista)
        prom_dic = statistics.mean(t_dic)
        veces_lista = "—" if anterior_lista is None else f"{prom_lista / anterior_lista:.2f}"
        veces_dic = "—" if anterior_dic is None else f"{prom_dic / anterior_dic:.2f}"
        anterior_lista = prom_lista
        anterior_dic = prom_dic

        filas.append((n, prom_lista, veces_lista, ruido(t_lista),
                      prom_dic, veces_dic, ruido(t_dic), t_lista, t_dic))

    print("| n | Lista: ms (promedio) | Lista: veces vs fila anterior | Lista: ruido | "
          "Diccionario: ms (promedio) | Diccionario: veces vs fila anterior | Diccionario: ruido |")
    print("|---|---|---|---|---|---|---|")
    for n, pl, vl, rl, pd, vd, rd, _, _ in filas:
        print(f"| {n:,} | {pl:.2f} | {vl} | {rl:.0f} % | {pd:.3f} | {vd} | {rd:.0f} % |")

    print()
    print("Las 3 repeticiones de cada celda (ms):")
    print("| n | Lista | Diccionario |")
    print("|---|---|---|")
    for n, _, _, _, _, _, _, tl, td in filas:
        print(f"| {n:,} | {' / '.join(f'{t:.2f}' for t in tl)} | {' / '.join(f'{t:.3f}' for t in td)} |")


if __name__ == "__main__":
    main()
