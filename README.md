# tienda-algoritmo-garcia

Proyecto de algoritmos aplicado a un caso real: el **inventario de un minimarket** (unos 20 000 productos y unas 500 ventas por día). El problema es que el catálogo trae códigos de producto repetidos y que cada venta busca el producto recorriendo la lista completa, lo que vuelve lento el proceso.

## Mi proceso

1. **[H1 – El proceso lento](h1/)**: describo el caso, qué tarda y por qué (O(n²) para detectar duplicados, O(n) para buscar), y comparo una versión ingenua (`tienda_lento.py`) con una adecuada (`tienda_rapido.py`).
2. **[H2 – La estructura de datos](hitos/h2/)**: inventario de las operaciones que hago y cuántas veces, elección del diccionario (tabla hash) y medición contra la lista (`inventario.md`, `estructura.md`, `medicion.md`).
3. **[H3 – ¿Voraz o dinámica?](hitos/h3/)**: el problema de dar cambio al cliente y la decisión argumentada entre estrategia voraz y programación dinámica (`decision.md`).
4. **[Prácticas](practicas/)**: mediciones con el mismo protocolo (calentar, repetir 3 veces, promediar).
   - [C4 – búsqueda lineal vs binaria](practicas/c4/)
   - [C5 – torneo de ordenamientos](practicas/c5/)
   - [C6 – elección del algoritmo de ordenamiento](practicas/c6/)

## Cómo reproducir

Cada carpeta con medición tiene su script de Python; se ejecuta desde la propia carpeta, por ejemplo `python busqueda.py` dentro de `practicas/c4/`.
