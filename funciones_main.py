import requests
import pandas as pd
import matplotlib.pyplot as plt

def get_stock_prices(ticker,start_date,end_date,key_polygon):
    '''
    Trae los precios de la accion solicitada, entre las fechas especificadas
    
    ticker: el nombre abreviado de la accion a consultar, por ejemplo: 'AAPL'
    start_date: fecha inicial de la consulta, en formato YYYY-MM-DD
    end_date: fecha final de la consulta, en formato YYYY-MM-DD
    key_plygon: key que permite usar la api
    '''
    req = requests.get(f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}', params = {'apiKey': key_polygon}) #request del tipo get para traer los datos

    return req.json() # devuelve el json del request realizado

def clean_request(req_dictionary):

    '''
    Recibe un diccionario (del .json resultado del request) y devuelve un dataframe con solo tres columnas:
    ticker: el nombre del ticker de la accion
    c: el precio de cierre de la accion
    date: la fecha de cada registro
    '''
    
    df_req = pd.DataFrame.from_dict(req_dictionary['results']) # transforma de diccionario a dataframe
    
    df_req['ticker'] = req_dictionary['ticker'] #agrega el ticker como una columna al dataframe
    
    df_req['date'] = pd.to_datetime(df_req.t, unit="ms").dt.date #convierte la fecha de milisegundos a formato fecha

    df_final = df_req.drop(['v','n','vw','o','h','l','t'], axis=1) #quita la columnas no usadas, en futuras versiones se planea usar algunas de las columnas dropeadas para visualizar en graficos mas complejos

    return df_final # devuelve un dataframe con los datos en forma de tabla

def visualize_df(dataframe,ticker_visualizado):
    '''
    Recibe un dataframe de pandas y devuelve un gráfico de linas con las fechas y el precio de venta de la accion
    Tambien recibe el nombre del ticker para incluir en el titulo del gráfico
    '''

    plt.xticks(rotation=45) # rota 45 grados los ticker del eje x
    plt.plot(dataframe.Fecha,dataframe.Precio) # grafica con evolutivo
    plt.title(f'Gráfico evolutivo de {ticker_visualizado}') # escribe titulo
    plt.xlabel("Fecha") # agrega titulo a eje x
    plt.ylabel("Precio") # agrega titulo a eje y
    plt.show() # linea para que se visualice el grafico al correr el programa


def clean_dataframe(dataframe):
    '''
    se usa para imprimir el dataframe en una tabla más "limpia" que solo muestre precio y fecha
    '''

    df_clean = dataframe.drop(['ticker'], axis=1).rename(columns={'date':'Fecha','c':'Precio'}) # elimina la columna ticker y ademas renombra date a Fecha y c a Precio
    print(df_clean) # imprime el dataframe transformado