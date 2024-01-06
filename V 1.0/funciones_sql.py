import sqlite3
import pandas as pd
import os

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

def temp_table(dataframe):
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

def append_entries(dataframe):

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
            DISTINCT(ticker), 
            MIN(date) as fecha_inicial, 
            MAX  (date) as fecha_final
            FROM stock_data
            GROUP BY ticker
            ORDER BY ticker ASC
            '''


    print('Los tickers guardados en la base de datos son:\n')
    print(pd.read_sql(query,con)) # imprime la tabla creade de la consulta

    con.close()

def query_ticker_close(ticker):

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

def query_ticker_all(ticker):

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