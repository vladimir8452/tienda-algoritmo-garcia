"""
H3 - Voraz vs dinámica: dar cambio al cliente en la tienda.

Decisión que se repite: en cada venta, qué moneda o billete entregar a continuación.
Resultado a optimizar: la menor cantidad de monedas/billetes en el cambio.

  Voraz:     tomar siempre la denominación más grande que quepa.
  Dinámica:  cambio(m) = 1 + min(cambio(m - d)) sobre cada denominación d; se guarda
             en una tabla para no recalcular los mismos subproblemas.

Todo en centavos (enteros) para evitar errores de decimales.
Ejecutar:  python medicion_h3.py
"""

import platform
import random
import statistics
import time

SEMILLA = 42
CAMBIOS = 500                                  # ~500 ventas por día (H1)
TAMANOS = [10_000, 20_000, 40_000, 80_000]     # monto máximo en centavos; se duplica
REPETICIONES = 3

# Denominaciones de Bolivia en centavos (verificar contra las que usa tu tienda).
BOLIVIA = [20000, 10000, 5000, 2000, 1000, 500, 200, 100, 50, 20, 10]
# Sistema NO canónico, solo para mostrar cuándo el voraz falla.
CONTRAEJEMPLO = [4, 3, 1]


def cambio_voraz(monto, denominaciones):
    """Devuelve la cantidad de piezas (denominaciones ordenadas de mayor a menor)."""
    piezas = 0
    for d in denominaciones:
        piezas += monto // d
        monto %= d
    return piezas if monto == 0 else None


def construir_tabla(maximo, denominaciones):
    """minimo[m] = menor cantidad de piezas para m. Cada m se calcula una sola vez."""
    INF = float("inf")
    minimo = [0] + [INF] * maximo
    for m in range(1, maximo + 1):
        mejor = INF
        for d in denominaciones:
            if d <= m and minimo[m - d] + 1 < mejor:
                mejor = minimo[m - d] + 1
        minimo[m] = mejor
    return minimo


def jornada_voraz(montos, denominaciones):
    return [cambio_voraz(m, denominaciones) for m in montos]


def jornada_dinamica(montos, denominaciones, maximo):
    tabla = construir_tabla(maximo, denominaciones)      # se paga una vez por jornada
    return [tabla[m] for m in montos]


def medir(accion):
    accion()                                             # calentamiento, no se mide
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
    print(f"Semilla: {SEMILLA} | Cambios por jornada: {CAMBIOS} | "
          f"Protocolo: 1 calentamiento + {REPETICIONES} repeticiones, promedio\n")

    # 1) ¿El voraz alcanza? Comparar contra la dinámica en TODOS los montos hasta 1 000 Bs.
    tope = 100_000
    tabla = construir_tabla(tope, BOLIVIA)
    # Solo los montos múltiplos de 10 centavos son pagables con estas denominaciones.
    distintos = [m for m in range(10, tope + 1, 10) if cambio_voraz(m, BOLIVIA) != tabla[m]]
    print(f"Denominaciones de Bolivia: montos revisados = {tope // 10:,}, "
          f"donde voraz != óptimo = {len(distintos)}")

    t = construir_tabla(10, CONTRAEJEMPLO)
    print(f"Contraejemplo {CONTRAEJEMPLO}, monto 6: voraz = {cambio_voraz(6, CONTRAEJEMPLO)} piezas, "
          f"óptimo = {t[6]} piezas\n")

    # 2) Medición: voraz vs dinámica sobre una jornada, con 4 tamaños que se duplican.
    print("| n (monto máx., centavos) | Voraz: ms | veces vs anterior | ruido | "
          "Dinámica: ms | veces vs anterior | ruido | piezas iguales |")
    print("|---|---|---|---|---|---|---|---|")
    ant_v = ant_d = None
    for n in TAMANOS:
        rnd = random.Random(SEMILLA)
        montos = [rnd.randrange(1, n // 10 + 1) * 10 for _ in range(CAMBIOS)]
        tv = medir(lambda: jornada_voraz(montos, BOLIVIA))
        td = medir(lambda: jornada_dinamica(montos, BOLIVIA, n))
        iguales = jornada_voraz(montos, BOLIVIA) == jornada_dinamica(montos, BOLIVIA, n)
        mv, md = statistics.mean(tv), statistics.mean(td)
        rv = "—" if ant_v is None else f"{mv / ant_v:.2f}"
        rd = "—" if ant_d is None else f"{md / ant_d:.2f}"
        print(f"| {n:,} | {mv:.3f} | {rv} | {ruido(tv):.0f} % | "
              f"{md:.3f} | {rd} | {ruido(td):.0f} % | {'sí' if iguales else 'NO'} |")
        ant_v, ant_d = mv, md


if __name__ == "__main__":
    main()
