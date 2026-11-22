 vladimir Garcia Rojas
# P2.1 - Elegir: receptor de pedidos

## Mi elección

Uso **dos estructuras que trabajan juntas**:

- **Montículo mínimo** (`PriorityQueue` en C#) con prioridad **(plazo, llegada)**. Siempre tiene en la raíz el pedido más urgente, y el desempate por llegada cumple la regla "si empatan, el que llegó antes".
- **Conjunto hash** (`HashSet<string>`) con los nombres de los pedidos pendientes, para responder "¿sigue pendiente?" sin recorrer nada.

`Registrar` agrega a las dos. `PrepararSiguiente` saca la raíz del montículo y quita ese nombre del conjunto. Como los nombres son únicos y solo se saca el más urgente (nunca uno del medio), las dos estructuras se mantienen iguales sin trucos.

## Tabla de operaciones (n = 120 000)

| Operación | Veces por jornada | Estructura que uso | Costo O | Lista simple |
|---|---|---|---|---|
| `Registrar` | 120 000 | Montículo + conjunto | O(log n) + O(1) promedio = **O(log n)** | O(1) |
| `PrepararSiguiente` | 120 000 | Montículo (sacar la raíz) + quitar del conjunto | O(log n) + O(1) promedio = **O(log n)** | O(n) |
| `EstaPendiente` | 40 000 | Conjunto hash | **O(1)** promedio | O(n) |
| `Pendientes` | No se indica; la trato como consulta ocasional | Contador (`Count`) | **O(1)** | O(1) |

## Por qué no sirve la lista simple (con números)

Cuento operaciones elementales (comparaciones o inserciones), no segundos. Tomo el peor caso de la lista: los 120 000 pedidos llegan antes de empezar a prepararse, como en `EjecutarCarga`, y log2(120 000) ≈ 17.

| | Lista simple | Mi estructura |
|---|---|---|
| `Registrar` × 120 000 | 120 000 | 120 000 × 17 ≈ 2.0 millones |
| `PrepararSiguiente` × 120 000 | n(n+1)/2 ≈ **7 200 millones** (cada preparación recorre todos los pendientes que quedan) | 120 000 × 2 × 17 ≈ 4.1 millones |
| `EstaPendiente` × 40 000 | hasta 40 000 × 120 000 = **4 800 millones** | 40 000 |
| Conjunto (agregar y quitar) | — | 2 × 120 000 = 0.24 millones |
| **Total de la jornada** | **hasta ≈ 12 000 millones** | **≈ 6.4 millones** |

En el peor caso, la lista hace casi 2 000 veces más trabajo, y solo `PrepararSiguiente` ya son unas 1 100 veces más. Además, cada `RemoveAt` de la lista desplaza elementos, lo que suma más trabajo que no conté.
Si los pedidos se prepararan a medida que llegan, habría menos pendientes a la vez y la diferencia sería menor, pero seguiría creciendo con n.

## Una condición en la que cambiaría de opinión

Si el sistema tuviera que **cancelar un pedido o cambiar su plazo**: el montículo no saca bien un elemento del medio. Cambiaría a un **árbol balanceado ordenado por (plazo, llegada)** junto con un diccionario de nombre a pedido, con costo O(log n) para registrar, preparar, cancelar y cambiar el plazo.
También volvería a la lista simple si n fuera muy pequeño (unas decenas de pedidos), porque sería más simple y igual de rápida.
