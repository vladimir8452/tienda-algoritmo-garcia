# C5 - Torneo de ordenamientos (caso: tienda)

## Cómo se hizo

Ordeno los **códigos de producto** (`P000001`...) mezclados al azar con semilla 42, como un catálogo recién importado sin orden. Cada algoritmo recibe una copia de la misma lista y su resultado se comprueba contra `sorted()`.

- **Inserción** (cuadrático, O(n²)): el lento.
- **MergeSort** (O(n log n) siempre, usa memoria extra).
- **QuickSort** (O(n log n) promedio, O(n²) en el peor caso): pivote al azar y partición en 3 vías.
- **`sorted()` de Python**: solo como referencia, no compite (está escrito en C).

Los tres primeros están escritos a mano en Python. **Protocolo:** 1 calentamiento (no se mide) + 3 repeticiones, promedio. Tamaños que se duplican; 20,000 es mi catálogo real.

Equipo: Python 3.14.10 en Windows AMD64 (mi PC). Código: `torneo.py`. Salida completa (con las 3 repeticiones de cada celda): `resultado.txt`.

## Resultados: tiempo en ms (promedio; entre paréntesis, el ruido)

| n | Inserción | MergeSort | QuickSort | sorted() (referencia) |
|---|---|---|---|---|
| 2,500 | 106.0 (22 %) | 5.1 (69 %) | 3.6 (9 %) | 0.3 (3 %) |
| 5,000 | 410.1 (6 %) | 8.4 (1 %) | 8.0 (2 %) | 0.8 (13 %) |
| 10,000 | 1,614.2 (0 %) | 18.1 (0 %) | 17.0 (1 %) | 1.6 (2 %) |
| **20,000** | **6,386.7 (1 %)** | **37.7 (1 %)** | **35.7 (4 %)** | 3.6 (1 %) |

Veces que tarda más al duplicar n:

| n | Inserción | MergeSort | QuickSort |
|---|---|---|---|
| 5,000 | 3.87 | 1.66 | 2.21 |
| 10,000 | 3.94 | 2.15 | 2.12 |
| 20,000 | 3.96 | 2.09 | 2.10 |

## Conclusiones

1. **La inserción crece como O(n²):** al duplicar n tarda casi 4 veces más (×3.87, ×3.94, ×3.96). MergeSort y QuickSort tardan algo más del doble (≈ ×2.1 en las dos últimas filas), lo esperado para O(n log n). El ×1.66 de MergeSort en la primera duplicación viene de una repetición lenta con n = 2,500 (ruido de 69 %); no lo comprobé más.
2. **En mi catálogo real (20,000) la diferencia es enorme:** 6.4 s contra unos 36 a 38 ms, es decir, 169 veces más para la inserción frente a MergeSort y 179 frente a QuickSort. La brecha crece con n (21 y 29 veces con 2,500 → 169 y 179 con 20,000).
3. **MergeSort y QuickSort quedan empatados:** con n ≥ 5,000 QuickSort fue un poco más rápido (cociente MergeSort / QuickSort entre 1.05 y 1.07), una diferencia de 0.4 a 2 ms. Con n = 2,500 la diferencia es mayor (1.41) pero MergeSort tuvo 69 % de ruido. Con 3 repeticiones no afirmo que uno sea más rápido; en otro equipo, donde corrí antes este mismo torneo, el orden entre los dos salió al revés.
4. **El `sorted()` de Python es ~10 veces más rápido** que mis dos algoritmos con n = 20,000 (3.6 ms contra 36 a 38), porque corre en C y es un algoritmo híbrido. En un programa real de la tienda usaría `sorted()`; los algoritmos a mano sirven para entender y medir.

## Límites

- Solo datos al azar. Con datos ya ordenados o casi ordenados la inserción cambia por completo; eso lo mido en C6.
- El peor caso de QuickSort (O(n²)) no apareció porque uso pivote al azar; no lo provoqué.
- Un solo equipo y un solo lenguaje. Con n = 2,500 los tiempos son tan chicos que el ruido llega a 69 %; las conclusiones se apoyan en los tamaños mayores.
