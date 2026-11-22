vladimir Garcia Rojas

# P2.3 - Medición: ReceptorIngenuo vs ReceptorMejorado

## Qué se mide

La función `EjecutarCarga`: llegan **n pedidos** y después se **preparan los n**. Los plazos se repiten en ciclo (15, 30, 45, 60, 75 y 90 minutos).
Cada corrida usa un receptor nuevo y vacío, y crearlo no entra en el tiempo medido.

- **Ingenua:** `ReceptorIngenuo`, lista simple.
- **Mejorada:** `ReceptorMejorado`, montículo mínimo (`PriorityQueue`) con prioridad (plazo, llegada) más un `HashSet` con los nombres pendientes.

## Protocolo

**1 corrida de calentamiento** (no se mide) + **3 corridas medidas** con `Stopwatch`, y se reporta el **promedio**. Se ejecuta en Release (`dotnet run -c Release`).
Tres tamaños que se duplican: n = 10 000, 2n = 20 000 y 4n = 40 000. Con 4n la ingenua tardó 1644 ms, dentro del rango pedido (0.5 a 20 segundos).
"Ruido" es (máximo − mínimo) / promedio entre las 3 corridas medidas.

Equipo: [COMPLETAR: versión de .NET (`dotnet --version`), Windows y procesador].

## El O que declaré (ver `eleccion.md`)

| | Por operación | Carga completa (n registros + n preparaciones) | Esperado al duplicar n |
|---|---|---|---|
| Ingenua | `PrepararSiguiente` es O(n) | n × O(n) = **O(n²)** | cerca de **×4** |
| Mejorada | `Registrar` y `PrepararSiguiente` son O(log n) | n × O(log n) = **O(n log n)** | un poco más de **×2** (alrededor de ×2.1) |

## Resultados

| n | Ingenua: ms (promedio) | Ingenua: veces vs fila anterior | Ingenua: ruido | Mejorada: ms (promedio) | Mejorada: veces vs fila anterior | Mejorada: ruido |
|---|---|---|---|---|---|---|
| 10,000 | 110.70 | — | 19 % | 8.635 | — | 30 % |
| 20,000 | 482.10 | 4.36 | 9 % | 5.972 | 0.69 | 51 % |
| 40,000 | 1643.52 | 3.41 | 5 % | 9.602 | 1.61 | 29 % |

Las 3 corridas medidas de cada celda (ms):

| n | Ingenua | Mejorada |
|---|---|---|
| 10,000 | 108.52 / 122.15 / 101.41 | 7.881 / 7.723 / 10.300 |
| 20,000 | 465.63 / 473.86 / 506.80 | 7.335 / 6.309 / 4.272 |
| 40,000 | 1688.13 / 1607.82 / 1634.60 | 11.045 / 9.521 / 8.240 |

## Conclusión

1. **Ingenua:** sí se comporta como el O(n²) que declaré. Al duplicar n tardó ×4.36 y ×3.41 (promedio ×3.85) frente al ×4 esperado, con un ruido de 5 % a 19 %: pasó de 110.70 a 1643.52 ms con 4 veces más pedidos.
2. **Mejorada:** mis datos **no confirman** O(n log n). Esperaba un poco más de ×2 por fila y obtuve ×0.69 y ×1.61; con n = 20 000 tardó menos que con 10 000, algo que ningún O permite. Con tiempos de pocos milisegundos y un ruido de 29 % a 51 %, el ruido tapa la tendencia (posibles causas: la compilación JIT o el recolector de basura; no lo comprobé). Lo que sí se ve es que con 40 000 pedidos es unas 171 veces más rápida que la ingenua, y que no crece como una curva cuadrática. Para ver el n log n haría falta medirla con tamaños mucho mayores.
3. **Ruido:** con solo 3 corridas medidas, el ruido de la mejorada es demasiado grande para leer cada razón por separado; la ingenua, al tardar cientos de milisegundos, sale mucho más estable.
