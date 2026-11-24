# H3 - ¿Voraz o dinámica? Caso: tienda (minimarket)

## 1. Qué decisión se repite y qué resultado quiero optimizar

Reviso los dos procesos de H1/H2 y uno que ya existe en la tienda pero no había modelado.

| Proceso | ¿Hay una decisión que se repite? | ¿Hay un resultado a optimizar? |
|---|---|---|
| Detectar códigos duplicados | No: es una pasada que responde "¿ya existe este código?" | No: la respuesta es sí o no, no hay mejor ni peor |
| Buscar un producto por código | No: es una consulta | No: se trata de encontrar, no de elegir entre opciones |
| **Dar cambio al cliente** | **Sí: en cada venta (~500 al día) elijo qué moneda o billete entregar a continuación** | **Sí: la menor cantidad de monedas y billetes** |

**Conclusión sobre H1/H2:** ni voraz ni dinámica aplican a duplicados ni a búsqueda. Son problemas de pertenencia y acceso por clave, y se resuelven con la estructura de datos (diccionario), que ya medí en H2. Esos casos se quedan como están.

**Problema que uso para H3:** dar cambio. Es parte de registrar la venta, así que sigue siendo mi caso de la tienda.

## 2. ¿Alcanza elegir lo mejor ahora (voraz)?

Estrategia voraz: tomar siempre la denominación más grande que quepa en lo que falta devolver.

- Con las denominaciones de Bolivia (en centavos: 20000, 10000, 5000, 2000, 1000, 500, 200, 100, 50, 20, 10) la comprobé con `medicion_h3.py`: comparé el voraz contra el óptimo en los 10 000 montos posibles hasta 1 000 Bs y **no hubo ninguna diferencia**. Verifica contra las denominaciones que realmente usa tu tienda.
- No es una propiedad general. Con denominaciones {4, 3, 1} y monto 6, el voraz da 3 piezas (4+1+1) y lo óptimo son 2 (3+3). Así que "alcanza" depende del sistema de monedas, no del algoritmo.

## 3. ¿Hay subproblemas que se repiten (dinámica)?

Sí, en la formulación: `cambio(m) = 1 + min(cambio(m - d))` para cada denominación `d`. Calcular `cambio(m)` reutiliza `cambio(m - d)` de otros montos, y esos mismos subproblemas aparecen en muchas ventas. La tabla guarda cada uno una sola vez.

## 4. Veredicto

**Voraz**, para mi caso con las denominaciones de Bolivia: da lo óptimo y es mucho más barato. La dinámica es correcta también, pero paga una tabla que no necesito.

Cuándo cambiaría a dinámica: si las denominaciones dejaran de ser un sistema donde el voraz acierta, o si la caja tuviera cantidad limitada de monedas (por ejemplo, un solo billete de 5 y ninguna moneda de 1: el voraz se queda sin cambio para 6 aunque 2+2+2 existe). Este segundo caso lo razono, no lo medí.

## 5. Comparación medida

Protocolo igual al de H2: 1 calentamiento + 3 repeticiones, promedio, semilla 42, 500 cambios por jornada, tamaño = monto máximo en centavos, duplicado en cada fila. La dinámica construye su tabla una vez por jornada y luego consulta; las dos terminan con las mismas piezas en cada cambio (columna "piezas iguales").

Salida de `python medicion_h3.py` en mi PC (Python 3.14.10 en Windows AMD64):

```
Denominaciones de Bolivia: montos revisados = 10,000, donde voraz != óptimo = 0
Contraejemplo [4, 3, 1], monto 6: voraz = 3 piezas, óptimo = 2 piezas

| n (monto máx., centavos) | Voraz: ms | veces vs anterior | ruido | Dinámica: ms | veces vs anterior | ruido | piezas iguales |
|---|---|---|---|---|---|---|---|
| 10,000 | 0.247 | — | 3 % | 5.010 | — | 3 % | sí |
| 20,000 | 0.264 | 1.07 | 13 % | 11.371 | 2.27 | 8 % | sí |
| 40,000 | 0.247 | 0.93 | 1 % | 23.242 | 2.04 | 2 % | sí |
| 80,000 | 0.246 | 1.00 | 2 % | 48.668 | 2.09 | 5 % | sí |
```

Qué esperar: el voraz casi no depende del tamaño (siempre recorre las mismas 11 denominaciones), y la dinámica crece con el monto máximo porque construye una tabla de ese tamaño.

**Lo que obtuve:**

1. **El voraz acierta con las denominaciones de Bolivia:** en los 10 000 montos revisados no hubo ninguna diferencia con el óptimo, y en las cuatro filas de la medición las dos estrategias dieron las mismas piezas en cada cambio (columna «piezas iguales»). Con {4, 3, 1} y monto 6 sí falla (3 piezas contra 2), así que el acierto depende de las denominaciones y no del algoritmo.
2. **El voraz no depende del tamaño:** 0.247, 0.264, 0.247 y 0.246 ms; las razones (×1.07, ×0.93, ×1.00) son ruido, con 13 % en la segunda fila.
3. **La dinámica se duplica con n:** de 5.010 a 48.668 ms, con razones de ×2.27, ×2.04 y ×2.09, coherente con una tabla cuyo tamaño crece con el monto máximo.
4. **Diferencia entre las dos:** con n = 80,000 la dinámica tarda unas 198 veces más que el voraz (48.668 contra 0.246 ms), y con n = 10,000 unas 20 veces.

Mis razones coinciden con lo esperado. Con 3 repeticiones puede haber ruido (13 % en una celda del voraz), pero la tendencia es clara y no cambia el veredicto: **voraz** para mi caso.
