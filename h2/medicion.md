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

Equipo de la corrida que se muestra: Python 3.12.3 en Linux x86_64.

## Resultados

| n | Lista: ms (promedio) | Lista: veces vs fila anterior | Lista: ruido | Diccionario: ms (promedio) | Diccionario: veces vs fila anterior | Diccionario: ruido |
|---|---|---|---|---|---|---|
| 10,000 | 66.93 | — | 15 % | 0.071 | — | 38 % |
| 20,000 | 246.73 | 3.69 | 12 % | 0.076 | 1.08 | 8 % |
| 40,000 | 680.91 | 2.76 | 8 % | 0.084 | 1.11 | 19 % |
| 80,000 | 1354.75 | 1.99 | 24 % | 0.124 | 1.47 | 65 % |

Las 3 repeticiones de cada celda (ms):

| n | Lista | Diccionario |
|---|---|---|
| 10,000 | 73.39 / 64.26 / 63.15 | 0.088 / 0.063 / 0.061 |
| 20,000 | 259.79 / 250.58 / 229.80 | 0.079 / 0.076 / 0.073 |
| 40,000 | 661.62 / 717.10 / 663.99 | 0.095 / 0.079 / 0.078 |
| 80,000 | 1168.80 / 1487.67 / 1407.77 | 0.166 / 0.120 / 0.085 |

## Conclusión

1. Con 8 veces más productos (de 10 000 a 80 000), la lista pasó de 66.93 a 1354.75 ms (unas 20 veces más) y el diccionario de 0.071 a 0.124 ms (unas 1.7 veces): la lista se degrada con n y el diccionario casi no.
2. Como la búsqueda en lista es O(n), esperaba cerca de ×2 por fila. Dio ×3.69, ×2.76 y ×1.99: va hacia 2, pero las primeras filas lo superan. Una posible causa es la memoria caché del procesador (una lista chica cabe y una grande no), pero no lo comprobé.
3. El ruido es real: las 3 repeticiones del diccionario van de 0.085 a 0.166 ms en n = 80 000 (65 %), porque son tiempos de décimas de milisegundo, cerca de lo que se puede medir bien. Por eso sus razones (×1.08, ×1.11, ×1.47) no se leen una por una: con 3 repeticiones no distingo ×1.1 de ×1.5.
4. La tabla es coherente con O(n) frente a O(1) promedio, aunque no exacta. Para afinar el diccionario haría falta más repeticiones o más ventas por corrida.

## Cómo reproducir

```
python medicion.py
```
