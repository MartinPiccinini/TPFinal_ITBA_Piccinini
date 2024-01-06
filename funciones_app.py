import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta
import sqlite3
import pandas as pd
import os
plt.style.use('dark_background')

#region SQL

def query_dates(ticker_req: str):

        con = sqlite3.connect('stock_data.db')

        query = f'''
                SELECT date
                FROM stock_data
                WHERE ticker = "{ticker_req}"
                ORDER BY date ASC
                '''

        df_dates_sql = pd.read_sql(query,con)

        con.close()

        min_date_f = min(list(df_dates_sql.date))
        max_date_f = max(list(df_dates_sql.date))

        return min_date_f, max_date_f


def create_database():
    '''
    Funcion que crea base de datos que se utilizará en el resto del código
    '''

    if not os.path.exists('stock_data.db'): #chequea si ya existe la base de datos     
        # conecta a la base de datos de SQLite (la crea si no existe)
        con = sqlite3.connect('stock_data.db')
        
        # crea el cursor para ejecutar comandos
        cursor = con.cursor()
        
        # define la consulta sql para crear la tabla
        crear_tabla = '''
        CREATE TABLE stock_data(
            
            ticker TEXT NOT NULL,
            c FLOAT NOT NULL,
            o FLOAT NOT NULL,
            h FLOAT NOT NULL,
            l FLOAT NOT NULL,
            date DATE NOT NULL
        );
        '''
        
        # ejecuta la consulta
        cursor.execute(crear_tabla)
        
        # commit de cambios y cierra la conexion
        con.commit()
        con.close()

def check_tickers():
    '''
    Devuelve "true" si ya existen tickers dentro de la base de datos
    "false" si no existe ningun ticker

    Ademas devuelve una lista de los tickers presentes
    '''

    con = sqlite3.connect('stock_data.db') #crea conexion

    #consulta que se le hace a la base de datos
    query = f''' 
            SELECT 
            DISTINCT(ticker)
            FROM stock_data
            '''
    df_consulta = pd.read_sql(query,con) # se guarda la consulta en un dataframe, usando una funcion de pandas
    
    con.close() # cierra conexion

    return len(list(df_consulta.ticker)) > 0, list(df_consulta.ticker) # devuelve dos variables: booleano de si hay tickers o no en la base, lista de los tickers presentes

def temp_table(dataframe: pd.DataFrame):
    '''
    Función que crea una tabla temporaria en la base de datos para incluir los datos que se hayan consultado a la api
    '''

    con = sqlite3.connect('stock_data.db') # crea conexion a base de datos
    
    dataframe.to_sql(name="tabla_temp", con=con, if_exists='replace', index=False) #sube dataframe creado por el request a tabla temporaria
    
    con.close() #cierra conexion


def compare():
    '''
    Función que hace una consulta a la base de datos, y que devuelve un dataframe solo con aquellos datos que
    no se encuentren ya en la base
    '''

    con = sqlite3.connect('stock_data.db') # crea conexion

    # crea consulta para comparar los datos que ya estan en la base y los nuevos traidos del request, para que devuelva solo los que no estan ya en la base
    query = '''
        SELECT c, o, h, l, ticker, date FROM tabla_temp                     
        EXCEPT 
        SELECT c, o, h, l, ticker, date FROM stock_data;
        '''
    
    # se los baja a un datafame, que tiene solo los datos nuevos
    new_entries = pd.read_sql(query, con=con)
    
    con.close() #cierra conexion

    return new_entries

def append_entries(dataframe: pd.DataFrame):

    '''
    Funcion que agrega aquellos datos nuevos que no se encuentren en la base de datos
    '''

    con = sqlite3.connect('stock_data.db')
    
    # por ultimo se usa el dataframe creado en la funcion compare() y se insertan los datos en la tabla principal, por medio de un append
    dataframe.to_sql(name="stock_data", con=con, if_exists='append',index=False)
    
    con.close()

def print_summary():
    
    '''
    Función que imprime el resumen de cuales tickers se encuentran en la base de datos y el rango de fechas
    existente para cada ticker
    '''

    con = sqlite3.connect('stock_data.db')

    # consulta que trae los tickers unicos, y el maximo y minimo de fechas
    query = '''
            SELECT 
            DISTINCT(ticker) as Ticker, 
            MIN(date) as "Fecha Inicial", 
            MAX  (date) as "Fecha Final"
            FROM stock_data
            GROUP BY ticker
            ORDER BY ticker ASC
            '''
    
    return pd.read_sql(query,con) # imprime la tabla creade de la consulta

    con.close()

