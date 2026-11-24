# C5 - Torneo de ordenamientos (caso: tienda)

## Cómo se hizo

Ordeno los **códigos de producto** (`P000001`...) mezclados al azar con semilla 42, como un catálogo recién importado sin orden. Cada algoritmo recibe una copia de la misma lista y su resultado se comprueba contra `sorted()`.

- **Inserción** (cuadrático, O(n²)): el lento.
- **MergeSort** (O(n log n) siempre, usa memoria extra).
- **QuickSort** (O(n log n) promedio, O(n²) en el peor caso): pivote al azar y partición en 3 vías.
- **`sorted()` de Python**: solo como referencia, no compite (está escrito en C).

Los tres primeros están escritos a mano en Python. **Protocolo:** 1 calentamiento (no se mide) + 3 repeticiones, promedio. Tamaños que se duplican; 20,000 es mi catálogo real.

Equipo: Python 3.12.3 en Linux x86_64. Código: `torneo.py`. Salida completa (con las 3 repeticiones de cada celda): `resultado.txt`.

## Resultados: tiempo en ms (promedio; entre paréntesis, el ruido)

| n | Inserción | MergeSort | QuickSort | sorted() (referencia) |
|---|---|---|---|---|
| 2,500 | 91.6 (2 %) | 3.4 (2 %) | 3.5 (13 %) | 0.3 (9 %) |
| 5,000 | 350.9 (3 %) | 7.2 (0 %) | 7.6 (3 %) | 0.7 (2 %) |
| 10,000 | 1,549.1 (7 %) | 15.8 (1 %) | 19.4 (43 %) | 1.7 (5 %) |
| **20,000** | **5,813.0 (3 %)** | **33.3 (1 %)** | **37.5 (17 %)** | 3.7 (2 %) |

Veces que tarda más al duplicar n:

| n | Inserción | MergeSort | QuickSort |
|---|---|---|---|
| 5,000 | 3.83 | 2.11 | 2.16 |
| 10,000 | 4.41 | 2.20 | 2.53 |
| 20,000 | 3.75 | 2.11 | 1.93 |

## Conclusiones

1. **La inserción crece como O(n²):** al duplicar n tarda unas 4 veces más (×3.83, ×4.41, ×3.75). MergeSort y QuickSort tardan algo más del doble (≈ ×2.1), lo esperado para O(n log n). Las desviaciones (por ejemplo ×4.41) las atribuyo a ruido; no las comprobé.
2. **En mi catálogo real (20,000) la diferencia es enorme:** 5.8 s contra 33 ms, unas 175 veces más para la inserción frente a MergeSort y 155 frente a QuickSort. Y la brecha crece con n (27 veces con 2,500 → 175 con 20,000), así que con un catálogo mayor la inserción se vuelve inviable.
3. **MergeSort y QuickSort quedan prácticamente empatados.** MergeSort fue algo más rápido en las 4 filas (cociente MergeSort / QuickSort entre 0.81 y 0.96), pero QuickSort tuvo bastante ruido (hasta 43 %, por una repetición lenta de 24.9 ms con n = 10,000), así que no afirmo que uno sea mejor en velocidad con esta evidencia.
4. **El `sorted()` de Python es ~9 veces más rápido** que mi MergeSort (3.7 contra 33.3 ms con n = 20,000), porque corre en C y es un algoritmo híbrido. En un programa real de la tienda usaría `sorted()`; los algoritmos a mano sirven para entender y medir.

## Límites

- Solo datos al azar. Con datos ya ordenados o casi ordenados la inserción cambia por completo; eso lo mido en C6.
- El peor caso de QuickSort (O(n²)) no apareció porque uso pivote al azar; no lo provoqué.
- Una sola máquina y un solo lenguaje. Vuelve a correr `python torneo.py` en tu PC y pega tu salida en `resultado.txt` (con n = 20,000 la inserción tarda cerca de 1 minuto en total).
