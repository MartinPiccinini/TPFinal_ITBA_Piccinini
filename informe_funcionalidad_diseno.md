# Informa de funcionalidad y diseño
## Introducción
En este informe se explican las decisiones tomadas al momento de desarrollar la aplicación y se da detalle de algunas partes del código y módulos.

## Funcionalidades

El programa corre en su totalidad con lineas de comando, aunque en una futura version espero poder implementarlo con una interfaz de usuario más amigable, como puede ser streamlit.

Se implementaron las funcionalidades mínimas requeridas por el TP final, que son la posibilidad de pedir datos a una api financiera (en este desarrollo se utilizó la api de Polygon), los cuales se guardan en una base de datos de SQLite mediante el uso de la librería **sqlite3**, haciendo bastante uso además de la librería **pandas** para la escritura de datos desde un dataframe a la base de datos y la escritura de datos desde la base a un dataframe, el cual posteriormente se usa para imprimir los resultados. 

Además el programa permite graficar cualquier acción solicitada con el uso de la librería **matplotlib**.

Una pequeña funcionalidad extra es que el programa permite imprimir los datos en forma de tabla desde la aplicación misma, usando el comando "Tabla".

## Módulos

Para facilitar la escritura de código dentro del programa principal se crearon dos módulos donde se definieron las funciones que se usan dentro del programa, siendo los módulos los siguentes:

* funciones_main.py
* funciones_sql.py

### funciones_main
Este módulo concentra las funciones más relacionadas con la interacción con el api de polygon mediante la libreria **requests**, lo relacionado a transformaciones de datos mediante la librería **pandas** y visualización de datos mediante la librería **matplotlib**.

### funciones_sql
Este módulo concentra las funciones relacionadas con el uso de la librería **sqlite3** (y en parte tambien pandas). Acá hay funciones para la creación de la base de datos inicial, escritura de datos dentro de la base de datos (cuidando de no duplicar datos que ya puedan existir dentro de la base - a detallarse más adelante), consulta de la base de datos y bajada de la misma a dataframes de pandas.

Tambien una función que se usa de control dentro del código principal para considerar errores que puedan venir del usuario.

## Detalles
En esta sección detallo algunas líneas de código que me pareció relevante detallar. No se va a detallar funcion por funcion ni linea por linea, pero se dejaron comentarios en el código y en los módulos para ello.


Se consideró el error que puede venir del usuario cuando por ejemplo usando el comando "Resumen" se pida imprimir el resumen cuando la base de datos está vacia, informando que la misma no tiene datos todavía y se debe solicitar los mismos con otro comando. Para esto se crea un booleano al principio del código para determinar si existen o no. Esta lógica tambien es usada en los comandos "Tabla" y "Resumen"

```python
case "resumen": 
    if hay_tickers: 
        print('\n')
        f_sql.print_summary() 
        print('\n')
    else: 
        print('\nTodavía no se guardaron datos dentro de la base de datos.\nUse el comando "Pedir datos" para empezar a agregar datos que pueda visualizar\n')
```

Tambien se consideró el error que puede surgir de intentar imprimir una tabla o graficar un ticker que no existe en la base de datos. Para esto, dentro del código se va actualizando una lista con los tickers que sí existen en la base de datos y si no está dentro de esta lista, se informa al usuario de ello y se sugiere que se pidan datos del ticker. Tambien se usa cuando se entra al comando "Graficar".

```python
if hay_tickers: 
    tick_v = input('Ingrese el ticker a consultar:').upper() 
    if tick_v in l_tickers: # check si existe el ticker
        print(f'\nLos datos de {tick_v} son los siguientes:\n') 

        print(f_sql.query_ticker(tick_v))
    else:
        print('\nEl ticker solicitado no se encuentra en la base de datos, solicite los datos con el comando "Pedir datos"\n')
else:
    print('\nTodavía no se guardaron datos dentro de la base de datos.\nUse el comando "Pedir datos" para empezar a agregar datos que pueda visualizar\n') 
```

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
## Funcionalidades
Por temas de tiempo no llegué a implementear otras funcionalidades que quería, pero tengo en mente hacerlo en un futuro, como puede ser:

* Considerar error al consultar un ticker que no exista en la base de datos de Polygon.
* Visualizar el programa en una interfaz con por ejemplo streamlit.
* Crear gráfico tipo velas con las columnas no usadas del request a la api.
* Comparar fechas ya existentes de tickers que existan en la base para solo hacer gets de las fechas que no existen en la base