def query_ticker_close(ticker: str):

    '''
    Función que devuelve un dataframe del precio de cierre y fecha que se encuentran en la base de datos 
    segun el ticker que se especificó en el único argumento
    '''

    con = sqlite3.connect('stock_data.db')

    # consulta la base solo con el ticker seleccionado y ordena por el campo de fecha
    query = f'''
            SELECT 
            c as Precio,
            date as Fecha
            FROM stock_data
            WHERE ticker = '{ticker}'
            ORDER BY Fecha ASC
            '''
    df_consulta = pd.read_sql(query,con) # guarda consulta en un dataframe
    
    con.close()

    return df_consulta

def query_ticker_all(ticker: str):

    '''
    Función que devuelve un dataframe del precio de cierre y fecha que se encuentran en la base de datos 
    segun el ticker que se especificó en el único argumento
    '''

    con = sqlite3.connect('stock_data.db')

    # consulta la base solo con el ticker seleccionado y ordena por el campo de fecha
    query = f'''
            SELECT 
            c,
            o,
            h,
            l,
            date
            FROM stock_data
            WHERE ticker = '{ticker}'
            ORDER BY date ASC
            '''
    df_consulta = pd.read_sql(query,con) # guarda consulta en un dataframe
    
    con.close()

    return df_consulta

def query_ticker_all_viz(ticker: str):

    '''
    Función que devuelve un dataframe del precio de cierre y fecha que se encuentran en la base de datos 
    segun el ticker que se especificó en el único argumento
    Se cambian los nombres de las columnas para que sea más legible para el usuario
    '''

    con = sqlite3.connect('stock_data.db')

    # consulta la base solo con el ticker seleccionado y ordena por el campo de fecha
    query = f'''
            SELECT
            date as "Fecha", 
            c as "Precio Cierre",
            o as "Precio Apertura",
            h as "Precio Máximo",
            l as "Precio Mínimo"

            FROM stock_data
            WHERE ticker = '{ticker}'
            ORDER BY Fecha ASC
            '''
    df_consulta = pd.read_sql(query,con) # guarda consulta en un dataframe
    
    con.close()

    return df_consulta

#endregion


#region VIZ
def visualize_df(dataframe: pd.DataFrame,ticker_visualizado: str):
    '''
    Recibe un dataframe de pandas y devuelve un gráfico de linas con las fechas y el precio de venta de la accion
    Tambien recibe el nombre del ticker para incluir en el titulo del gráfico
    '''
    
    fig, ax = plt.subplots()
    ax.plot(dataframe.Fecha,dataframe.Precio, marker = ".", color='orange') # grafica con evolutivo
    plt.xticks(rotation=45, ha='right') # rota 45 grados los ticker del eje x
    ax.set_xticks(ax.get_xticks()[::2]) # hace que se muestre solo 1 de cada 2 ticks
    ax.set_facecolor("#161414")

    plt.title(f'Gráfico evolutivo de {ticker_visualizado}') # escribe titulo
    plt.xlabel("Fecha") # agrega titulo a eje x
    
    plt.ylabel("Precio") # agrega titulo a eje y
    plt.grid(axis = 'y', color='#453F3F',linestyle='--')

    return fig
    #plt.show() # linea para que se visualice el grafico al correr el programa

def candlestick_plot(dataframe: pd.DataFrame,ticker_visualizado: str):
    '''
    Recibe un dataframe de pandas y devuelve un gráfico tipo velas con las fechas y el precio de cierre, apertura, maximo y minimo
    de la accion
    Tambien recibe el nombre del ticker para incluir en el titulo del gráfico
    '''

    #create figure
    fig, ax = plt.subplots() #plt.figure()

    #define width of candlestick elements
    width = .4
    width2 = .05

    #define up and down prices
    up = dataframe[dataframe.c>=dataframe.o]
    down = dataframe[dataframe.c<dataframe.o]

    #define colors to use
    col1 = 'green'
    col2 = 'red'


    #plot up prices
    ax.bar(pd.to_datetime(up.date),up.c-up.o,width,bottom=up.o,color=col1)
    ax.bar(pd.to_datetime(up.date),up.h-up.c,width2,bottom=up.c,color=col1)
    ax.bar(pd.to_datetime(up.date),up.l-up.o,width2,bottom=up.o,color=col1)


    #plot down prices
    ax.bar(pd.to_datetime(down.date),down.c-down.o,width,bottom=down.o,color=col2)
    ax.bar(pd.to_datetime(down.date),down.h-down.o,width2,bottom=down.o,color=col2)
    ax.bar(pd.to_datetime(down.date),down.l-down.c,width2,bottom=down.c,color=col2)

    #rotate x-axis tick labels
    plt.xticks(rotation=45, ha='right')


    plt.title(f'Gráfico de velas de {ticker_visualizado}') # escribe titulo
    plt.xlabel("Fecha") # agrega titulo a eje x
    plt.ylabel("Precio")
    ax.set_facecolor("#161414")
    plt.grid(axis = 'y' ,color='#453F3F',linestyle='--')

    #display candlestick chart
    return fig #plt.show()

