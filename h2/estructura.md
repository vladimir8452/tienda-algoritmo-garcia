# H2 - Estructura elegida

## Mi elección

**Diccionario (tabla hash) con el código como clave:** `dict` de Python, `codigo -> Producto`.
Para el reporte ocasional ordenado por código, se ordenan las claves en ese momento (`sorted`).

La estructura **ingenua** con la que la comparo es una **lista sin orden** de productos, recorrida de principio a fin.

## Costo de cada operación

| Operación | Veces por día | Lista sin orden (ingenua) | Diccionario (elegida) |
|---|---|---|---|
| **Buscar por clave** | ~700 | O(n): recorre la lista hasta encontrarlo | **O(1) promedio** |
| **Insertar** (validando que no exista) | ~10 | O(n): hay que buscar si el código ya está | **O(1) promedio** (amortizado) |
| **Borrar** | ~2 | O(n): buscarlo y luego quitarlo | **O(1) promedio** |
| **Recorrer en orden** | ~1 | O(n log n): ordenar | O(n log n): ordenar las claves |
| El menor o el siguiente | 0 | O(n): recorrer todo | O(n): recorrer todo |
| Un rango | 0 | O(n): recorrer todo | O(n): recorrer todo |

El peor caso del diccionario es O(n) si muchas claves chocan en la misma posición, pero con códigos de texto normales es muy improbable.

## Por qué esta elección

- Lo que hago casi siempre es **buscar por clave** (~700 veces al día), y ahí el diccionario pasa de recorrer la lista a ir directo al producto: O(n) pasa a O(1) promedio.
- **Insertar** también mejora, porque validar que el código no exista deja de ser un recorrido completo.
- Lo que el diccionario hace mal (orden, siguiente, rango) es justo lo que casi no uso. El reporte ordenado es una vez al día y cuesta O(n log n) igual en las dos estructuras.
- Consideré un **árbol balanceado** o una **lista ordenada con búsqueda binaria**. Dan búsqueda en O(log n) y ofrecen orden, siguiente y rango, pero no los necesito, y buscar sería más lento que O(1). La lista ordenada, además, hace costoso insertar y borrar, O(n).
- Lo que pierdo: algo más de memoria y el orden. Si la tienda empezara a consultar rangos de códigos, cambiaría a un árbol balanceado o a una lista ordenada con `bisect`.
