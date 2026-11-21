"""
CASO TIENDA - Versión INGENUA (lista + recorrido lineal)

Escenario: la tienda carga su catálogo de productos. Por errores de digitación,
algunos códigos aparecen repetidos. Luego registra una venta, para lo cual
debe buscar el producto por su código y descontar el stock.
"""

import time


class Producto:
    def __init__(self, codigo, nombre, stock):
        self.codigo = codigo
        self.nombre = nombre
        self.stock = stock


def main():
    # Catálogo cargado (P001 y P005 aparecen dos veces por error de carga)
    catalogo = [
        Producto("P001", "Arroz 1kg", 50),
        Producto("P002", "Azucar 1kg", 40),
        Producto("P003", "Aceite 1L", 30),
        Producto("P004", "Fideos 500g", 60),
        Producto("P005", "Harina 1kg", 25),
        Producto("P006", "Leche 1L", 45),
        Producto("P007", "Sal 500g", 70),
        Producto("P008", "Cafe 250g", 20),
        Producto("P009", "Te 25 sobres", 35),
        Producto("P010", "Galletas", 80),
        Producto("P011", "Atun en lata", 55),
        Producto("P012", "Jabon", 65),
        Producto("P013", "Detergente 1kg", 30),
        Producto("P014", "Papel higienico", 90),
        Producto("P015", "Shampoo", 25),
        Producto("P016", "Pasta dental", 40),
        Producto("P017", "Gaseosa 2L", 48),
        Producto("P018", "Agua 2L", 100),
        Producto("P001", "Arroz 1kg", 20),
        Producto("P005", "Harina 1kg", 10),
    ]

    print("ALGORITMO LENTO (TIENDA)")

    # --- Paso 1: detectar códigos duplicados (bucles anidados) ---
    comparaciones_duplicados = 0
    inicio = time.perf_counter()

    for i in range(len(catalogo)):
        for j in range(i + 1, len(catalogo)):
            comparaciones_duplicados += 1

            if catalogo[i].codigo == catalogo[j].codigo:
                print("Duplicado: " + catalogo[i].codigo)

    ms_duplicados = (time.perf_counter() - inicio) * 1000

    # --- Paso 2: registrar una venta (buscar por código y descontar stock) ---
    codigo_venta = "P017"
    unidades = 3
    comparaciones_busqueda = 0
    inicio = time.perf_counter()

    producto_vendido = None
    for producto in catalogo:
        comparaciones_busqueda += 1
        if producto.codigo == codigo_venta:
            producto_vendido = producto
            break

    if producto_vendido is not None:
        producto_vendido.stock -= unidades

    ms_busqueda = (time.perf_counter() - inicio) * 1000

    if producto_vendido is not None:
        print("Venta: " + str(unidades) + " x " + producto_vendido.nombre
              + " | Stock restante: " + str(producto_vendido.stock))

    print("Comparaciones (duplicados): " + str(comparaciones_duplicados))
    print("Tiempo (duplicados): " + str(ms_duplicados) + " ms")
    print("Comparaciones (busqueda): " + str(comparaciones_busqueda))
    print("Tiempo (busqueda): " + str(ms_busqueda) + " ms")


if __name__ == "__main__":
    main()
