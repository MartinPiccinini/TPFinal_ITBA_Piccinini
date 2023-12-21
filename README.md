# Aplicación de Consultas de Acciones

## Cómo correr el programa

El programa debe ser iniciado con cualquier aplicación que permita correr archivos de python como puede ser con lineas de comando.

Por ejemplo con lineas de comando de Windows, usando el path donde se encuentra guardado el archivo .py:

```
>>> python C:\Users\nombre_usuario\Carpeta\programa_finanzas.py
```

Asegurarse de que python esté usando las librerías dentro del archivo **requirements.txt**

Al iniciar el programa, se puede consultar los comandos permitidos al escribir el comando "Info"

## Ejemplos de uso

Se detallan unos ejemplos de uso del programa

### Pedido de datos de una acción

```
>>> Introduzca un comando ("Info", "Pedir datos", "Resumen", "Tabla", "Graficar","Cerrar"): Pedir datos
>>> Escriba el ticker a buscar (ejemplo: AAPL): AAPL
>>> Escriba la fecha inicial a buscar (formato YYYY-MM-DD): 2023-12-01
>>> Escriba la fecha final a buscar (formato YYYY-MM-DD): 2023-12-20
>>> Pidiendo datos...

>>> Se guardaron los datos correctamente.
```

### Imprimir tabla de datos

Mostrar una tabla con los datos mediante el comando "Tabla"

```
>>> Introduzca un comando ("Info", "Pedir datos", "Resumen", "Tabla", "Graficar","Cerrar"): Tabla
>>> Ingrese el ticker a consultar:AAPL

>>> Los datos de AAPL son los siguientes:

    Precio       Fecha
0   191.24  2023-12-01
1   189.43  2023-12-04
2   193.42  2023-12-05
3   192.32  2023-12-06
4   194.27  2023-12-07
5   195.71  2023-12-08
6   193.18  2023-12-11
7   194.71  2023-12-12
8   197.96  2023-12-13
9   198.11  2023-12-14
10  197.57  2023-12-15
11  195.89  2023-12-18
12  196.94  2023-12-19
13  194.83  2023-12-20
```

### Graficar de datos

Mediante el comando "Graficar" el programa abre una nueva ventana donde se grafica un gráfico evolutivo de la acción seleccionada.

```
>>> Introduzca un comando ("Info", "Pedir datos", "Resumen", "Tabla", "Graficar","Cerrar"): Graficar
>>> Ingrese el ticker a graficar: AAPL
```
En el caso que se ilustra en este documento, se visualizará la siguiente imagen:

<p align="center">
    <img src="https://i.ibb.co/Srdhkzx/Figure-1.png" width="500">
</p>

### Resumen de base de datos
Por último el programa tambien permite consultar todos los tickers disponibles en la base de datos y el rango de fechas disponible para cada ticker, usando el comando "Resumen"

```
>>> Introduzca un comando ("Info", "Pedir datos", "Resumen", "Tabla", "Graficar","Cerrar"): Resumen


>>> Los tickers guardados en la base de datos son:

  ticker fecha_inicial fecha_final
0   AAPL    2023-12-01  2023-12-20
1   MSFT    2023-12-01  2023-12-20
2   NVDA    2023-11-15  2023-12-20
3    SPY    2023-11-01  2023-12-20
```
