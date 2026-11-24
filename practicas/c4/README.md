# C4 - Búsqueda lineal vs búsqueda binaria (caso: tienda)

## Qué comparo

El proceso de mi caso: **buscar un producto por su código** al vender o consultar stock (~700 veces al día, ver `hitos/h2/inventario.md`).

- **Lineal:** recorre la lista sin orden desde el inicio. O(n).
- **Binaria:** lista ordenada por código; en cada paso descarta la mitad. O(log n).

Cada corrida hace **700 búsquedas** (una jornada) a productos que existen, elegidos al azar con semilla 42. Las dos búsquedas están escritas a mano en Python (no uso `bisect`, que está en C y haría la comparación injusta) y se comprueba que encuentran el mismo producto.

**Protocolo:** 1 corrida de calentamiento (no se mide), 3 repeticiones medidas con `time.perf_counter()`, se reporta el promedio. "Ruido" = (máx − mín) / promedio.

Equipo: Python 3.12.3 en Linux x86_64. Código: `busqueda.py`. Salida completa: `resultado.txt`.

## Resultados (700 búsquedas, ms)

| n | Lineal: ms | Binaria: ms | Cociente lineal / binaria | Ruido lineal | Ruido binaria |
|---|---|---|---|---|---|
| 5,000 | 46.19 | 0.783 | 59 | 7 % | 4 % |
| 10,000 | 82.35 | 0.835 | 99 | 1 % | 10 % |
| **20,000 (mi catálogo)** | **176.94** | **0.889** | **199** | 11 % | 1 % |
| 40,000 | 382.52 | 1.089 | 351 | 0 % | 27 % |

Con n = 20,000 una jornada de búsquedas tarda 177 ms con la lineal y 0,9 ms con la binaria: unas 200 veces menos. El cociente crece al aumentar n (59 → 351), como se espera de O(n) frente a O(log n): la lineal se duplica con n y la binaria casi no cambia. El ruido de la binaria en n = 40,000 (27 %) viene de una sola repetición lenta (1.281 ms contra 1.002 y 0.984), y a estos tiempos tan chicos cualquier interrupción pesa mucho.

## ¿Conviene ordenar primero en mi proceso?

Medí también ordenar una vez con `sorted()` (3.77 ms con n = 20,000): ordenar + 700 binarias cuesta 4.66 ms contra 176.94 ms de las lineales, y el orden se paga solo después de ~15 búsquedas, así que **si buscara en una lista, sí conviene ordenar primero** (con mi propio MergeSort de C5, 33 ms, se paga tras ~130 búsquedas: también conviene con 700 al día).

Pero **en mi proceso no hace falta ni lista ordenada ni binaria**: la estructura que elegí en H2 es el diccionario (O(1) promedio) y no necesita orden; solo ordeno una vez al día para el reporte. La binaria sería la opción si necesitara rangos u orden de forma continua (no es mi caso). Esto último lo razono con los datos de H2, no lo medí aquí: son otro equipo y otro experimento.

## Límites de la medición

- Una sola máquina y un solo lenguaje (Python); en tu PC los milisegundos serán otros, el cociente debería ser parecido. Vuelve a correr `python busqueda.py` y pega tu salida en `resultado.txt`.
- Solo busco productos que existen; las búsquedas de códigos inexistentes recorren siempre la lista completa y favorecerían aún más a la binaria.
- 3 repeticiones: los ruidos de arriba muestran que las diferencias pequeñas (por ejemplo entre filas de la binaria) no son concluyentes.
