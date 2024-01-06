import streamlit as st
import funciones_app as f_module

key_api = 'HOzRroodgM7p6haWXE4GSZgtn5jhzZC2'

f_module.create_database()

hay_tickers, l_tickers = f_module.check_tickers()

date_min_allowed, date_max_allowed = f_module.date_range_allowed()

'''
## :chart_with_upwards_trend: Buscador de Información Financiera :chart_with_downwards_trend:

Esta aplicación permite solicitar datos de cualquier acción del mercado estadounidense y guardarla en una base de datos.

Además permite visualizar la información de los datos solicitados en forma de tabla o en forma gráfica.

Para usar las funciones de la aplicación, expanda alguna de las secciones siguientes.
'''
'\n'

#region pedir datos
with st.expander("# Pedir Datos 🔎", expanded=False):
    '''
    Ingrese el ticker de la acción que quiere consultar y el rango de fechas que se necesita 
    y luego presion el boton "Pedir Datos".
    '''
    
    tick = st.text_input('Ticker :dollar:', "",key='tick_b')
    
    desde = st.date_input(
                    'Desde :date:',
                    value=date_max_allowed,
                    key='desde',
                    min_value=date_min_allowed,
                    max_value=date_max_allowed
                    ) #
    
    hasta = st.date_input(
                    'Hasta :date:',
                    value=date_max_allowed,
                    key='hasta',
                    min_value=date_min_allowed,
                    max_value=date_max_allowed
                    ) #

    if st.button("Pedir Datos"):
        
        

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
#endregion

'\n'
'\n'


#region tabular datos
with st.expander("Ver tabla :page_facing_up:", expanded=False):

    '''
    Seleccione el ticker de la acción que quiere consultar para ver en formato de tabla todos los datos existentes en la base
    '''

    if not hay_tickers:
        '''
        Aún no existen tickers en la base de datos. Para agregar datos a la base use la sección de "Pedir Datos".
        '''
    
    tick_t = st.selectbox(
    'Ticker',
    l_tickers, #la lista de los tickers presentes en la base
    key = 'dd_tabla'
    )

    if st.button("Tabular Datos", key='b_tabular', disabled = not hay_tickers):
        
        
        df_t = f_module.query_ticker_all_viz(tick_t)
        
        f'Los datos tabulados de {tick_t} son'
        st.dataframe(
            df_t,
            hide_index=True,
            column_config = {"Precio Cierre": st.column_config.NumberColumn(format="$ %.2f"),
                             "Precio Apertura": st.column_config.NumberColumn(format="$ %.2f"),
                             "Precio Máximo": st.column_config.NumberColumn(format="$ %.2f"),
                             "Precio Mínimo": st.column_config.NumberColumn(format="$ %.2f")
                            }
            )
#endregion

'\n'
'\n'

#region graficar datos
with st.expander("Visualizar :bar_chart:", expanded=False):
    
    '''
    Seleccione el ticker de la acción que quiere consultar y el tipo de gráfico que quiere ver para visualizar los datos.
    '''

    if not hay_tickers:
        '''
        Aún no existen tickers en la base de datos. Para agregar datos a la base use la sección de "Pedir Datos".
        '''

    tick_v = st.selectbox(
    label = 'Ticker',
    options = l_tickers, #la lista de los tickers presentes en la base
    key = 'dd_graf'
    )
    
    tipo_graf = st.selectbox(
    '¿Qué tipo de gráfico?',
    ('Lineas', 'Velas'),
    disabled = not hay_tickers
    ).lower()


    if st.button("Visualizar datos",key="b_viz", disabled = not hay_tickers):
        
        if tipo_graf == "lineas":
            df_v = f_module.query_ticker_close(tick_v)
            st.pyplot(f_module.visualize_df(df_v,tick_v))
        else:
            df_viz = f_module.query_ticker_all(tick_v) # si existe, se grafican los datos presentes en la base de datos
            st.pyplot(f_module.candlestick_plot(df_viz,tick_v))
#endregion

#region resumen

if hay_tickers:
    st.sidebar.write(
    '''
    Tickers presentes en la base de datos y rango de fechas disponible para cada uno:
    '''
    )

    df_res = f_module.print_summary()
    st.sidebar.dataframe(df_res,hide_index=True)
else:
    st.sidebar.write(
    '''
    Aún no existen tickers en la base de datos. Para agregar datos a la base use la sección de "Pedir Datos".
    '''
    )
#endregion


'\n'
'\n'
'\n'
'\n'

'''
Código disponible en el repo de github: https://github.com/MartinPiccinini/TPFinal_ITBA_Piccinini.git
'''