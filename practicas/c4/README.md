# C4 - Búsqueda lineal vs búsqueda binaria (caso: tienda)

## Qué comparo

El proceso de mi caso: **buscar un producto por su código** al vender o consultar stock (~700 veces al día, ver `hitos/h2/inventario.md`).

- **Lineal:** recorre la lista sin orden desde el inicio. O(n).
- **Binaria:** lista ordenada por código; en cada paso descarta la mitad. O(log n).

Cada corrida hace **700 búsquedas** (una jornada) a productos que existen, elegidos al azar con semilla 42. Las dos búsquedas están escritas a mano en Python (no uso `bisect`, que está en C y haría la comparación injusta) y se comprueba que encuentran el mismo producto.

**Protocolo:** 1 corrida de calentamiento (no se mide), 3 repeticiones medidas con `time.perf_counter()`, se reporta el promedio. "Ruido" = (máx − mín) / promedio.

Equipo: Python 3.14.10 en Windows AMD64 (mi PC). Código: `busqueda.py`. Salida completa: `resultado.txt`.

## Resultados (700 búsquedas, ms)

| n | Lineal: ms | Binaria: ms | Cociente lineal / binaria | Ruido lineal | Ruido binaria |
|---|---|---|---|---|---|
| 5,000 | 50.94 | 0.791 | 64 | 2 % | 6 % |
| 10,000 | 96.10 | 0.872 | 110 | 6 % | 1 % |
| **20,000 (mi catálogo)** | **265.96** | **0.918** | **290** | 16 % | 1 % |
| 40,000 | 483.38 | 1.018 | 475 | 3 % | 0 % |

Con n = 20,000 una jornada de búsquedas tarda 266 ms con la lineal y 0,92 ms con la binaria: unas 290 veces menos. El cociente crece al aumentar n (64 → 475), como se espera de O(n) frente a O(log n): la lineal crece con n y la binaria casi no cambia.

La lineal debería duplicarse con n. Dio ×1.89, ×2.77 y ×1.82. Repetí la medición completa en una copia limpia del repositorio y salió ×1.86, ×2.77 y ×1.88 (245.59 ms con n = 20,000, ruido de 6 %), así que el salto del 20,000 **se repite y no es ruido**. No sé a qué se debe: podría ser la memoria caché del procesador, pero no lo comprobé; algo parecido vi en H2 (×2.79 en la primera duplicación). Fuera de ese salto, la tendencia coincide con O(n).

## ¿Conviene ordenar primero en mi proceso?

Medí también ordenar una vez con `sorted()` (3.55 ms con n = 20,000): ordenar + 700 binarias cuesta 4.47 ms contra 265.96 ms de las lineales, y el orden se paga solo después de ~9 búsquedas. Con mi propio MergeSort de C5 (37.7 ms) se paga tras unas 100 búsquedas. Como hago ~700 al día, **si buscara en una lista, sí conviene ordenar primero**.

Pero **en mi proceso no hace falta ni lista ordenada ni binaria**: la estructura que elegí en H2 es el diccionario (O(1) promedio) y no necesita orden; solo ordeno una vez al día para el reporte. La binaria sería la opción si necesitara rangos u orden de forma continua (no es mi caso). Esto último lo razono con los datos de H2, no lo medí en esta práctica.

## Límites de la medición

- Un solo equipo y un solo lenguaje (Python); los milisegundos dependen del equipo, el cociente debería ser parecido.
- Solo busco productos que existen; las búsquedas de códigos inexistentes recorren siempre la lista completa y favorecerían aún más a la binaria.
- 3 repeticiones: con tiempos de 1 ms o menos y ruidos de hasta 16 %, las diferencias pequeñas no son concluyentes.
