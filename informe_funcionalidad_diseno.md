# Informa de funcionalidad y diseño
## Introducción
En este informe se explican las decisiones tomadas al momento de desarrollar la aplicación y se da detalle de algunas partes del código y módulos.

## Funcionalidades

La aplicación se desarrolló para ser visualizada e interactuada con el uso de **streamlit**, insertando las funcionalidades en elementos dentro de la interfaz en el navegador que usa streamlit al momento de ejecutar la aplicación.

Se implementaron las funcionalidades mínimas requeridas por el TP final, que son la posibilidad de pedir datos a una api financiera (en este desarrollo se utilizó la api de Polygon), los cuales se guardan en una base de datos de SQLite mediante el uso de la librería **sqlite3**, haciendo bastante uso además de la librería **pandas** para la escritura de datos desde un dataframe a la base de datos y la escritura de datos desde la base a un dataframe, el cual posteriormente se usa para imprimir los resultados. 

Además el programa permite graficar cualquier acción solicitada con el uso de la librería **matplotlib**. Un adicional es que se incluyó la posibilidad de graficar la acción en un gráfico de tipo "velas".

Una pequeña funcionalidad extra es que el programa permite imprimir los datos en forma de tabla desde la aplicación misma, usando el comando "Tabla".

## Módulos

Para facilitar la escritura de código dentro del programa principal se creaó un módulos donde se definieron las funciones que se usan dentro del programa, llamado funciones_app.py.

Este módulo concentra las funciones relacionadas con la interacción con el api de polygon mediante la libreria **requests**, lo relacionado a transformaciones de datos mediante la librería **pandas** y visualización de datos mediante la librería **matplotlib**, además se definieron funciones relacionadas con el uso de la librería **sqlite3** (y en parte tambien pandas). Acá hay funciones para la creación de la base de datos inicial, escritura de datos dentro de la base de datos (cuidando de no duplicar datos que ya puedan existir dentro de la base - a detallarse más adelante), consulta de la base de datos y bajada de la misma a dataframes de pandas.

## Detalles
En esta sección comparto algunas líneas de código que me pareció relevante resaltar. No se va a detallar funcion por funcion ni linea por linea, pero se dejaron comentarios en el código y en los módulos para ello.


Como se implementó


En el código se agregaron variables globales que chequean si existen datos en la base y se usan repetidamente para ocultar secciones que no deberían verse si no hay datos o para deshabilitar funcionalidades que no deberían usarse si no existen acciones en la base de datos, como puede ser la tabulación de datos de una acción o la visualización de una acción.

Dentro del código principal de la aplicación se usa la función check_tickers() para asignar valores a dos variables:
* booleano que chequea la existencia de tickers dentro de la base, asignando True si hay datos o False si no los hay
* una lista de tickers disponibles en la base. Esta luego se usa para las secciones de tabulación y de visualización, en los desplegables donde el usuario puede elegir el ticker a tabular/visualizar, para prevenir un error que pueda surgir de querer realizar alguna de esas interacciones con una acción que no exista en la base.

```python
hay_tickers, l_tickers = f_module.check_tickers()
```

En el caso de los botones que se crearon para tabular y graficar, se usó la variable "hay_tickers" dentro del parámetro de la función que crea un boton que permite habilitar/deshabilitar el mismo (parámetro "disabled"). Cuando existen datos en la base la variable devolverá un True, haciendo que el parámetro sea disabled = False, por lo tanto habilitando la posibilidad de presionar el botón.

```python
if st.button("Tabular Datos", key='b_tabular', disabled = not hay_tickers):
```

Como se mencionó tambien se usa la variable l_tickers para que el usuario sólo pueda elegir únicamente las acciones que existan en la base, en este caso asignando la variable al parámetro "options".

```python
tick_v = st.selectbox(
label = 'Ticker',
options = l_tickers, #la lista de los tickers presentes en la base
key = 'dd_graf'
)
```

---

También se consideró el error que pudiera surgir de un usuario que intente pedir datos por fuera del rango de fechas permitido por la API (considerando que sólo se usa la version gratis de la misma). En este caso sólo se permite como fecha máxima la fecha anterior al día actual y como fecha mínima dos años antes de la fecha actual.

Estas se asignan a las variables "date_min_allowed" y "date_max_allowed" mediante la función "date_range_allowed()" dentro del módulo. Estas luego se usan en los selectores de fechas dentro de la sección "Pedir Datos"


