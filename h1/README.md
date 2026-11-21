# H1 - Proceso lento a optimizar: inventario de la tienda

- **Proceso:** validación del catálogo de productos y registro de ventas en el inventario de un minimarket.
- **Quién lo sufre:** el encargado de inventario, que espera la validación del catálogo, y el cajero, que espera la búsqueda de cada producto al vender.
- **Problema:** cada código de producto debe ser único, pero al cargar el catálogo (digitado o importado de proveedores) aparecen códigos repetidos.
- **Cómo se hace hoy:** se compara cada producto con todos los demás para encontrar repetidos, y cada venta busca el producto recorriendo la lista desde el inicio.
- **Datos que maneja:** unos 20 000 productos en el catálogo y unas 500 ventas por día (cifras estimadas para este caso).
- **Cuánto tarda hoy:** validar el catálogo toma unos 20 s (cerca de 200 millones de comparaciones) y cada búsqueda unos 1,4 ms, medido con la versión lenta del programa.
- **Consecuencia:** los duplicados provocan stock y precios inconsistentes y errores al facturar.
- **O de detectar duplicados hoy: O(n²).** Cada producto se compara con todos los que le siguen, lo que da n(n-1)/2 comparaciones; si n se multiplica por 10, el trabajo se multiplica por 100.
- **O de buscar un producto hoy: O(n).** En el peor caso la lista se recorre completa (n comparaciones) y en promedio la mitad; si n se multiplica por 10, la búsqueda tarda 10 veces más.
- **Qué se optimizará este mes:** la detección de duplicados y la búsqueda por código.
- **Estructura propuesta: diccionario y conjunto, O(1) promedio.** La tabla hash convierte el código en una posición con una función hash y va directo a ella, sin recorrer la lista (el peor caso, con muchas colisiones, sería O(n)).
- **Cómo se medirá:** comparaciones y tiempo en ms con n = 1 000, 10 000, 100 000 y 1 000 000 para búsqueda, comparando lista contra diccionario.
- **Evidencia:** muestra de 20 filas (abajo y en `muestra_datos.csv`), con los repetidos P001 y P005, y los programas `tienda_lento.py` y `tienda_rapido.py`.

## Muestra de datos (20 filas)

```csv
codigo,nombre,categoria,stock,precio
P001,Arroz 1kg,Abarrotes,50,9.50
P002,Azucar 1kg,Abarrotes,40,8.00
P003,Aceite 1L,Abarrotes,30,18.50
P004,Fideos 500g,Abarrotes,60,6.50
P005,Harina 1kg,Abarrotes,25,7.50
P006,Leche 1L,Lacteos,45,7.00
P007,Sal 500g,Abarrotes,70,3.00
P008,Cafe 250g,Bebidas,20,22.00
P009,Te 25 sobres,Bebidas,35,10.00
P010,Galletas,Snacks,80,2.50
P011,Atun en lata,Conservas,55,12.00
P012,Jabon,Limpieza,65,3.50
P013,Detergente 1kg,Limpieza,30,16.00
P014,Papel higienico,Limpieza,90,15.00
P015,Shampoo,Cuidado personal,25,20.00
P016,Pasta dental,Cuidado personal,40,11.00
P017,Gaseosa 2L,Bebidas,48,12.50
P018,Agua 2L,Bebidas,100,6.00
P001,Arroz 1kg,Abarrotes,20,9.50
P005,Harina 1kg,Abarrotes,10,7.50
```
