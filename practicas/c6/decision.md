# C6 - Elección del algoritmo de ordenamiento (caso: tienda)

## Mi elección

**MergeSort**, para ordenar el catálogo (~20,000 productos) por código: el reporte de inventario diario y, si hiciera falta, dejar la lista lista para búsqueda binaria.

## Mis datos

Catálogo de unos 20,000 productos con código de texto (`hitos/h2/inventario.md`). Se ordena una vez al día (reporte). No sé en qué estado llega, así que probé cinco formas posibles con n = 20,000: **aleatorio** (importado de proveedores), **casi ordenado** (catálogo de ayer ordenado + 10 productos fuera de lugar, por las ~10 altas diarias), **ordenado**, **inverso** y **5 % de códigos repetidos** (el problema de H1).

## Evidencia (`eleccion.py`, `resultado.txt`)

Tiempo en ms, promedio de 3 repeticiones tras 1 calentamiento, semilla 42, Python 3.12.3 en Linux (entre paréntesis, el ruido):

| Forma de los datos | Inserción | MergeSort | QuickSort | sorted() (ref.) |
|---|---|---|---|---|
| aleatorio | 5,735.0 (3 %) | 33.3 (0 %) | 36.9 (5 %) | 3.7 (3 %) |
| casi ordenado (10 fuera de lugar) | **7.0 (0 %)** | 20.6 (1 %) | 34.9 (13 %) | 0.2 (12 %) |
| ordenado | **1.4 (2 %)** | 22.3 (1 %) | 36.5 (33 %) | 0.2 (12 %) |
| inverso | 11,418.1 (1 %) | 21.5 (2 %) | 37.8 (17 %) | 0.1 (0 %) |
| 5 % repetidos | 5,651.7 (6 %) | 33.2 (1 %) | 35.3 (8 %) | 3.7 (1 %) |

## Por qué MergeSort

1. **Nunca se degrada:** su peor tiempo en las cinco formas fue 33.3 ms y el mejor 20.6 ms. Su O(n log n) vale siempre, sin depender de cómo llegue el catálogo.
2. **La inserción gana solo en un caso y pierde feo en los demás.** Con datos ordenados o casi ordenados es más rápida (7.0 contra 20.6 ms), pero esa ventaja son unos 14 ms al día, que no se notan; con datos al azar o inversos tarda 5.7 y 11.4 **segundos**. Es una apuesta de ahorrar milisegundos arriesgando segundos.
3. **QuickSort no ganó en ninguna forma** (34.9 a 37.8 ms contra 20.6 a 33.3 de MergeSort), tuvo más ruido (hasta 33 %) y su peor caso es O(n²) si el pivote sale mal; aquí lo evité con pivote al azar, pero es una complicación que MergeSort no tiene. La diferencia de velocidad entre ambos es pequeña; mi decisión se apoya más en predecibilidad que en velocidad.
4. **Es estable:** los códigos repetidos (P001, P005 en H1) conservan su orden de llegada, útil para revisar después cuál duplicado vale. No lo medí; es una propiedad del algoritmo.
5. **Su costo, memoria extra O(n), es irrelevante con 20,000 códigos.**

## Cuándo cambiaría

- Si el catálogo llegara **siempre casi ordenado** y yo lo supiera con certeza, usaría inserción (7 ms contra 21 ms), pero no tengo esa garantía.
- Si el catálogo creciera a millones de productos y la memoria extra importara, QuickSort in situ sería candidato.
- En un programa real usaría `sorted()` de Python: 3.7 ms con datos al azar (9 veces menos que mi MergeSort) y 0.2 ms con datos casi ordenados. Es un MergeSort híbrido que aprovecha el orden previo, lo que apoya la elección de la familia MergeSort.

## Límites

- No sé en qué estado llega mi catálogo real: elegí MergeSort justamente porque rinde bien en todas las formas probadas. Si me confirmas cómo llega de verdad, la elección puede afinarse.
- Una sola máquina y un solo lenguaje; en tu PC los milisegundos serán distintos, el orden entre algoritmos debería mantenerse. Vuelve a correr `python eleccion.py` (necesita `../c5/torneo.py`; tarda unos 2 minutos) y pega tu salida en `resultado.txt`.
- 3 repeticiones: el ruido de QuickSort (hasta 33 %) y de `sorted()` en tiempos de 0.1 a 0.2 ms muestra que esas celdas no son precisas.
