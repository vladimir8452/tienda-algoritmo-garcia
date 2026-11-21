# H2 - Inventario del caso: tienda (minimarket)

## Los datos de mi caso

Catálogo de productos de un minimarket. Cada producto es un registro con estos campos:

| Campo | Ejemplo | Nota |
|---|---|---|
| `codigo` | P017 | **Clave única**, texto. Es por lo que se busca. |
| `nombre` | Gaseosa 2L | |
| `categoria` | Bebidas | |
| `stock` | 48 | Cambia con cada venta. |
| `precio` | 12.50 | |

Volumen (cifras estimadas, las mismas de H1): unos **20 000 productos** y unas **500 ventas por día**.
La muestra de 20 filas está en `h1/muestra_datos.csv`.

## Operaciones que hago y cuántas veces

| Operación | Para qué la uso en la tienda | Veces por día (estimadas) |
|---|---|---|
| **Buscar por clave** | Encontrar el producto por su código al registrar una venta y al consultar su stock | ~700 (500 ventas + ~200 consultas) |
| **Insertar** | Dar de alta un producto nuevo, validando que su código no exista ya | ~10 |
| **Borrar** | Dar de baja un producto descontinuado | ~2 |
| **Recorrer en orden** | Reporte de inventario ordenado por código | ~1 |
| **El menor o el siguiente** | No lo necesito en el trabajo diario | 0 |
| **Un rango** | No consulto "los productos entre P100 y P200" | 0 |

## Cuáles hago más veces

1. **Buscar por clave** es, por mucho, la operación dominante (~700 al día, más de 50 veces cualquier otra).
2. **Insertar** (con validación de duplicados) es la segunda, aunque pocas veces al día.
3. Borrar y recorrer en orden son ocasionales, y el menor/siguiente y los rangos no se usan.

Por eso mi caso es de **acceso por clave**: no necesito orden ni rangos en el trabajo diario.
El orden solo aparece en un reporte ocasional, que se puede resolver ordenando en ese momento.
