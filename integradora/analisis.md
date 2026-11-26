Vladimir Garcia Rojas

# Integradora - Análisis (I1): inventario de la tienda

Caso: minimarket con unos **20 000 productos** y unas **500 ventas por día** (cifras estimadas, las mismas de H1). Los datos de partida están en `h1/README.md` y `hitos/h2/inventario.md`.

## 1. Costos: la versión ingenua contra la elegida

Dos procesos duelen: validar el catálogo (códigos únicos) y buscar un producto por código al vender.

| Proceso | Ingenua | Elegida | Con n = 20 000 | Con n = 200 000 (cálculo, no medido) |
|---|---|---|---|---|
| Detectar duplicados | Comparar cada producto con los que le siguen: n(n-1)/2, **O(n²)** | Recorrer una vez y consultar un conjunto/diccionario: **O(n) promedio** | 199 990 000 comparaciones contra unas 20 000 consultas | ~20 000 millones de comparaciones (×100) contra ~200 000 consultas (×10) |
| Buscar un producto | Recorrer la lista: **O(n)**, en promedio n/2 comparaciones | Diccionario: **O(1) promedio** | ~10 000 comparaciones por búsqueda contra 1 consulta | ×10 en la lista, igual en el diccionario |
| Una jornada de búsquedas (~700) | 700 × n/2 | 700 consultas | ~7 000 000 comparaciones contra 700 consultas | ×10 en la lista |

Medido en mi PC con la versión lenta (H1): validar el catálogo tarda unos 20 s y cada búsqueda unos 1,4 ms. Si n se multiplica por 10, la validación se multiplicaría por 100 (unos 2 000 s, una extrapolación mía, no una medición).

El peor caso del diccionario es O(n) si muchas claves chocan en la misma posición; con códigos de texto normales es muy improbable, pero no es imposible.

## 2. Recurrencias

- **Detectar duplicados (ingenua).** Mi código es iterativo, pero su conteo equivale a esta recurrencia: `T(n) = T(n-1) + (n-1)`, con `T(1) = 0`. Al desarrollarla da n(n-1)/2, es decir O(n²).
- **Búsqueda binaria** (la alternativa que descarté en H2 y C4): `T(n) = T(n/2) + 1`, con `T(1) = 1`. Da log₂ n; con n = 20 000 son unos 15 pasos.
- **Dar cambio al cliente** (H3): `cambio(m) = 1 + min cambio(m - d)` sobre cada denominación d, con `cambio(0) = 0`. Llenar la tabla cuesta O(m · k), con k = 11 denominaciones.
- **Diccionario:** sin recurrencia, es un acceso directo por clave.

## 3. Contraejemplo del voraz, con números

El voraz toma siempre la denominación más grande que cabe. No siempre da lo óptimo:

- **Denominaciones {4, 3, 1} y monto 6.** Voraz: 4 + 1 + 1 = **3 piezas**. Óptimo: 3 + 3 = **2 piezas**.
- **Caja con monedas limitadas** (un billete de 5, tres monedas de 2, ninguna de 1) **y monto 6.** Voraz: toma el 5, le falta 1 y no tiene cómo darlo, así que falla. Existe la solución 2 + 2 + 2. Este caso lo razoné, no lo medí.

Con las denominaciones de Bolivia (en centavos: 20000, 10000, 5000, 2000, 1000, 500, 200, 100, 50, 20, 10) comparé el voraz contra la dinámica en los 10 000 montos posibles hasta 1 000 Bs y no hubo ninguna diferencia (`hitos/h3/medicion_h3.py`). Es una comprobación por cálculo, no una demostración.

## 4. Estrategia

- **Detectar duplicados y buscar por código:** aquí no hay un resultado que optimizar entre varias opciones (es "¿existe?" y "¿dónde está?"), así que ni voraz ni dinámica aplican. La estrategia es **cambiar la forma de guardar los datos** para no comparar cada par: recordar lo ya visto en una tabla hash y gastar algo de memoria para ganar tiempo.
- **Dar cambio:** **voraz**, porque con las denominaciones reales da lo óptimo y es mucho más barato que la dinámica (en H3, unas 198 veces más rápido con n = 80 000). Cambiaría a dinámica si las denominaciones dejaran de comportarse así o si la caja tuviera monedas limitadas.

## 5. Estructura

**Diccionario `codigo -> Producto`**, porque la operación dominante es buscar por clave (~700 veces al día, más de 50 veces cualquier otra).

Alternativas que descarté:
- **Lista ordenada con búsqueda binaria:** buscar sería O(log n), peor que O(1), e insertar y borrar costarían O(n).
- **Árbol balanceado:** O(log n) y da orden, siguiente y rango, pero en mi trabajo diario no uso ninguno de los tres.

Lo que pierdo: algo más de memoria y el orden. Si la tienda empezara a consultar rangos de códigos, cambiaría a un árbol balanceado o a una lista ordenada con `bisect`.

## 6. Lo que todavía no resuelve

- El reporte ordenado por código sigue costando O(n log n) (ordenar las claves una vez al día).
- Con muchas colisiones, el diccionario se degrada hacia O(n); no lo medí.
- En mis mediciones hubo un salto que no sé explicar (×2,79 en la primera duplicación de H2, que se repite en C4); podría ser la caché del procesador, pero no lo comprobé.
- El caso de monedas limitadas lo razoné, no lo medí.
