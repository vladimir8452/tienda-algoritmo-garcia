# C3 - Primera tabla de mediciones (caso: tienda)

## Qué mido

La **búsqueda lineal** de un producto por código en la lista del catálogo de la tienda (el mismo proceso de H1 y H2). Busco un código que no existe, así cada corrida recorre los n elementos y hace siempre el mismo trabajo. Código: `busqueda_lineal.py`.

**Protocolo del taller:** 1 corrida de calentamiento (no se mide) + 5 corridas medidas con `time.perf_counter()`, promedio, con n, 4n y 16n. Elegí n = 50 000 para que cada corrida dure varios ms. "Ruido" = (máx − mín) / promedio.

Equipo: Python 3.14.10 en Windows AMD64 (mi PC)

## Resultados (en mi PC)

| n | Promedio (ms) | Razón vs fila anterior | Esperado | Ruido |
|---|---|---|---|---|
| 50,000 | 1.000 | — | — | 3 % |
| 200,000 | 4.647 | 4.65 | ≈ 4 | 20 % |
| 800,000 | 17.904 | 3.85 | ≈ 4 | 16 % |

Las 5 corridas de cada fila están en `resultado.txt`.

## Qué vi

Las razones dieron ×4.65 y ×3.85, cerca del ×4 esperado para una búsqueda lineal (O(n)). Entre la primera y la última fila, n se multiplicó por 16 y el tiempo por 17.9 (de 1.000 a 17.904 ms). El tiempo por elemento recorrido salió parecido en las tres filas (unos 20 a 23 nanosegundos), que es lo que se espera si el costo crece proporcional a n. Las dos razones se desvían del 4 exacto en sentidos opuestos y las filas de 200 000 y 800 000 tienen ruido de 20 % y 16 %, así que no puedo decir si esa desviación es real o ruido; no lo comprobé. Para afinar haría falta más de 5 corridas o un n mayor.

