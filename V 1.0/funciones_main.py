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
    query_count = req.json()['queryCount']

    return req.json(), query_count # devuelve el json del request realizado y la cantidad de queries que devolvió la api, para verificar que existan datos

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

    df_final = df_req.drop(['v','n','vw','t'], axis=1) #quita la columnas no usadas, en futuras versiones se planea usar algunas de las columnas dropeadas para visualizar en graficos mas complejos

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

def candlestick_plot(dataframe,ticker_visualizado):
    '''
    Recibe un dataframe de pandas y devuelve un gráfico tipo velas con las fechas y el precio de cierre, apertura, maximo y minimo
    de la accion
    Tambien recibe el nombre del ticker para incluir en el titulo del gráfico
    '''

    #create figure
    plt.figure()

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
    plt.bar(pd.to_datetime(up.date),up.c-up.o,width,bottom=up.o,color=col1)
    plt.bar(pd.to_datetime(up.date),up.h-up.c,width2,bottom=up.c,color=col1)
    plt.bar(pd.to_datetime(up.date),up.l-up.o,width2,bottom=up.o,color=col1)


    #plot down prices
    plt.bar(pd.to_datetime(down.date),down.c-down.o,width,bottom=down.o,color=col2)
    plt.bar(pd.to_datetime(down.date),down.h-down.o,width2,bottom=down.o,color=col2)
    plt.bar(pd.to_datetime(down.date),down.l-down.c,width2,bottom=down.c,color=col2)

    #rotate x-axis tick labels
    plt.xticks(rotation=45, ha='right')


    #plt.title(f'Gráfico de velas de {ticker_visualizado}') # escribe titulo

    #display candlestick chart
    plt.show()


def clean_dataframe(dataframe):
    '''
    se usa para imprimir el dataframe en una tabla más "limpia" que solo muestre precio y fecha
    '''

    df_clean = dataframe.drop(['ticker'], axis=1).rename(columns={'date':'Fecha','c':'Precio'}) # elimina la columna ticker y ademas renombra date a Fecha y c a Precio
    print(df_clean) # imprime el dataframe transformado