# tienda-algoritmo-garcia

Vladimir Garcia Rojas

Proyecto de algoritmos aplicado a un caso real: el **inventario de un minimarket** (unos 20 000 productos y unas 500 ventas por día). El problema es que el catálogo trae códigos de producto repetidos y que cada venta busca el producto recorriendo la lista completa, lo que vuelve lento el proceso.

## Mi proceso

1. **[H1 – El proceso lento](h1/)**: describo el caso, qué tarda y por qué (O(n²) para detectar duplicados, O(n) para buscar), y comparo una versión ingenua (`tienda_lento.py`) con una adecuada (`tienda_rapido.py`).
2. **[H2 – La estructura de datos](hitos/h2/)**: inventario de las operaciones que hago y cuántas veces, elección del diccionario (tabla hash) y medición contra la lista (`inventario.md`, `estructura.md`, `medicion.md`).
3. **[H3 – ¿Voraz o dinámica?](hitos/h3/)**: el problema de dar cambio al cliente y la decisión argumentada entre estrategia voraz y programación dinámica, con comparación medida (`decision.md`, `medicion_h3.py`).
4. **[Prácticas](practicas/)**: mediciones con protocolo (calentar, repetir y promediar; 5 corridas en C3 y 3 repeticiones en las demás).
   - [C3 – búsqueda lineal con n, 4n y 16n](practicas/c3/)
   - [C4 – búsqueda lineal vs binaria](practicas/c4/)
   - [C5 – torneo de ordenamientos](practicas/c5/)
   - [C6 – elección del algoritmo de ordenamiento](practicas/c6/)
5. **[Integradora](integradora/)**: análisis de costos, recurrencias, contraejemplo del voraz, estrategia y estructura (`analisis.md`), y la medición de mi solución contra la ingenua con su conclusión y la escala (`medicion.md`).
6. **[Parcial 2 – receptor de pedidos](parcial2/)**: trabajo aparte (C#), con su elección y su medición.

## Cómo reproducir

Cada carpeta con medición tiene su script de Python; se ejecuta desde la propia carpeta, por ejemplo `python busqueda.py` dentro de `practicas/c4/`. Las salidas que pegué en los informes son las de mi PC (Python 3.14.10 en Windows).

## Declaración de ayuda

- **H3, C3 e integradora (`analisis.md` y `medicion.md`):** usé Claude (IA) para plantear el análisis y escribir los borradores y los scripts de `hitos/h3/` y `practicas/c3/`. Las mediciones las ejecuté yo en mi PC y las cifras de las tablas son las de mi equipo.
- **H1, H2, C4, C5, C6 y Parcial 2:** usé una IA solo en algunas partes; el resto lo hice yo. Las mediciones las ejecuté yo en mi PC.
- **Código ajeno:** ninguno.
