Vladimir Garcia Rojas

# Integradora - Medición (I3): lista (ingenua) contra diccionario (la mía)

## Qué mido

La operación que más repito en mi caso: **registrar una venta**, que busca el producto por su código y le descuenta una unidad de stock (unas 700 veces al día, ver `hitos/h2/inventario.md`).

- **Ingenua:** lista sin orden, recorrida desde el inicio hasta encontrar el código.
- **Mía:** diccionario con el código como clave.

Cada corrida procesa **1 000 ventas** a productos que existen, elegidos al azar con semilla 42. Las dos estructuras reciben exactamente las mismas ventas, y al final el programa comprueba que las dos terminan con el mismo stock total. Código: `hitos/h2/medicion.py`.

## Protocolo

Por cada tamaño y cada estructura: **1 corrida de calentamiento** (no se mide), **3 repeticiones medidas** con `time.perf_counter()` y se reporta el **promedio**. Cuatro tamaños que se duplican: 10 000, 20 000, 40 000 y 80 000 productos. "Ruido" = (máximo − mínimo) / promedio entre las 3 repeticiones.

Equipo: Python 3.14.10 en Windows AMD64 (mi PC).

## Resultados (1 000 ventas, en ms)

| n | Lista: ms | Lista: veces vs fila anterior | Lista: ruido | Diccionario: ms | Diccionario: veces vs fila anterior | Diccionario: ruido |
|---|---|---|---|---|---|---|
| 10,000 | 105.61 | — | 6 % | 0.071 | — | 8 % |
| 20,000 (mi catálogo) | 294.68 | 2.79 | 9 % | 0.080 | 1.13 | 11 % |
| 40,000 | 510.16 | 1.73 | 6 % | 0.095 | 1.19 | 18 % |
| 80,000 | 1044.32 | 2.05 | 9 % | 0.106 | 1.11 | 22 % |

Las 3 repeticiones de cada celda están en `hitos/h2/resultado.txt`.

## Conclusión

1. De 10 000 a 80 000 productos (8 veces más), la lista pasó de 105.61 a 1044.32 ms (unas 9.9 veces) y el diccionario de 0.071 a 0.106 ms (unas 1.5 veces). La lista se degrada con n y el diccionario casi no.
2. Esperaba cerca de ×2 por fila en la lista (O(n)). Dio ×2.79, ×1.73 y ×2.05, con promedio de ×2.15 por duplicación: la tendencia coincide con O(n), pero cada fila se desvía. No sé si el ×2.79 es un efecto real (por ejemplo, la memoria caché del procesador) o ruido; no lo comprobé. Algo parecido vi en la práctica C4.
3. El diccionario tarda décimas de milisegundo, cerca del límite de lo que se mide bien, y su ruido llega a 22 %. Sus razones (×1.13, ×1.19, ×1.11) son un poco mayores que 1, pero con 3 repeticiones no distingo un crecimiento pequeño real de ruido.
4. La tabla es coherente con O(n) frente a O(1) promedio, aunque no exacta. Para afinar el diccionario haría falta más repeticiones o más ventas por corrida.

## Qué pasa a escala

Con mi catálogo real (20 000 productos), la lista tarda unos 0.3 ms por venta (294.68 ms entre 1 000 ventas) y el diccionario una fracción mínima de eso. **Ninguna de las dos diferencias la nota un cajero por separado**: el costo importa cuando n crece o cuando se repite miles de veces. Lo que sí duele hoy es validar el catálogo en O(n²), que en H1 tardó unos 20 s.

Estimación hacia n más grande (**es una extrapolación, no una medición**):

- **Lista con n = 320 000** (4 × 80 000): si sigue siendo lineal, entre unos 4 200 y 4 800 ms por 1 000 ventas (×4 o ×2.15², partiendo de 1044.32 ms).
- **Diccionario con n = 320 000:** debería seguir en décimas de milisegundo, pero la caché podría cambiarlo y no lo comprobé.
- **Validar duplicados con n = 200 000** (10 × 20 000): el trabajo se multiplica por 100, unos 2 000 s con la versión ingenua (también extrapolado desde H1). Con un conjunto, el trabajo se multiplica por 10.

Medición de escala grande en mi PC (cambié `TAMANOS` en `medicion.py` a `[80_000, 160_000, 320_000]` y la ejecuté):

```
(pega aquí la salida de tu PC)
```

## Cómo reproducir

```
python hitos/h2/medicion.py
```

## Ayuda recibida

La estructura de este documento la planteé con ayuda de Claude (IA). Las mediciones las ejecuté yo en mi PC y las cifras de las tablas son las de mi equipo.
