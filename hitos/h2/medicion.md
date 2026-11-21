# H2 - Medición: lista (ingenua) vs diccionario (adecuada)

## El problema

El mismo de mi caso: **registrar ventas**. Cada venta busca el producto por su código y le descuenta una unidad de stock.
Es la operación que más hago (ver `inventario.md`). Cada corrida procesa **1 000 ventas** a productos que existen, elegidos al azar con semilla fija (42).
Las dos estructuras reciben exactamente las mismas ventas, y al final el programa comprueba que las dos terminan con el mismo stock total.

- **Ingenua:** lista sin orden, recorrida desde el inicio hasta encontrar el código (`vender_en_lista`).
- **Adecuada:** diccionario con el código como clave (`vender_en_diccionario`).

El código está en `medicion.py`.

## Protocolo

Por cada tamaño y cada estructura: **1 corrida de calentamiento** (no se mide), luego **3 repeticiones medidas** con `time.perf_counter()`, y se reporta el **promedio**.
Los cuatro tamaños se duplican: 10 000, 20 000, 40 000 y 80 000 productos.
"Ruido" es (máximo − mínimo) / promedio entre las 3 repeticiones.

Equipo: Python 3.14.10 en Windows AMD64.

## Resultados

| n | Lista: ms (promedio) | Lista: veces vs fila anterior | Lista: ruido | Diccionario: ms (promedio) | Diccionario: veces vs fila anterior | Diccionario: ruido |
|---|---|---|---|---|---|---|
| 10,000 | 105.61 | — | 6 % | 0.071 | — | 8 % |
| 20,000 | 294.68 | 2.79 | 9 % | 0.080 | 1.13 | 11 % |
| 40,000 | 510.16 | 1.73 | 6 % | 0.095 | 1.19 | 18 % |
| 80,000 | 1044.32 | 2.05 | 9 % | 0.106 | 1.11 | 22 % |

Las 3 repeticiones de cada celda (ms):

| n | Lista | Diccionario |
|---|---|---|
| 10,000 | 105.96 / 108.51 / 102.36 | 0.074 / 0.069 / 0.069 |
| 20,000 | 282.82 / 310.50 / 290.73 | 0.085 / 0.078 / 0.077 |
| 40,000 | 529.33 / 504.09 / 497.05 | 0.106 / 0.091 / 0.089 |
| 80,000 | 1099.42 / 1009.40 / 1024.14 | 0.121 / 0.099 / 0.098 |

## Conclusión

1. Con 8 veces más productos (de 10 000 a 80 000), la lista pasó de 105.61 a 1044.32 ms (unas 9.9 veces más) y el diccionario de 0.071 a 0.106 ms (unas 1.5 veces): la lista se degrada con n y el diccionario casi no.
2. Como la búsqueda en lista es O(n), esperaba cerca de ×2 por fila. Dio ×2.79, ×1.73 y ×2.05, con un promedio de ×2.15 por duplicación: la tendencia coincide con O(n), pero cada fila se desvía. No sé si el ×2.79 de la primera duplicación es un efecto real (por ejemplo, la memoria caché del procesador) o ruido; no lo comprobé.
3. El diccionario tarda siempre décimas de milisegundo, cerca de lo que se puede medir bien, y su ruido llega a 22 %. Sus razones (×1.13, ×1.19, ×1.11) son todas un poco mayores que 1, pero con 3 repeticiones no puedo distinguir un crecimiento real y pequeño de simple ruido.
4. La tabla es coherente con O(n) frente a O(1) promedio, aunque no exacta. Para afinar la medición del diccionario haría falta más repeticiones o más ventas por corrida.

## Cómo reproducir

```
python medicion.py
```
