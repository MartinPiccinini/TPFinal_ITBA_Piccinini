# Aplicación de Consultas de acciones

## Cómo correr el programa

El programa debe ser iniciado con cualquier aplicación que permita correr archivos de python como puede ser con lineas de comando.

Primero es necesario instalar los requerimientos que se encuentran en el archivo requirements.txt

Se debe ejecutar el archivo .py mediante powershell con el comando streamlit run y la ruta donde se ubica el archivo, por ejemplo:

```
>>> streamlit run C:\Users\nombre_usuario\Carpeta\programa_finanzas.py
```

Al iniciar el programa se abrirá una ventana nueva en el navegador predeterminado.

La aplicación contiene tres secciones donde se puede interactuar:
* Pedir Datos
* Ver tabla
* Visualizar


<p align="center">
    <img src="https://i.ibb.co/phSF5Ys/portada.png" width="500">
</p>

## Ejemplos de uso

Se detallan unos ejemplos de uso del programa

### Pedido de datos de una acción

En la primera sección se puede escribir dentro del campo "Ticker" la acción sobre la que se quiere solicitar información. En los dos campos inferiores se selecciona la fecha de inicio y la fecha de fin.

Al presionar el boton de "Pedir Datos" la aplicación pide los datos a la API y luego almacena los mismos en la base de datos.

<p align="center">
    <img src="https://i.ibb.co/Gc4KTvP/Pedir.png" width="500">
</p>


### Imprimir tabla de datos

Una vez que existan datos en la base, en la sección de "Ver tabla" se puede elegir la acción en el desplegable y al presionar el botón de "Tabular Datos" la aplicación devuelve una tabla con la fecha, precio de cierre, precio de apertura, precio máximo y precio mínimo. Esta tabla puede ser luego descargada como un csv dentro de la misma interfaz.

<p align="center">
    <img src="https://i.ibb.co/qjtfzkf/tabla.png" width="500">
</p>

### Visualizar gráficos

Una vez que existan datos en la base, en la sección de "Visualizar" se puede elegir la acción en el desplegable y el tipo de gráfico que se quiere ver. Al presionar el botón de "Visualizar Datos" se devuelve el solicitado.

Ejemplo de gráfico de lineas:
<p align="center">
    <img src="https://i.ibb.co/PFBqfWP/lineas.png" width="500">
</p>

Ejemplo de gráfico de velas:
<p align="center">
    <img src="https://i.ibb.co/qnw2v58/velas.png" width="500">
</p>


### Resumen de datos existentes en la base

En la sección desplegable de la izquierda, una vez que existan datos en la base, se mostrará una tabla con la información disponible en la base, mostrando los tickers existentes y el rango de fechas para cada uno.

<p align="center">
    <img src="https://i.ibb.co/qY6vLB8/resumen.png" width="500">
</p>