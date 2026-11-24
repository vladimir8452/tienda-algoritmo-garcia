# C6 - Elección del algoritmo de ordenamiento (caso: tienda)

## Mi elección

**MergeSort**, para ordenar el catálogo (~20,000 productos) por código: el reporte de inventario diario y, si hiciera falta, dejar la lista lista para búsqueda binaria.

## Mis datos

Catálogo de unos 20,000 productos con código de texto (`hitos/h2/inventario.md`). Se ordena una vez al día (reporte). No sé en qué estado llega, así que probé cinco formas posibles con n = 20,000: **aleatorio** (importado de proveedores), **casi ordenado** (catálogo de ayer ordenado + 10 productos fuera de lugar, por las ~10 altas diarias), **ordenado**, **inverso** y **5 % de códigos repetidos** (el problema de H1).

## Evidencia (`eleccion.py`, `resultado.txt`)

Tiempo en ms, promedio de 3 repeticiones tras 1 calentamiento, semilla 42, Python 3.14.10 en Windows AMD64 (mi PC); entre paréntesis, el ruido:

| Forma de los datos | Inserción | MergeSort | QuickSort | sorted() (ref.) |
|---|---|---|---|---|
| aleatorio | 6,384.1 (1 %) | 40.4 (13 %) | 35.3 (2 %) | 3.8 (12 %) |
| casi ordenado (10 fuera de lugar) | **7.7 (1 %)** | 24.0 (0 %) | 33.9 (10 %) | 0.2 (1 %) |
| ordenado | **1.5 (4 %)** | 24.0 (1 %) | 32.6 (1 %) | 0.2 (1 %) |
| inverso | 12,468.5 (1 %) | 28.4 (34 %) | 36.0 (7 %) | 0.2 (1 %) |
| 5 % repetidos | 6,226.9 (2 %) | 38.3 (1 %) | 36.3 (9 %) | 3.6 (1 %) |

## Por qué MergeSort

1. **Su tiempo se mantiene acotado en todas las formas:** entre 24.0 y 40.4 ms, y su O(n log n) vale siempre, sin depender de cómo llegue el catálogo. Su ventaja es la garantía, no la velocidad.
2. **La inserción gana solo con datos ordenados o casi ordenados** (7.7 contra 24.0 ms: unos 16 ms de ahorro al día, que no se notan). Con datos al azar o inversos tarda 6.4 y 12.5 **segundos**. Es una apuesta de ahorrar milisegundos arriesgando segundos.
3. **MergeSort y QuickSort quedan muy parejos.** QuickSort fue más rápido con datos al azar y con repetidos (por 5 y 2 ms), y MergeSort con datos ya ordenados, casi ordenados e inversos (por 8 a 10 ms). Todas son diferencias de milisegundos en una tarea que se hace una vez al día, y MergeSort tuvo ruidos de 13 % y 34 % en dos filas, así que no decido por velocidad. QuickSort además tiene un peor caso O(n²) si el pivote sale mal; aquí lo evité con pivote al azar, pero MergeSort no necesita esa precaución.
4. **Es estable:** los códigos repetidos (P001, P005 en H1) conservan su orden de llegada, útil para revisar después cuál duplicado vale. No lo medí; es una propiedad del algoritmo.
5. **Su costo, memoria extra O(n), es irrelevante con 20,000 códigos.**

## Cuándo cambiaría

- Si el catálogo llegara **siempre casi ordenado** y yo lo supiera con certeza, usaría inserción (7.7 ms contra 24.0 ms), pero no tengo esa garantía.
- Si el catálogo creciera a millones de productos y la memoria extra importara, QuickSort in situ sería candidato.
- En un programa real usaría `sorted()` de Python: 3.8 ms con datos al azar (unas 10 veces menos que mi MergeSort) y 0.2 ms con datos ordenados o casi ordenados. Es un MergeSort híbrido que aprovecha el orden previo, lo que apoya la elección de la familia MergeSort.

## Límites

- No sé en qué estado llega mi catálogo real: elegí MergeSort justamente porque se mantiene parejo en todas las formas probadas. Si lo supiera, la elección podría afinarse.
- Un solo equipo y un solo lenguaje; en otro equipo los milisegundos cambian y el orden entre MergeSort y QuickSort puede invertirse.
- 3 repeticiones: ruidos de 12 % a 34 % en algunas celdas de MergeSort y de `sorted()` muestran que esas celdas no son precisas.