```python
desde = st.date_input(
                'Desde :date:',
                value=date_max_allowed,
                key='desde',
                min_value=date_min_allowed,
                max_value=date_max_allowed
                ) 

hasta = st.date_input(
                'Hasta :date:',
                value=date_max_allowed,
                key='hasta',
                min_value=date_min_allowed,
                max_value=date_max_allowed
                ) 
```
---
Para minimizar la cantidad de pedidos que se hagan a la API, se consideró la posibilidad de chequear si los datos solicitados dentro de la sección "Pedir Datos" ya existen en la base de datos, permitiendo informar al usuario si ya existen dichos datos (previniendo una consulta innecesaria a la API) o acotando la consulta solo a las fechas que no existen ya en la base de datos.

Dentro de la función "get_stock_prices()" se agregó la funcionalidad de chequear si los datos solicitados ya existen cuando se devuelve un booleano que viene como True si los datos pedidos se encuentran en la base, la cual se asigna a la variable "bool_check_dates" dentro del código principal, que si resulta como True, devolverá un mensaje avisando al usuario de la situación.

Además la función "get_stock_prices()" devuelve como parte de su return un conteo de la cantidad de querys que devolvió la consulta a la API, siendo que si esta solo trajo 0 querys el pedido por parte del usuario se hizo con un ticker que no existe, entonces se chequea esto dentro del código principal con la variable "q_count"

```python
dicc, q_count, bool_check_dates  = f_module.get_stock_prices(tick,desde,hasta,key_api)

if bool_check_dates:
    'El pedido ya existe en la base de datos'

elif q_count > 0: #chequea que el request haya traido datos
    
    'Pidiendo Datos'

    df_request = f_module.clean_request(dicc) #se guarda en un dataframe los datos transformados desde el diccionario anterior

    f_module.temp_table(df_request) # crea tabla temporaria en base para incluir los datos que se solicitaron
    
    df_comp = f_module.compare() #compara datos nuevos con los que estan dentro de la base y guarda en un dataframe solo los datos que no se encuentran en la base

    f_module.append_entries(df_comp) #escribe los datos nuevos en base de datos

    hay_tickers, l_tickers = f_module.check_tickers()

    'Datos Guardados'

else:     # si el request no trajo datos se informa al usuario
    f'No existen datos para el ticker {tick}, pruebe con otro ticker.'

```


---

Por último, a raíz de querer evitar duplicación de datos, busqué en internet cómo podría hacer con SQL esto y adapté lo que aprendí en tres funciones.


La función temp_table se usa para mandar los datos a una tabla secundaria dentro de la base de datos.
```python
def temp_table(dataframe):
    '''
    Función que crea una tabla temporaria en la base de datos para incluir los datos que se hayan consultado a la api
    '''

    con = sqlite3.connect('stock_data.db') # crea conexion a base de datos
    
    dataframe.to_sql(name="tabla_temp", con=con, if_exists='replace', index=False) #sube dataframe creado por el request a tabla temporaria
    
    con.close() #cierra conexion
```

Esta tabla secundaria se usa para comparar los datos que salieron de la más reciente consulta a la api con los datos que ya existen en la base, y se queda solo con los datos nuevos, es decir, los que no existen en la base.
```python
def compare():
    '''
    Función que hace una consulta a la base de datos, y que devuelve un dataframe solo con aquellos datos que
    no se encuentren ya en la base
    '''

    con = sqlite3.connect('stock_data.db') # crea conexion

    # crea consulta para comparar los datos que ya estan en la base y los nuevos traidos del request, para que devuelva solo los que no estan ya en la base
    query = '''
        SELECT c, ticker, date FROM tabla_temp                     
        EXCEPT 
        SELECT c, ticker, date FROM stock_data;
        '''
    
    # se los baja a un datafame, que tiene solo los datos nuevos
    new_entries = pd.read_sql(query, con=con)
    
    con.close() #cierra conexion

    return new_entries
```

Los datos nuevo luego son escritos en la table principal, sobre la que se realizan las consultas SQL para imprimir las tablas o graficar los datos.
```python
def append_entries(dataframe):

    '''
    Funcion que agrega aquellos datos nuevos que no se encuentren en la base de datos
    '''

    con = sqlite3.connect('stock_data.db')
    
    # por ultimo se usa el dataframe creado en la funcion compare() y se insertan los datos en la tabla principal, por medio de un append
    dataframe.to_sql(name="stock_data", con=con, if_exists='append',index=False)
    
    con.close()
```