#endregion


#region Misc
def check_dates(ticker_check: str, start_date_check, end_date_check):
    
    min_date_query, max_date_query = query_dates(ticker_check)

    check_min_date = min_date_query <= str(start_date_check) <= max_date_query # chequea si la fecha inicial que pide usuario está dentro del rango de las fechas presentes en la base
    check_max_date = min_date_query <= str(end_date_check) <= max_date_query   # chequea si la fecha final que pide usuario está dentro del rango de las fechas presentes en la base

    if check_min_date and check_max_date:
        #devuelve True para el primer return, indicando que las fechas ya estan presentes en la base
        return True, start_date_check, end_date_check

    elif not check_min_date and check_max_date: # si NO esta la fecha de inicio, pero sí esta la fecha de fin
        #hacer un request a la API desde la fecha de inicio solicitada hasta la fecha minima que se encuentra en la base

        return_min_date = start_date_check
        return_max_date = min_date_query

        return False, return_min_date, return_max_date

    elif check_min_date and not check_max_date: # si NO esta la fecha de fin, pero sí esta la fecha de inicio
        #hacer un request a la API desde la fecha maxima de la base hasta la fecha de fin solicitada

        return_min_date = max_date_query
        return_max_date = end_date_check

        return False, return_min_date, return_max_date
    
    else:
        #hacer una request a la API desde fecha inicio hasta fecha de fin
        return_min_date = start_date_check
        return_max_date = end_date_check

        return False, return_min_date, return_max_date


def get_stock_prices(ticker: str,start_date,end_date,key_polygon: str):
    '''
    Trae los precios de la accion solicitada, entre las fechas especificadas
    
    ticker: el nombre abreviado de la accion a consultar, por ejemplo: 'AAPL'
    start_date: fecha inicial de la consulta, en formato YYYY-MM-DD
    end_date: fecha final de la consulta, en formato YYYY-MM-DD
    key_polygon: key que permite usar la api
    '''
    
    _ , l_tickers = check_tickers()

    if ticker in l_tickers:

        bool_dates, start_date_actual, end_date_actual = check_dates(ticker,start_date,end_date)

        if bool_dates:
            return 0, 0, True

        else:
            req = requests.get(f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date_actual}/{end_date_actual}', params = {'apiKey': key_polygon}) #request del tipo get para traer los datos
            query_count = req.json()['queryCount']
            return req.json(), query_count, False # devuelve el json del request realizado y la cantidad de queries que devolvió la api, para verificar que existan datos

    else:
        req = requests.get(f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}', params = {'apiKey': key_polygon}) #request del tipo get para traer los datos
        query_count = req.json()['queryCount']
        return req.json(), query_count, False # devuelve el json del request realizado y la cantidad de queries que devolvió la api, para verificar que existan datos


def clean_request(req_dictionary: dict):

    '''
    Recibe un diccionario (del .json resultado del request) y devuelve un dataframe con solo tres columnas:
    ticker: el nombre del ticker de la accion
    c: el precio de cierre de la accion
    date: la fecha de cada registro
    '''
    
    df_req = pd.DataFrame.from_dict(req_dictionary['results']) # transforma de diccionario a dataframe
    
    df_req['ticker'] = req_dictionary['ticker'] #agrega el ticker como una columna al dataframe
    
    df_req['date'] = pd.to_datetime(df_req.t, unit="ms").dt.date #convierte la fecha de milisegundos a formato fecha

    df_final = df_req.drop(['v','n','vw','t'], axis=1) #quita la columnas no usadas, en futuras versiones se planea usar algunas de las columnas dropeadas para visualizar en graficos mas complejos

    return df_final # devuelve un dataframe con los datos en forma de tabla


def clean_dataframe(dataframe: pd.DataFrame):
    '''
    se usa para imprimir el dataframe en una tabla más "limpia" que solo muestre precio y fecha
    '''

    df_clean = dataframe.drop(['ticker'], axis=1).rename(columns={'date':'Fecha','c':'Precio'}) # elimina la columna ticker y ademas renombra date a Fecha y c a Precio
    print(df_clean) # imprime el dataframe transformado

def date_range_allowed():
    '''
    Función que devuelve el rango de fechas permitido por la API de Polygon, para limitar la seleción de fechas que puede ingresar
    el usuario
    '''

    today = date.today()
    date_min = today - timedelta(days= 365 * 2) # el limite de fecha minima de polygon para cuenta gratis es 2 años
    date_max = today - timedelta(days=1)        # el limite de fecha maxima de polygon para cuenta gratis es hasta el dia anterior

    return date_min, date_max
#endregion